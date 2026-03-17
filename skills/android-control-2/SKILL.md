---
name: android_control
description: 通过命令行工具 (uiautomator, screencap, input, am) 控制 Android 设备。它会自动先尝试以非 root 权限执行，必要时自动回退到 root 权限执行。
homepage: https://developer.android.com/studio/test/uiautomator
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":["sh"],"optional_bins":["su","uiautomator","input","am","screencap"]}}}
---

# Android Control 技能

直接使用 Clawdbot 通过内置的 Android 命令行工具控制 Android 手机。  
该技能始终首先尝试 **普通 (非 root)** 命令；如果失败，当 root 权限可用时，它会自动重试 **root 模式 (su)**。

## 功能特性

- 通过 `uiautomator dump` 获取 UI 层级结构快照
- 使用 `screencap` 截取屏幕
- 通过 `input` 模拟点击、滑动和输入事件
- 使用 `am start` 启动应用
- 如果非 root 失败，自动使用 root 重试

# 设置

大多数 Android ROM 包含 `uiautomator`, `input`, `screencap`, 以及 `am`。

为了启用 root 回退机制，请安装 Magisk 或者运行：
```bash
su
```

# 使用方法

## 获取 UI 快照 (uiautomator dump)

```bash
# 尝试非 root
uiautomator dump /sdcard/ui_dump.xml 2>/dev/null \
  && cat /sdcard/ui_dump.xml \
  || (
    # 回退到 root
    su -c "uiautomator dump /sdcard/ui_dump.xml" && su -c "cat /sdcard/ui_dump.xml"
  )
```

## 截取屏幕 (PNG, base64 编码)

```bash
TMP="/sdcard/ai_screen.png"

# 尝试非 root
screencap -p "$TMP" 2>/dev/null \
  && base64 "$TMP" \
  || (
    # 回退到 root
    su -c "screencap -p $TMP"
    su -c "base64 $TMP"
  )
```

## 点击屏幕

```bash
# 示例: 在坐标 (540, 1600) 处点击

input tap 540 1600 2>/dev/null \
  || su -c "input tap 540 1600"
```

## 滑动屏幕

```bash
# 示例: 在 300 毫秒内从 (500, 1600) 滑动到 (500, 600)

input swipe 500 1600 500 600 300 2>/dev/null \
  || su -c "input swipe 500 1600 500 600 300"
```

## 启动应用

```bash
# 示例: 启动 Android 设置

am start -n com.android.settings/.Settings 2>/dev/null \
  || su -c "am start -n com.android.settings/.Settings"
```

## 发送文本输入

```bash
# 示例: 发送文本 "Hello"

input text "Hello" 2>/dev/null \
  || su -c "input text 'Hello'"
```
