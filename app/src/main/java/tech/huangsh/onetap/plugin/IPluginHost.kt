package tech.huangsh.onetap.plugin

import android.content.Context
import kotlinx.coroutines.flow.Flow

/**
 * 插件宿主接口
 * 提供插件运行环境和API支持
 */
interface IPluginHost {
    /**
     * 获取应用上下文
     */
    fun getContext(): Context
    
    /**
     * 获取已安装的插件列表
     */
    fun getInstalledPlugins(): Flow<List<IPlugin>>
    
    /**
     * 获取已启用的插件列表
     */
    fun getEnabledPlugins(): Flow<List<IPlugin>>
    
    /**
     * 根据ID获取插件
     */
    fun getPlugin(pluginId: String): IPlugin?
    
    /**
     * 安装插件
     */
    suspend fun installPlugin(plugin: IPlugin): Boolean
    
    /**
     * 卸载插件
     */
    suspend fun uninstallPlugin(pluginId: String): Boolean
    
    /**
     * 启用插件
     */
    suspend fun enablePlugin(pluginId: String): Boolean
    
    /**
     * 禁用插件
     */
    suspend fun disablePlugin(pluginId: String): Boolean
    
    /**
     * 通知插件系统事件
     */
    suspend fun notifyPluginEvent(event: PluginEvent)
    
    /**
     * 获取插件间通信接口
     */
    fun getPluginMessenger(): IPluginMessenger
    
    /**
     * 获取插件配置存储
     */
    fun getPluginConfigStorage(pluginId: String): IPluginConfigStorage
}