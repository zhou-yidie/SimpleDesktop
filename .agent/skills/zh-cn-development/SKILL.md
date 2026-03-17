---
name: zh-cn-dev-standard
description: 编码标识符遵循英文规范；注释、文档、所有 AI 生成的中间产物（Task/Plan/Walkthrough 等）全部使用中文。
trigger: 涉及代码编写、注释、文档生成、技术说明以及 AI 任务管理时自动触发
---

# 中文开发规范 (Chinese Dev Standard)

为了在中文语境下保持代码的专业性与可维护性，本项目遵循“**代码全球化逻辑，所有文档与 AI 交互产物本地化表述**”的核心原则。

> [!IMPORTANT]
> **AI 产物要求**：本规范不仅适用于项目源代码，同样适用于 AI 生成的 `task.md`、`implementation_plan.md`、`walkthrough.md` 以及 Task Boundary 中的 Summary。**禁止在这些文件中出现英文描述**。

## 1. 代码命名规范 (Code Naming)

**强制规则：所有代码层级的标识符必须使用英文。**

- **变量与函数**：使用对应语言的惯例（如 Python 用 `snake_case`，Java/JS 用 `camelCase`）。
- **类名**：使用 `PascalCase`（如 `DesktopManager`）。
- **常量**：使用全大写加下划线（如 `MAX_RETRY_COUNT`）。
- **严禁使用**：拼音命令（如 `yonghu_name`）、拼音首字母缩写、或者中英混杂。

> [!TIP]
> 如果遇到难以用简洁英文表达的业务名词，优先查阅本项目术语表（Glossary），或使用通用的行业术语。

## 2. 注释与文档规范 (Comments & Docs)

**核心原则：所有面向人类阅读的说明必须使用准确、简洁的中文。**

- **文件头注释**：说明文件的用途、版权及维护者。
- **函数/方法注释**：
  - **描述**：逻辑功能的概述。
  - **参数**：中文说明参数的具体含义、单位、范围。
  - **返回值**：说明返回数据的类型及业务意义。
- **逻辑内联注释**：解释“为什么”这样做（Why），而不仅仅是做了“什么”（What）。

```python
def check_wifi_persistence(retry_count):
    """
    检查 WiFi 连接的持久性，并在断开时尝试恢复。
    
    参数:
        retry_count: 最大尝试重连次数（整数）
    返回:
        bool: 是否最终连接成功
    """
    # 如果已手动关闭，则跳过检查（防止干扰用户意图）
    if is_manually_disabled:
        return True
    ...
```

## 3. Git 提交规范 (Commit Messages)

推荐格式：`<type>: <中文描述>`

| 类型 (Type) | 含义 |
| :--- | :--- |
| `feat` | 新功能 |
| `fix` | 修复缺陷 |
| `docs` | 文档更新 |
| `style` | 代码格式调整（不影响逻辑） |
| `refactor` | 重构代码 |
| `perf` | 性能优化 |
| `test` | 测试用例 |
| `chore` | 构建流程、工具变动 |

**示例：** `feat: 实现手机桌面无障碍节点自动提取功能`

## 4. 术语对照表 (Glossary)

为了防止翻译歧义，项目内统一以下常用术语：

- **Accessibility Service** -> 无障碍服务
- **UI Hierarchy / Node Tree** -> UI 节点树
- **Simulated Tap** -> 模拟点击
- **Launcher / Desktop** -> 桌面/启动器
- **Permission Grant** -> 权限授予

---
*本规范将根据项目演进持续更新，修改请同步至 `.agent/skills/` 对应位置。*