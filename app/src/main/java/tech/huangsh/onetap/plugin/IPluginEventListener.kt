package tech.huangsh.onetap.plugin

/**
 * 插件事件监听器接口
 * 插件可以实现此接口以接收系统事件通知
 */
interface IPluginEventListener {
    /**
     * 插件事件回调
     */
    suspend fun onPluginEvent(event: PluginEvent)
}