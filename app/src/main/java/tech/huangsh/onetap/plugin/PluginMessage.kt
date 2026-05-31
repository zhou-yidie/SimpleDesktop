package tech.huangsh.onetap.plugin

import kotlinx.serialization.Serializable

/**
 * 插件间通信消息
 */
@Serializable
data class PluginMessage(
    /**
     * 消息类型
     */
    val type: String,
    
    /**
     * 消息内容
     */
    val data: Map<String, String> = emptyMap(),
    
    /**
     * 源插件ID
     */
    val sourcePluginId: String,
    
    /**
     * 目标插件ID（可选，为空则广播）
     */
    val targetPluginId: String? = null,
    
    /**
     * 时间戳
     */
    val timestamp: Long = System.currentTimeMillis(),
    
    /**
     * 消息ID（用于跟踪请求-响应）
     */
    val messageId: String? = null,
    
    /**
     * 是否是响应消息
     */
    val isResponse: Boolean = false
) {
    companion object {
        /**
         * 创建消息
         */
        fun create(
            type: String,
            sourcePluginId: String,
            targetPluginId: String? = null,
            data: Map<String, String> = emptyMap(),
            messageId: String? = null
        ): PluginMessage {
            return PluginMessage(
                type = type,
                data = data,
                sourcePluginId = sourcePluginId,
                targetPluginId = targetPluginId,
                messageId = messageId
            )
        }
        
        /**
         * 创建响应消息
         */
        fun createResponse(
            originalMessage: PluginMessage,
            data: Map<String, String> = emptyMap()
        ): PluginMessage {
            return PluginMessage(
                type = "response:${originalMessage.type}",
                data = data,
                sourcePluginId = originalMessage.targetPluginId ?: "",
                targetPluginId = originalMessage.sourcePluginId,
                messageId = originalMessage.messageId,
                isResponse = true
            )
        }
    }
}