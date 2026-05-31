package tech.huangsh.onetap.ui.activity

import android.app.role.RoleManager
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts

/**
 * 桌面选择器Activity (透明中转站)
 * 专门用于向系统请求 "默认桌面" 角色 (ROLE_HOME) 或显示选择器弹窗。
 */
class LauncherChooserActivity : ComponentActivity() {

    // 注册返回结果监听器（虽然目前我们不在乎结果，但RoleManager需要用它启动）
    private val roleRequestLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        // 不管用户点了接受还是拒绝，弹窗结束我们就关掉这个透明Activity
        finish()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        triggerLauncherChooser()
    }

    private fun triggerLauncherChooser() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                // Android 10及以上：必定弹出系统级的桌面选择授权框
                val roleManager = getSystemService(RoleManager::class.java)
                if (roleManager != null && roleManager.isRoleAvailable(RoleManager.ROLE_HOME)) {
                    if (!roleManager.isRoleHeld(RoleManager.ROLE_HOME)) {
                        val intent = roleManager.createRequestRoleIntent(RoleManager.ROLE_HOME)
                        roleRequestLauncher.launch(intent)
                        return // 启动后等待回调，不走到后面的兼容逻辑
                    } else {
                        Toast.makeText(this, "已经是默认桌面了！", Toast.LENGTH_SHORT).show()
                        finish()
                        return
                    }
                }
            }

            // Android 10 以下或 RoleManager 获取失败的兜底策略
            fallbackToHomeIntent()

        } catch (e: Exception) {
            e.printStackTrace()
            fallbackToHomeIntent()
        }
    }

    private fun fallbackToHomeIntent() {
        try {
            // 发送 HOME Intent 并强制系统展示选择器
            val homeIntent = Intent(Intent.ACTION_MAIN).apply {
                addCategory(Intent.CATEGORY_HOME)
                flags = Intent.FLAG_ACTIVITY_NEW_TASK
            }
            // 使用 createChooser 更容易强迫不同厂商弹出列表
            val chooser = Intent.createChooser(homeIntent, "请选择桌面应用")
            startActivity(chooser)
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "拉起设置失败，系统限制", Toast.LENGTH_SHORT).show()
        } finally {
            finish()
        }
    }
}
