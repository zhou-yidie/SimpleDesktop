package tech.huangsh.onetap.plugin

import kotlinx.coroutines.flow.Flow

/**
 * 插件配置存储接口
 */
interface IPluginConfigStorage {
    /**
     * 保存配置项
     */
    suspend fun setValue(key: String, value: Any)
    
    /**
     * 获取配置项
     */
    suspend fun getValue(key: String, defaultValue: Any? = null): Any?
    
    /**
     * 获取字符串配置项
     */
    suspend fun getString(key: String, defaultValue: String = ""): String
    
    /**
     * 获取布尔配置项
     */
    suspend fun getBoolean(key: String, defaultValue: Boolean = false): Boolean
    
    /**
     * 获取整数配置项
     */
    suspend fun getInt(key: String, defaultValue: Int = 0): Int
    
    /**
     * 获取长整数配置项
     */
    suspend fun getLong(key: String, defaultValue: Long = 0L): Long
    
    /**
     * 获取浮点数配置项
     */
    suspend fun getFloat(key: String, defaultValue: Float = 0f): Float
    
    /**
     * 删除配置项
     */
    suspend fun removeValue(key: String)
    
    /**
     * 清空所有配置
     */
    suspend fun clear()
    
    /**
     * 检查配置项是否存在
     */
    suspend fun contains(key: String): Boolean
    
    /**
     * 获取所有配置项的键
     */
    suspend fun getAllKeys(): Set<String>
    
    /**
     * 观察配置项变化
     */
    fun observeChanges(): Flow<ConfigChange>
    
    /**
     * 批量保存配置项
     */
    suspend fun setValues(values: Map<String, Any>)
}

/**
 * 配置变更事件
 */
data class ConfigChange(
    val key: String,
    val oldValue: Any?,
    val newValue: Any?
)