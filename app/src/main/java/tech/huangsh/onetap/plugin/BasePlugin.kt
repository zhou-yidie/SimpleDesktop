package tech.huangsh.onetap.plugin

import android.content.Context
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

/**
 * 基础插件抽象类
 * 提供插件的基础实现，简化插件开发
 */
abstract class BasePlugin : IPlugin {
    
    // 插件宿主引用
    protected lateinit var pluginHost: IPluginHost
        private set
    
    // 应用上下文
    protected lateinit var context: Context
        private set
    
    // 插件是否已初始化
    private var _isInitialized = false
    
    // 插件是否已启动
    private var _isStarted = false
    
    // 插件状态
    private val _pluginState = MutableStateFlow(PluginState.UNINSTALLED)
    val pluginState: StateFlow<PluginState> = _pluginState
    
    // 插件是否已启用
    override var isEnabled: Boolean = false
        set(value) {
            if (field != value) {
                field = value
                onEnabledChanged(value)
            }
        }
    
    /**
     * 插件状态枚举
     */
    enum class PluginState {
        UNINSTALLED,    // 未安装
        INSTALLED,      // 已安装
        INITIALIZING,   // 初始化中
        INITIALIZED,    // 已初始化
        STARTING,       // 启动中
        RUNNING,        // 运行中
        STOPPING,       // 停止中
        STOPPED,        // 已停止
        ERROR           // 错误状态
    }
    
    override suspend fun initialize(context: Context, pluginHost: IPluginHost) {
        if (_isInitialized) {
            return
        }
        
        try {
            _pluginState.value = PluginState.INITIALIZING
            this.context = context
            this.pluginHost = pluginHost
            
            onInitializing()
            
            _isInitialized = true
            _pluginState.value = PluginState.INITIALIZED
            
            onInitialized()
        } catch (e: Exception) {
            _pluginState.value = PluginState.ERROR
            throw e
        }
    }
    
    override suspend fun start() {
        if (!_isInitialized) {
            throw IllegalStateException("Plugin must be initialized before starting")
        }
        
        if (_isStarted) {
            return
        }
        
        try {
            _pluginState.value = PluginState.STARTING
            
            onStarting()
            
            _isStarted = true
            _pluginState.value = PluginState.RUNNING
            
            onStarted()
        } catch (e: Exception) {
            _pluginState.value = PluginState.ERROR
            throw e
        }
    }
    
    override suspend fun stop() {
        if (!_isStarted) {
            return
        }
        
        try {
            _pluginState.value = PluginState.STOPPING
            
            onStopping()
            
            _isStarted = false
            _pluginState.value = PluginState.STOPPED
            
            onStopped()
        } catch (e: Exception) {
            _pluginState.value = PluginState.ERROR
            throw e
        }
    }
    
    override suspend fun destroy() {
        try {
            if (_isStarted) {
                stop()
            }
            
            onDestroying()
            
            _isInitialized = false
            _pluginState.value = PluginState.INSTALLED
            
            onDestroyed()
        } catch (e: Exception) {
            _pluginState.value = PluginState.ERROR
            throw e
        }
    }
    
    /**
     * 插件正在初始化回调
     */
    protected open suspend fun onInitializing() {
        // 子类可以重写
    }
    
    /**
     * 插件已初始化回调
     */
    protected open suspend fun onInitialized() {
        // 子类可以重写
    }
    
    /**
     * 插件正在启动回调
     */
    protected open suspend fun onStarting() {
        // 子类可以重写
    }
    
    /**
     * 插件已启动回调
     */
    protected open suspend fun onStarted() {
        // 子类可以重写
    }
    
    /**
     * 插件正在停止回调
     */
    protected open suspend fun onStopping() {
        // 子类可以重写
    }
    
    /**
     * 插件已停止回调
     */
    protected open suspend fun onStopped() {
        // 子类可以重写
    }
    
    /**
     * 插件正在销毁回调
     */
    protected open suspend fun onDestroying() {
        // 子类可以重写
    }
    
    /**
     * 插件已销毁回调
     */
    protected open suspend fun onDestroyed() {
        // 子类可以重写
    }
    
    /**
     * 插件启用状态变化回调
     */
    protected open fun onEnabledChanged(enabled: Boolean) {
        // 子类可以重写
    }
    
    /**
     * 获取插件配置存储
     */
    protected fun getConfigStorage(): IPluginConfigStorage {
        return pluginHost.getPluginConfigStorage(pluginId)
    }
    
    /**
     * 获取插件消息通信器
     */
    protected fun getMessenger(): IPluginMessenger {
        return pluginHost.getPluginMessenger()
    }
    
    /**
     * 发送消息到其他插件
     */
    protected suspend fun sendMessage(
        targetPluginId: String,
        messageType: String,
        data: Map<String, String> = emptyMap()
    ): PluginMessage? {
        val message = PluginMessage.create(
            type = messageType,
            sourcePluginId = pluginId,
            targetPluginId = targetPluginId,
            data = data
        )
        return getMessenger().sendMessage(targetPluginId, message)
    }
    
    /**
     * 广播消息到所有插件
     */
    protected suspend fun broadcastMessage(
        messageType: String,
        data: Map<String, String> = emptyMap()
    ) {
        val message = PluginMessage.create(
            type = messageType,
            sourcePluginId = pluginId,
            data = data
        )
        getMessenger().broadcastMessage(message)
    }
    
    /**
     * 注册消息处理器
     */
    protected fun registerMessageHandler(
        messageType: String,
        handler: suspend (PluginMessage) -> PluginMessage?
    ) {
        getMessenger().registerMessageHandler(messageType, handler)
    }
    
    /**
     * 注销消息处理器
     */
    protected fun unregisterMessageHandler(messageType: String) {
        getMessenger().unregisterMessageHandler(messageType)
    }
    
    /**
     * 通知插件事件
     */
    protected suspend fun notifyEvent(event: PluginEvent) {
        pluginHost.notifyPluginEvent(event)
    }
}