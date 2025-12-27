package tech.huangsh.onetap.ui.screens.plugin

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import tech.huangsh.onetap.plugin.BasePlugin
import tech.huangsh.onetap.plugin.IPlugin
import tech.huangsh.onetap.ui.screens.components.ActionButton
import tech.huangsh.onetap.viewmodel.PluginManagementViewModel

/**
 * 插件管理屏幕
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PluginManagementScreen(
    viewModel: PluginManagementViewModel = hiltViewModel(),
    onBack: () -> Unit
) {
    val registeredPlugins by viewModel.registeredPlugins.collectAsStateWithLifecycle()
    val registrationState by viewModel.registrationState.collectAsStateWithLifecycle()
    
    Scaffold(
        topBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.primary)
                    .padding(16.dp, 25.dp, 16.dp, 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onBack) {
                    Icon(
                        imageVector = Icons.Default.ArrowBack,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onPrimary
                    )
                }
                Spacer(modifier = Modifier.width(16.dp))
                Text(
                    text = "插件管理",
                    style = MaterialTheme.typography.titleLarge,
                    color = MaterialTheme.colorScheme.onPrimary,
                    modifier = Modifier.weight(1f)
                )
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            // 操作按钮
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                ActionButton(
                    text = "启用所有插件",
                    backgroundColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary,
                    modifier = Modifier.weight(1f),
                    onClick = { viewModel.enableAllPlugins() }
                )
                
                ActionButton(
                    text = "禁用所有插件",
                    backgroundColor = MaterialTheme.colorScheme.error,
                    contentColor = MaterialTheme.colorScheme.onError,
                    modifier = Modifier.weight(1f),
                    onClick = { viewModel.disableAllPlugins() }
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // 插件列表
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(registeredPlugins) { plugin ->
                    PluginItem(
                        plugin = plugin,
                        onToggleEnabled = { enabled ->
                            if (enabled) {
                                viewModel.enablePlugin(plugin.pluginId)
                            } else {
                                viewModel.disablePlugin(plugin.pluginId)
                            }
                        },
                        onConfigure = { viewModel.configurePlugin(plugin.pluginId) }
                    )
                }
            }
        }
    }
}

/**
 * 插件项组件
 */
@Composable
fun PluginItem(
    plugin: IPlugin,
    onToggleEnabled: (Boolean) -> Unit,
    onConfigure: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surface
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            // 插件名称和启用开关
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = plugin.name,
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    
                    Spacer(modifier = Modifier.height(4.dp))
                    
                    Text(
                        text = plugin.pluginId,
                        fontSize = 14.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                Switch(
                    checked = plugin.isEnabled,
                    onCheckedChange = onToggleEnabled
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // 插件描述
            Text(
                text = plugin.description,
                fontSize = 14.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(4.dp))
            
            // 插件版本和作者
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "版本: ${plugin.version}",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                
                Text(
                    text = "作者: ${plugin.author}",
                    fontSize = 12.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            // 插件状态
            if (plugin is BasePlugin) {
                val pluginState by plugin.pluginState.collectAsState()
                
                Spacer(modifier = Modifier.height(8.dp))
                
                val (stateText, stateColor) = when (pluginState) {
                    BasePlugin.PluginState.INSTALLED -> "已安装" to Color.Gray
                    BasePlugin.PluginState.INITIALIZING -> "初始化中" to Color.Blue
                    BasePlugin.PluginState.INITIALIZED -> "已初始化" to Color.Blue
                    BasePlugin.PluginState.STARTING -> "启动中" to Color.Blue
                    BasePlugin.PluginState.RUNNING -> "运行中" to Color.Green
                    BasePlugin.PluginState.STOPPING -> "停止中" to Color.Blue
                    BasePlugin.PluginState.STOPPED -> "已停止" to Color.Gray
                    BasePlugin.PluginState.ERROR -> "错误" to Color.Red
                    BasePlugin.PluginState.UNINSTALLED -> "未安装" to Color.Red
                }
                
                Text(
                    text = "状态: $stateText",
                    fontSize = 12.sp,
                    color = stateColor,
                    fontWeight = FontWeight.Bold
                )
            }
            
            // 配置按钮
            if (plugin.getConfigScreen() != null) {
                Spacer(modifier = Modifier.height(8.dp))
                
                ActionButton(
                    text = "配置",
                    backgroundColor = MaterialTheme.colorScheme.secondary,
                    contentColor = MaterialTheme.colorScheme.onSecondary,
                    onClick = onConfigure
                )
            }
        }
    }
}