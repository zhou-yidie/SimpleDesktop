package tech.huangsh.onetap.plugin.impl

import android.content.Context
import tech.huangsh.onetap.data.model.AppInfo
import tech.huangsh.onetap.data.repository.AppRepository
import tech.huangsh.onetap.plugin.*
import tech.huangsh.onetap.ui.screens.app.AppManagementScreen
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.first
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 应用管理插件
 * 提供应用管理功能
 */
@Singleton
class AppPlugin @Inject constructor(
    @ApplicationContext private val appContext: Context,
    private val appRepository: AppRepository
) : BasePlugin(), IPluginEventListener {
    
    override val pluginId: String = "app_plugin"
    override val name: String = "应用管理"
    override val version: String = "1.0.0"
    override val description: String = "提供应用管理功能，包括已安装应用扫描、常用应用管理和启动"
    override val author: String = "SimpleDesktop Team"
    
    override suspend fun onInitializing() {
        super.onInitializing()
        
        // 初始化插件配置
        val config = getConfigStorage()
        if (!config.contains("initialized")) {
            // 设置默认配置
            config.setValue("max_app_count", 20)
            config.setValue("auto_refresh", true)
            config.setValue("show_system_apps", false)
            config.setValue("initialized", true)
        }
        
        // 初始扫描应用
        scanApps()
    }
    
    override suspend fun onStarted() {
        super.onStarted()
        
        // 注册消息处理器
        registerMessageHandler("get_apps") { message ->
            handleGetApps(message)
        }
        
        registerMessageHandler("refresh_apps") { message ->
            handleRefreshApps(message)
        }
        
        registerMessageHandler("add_app") { message ->
            handleAddApp(message)
        }
        
        registerMessageHandler("remove_app") { message ->
            handleRemoveApp(message)
        }
        
        registerMessageHandler("reorder_apps") { message ->
            handleReorderApps(message)
        }
        
        registerMessageHandler("launch_app") { message ->
            handleLaunchApp(message)
        }
        
        registerMessageHandler("get_app_ui") { message ->
            handleGetAppUI(message)
        }
        
        registerMessageHandler("get_home_apps") { message ->
            handleGetHomeApps(message)
        }
    }
    
    override fun getMainComponent(): Any? {
        return AppManagementScreenRoute
    }
    
    override fun getConfigScreen(): Any? {
        return AppPluginConfigScreen
    }
    
    override suspend fun onPluginEvent(event: PluginEvent) {
        when (event) {
            is PluginEvent.AppStarted -> {
                // 应用启动时，检查是否需要自动刷新应用列表
                val config = getConfigStorage()
                val autoRefresh = config.getBoolean("auto_refresh", true)
                
                if (autoRefresh) {
                    scanApps()
                }
            }
            else -> {
                // 其他事件处理
            }
        }
    }
    
    /**
     * 扫描已安装的应用
     */
    private suspend fun scanApps() {
        try {
            android.util.Log.d("AppPlugin", "开始扫描已安装应用...")
            appRepository.scanInstalledApps()
            android.util.Log.d("AppPlugin", "应用扫描完成")
        } catch (e: Exception) {
            android.util.Log.e("AppPlugin", "扫描应用失败", e)
            e.printStackTrace()
        }
    }
    
    /**
     * 处理获取应用列表的请求
     */
    private suspend fun handleGetApps(message: PluginMessage): PluginMessage {
        return try {
            android.util.Log.d("AppPlugin", "处理获取应用列表请求")
            
            val showSystemApps = message.data["showSystemApps"]?.toBoolean() ?: false
            val apps = appRepository.allApps.first()
            
            // 将应用信息转换为简单的键值对格式
            val appsData = apps.mapIndexed { index, app ->
                // 每个应用的数据使用 "app_{index}_{field}" 的格式
                listOf(
                    "app_${index}_packageName" to app.packageName,
                    "app_${index}_appName" to app.appName,
                    "app_${index}_order" to app.order.toString(),
                    "app_${index}_isEnabled" to app.isEnabled.toString()
                )
            }.flatten().toMap().toMutableMap()
            
            // 添加应用数量
            appsData["count"] = apps.size.toString()
            
            android.util.Log.d("AppPlugin", "返回 ${apps.size} 个应用")
            
            PluginMessage.createResponse(
                message,
                appsData
            )
        } catch (e: Exception) {
            android.util.Log.e("AppPlugin", "获取应用列表失败", e)
            e.printStackTrace()
            return PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理刷新应用列表的请求
     */
    private suspend fun handleRefreshApps(message: PluginMessage): PluginMessage {
        return try {
            scanApps()
            PluginMessage.createResponse(
                message,
                mapOf("success" to "true")
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理添加常用应用的请求
     */
    private suspend fun handleAddApp(message: PluginMessage): PluginMessage {
        return try {
            val packageName = message.data["packageName"] ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Missing package name")
            )
            
            val app = appRepository.getAppByPackage(packageName)
            if (app != null && !app.isEnabled) {
                val maxOrder = appRepository.getMaxEnabledAppOrder() ?: -1
                val updatedApp = app.copy(
                    isEnabled = true,
                    order = maxOrder + 1
                )
                appRepository.updateApp(updatedApp)
                
                PluginMessage.createResponse(
                    message,
                    mapOf("success" to "true")
                )
            } else {
                PluginMessage.createResponse(
                    message,
                    mapOf("error" to "App not found or already enabled")
                )
            }
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理移除常用应用的请求
     */
    private suspend fun handleRemoveApp(message: PluginMessage): PluginMessage {
        return try {
            val packageName = message.data["packageName"] ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Missing package name")
            )
            
            val app = appRepository.getAppByPackage(packageName)
            if (app != null && app.isEnabled) {
                val updatedApp = app.copy(isEnabled = false)
                appRepository.updateApp(updatedApp)
                
                PluginMessage.createResponse(
                    message,
                    mapOf("success" to "true")
                )
            } else {
                PluginMessage.createResponse(
                    message,
                    mapOf("error" to "App not found or already disabled")
                )
            }
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理重新排序应用的请求
     */
    private suspend fun handleReorderApps(message: PluginMessage): PluginMessage {
        return try {
            val packageName = message.data["packageName"] ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Missing package name")
            )
            
            val fromPosition = message.data["fromPosition"]?.toIntOrNull() ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Invalid from position")
            )
            
            val toPosition = message.data["toPosition"]?.toIntOrNull() ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Invalid to position")
            )
            
            appRepository.moveApp(packageName, fromPosition, toPosition)
            
            PluginMessage.createResponse(
                message,
                mapOf("success" to "true")
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理启动应用的请求
     */
    private suspend fun handleLaunchApp(message: PluginMessage): PluginMessage {
        return try {
            val packageName = message.data["packageName"] ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Missing package name")
            )
            
            val intent = appRepository.launchApp(packageName)
            if (intent != null) {
                context.startActivity(intent)
                PluginMessage.createResponse(
                    message,
                    mapOf("success" to "true")
                )
            } else {
                PluginMessage.createResponse(
                    message,
                    mapOf("error" to "Failed to create launch intent")
                )
            }
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理获取应用UI的请求
     */
    private suspend fun handleGetAppUI(message: PluginMessage): PluginMessage {
        return try {
            val screenType = message.data["screenType"] ?: "management"
            
            val uiComponent = when (screenType) {
                "management" -> "AppManagementScreen"
                else -> "AppManagementScreen"
            }
            
            PluginMessage.createResponse(
                message,
                mapOf("uiComponent" to uiComponent)
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理获取主页应用的请求
     */
    private suspend fun handleGetHomeApps(message: PluginMessage): PluginMessage {
        return try {
            val limit = message.data["limit"]?.toIntOrNull() ?: 2
            val apps = appRepository.enabledApps.first().take(limit)
            
            val appsJson = apps.map { app ->
                mapOf(
                    "packageName" to app.packageName,
                    "appName" to app.appName,
                    "order" to app.order.toString()
                )
            }
            
            PluginMessage.createResponse(
                message,
                mapOf(
                    "apps" to appsJson.toString(),
                    "count" to appsJson.size.toString()
                )
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
}

/**
 * 应用管理屏幕路由
 */
object AppManagementScreenRoute

/**
 * 应用插件配置屏幕
 */
object AppPluginConfigScreen