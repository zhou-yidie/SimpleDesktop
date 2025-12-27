package tech.huangsh.onetap.plugin

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringSetPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import java.util.concurrent.ConcurrentHashMap
import javax.inject.Inject
import javax.inject.Singleton

val Context.pluginManagerDataStore: DataStore<Preferences> by preferencesDataStore(name = "plugin_manager")

/**
 * 插件管理器实现
 * 负责插件的安装、卸载、启用、禁用等管理功能
 */
@Singleton
class PluginManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val pluginMessenger: PluginMessenger
) : IPluginHost {
    
    private val dataStore = context.pluginManagerDataStore
    
    // 已安装的插件映射
    private val installedPlugins = ConcurrentHashMap<String, IPlugin>()
    
    // 已安装的插件列表状态流
    private val _installedPluginsFlow = MutableStateFlow<List<IPlugin>>(emptyList())
    val installedPluginsFlow: StateFlow<List<IPlugin>> = _installedPluginsFlow.asStateFlow()
    
    // 已启用的插件列表状态流
    private val _enabledPluginsFlow = MutableStateFlow<List<IPlugin>>(emptyList())
    val enabledPluginsFlow: StateFlow<List<IPlugin>> = _enabledPluginsFlow.asStateFlow()
    
    // 插件操作互斥锁
    private val pluginMutex = Mutex()
    
    // DataStore 键
    private val ENABLED_PLUGINS_KEY = stringSetPreferencesKey("enabled_plugins")
    
    init {
        // 从配置中加载已启用的插件
        // TODO: 临时注释，修复后启用
        // loadEnabledPlugins()
    }
    
    override fun getContext(): Context = context
    
    override fun getInstalledPlugins(): Flow<List<IPlugin>> {
        return _installedPluginsFlow.asStateFlow()
    }
    
    override fun getEnabledPlugins(): Flow<List<IPlugin>> {
        return _enabledPluginsFlow.asStateFlow()
    }
    
    override fun getPlugin(pluginId: String): IPlugin? {
        return installedPlugins[pluginId]
    }
    
    override suspend fun installPlugin(plugin: IPlugin): Boolean {
        return pluginMutex.withLock {
            try {
                // 检查插件是否已安装
                if (installedPlugins.containsKey(plugin.pluginId)) {
                    return@withLock false
                }
                
                // 检查依赖
                val dependencies = plugin.getDependencies()
                for (dependencyId in dependencies) {
                    if (!installedPlugins.containsKey(dependencyId)) {
                        return@withLock false
                    }
                }
                
                // 初始化插件
                plugin.initialize(context, this)
                
                // 添加到已安装列表
                installedPlugins[plugin.pluginId] = plugin
                
                // 更新UI状态
                updatePluginLists()
                
                // 通知插件安装事件
                notifyAllPlugins(PluginEvent.PluginInstalled(plugin.pluginId))
                
                return@withLock true
            } catch (e: Exception) {
                e.printStackTrace()
                return@withLock false
            }
        }
    }
    
    override suspend fun uninstallPlugin(pluginId: String): Boolean {
        return pluginMutex.withLock {
            try {
                val plugin = installedPlugins[pluginId] ?: return@withLock false
                
                // 检查是否有其他插件依赖此插件
                checkDependents(pluginId)?.let { dependents ->
                    if (dependents.isNotEmpty()) {
                        return@withLock false
                    }
                }
                
                // 先禁用插件
                if (plugin.isEnabled) {
                    disablePlugin(pluginId)
                }
                
                // 销毁插件
                plugin.destroy()
                
                // 从已安装列表中移除
                installedPlugins.remove(pluginId)
                
                // 更新UI状态
                updatePluginLists()
                
                // 通知插件卸载事件
                notifyAllPlugins(PluginEvent.PluginUninstalled(pluginId))
                
                return@withLock true
            } catch (e: Exception) {
                e.printStackTrace()
                return@withLock false
            }
        }
    }
    
    override suspend fun enablePlugin(pluginId: String): Boolean {
        return pluginMutex.withLock {
            try {
                val plugin = installedPlugins[pluginId] ?: return@withLock false
                
                if (!plugin.isEnabled) {
                    // 启动插件
                    plugin.start()
                    plugin.isEnabled = true
                    
                    // 更新启用列表
                    updateEnabledPluginsInDataStore(pluginId, add = true)
                    updatePluginLists()
                    
                    // 通知插件启用事件
                    notifyAllPlugins(PluginEvent.PluginEnabled(pluginId))
                }
                
                return@withLock true
            } catch (e: Exception) {
                e.printStackTrace()
                return@withLock false
            }
        }
    }
    
    override suspend fun disablePlugin(pluginId: String): Boolean {
        return pluginMutex.withLock {
            try {
                val plugin = installedPlugins[pluginId] ?: return@withLock false
                
                if (plugin.isEnabled) {
                    // 停止插件
                    plugin.stop()
                    plugin.isEnabled = false
                    
                    // 更新启用列表
                    updateEnabledPluginsInDataStore(pluginId, add = false)
                    updatePluginLists()
                    
                    // 通知插件禁用事件
                    notifyAllPlugins(PluginEvent.PluginDisabled(pluginId))
                }
                
                return@withLock true
            } catch (e: Exception) {
                e.printStackTrace()
                return@withLock false
            }
        }
    }
    
    override suspend fun notifyPluginEvent(event: PluginEvent) {
        notifyAllPlugins(event)
    }
    
    override fun getPluginMessenger(): IPluginMessenger {
        return pluginMessenger
    }
    
    override fun getPluginConfigStorage(pluginId: String): IPluginConfigStorage {
        return PluginConfigStorageWrapper(pluginId, context)
    }
    
    /**
     * 加载已启用的插件
     */
    private suspend fun loadEnabledPlugins() {
        dataStore.data.collect { preferences ->
            val enabledPluginIds = preferences[ENABLED_PLUGINS_KEY] ?: emptySet()
            
            // 启用配置中记录的插件
            enabledPluginIds.forEach { pluginId ->
                installedPlugins[pluginId]?.let { plugin ->
                    if (!plugin.isEnabled) {
                        try {
                            plugin.start()
                            plugin.isEnabled = true
                        } catch (e: Exception) {
                            e.printStackTrace()
                        }
                    }
                }
            }
            
            updatePluginLists()
        }
    }
    
    /**
     * 更新DataStore中的启用插件列表
     */
    private suspend fun updateEnabledPluginsInDataStore(pluginId: String, add: Boolean) {
        dataStore.edit { preferences ->
            val enabledPlugins = preferences[ENABLED_PLUGINS_KEY]?.toMutableSet() ?: mutableSetOf()
            
            if (add) {
                enabledPlugins.add(pluginId)
            } else {
                enabledPlugins.remove(pluginId)
            }
            
            preferences[ENABLED_PLUGINS_KEY] = enabledPlugins
        }
    }
    
    /**
     * 更新插件列表状态
     */
    private fun updatePluginLists() {
        _installedPluginsFlow.value = installedPlugins.values.toList()
        _enabledPluginsFlow.value = installedPlugins.values.filter { it.isEnabled }
    }
    
    /**
     * 检查依赖此插件的其他插件
     */
    private fun checkDependents(pluginId: String): Set<String>? {
        return installedPlugins.values
            .filter { it.getDependencies().contains(pluginId) }
            .map { it.pluginId }
            .toSet()
    }
    
    /**
     * 通知所有插件事件
     */
    private suspend fun notifyAllPlugins(event: PluginEvent) {
        installedPlugins.values.forEach { plugin ->
            try {
                if (plugin.isEnabled) {
                    // 如果插件实现了事件监听接口，通知事件
                    if (plugin is IPluginEventListener) {
                        plugin.onPluginEvent(event)
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    /**
     * 获取插件依赖图
     */
    fun getDependencyGraph(): Map<String, List<String>> {
        return installedPlugins.mapValues { (_, plugin) ->
            plugin.getDependencies()
        }
    }
    
    /**
     * 拓扑排序插件启动顺序
     */
    fun getStartupOrder(): List<String> {
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
            installedPlugins[pluginId]?.getDependencies()?.forEach { dep ->
                visit(dep)
            }
            visiting.remove(pluginId)
            visited.add(pluginId)
            result.add(pluginId)
        }
        
        installedPlugins.keys.forEach { pluginId ->
            if (pluginId !in visited) {
                visit(pluginId)
            }
        }
        
        return result
    }
    
    /**
     * 启用所有插件
     */
    suspend fun enableAllPlugins() {
        val startupOrder = getStartupOrder()
        
        startupOrder.forEach { pluginId ->
            enablePlugin(pluginId)
        }
    }
    
    /**
     * 禁用所有插件
     */
    suspend fun disableAllPlugins() {
        val shutdownOrder = getStartupOrder().reversed()
        
        shutdownOrder.forEach { pluginId ->
            disablePlugin(pluginId)
        }
    }
}