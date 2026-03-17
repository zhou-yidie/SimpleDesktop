package tech.huangsh.onetap.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.net.wifi.WifiManager
import android.os.Build
import android.os.CountDownTimer
import android.os.IBinder
import android.provider.Settings
import android.util.Log
import androidx.core.app.NotificationCompat
import tech.huangsh.onetap.R
import tech.huangsh.onetap.ui.activity.MainActivity
import tech.huangsh.onetap.config.AppConfig

/**
 * WiFi网络监控前台服务
 * 
 * 功能：
 * 1. 持续监控WiFi连接状态
 * 2. 自动保持WiFi开启（Android 10以下直接开启，10及以上引导用户开启）
 * 3. WiFi开启后20秒内未连接成功，发送广播通知UI层弹窗+语音播报
 * 4. WiFi重新连接后，发送广播通知UI层关闭弹窗
 */
class WifiMonitorService : Service() {

    companion object {
        private const val TAG = AppConfig.Debug.APP_TAG + "_WifiMonitor"
        private val CHANNEL_ID = AppConfig.WifiMonitor.CHANNEL_ID
        private val NOTIFICATION_ID = AppConfig.WifiMonitor.NOTIFICATION_ID
        private val WIFI_TIMEOUT_MS = AppConfig.WifiMonitor.DISCONNECT_TIMEOUT_MS
        private val WIFI_CHECK_INTERVAL_MS = AppConfig.WifiMonitor.CHECK_INTERVAL_MS

        // 广播Action
        const val ACTION_WIFI_DISCONNECTED = AppConfig.WifiMonitor.ACTION_WIFI_DISCONNECTED
        const val ACTION_WIFI_CONNECTED = AppConfig.WifiMonitor.ACTION_WIFI_CONNECTED
        const val ACTION_WIFI_DISABLED = AppConfig.WifiMonitor.ACTION_WIFI_DISABLED

        fun start(context: Context) {
            val intent = Intent(context, WifiMonitorService::class.java)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(intent)
            } else {
                context.startService(intent)
            }
        }

        fun stop(context: Context) {
            val intent = Intent(context, WifiMonitorService::class.java)
            context.stopService(intent)
        }
    }

    private var connectivityManager: ConnectivityManager? = null
    private var wifiManager: WifiManager? = null
    private var networkCallback: ConnectivityManager.NetworkCallback? = null
    private var disconnectTimer: CountDownTimer? = null
    private var isWifiConnected = false
    private var hasNotifiedDisconnection = false // 确保每次断网只通知一次

    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "WiFi监控服务已创建")
        
        connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        
        createNotificationChannel()
        startForeground(NOTIFICATION_ID, createNotification())
        
        // 启动时检查WiFi状态并尝试开启
        ensureWifiEnabled()
        
        // 注册网络状态监听
        registerNetworkCallback()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return START_STICKY // 服务被杀后自动重启
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "WiFi监控服务已销毁")
        
        // 取消网络监听
        networkCallback?.let {
            connectivityManager?.unregisterNetworkCallback(it)
        }
        networkCallback = null
        
        // 取消计时器
        disconnectTimer?.cancel()
        disconnectTimer = null
    }

    /**
     * 确保WiFi处于开启状态
     */
    @Suppress("DEPRECATION")
    private fun ensureWifiEnabled() {
        val wm = wifiManager ?: return
        if (!wm.isWifiEnabled) {
            if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
                // Android 9及以下：直接开启WiFi
                wm.isWifiEnabled = true
                Log.d(TAG, "已自动开启WiFi（API < 29）")
            } else {
                // Android 10及以上：发送广播让UI引导用户，并尝试拉起WiFi设置页让无障碍服务自动开启
                Log.d(TAG, "WiFi已关闭，尝试拉起设置页执行辅助开启（API >= 29）")
                
                // 告诉无障碍服务：我们要开始自动开启WiFi了
                tech.huangsh.onetap.service.WifiAutoEnableService.isAutoEnabling = true
                
                // 发送引导广播（同时保留原有逻辑作为兜底）
                sendBroadcast(Intent(ACTION_WIFI_DISABLED).setPackage(packageName))
                
                // 直接拉起系统的WiFi设置页
                try {
                    val intent = Intent(Settings.ACTION_WIFI_SETTINGS).apply {
                        flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
                    }
                    startActivity(intent)
                } catch (e: Exception) {
                    Log.e(TAG, "拉起WiFi设置页失败", e)
                    tech.huangsh.onetap.service.WifiAutoEnableService.isAutoEnabling = false
                }
            }
        }
    }

    /**
     * 注册网络状态变化回调
     */
    private fun registerNetworkCallback() {
        val request = NetworkRequest.Builder()
            .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
            .build()

        networkCallback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                Log.d(TAG, "WiFi已连接")
                isWifiConnected = true
                hasNotifiedDisconnection = false
                
                // 取消断网倒计时
                disconnectTimer?.cancel()
                disconnectTimer = null
                
                // 通知UI层：WiFi已恢复，关闭弹窗
                sendBroadcast(Intent(ACTION_WIFI_CONNECTED).setPackage(packageName))
            }

            override fun onLost(network: Network) {
                Log.d(TAG, "WiFi连接丢失")
                isWifiConnected = false
                
                // 先检查WiFi开关是否被关闭了
                ensureWifiEnabled()
                
                // 启动20秒倒计时
                startDisconnectTimer()
            }
        }

        connectivityManager?.registerNetworkCallback(request, networkCallback!!)
        
        // 检查当前WiFi连接状态
        checkCurrentWifiStatus()
    }

    /**
     * 检查当前WiFi连接状态（服务启动时调用）
     */
    private fun checkCurrentWifiStatus() {
        val activeNetwork = connectivityManager?.activeNetwork
        val capabilities = activeNetwork?.let { connectivityManager?.getNetworkCapabilities(it) }
        isWifiConnected = capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) == true
        
        if (!isWifiConnected && wifiManager?.isWifiEnabled == true) {
            // WiFi已开启但未连接，启动倒计时
            startDisconnectTimer()
        }
    }

    /**
     * 启动20秒断网倒计时
     */
    private fun startDisconnectTimer() {
        // 如果已经通知过断网，不再重复计时
        if (hasNotifiedDisconnection) return
        
        // 取消之前的计时器
        disconnectTimer?.cancel()
        
        disconnectTimer = object : CountDownTimer(WIFI_TIMEOUT_MS, WIFI_CHECK_INTERVAL_MS) {
            override fun onTick(millisUntilFinished: Long) {
                val secondsLeft = millisUntilFinished / 1000
                if (secondsLeft % 10 == 0L) {
                    Log.d(TAG, "断网倒计时剩余: ${secondsLeft}秒")
                }
            }

            override fun onFinish() {
                if (!isWifiConnected && !hasNotifiedDisconnection) {
                    Log.d(TAG, "20秒超时，WiFi仍未连接，通知UI弹窗")
                    hasNotifiedDisconnection = true
                    
                    // 发送广播：无可用WiFi网络
                    sendBroadcast(Intent(ACTION_WIFI_DISCONNECTED).setPackage(packageName))
                }
            }
        }.start()
    }

    /**
     * 创建通知渠道（Android 8.0+）
     */
    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                getString(R.string.wifi_monitor_channel_name),
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = getString(R.string.wifi_monitor_channel_desc)
                setShowBadge(false)
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    /**
     * 创建前台服务通知
     */
    private fun createNotification(): Notification {
        val pendingIntent = PendingIntent.getActivity(
            this, 0,
            Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(getString(R.string.wifi_monitor_notification_title))
            .setContentText(getString(R.string.wifi_monitor_notification_text))
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setSilent(true)
            .build()
    }
}
