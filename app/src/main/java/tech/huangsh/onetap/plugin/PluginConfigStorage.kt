package tech.huangsh.onetap.plugin

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.longPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import java.io.IOException
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 插件配置存储实现
 * 使用 DataStore Preferences，提供类型安全的读写
 */
@Singleton
class PluginConfigStorage @Inject constructor(
    @ApplicationContext private val context: Context
) : IPluginConfigStorage {

    private val Context.pluginConfigDataStore: DataStore<Preferences> by preferencesDataStore(
        name = "plugin_config"
    )

    private val dataStore = context.pluginConfigDataStore

    override suspend fun setValue(key: String, value: Any) {
        dataStore.edit { preferences ->
            when (value) {
                is String -> preferences[stringPreferencesKey(key)] = value
                is Boolean -> preferences[booleanPreferencesKey(key)] = value
                is Int -> preferences[intPreferencesKey(key)] = value
                is Long -> preferences[longPreferencesKey(key)] = value
                is Float -> preferences[floatPreferencesKey(key)] = value
                else -> throw IllegalArgumentException("Unsupported value type: ${value::class.java}")
            }
        }
    }

    override suspend fun getValue(key: String, defaultValue: Any?): Any? {
        return when (defaultValue) {
            is String? -> getString(key, defaultValue ?: "")
            is Boolean? -> getBoolean(key, defaultValue ?: false)
            is Int? -> getInt(key, defaultValue ?: 0)
            is Long? -> getLong(key, defaultValue ?: 0L)
            is Float? -> getFloat(key, defaultValue ?: 0f)
            else -> null
        }
    }

    override suspend fun getString(key: String, defaultValue: String): String {
        return readPreference(stringPreferencesKey(key), defaultValue)
    }

    override suspend fun getBoolean(key: String, defaultValue: Boolean): Boolean {
        return readPreference(booleanPreferencesKey(key), defaultValue)
    }

    override suspend fun getInt(key: String, defaultValue: Int): Int {
        return readPreference(intPreferencesKey(key), defaultValue)
    }

    override suspend fun getLong(key: String, defaultValue: Long): Long {
        return readPreference(longPreferencesKey(key), defaultValue)
    }

    override suspend fun getFloat(key: String, defaultValue: Float): Float {
        return readPreference(floatPreferencesKey(key), defaultValue)
    }

    override suspend fun removeValue(key: String) {
        dataStore.edit { preferences ->
            preferences.remove(stringPreferencesKey(key))
            preferences.remove(booleanPreferencesKey(key))
            preferences.remove(intPreferencesKey(key))
            preferences.remove(longPreferencesKey(key))
            preferences.remove(floatPreferencesKey(key))
        }
    }

    override suspend fun clear() {
        dataStore.edit { preferences ->
            preferences.clear()
        }
    }

    override suspend fun contains(key: String): Boolean {
        val prefs = safeReadPreferences()
        return prefs[stringPreferencesKey(key)] != null ||
            prefs[booleanPreferencesKey(key)] != null ||
            prefs[intPreferencesKey(key)] != null ||
            prefs[longPreferencesKey(key)] != null ||
            prefs[floatPreferencesKey(key)] != null
    }

    override suspend fun getAllKeys(): Set<String> {
        val prefs = safeReadPreferences()
        return prefs.asMap().keys.map { it.name }.toSet()
    }

    override fun observeChanges(): Flow<ConfigChange> {
        // 简化：仅提供键变更通知，实际可扩展为比较前后值
        return dataStore.data.map { preferences ->
            ConfigChange("", null, preferences) // 占位符，调用方可自行扩展
        }
    }

    override suspend fun setValues(values: Map<String, Any>) {
        dataStore.edit { preferences ->
            values.forEach { (key, value) ->
                when (value) {
                    is String -> preferences[stringPreferencesKey(key)] = value
                    is Boolean -> preferences[booleanPreferencesKey(key)] = value
                    is Int -> preferences[intPreferencesKey(key)] = value
                    is Long -> preferences[longPreferencesKey(key)] = value
                    is Float -> preferences[floatPreferencesKey(key)] = value
                    else -> throw IllegalArgumentException("Unsupported value type: ${value::class.java}")
                }
            }
        }
    }

    private suspend fun <T> readPreference(prefKey: Preferences.Key<T>, default: T): T {
        val prefs = safeReadPreferences()
        return prefs[prefKey] ?: default
    }

    private suspend fun safeReadPreferences(): Preferences {
        return try {
            dataStore.data.first()
        } catch (e: IOException) {
            emptyPreferences()
        }
    }
}