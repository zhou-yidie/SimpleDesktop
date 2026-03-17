# SimpleDesktop 简易桌面

<div align="center">
  <img src="app/src/main/ic_launcher-playstore.png" width="120" height="120" alt="SimpleDesktop Logo">
  <br>
  <h3>为老年人量身定制的简化版Android桌面应用</h3>
  <p>让科技更贴心，让操作更简单</p>
</div>

## 📱 项目简介

SimpleDesktop（简易桌面）是一款专为老年人设计的Android桌面启动器应用。它简化了智能手机的操作界面，提供大字体、高对比度的显示效果，让老年人能够轻松使用智能手机的基本功能。

### ✨ 主要特性

- 🏠 **简化桌面**：系统级桌面接管，提供极致简洁的交互体验
- 👥 **通讯增强**：支持一键快速拨打普通电话、微信语音及微信视频通话
- 🎙️ **智能语音**：内置语音助手，支持“打电话给某某”等自然语言指令
- ♿ **高鲁棒性无障碍**：针对微信自动化进行了深度优化（Activity模糊匹配、节点/文本双重定位）
- 🌤️ **实时信息板**：首页集成时间、农历、节气与实时天气聚合
- 🛡️ **网络守护**：WiFi 异常自动检测与自愈引导系统
- 🎨 **主题定制**：支持蓝色/橙色高对比度主题，全局字体动态缩放

## 🏗️ 技术架构

### 开发环境
- **开发语言**：Kotlin
- **最小SDK版本**：API 24 (Android 7.0)
- **目标SDK版本**：API 35 (Android 15)
- **编译SDK版本**：API 35

### 核心技术栈
- **UI框架**：Jetpack Compose + Material3
- **架构模式**：MVVM + Repository Pattern + 动态插件化架构 (Plugin Architecture)
- **依赖注入**：Dagger Hilt
- **数据库**：Room Database
- **数据存储**：DataStore Preferences
- **网络请求**：Retrofit + OkHttp
- **图片加载**：Coil
- **异步处理**：Kotlin Coroutines
- **导航**：Navigation Compose

### 📂 项目目录结构

```text
SimpleDesktop/
├── app/                    # Android 应用主工程
├── docs/                   # 项目说明文档、进度表与架构设计
│   ├── BUILD_SUCCESS.md    # 最近一次构建成功报告
│   ├── NEW_FEATURES.md      # 新增特性详细说明
│   ├── PLUGIN_ARCHITECTURE.md # 插件化架构设计文档
│   └── ...                 # 毕业设计进度及路线图
├── skills/                 # 智能体扩展技能包 (Skillhub)
├── .learnings/             # 自我改进记录与错误库
├── AGENTS.md               # 全局 AI 开发准则 (核心规范)
└── README.md               # 项目主页
```

## 🚀 功能模块

### 1. 主界面 (HomeScreen)
- 显示当前时间、日期、星期
- 显示农历日期
- 实时天气信息
- 联系人快速拨号网格
- 常用应用快速启动

### 2. 联系人管理
- 添加/编辑/删除联系人
- 支持头像设置
- 拖拽排序功能
- 从系统通讯录导入
- 支持电话、微信语音、微信视频通话

### 3. 应用管理
- 扫描已安装应用
- 自定义常用应用列表
- 应用分类显示
- 拖拽排序

### 4. 引导与设置功能 (Onboarding & Settings)
- 首次进入的4页滑动交互式图文引导
- 集中式的权限管理页面与可视化状态面板
- 智能的无障碍服务图文引导对话框与检测机制
- 语音设置（语音反馈、语速、音量）
- 显示设置（字体大小、对比度）
- 主题设置（蓝色/橙色主题）
- 开机自启动设置

### 5. 微信集成与自动化优化
- **全自动拨号**：一键/语音触发微信视频、语音通话流程。
- **焦点冲突解决**：同步 UI 关闭与 Intent 启动，确保微信获取首屏焦点。
- **高兼容性方案**：深度使用 `AccessibilityService`，支持 Activity 模糊类名匹配与“ID+文本”双重节点查找。
- **执行状态追踪**：全链路 Index (1-7) 状态追踪日志，方便调试与维护。

## 📋 权限说明

应用需要以下权限来提供完整功能：

- **电话权限**：拨打电话功能
- **联系人权限**：读取和管理联系人
- **相机权限**：拍摄联系人头像
- **存储权限**：保存图片和数据
- **位置权限**：获取天气信息
- **网络权限**：获取天气数据
- **悬浮窗权限**：显示提醒窗口
- **无障碍服务**：微信自动化操作
- **开机启动权限**：自动启动应用

## 🛠️ 开发设置

### 环境要求
- Android Studio 2024.2.1 或更高版本
- JDK 8 或更高版本
- Android SDK API 35
- Gradle 8.10.0

### 构建项目
1. 克隆项目到本地
```bash
git clone https://github.com/zhou-yidie/SimpleDesktop.git
cd SimpleDesktop
```

2. 使用Android Studio打开项目

3. 同步Gradle依赖
```bash
./gradlew build
```

4. 运行项目
```bash
./gradlew installDebug
```

### 主要依赖版本
- Kotlin: 2.0.21
- Compose BOM: 2024.09.00
- Hilt: 2.56.2
- Room: 2.6.1
- Retrofit: 2.9.0
- Navigation: 2.7.5

## 📦 安装说明

### 从源码构建
1. 确保满足开发环境要求
2. 构建Release版本：
```bash
./gradlew assembleRelease
```
3. 安装APK文件到设备

### 首次使用
1. 安装后首次启动会请求必要权限
2. 建议设置为默认桌面应用
3. 根据使用习惯配置联系人和常用应用

## 🤝 协作与规范

### 全局准则
本仓库已配置智能体协作规范，**所有 AI 开发助手在开始工作前必须阅读并遵循 [AGENTS.md](AGENTS.md)**。

### 开发规范
- **语言原则**：
  - **代码标识符**：必须使用**英文**（变量、函数、类名严禁拼音）。
  - **文档与注释**：包括 `task.md`、代码注释、及所有生成文档，必须使用**中文**。
- **Git 规范**：使用标准类型头，如 `feat: 新增...` 或 `fix: 修复...`。
- **自我改进**：遇到错误或修正时，使用 `self-improvement` 技能更新 `.learnings/`。

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- [wechat_video_call](https://github.com/davidche1116/wechat_video_call)
- [微信控件混淆导致节点无法识别解决方案](https://zhuanlan.zhihu.com/p/1898312642701026938)

---

<div align="center">
  <p>让科技更有温度，让每一次触碰都充满关怀 ❤️</p>
</div>
