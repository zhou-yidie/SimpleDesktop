package tech.huangsh.onetap.ui.activity

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import dagger.hilt.android.AndroidEntryPoint
import tech.huangsh.onetap.plugin.impl.AppPlugin
import tech.huangsh.onetap.plugin.impl.ContactPlugin
import tech.huangsh.onetap.plugin.impl.WeatherPlugin
import tech.huangsh.onetap.ui.screens.plugin.PluginConfigScreen
import tech.huangsh.onetap.ui.theme.SimpleDesktopTheme
import javax.inject.Inject

/**
 * 插件配置Activity
 */
@AndroidEntryPoint
class PluginConfigActivity : ComponentActivity() {
    
    @Inject
    lateinit var contactPlugin: ContactPlugin
    
    @Inject
    lateinit var appPlugin: AppPlugin
    
    @Inject
    lateinit var weatherPlugin: WeatherPlugin
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val pluginId = intent.getStringExtra("plugin_id") ?: ""
        val pluginName = intent.getStringExtra("plugin_name") ?: "插件配置"
        
        setContent {
            SimpleDesktopTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    PluginConfigScreen(
                        pluginId = pluginId,
                        pluginName = pluginName,
                        contactPlugin = contactPlugin,
                        appPlugin = appPlugin,
                        weatherPlugin = weatherPlugin,
                        onBack = { finish() }
                    )
                }
            }
        }
    }
}
