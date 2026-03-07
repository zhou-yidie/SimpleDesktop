package tech.huangsh.onetap.ui.activity

import android.os.Bundle
import android.content.Intent
import android.view.KeyEvent
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.lifecycleScope
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import tech.huangsh.onetap.data.model.Settings
import tech.huangsh.onetap.ui.screens.home.HomeScreen
import tech.huangsh.onetap.ui.screens.onboarding.PermissionOnboardingScreen
import tech.huangsh.onetap.ui.theme.OneTapTheme
import tech.huangsh.onetap.utils.LauncherUtils
import tech.huangsh.onetap.viewmodel.MainViewModel
import tech.huangsh.onetap.viewmodel.SettingsViewModel

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    private val viewModel: MainViewModel by viewModels()
    private val settingsViewModel: SettingsViewModel by viewModels()
    private var allowUserLeave = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        // 检查并更新默认启动器状态
        updateLauncherStatus()
        
        setContent {
            val settings by settingsViewModel.settings.collectAsState(initial = Settings())
            OneTapTheme(
                darkTheme = false,
                highContrast = settings.highContrast,
                fontSize = settings.fontSize,
                themeMode = settings.themeMode
            ) {
                if (settings.onboardingCompleted) {
                    HomeScreen(viewModel)
                } else {
                    PermissionOnboardingScreen(
                        onFinished = { settingsViewModel.markOnboardingCompleted() }
                    )
                }
            }
        }
    }
    
    override fun onResume() {
        super.onResume()
        allowUserLeave = false
        // 每次恢复时检查启动器状态
        updateLauncherStatus()
    }
    
    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        // 处理Home键和返回键，确保启动器行为正确
        return when (keyCode) {
            KeyEvent.KEYCODE_HOME -> {
                // 如果启用了“应用桌面”开关或当前是默认启动器，不做任何处理，保持在当前界面
                if (settingsViewModel.launcherMode.value || LauncherUtils.isDefaultLauncher(this)) {
                    true
                } else {
                    super.onKeyDown(keyCode, event)
                }
            }
            KeyEvent.KEYCODE_BACK -> {
                // 如果启用了“应用桌面”开关或当前是默认启动器，返回键也不退出应用
                if (settingsViewModel.launcherMode.value || LauncherUtils.isDefaultLauncher(this)) {
                    true
                } else {
                    super.onKeyDown(keyCode, event)
                }
            }
            else -> super.onKeyDown(keyCode, event)
        }
    }

    override fun onUserLeaveHint() {
        super.onUserLeaveHint()
        if (allowUserLeave) {
            allowUserLeave = false
            return
        }
        // 当启用了应用桌面模式时，用户尝试通过手势离开（如上滑）时，将应用重新拉回，防止误触退出
        try {
            if (settingsViewModel.launcherMode.value) {
                val intent = Intent(this, MainActivity::class.java).apply {
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_CLEAR_TOP)
                }
                startActivity(intent)
            }
        } catch (e: Exception) {
            // 忽略异常，保持原有行为
        }
    }
    
    /**
     * 更新启动器状态
     */
    private fun updateLauncherStatus() {
        lifecycleScope.launch {
            settingsViewModel.refreshDefaultLauncherStatus()
        }
    }

    override fun startActivity(intent: Intent?) {
        allowUserLeave = true
        super.startActivity(intent)
    }

    override fun startActivity(intent: Intent?, options: Bundle?) {
        allowUserLeave = true
        super.startActivity(intent, options)
    }
}