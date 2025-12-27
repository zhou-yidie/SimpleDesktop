package tech.huangsh.onetap.plugin

import android.content.Context

/**
 * 插件基础接口
 * 所有插件必须实现此接口
 */
interface IPlugin {
    /**
     * 插件唯一标识符
     */
    val pluginId: String
    
    /**
     * 插件名称
     */
    val name: String
    
    /**
     * 插件版本
     */
    val version: String
    
    /**
     * 插件描述
     */
    val description: String
    
    /**
     * 插件作者
     */
    val author: String
    
    /**
     * 插件是否已启用
     */
    var isEnabled: Boolean
    
    /**
     * 插件初始化
     * @param context 应用上下文
     * @param pluginHost 插件宿主
     */
    suspend fun initialize(context: Context, pluginHost: IPluginHost)
    
    /**
     * 插件启动
     */
    suspend fun start()
    
    /**
     * 插件停止
     */
    suspend fun stop()
    
    /**
     * 插件销毁
     */
    suspend fun destroy()
    
    /**
     * 获取插件配置页面
     */
    fun getConfigScreen(): Any? = null
    
    /**
     * 获取插件主界面组件
     */
    fun getMainComponent(): Any? = null
    
    /**
     * 获取插件依赖的其他插件ID列表
     */
    fun getDependencies(): List<String> = emptyList()
    
    /**
     * 检查插件兼容性
     */
    fun isCompatible(version: String): Boolean = true
}