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
                // 注册所有内置插件
                val success = pluginRegistry.registerAllBuiltinPlugins()
                if (success) {
                    // 启用依赖顺序内所有插件
                    pluginManager.enableAllPlugins()
                    // 通知应用已启动
                    pluginManager.notifyPluginEvent(PluginEvent.AppStarted)
                }
            } catch (e: Exception) {
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