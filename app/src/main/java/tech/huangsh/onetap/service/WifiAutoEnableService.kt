package tech.huangsh.onetap.service

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.graphics.Path
import android.graphics.Rect
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo

/**
 * 自动开启 WiFi 的无障碍服务
 * 
 * 用于在 Android 10+ 手机上自动点击设置页面的 WiFi 开关。
 */
class WifiAutoEnableService : AccessibilityService() {

    companion object {
        private const val TAG = "WifiAutoEnableService"
        
        // 用于标识是否是我们自己发起的开启WiFi请求
        var isAutoEnabling = false
    }

    private val handler = Handler(Looper.getMainLooper())
    
    // 重试计数器
    private var retryCount = 0
    private val maxRetries = 5
    
    // 是否已经成功处理
    private var hasSucceeded = false

    override fun onAccessibilityEvent(event: AccessibilityEvent) {
        // 如果不是我们主动请求开启WiFi，或者已经成功了，直接跳过
        if (!isAutoEnabling || hasSucceeded) return

        if (event.eventType == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED || 
            event.eventType == AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED) {
            
            val packageName = event.packageName?.toString() ?: ""
            
            // 检查当前是不是设置页面
            val isSettingsPage = packageName.contains("settings", ignoreCase = true)
                    || packageName.contains("coloros", ignoreCase = true)
                    || packageName.contains("oplus", ignoreCase = true)
                    || packageName.contains("oppo", ignoreCase = true)
                    || packageName.contains("oneplus", ignoreCase = true)

            if (isSettingsPage) {
                Log.d(TAG, "检测到设置页面(包名: $packageName), 重试次数: $retryCount")
                
                // 延迟一点再操作，给页面加载时间
                handler.removeCallbacksAndMessages(null)
                handler.postDelayed({
                    attemptClickWifiSwitch()
                }, 500)
            }
        }
    }
    
    /**
     * 尝试点击WiFi开关（带重试逻辑）
     */
    private fun attemptClickWifiSwitch() {
        if (!isAutoEnabling || hasSucceeded) return
        
        val rootNode = rootInActiveWindow
        if (rootNode == null) {
            Log.w(TAG, "rootInActiveWindow 为 null，等待重试...")
            scheduleRetry()
            return
        }
        
        // 打印 UI 树（仅首次）
        if (retryCount == 0) {
            dumpNodeTree(rootNode, 0)
        }
        
        // 尝试节点点击策略
        val success = findAndClickWifiSwitch(rootNode)
        
        if (success) {
            onSwitchClicked()
        } else {
            retryCount++
            Log.w(TAG, "节点点击策略失败, 已重试 $retryCount 次")
            
            if (retryCount >= maxRetries) {
                // 达到最大重试次数，使用手势兜底
                Log.w(TAG, "达到最大重试次数，使用手势点击！")
                val switchNode = findWlanTextNode(rootNode)
                if (switchNode != null) {
                    tapNodeByGesture(switchNode)
                } else {
                    val dm = resources.displayMetrics
                    val x = dm.widthPixels * 0.85f
                    val y = dm.heightPixels * 0.13f
                    tapScreen(x, y)
                }
            } else {
                scheduleRetry()
            }
        }
    }
    
    /**
     * 安排一次重试
     */
    private fun scheduleRetry() {
        handler.postDelayed({
            attemptClickWifiSwitch()
        }, 800)
    }
    
    /**
     * 开关点击成功后的清理
     */
    private fun onSwitchClicked() {
        hasSucceeded = true
        Log.d(TAG, "WiFi开关已点击成功，准备返回上一页")
        
        handler.postDelayed({
            // 使用 HOME 键直接返回桌面（比 BACK 键更可靠，不受设置页面层级影响）
            performGlobalAction(GLOBAL_ACTION_HOME)
            handler.postDelayed({
                resetState()
            }, 500)
        }, 500)
    }
    
    /**
     * 重置所有状态，准备下一次使用
     */
    private fun resetState() {
        isAutoEnabling = false
        hasSucceeded = false
        retryCount = 0
        handler.removeCallbacksAndMessages(null)
    }

    /**
     * 递归遍历UI树，寻找并点击WiFi开关
     * 适配多种手机厂商（小米、华为、OPPO、vivo等）的自定义控件
     * @return 是否成功点击了开关
     */
    private fun findAndClickWifiSwitch(node: AccessibilityNodeInfo?): Boolean {
        if (node == null) return false

        // 先尝试精准策略
        if (tryPreciseClick(node)) return true

        // 精准策略未命中，使用暴力策略：在WLAN页面找到任何看起来像开关的东西
        return tryBruteForceClick(node)
    }

    /**
     * 精准策略：递归查找开关类控件
     */
    private fun tryPreciseClick(node: AccessibilityNodeInfo?): Boolean {
        if (node == null) return false

        val className = node.className?.toString()?.lowercase() ?: ""

        // 判断是否是"开关类"控件（覆盖各厂商自定义类名）
        val isSwitchLike = className.contains("switch")
                || className.contains("toggle")
                || className.contains("checkbox")
                || node.isCheckable

        if (isSwitchLike) {
            Log.d(TAG, "找到开关类控件: class=$className, checked=${node.isChecked}, text=${node.text}")
            if (!node.isChecked) {
                Log.d(TAG, "尝试直接点击开关...")
                val clicked = node.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                if (clicked) {
                    Log.d(TAG, "直接点击开关成功！")
                    return true
                }
                // 如果直接点击失败，尝试点击父容器
                Log.d(TAG, "直接点击失败，尝试点击父容器...")
                return tryClickParent(node)
            } else {
                Log.d(TAG, "开关已经是开启状态，任务完成。")
                return true
            }
        }

        // 递归遍历子节点
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            if (tryPreciseClick(child)) return true
        }

        return false
    }

    /**
     * 暴力策略：在页面上查找包含 WLAN/WiFi 文字且可点击的元素
     */
    private fun tryBruteForceClick(node: AccessibilityNodeInfo?): Boolean {
        if (node == null) return false

        val text = node.text?.toString()?.lowercase() ?: ""
        val desc = node.contentDescription?.toString()?.lowercase() ?: ""
        val combined = "$text $desc"

        val isWifiRelated = combined.contains("wlan") || combined.contains("wi-fi") || combined.contains("wifi")

        if (isWifiRelated) {
            Log.d(TAG, "暴力策略-找到WiFi相关元素: text='${node.text}', class=${node.className}, clickable=${node.isClickable}, checkable=${node.isCheckable}")

            // 情况A: 这个元素本身就可点击或可选中
            if (node.isClickable || node.isCheckable) {
                if (node.isCheckable && node.isChecked) {
                    Log.d(TAG, "已经是开启状态了。")
                    return true
                }
                Log.d(TAG, "暴力策略-执行点击！")
                val clicked = node.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                if (clicked) return true
            }

            // 情况B: 尝试点击父容器
            if (tryClickParent(node)) return true
        }

        // 递归
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            if (tryBruteForceClick(child)) return true
        }

        return false
    }

    /**
     * 向上查找第一个可点击的父容器并执行点击
     */
    private fun tryClickParent(node: AccessibilityNodeInfo): Boolean {
        var current = node.parent
        var depth = 0
        while (current != null && depth < 5) {
            if (current.isClickable) {
                Log.d(TAG, "点击父容器: class=${current.className}, depth=$depth")
                val clicked = current.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                if (clicked) {
                    Log.d(TAG, "父容器点击成功！")
                    return true
                }
            }
            current = current.parent
            depth++
        }
        return false
    }

    override fun onInterrupt() {
        Log.e(TAG, "服务被中断")
        resetState()
    }

    /**
     * 打印完整的 UI 节点树（调试用）
     */
    private fun dumpNodeTree(node: AccessibilityNodeInfo?, depth: Int) {
        if (node == null) return
        val indent = "  ".repeat(depth)
        Log.d(TAG, "${indent}[${node.className}] text='${node.text}' desc='${node.contentDescription}' " +
                "clickable=${node.isClickable} checkable=${node.isCheckable} checked=${node.isChecked} " +
                "enabled=${node.isEnabled}")
        for (i in 0 until node.childCount) {
            dumpNodeTree(node.getChild(i), depth + 1)
        }
    }

    /**
     * 查找包含 WLAN/WiFi 文字的节点（用于确定手势点击位置）
     */
    private fun findWlanTextNode(node: AccessibilityNodeInfo?): AccessibilityNodeInfo? {
        if (node == null) return null

        val text = node.text?.toString()?.lowercase() ?: ""
        val desc = node.contentDescription?.toString()?.lowercase() ?: ""
        if (text.contains("wlan") || text.contains("wi-fi") || text.contains("wifi")
            || desc.contains("wlan") || desc.contains("wi-fi") || desc.contains("wifi")) {
            return node
        }

        for (i in 0 until node.childCount) {
            val result = findWlanTextNode(node.getChild(i))
            if (result != null) return result
        }
        return null
    }

    /**
     * 通过手势在节点右侧的开关位置模拟点击
     */
    private fun tapNodeByGesture(node: AccessibilityNodeInfo) {
        val rect = Rect()
        node.getBoundsInScreen(rect)

        // 开关通常在文字行的右边
        val x = resources.displayMetrics.widthPixels * 0.85f
        val y = rect.centerY().toFloat()

        Log.d(TAG, "手势点击开关: x=$x, y=$y (节点范围: $rect)")
        tapScreen(x, y)
    }

    /**
     * 在屏幕指定坐标模拟点击
     */
    private fun tapScreen(x: Float, y: Float) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.N) {
            Log.w(TAG, "手势点击需要 Android 7.0+")
            return
        }

        val path = Path()
        path.moveTo(x, y)
        val gesture = GestureDescription.Builder()
            .addStroke(GestureDescription.StrokeDescription(path, 0, 100))
            .build()

        dispatchGesture(gesture, object : GestureResultCallback() {
            override fun onCompleted(gestureDescription: GestureDescription?) {
                Log.d(TAG, "手势点击成功！坐标: ($x, $y)")
                onSwitchClicked()
            }
            override fun onCancelled(gestureDescription: GestureDescription?) {
                Log.w(TAG, "手势点击被取消")
            }
        }, null)
    }
}
