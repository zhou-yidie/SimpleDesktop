package tech.huangsh.onetap.plugin

/**
 * 插件事件类
 */
sealed class PluginEvent {
    /**
     * 插件安装事件
     */
    data class PluginInstalled(val pluginId: String) : PluginEvent()
    
    /**
     * 插件卸载事件
     */
    data class PluginUninstalled(val pluginId: String) : PluginEvent()
    
    /**
     * 插件启用事件
     */
    data class PluginEnabled(val pluginId: String) : PluginEvent()
    
    /**
     * 插件禁用事件
     */
    data class PluginDisabled(val pluginId: String) : PluginEvent()
    
    /**
     * 插件更新事件
     */
    data class PluginUpdated(val pluginId: String, val oldVersion: String, val newVersion: String) : PluginEvent()
    
    /**
     * 应用启动事件
     */
    object AppStarted : PluginEvent()
    
    /**
     * 应用进入前台事件
     */
    object AppResumed : PluginEvent()
    
    /**
     * 应用进入后台事件
     */
    object AppPaused : PluginEvent()
    
    /**
     * 用户登录事件
     */
    data class UserLoggedIn(val userId: String) : PluginEvent()
    
    /**
     * 用户登出事件
     */
    object UserLoggedOut : PluginEvent()
    
    /**
     * 系统设置变更事件
     */
    data class SettingsChanged(val key: String, val value: Any) : PluginEvent()
    
    /**
     * 自定义事件
     */
    data class CustomEvent(val eventType: String, val data: Map<String, Any>) : PluginEvent()
}