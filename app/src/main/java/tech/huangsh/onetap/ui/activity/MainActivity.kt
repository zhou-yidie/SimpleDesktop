package tech.huangsh.onetap.ui.activity

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.view.KeyEvent
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.lifecycleScope
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import tech.huangsh.onetap.data.model.Settings as AppSettings
import tech.huangsh.onetap.service.WifiMonitorService
import tech.huangsh.onetap.ui.screens.components.NoWifiDialog
import tech.huangsh.onetap.ui.screens.home.HomeScreen
import tech.huangsh.onetap.ui.theme.SimpleDesktopTheme
import tech.huangsh.onetap.utils.LauncherUtils
import tech.huangsh.onetap.utils.VoiceAssistant
import tech.huangsh.onetap.viewmodel.MainViewModel
import tech.huangsh.onetap.viewmodel.SettingsViewModel

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    private val viewModel: MainViewModel by viewModels()
    private val settingsViewModel: SettingsViewModel by viewModels()
    
    // WiFi弹窗状态
    private var showNoWifiDialog = mutableStateOf(false)
    
    // 语音助手（用于WiFi断网播报）
    private var voiceAssistant: VoiceAssistant? = null
    
    // WiFi监控广播接收器
    private val wifiReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            when (intent?.action) {
                WifiMonitorService.ACTION_WIFI_DISCONNECTED -> {
                    // 20秒超时，WiFi仍未连接
                    showNoWifiDialog.value = true
                    // 语音播报（仅一次）
                    voiceAssistant?.speak("当前没有可用WiFi网络，请寻找合适的网络")
                }
                WifiMonitorService.ACTION_WIFI_CONNECTED -> {
                    // WiFi已恢复连接，自动关闭弹窗
                    showNoWifiDialog.value = false
                }
                WifiMonitorService.ACTION_WIFI_DISABLED -> {
                    // WiFi被关闭（Android 10+），引导用户手动打开
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                        try {
                            val panelIntent = Intent(Settings.Panel.ACTION_WIFI)
                            startActivity(panelIntent)
                        } catch (e: Exception) {
                            // 如果Panel不可用，跳转到WiFi设置
                            val wifiIntent = Intent(Settings.ACTION_WIFI_SETTINGS)
                            startActivity(wifiIntent)
                        }
                    }
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        // 初始化语音助手
        voiceAssistant = VoiceAssistant(this)
        
        // 检查是否首次启动
        checkFirstLaunch()
        
        // 检查并更新默认启动器状态
        updateLauncherStatus()
        
        // 根据设置启动WiFi监控服务
        startWifiMonitorIfEnabled()
        
        setContent {
            val settings by settingsViewModel.settings.collectAsState(initial = AppSettings())
            val showDialog by showNoWifiDialog
            
            SimpleDesktopTheme(
                darkTheme = false,
                highContrast = settings.highContrast,
                fontSize = settings.fontSize,
                themeMode = settings.themeMode
            ) {
                HomeScreen(viewModel)
                
                // 无WiFi网络弹窗
                if (showDialog) {
                    NoWifiDialog(
                        onDismiss = { showNoWifiDialog.value = false }
                    )
                }
            }
        }
    }
    
    override fun onResume() {
        super.onResume()
        // 每次恢复时检查启动器状态
        updateLauncherStatus()
    }
    
    override fun onStart() {
        super.onStart()
        // 注册WiFi监控广播接收器
        val filter = IntentFilter().apply {
            addAction(WifiMonitorService.ACTION_WIFI_DISCONNECTED)
            addAction(WifiMonitorService.ACTION_WIFI_CONNECTED)
            addAction(WifiMonitorService.ACTION_WIFI_DISABLED)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(wifiReceiver, filter, RECEIVER_NOT_EXPORTED)
        } else {
            registerReceiver(wifiReceiver, filter)
        }
    }
    
    override fun onStop() {
        super.onStop()
        try {
            unregisterReceiver(wifiReceiver)
        } catch (_: Exception) { }
    }
    
    override fun onDestroy() {
        super.onDestroy()
        voiceAssistant?.shutdown()
    }
    
    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        // 处理Home键和返回键，确保启动器行为正确
        return when (keyCode) {
            KeyEvent.KEYCODE_HOME -> {
                // 如果是默认启动器，不做任何处理，保持在当前界面
                if (LauncherUtils.isDefaultLauncher(this)) {
                    true
                } else {
                    super.onKeyDown(keyCode, event)
                }
            }
            KeyEvent.KEYCODE_BACK -> {
                // 如果是默认启动器，返回键也不退出应用
                if (LauncherUtils.isDefaultLauncher(this)) {
                    true
                } else {
                    super.onKeyDown(keyCode, event)
                }
            }
            else -> super.onKeyDown(keyCode, event)
        }
    }
    
    /**
     * 检查是否首次启动
     */
    private fun checkFirstLaunch() {
        lifecycleScope.launch {
            val settings = settingsViewModel.settings.first()
            if (settings.isFirstLaunch) {
                // 跳转到引导页
                val intent = Intent(this@MainActivity, OnboardingActivity::class.java)
                intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
                startActivity(intent)
                finish()
            }
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
    
    /**
     * 根据设置启动WiFi监控服务
     */
    private fun startWifiMonitorIfEnabled() {
        lifecycleScope.launch {
            val settings = settingsViewModel.settings.first()
            if (settings.isWifiMonitorEnabled) {
                WifiMonitorService.start(this@MainActivity)
            }
        }
    }
}