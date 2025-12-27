package tech.huangsh.onetap.ui.activity

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import dagger.hilt.android.AndroidEntryPoint
import tech.huangsh.onetap.ui.screens.plugin.PluginManagementScreen
import tech.huangsh.onetap.ui.theme.OneTapTheme

/**
 * 插件管理Activity
 */
@AndroidEntryPoint
class PluginManagementActivity : ComponentActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        setContent {
            OneTapTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    PluginManagementScreen(
                        onBack = { finish() }
                    )
                }
            }
        }
    }
}