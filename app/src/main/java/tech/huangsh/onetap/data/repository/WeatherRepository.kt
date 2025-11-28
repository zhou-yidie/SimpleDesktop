package tech.huangsh.onetap.data.repository

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.longPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import tech.huangsh.onetap.data.model.WeatherInfo
import tech.huangsh.onetap.data.remote.WeatherService

private val Context.weatherDataStore: DataStore<Preferences> by preferencesDataStore(name = "weather_cache")

/**
 * 天气数据仓库，负责缓存最近一次天气数据并触发刷新。
 */
@Singleton
class WeatherRepository @Inject constructor(
    @ApplicationContext private val context: Context,
    private val weatherService: WeatherService
) {

    private val dataStore = context.weatherDataStore

    private object Keys {
        val TEMPERATURE = intPreferencesKey("temperature")
        val WEATHER = stringPreferencesKey("weather")
        val WEATHER_ICON = stringPreferencesKey("weather_icon")
        val HUMIDITY = intPreferencesKey("humidity")
        val WIND_SPEED = floatPreferencesKey("wind_speed")
        val CITY = stringPreferencesKey("city")
        val UPDATE_TIME = longPreferencesKey("update_time")
    }

    val weatherInfo: Flow<WeatherInfo> = dataStore.data.map { preferences ->
        WeatherInfo(
            temperature = preferences[Keys.TEMPERATURE] ?: 25,
            weather = preferences[Keys.WEATHER] ?: "晴",
            weatherIcon = preferences[Keys.WEATHER_ICON] ?: "☀️",
            humidity = preferences[Keys.HUMIDITY] ?: 50,
            windSpeed = preferences[Keys.WIND_SPEED] ?: 3.0f,
            city = preferences[Keys.CITY] ?: "北京",
            updateTime = preferences[Keys.UPDATE_TIME] ?: System.currentTimeMillis()
        )
    }

    suspend fun refreshWeather(): WeatherInfo {
        val latest = weatherService.getWeatherInfo()
        cacheWeather(latest)
        return latest
    }

    suspend fun cacheWeather(info: WeatherInfo) {
        dataStore.edit { preferences ->
            preferences[Keys.TEMPERATURE] = info.temperature
            preferences[Keys.WEATHER] = info.weather
            preferences[Keys.WEATHER_ICON] = info.weatherIcon
            preferences[Keys.HUMIDITY] = info.humidity
            preferences[Keys.WIND_SPEED] = info.windSpeed
            preferences[Keys.CITY] = info.city
            preferences[Keys.UPDATE_TIME] = info.updateTime
        }
    }
}
