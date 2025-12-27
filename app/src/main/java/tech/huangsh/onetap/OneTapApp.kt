package tech.huangsh.onetap

import android.app.Activity
import android.app.Application
import android.os.Bundle
import dagger.hilt.android.HiltAndroidApp
import coil.ImageLoader
import coil.ImageLoaderFactory
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import tech.huangsh.onetap.plugin.PluginEvent
import tech.huangsh.onetap.plugin.PluginManager
import tech.huangsh.onetap.plugin.PluginRegistry
import tech.huangsh.onetap.utils.PerformanceUtils
import javax.inject.Inject

/**
 * 简易桌面应用类
 */
@HiltAndroidApp
class OneTapApp : Application(), ImageLoaderFactory {
    
    @Inject
    lateinit var pluginRegistry: PluginRegistry

    @Inject
    lateinit var pluginManager: PluginManager
    
    private lateinit var imageLoader: ImageLoader
    private val applicationScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    
    override fun onCreate() {
        super.onCreate()
        
        // 初始化优化的图片加载器
        imageLoader = PerformanceUtils.getOptimizedImageLoader(this)
        
        // 注册全局生命周期回调
        registerLifecycleCallbacks()

        // 初始化插件系统
        initializePluginSystem()
        
        // 预加载常用资源
        preloadResources()
    }
    
    override fun newImageLoader(): ImageLoader {
        return imageLoader
    }
    
    /**
     * 初始化插件系统
     */
    private fun initializePluginSystem() {
        applicationScope.launch {
            try {
                // 步骤1: 注册所有内置插件
                val registerSuccess = pluginRegistry.registerAllBuiltinPlugins()
                if (!registerSuccess) {
                    android.util.Log.e("OneTapApp", "注册内置插件失败")
                    return@launch
                }
                android.util.Log.d("OneTapApp", "内置插件注册成功")
                
                // 步骤2: 加载上次保存的插件启用状态
                // 如果是首次启动，会自动启用所有插件
                pluginManager.loadEnabledPlugins()
                android.util.Log.d("OneTapApp", "插件启用状态加载完成")
                
                // 步骤3: 通知应用已启动
                pluginManager.notifyPluginEvent(PluginEvent.AppStarted)
                android.util.Log.d("OneTapApp", "插件系统初始化完成")
            } catch (e: Exception) {
                android.util.Log.e("OneTapApp", "初始化插件系统失败", e)
                e.printStackTrace()
            }
        }
    }

    /**
     * 注册应用前后台生命周期回调，通知插件
     */
    private fun registerLifecycleCallbacks() {
        registerActivityLifecycleCallbacks(object : ActivityLifecycleCallbacks {
            override fun onActivityResumed(activity: android.app.Activity) {
                applicationScope.launch {
                    pluginManager.notifyPluginEvent(PluginEvent.AppResumed)
                }
            }

            override fun onActivityPaused(activity: android.app.Activity) {
                applicationScope.launch {
                    pluginManager.notifyPluginEvent(PluginEvent.AppPaused)
                }
            }

            override fun onActivityCreated(activity: android.app.Activity, savedInstanceState: android.os.Bundle?) {}
            override fun onActivityStarted(activity: android.app.Activity) {}
            override fun onActivityStopped(activity: android.app.Activity) {}
            override fun onActivitySaveInstanceState(activity: android.app.Activity, outState: android.os.Bundle) {}
            override fun onActivityDestroyed(activity: android.app.Activity) {}
        })
    }
    
    /**
     * 预加载常用资源
     */
    private fun preloadResources() {
        // 在这里可以预加载一些常用资源
        // 例如：默认图标、占位图等
    }
}