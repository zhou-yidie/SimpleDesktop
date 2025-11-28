package tech.huangsh.onetap

import android.app.Application
import androidx.work.Configuration
import coil.ImageLoader
import coil.ImageLoaderFactory
import dagger.hilt.android.HiltAndroidApp
import javax.inject.Inject
import androidx.hilt.work.HiltWorkerFactory
import tech.huangsh.onetap.utils.PerformanceUtils
import tech.huangsh.onetap.utils.WeatherWorkScheduler

/**
 * 一键通应用类
 */
@HiltAndroidApp
class OneTapApp : Application(), ImageLoaderFactory, Configuration.Provider {
    
    private lateinit var imageLoader: ImageLoader
    @Inject lateinit var workerFactory: HiltWorkerFactory
    
    override fun onCreate() {
        super.onCreate()
        
        // 初始化优化的图片加载器
        imageLoader = PerformanceUtils.getOptimizedImageLoader(this)
        
        // 预加载常用资源
        preloadResources()

        // 启动定时天气同步任务
        WeatherWorkScheduler.schedulePeriodic(this)
        WeatherWorkScheduler.triggerImmediate(this)
    }
    
    override fun newImageLoader(): ImageLoader {
        return imageLoader
    }
    
    /**
     * 预加载常用资源
     */
    private fun preloadResources() {
        // 在这里可以预加载一些常用资源
        // 例如：默认图标、占位图等
    }

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()
}