package tech.huangsh.onetap.plugin.impl

import android.content.Context
import tech.huangsh.onetap.data.model.WeatherInfo
import tech.huangsh.onetap.data.remote.WeatherService
import tech.huangsh.onetap.plugin.*
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 天气插件
 * 提供天气信息功能
 */
@Singleton
class WeatherPlugin @Inject constructor(
    @ApplicationContext private val appContext: Context,
    private val weatherService: WeatherService
) : BasePlugin(), IPluginEventListener {
    
    // 当前天气信息
    private var currentWeather: WeatherInfo? = null
    
    override val pluginId: String = "weather_plugin"
    override val name: String = "天气服务"
    override val version: String = "1.0.0"
    override val description: String = "提供天气信息显示和预警功能"
    override val author: String = "SimpleDesktop Team"
    
    override suspend fun onInitializing() {
        super.onInitializing()
        
        // 初始化插件配置
        val config = getConfigStorage()
        if (!config.contains("initialized")) {
            // 设置默认配置
            config.setValue("auto_update", true)
            config.setValue("update_interval", 3600) // 1小时
            config.setValue("show_weather_icon", true)
            config.setValue("show_temperature", true)
            config.setValue("initialized", true)
        }
        
        // 获取初始天气信息
        updateWeather()
    }
    
    override suspend fun onStarted() {
        super.onStarted()
        
        // 注册消息处理器
        registerMessageHandler("get_weather") { message ->
            handleGetWeather(message)
        }
        
        registerMessageHandler("update_weather") { message ->
            handleUpdateWeather(message)
        }
        
        registerMessageHandler("get_weather_forecast") { message ->
            handleGetWeatherForecast(message)
        }
        
        registerMessageHandler("set_weather_location") { message ->
            handleSetWeatherLocation(message)
        }
        
        registerMessageHandler("get_weather_ui") { message ->
            handleGetWeatherUI(message)
        }
        
        // 启动天气更新任务
        startWeatherUpdateTask()
    }
    
    override fun getMainComponent(): Any? {
        return WeatherPluginScreenRoute
    }
    
    override fun getConfigScreen(): Any? {
        return WeatherPluginConfigScreen
    }
    
    override suspend fun onPluginEvent(event: PluginEvent) {
        when (event) {
            is PluginEvent.AppStarted -> {
                // 应用启动时，检查是否需要自动更新天气
                val config = getConfigStorage()
                val autoUpdate = config.getBoolean("auto_update", true)
                
                if (autoUpdate) {
                    updateWeather()
                }
            }
            is PluginEvent.SettingsChanged -> {
                // 设置变更时，检查天气设置
                if (event.key == "weather_location") {
                    // 位置变更时，更新天气
                    updateWeather()
                }
            }
            else -> {
                // 其他事件处理
            }
        }
    }
    
    /**
     * 启动天气更新任务
     */
    private fun startWeatherUpdateTask() {
        launch {
            while (isEnabled) {
                try {
                    val config = getConfigStorage()
                    val autoUpdate = config.getBoolean("auto_update", true)
                    
                    if (autoUpdate) {
                        val updateInterval = config.getLong("update_interval", 3600) * 1000L
                        delay(updateInterval)
                        updateWeather()
                    } else {
                        delay(3600000L) // 1小时后再次检查
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                    delay(3600000L) // 出错后1小时后再试
                }
            }
        }
    }
    
    /**
     * 更新天气信息
     */
    private suspend fun updateWeather() {
        try {
            currentWeather = weatherService.getWeatherInfo()
            
            // 广播天气更新事件
            broadcastMessage(
                "weather_updated",
                mapOf(
                    "temperature" to (currentWeather?.temperature?.toString() ?: ""),
                    "weather" to (currentWeather?.weather ?: ""),
                    "weatherIcon" to (currentWeather?.weatherIcon ?: ""),
                    "city" to (currentWeather?.city ?: ""),
                    "humidity" to (currentWeather?.humidity?.toString() ?: ""),
                    "windSpeed" to (currentWeather?.windSpeed?.toString() ?: "")
                )
            )
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    /**
     * 处理获取天气信息的请求
     */
    private suspend fun handleGetWeather(message: PluginMessage): PluginMessage {
        return try {
            if (currentWeather == null) {
                updateWeather()
            }
            
            PluginMessage.createResponse(
                message,
                mapOf(
                    "temperature" to (currentWeather?.temperature?.toString() ?: ""),
                    "weather" to (currentWeather?.weather ?: ""),
                    "weatherIcon" to (currentWeather?.weatherIcon ?: ""),
                    "city" to (currentWeather?.city ?: ""),
                    "humidity" to (currentWeather?.humidity?.toString() ?: ""),
                    "windSpeed" to (currentWeather?.windSpeed?.toString() ?: "")
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
    
    /**
     * 处理更新天气信息的请求
     */
    private suspend fun handleUpdateWeather(message: PluginMessage): PluginMessage {
        return try {
            updateWeather()
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
     * 处理获取天气预报的请求
     */
    private suspend fun handleGetWeatherForecast(message: PluginMessage): PluginMessage {
        return try {
            // 简化实现，返回当前天气信息
            // 实际应用中应该调用天气API获取预报数据
            PluginMessage.createResponse(
                message,
                mapOf(
                    "forecast" to "Not implemented yet",
                    "current_temperature" to (currentWeather?.temperature?.toString() ?: ""),
                    "current_weather" to (currentWeather?.weather ?: "")
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
    
    /**
     * 处理设置天气位置的请求
     */
    private suspend fun handleSetWeatherLocation(message: PluginMessage): PluginMessage {
        return try {
            val city = message.data["city"]
            val latitude = message.data["latitude"]?.toDoubleOrNull()
            val longitude = message.data["longitude"]?.toDoubleOrNull()
            
            val config = getConfigStorage()
            city?.let { config.setValue("weather_city", it) }
            latitude?.let { config.setValue("weather_latitude", it) }
            longitude?.let { config.setValue("weather_longitude", it) }
            
            // 重新获取天气信息
            updateWeather()
            
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
     * 处理获取天气UI的请求
     */
    private suspend fun handleGetWeatherUI(message: PluginMessage): PluginMessage {
        return try {
            val showIcon = message.data["showIcon"]?.toBoolean() ?: true
            val showTemperature = message.data["showTemperature"]?.toBoolean() ?: true
            
            val weatherText = if (currentWeather != null) {
                val icon = if (showIcon) currentWeather!!.weatherIcon ?: "" else ""
                val temp = if (showTemperature) "${currentWeather!!.temperature}°C" else ""
                "$icon $temp ${currentWeather!!.weather}"
            } else {
                "获取天气中..."
            }
            
            PluginMessage.createResponse(
                message,
                mapOf(
                    "weatherText" to weatherText,
                    "uiComponent" to "WeatherDisplay"
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
    
    /**
     * 用于在协程作用域中启动任务
     */
    private fun launch(block: suspend () -> Unit) {
        // 在实际应用中，应该使用合适的作用域
        // 这里简化处理
    }
}

/**
 * 天气插件屏幕路由
 */
object WeatherPluginScreenRoute

/**
 * 天气插件配置屏幕
 */
object WeatherPluginConfigScreen