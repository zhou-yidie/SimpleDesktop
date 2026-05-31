package tech.huangsh.onetap.plugin

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import dagger.hilt.android.testing.HiltAndroidRule
import dagger.hilt.android.testing.HiltAndroidTest
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import tech.huangsh.onetap.plugin.impl.ContactPlugin
import tech.huangsh.onetap.plugin.impl.AppPlugin
import tech.huangsh.onetap.plugin.impl.WeatherPlugin
import javax.inject.Inject

/**
 * 插件系统测试
 */
@HiltAndroidTest
class PluginSystemTest {

    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @Inject
    lateinit var pluginRegistry: PluginRegistry

    @Inject
    lateinit var pluginManager: PluginManager

    @Inject
    lateinit var contactPlugin: ContactPlugin

    @Inject
    lateinit var appPlugin: AppPlugin

    @Inject
    lateinit var weatherPlugin: WeatherPlugin

    private lateinit var context: Context

    @Before
    fun setup() {
        hiltRule.inject()
        context = ApplicationProvider.getApplicationContext()
    }

    /**
     * 测试插件注册
     */
    @Test
    fun testPluginRegistration() = runBlocking {
        // 注册联系人插件
        val contactRegistered = pluginRegistry.registerPlugin(contactPlugin)
        assert(contactRegistered) { "Failed to register contact plugin" }
        assert(pluginRegistry.isPluginRegistered(contactPlugin.pluginId))

        // 注册应用插件
        val appRegistered = pluginRegistry.registerPlugin(appPlugin)
        assert(appRegistered) { "Failed to register app plugin" }
        assert(pluginRegistry.isPluginRegistered(appPlugin.pluginId))

        // 注册天气插件
        val weatherRegistered = pluginRegistry.registerPlugin(weatherPlugin)
        assert(weatherRegistered) { "Failed to register weather plugin" }
        assert(pluginRegistry.isPluginRegistered(weatherPlugin.pluginId))
    }

    /**
     * 测试插件启用和禁用
     */
    @Test
    fun testPluginEnableDisable() = runBlocking {
        // 先注册所有插件
        pluginRegistry.registerAllBuiltinPlugins()

        // 启用联系人插件
        val contactEnabled = pluginRegistry.enablePlugin(contactPlugin.pluginId)
        assert(contactEnabled) { "Failed to enable contact plugin" }
        assert(contactPlugin.isEnabled)

        // 禁用联系人插件
        val contactDisabled = pluginRegistry.disablePlugin(contactPlugin.pluginId)
        assert(contactDisabled) { "Failed to disable contact plugin" }
        assert(!contactPlugin.isEnabled)
    }

    /**
     * 测试插件消息通信
     */
    @Test
    fun testPluginMessageCommunication() = runBlocking {
        // 先注册并启用联系人插件
        pluginRegistry.registerPlugin(contactPlugin)
        pluginRegistry.enablePlugin(contactPlugin.pluginId)

        // 发送消息到联系人插件
        val messenger = pluginManager.getPluginMessenger()
        val message = PluginMessage.create(
            type = "get_contacts",
            sourcePluginId = "test_plugin",
            targetPluginId = contactPlugin.pluginId
        )

        val response = messenger.sendMessage(contactPlugin.pluginId, message)
        assert(response != null) { "Failed to get response from contact plugin" }
        assert(!response!!.data["error"].isNullOrEmpty().not()) { "Got error response: ${response.data["error"]}" }
    }

    /**
     * 测试插件配置存储
     */
    @Test
    fun testPluginConfigStorage() = runBlocking {
        // 获取联系人插件的配置存储
        val configStorage = pluginManager.getPluginConfigStorage(contactPlugin.pluginId)

        // 测试设置和获取配置
        configStorage.setValue("test_key", "test_value")
        val value = configStorage.getValue("test_key")
        assert(value == "test_value") { "Failed to get stored config value" }

        // 测试布尔值配置
        configStorage.setValue("test_bool", true)
        val boolValue = configStorage.getBoolean("test_bool")
        assert(boolValue) { "Failed to get stored boolean config value" }

        // 测试整数配置
        configStorage.setValue("test_int", 42)
        val intValue = configStorage.getInt("test_int")
        assert(intValue == 42) { "Failed to get stored int config value" }
    }

    /**
     * 测试插件依赖图
     */
    @Test
    fun testPluginDependencyGraph() = runBlocking {
        // 注册所有插件
        pluginRegistry.registerAllBuiltinPlugins()

        // 获取依赖图
        val dependencyGraph = pluginRegistry.getDependencyGraph()
        assert(dependencyGraph.isNotEmpty()) { "Dependency graph should not be empty" }

        // 检查每个插件的依赖
        assert(dependencyGraph.containsKey(contactPlugin.pluginId))
        assert(dependencyGraph.containsKey(appPlugin.pluginId))
        assert(dependencyGraph.containsKey(weatherPlugin.pluginId))
    }
}