package tech.huangsh.onetap.plugin

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.filter
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch
import java.util.concurrent.ConcurrentHashMap
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 插件消息通信实现
 * 使用 SharedFlow 替换已废弃的 BroadcastChannel，确保背压与生命周期安全
 */
@Singleton
class PluginMessenger @Inject constructor() : IPluginMessenger {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    // 消息处理器映射：消息类型 -> 处理器函数
    private val messageHandlers = ConcurrentHashMap<String, suspend (PluginMessage) -> PluginMessage?>()

    // 插件订阅流：源插件ID -> SharedFlow
    private val pluginFlows = ConcurrentHashMap<String, MutableSharedFlow<PluginMessage>>()

    // 消息类型订阅流：消息类型 -> SharedFlow
    private val messageTypeFlows = ConcurrentHashMap<String, MutableSharedFlow<PluginMessage>>()

    override suspend fun sendMessage(targetPluginId: String, message: PluginMessage): PluginMessage? {
        return try {
            val handler = messageHandlers[message.type]
            handler?.invoke(message)
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }

    override suspend fun broadcastMessage(message: PluginMessage) {
        try {
            // 通知按插件订阅者
            pluginFlows[message.sourcePluginId]?.emit(message)

            // 通知按类型订阅者
            messageTypeFlows[message.type]?.emit(message)

            // 调用处理器（异步，避免阻塞）
            messageHandlers[message.type]?.let { handler ->
                scope.launch {
                    try {
                        handler(message)
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    override fun subscribeToMessages(sourcePluginId: String): Flow<PluginMessage> {
        val flow = pluginFlows.getOrPut(sourcePluginId) {
            MutableSharedFlow(extraBufferCapacity = 64)
        }
        return flow.asSharedFlow()
    }

    override fun subscribeToMessageType(messageType: String): Flow<PluginMessage> {
        val flow = messageTypeFlows.getOrPut(messageType) {
            MutableSharedFlow(extraBufferCapacity = 64)
        }
        return flow.asSharedFlow()
    }

    override fun registerMessageHandler(
        messageType: String,
        handler: suspend (PluginMessage) -> PluginMessage?
    ) {
        messageHandlers[messageType] = handler
    }

    override fun unregisterMessageHandler(messageType: String) {
        messageHandlers.remove(messageType)
    }

    /**
     * 清理资源
     */
    fun cleanup() {
        pluginFlows.clear()
        messageTypeFlows.clear()
        messageHandlers.clear()
    }
}