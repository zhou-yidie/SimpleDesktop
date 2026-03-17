# 新增功能说明

## 本次更新内容

本次更新添加了三个重要的用户引导和权限管理功能:

### 1. 首次启动引导页 (Onboarding)

**位置**: `OnboardingActivity` + `OnboardingScreen`

**功能特点**:
- 4页滑动引导界面
  - 第1页: 欢迎页 - 介绍产品定位
  - 第2页: 功能展示 - 核心功能介绍
  - 第3页: 权限说明 - 解释为什么需要权限
  - 第4页: 开始设置 - 引导用户完成配置

- 页面指示器显示当前进度
- 支持跳过功能
- 完成后标记 `isFirstLaunch = false`

**实现细节**:
```kotlin
// Settings模型新增字段
data class Settings(
    ...
    val isFirstLaunch: Boolean = true  // 首次启动标记
)

// MainActivity检查首次启动
private fun checkFirstLaunch() {
    if (settings.isFirstLaunch) {
        // 跳转到引导页
        startActivity(Intent(this, OnboardingActivity::class.java))
    }
}
```

### 2. 无障碍服务引导对话框

**位置**: `AccessibilityGuideDialog`

**功能特点**:
- 实时检测无障碍服务状态
- 清晰的图文说明:
  - ✅ 为什么需要无障碍服务
  - 📝 详细的开启步骤 (4步骤)
  - 🎯 操作按钮: "打开设置"、"检查状态"、"稍后设置"
- 状态卡片显示:
  - 🟢 已启用 - 绿色提示
  - 🔴 未启用 - 红色提示

**调用方式**:
```kotlin
var showAccessibilityGuide by remember { mutableStateOf(false) }

// 触发引导
if (needAccessibilityService) {
    showAccessibilityGuide = true
}

// 显示对话框
if (showAccessibilityGuide) {
    AccessibilityGuideDialog(
        onDismiss = { showAccessibilityGuide = false },
        onSuccess = { /* 成功回调 */ }
    )
}
```

**检测逻辑**:
```kotlin
private fun isAccessibilityServiceEnabled(context: Context): Boolean {
    val serviceId = context.packageName + "/" + 
                    SelectToSpeakService::class.java.canonicalName
    // 检查系统设置中是否启用该服务
    ...
}
```

### 3. 权限管理页面

**位置**: `PermissionManagementScreen`

**功能特点**:

#### 权限分类
- **必需权限** (Essential Permissions):
  - 📞 拨打电话 - 快速拨打联系人电话
  - 👥 读取联系人 - 从系统导入联系人
  - 🏠 默认桌面 - 设为默认桌面

- **可选权限** (Optional Permissions):
  - 📷 相机 - 拍摄联系人头像
  - 📍 位置信息 - 获取天气
  - ♿ 无障碍服务 - 微信自动拨号

#### 界面设计
- 顶部状态卡片:
  - 全部授予: 绿色✅
  - 部分缺失: 红色⚠️
  
- 权限卡片:
  - 图标 + 标题 + 描述
  - 状态标签 (已授权/未授权)
  - 操作按钮 (未授权时显示"授权"按钮)

- 实时刷新: 从其他应用返回时自动检测权限变化

#### 集成位置
在设置页面添加入口:
```kotlin
// SettingsScreen.kt
SettingsItem(
    icon = Icons.Default.Security,
    title = "权限管理",
    onClick = {
        val intent = Intent(context, PermissionSetupActivity::class.java)
        context.startActivity(intent)
    }
)
```

### 4. 权限辅助工具类

**位置**: `PermissionHelper`

**提供方法**:
```kotlin
// 检查权限
PermissionHelper.isAccessibilityServiceEnabled(context)
PermissionHelper.hasPhonePermission(context)
PermissionHelper.hasContactsPermission(context)
PermissionHelper.hasCameraPermission(context)
PermissionHelper.hasLocationPermission(context)
PermissionHelper.isDefaultLauncher(context)

// 请求权限
PermissionHelper.requestPhonePermission(activity,
    onGranted = { /* 成功 */ },
    onDenied = { /* 拒绝 */ }
)

// 打开设置
PermissionHelper.openAccessibilitySettings(context)

// 检查所有必需权限
val status = PermissionHelper.checkEssentialPermissions(context)
if (status.allEssentialGranted) {
    // 所有必需权限已授予
}
```

## 用户流程

### 首次启动流程
```
启动APP
  ↓
检查 isFirstLaunch
  ↓
├─ true → OnboardingActivity (引导页)
│          ↓
│        4页滑动介绍
│          ↓
│        点击"开始使用"
│          ↓
│        PermissionSetupActivity (权限设置)
│          ↓
│        请求必需权限
│          ↓
│        设为默认桌面
│          ↓
│        进入 MainActivity
│          ↓
│        标记 isFirstLaunch = false
│
└─ false → MainActivity (主页)
```

### 权限管理流程
```
设置页面
  ↓
点击"权限管理"
  ↓
PermissionManagementScreen
  ↓
├─ 查看所有权限状态
├─ 点击"授权"按钮 → 请求权限
├─ 点击"无障碍服务" → AccessibilityGuideDialog
└─ 返回时自动刷新状态
```

## 字符串资源

所有新增的字符串资源已添加到 `strings.xml`:
- `onboarding_*` - 引导页相关
- `permission_*` - 权限管理相关
- `accessibility_guide_*` - 无障碍引导相关

## AndroidManifest 更新

新增两个Activity:
```xml
<!-- 引导页Activity -->
<activity android:name=".ui.activity.OnboardingActivity" ... />

<!-- 权限设置Activity -->
<activity android:name=".ui.activity.PermissionSetupActivity" ... />
```

## 数据持久化

使用DataStore存储首次启动标记:
```kotlin
// SettingsRepository
val IS_FIRST_LAUNCH = booleanPreferencesKey("is_first_launch")

suspend fun updateIsFirstLaunch(isFirst: Boolean) {
    dataStore.edit { it[IS_FIRST_LAUNCH] = isFirst }
}
```

## 测试建议

1. **首次启动测试**:
   - 卸载并重新安装APP
   - 验证引导页是否显示
   - 跳过功能是否正常
   - 完成后是否不再显示

2. **权限管理测试**:
   - 进入权限管理页面
   - 点击各个权限的"授权"按钮
   - 验证状态实时更新
   - 在系统设置中撤销权限,返回验证状态

3. **无障碍引导测试**:
   - 点击无障碍服务权限
   - 验证引导对话框显示
   - 跟随步骤开启服务
   - 点击"检查状态"验证检测逻辑

## 注意事项

1. **权限请求时机**: 
   - 必需权限在首次启动时集中请求
   - 可选权限按需请求(如拍照时才请求相机)

2. **无障碍服务检测**:
   - 使用系统API检测,准确可靠
   - ServiceId格式: `包名/完整类名`

3. **用户体验**:
   - 引导页可跳过,不强制用户观看
   - 权限说明清晰,让用户理解为什么需要
   - 支持稍后设置,不阻塞用户使用

## 后续优化建议

## 最近新增功能 (2026-03-13)

### 4. 智能语音助手 (Voice Assistant)

**位置**: `VoiceAssistantDialog` + `VoiceCommandParser`

**功能特点**:
- **指令解析**: 基于关键词加权的 `VoiceCommandParser`，支持自然语言识别。
- **自动拨号**: 识别到“打电话给 [备注名]”后，自动调起微信全自动拨号流程。
- **UI 对话框**: 实时展示语音识别文本与解析后的执行指令。
- **焦点同步**: 触发指令后立即关闭对话框，确保后台微信能够成功抢占首屏焦点。

### 5. 微信无障碍服务鲁棒性优化

针对微信不同版本和 UI 变动，对 `SelectToSpeakService` 进行了深度加固。

**优化点**:
- **Activity 模糊匹配**: 兼容微信在搜索流程中可能出现的多种类名（如 `FTSMainUI`, `FrameLayout` 等），不再死板依赖单一 Activity 名称识别。
- **双重节点定位**: 在点击联系人环节，支持 `viewId 查找` + `备注名文本查找` 双重保障逻辑。
- **全链路追踪日志**: 为 1-7 个自动化阶段（Index）添加了详细的追踪日志，方便调试。

## 毕业设计进度规划重构

**位置**: `docxment/GRADUATION_PROJECT_SCHEDULE.md`

**更新内容**:
- 将原有 7 周计划扩展为 **14 周** 详细进度表。
- 前 3 周保持基础框架建设不变。
- 后 11 周针对目前已实现的真实功能进行了详细任务拆解，涵盖：响应式时钟、联系人模型、微信自动化及插件化重构等。

---
*更新时间: 2026-03-13*
