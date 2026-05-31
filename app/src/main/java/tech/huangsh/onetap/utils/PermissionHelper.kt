package tech.huangsh.onetap.utils

import android.Manifest
import android.content.Context
import android.content.Intent
import android.provider.Settings
import android.text.TextUtils
import androidx.activity.ComponentActivity
import com.google.android.accessibility.selecttospeak.SelectToSpeakService
import com.hjq.permissions.XXPermissions

/**
 * 权限辅助工具类
 */
object PermissionHelper {
    
    /**
     * 检查无障碍服务是否已启用
     */
    fun isAccessibilityServiceEnabled(context: Context): Boolean {
        var accessibilityEnabled: Int
        val serviceId = context.packageName + "/" + SelectToSpeakService::class.java.canonicalName
        try {
            accessibilityEnabled = Settings.Secure.getInt(
                context.applicationContext.contentResolver,
                Settings.Secure.ACCESSIBILITY_ENABLED
            )
        } catch (e: Settings.SettingNotFoundException) {
            return false
        }
        val colonSplitter: TextUtils.SimpleStringSplitter = TextUtils.SimpleStringSplitter(':')
        if (accessibilityEnabled == 1) {
            val settingValue: String? = Settings.Secure.getString(
                context.applicationContext.contentResolver,
                Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
            )
            if (settingValue != null) {
                colonSplitter.setString(settingValue)
                while (colonSplitter.hasNext()) {
                    val accessibilityService: String = colonSplitter.next()
                    if (accessibilityService.equals(serviceId, true)) {
                        return true
                    }
                }
            }
        }
        return false
    }
    
    /**
     * 打开无障碍服务设置页面
     */
    fun openAccessibilitySettings(context: Context) {
        val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
        context.startActivity(intent)
    }
    
    /**
     * 检查是否有拨打电话权限
     */
    fun hasPhonePermission(context: Context): Boolean {
        return XXPermissions.isGranted(context, Manifest.permission.CALL_PHONE)
    }
    
    /**
     * 检查是否有读取联系人权限
     */
    fun hasContactsPermission(context: Context): Boolean {
        return XXPermissions.isGranted(context, Manifest.permission.READ_CONTACTS)
    }
    
    /**
     * 检查是否有相机权限
     */
    fun hasCameraPermission(context: Context): Boolean {
        return XXPermissions.isGranted(context, Manifest.permission.CAMERA)
    }
    
    /**
     * 检查是否有位置权限
     */
    fun hasLocationPermission(context: Context): Boolean {
        return XXPermissions.isGranted(context, Manifest.permission.ACCESS_FINE_LOCATION)
    }
    
    /**
     * 检查是否是默认桌面
     */
    fun isDefaultLauncher(context: Context): Boolean {
        return LauncherUtils.isDefaultLauncher(context)
    }
    
    /**
     * 请求拨打电话权限
     */
    fun requestPhonePermission(
        activity: ComponentActivity,
        onGranted: () -> Unit = {},
        onDenied: () -> Unit = {}
    ) {
        XXPermissions.with(activity)
            .permission(Manifest.permission.CALL_PHONE)
            .request(object : com.hjq.permissions.OnPermissionCallback {
                override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {
                    if (allGranted) {
                        onGranted()
                    }
                }
                
                override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {
                    onDenied()
                }
            })
    }
    
    /**
     * 请求读取联系人权限
     */
    fun requestContactsPermission(
        activity: ComponentActivity,
        onGranted: () -> Unit = {},
        onDenied: () -> Unit = {}
    ) {
        XXPermissions.with(activity)
            .permission(Manifest.permission.READ_CONTACTS)
            .request(object : com.hjq.permissions.OnPermissionCallback {
                override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {
                    if (allGranted) {
                        onGranted()
                    }
                }
                
                override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {
                    onDenied()
                }
            })
    }
    
    /**
     * 检查所有必需权限
     */
    fun checkEssentialPermissions(context: Context): PermissionStatus {
        val hasPhone = hasPhonePermission(context)
        val hasContacts = hasContactsPermission(context)
        val isLauncher = isDefaultLauncher(context)
        
        return PermissionStatus(
            hasPhone = hasPhone,
            hasContacts = hasContacts,
            isDefaultLauncher = isLauncher,
            allEssentialGranted = hasPhone && hasContacts && isLauncher
        )
    }
}

/**
 * 权限状态数据类
 */
data class PermissionStatus(
    val hasPhone: Boolean,
    val hasContacts: Boolean,
    val isDefaultLauncher: Boolean,
    val allEssentialGranted: Boolean
)
