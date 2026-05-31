package tech.huangsh.onetap.utils

import android.content.Context
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.*

class VoiceAssistant(private val context: Context) : TextToSpeech.OnInitListener {
    
    private val TAG = "VoiceAssistant"
    private var tts: TextToSpeech? = null
    private val _isSpeaking = MutableStateFlow(false)
    val isSpeaking: StateFlow<Boolean> = _isSpeaking
    
    init {
        tts = TextToSpeech(context, this)
    }
    
    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            // 尝试多种中文 Locale（不同厂商TTS引擎支持的Locale名称不同）
            val locales = listOf(
                Locale.CHINA,                          // zh_CN
                Locale.SIMPLIFIED_CHINESE,              // zh
                Locale.CHINESE,                         // zh
                Locale("zh", "CN"),                     // 手动构造
                Locale.getDefault()                     // 系统默认（通常是中文）
            )
            
            var success = false
            for (locale in locales) {
                val result = tts?.setLanguage(locale)
                if (result != TextToSpeech.LANG_MISSING_DATA && result != TextToSpeech.LANG_NOT_SUPPORTED) {
                    Log.d(TAG, "TTS语言设置成功: $locale")
                    success = true
                    break
                }
            }
            
            if (!success) {
                // 即使报告不支持，很多厂商TTS实际上仍然可以播放中文
                // 强制设置为系统默认语言，不阻断功能
                Log.w(TAG, "所有中文Locale尝试均返回不支持，但仍尝试使用默认语言")
                tts?.setLanguage(Locale.getDefault())
            }
            
            // 给老人用，语速稍慢一点
            tts?.setSpeechRate(0.9f)
            
            // Set utterance progress listener
            tts?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(utteranceId: String?) {
                    _isSpeaking.value = true
                }
                
                override fun onDone(utteranceId: String?) {
                    _isSpeaking.value = false
                }
                
                override fun onError(utteranceId: String?) {
                    _isSpeaking.value = false
                }
            })
        } else {
            Log.e(TAG, "TTS引擎初始化失败, status=$status")
        }
    }
    
    fun speak(text: String) {
        if (tts?.isSpeaking == true) {
            tts?.stop()
        }
        
        tts?.speak(
            text,
            TextToSpeech.QUEUE_ADD,
            null,
            System.currentTimeMillis().toString()
        )
    }
    
    fun stop() {
        tts?.stop()
    }
    
    fun setSpeechRate(rate: Float) {
        tts?.setSpeechRate(rate)
    }
    
    fun setPitch(pitch: Float) {
        tts?.setPitch(pitch)
    }
    
    fun shutdown() {
        tts?.shutdown()
    }
    
    fun isAvailable(): Boolean {
        return tts != null
    }
}