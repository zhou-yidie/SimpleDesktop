package com.google.android.accessibility.selecttospeak

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.accessibilityservice.GestureDescription.StrokeDescription
import android.graphics.Path
import android.graphics.Rect
import android.os.Bundle
import android.util.Log
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import tech.huangsh.onetap.service.wechat.WeChatActivity
import tech.huangsh.onetap.service.wechat.WeChatData
import tech.huangsh.onetap.service.wechat.WeChatId

class SelectToSpeakService : AccessibilityService() {

    private val tag: String = "WechatAccessibilityTag"

    override fun onInterrupt() {
        WeChatData.updateIndex(0)
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        val packageName = event?.packageName?.toString() ?: ""
        if (packageName != "com.tencent.mm") return

        val currentActivity = event?.className ?: ""
        Log.d(tag, "Event: ${event?.eventType}, Class: $currentActivity, Index: ${WeChatData.index}")

        if (WeChatData.index == 1) {
            if (currentActivity == WeChatActivity.INDEX.id) {
                var tables =
                    rootInActiveWindow.findAccessibilityNodeInfosByViewId(WeChatId.TABLES.id)
                Log.d(tag, "发现底部 Tab: ${tables?.size ?: 0} 个")
                if (!tables.isNullOrEmpty()) {
                    val clicked = tables[0].click()
                    Log.d(tag, "点击第一个 Tab 结果: $clicked")
                    WeChatData.updateIndex(2)
                }
            } else if (currentActivity.contains("dialog")) {
                performGlobalAction(GLOBAL_ACTION_BACK)
                Thread.sleep(500)
                performGlobalAction(GLOBAL_ACTION_BACK)
                Thread.sleep(500)
            } else {
                performGlobalAction(GLOBAL_ACTION_BACK)
                Thread.sleep(500)
            }
        }

        if (WeChatData.index == 2) {
            Log.d(tag, "执行 Index 2: 点击搜索图标")
            val searchIcon = rootInActiveWindow.findAccessibilityNodeInfosByViewId(WeChatId.SEARCH.id)
            if (searchIcon.isNotEmpty()) {
                val clicked = searchIcon.first().click()
                Log.d(tag, "点击搜索图标结果: $clicked")
                Thread.sleep(500)
                WeChatData.updateIndex(3)
            }
        }

        if (WeChatData.index == 3) {
            Log.d(tag, "执行 Index 3: 输入联系人姓名 ${WeChatData.value}")
            val input = rootInActiveWindow.findAccessibilityNodeInfosByViewId(WeChatId.INPUT.id)
            if (input.isNotEmpty()) {
                val inputted = input.first().input(WeChatData.value)
                Log.d(tag, "输入文字结果: $inputted")
                Thread.sleep(1000)
                WeChatData.updateIndex(4)
            }
        }

        if (WeChatData.index == 4) {
            Log.d(tag, "执行 Index 4: 点击列表第一个联系人, 文本: ${WeChatData.value}")
            var contacts = rootInActiveWindow.findAccessibilityNodeInfosByViewId(WeChatId.LIST.id)
            if (contacts.isNullOrEmpty()) {
                Log.d(tag, "ID 找不到，尝试文本查找: ${WeChatData.value}")
                contacts = rootInActiveWindow.findAccessibilityNodeInfosByText(WeChatData.value)
            }

            if (!contacts.isNullOrEmpty()) {
                val clicked = contacts.first().click()
                Log.d(tag, "点击联系人结果: $clicked")
                Thread.sleep(500)
                WeChatData.updateIndex(5)
            }
        }

        if (WeChatData.index == 5) {
            Log.d(tag, "执行 Index 5: 聊天界面点击更多")
            val more = rootInActiveWindow.findAccessibilityNodeInfosByViewId(WeChatId.MORE.id)
            if (more.isNotEmpty()) {
                val clicked = more.first().click()
                Log.d(tag, "点击更多结果: $clicked")
                Thread.sleep(1000)
                WeChatData.updateIndex(6)
            }
        }

        if (WeChatData.index == 6) {
            Log.d(tag, "执行 Index 6: 点击视频通话菜单")
            val menu = rootInActiveWindow.findAccessibilityNodeInfosByText(WeChatData.findText(false))
            if (menu.isNotEmpty()) {
                val rect = Rect()
                menu.first().getBoundsInScreen(rect)
                Log.d(tag, "执行坐标点击: ${rect.centerX()}, ${rect.centerY()}")
                performClick(rect.exactCenterX(), rect.exactCenterY())
                Thread.sleep(500)
                WeChatData.updateIndex(7)
            }
        }

        if (WeChatData.index == 7) {
            Log.d(tag, "执行 Index 7: 选择视频/语音通话")
            val options = rootInActiveWindow.findAccessibilityNodeInfosByText(WeChatData.findText(true))
            if (options.isNotEmpty()) {
                val clicked = options.first().click()
                Log.d(tag, "点击确定结果: $clicked")
                Thread.sleep(500)
                WeChatData.updateIndex(0)
            }
        }
    }

    private fun AccessibilityNodeInfo?.click(): Boolean {
        this ?: return false
        return if (isClickable) {
            performAction(AccessibilityNodeInfo.ACTION_CLICK)
        } else {
            parent?.click() == true
        }
    }

    private fun AccessibilityNodeInfo?.input(text: String): Boolean {
        this ?: return false
        return if (isEditable) {
            val arguments: Bundle = Bundle()
            arguments.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text)
            performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, arguments)
        } else {
            parent?.input(text) == true
        }
    }

    private fun performClick(x: Float, y: Float) {
        val gestureBuilder = GestureDescription.Builder()
        val path = Path()
        path.moveTo(x, y)
        gestureBuilder.addStroke(StrokeDescription(path, 0, 1))
        val gestureDescription = gestureBuilder.build()
        dispatchGesture(gestureDescription, null, null)
    }
}