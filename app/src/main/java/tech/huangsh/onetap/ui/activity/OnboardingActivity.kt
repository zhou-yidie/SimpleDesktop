package tech.huangsh.onetap.ui.activity

import android.Manifest
import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.lifecycleScope
import com.hjq.permissions.OnPermissionCallback
import com.hjq.permissions.XXPermissions
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import tech.huangsh.onetap.data.model.Settings
import tech.huangsh.onetap.data.repository.AppRepository
import tech.huangsh.onetap.ui.screens.onboarding.OnboardingScreen
import tech.huangsh.onetap.ui.screens.settings.PermissionManagementScreen
import tech.huangsh.onetap.ui.theme.OneTapTheme
import tech.huangsh.onetap.utils.LauncherUtils
import tech.huangsh.onetap.viewmodel.SettingsViewModel
import javax.inject.Inject

@AndroidEntryPoint
class OnboardingActivity : ComponentActivity() {
    
    private val settingsViewModel: SettingsViewModel by viewModels()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        setContent {
            val settings by settingsViewModel.settings.collectAsState(initial = Settings())
            OneTapTheme(
                darkTheme = false,
                highContrast = settings.highContrast,
                fontSize = settings.fontSize,
                themeMode = settings.themeMode
            ) {
                OnboardingScreen(
                    onFinish = {
                        // 标记引导完成
                        lifecycleScope.launch {
                            settingsViewModel.updateIsFirstLaunch(false)
                        }
                        
                        // 进入权限管理页面（标记为从引导流程进入）
                        val intent = Intent(this@OnboardingActivity, PermissionSetupActivity::class.java)
                        intent.putExtra("from_onboarding", true)
                        startActivity(intent)
                        finish()
                    }
                )
            }
        }
    }
}

@AndroidEntryPoint
class PermissionSetupActivity : ComponentActivity() {
    
    private val settingsViewModel: SettingsViewModel by viewModels()
    
    @Inject
    lateinit var appRepository: AppRepository
    
    private var hasRequestedPermissions = false
    private var isFromOnboarding = false
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        // 检查是否从引导流程进入（通过 Intent extra 标记）
        isFromOnboarding = intent.getBooleanExtra("from_onboarding", false)
        
        setContent {
            val settings by settingsViewModel.settings.collectAsState(initial = Settings())
            OneTapTheme(
                darkTheme = false,
                highContrast = settings.highContrast,
                fontSize = settings.fontSize,
                themeMode = settings.themeMode
            ) {
                PermissionManagementScreen(
                    onBack = {
                        if (isFromOnboarding) {
                            // 如果是从引导流程进入，检查权限后跳转到主界面
                            if (checkIfCanProceed()) {
                                navigateToMain()
                            } else {
                                // 否则提示用户
                                android.widget.Toast.makeText(
                                    this@PermissionSetupActivity,
                                    "请至少授予电话和联系人权限",
                                    android.widget.Toast.LENGTH_SHORT
                                ).show()
                            }
                        } else {
                            // 如果是从设置页面进入，直接返回
                            finish()
                        }
                    },
                    appRepository = appRepository
                )
            }
        }
    }
    
    override fun onResume() {
        super.onResume()
        // 不在 onResume 中自动检查和跳转，避免意外跳转
    }
    
    private fun requestEssentialPermissions() {
        if (hasRequestedPermissions) return
        hasRequestedPermissions = true
        
        XXPermissions.with(this)
            .permission(
                Manifest.permission.CALL_PHONE,
                Manifest.permission.READ_CONTACTS
            )
            .request(object : OnPermissionCallback {
                override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {
                    // 请求设置为默认桌面
                    LauncherUtils.triggerDefaultLauncherChooser(this@PermissionSetupActivity)
                }
                
                override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {
                    // 被拒绝不做处理
                }
            })
    }
    
    private fun checkIfCanProceed(): Boolean {
        // 检查是否已授予基本权限
        val hasPhone = XXPermissions.isGranted(this, Manifest.permission.CALL_PHONE)
        val hasContacts = XXPermissions.isGranted(this, Manifest.permission.READ_CONTACTS)
        val isDefaultLauncher = LauncherUtils.isDefaultLauncher(this)
        
        // 至少需要电话和联系人权限
        return hasPhone && hasContacts
    }
    
    private fun navigateToMain() {
        val intent = Intent(this, MainActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
        finish()
    }
}
