# 智能体协作规范 (Agent Guidelines)

本文件定义了 AI 智能体（如 Antigravity, Claude, Copilot）在参与本仓库开发时必须遵循的全局准则。

## 1. 核心工作语言：中文 (Primary Language: Chinese)

> [!IMPORTANT]
> 本项目的**工作语言为中文**。

- **所有 AI 生成的内部/外部文档**（包括但不限于 `task.md`、`implementation_plan.md`、`walkthrough.md`）必须使用**中文**编写。
- **对话回复**必须使用**中文**。
- **Git 提交信息**建议格式：`<type>: <中文描述>`。
- **代码注释**必须包含详细的**中文**说明。

## 2. 编码规范 (Coding Standards)

请严格遵守 `zh-cn-dev-standard` 技能中的定义：
- **标识符英文**：变量、函数、类名严禁拼音，必须使用专业英文。
- **注释中文**：解释逻辑背后的原因（Why）。

## 3. 自我改进与学习 (Self-Improvement)

- 在发现工具报错、规范冲突或收到用户修正时，请务必调用 `self-improvement` 技能。
- 所有的学习成果应记录在 `.learnings/` 目录下，并定期评估是否有必要提升至本文件。

---
*这些规则旨在确保开发过程的高效与一致性，AI 智能体在处理任何任务前应首先阅读本文件。*
