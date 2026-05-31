# SimpleDesktop 插件架构

## 概述

SimpleDesktop插件架构是一个灵活、可扩展的插件系统，允许将应用功能模块化为独立的插件，降低功能模块间的耦合度，并支持动态加载和卸载插件。

## 架构组成

### 核心接口与类

1. **IPlugin** - 插件基础接口
   - 所有插件必须实现此接口
   - 定义了插件的生命周期方法：初始化、启动、停止、销毁
   - 提供插件的基本信息：ID、名称、版本、描述等

2. **BasePlugin** - 插件基础抽象类
   - 实现IPlugin接口，提供默认实现
   - 简化插件开发，提供状态管理和事件回调
   - 提供便捷的配置存储和消息通信方法

3. **IPluginHost** - 插件宿主接口
   - 提供插件运行环境和API支持
   - 负责插件的安装、卸载、启用、禁用
   - 提供插件间通信和配置存储接口

4. **PluginManager** - 插件管理器
   - 实现IPluginHost接口
   - 负责插件的生命周期管理
   - 使用DataStore持久化插件启用状态

### 插件通信系统

1. **IPluginMessenger** - 插件消息通信接口
   - 提供点对点和广播消息功能
   - 支持消息类型订阅和处理
   - 实现插件间的解耦通信

2. **PluginMessage** - 插件消息类
   - 使用Kotlin序列化，支持类型安全的消息传递
   - 包含消息类型、数据、源插件、目标插件等信息
   - 支持请求-响应模式的消息交互

### 插件配置系统

1. **IPluginConfigStorage** - 插件配置存储接口
   - 提供键值对配置存储
   - 支持字符串、布尔、整数、浮点数等类型
   - 提供配置变更监听功能

2. **PluginConfigStorage** - 配置存储实现
   - 使用Android DataStore Preferences实现
   - 为每个插件提供独立的配置空间
   - 支持异步读写和流式观察

### 插件加载机制

1. **PluginLoader** - 插件加载器
   - 支持内置插件和外部插件加载
   - 提供APK和Dex文件加载能力
   - 验证插件兼容性和依赖关系

2. **PluginRegistry** - 插件注册中心
   - 管理插件的注册、发现和生命周期
   - 处理插件依赖关系和拓扑排序
   - 协调插件管理器和加载器的工作

## 内置插件

1. **ContactPlugin** - 联系人插件
   - 提供联系人管理核心功能（CRUD）。
   - **增强通话链路**: 实现了高度同步的通话启动逻辑，支持电话直拨与微信音视频全自动拨号。
   - **焦点治理策略**: 插件内部集成 UI 退避机制，在调起外部应用（如微信）时，第一时间释放宿主 UI 焦点，确保无障碍服务能够顺利接管目标界面。
   - **多模触发支持**: 同时兼容手动点击触发与 `VoiceAssistant` 语义指令触发。

2. **AppPlugin** - 应用管理插件
   - 提供应用管理功能
   - 支持应用扫描、启动和排序
   - 管理常用应用列表

3. **WeatherPlugin** - 天气插件
   - 提供天气信息显示
   - 支持实时天气更新
   - 可配置更新频率和位置

## 使用示例

### 创建新插件

```kotlin
class MyPlugin @Inject constructor(
    @ApplicationContext private val appContext: Context
) : BasePlugin() {
    
    override val pluginId: String = "my_plugin"
    override val name: String = "我的插件"
    override val version: String = "1.0.0"
    override val description: String = "这是一个示例插件"
    override val author: String = "SimpleDesktop Team"
    
    override suspend fun onStarted() {
        super.onStarted()
        
        // 注册消息处理器
        registerMessageHandler("my_action") { message ->
            handleMyAction(message)
        }
    }
    
    private suspend fun handleMyAction(message: PluginMessage): PluginMessage {
        // 处理消息
        return PluginMessage.createResponse(
            message,
            mapOf("result" to "success")
        )
    }
}
```

### 注册插件

```kotlin
// 在AppModule中提供插件实例
@Provides
@Singleton
fun provideMyPlugin(
    @ApplicationContext context: Context
): MyPlugin {
    return MyPlugin(context)
}

// 在应用启动时注册插件
@HiltAndroidApp
class SimpleDesktopApp : Application() {
    @Inject
    lateinit var pluginRegistry: PluginRegistry
    
    override fun onCreate() {
        super.onCreate()
        
        // 注册插件
        lifecycleScope.launch {
            val myPlugin = MyPlugin(this@SimpleDesktopApp)
            pluginRegistry.registerPlugin(myPlugin)
        }
    }
}
```

### 插件间通信

```kotlin
// 发送消息到其他插件
val response = sendMessage(
    targetPluginId = "contact_plugin",
    messageType = "get_contacts",
    data = emptyMap()
)

// 处理响应
if (response != null) {
    val contactsJson = response.data["contacts"]
    // 处理联系人数据
}
```

## 优势

1. **模块化** - 将应用功能分解为独立模块，降低耦合度
2. **可扩展性** - 轻松添加新功能，无需修改核心代码
3. **可维护性** - 插件独立开发和测试，提高代码质量
4. **动态性** - 支持运行时加载、启用、禁用插件
5. **隔离性** - 插件故障不影响核心应用和其他插件

## 未来扩展

1. **插件市场** - 实现插件下载和自动更新
2. **沙箱机制** - 增强插件安全性和权限控制
3. **热更新** - 支持插件的热修复和更新
4. **插件依赖管理** - 更完善的依赖解析和版本管理
5. **插件性能监控** - 监控插件资源使用和性能指标