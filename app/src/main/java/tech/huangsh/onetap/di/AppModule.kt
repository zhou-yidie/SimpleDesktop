package tech.huangsh.onetap.di

import android.content.Context
import androidx.room.Room
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.SupervisorJob
import tech.huangsh.onetap.data.local.AppDatabase
import tech.huangsh.onetap.data.local.dao.AppInfoDao
import tech.huangsh.onetap.data.local.dao.ContactDao
import tech.huangsh.onetap.data.remote.WeatherService
import tech.huangsh.onetap.data.repository.AppRepository
import tech.huangsh.onetap.data.repository.ContactRepository
import tech.huangsh.onetap.data.repository.SettingsRepository
import tech.huangsh.onetap.plugin.PluginConfigStorage
import tech.huangsh.onetap.plugin.PluginLoader
import tech.huangsh.onetap.plugin.PluginManager
import tech.huangsh.onetap.plugin.PluginMessenger
import tech.huangsh.onetap.plugin.PluginRegistry
import tech.huangsh.onetap.plugin.impl.AppPlugin
import tech.huangsh.onetap.plugin.impl.ContactPlugin
import tech.huangsh.onetap.plugin.impl.WeatherPlugin
import tech.huangsh.onetap.plugin.IPlugin
import javax.inject.Singleton
import dagger.multibindings.IntoSet

/**
 * 应用模块 - 提供应用级别的依赖
 */
@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideAppDatabase(
        @ApplicationContext context: Context
    ): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "one_tap_database"
        )
            .fallbackToDestructiveMigration()
            .build()
    }

    @Provides
    fun provideContactDao(database: AppDatabase): ContactDao = database.contactDao()

    @Provides
    fun provideAppInfoDao(database: AppDatabase): AppInfoDao = database.appInfoDao()

    @Provides
    @Singleton
    fun provideApplicationScope(): CoroutineScope = CoroutineScope(SupervisorJob())

    @Provides
    @Singleton
    fun provideContactRepository(
        contactDao: ContactDao,
        @ApplicationContext context: Context
    ): ContactRepository {
        return ContactRepository(contactDao, context)
    }

    @Provides
    @Singleton
    fun provideAppRepository(
        appInfoDao: AppInfoDao,
        @ApplicationContext context: Context
    ): AppRepository {
        return AppRepository(appInfoDao, context)
    }

    @Provides
    @Singleton
    fun provideSettingsRepository(
        @ApplicationContext context: Context
    ): SettingsRepository {
        return SettingsRepository(context)
    }

    @Provides
    @Singleton
    fun provideWeatherService(
        @ApplicationContext context: Context
    ): WeatherService {
        return WeatherService(context)
    }
    
    // 插件系统相关依赖
    
    @Provides
    @Singleton
    fun providePluginConfigStorage(
        @ApplicationContext context: Context
    ): PluginConfigStorage {
        return PluginConfigStorage(context)
    }
    
    @Provides
    @Singleton
    fun providePluginMessenger(): PluginMessenger {
        return PluginMessenger()
    }
    
    @Provides
    @Singleton
    fun providePluginManager(
        @ApplicationContext context: Context,
        pluginMessenger: PluginMessenger
    ): PluginManager {
        return PluginManager(context, pluginMessenger)
    }
    
    @Provides
    @Singleton
    fun providePluginLoader(
        @ApplicationContext context: Context
    ): PluginLoader {
        return PluginLoader(context)
    }
    
    @Provides
    @Singleton
    fun providePluginRegistry(
        pluginLoader: PluginLoader,
        pluginManager: PluginManager,
        builtinPlugins: Set<@JvmSuppressWildcards IPlugin>
    ): PluginRegistry {
        return PluginRegistry(pluginLoader, pluginManager, builtinPlugins)
    }
    
    // 内置插件实例
    
    @Provides
    @Singleton
    fun provideContactPlugin(
        @ApplicationContext context: Context,
        contactRepository: ContactRepository
    ): ContactPlugin {
        return ContactPlugin(context, contactRepository)
    }

    @Provides
    @IntoSet
    fun bindContactPlugin(contactPlugin: ContactPlugin): IPlugin = contactPlugin
    
    @Provides
    @Singleton
    fun provideAppPlugin(
        @ApplicationContext context: Context,
        appRepository: AppRepository
    ): AppPlugin {
        return AppPlugin(context, appRepository)
    }

    @Provides
    @IntoSet
    fun bindAppPlugin(appPlugin: AppPlugin): IPlugin = appPlugin
    
    @Provides
    @Singleton
    fun provideWeatherPlugin(
        @ApplicationContext context: Context,
        weatherService: WeatherService
    ): WeatherPlugin {
        return WeatherPlugin(context, weatherService)
    }

    @Provides
    @IntoSet
    fun bindWeatherPlugin(weatherPlugin: WeatherPlugin): IPlugin = weatherPlugin
}