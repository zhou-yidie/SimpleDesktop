package tech.huangsh.onetap.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch
import tech.huangsh.onetap.plugin.IPlugin
import tech.huangsh.onetap.plugin.PluginRegistry
import tech.huangsh.onetap.plugin.impl.AppPlugin
import tech.huangsh.onetap.plugin.impl.ContactPlugin
import tech.huangsh.onetap.plugin.impl.WeatherPlugin
import javax.inject.Inject

/**
 * 插件管理ViewModel
 */
@HiltViewModel
class PluginManagementViewModel @Inject constructor(
    private val pluginRegistry: PluginRegistry,
    private val contactPlugin: ContactPlugin,
    private val appPlugin: AppPlugin,
    private val weatherPlugin: WeatherPlugin
) : ViewModel() {
    
    // 注册状态
    private val _registrationState = MutableStateFlow<PluginRegistry.RegistrationState>(PluginRegistry.RegistrationState.Idle)
    val registrationState: StateFlow<PluginRegistry.RegistrationState> = _registrationState.asStateFlow()
    
    // 已注册的插件列表
    private val _registeredPlugins = MutableStateFlow<List<IPlugin>>(emptyList())
    val registeredPlugins: StateFlow<List<IPlugin>> = _registeredPlugins.asStateFlow()
    
    init {
        // 初始化插件列表
        _registeredPlugins.value = pluginRegistry.getAllRegisteredPlugins()
        
        // 监听注册状态变化
        viewModelScope.launch {
            pluginRegistry.registrationState.collect { state ->
                _registrationState.value = state
                // 状态变化时更新插件列表
                _registeredPlugins.value = pluginRegistry.getAllRegisteredPlugins()
            }
        }
    }
    
    /**
     * 启用插件
     */
    fun enablePlugin(pluginId: String) {
        viewModelScope.launch {
            pluginRegistry.enablePlugin(pluginId)
        }
    }
    
    /**
     * 禁用插件
     */
    fun disablePlugin(pluginId: String) {
        viewModelScope.launch {
            pluginRegistry.disablePlugin(pluginId)
        }
    }
    
    /**
     * 配置插件
     */
    fun configurePlugin(context: android.content.Context, pluginId: String, pluginName: String) {
        // 启动插件配置界面
        val intent = android.content.Intent(context, tech.huangsh.onetap.ui.activity.PluginConfigActivity::class.java)
        intent.putExtra("plugin_id", pluginId)
        intent.putExtra("plugin_name", pluginName)
        context.startActivity(intent)
    }
    
    /**
     * 启用所有插件
     */
    fun enableAllPlugins() {
        viewModelScope.launch {
            val plugins = pluginRegistry.getAllRegisteredPlugins()
            plugins.forEach { plugin ->
                if (!plugin.isEnabled) {
                    pluginRegistry.enablePlugin(plugin.pluginId)
                }
            }
        }
    }
    
    /**
     * 禁用所有插件
     */
    fun disableAllPlugins() {
        viewModelScope.launch {
            val plugins = pluginRegistry.getAllRegisteredPlugins()
            plugins.forEach { plugin ->
                if (plugin.isEnabled) {
                    pluginRegistry.disablePlugin(plugin.pluginId)
                }
            }
        }
    }
    
    /**
     * 注册联系人插件
     */
    fun registerContactPlugin() {
        viewModelScope.launch {
            pluginRegistry.registerPlugin(contactPlugin)
        }
    }
    
    /**
     * 注销联系人插件
     */
    fun unregisterContactPlugin() {
        viewModelScope.launch {
            pluginRegistry.unregisterPlugin(contactPlugin.pluginId)
        }
    }
    
    /**
     * 注册应用插件
     */
    fun registerAppPlugin() {
        viewModelScope.launch {
            pluginRegistry.registerPlugin(appPlugin)
        }
    }
    
    /**
     * 注销应用插件
     */
    fun unregisterAppPlugin() {
        viewModelScope.launch {
            pluginRegistry.unregisterPlugin(appPlugin.pluginId)
        }
    }
    
    /**
     * 注册天气插件
     */
    fun registerWeatherPlugin() {
        viewModelScope.launch {
            pluginRegistry.registerPlugin(weatherPlugin)
        }
    }
    
    /**
     * 注销天气插件
     */
    fun unregisterWeatherPlugin() {
        viewModelScope.launch {
            pluginRegistry.unregisterPlugin(weatherPlugin.pluginId)
        }
    }
    
    /**
     * 获取插件依赖图
     */
    fun getDependencyGraph(): Map<String, List<String>> {
        return pluginRegistry.getDependencyGraph()
    }
}