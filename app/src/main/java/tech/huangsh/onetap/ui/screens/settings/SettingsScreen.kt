package tech.huangsh.onetap.ui.screens.settings

import android.content.Intent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.Apps
import androidx.compose.material.icons.filled.DisplaySettings
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.People
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import tech.huangsh.onetap.R
import tech.huangsh.onetap.data.model.Settings
import tech.huangsh.onetap.ui.activity.AppManagementActivity
import tech.huangsh.onetap.ui.activity.ContactManagementActivity
import tech.huangsh.onetap.ui.activity.DisplaySettingsActivity
import tech.huangsh.onetap.ui.activity.PermissionGuideActivity
import tech.huangsh.onetap.ui.screens.components.CommonTopBar
import tech.huangsh.onetap.viewmodel.SettingsViewModel
import androidx.compose.material.icons.filled.Bolt

@Composable
fun SettingsScreen(
    onBack: () -> Unit,
    settingsViewModel: SettingsViewModel = viewModel()
) {
    val context = LocalContext.current
    val settings by settingsViewModel.settings.collectAsState(initial = Settings())
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        // 顶部栏 - 使用统一的样式
        CommonTopBar(
            title = stringResource(R.string.settings),
            onBack = onBack
        )

        // 设置列表 - 与首页保持一致的白色卡片风格
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            SettingsItem(
                icon = Icons.Default.People,
                title = stringResource(R.string.contact_management),
                onClick = {
                    val intent = Intent(context, ContactManagementActivity::class.java)
                    context.startActivity(intent)
                }
            )

            SettingsItem(
                icon = Icons.Default.Apps,
                title = stringResource(R.string.app_settings),
                onClick = {
                    val intent = Intent(context, AppManagementActivity::class.java)
                    context.startActivity(intent)
                }
            )
            
            // 显示设置
            SettingsItem(
                icon = Icons.Default.DisplaySettings,
                title = stringResource(R.string.display_settings),
                onClick = {
                    val intent = Intent(context, DisplaySettingsActivity::class.java)
                    context.startActivity(intent)
                }
            )
            
            // 权限指引
            SettingsItem(
                icon = Icons.Default.Bolt,
                title = stringResource(R.string.permission_guide),
                onClick = {
                    val intent = Intent(context, PermissionGuideActivity::class.java)
                    context.startActivity(intent)
                }
            )
            
            // 桌面启动器设置
            if (settings.showExitLauncher) {
                LauncherSettingsSection(settingsViewModel)
            }
        }
    }
}

@Composable
fun SettingsItem(
    icon: ImageVector,
    title: String,
    modifier: Modifier = Modifier,
    onClick: () -> Unit = {},
    trailing: @Composable () -> Unit = {
        Icon(
            imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.primary,
            modifier = Modifier.size(24.dp)
        )
    }
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable { onClick() },
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 图标背景 - 使用与首页一致的蓝色主题
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    modifier = Modifier.size(28.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
            }

            Spacer(modifier = Modifier.width(20.dp))

            // 标题
            Text(
                text = title,
                style = MaterialTheme.typography.headlineSmall,
                color = MaterialTheme.colorScheme.onSurface,
                modifier = Modifier.weight(1f)
            )

            // 尾部内容
            trailing()
        }
    }
}

@Composable
fun LauncherSettingsSection(settingsViewModel: SettingsViewModel) {
    val context = LocalContext.current
    val isDefaultLauncher by settingsViewModel.isDefaultLauncher.collectAsState()
    val launcherMode by settingsViewModel.launcherMode.collectAsState()
    var pendingLauncherMode by remember { mutableStateOf<Boolean?>(null) }
    var showLauncherDialog by remember { mutableStateOf(false) }
    var dialogType by remember { mutableStateOf<LauncherDialogType?>(null) }
    val switchState = pendingLauncherMode ?: launcherMode
    
    Column(
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // 合并为单个开关：是否开启应用桌面
        SettingsItem(
            icon = Icons.Default.Home,
            title = stringResource(R.string.enable_app_launcher),
            trailing = {
                Switch(
                    checked = switchState,
                    onCheckedChange = { checked ->
                        pendingLauncherMode = checked
                        dialogType = if (checked) LauncherDialogType.Enable else LauncherDialogType.Disable
                        showLauncherDialog = true
                    }
                )
            }
        )

        // 不再显示“打开桌面设置”入口，开关仅控制是否吞掉返回/Home 操作以防老人误触
    }
    
    if (showLauncherDialog && dialogType != null) {
        val targetMode = pendingLauncherMode ?: launcherMode
        val (title, message, confirmLabel) = when (dialogType) {
            LauncherDialogType.Enable -> Triple(
                stringResource(R.string.launcher_enable_dialog_title),
                stringResource(R.string.launcher_enable_dialog_message),
                stringResource(R.string.launcher_enable_dialog_confirm)
            )
            LauncherDialogType.Disable -> Triple(
                stringResource(R.string.launcher_disable_dialog_title),
                stringResource(R.string.launcher_disable_dialog_message),
                stringResource(R.string.launcher_disable_dialog_confirm)
            )
            else -> Triple("", "", "")
        }

        AlertDialog(
            onDismissRequest = {
                pendingLauncherMode = null
                showLauncherDialog = false
                dialogType = null
            },
            title = {
                Text(text = title, style = MaterialTheme.typography.headlineSmall)
            },
            text = {
                Text(text = message, style = MaterialTheme.typography.bodyMedium)
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        dialogType?.let {
                            if (it == LauncherDialogType.Enable) {
                                settingsViewModel.updateLauncherMode(true)
                                settingsViewModel.triggerDefaultLauncherChooser()
                            } else {
                                settingsViewModel.updateLauncherMode(false)
                                settingsViewModel.exitLauncherMode()
                            }
                        }
                        pendingLauncherMode = null
                        showLauncherDialog = false
                        dialogType = null
                    }
                ) {
                    Text(confirmLabel)
                }
            },
            dismissButton = {
                TextButton(
                    onClick = {
                        pendingLauncherMode = null
                        showLauncherDialog = false
                        dialogType = null
                    }
                ) {
                    Text(stringResource(R.string.cancel))
                }
            }
        )
    }
}

@Composable
fun SettingsItemWithDescription(
    icon: ImageVector,
    title: String,
    description: String,
    modifier: Modifier = Modifier,
    descriptionColor: androidx.compose.ui.graphics.Color = MaterialTheme.colorScheme.onSurfaceVariant,
    onClick: () -> Unit = {},
    trailing: @Composable () -> Unit = {
        Icon(
            imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.primary,
            modifier = Modifier.size(24.dp)
        )
    }
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable { onClick() },
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 图标背景 - 使用与首页一致的蓝色主题
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    modifier = Modifier.size(28.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
            }

            Spacer(modifier = Modifier.width(20.dp))

            // 标题和描述
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.headlineSmall,
                    color = MaterialTheme.colorScheme.onSurface
                )
                
                Spacer(modifier = Modifier.height(4.dp))
                
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = descriptionColor,
                    lineHeight = MaterialTheme.typography.bodyMedium.lineHeight
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            // 尾部内容
            trailing()
        }
    }
}

private enum class LauncherDialogType {
    Enable,
    Disable
}