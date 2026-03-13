package tech.huangsh.onetap.ui.screens.home

import android.Manifest
import android.content.Context
import android.content.Intent
import android.hardware.camera2.CameraCharacteristics
import android.hardware.camera2.CameraManager
import android.widget.Toast
import com.hjq.permissions.XXPermissions
import com.hjq.permissions.OnPermissionCallback
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Android
import androidx.compose.material.icons.filled.FlashlightOn
import androidx.compose.material.icons.filled.FlashlightOff
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import tech.huangsh.onetap.R
import tech.huangsh.onetap.data.model.AppInfo
import tech.huangsh.onetap.ui.activity.PluginManagementActivity
import tech.huangsh.onetap.ui.activity.SettingsActivity
import tech.huangsh.onetap.ui.screens.components.ContactActionBottomSheet
import tech.huangsh.onetap.ui.screens.components.ContactItem
import tech.huangsh.onetap.ui.screens.components.VoiceAssistantDialog
import tech.huangsh.onetap.ui.theme.SimpleDesktopTheme
import tech.huangsh.onetap.utils.ImageUtils
import tech.huangsh.onetap.viewmodel.MainViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(viewModel: MainViewModel) {
    val context = LocalContext.current
    val contacts by viewModel.contacts.collectAsState()
    val apps by viewModel.apps.collectAsState()
    val currentTime by viewModel.currentTime.collectAsState() // 时间
    val currentDate by viewModel.currentDate.collectAsState() // 日期
    val currentWeek by viewModel.currentWeek.collectAsState() // 星期
    val currentLunarDate by viewModel.currentLunarDate.collectAsState() // 农历日期
    val weatherInfo by viewModel.weatherInfo.collectAsState() // 天气
    val showBottomSheet by viewModel.showBottomSheet.collectAsState()
    val selectedContact by viewModel.selectedContact.collectAsState()
    
    // 语音助手对话框状态
    var showVoiceAssistantDialog by remember { mutableStateOf(false) }
    
    // 手电筒状态
    var isFlashlightOn by remember { mutableStateOf(tech.huangsh.onetap.utils.FlashlightHelper.isOn()) }
    
    // 手电筒开关函数
    fun toggleFlashlight() {
        if (tech.huangsh.onetap.utils.FlashlightHelper.toggle(context)) {
            isFlashlightOn = tech.huangsh.onetap.utils.FlashlightHelper.isOn()
        } else {
            Toast.makeText(context, "手电筒操作失败", Toast.LENGTH_SHORT).show()
        }
    }
    
    // 页面销毁时关闭手电筒
    DisposableEffect(Unit) {
        onDispose {
            if (tech.huangsh.onetap.utils.FlashlightHelper.isOn()) {
                tech.huangsh.onetap.utils.FlashlightHelper.turnOff(context)
            }
        }
    }
    
    // 使用XXPermissions申请电话权限并拨打电话
    fun requestPhonePermissionAndCall(phoneNumber: String) {
        XXPermissions.with(context as androidx.activity.ComponentActivity)
            .permission(Manifest.permission.CALL_PHONE)
            .request(object : OnPermissionCallback {
                override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {
                    if (allGranted) {
                        // 权限已授予，执行打电话
                        val intent = viewModel.makePhoneCall(phoneNumber)
                        intent?.let { context.startActivity(it) }
                    }
                }
                
                override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {
                    // 权限被拒绝，显示提示
                    if (doNotAskAgain) {
                        Toast.makeText(context, "请在设置中开启电话权限才能拨打电话", Toast.LENGTH_LONG).show()
                        // 可以引导用户到设置页面
                        XXPermissions.startPermissionActivity(context, permissions)
                    } else {
                        Toast.makeText(context, "需要电话权限才能拨打电话", Toast.LENGTH_SHORT).show()
                    }
                }
            })
    }

    Scaffold(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background),
        containerColor = MaterialTheme.colorScheme.background
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                // 顶部时间 + 天气 + 设置按钮
                Card(
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primary),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Box(
                        modifier = Modifier.padding(16.dp).fillMaxWidth()
                    ) {
                        Column(
                            horizontalAlignment = Alignment.Start
                        ) {
                            Text(currentTime, fontSize = 50.sp, color = MaterialTheme.colorScheme.onPrimary, fontWeight = FontWeight.Bold)
                            Spacer(Modifier.height(4.dp))
                            Text("$currentDate $currentWeek", color = MaterialTheme.colorScheme.onPrimary)
                            Text(
                                "$currentLunarDate  ${weatherInfo?.weatherIcon ?: ""} ${weatherInfo?.weather ?: ""} ${weatherInfo?.temperature ?: ""}°C",
                                color = MaterialTheme.colorScheme.onPrimary
                            )
                        }

                        Row(
                            modifier = Modifier.align(Alignment.TopEnd),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            // 插件管理按钮
                            IconButton(
                                onClick = {
                                    val intent = Intent(context, PluginManagementActivity::class.java)
                                    context.startActivity(intent)
                                },
                                modifier = Modifier.size(40.dp)
                            ) {
                                Icon(
                                    Icons.Default.Android, 
                                    contentDescription = "插件管理", 
                                    modifier = Modifier.size(40.dp), 
                                    tint = MaterialTheme.colorScheme.onPrimary
                                )
                            }
                            
                            // 设置按钮
                            IconButton(
                                onClick = {
                                    val intent = Intent(context, SettingsActivity::class.java)
                                    context.startActivity(intent)
                                },
                                modifier = Modifier.size(50.dp)
                            ) {
                                Icon(Icons.Default.Settings, contentDescription = stringResource(R.string.settings), modifier = Modifier.size(50.dp), tint = MaterialTheme.colorScheme.onPrimary)
                            }
                        }
                    }

                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // 统一网格：外设 + 联系人 + 应用程序
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                contentPadding = PaddingValues(bottom = 100.dp)
            ) {
                // 1. 第一行左边：手电筒大卡片
                item {
                    FlashlightCard(
                        isOn = isFlashlightOn,
                        onClick = { toggleFlashlight() }
                    )
                }
                
                // 2. 第一行右边：语音助手
                item {
                    VoiceAssistantPlaceholderCard(
                        onClick = { showVoiceAssistantDialog = true }
                    )
                }
                
                // 3. 第二行及以后：优先排列系统联系人
                items(contacts) { contact ->
                    ContactItem(
                        contact = contact,
                        onClick = { viewModel.showContactActions(contact) },
                        isHomeScreen = true
                    )
                }
                
                // 4. 联系人之后：排列用户安装的应用程序
                items(apps) { app ->
                    AppGridCard(
                        app = app,
                        onClick = { packageName ->
                            val intent = viewModel.launchApp(packageName)
                            intent?.let { appIntent -> context.startActivity(appIntent) }
                        }
                    )
                }
            }
        }

        // 底部菜单
        if (showBottomSheet && selectedContact != null) {
            ContactActionBottomSheet(
                contact = selectedContact!!,
                onDismiss = { viewModel.hideBottomSheet() },
                onVideoCall = {
                    viewModel.startWeChatVideoCall(selectedContact!!.wechatNickname)
                    viewModel.hideBottomSheet()
                },
                onVoiceCall = {
                    viewModel.startWeChatVoiceCall(selectedContact!!.wechatNickname)
                    viewModel.hideBottomSheet()
                },
                onPhoneCall = { phone ->
                    // 使用XXPermissions申请电话权限并拨打电话
                    requestPhonePermissionAndCall(phone)
                    viewModel.hideBottomSheet()
                },
                onCancelCall = {
                    viewModel.hideBottomSheet()
                }
            )
        }
        
        // 语音助手对话框
        if (showVoiceAssistantDialog) {
            val scope = rememberCoroutineScope()
            VoiceAssistantDialog(
                contacts = contacts,
                onDismiss = { showVoiceAssistantDialog = false },
                onMakePhoneCall = { contact ->
                    contact.phone?.let { phone ->
                        requestPhonePermissionAndCall(phone)
                    }
                },
                onMakeWeChatCall = { contact ->
                    viewModel.startWeChatVideoCall(contact.wechatNickname)
                },
                onLaunchApp = { app ->
                    val intent = viewModel.launchApp(app.packageName)
                    intent?.let { context.startActivity(it) }
                },
                onSearchApp = { name ->
                    viewModel.findAppByName(name)
                },
                voiceAssistant = null // 如果有全局 VoiceAssistant 实例可以传入
            )
        }
    }
}

@Composable
fun AppGridCard(
    app: AppInfo,
    onClick: (String) -> Unit
) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(1f)
            .clickable { onClick(app.packageName) }
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            // 图标渲染部分复用原有逻辑，限制大小以适应卡片
            Box(
                modifier = Modifier.size(80.dp),
                contentAlignment = Alignment.Center
            ) {
                when {
                    app.iconBytes != null -> {
                        val bitmap = ImageUtils.byteArrayToBitmap(app.iconBytes)
                        bitmap?.let {
                            Image(
                                bitmap = it.asImageBitmap(),
                                contentDescription = app.appName,
                                modifier = Modifier.fillMaxSize()
                            )
                        }
                    }

                    else -> {
                        Icon(
                            imageVector = Icons.Default.Android,
                            contentDescription = app.appName,
                            modifier = Modifier.fillMaxSize(),
                            tint = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }
            Spacer(Modifier.height(12.dp))
            Text(
                text = app.appName,
                fontSize = 20.sp,
                fontWeight = FontWeight.Medium,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 1,
                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
fun VoiceAssistantPlaceholderCard(
    onClick: () -> Unit
) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        ),
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(1f)
            .clickable { onClick() }
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(
                imageVector = Icons.Default.Mic,
                contentDescription = "语音助手",
                modifier = Modifier.size(80.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Spacer(Modifier.height(12.dp))
            Text(
                text = "语音助手",
                fontSize = 20.sp,
                fontWeight = FontWeight.Medium,
                color = MaterialTheme.colorScheme.onSurface
            )
        }
    }
}

/**
 * 手电筒大卡片，和联系人卡片样式一致
 */
@Composable
fun FlashlightCard(
    isOn: Boolean,
    onClick: () -> Unit
) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isOn) Color(0xFFFFD54F) else MaterialTheme.colorScheme.surface
        ),
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(1f)
            .clickable { onClick() }
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(
                imageVector = if (isOn) Icons.Default.FlashlightOn else Icons.Default.FlashlightOff,
                contentDescription = "手电筒",
                modifier = Modifier.size(80.dp),
                tint = if (isOn) Color(0xFF424242) else MaterialTheme.colorScheme.primary
            )
            Spacer(Modifier.height(12.dp))
            Text(
                text = if (isOn) "手电筒(开)" else "手电筒",
                fontSize = 20.sp,
                fontWeight = FontWeight.Medium,
                color = if (isOn) Color(0xFF424242) else MaterialTheme.colorScheme.onSurface
            )
        }
    }
}

@Preview
@Composable
fun contactCardPreview() {
    SimpleDesktopTheme {
        val apps = listOf(
            AppInfo(
                packageName = "tech.huangsh.assistant",
                appName = "微信",
                iconBytes = null,
                isEnabled = true,
                order = 1,
                installTime = 1,
                lastUpdateTime = 1,
            )
        )
        Row(
            modifier = Modifier.fillMaxWidth().padding(20.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            apps.forEach { app ->
                Box(modifier = Modifier.weight(1f)) {
                    AppGridCard(app = app) { }
                }
            }
        }
    }
}