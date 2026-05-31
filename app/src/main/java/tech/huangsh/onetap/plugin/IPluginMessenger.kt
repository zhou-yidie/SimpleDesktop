package tech.huangsh.onetap.plugin

import kotlinx.coroutines.flow.Flow

/**
 * 插件间通信接口
 */
interface IPluginMessenger {
    /**
     * 发送消息到指定插件
     */
    suspend fun sendMessage(targetPluginId: String, message: PluginMessage): PluginMessage?
    
    /**
     * 广播消息到所有插件
     */
    suspend fun broadcastMessage(message: PluginMessage)
    
    /**
     * 订阅来自指定插件的消息
     */
    fun subscribeToMessages(sourcePluginId: String): Flow<PluginMessage>
    
    /**
     * 订阅指定类型的消息
     */
    fun subscribeToMessageType(messageType: String): Flow<PluginMessage>
    
    /**
     * 注册消息处理器
     */
    fun registerMessageHandler(messageType: String, handler: suspend (PluginMessage) -> PluginMessage?)
    
    /**
     * 注销消息处理器
     */
    fun unregisterMessageHandler(messageType: String)
}