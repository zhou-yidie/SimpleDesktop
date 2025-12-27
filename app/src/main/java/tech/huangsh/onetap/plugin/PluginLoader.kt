package tech.huangsh.onetap.plugin

import android.content.Context
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import android.os.Build
import androidx.annotation.RequiresApi
import dalvik.system.DexFile
import dalvik.system.PathClassLoader
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import tech.huangsh.onetap.plugin.impl.AppPlugin
import tech.huangsh.onetap.plugin.impl.ContactPlugin
import tech.huangsh.onetap.plugin.impl.WeatherPlugin
import java.io.File
import java.lang.reflect.Modifier
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 插件加载器
 * 负责动态加载和卸载插件
 */
@Singleton
class PluginLoader @Inject constructor(
    private val context: Context
) {
    
    /**
     * 插件描述信息
     */
    data class PluginDescriptor(
        val className: String,
        val pluginId: String,
        val name: String,
        val version: String,
        val description: String,
        val author: String,
        val dependencies: List<String> = emptyList(),
        val minAppVersion: String = "1.0.0"
    )
    
    /**
     * 内置插件列表（应用内插件）
     */
    private val builtinPlugins = mapOf(
        "contact_plugin" to ContactPlugin::class.java,
        "app_plugin" to AppPlugin::class.java,
        "weather_plugin" to WeatherPlugin::class.java
    )
    
    /**
     * 加载内置插件
     */
    suspend fun loadBuiltinPlugin(pluginId: String): IPlugin? {
        return withContext(Dispatchers.IO) {
            try {
                val pluginClass = builtinPlugins[pluginId] ?: return@withContext null
                
                // 使用反射创建插件实例
                val constructor = pluginClass.getDeclaredConstructor()
                constructor.isAccessible = true
                val plugin = constructor.newInstance() as IPlugin
                
                plugin
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }
    }
    
    /**
     * 加载所有内置插件
     */
    suspend fun loadAllBuiltinPlugins(): List<IPlugin> {
        return withContext(Dispatchers.IO) {
            val plugins = mutableListOf<IPlugin>()
            
            builtinPlugins.forEach { (pluginId, pluginClass) ->
                try {
                    val constructor = pluginClass.getDeclaredConstructor()
                    constructor.isAccessible = true
                    val plugin = constructor.newInstance() as IPlugin
                    plugins.add(plugin)
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
            
            plugins
        }
    }
    
    /**
     * 从APK文件加载插件
     * 注意：这是一个简化实现，实际生产环境中需要更严格的安全检查
     */
    @RequiresApi(Build.VERSION_CODES.O)
    suspend fun loadPluginFromApk(apkPath: String): IPlugin? {
        return withContext(Dispatchers.IO) {
            try {
                // 检查APK文件是否存在
                val apkFile = File(apkPath)
                if (!apkFile.exists()) {
                    return@withContext null
                }
                
                // 获取包信息
                val packageManager = context.packageManager
                val packageInfo: PackageInfo? = packageManager.getPackageArchiveInfo(
                    apkPath,
                    PackageManager.GET_ACTIVITIES or PackageManager.GET_SERVICES or PackageManager.GET_PROVIDERS or PackageManager.GET_META_DATA
                )
                
                if (packageInfo == null) {
                    return@withContext null
                }
                
                // 检查插件元数据
                val metaData = packageInfo.applicationInfo?.metaData ?: return@withContext null
                
                // 从元数据获取插件描述符
                val pluginClass = metaData.getString("plugin_class") ?: return@withContext null
                val pluginId = metaData.getString("plugin_id") ?: return@withContext null
                val name = metaData.getString("plugin_name") ?: return@withContext null
                val version = metaData.getString("plugin_version") ?: return@withContext null
                val description = metaData.getString("plugin_description") ?: ""
                val author = metaData.getString("plugin_author") ?: ""
                
                // 加载APK到类加载器
                val classLoader = PathClassLoader(apkPath, ClassLoader.getSystemClassLoader())
                
                // 加载插件类
                val clazz = Class.forName(pluginClass, true, classLoader)
                
                // 检查类是否实现了IPlugin接口
                if (!IPlugin::class.java.isAssignableFrom(clazz)) {
                    return@withContext null
                }
                
                // 创建插件实例
                val constructor = clazz.getDeclaredConstructor()
                constructor.isAccessible = true
                val plugin = constructor.newInstance() as IPlugin
                
                // 验证插件信息
                if (plugin.pluginId != pluginId || plugin.name != name || plugin.version != version) {
                    return@withContext null
                }
                
                plugin
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }
    }
    
    /**
     * 从Dex文件加载插件
     */
    suspend fun loadPluginFromDex(dexPath: String): IPlugin? {
        return withContext(Dispatchers.IO) {
            try {
                // 检查Dex文件是否存在
                val dexFile = File(dexPath)
                if (!dexFile.exists()) {
                    return@withContext null
                }
                
                // 加载Dex文件
                val dex = DexFile(dexFile)
                
                // 遍历Dex中的类
                val entries = dex.entries()
                while (entries.hasMoreElements()) {
                    val className = entries.nextElement()
                    
                    // 跳过系统类和内部类
                    if (className.contains("$") || className.startsWith("android.") || 
                        className.startsWith("java.") || className.startsWith("kotlin.") ||
                        className.startsWith("kotlinx.") || className.startsWith("androidx.")) {
                        continue
                    }
                    
                    try {
                        // 加载类
                        val clazz = Class.forName(className, true, PathClassLoader(dexPath, ClassLoader.getSystemClassLoader()))
                        
                        // 检查类是否实现了IPlugin接口
                        if (IPlugin::class.java.isAssignableFrom(clazz)) {
                            // 检查类是否是具体类（非抽象类）
                            if (!Modifier.isAbstract(clazz.modifiers)) {
                                // 创建插件实例
                                val constructor = clazz.getDeclaredConstructor()
                                constructor.isAccessible = true
                                val plugin = constructor.newInstance() as IPlugin
                                
                                return@withContext plugin
                            }
                        }
                    } catch (e: Exception) {
                        // 忽略加载失败的类
                    }
                }
                
                null
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }
    }
    
    /**
     * 从目录扫描并加载插件
     */
    suspend fun scanAndLoadPluginsFromDirectory(directory: File): List<IPlugin> {
        return withContext(Dispatchers.IO) {
            val plugins = mutableListOf<IPlugin>()
            
            if (!directory.exists() || !directory.isDirectory) {
                return@withContext plugins
            }
            
            // 扫描目录中的文件
            directory.listFiles()?.forEach { file ->
                if (file.isFile) {
                    // 根据文件扩展名决定加载方式
                    when {
                        file.name.endsWith(".apk") -> {
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                                loadPluginFromApk(file.absolutePath)?.let { plugins.add(it) }
                            }
                        }
                        file.name.endsWith(".dex") -> {
                            loadPluginFromDex(file.absolutePath)?.let { plugins.add(it) }
                        }
                    }
                }
            }
            
            plugins
        }
    }
    
    /**
     * 获取内置插件列表
     */
    fun getBuiltinPluginList(): List<PluginDescriptor> {
        return builtinPlugins.map { (pluginId, pluginClass) ->
            try {
                // 创建临时实例以获取插件信息
                val constructor = pluginClass.getDeclaredConstructor()
                constructor.isAccessible = true
                val tempInstance = constructor.newInstance() as IPlugin
                
                PluginDescriptor(
                    className = pluginClass.name,
                    pluginId = tempInstance.pluginId,
                    name = tempInstance.name,
                    version = tempInstance.version,
                    description = tempInstance.description,
                    author = tempInstance.author,
                    dependencies = tempInstance.getDependencies()
                )
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }.filterNotNull()
    }
    
    /**
     * 验证插件兼容性
     */
    suspend fun validatePlugin(plugin: IPlugin): Boolean {
        return withContext(Dispatchers.IO) {
            try {
                // 检查基本字段
                if (plugin.pluginId.isEmpty() || plugin.name.isEmpty() || plugin.version.isEmpty()) {
                    return@withContext false
                }
                
                // 检查依赖是否满足
                plugin.getDependencies().forEach { depId ->
                    // 这里应该检查依赖是否已安装
                    // 简化处理，返回true
                }
                
                true
            } catch (e: Exception) {
                e.printStackTrace()
                false
            }
        }
    }
}