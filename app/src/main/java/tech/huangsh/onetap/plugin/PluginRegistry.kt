package tech.huangsh.onetap.plugin

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import java.util.concurrent.ConcurrentHashMap
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.jvm.JvmSuppressWildcards

/**
 * 插件注册中心
 * 负责管理插件的注册、发现和生命周期
 */
@Singleton
class PluginRegistry @Inject constructor(
    private val pluginLoader: PluginLoader,
    private val pluginManager: PluginManager,
    private val builtinPlugins: Set<@JvmSuppressWildcards IPlugin>
) {
    
    // 已注册的插件映射
    private val registeredPlugins = ConcurrentHashMap<String, IPlugin>()
    
    // 注册状态流
    private val _registrationState = MutableStateFlow<RegistrationState>(RegistrationState.Idle)
    val registrationState: Flow<RegistrationState> = _registrationState.asStateFlow()
    
    // 操作互斥锁
    private val mutex = Mutex()
    
    /**
     * 注册状态枚举
     */
    enum class RegistrationState {
        Idle,           // 空闲
        Registering,    // 注册中
        Unregistering,  // 注销中
        Error           // 错误
    }
    
    /**
     * 注册单个插件
     */
    suspend fun registerPlugin(plugin: IPlugin): Boolean {
        return mutex.withLock {
            try {
                _registrationState.value = RegistrationState.Registering
                
                // 检查插件是否已注册
                if (registeredPlugins.containsKey(plugin.pluginId)) {
                    return@withLock false
                }
                
                // 验证插件兼容性
                if (!pluginLoader.validatePlugin(plugin)) {
                    return@withLock false
                }
                
                // 检查依赖是否满足
                val dependencies = plugin.getDependencies()
                for (depId in dependencies) {
                    if (!registeredPlugins.containsKey(depId)) {
                        return@withLock false
                    }
                }
                
                // 安装插件到插件管理器
                val installed = pluginManager.installPlugin(plugin)
                if (installed) {
                    registeredPlugins[plugin.pluginId] = plugin
                }
                
                _registrationState.value = RegistrationState.Idle
                installed
            } catch (e: Exception) {
                _registrationState.value = RegistrationState.Error
                e.printStackTrace()
                false
            }
        }
    }
    
    /**
     * 注销单个插件
     */
    suspend fun unregisterPlugin(pluginId: String): Boolean {
        return mutex.withLock {
            try {
                _registrationState.value = RegistrationState.Unregistering
                
                // 检查插件是否已注册
                if (!registeredPlugins.containsKey(pluginId)) {
                    return@withLock false
                }
                
                // 检查是否有其他插件依赖此插件
                for (plugin in registeredPlugins.values) {
                    if (plugin.getDependencies().contains(pluginId)) {
                        return@withLock false
                    }
                }
                
                // 卸载插件
                val uninstalled = pluginManager.uninstallPlugin(pluginId)
                if (uninstalled) {
                    registeredPlugins.remove(pluginId)
                }
                
                _registrationState.value = RegistrationState.Idle
                uninstalled
            } catch (e: Exception) {
                _registrationState.value = RegistrationState.Error
                e.printStackTrace()
                false
            }
        }
    }
    
    /**
     * 注册所有内置插件
     */
    suspend fun registerAllBuiltinPlugins(): Boolean {
        return mutex.withLock {
            try {
                _registrationState.value = RegistrationState.Registering

                var success = true
                val sortedPlugins = sortPluginsByDependency(builtinPlugins.toList())

                for (plugin in sortedPlugins) {
                    val registered = registerPluginInternal(plugin)
                    if (!registered) {
                        success = false
                    }
                }

                _registrationState.value = RegistrationState.Idle
                success
            } catch (e: Exception) {
                _registrationState.value = RegistrationState.Error
                e.printStackTrace()
                false
            }
        }
    }
    
    /**
     * 注销所有插件
     */
    suspend fun unregisterAllPlugins(): Boolean {
        return mutex.withLock {
            try {
                _registrationState.value = RegistrationState.Unregistering
                
                val pluginIds = registeredPlugins.keys.toList()
                var success = true
                
                // 按依赖顺序的反序注销插件
                val sortedIds = sortPluginIdsByDependency(pluginIds).reversed()
                
                for (pluginId in sortedIds) {
                    val unregistered = unregisterPluginInternal(pluginId)
                    if (!unregistered) {
                        success = false
                    }
                }
                
                _registrationState.value = RegistrationState.Idle
                success
            } catch (e: Exception) {
                _registrationState.value = RegistrationState.Error
                e.printStackTrace()
                false
            }
        }
    }
    
    /**
     * 获取已注册的插件
     */
    fun getRegisteredPlugin(pluginId: String): IPlugin? {
        return registeredPlugins[pluginId]
    }
    
    /**
     * 获取所有已注册的插件
     */
    fun getAllRegisteredPlugins(): List<IPlugin> {
        return registeredPlugins.values.toList()
    }
    
    /**
     * 获取已启用的插件
     */
    fun getEnabledPlugins(): List<IPlugin> {
        return registeredPlugins.values.filter { it.isEnabled }
    }
    
    /**
     * 检查插件是否已注册
     */
    fun isPluginRegistered(pluginId: String): Boolean {
        return registeredPlugins.containsKey(pluginId)
    }
    
    /**
     * 启用插件
     */
    suspend fun enablePlugin(pluginId: String): Boolean {
        return pluginManager.enablePlugin(pluginId)
    }
    
    /**
     * 禁用插件
     */
    suspend fun disablePlugin(pluginId: String): Boolean {
        return pluginManager.disablePlugin(pluginId)
    }
    
    /**
     * 获取插件依赖图
     */
    fun getDependencyGraph(): Map<String, List<String>> {
        return registeredPlugins.mapValues { (_, plugin) ->
            plugin.getDependencies()
        }
    }
    
    /**
     * 内部注册插件方法，不加锁
     */
    private suspend fun registerPluginInternal(plugin: IPlugin): Boolean {
        return try {
            // 检查插件是否已注册
            if (registeredPlugins.containsKey(plugin.pluginId)) {
                return false
            }
            
            // 验证插件兼容性
            if (!pluginLoader.validatePlugin(plugin)) {
                return false
            }
            
            // 检查依赖是否满足
            val dependencies = plugin.getDependencies()
            for (depId in dependencies) {
                if (!registeredPlugins.containsKey(depId)) {
                    return false
                }
            }
            
            // 安装插件到插件管理器
            val installed = pluginManager.installPlugin(plugin)
            if (installed) {
                registeredPlugins[plugin.pluginId] = plugin
            }
            
            installed
        } catch (e: Exception) {
            e.printStackTrace()
            false
        }
    }
    
    /**
     * 内部注销插件方法，不加锁
     */
    private suspend fun unregisterPluginInternal(pluginId: String): Boolean {
        return try {
            // 检查插件是否已注册
            if (!registeredPlugins.containsKey(pluginId)) {
                return false
            }
            
            // 检查是否有其他插件依赖此插件
            for (plugin in registeredPlugins.values) {
                if (plugin.getDependencies().contains(pluginId)) {
                    return false
                }
            }
            
            // 卸载插件
            val uninstalled = pluginManager.uninstallPlugin(pluginId)
            if (uninstalled) {
                registeredPlugins.remove(pluginId)
            }
            
            uninstalled
        } catch (e: Exception) {
            e.printStackTrace()
            false
        }
    }
    
    /**
     * 按依赖顺序排序插件
     */
    private fun sortPluginsByDependency(plugins: List<IPlugin>): List<IPlugin> {
        val result = mutableListOf<IPlugin>()
        val visited = mutableSetOf<String>()
        val visiting = mutableSetOf<String>()
        val pluginMap = plugins.associateBy { it.pluginId }
        
        fun visit(pluginId: String) {
            if (pluginId in visiting) {
                throw RuntimeException("Circular dependency detected")
            }
            if (pluginId in visited) {
                return
            }
            
            visiting.add(pluginId)
            pluginMap[pluginId]?.getDependencies()?.forEach { dep ->
                visit(dep)
            }
            visiting.remove(pluginId)
            visited.add(pluginId)
            pluginMap[pluginId]?.let { result.add(it) }
        }
        
        plugins.forEach { plugin ->
            if (plugin.pluginId !in visited) {
                visit(plugin.pluginId)
            }
        }
        
        return result
    }
    
    /**
     * 按依赖顺序排序插件ID
     */
    private fun sortPluginIdsByDependency(pluginIds: List<String>): List<String> {
        val result = mutableListOf<String>()
        val visited = mutableSetOf<String>()
        val visiting = mutableSetOf<String>()
        
        fun visit(pluginId: String) {
            if (pluginId in visiting) {
                throw RuntimeException("Circular dependency detected")
            }
            if (pluginId in visited) {
                return
            }
            
            visiting.add(pluginId)
            registeredPlugins[pluginId]?.getDependencies()?.forEach { dep ->
                visit(dep)
            }
            visiting.remove(pluginId)
            visited.add(pluginId)
            result.add(pluginId)
        }
        
        pluginIds.forEach { pluginId ->
            if (pluginId !in visited) {
                visit(pluginId)
            }
        }
        
        return result
    }
}