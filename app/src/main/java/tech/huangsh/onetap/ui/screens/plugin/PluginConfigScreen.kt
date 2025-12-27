package tech.huangsh.onetap.ui.screens.plugin

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import tech.huangsh.onetap.plugin.IPluginConfigStorage
import tech.huangsh.onetap.plugin.impl.AppPlugin
import tech.huangsh.onetap.plugin.impl.ContactPlugin
import tech.huangsh.onetap.plugin.impl.WeatherPlugin
import tech.huangsh.onetap.ui.screens.components.CommonTopBar

/**
 * 插件配置通用界面
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PluginConfigScreen(
    pluginId: String,
    pluginName: String,
    contactPlugin: ContactPlugin? = null,
    appPlugin: AppPlugin? = null,
    weatherPlugin: WeatherPlugin? = null,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    
    Scaffold(
        topBar = {
            CommonTopBar(
                title = "$pluginName 配置",
                onBack = onBack
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            when (pluginId) {
                "contact_plugin" -> contactPlugin?.let { plugin ->
                    ContactPluginConfigContent(plugin = plugin)
                }
                "app_plugin" -> appPlugin?.let { plugin ->
                    AppPluginConfigContent(plugin = plugin)
                }
                "weather_plugin" -> weatherPlugin?.let { plugin ->
                    WeatherPluginConfigContent(plugin = plugin)
                }
                else -> {
                    Text("该插件暂无配置选项", style = MaterialTheme.typography.bodyLarge)
                }
            }
        }
    }
}

/**
 * 联系人插件配置内容
 */
@Composable
fun ContactPluginConfigContent(plugin: ContactPlugin) {
    val config = plugin.getConfigStorage()
    val scope = rememberCoroutineScope()
    
    var defaultCallMethod by remember { mutableStateOf("phone") }
    var maxContactCount by remember { mutableStateOf(8) }
    var avatarSize by remember { mutableStateOf("large") }
    
    LaunchedEffect(Unit) {
        defaultCallMethod = config.getString("default_call_method", "phone")
        maxContactCount = config.getInt("max_contact_count", 8)
        avatarSize = config.getString("avatar_size", "large")
    }
    
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(
                "联系人设置",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            // 默认通话方式
            Text("默认通话方式", style = MaterialTheme.typography.bodyMedium)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                FilterChip(
                    selected = defaultCallMethod == "phone",
                    onClick = {
                        defaultCallMethod = "phone"
                        scope.launch {
                            config.setValue("default_call_method", "phone")
                        }
                    },
                    label = { Text("电话") },
                    leadingIcon = { Icon(Icons.Default.Phone, null) }
                )
                FilterChip(
                    selected = defaultCallMethod == "wechat_voice",
                    onClick = {
                        defaultCallMethod = "wechat_voice"
                        scope.launch {
                            config.setValue("default_call_method", "wechat_voice")
                        }
                    },
                    label = { Text("微信语音") }
                )
                FilterChip(
                    selected = defaultCallMethod == "wechat_video",
                    onClick = {
                        defaultCallMethod = "wechat_video"
                        scope.launch {
                            config.setValue("default_call_method", "wechat_video")
                        }
                    },
                    label = { Text("微信视频") }
                )
            }
            
            Divider()
            
            // 最大联系人数量
            Text("显示联系人数量: $maxContactCount 个", style = MaterialTheme.typography.bodyMedium)
            Slider(
                value = maxContactCount.toFloat(),
                onValueChange = { 
                    maxContactCount = it.toInt()
                },
                onValueChangeFinished = {
                    scope.launch {
                        config.setValue("max_contact_count", maxContactCount)
                    }
                },
                valueRange = 4f..16f,
                steps = 11
            )
            
            Divider()
            
            // 头像大小
            Text("头像大小", style = MaterialTheme.typography.bodyMedium)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                FilterChip(
                    selected = avatarSize == "small",
                    onClick = {
                        avatarSize = "small"
                        scope.launch {
                            config.setValue("avatar_size", "small")
                        }
                    },
                    label = { Text("小") }
                )
                FilterChip(
                    selected = avatarSize == "medium",
                    onClick = {
                        avatarSize = "medium"
                        scope.launch {
                            config.setValue("avatar_size", "medium")
                        }
                    },
                    label = { Text("中") }
                )
                FilterChip(
                    selected = avatarSize == "large",
                    onClick = {
                        avatarSize = "large"
                        scope.launch {
                            config.setValue("avatar_size", "large")
                        }
                    },
                    label = { Text("大") }
                )
            }
        }
    }
}

/**
 * 应用插件配置内容
 */
@Composable
fun AppPluginConfigContent(plugin: AppPlugin) {
    val config = plugin.getConfigStorage()
    val scope = rememberCoroutineScope()
    
    var maxAppCount by remember { mutableStateOf(20) }
    var autoRefresh by remember { mutableStateOf(true) }
    var showSystemApps by remember { mutableStateOf(false) }
    
    LaunchedEffect(Unit) {
        maxAppCount = config.getInt("max_app_count", 20)
        autoRefresh = config.getBoolean("auto_refresh", true)
        showSystemApps = config.getBoolean("show_system_apps", false)
    }
    
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(
                "应用设置",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            // 最大应用数量
            Text("最多显示应用数量: $maxAppCount 个", style = MaterialTheme.typography.bodyMedium)
            Slider(
                value = maxAppCount.toFloat(),
                onValueChange = { 
                    maxAppCount = it.toInt()
                },
                onValueChangeFinished = {
                    scope.launch {
                        config.setValue("max_app_count", maxAppCount)
                    }
                },
                valueRange = 10f..50f,
                steps = 39
            )
            
            Divider()
            
            // 自动刷新
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("自动刷新应用列表", style = MaterialTheme.typography.bodyMedium)
                    Text(
                        "启动时自动扫描新安装的应用",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = autoRefresh,
                    onCheckedChange = { 
                        autoRefresh = it
                        scope.launch {
                            config.setValue("auto_refresh", it)
                        }
                    }
                )
            }
            
            Divider()
            
            // 显示系统应用
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("显示系统应用", style = MaterialTheme.typography.bodyMedium)
                    Text(
                        "在应用管理中显示系统应用",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = showSystemApps,
                    onCheckedChange = { 
                        showSystemApps = it
                        scope.launch {
                            config.setValue("show_system_apps", it)
                        }
                    }
                )
            }
        }
    }
}

/**
 * 天气插件配置内容
 */
@Composable
fun WeatherPluginConfigContent(plugin: WeatherPlugin) {
    val config = plugin.getConfigStorage()
    val scope = rememberCoroutineScope()
    
    var autoUpdate by remember { mutableStateOf(true) }
    var updateInterval by remember { mutableStateOf(3600) }
    var showWeatherIcon by remember { mutableStateOf(true) }
    var showTemperature by remember { mutableStateOf(true) }
    
    LaunchedEffect(Unit) {
        autoUpdate = config.getBoolean("auto_update", true)
        updateInterval = config.getInt("update_interval", 3600)
        showWeatherIcon = config.getBoolean("show_weather_icon", true)
        showTemperature = config.getBoolean("show_temperature", true)
    }
    
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(
                "天气设置",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            // 自动更新
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("自动更新天气", style = MaterialTheme.typography.bodyMedium)
                    Text(
                        "定时自动更新天气信息",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = autoUpdate,
                    onCheckedChange = { 
                        autoUpdate = it
                        scope.launch {
                            config.setValue("auto_update", it)
                        }
                    }
                )
            }
            
            Divider()
            
            // 更新间隔
            if (autoUpdate) {
                Text("更新间隔", style = MaterialTheme.typography.bodyMedium)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    FilterChip(
                        selected = updateInterval == 1800,
                        onClick = {
                            updateInterval = 1800
                            scope.launch {
                                config.setValue("update_interval", 1800)
                            }
                        },
                        label = { Text("30分钟") }
                    )
                    FilterChip(
                        selected = updateInterval == 3600,
                        onClick = {
                            updateInterval = 3600
                            scope.launch {
                                config.setValue("update_interval", 3600)
                            }
                        },
                        label = { Text("1小时") }
                    )
                    FilterChip(
                        selected = updateInterval == 7200,
                        onClick = {
                            updateInterval = 7200
                            scope.launch {
                                config.setValue("update_interval", 7200)
                            }
                        },
                        label = { Text("2小时") }
                    )
                }
                
                Divider()
            }
            
            // 显示天气图标
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("显示天气图标", style = MaterialTheme.typography.bodyMedium)
                Switch(
                    checked = showWeatherIcon,
                    onCheckedChange = { 
                        showWeatherIcon = it
                        scope.launch {
                            config.setValue("show_weather_icon", it)
                        }
                    }
                )
            }
            
            Divider()
            
            // 显示温度
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("显示温度", style = MaterialTheme.typography.bodyMedium)
                Switch(
                    checked = showTemperature,
                    onCheckedChange = { 
                        showTemperature = it
                        scope.launch {
                            config.setValue("show_temperature", it)
                        }
                    }
                )
            }
        }
    }
}
