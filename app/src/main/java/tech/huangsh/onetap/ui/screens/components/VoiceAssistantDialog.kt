package tech.huangsh.onetap.ui.screens.components

import android.Manifest
import android.content.Context
import android.content.Intent
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.util.Log
import android.widget.Toast
import android.view.ContextThemeWrapper
import androidx.activity.ComponentActivity
import androidx.activity.ComponentDialog
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.MicOff
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.hjq.permissions.OnPermissionCallback
import com.hjq.permissions.XXPermissions
import kotlinx.coroutines.delay
import androidx.lifecycle.lifecycleScope
import tech.huangsh.onetap.data.model.AppInfo
import tech.huangsh.onetap.data.model.Contact
import tech.huangsh.onetap.utils.ContactMatcher
import tech.huangsh.onetap.utils.VoiceAssistant
import tech.huangsh.onetap.utils.VoiceCommandParser

/**
 * 语音助手对话框
 *
 * 流程: 点击麦克风开始录音 → 实时显示识别文字 → 再次点击或20秒超时停止 → 解析意图 → 执行动作
 */
@Composable
fun VoiceAssistantDialog(
    contacts: List<Contact>,
    onDismiss: () -> Unit,
    onMakePhoneCall: (Contact) -> Unit,
    onMakeWeChatCall: (Contact) -> Unit,
    onLaunchApp: (AppInfo) -> Unit,
    onSearchApp: suspend (String) -> AppInfo?,
    voiceAssistant: VoiceAssistant?
) {
    val context = LocalContext.current

    // 状态
    var isListening by remember { mutableStateOf(false) }
    var recognizedText by remember { mutableStateOf("") }
    var statusText by remember { mutableStateOf("点击麦克风开始说话") }
    var remainingSeconds by remember { mutableIntStateOf(20) }
    var hasResult by remember { mutableStateOf(false) }

    // SpeechRecognizer 引用
    var speechRecognizer by remember { mutableStateOf<SpeechRecognizer?>(null) }
    
    // 检查引擎是否可用
    val isEngineAvailable = remember { SpeechRecognizer.isRecognitionAvailable(context) }
    val keyboardController = LocalSoftwareKeyboardController.current
    val voiceFocusRequester = remember { FocusRequester() }
    val voiceFocusManager = LocalFocusManager.current

    // 麦克风脉冲动画
    val pulseAnim = rememberInfiniteTransition(label = "pulse")
    val pulseScale by pulseAnim.animateFloat(
        initialValue = 1f,
        targetValue = 1.15f,
        animationSpec = infiniteRepeatable(
            animation = tween(600, easing = EaseInOutCubic),
            repeatMode = RepeatMode.Reverse
        ),
        label = "scale"
    )

    // 自动弹出键盘并初始化状态
    LaunchedEffect(Unit) {
        if (!isEngineAvailable) {
            statusText = "请使用键盘自带的语音功能"
        }
        delay(500)
        voiceFocusRequester.requestFocus()
        keyboardController?.show()
    }

    // 20秒倒计时
    LaunchedEffect(isListening) {
        if (isListening) {
            remainingSeconds = 20
            while (remainingSeconds > 0 && isListening) {
                delay(1000)
                remainingSeconds--
            }
            // 超时自动停止
            if (isListening) {
                isListening = false
                speechRecognizer?.stopListening()
            }
        }
    }

    // 停止录音后自动处理结果
    LaunchedEffect(isListening, hasResult) {
        if (!isListening && hasResult) {
            processVoiceResult(
                context = context,
                text = recognizedText,
                contacts = contacts,
                voiceAssistant = voiceAssistant,
                onMakePhoneCall = onMakePhoneCall,
                onMakeWeChatCall = onMakeWeChatCall,
                onLaunchApp = onLaunchApp,
                onSearchApp = onSearchApp,
                onDismiss = onDismiss,
                updateStatus = { statusText = it }
            )
        }
    }

    // 页面退出时释放资源
    DisposableEffect(Unit) {
        onDispose {
            speechRecognizer?.destroy()
        }
    }

    // 创建 SpeechRecognizer 和其监听器
    fun createRecognizer(): SpeechRecognizer? {
        if (!isEngineAvailable) return null
        
        val sr = try {
            SpeechRecognizer.createSpeechRecognizer(context)
        } catch (e: Exception) {
            Log.e("VoiceAssistantDialog", "创建 SpeechRecognizer 失败", e)
            null
        } ?: return null
        
        sr.setRecognitionListener(object : RecognitionListener {
            override fun onReadyForSpeech(params: Bundle?) {
                statusText = "正在聆听..."
            }
            override fun onBeginningOfSpeech() {}
            override fun onRmsChanged(rmsdB: Float) {}
            override fun onBufferReceived(buffer: ByteArray?) {}
            override fun onEndOfSpeech() {
                // 注意：不在这里停止，而是等用户点击或超时
            }
            override fun onError(error: Int) {
                val errorMsg = when (error) {
                    SpeechRecognizer.ERROR_AUDIO -> "录音失败"
                    SpeechRecognizer.ERROR_NO_MATCH -> "没有识别到语音"
                    SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "语音超时"
                    SpeechRecognizer.ERROR_NETWORK -> "网络错误"
                    SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "网络超时"
                    else -> "识别出错($error)"
                }
                statusText = errorMsg
                isListening = false
                if (recognizedText.isNotBlank()) {
                    hasResult = true
                }
            }
            override fun onResults(results: Bundle?) {
                val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                if (!matches.isNullOrEmpty()) {
                    recognizedText = matches[0]
                }
                isListening = false
                hasResult = true
            }
            override fun onPartialResults(partialResults: Bundle?) {
                val matches = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                if (!matches.isNullOrEmpty()) {
                    recognizedText = matches[0]
                }
            }
            override fun onEvent(eventType: Int, params: Bundle?) {}
        })
        return sr
    }

    // 系统语音输入启动器 (用于后台引擎不可用时的兜底)
    val voiceLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK) {
            val results = result.data?.getStringArrayListExtra(SpeechRecognizer.RESULTS_RECOGNITION)
            if (!results.isNullOrEmpty()) {
                recognizedText = results[0]
                hasResult = true
                isListening = false
            }
        } else {
            isListening = false
            statusText = "未完成语音识别"
        }
    }

    // 开始录音
    fun startListening() {
        if (!isEngineAvailable) {
            // 引导模式
            statusText = "请使用键盘语音输入"
            voiceFocusRequester.requestFocus()
            keyboardController?.show()
            voiceAssistant?.speak("请使用键盘上的语音键")
            return
        }

        val sr = createRecognizer()
        if (sr == null) {
            // 如果后台引擎不可用，但系统报支持（比如被精简过），尝试拉起系统语音对话框
            Log.w("VoiceAssistantDialog", "引擎创建失败，尝试拉起系统语音对话框")
            val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                putExtra(RecognizerIntent.EXTRA_LANGUAGE, "zh-CN")
                putExtra(RecognizerIntent.EXTRA_PROMPT, "请说话...")
            }
            try {
                isListening = true
                voiceLauncher.launch(intent)
            } catch (e: Exception) {
                isListening = false
                statusText = "系统语音组件缺失"
                Toast.makeText(context, "未找到语音识别组件，请安装搜狗/百度输入法并开启语音权限", Toast.LENGTH_LONG).show()
                Log.e("VoiceAssistantDialog", "拉起系统语音界面失败", e)
            }
            return
        }
        
        speechRecognizer = sr

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, "zh-CN")
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
        }

        recognizedText = ""
        hasResult = false
        statusText = "正在聆听..."
        isListening = true

        sr.startListening(intent)
    }

    // 停止录音
    fun stopListening() {
        isListening = false
        speechRecognizer?.stopListening()
        if (recognizedText.isNotBlank()) {
            hasResult = true
        }
    }

    // 请求录音权限并开始
    fun requestPermissionAndStart() {
        // 从 Context 中提取 Activity（Compose Dialog 的 context 可能被包装了多层）
        val activity = context.findActivity()
        if (activity == null) {
            statusText = "无法获取Activity上下文"
            Toast.makeText(context, "无法启动录音，请重试", Toast.LENGTH_SHORT).show()
            return
        }

        try {
            XXPermissions.with(activity)
                .permission(Manifest.permission.RECORD_AUDIO)
                .request(object : OnPermissionCallback {
                    override fun onGranted(permissions: MutableList<String>, allGranted: Boolean) {
                        if (allGranted) {
                            startListening()
                        }
                    }
                    override fun onDenied(permissions: MutableList<String>, doNotAskAgain: Boolean) {
                        if (doNotAskAgain) {
                            Toast.makeText(context, "请在设置中开启录音权限", Toast.LENGTH_LONG).show()
                            XXPermissions.startPermissionActivity(context, permissions)
                        } else {
                            Toast.makeText(context, "需要录音权限才能使用语音助手", Toast.LENGTH_SHORT).show()
                        }
                    }
                })
        } catch (e: Exception) {
            statusText = "权限请求失败"
            Toast.makeText(context, "权限请求失败: ${e.message}", Toast.LENGTH_SHORT).show()
            Log.e("VoiceAssistantDialog", "权限请求异常", e)
        }
    }

    // ===== UI =====
    Dialog(
        onDismissRequest = {
            speechRecognizer?.destroy()
            onDismiss()
        },
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background.copy(alpha = 0.95f))
                .padding(32.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
                modifier = Modifier.fillMaxWidth()
            ) {
                // 关闭按钮
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    IconButton(onClick = {
                        speechRecognizer?.destroy()
                        onDismiss()
                    }) {
                        Icon(
                            Icons.Default.Close,
                            contentDescription = "关闭",
                            modifier = Modifier.size(32.dp),
                            tint = MaterialTheme.colorScheme.onSurface
                        )
                    }
                }

                Spacer(modifier = Modifier.height(40.dp))

                // 状态文字
                Text(
                    text = statusText,
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Medium,
                    color = MaterialTheme.colorScheme.onSurface,
                    textAlign = TextAlign.Center
                )

                Spacer(modifier = Modifier.height(16.dp))

                // 倒计时 (仅在录音时显示)
                if (isListening) {
                    Text(
                        text = "${remainingSeconds}秒",
                        fontSize = 18.sp,
                        color = MaterialTheme.colorScheme.primary,
                        textAlign = TextAlign.Center
                    )
                }

                Spacer(modifier = Modifier.height(24.dp))

                // 识别出的文字
                if (recognizedText.isNotBlank()) {
                    Card(
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.primaryContainer
                        ),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            text = "\"$recognizedText\"",
                            fontSize = 22.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                            textAlign = TextAlign.Center,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(20.dp)
                        )
                    }
                }

                Spacer(modifier = Modifier.height(32.dp))

                // 输入框适配 (让用户可以使用输入法的语音键)
                OutlinedTextField(
                    value = recognizedText,
                    onValueChange = { 
                        recognizedText = it
                        statusText = "正在输入..."
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .focusRequester(voiceFocusRequester),
                    placeholder = { Text("也可以直接在这里输入（或使用输入法语音）", fontSize = 16.sp) },
                    shape = RoundedCornerShape(12.dp),
                    trailingIcon = {
                        if (recognizedText.isNotBlank()) {
                            IconButton(onClick = { 
                                voiceFocusManager.clearFocus()
                                isListening = false
                                hasResult = true 
                            }) {
                                Icon(Icons.Default.Send, contentDescription = "确认", tint = MaterialTheme.colorScheme.primary)
                            }
                        }
                    },
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                    keyboardActions = KeyboardActions(onSearch = {
                        voiceFocusManager.clearFocus()
                        isListening = false
                        hasResult = true
                    }),
                    textStyle = androidx.compose.ui.text.TextStyle(fontSize = 20.sp, fontWeight = FontWeight.Bold)
                )

                Spacer(modifier = Modifier.height(24.dp))

                Text(
                    text = "提示：点击键盘上的“小麦克风”也可以说话哦",
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f),
                    textAlign = TextAlign.Center
                )

                Spacer(modifier = Modifier.height(48.dp))

                // 大麦克风按钮
                Box(
                    modifier = Modifier
                        .size(120.dp)
                        .scale(if (isListening) pulseScale else 1f)
                        .clip(CircleShape)
                        .background(
                            if (isListening) MaterialTheme.colorScheme.error
                            else MaterialTheme.colorScheme.primary
                        )
                        .clickable {
                            if (isListening) {
                                stopListening()
                            } else if (isEngineAvailable) {
                                requestPermissionAndStart()
                            } else {
                                // 引导模式
                                voiceFocusRequester.requestFocus()
                                keyboardController?.show()
                                voiceAssistant?.speak("请点击键盘上的小麦克风图标进行说话")
                                Toast.makeText(context, "请点击键盘上的语音按钮", Toast.LENGTH_SHORT).show()
                            }
                        },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = if (isListening) Icons.Default.MicOff else Icons.Default.Mic,
                        contentDescription = if (isListening) "停止录音" else "开始录音",
                        modifier = Modifier.size(60.dp),
                        tint = Color.White
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))

                Text(
                    text = if (isListening) "再次点击停止" else "点击尝试快速语音",
                    fontSize = 16.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center
                )
            }
        }
    }
}

/**
 * 处理语音识别结果，执行匹配和拨号
 */
private suspend fun processVoiceResult(
    context: Context,
    text: String,
    contacts: List<Contact>,
    voiceAssistant: VoiceAssistant?,
    onMakePhoneCall: (Contact) -> Unit,
    onMakeWeChatCall: (Contact) -> Unit,
    onLaunchApp: (AppInfo) -> Unit,
    onSearchApp: suspend (String) -> AppInfo?,
    onDismiss: () -> Unit,
    updateStatus: (String) -> Unit
) {
    android.util.Log.d("VoiceAssistantDialog", "收到识别结果: $text")
    if (text.isBlank()) {
        updateStatus("没有识别到语音内容")
        voiceAssistant?.speak("没有识别到语音内容，请再试一次")
        return
    }

    // 解析语音指令
    val command = VoiceCommandParser.parseCommand(text)
    if (command == null) {
        android.util.Log.w("VoiceAssistantDialog", "无法解析指令意图: $text")
        updateStatus("抱歉，无法理解指令")
        voiceAssistant?.speak("抱歉，我没有理解您的指令，请说类似'打电话给某某'的句式")
        return
    }

    android.util.Log.d("VoiceAssistantDialog", "执行动作: ${command.action}, 目标: ${command.targetName}")
    when (command.action) {
        VoiceCommandParser.Action.CALL -> {
            // 查找联系人
            updateStatus("正在匹配联系人: ${command.targetName}")
            val matchResult = ContactMatcher.findBestMatch(command.targetName, contacts)
            if (matchResult == null) {
                android.util.Log.w("VoiceAssistantDialog", "未找到联系人匹配: ${command.targetName}")
                updateStatus("没有找到联系人: ${command.targetName}")
                voiceAssistant?.speak("抱歉，没有找到${command.targetName}这个联系人")
                return
            }

            val contact = matchResult.contact
            android.util.Log.d("VoiceAssistantDialog", "匹配到联系人: ${contact.name}, phone=${contact.phone}, wechat=${contact.wechatNickname}")
            updateStatus("正在呼叫: ${contact.name}")
            

            // 判断网络状态：有WiFi就打微信视频，否则打手机电话
            val wifiConnected = isWifiConnected(context)
            android.util.Log.d("VoiceAssistantDialog", "当前WiFi状态: $wifiConnected")

            if (wifiConnected && !contact.wechatNickname.isNullOrEmpty()) {
                android.util.Log.d("VoiceAssistantDialog", "准备发起微信视频通话")
                updateStatus("正在发起视频通话: ${contact.name}")
                voiceAssistant?.speak("正在通过微信为您发起视频通话")
                onMakeWeChatCall(contact)
            } else if (!contact.phone.isNullOrEmpty()) {
                android.util.Log.d("VoiceAssistantDialog", "准备拨打普通电话")
                voiceAssistant?.speak("正在为您拨打电话")
                onMakePhoneCall(contact)
            } else {
                android.util.Log.w("VoiceAssistantDialog", "无可用拨号方式: wifi=$wifiConnected, wechat=${contact.wechatNickname}, phone=${contact.phone}")
                updateStatus("该联系人没有可用的拨号方式")
                voiceAssistant?.speak("抱歉，${contact.name}没有可用的拨号方式")
                return
            }

            // 立即关闭对话框，避免抢占焦点，确保无障碍服务能工作
            onDismiss()
        }

        VoiceCommandParser.Action.OPEN_APP -> {
            updateStatus("正在查找应用: ${command.targetName}")
            val app = onSearchApp(command.targetName)
            if (app != null) {
                updateStatus("正在打开: ${app.appName}")
                voiceAssistant?.speak("正在为您打开${app.appName}")
                onLaunchApp(app)
                delay(1500)
                onDismiss()
            } else {
                updateStatus("没有找到应用: ${command.targetName}")
                voiceAssistant?.speak("抱歉，没有找到${command.targetName}这个应用")
            }
        }

        VoiceCommandParser.Action.FLASHLIGHT -> {
            if (tech.huangsh.onetap.utils.FlashlightHelper.toggle(context)) {
                val isOn = tech.huangsh.onetap.utils.FlashlightHelper.isOn()
                val text = if (isOn) "已为您打开手电筒" else "已为您关闭手电筒"
                updateStatus(text)
                voiceAssistant?.speak(text)
                delay(1500)
                onDismiss()
            } else {
                updateStatus("手电筒操作失败")
                voiceAssistant?.speak("抱歉，手电筒操作失败")
            }
        }

        // 其他动作，后续扩展
        else -> {
            updateStatus("该功能暂未开放")
            voiceAssistant?.speak("该功能暂未开放，敬请期待")
        }
    }
}

/**
 * 遍历 Context 包装器找到 Activity
 * Compose Dialog 的 Context 通常是 ContextWrapper
 */
fun Context.findActivity(): ComponentActivity? {
    var context = this
    while (context is android.content.ContextWrapper) {
        if (context is ComponentActivity) return context
        context = context.baseContext
    }
    return null
}

/**
 * 检查当前是否连接了WiFi网络
 */
private fun isWifiConnected(context: Context): Boolean {
    val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
    val network = cm.activeNetwork ?: return false
    val capabilities = cm.getNetworkCapabilities(network) ?: return false
    return capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)
}
