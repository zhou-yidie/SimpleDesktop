package tech.huangsh.onetap.ui.screens.settings

import android.Manifest
import android.content.Context
import android.content.Intent
import android.provider.Settings
import android.text.TextUtils
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.google.android.accessibility.selecttospeak.SelectToSpeakService
import com.hjq.permissions.XXPermissions
import tech.huangsh.onetap.R
import tech.huangsh.onetap.ui.screens.components.AccessibilityGuideDialog
import tech.huangsh.onetap.ui.screens.components.CommonTopBar
import tech.huangsh.onetap.utils.LauncherUtils

data class PermissionItem(
    val icon: ImageVector,
    val title: String,
    val description: String,
    val isEssential: Boolean,
    val permissionName: String? = null,
    val checkMethod: (Context) -> Boolean,
    val requestMethod: (Context) -> Unit
)

@Composable
fun PermissionManagementScreen(
    onBack: () -> Unit
) {
    val context = LocalContext.current
    var showAccessibilityGuide by remember { mutableStateOf(false) }
    var refreshTrigger by remember { mutableStateOf(0) }
    
    val permissions = remember(refreshTrigger) {
        listOf(
            // 必需权限
            PermissionItem(
                icon = Icons.Default.Phone,
                title = context.getString(R.string.permission_phone_title),
                description = context.getString(R.string.permission_phone_desc),
                isEssential = true,
                permissionName = Manifest.permission.CALL_PHONE,
                checkMethod = { ctx ->
                    XXPermissions.isGranted(ctx, Manifest.permission.CALL_PHONE)
                },
                requestMethod = { ctx ->
                    XXPermissions.with(ctx as androidx.activity.ComponentActivity)
                        .permission(Manifest.permission.CALL_PHONE)
                        .request(object : com.hjq.permissions.OnPermissionCallback {
                        override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {}
                        override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {}
                    })
                }
            ),
            PermissionItem(
                icon = Icons.Default.People,
                title = context.getString(R.string.permission_contacts_title),
                description = context.getString(R.string.permission_contacts_desc),
                isEssential = true,
                permissionName = Manifest.permission.READ_CONTACTS,
                checkMethod = { ctx ->
                    XXPermissions.isGranted(ctx, Manifest.permission.READ_CONTACTS)
                },
                requestMethod = { ctx ->
                    XXPermissions.with(ctx as androidx.activity.ComponentActivity)
                        .permission(Manifest.permission.READ_CONTACTS)
                        .request(object : com.hjq.permissions.OnPermissionCallback {
                        override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {}
                        override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {}
                    })
                }
            ),
            PermissionItem(
                icon = Icons.Default.Home,
                title = context.getString(R.string.permission_launcher_title),
                description = context.getString(R.string.permission_launcher_desc),
                isEssential = true,
                checkMethod = { ctx ->
                    LauncherUtils.isDefaultLauncher(ctx)
                },
                requestMethod = { ctx ->
                    LauncherUtils.triggerDefaultLauncherChooser(ctx)
                }
            ),
            
            // 可选权限
            PermissionItem(
                icon = Icons.Default.CameraAlt,
                title = context.getString(R.string.permission_camera_title),
                description = context.getString(R.string.permission_camera_desc),
                isEssential = false,
                permissionName = Manifest.permission.CAMERA,
                checkMethod = { ctx ->
                    XXPermissions.isGranted(ctx, Manifest.permission.CAMERA)
                },
                requestMethod = { ctx ->
                    XXPermissions.with(ctx as androidx.activity.ComponentActivity)
                        .permission(Manifest.permission.CAMERA)
                        .request(object : com.hjq.permissions.OnPermissionCallback {
                        override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {}
                        override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {}
                    })
                }
            ),
            PermissionItem(
                icon = Icons.Default.LocationOn,
                title = context.getString(R.string.permission_location_title),
                description = context.getString(R.string.permission_location_desc),
                isEssential = false,
                permissionName = Manifest.permission.ACCESS_FINE_LOCATION,
                checkMethod = { ctx ->
                    XXPermissions.isGranted(ctx, Manifest.permission.ACCESS_FINE_LOCATION)
                },
                requestMethod = { ctx ->
                    XXPermissions.with(ctx as androidx.activity.ComponentActivity)
                        .permission(Manifest.permission.ACCESS_FINE_LOCATION)
                        .request(object : com.hjq.permissions.OnPermissionCallback {
                        override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {}
                        override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {}
                    })
                }
            ),
            PermissionItem(
                icon = Icons.Default.Accessibility,
                title = context.getString(R.string.permission_accessibility_title),
                description = context.getString(R.string.permission_accessibility_desc),
                isEssential = false,
                checkMethod = { ctx ->
                    isAccessibilityServiceEnabled(ctx)
                },
                requestMethod = { ctx ->
                    showAccessibilityGuide = true
                }
            )
        )
    }
    
    val essentialPermissions = permissions.filter { it.isEssential }
    val optionalPermissions = permissions.filter { !it.isEssential }
    
    val allEssentialGranted = essentialPermissions.all { it.checkMethod(context) }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        CommonTopBar(
            title = stringResource(R.string.permission_management),
            onBack = onBack
        )
        
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            // 状态卡片
            PermissionStatusCard(allGranted = allEssentialGranted)
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // 必需权限
            SectionHeader(stringResource(R.string.permission_essential))
            Spacer(modifier = Modifier.height(12.dp))
            
            essentialPermissions.forEach { permission ->
                PermissionCard(
                    permission = permission,
                    context = context,
                    onStatusChanged = { refreshTrigger++ }
                )
                Spacer(modifier = Modifier.height(12.dp))
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // 可选权限
            SectionHeader(stringResource(R.string.permission_optional))
            Spacer(modifier = Modifier.height(12.dp))
            
            optionalPermissions.forEach { permission ->
                PermissionCard(
                    permission = permission,
                    context = context,
                    onStatusChanged = { refreshTrigger++ }
                )
                Spacer(modifier = Modifier.height(12.dp))
            }
            
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
    
    // 无障碍服务引导对话框
    if (showAccessibilityGuide) {
        AccessibilityGuideDialog(
            onDismiss = { 
                showAccessibilityGuide = false
                refreshTrigger++
            },
            onSuccess = {
                refreshTrigger++
            }
        )
    }
}

@Composable
private fun PermissionStatusCard(allGranted: Boolean) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (allGranted)
                MaterialTheme.colorScheme.primaryContainer
            else
                MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.6f)
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(
                        if (allGranted)
                            MaterialTheme.colorScheme.primary.copy(alpha = 0.2f)
                        else
                            MaterialTheme.colorScheme.error.copy(alpha = 0.2f)
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = if (allGranted) Icons.Default.Check else Icons.Default.Info,
                    contentDescription = null,
                    modifier = Modifier.size(32.dp),
                    tint = if (allGranted)
                        MaterialTheme.colorScheme.primary
                    else
                        MaterialTheme.colorScheme.error
                )
            }
            
            Spacer(modifier = Modifier.width(20.dp))
            
            Column {
                Text(
                    text = if (allGranted)
                        stringResource(R.string.permission_all_granted)
                    else
                        stringResource(R.string.permission_some_denied),
                    style = MaterialTheme.typography.titleLarge,
                    color = if (allGranted)
                        MaterialTheme.colorScheme.onPrimaryContainer
                    else
                        MaterialTheme.colorScheme.onErrorContainer
                )
            }
        }
    }
}

@Composable
private fun SectionHeader(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleLarge,
        color = MaterialTheme.colorScheme.onBackground
    )
}

@Composable
private fun PermissionCard(
    permission: PermissionItem,
    context: Context,
    onStatusChanged: () -> Unit
) {
    val isGranted = permission.checkMethod(context)
    
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 图标
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(
                        if (isGranted)
                            MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)
                        else
                            MaterialTheme.colorScheme.error.copy(alpha = 0.1f)
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = permission.icon,
                    contentDescription = null,
                    modifier = Modifier.size(28.dp),
                    tint = if (isGranted)
                        MaterialTheme.colorScheme.primary
                    else
                        MaterialTheme.colorScheme.error
                )
            }
            
            Spacer(modifier = Modifier.width(16.dp))
            
            // 标题和描述
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = permission.title,
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onSurface
                )
                
                Spacer(modifier = Modifier.height(4.dp))
                
                Text(
                    text = permission.description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                // 状态标签
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = if (isGranted)
                        MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)
                    else
                        MaterialTheme.colorScheme.error.copy(alpha = 0.15f)
                ) {
                    Text(
                        text = if (isGranted)
                            stringResource(R.string.permission_status_granted)
                        else
                            stringResource(R.string.permission_status_denied),
                        style = MaterialTheme.typography.labelMedium,
                        color = if (isGranted)
                            MaterialTheme.colorScheme.primary
                        else
                            MaterialTheme.colorScheme.error,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                    )
                }
            }
            
            Spacer(modifier = Modifier.width(12.dp))
            
            // 操作按钮
            if (!isGranted) {
                Button(
                    onClick = {
                        permission.requestMethod(context)
                        // 立即刷新状态（不延迟）
                        onStatusChanged()
                    },
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text(
                        text = stringResource(R.string.permission_request),
                        style = MaterialTheme.typography.labelLarge
                    )
                }
            }
        }
    }
}

private fun isAccessibilityServiceEnabled(context: Context): Boolean {
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
