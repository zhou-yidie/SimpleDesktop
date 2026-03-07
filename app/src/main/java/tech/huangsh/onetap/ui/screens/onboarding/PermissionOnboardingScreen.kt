package tech.huangsh.onetap.ui.screens.onboarding

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import android.text.TextUtils
import androidx.activity.ComponentActivity
import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Accessibility
import androidx.compose.material.icons.filled.Apps
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Launch
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material.icons.filled.Place
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.core.content.ContextCompat
import com.hjq.permissions.OnPermissionCallback
import com.hjq.permissions.XXPermissions
import com.google.android.accessibility.selecttospeak.SelectToSpeakService
import kotlinx.coroutines.launch
import tech.huangsh.onetap.R

private enum class PermissionStepType {
    INFO,
    RUNTIME,
    OVERLAY,
    APP_LIST,
    ACCESSIBILITY
}

private data class PermissionStep(
    val id: String,
    val title: Int,
    val description: Int,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val bulletPoints: List<Int> = emptyList(),
    val permissions: List<String> = emptyList(),
    val type: PermissionStepType = PermissionStepType.RUNTIME,
    val actionLabel: Int = R.string.grant_permission
)

@Composable
fun PermissionOnboardingScreen(
    modifier: Modifier = Modifier,
    onFinished: () -> Unit
) {
    val steps = remember {
        mutableStateListOf(
            PermissionStep(
                id = "intro",
                title = R.string.onboarding_welcome_title,
                description = R.string.onboarding_welcome_desc,
                icon = Icons.Default.Bolt,
                bulletPoints = listOf(
                    R.string.onboarding_welcome_point_one,
                    R.string.onboarding_welcome_point_two,
                    R.string.onboarding_welcome_point_three
                ),
                type = PermissionStepType.INFO
            ),
            PermissionStep(
                id = "phone",
                title = R.string.onboarding_phone_title,
                description = R.string.onboarding_phone_desc,
                icon = Icons.Default.Phone,
                bulletPoints = listOf(
                    R.string.onboarding_phone_point_one,
                    R.string.onboarding_phone_point_two
                ),
                permissions = listOf(
                    Manifest.permission.CALL_PHONE,
                    Manifest.permission.READ_CONTACTS,
                    Manifest.permission.WRITE_CONTACTS
                )
            ),
            PermissionStep(
                id = "location",
                title = R.string.onboarding_location_title,
                description = R.string.onboarding_location_desc,
                icon = Icons.Default.Place,
                bulletPoints = listOf(
                    R.string.onboarding_location_point_one,
                    R.string.onboarding_location_point_two
                ),
                permissions = listOf(
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                    Manifest.permission.ACCESS_FINE_LOCATION
                )
            ),
            PermissionStep(
                id = "notification",
                title = R.string.onboarding_notification_title,
                description = R.string.onboarding_notification_desc,
                icon = Icons.Default.Notifications,
                bulletPoints = listOf(
                    R.string.onboarding_notification_point_one
                ),
                permissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    listOf(Manifest.permission.POST_NOTIFICATIONS)
                } else {
                    emptyList()
                }
            ),
            PermissionStep(
                id = "popup",
                title = R.string.onboarding_popup_title,
                description = R.string.onboarding_popup_desc,
                icon = Icons.Default.Launch,
                bulletPoints = listOf(
                    R.string.onboarding_popup_point_one,
                    R.string.onboarding_popup_point_two
                ),
                type = PermissionStepType.OVERLAY,
                actionLabel = R.string.go_to_settings
            ),
            PermissionStep(
                id = "app_list",
                title = R.string.onboarding_app_list_title,
                description = R.string.onboarding_app_list_desc,
                icon = Icons.Default.Apps,
                bulletPoints = listOf(
                    R.string.onboarding_app_list_point_one,
                    R.string.onboarding_app_list_point_two
                ),
                type = PermissionStepType.APP_LIST
            ),
            PermissionStep(
                id = "accessibility",
                title = R.string.onboarding_accessibility_title,
                description = R.string.onboarding_accessibility_desc,
                icon = Icons.Default.Accessibility,
                bulletPoints = listOf(
                    R.string.onboarding_accessibility_point_one,
                    R.string.onboarding_accessibility_point_two
                ),
                type = PermissionStepType.ACCESSIBILITY,
                actionLabel = R.string.go_to_settings
            )
        )
    }

    val context = LocalContext.current
    val activity = context as? ComponentActivity
    val lifecycleOwner = LocalLifecycleOwner.current
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    var currentStepIndex by rememberSaveable { mutableStateOf<Int>(0) }
    val permissionStatus = remember { mutableStateMapOf<String, Boolean>() }

    fun refreshPermissionStates() {
        steps.forEach { step ->
            permissionStatus[step.id] = when (step.type) {
                PermissionStepType.INFO -> true
                PermissionStepType.RUNTIME -> if (step.permissions.isEmpty()) {
                    true
                } else {
                    step.permissions.all { permission ->
                        permissionGranted(context, permission)
                    }
                }
                PermissionStepType.OVERLAY -> canDrawOverlaysCompat(context)
                PermissionStepType.APP_LIST -> hasAppListPermission(context)
                PermissionStepType.ACCESSIBILITY -> isAccessibilityServiceEnabled(context)
            }
        }
    }

    fun shouldShowActionButton(step: PermissionStep): Boolean {
        return when (step.type) {
            PermissionStepType.INFO -> false
            PermissionStepType.RUNTIME -> step.permissions.isNotEmpty()
            PermissionStepType.OVERLAY,
            PermissionStepType.APP_LIST,
            PermissionStepType.ACCESSIBILITY -> true
        }
    }

    fun requestPermissions(targetPermissions: List<String>) {
        if (activity == null || targetPermissions.isEmpty()) return
        XXPermissions.with(activity)
            .permission(targetPermissions)
            .request(object : OnPermissionCallback {
                override fun onGranted(
                    permissions: MutableList<String>,
                    allGranted: Boolean
                ) {
                    refreshPermissionStates()
                    if (allGranted) {
                        val msg = context.getString(R.string.permission_granted_tip)
                        scope.launch {
                            snackbarHostState.showSnackbar(message = msg)
                        }
                    }
                }

                override fun onDenied(
                    permissions: MutableList<String>,
                    doNotAskAgain: Boolean
                ) {
                    refreshPermissionStates()
                    val msg = if (doNotAskAgain) {
                        context.getString(R.string.permission_open_settings_tip)
                    } else {
                        context.getString(R.string.permission_denied_tip)
                    }
                    scope.launch {
                        snackbarHostState.showSnackbar(message = msg)
                    }
                    if (doNotAskAgain) {
                        XXPermissions.startPermissionActivity(context, permissions)
                    }
                }
            })
    }

    fun buildAppListPermissions(): List<String> {
        val permissions = mutableListOf<String>()
        when {
            isMiuiSystem() -> permissions.add("com.android.permission.GET_INSTALLED_APPS")
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.R -> permissions.add(Manifest.permission.QUERY_ALL_PACKAGES)
        }
        return permissions
    }

    fun handleStepAction(step: PermissionStep) {
        when (step.type) {
            PermissionStepType.RUNTIME -> requestPermissions(step.permissions)
            PermissionStepType.OVERLAY -> openOverlaySettings(context)
            PermissionStepType.APP_LIST -> {
                val appListPermissions = buildAppListPermissions()
                if (appListPermissions.isEmpty()) {
                    refreshPermissionStates()
                } else {
                    requestPermissions(appListPermissions)
                }
            }
            PermissionStepType.ACCESSIBILITY -> openAccessibilitySettings(context)
            PermissionStepType.INFO -> Unit
        }
    }

    LaunchedEffect(Unit) {
        refreshPermissionStates()
    }

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) {
                refreshPermissionStates()
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }

    val currentStep = steps[currentStepIndex]
    val isGranted = permissionStatus[currentStep.id] ?: false

    Scaffold(
        modifier = modifier.fillMaxSize(),
        snackbarHost = { SnackbarHost(hostState = snackbarHostState) }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(24.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.fillMaxWidth()) {
                StepHeader(step = currentStep, isGranted = isGranted)
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = stringResource(id = currentStep.description),
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onBackground
                )
                Spacer(modifier = Modifier.height(16.dp))
                currentStep.bulletPoints.forEach { bulletRes ->
                    BulletPoint(text = stringResource(id = bulletRes))
                }
                val showActionButton = shouldShowActionButton(currentStep)
                if (showActionButton) {
                    Spacer(modifier = Modifier.height(32.dp))
                    Button(
                        modifier = Modifier.fillMaxWidth(),
                        onClick = { handleStepAction(currentStep) },
                        enabled = !isGranted
                    ) {
                        Text(text = stringResource(id = currentStep.actionLabel))
                    }
                    if (isGranted) {
                        Text(
                            text = stringResource(R.string.permission_already_enabled),
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.primary,
                            modifier = Modifier
                                .align(Alignment.CenterHorizontally)
                                .padding(top = 12.dp)
                        )
                    }
                }
            }

            Column {
                LinearProgressIndicator(
                    progress = (currentStepIndex + 1) / steps.size.toFloat(),
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(8.dp),
                    trackColor = MaterialTheme.colorScheme.surfaceVariant,
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(24.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (currentStepIndex > 0) {
                        OutlinedButton(onClick = { currentStepIndex -= 1 }) {
                            Text(text = stringResource(id = R.string.onboarding_previous))
                        }
                    } else {
                        Spacer(modifier = Modifier.weight(0.3f))
                    }

                    Text(
                        text = stringResource(
                            id = R.string.onboarding_step_counter,
                            currentStepIndex + 1,
                            steps.size
                        ),
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.weight(1f),
                        textAlign = TextAlign.Center
                    )

                    val isLastStep = currentStepIndex == steps.lastIndex
                    Button(
                        onClick = {
                            if (isLastStep) {
                                onFinished()
                            } else {
                                currentStepIndex += 1
                            }
                        }
                    ) {
                        Text(
                            text = stringResource(
                                id = if (isLastStep) R.string.onboarding_finish else R.string.onboarding_next
                            )
                        )
                    }
                }

                TextButton(
                    onClick = onFinished,
                    modifier = Modifier.align(Alignment.CenterHorizontally)
                ) {
                    Text(text = stringResource(id = R.string.onboarding_skip))
                }
            }
        }
    }
}

@Composable
private fun StepHeader(step: PermissionStep, isGranted: Boolean) {
    val badgeColor by animateColorAsState(
        targetValue = if (isGranted) {
            MaterialTheme.colorScheme.primaryContainer
        } else {
            MaterialTheme.colorScheme.surfaceVariant
        }, label = "badge"
    )
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = badgeColor),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
        shape = RoundedCornerShape(20.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.background)
            ) {
                Icon(
                    imageVector = if (isGranted) Icons.Default.CheckCircle else step.icon,
                    contentDescription = stringResource(id = step.title),
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier
                        .padding(16.dp)
                        .height(32.dp)
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = stringResource(id = step.title),
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = stringResource(
                        id = if (isGranted) R.string.permission_status_ready else R.string.permission_status_needed
                    ),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
private fun BulletPoint(text: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = Icons.Default.CheckCircle,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.primary,
            modifier = Modifier.padding(end = 12.dp)
        )
        Text(
            text = text,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onBackground
        )
    }
}

private fun permissionGranted(context: Context, permission: String): Boolean {
    if (permission == Manifest.permission.POST_NOTIFICATIONS && Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) {
        return true
    }
    return ContextCompat.checkSelfPermission(
        context,
        permission
    ) == PackageManager.PERMISSION_GRANTED
}

private fun canDrawOverlaysCompat(context: Context): Boolean {
    return Build.VERSION.SDK_INT < Build.VERSION_CODES.M || Settings.canDrawOverlays(context)
}

private fun hasAppListPermission(context: Context): Boolean {
    return if (isMiuiSystem()) {
        ContextCompat.checkSelfPermission(context, "com.android.permission.GET_INSTALLED_APPS") == PackageManager.PERMISSION_GRANTED
    } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
        ContextCompat.checkSelfPermission(context, Manifest.permission.QUERY_ALL_PACKAGES) == PackageManager.PERMISSION_GRANTED
    } else {
        true
    }
}

private fun openOverlaySettings(context: Context) {
    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) return
    runCatching {
        val intent = Intent(
            Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
            Uri.parse("package:${context.packageName}")
        ).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(intent)
    }
}

private fun openAccessibilitySettings(context: Context) {
    runCatching {
        val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(intent)
    }
}

private fun isAccessibilityServiceEnabled(context: Context): Boolean {
    val serviceId = context.packageName + "/" + SelectToSpeakService::class.java.canonicalName
    val accessibilityEnabled = try {
        Settings.Secure.getInt(
            context.applicationContext.contentResolver,
            Settings.Secure.ACCESSIBILITY_ENABLED
        )
    } catch (_: Settings.SettingNotFoundException) {
        return false
    }

    if (accessibilityEnabled != 1) {
        return false
    }

    val settingValue = Settings.Secure.getString(
        context.applicationContext.contentResolver,
        Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
    ) ?: return false

    val colonSplitter = TextUtils.SimpleStringSplitter(':')
    colonSplitter.setString(settingValue)
    while (colonSplitter.hasNext()) {
        val accessibilityService = colonSplitter.next()
        if (accessibilityService.equals(serviceId, ignoreCase = true)) {
            return true
        }
    }
    return false
}

private fun isMiuiSystem(): Boolean {
    return Build.MANUFACTURER.equals("Xiaomi", ignoreCase = true) ||
        Build.BRAND.equals("Xiaomi", ignoreCase = true) ||
        Build.BRAND.equals("Redmi", ignoreCase = true) ||
        getSystemProperty("ro.miui.ui.version.name").isNotEmpty()
}

@Suppress("SwallowedException")
private fun getSystemProperty(key: String): String {
    return try {
        val systemProperties = Class.forName("android.os.SystemProperties")
        val get = systemProperties.getMethod("get", String::class.java)
        get.invoke(null, key) as? String ?: ""
    } catch (e: Exception) {
        ""
    }
}
