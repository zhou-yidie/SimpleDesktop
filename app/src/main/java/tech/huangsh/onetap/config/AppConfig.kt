package tech.huangsh.onetap.config

/**
 * 全局配置中心
 * 
 * 遵循“单一真理源”原则，所有业务逻辑常量、API 地址、超时设置等均在此统一管理。
 * 修改此文件中的值将影响全项目的对应行为。
 */
object AppConfig {

    /**
     * 网络配置
     */
    object Network {
        // 天气服务 API 基准地址
        const val WEATHER_BASE_URL = "https://api.open-meteo.com/"
        
        // 默认城市（用于无定位权限时）
        const val DEFAULT_CITY = "北京"
        
        // 建议的 Retrofit 超时时间（秒）
        const val CONNECT_TIMEOUT = 15L
        const val READ_TIMEOUT = 15L
    }

    /**
     * WiFi 监控模块配置
     */
    object WifiMonitor {
        // WiFi 异常断开后的自动重连/提醒倒计时（毫秒）
        const val DISCONNECT_TIMEOUT_MS = 20_000L
        
        // 状态检查频率（毫秒）
        const val CHECK_INTERVAL_MS = 1_000L
        
        // 通知相关
        const val NOTIFICATION_ID = 1001
        const val CHANNEL_ID = "wifi_monitor_channel"
        
        // 广播指令
        const val ACTION_WIFI_DISCONNECTED = "tech.huangsh.onetap.WIFI_DISCONNECTED"
        const val ACTION_WIFI_CONNECTED = "tech.huangsh.onetap.WIFI_CONNECTED"
        const val ACTION_WIFI_DISABLED = "tech.huangsh.onetap.WIFI_DISABLED"
    }

    /**
     * 语音助手配置
     */
    object Voice {
        const val TAG = "VoiceAssistant"
        // 默认语速
        const val DEFAULT_SPEECH_RATE = 1.0f
        // 默认音量
        const val DEFAULT_VOLUME = 1.0f
    }
    
    /**
     * 存储配置 (DataStore / Database)
     */
    object Storage {
        const val SETTINGS_DATASTORE_NAME = "settings"
        const val PLUGIN_MANAGER_DATASTORE_NAME = "plugin_manager"
        
        // 默认访问密码
        const val DEFAULT_PASSWORD = "666" // 示例：将 123456 修改为 666 以演示效果
    }

    /**
     * 调试与日志配置
     */
    object Debug {
        const val APP_TAG = "SimpleDesktop"
        // 是否开启详细日志（生产环境可切换为 false）
        const val IS_LOGGABLE = true
    }
}
