import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)
plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 扩大 figsize 容纳超大号文字
fig, ax = plt.subplots(figsize=(28, 18))
ax.axis('off')

# === 学术图表字体缩放数学模型 (方案一) ===
# 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
latex_scale = 1.0            # LaTeX 中的 width=\textwidth 缩放因子
latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
canvas_width_inch = 28.0     # Matplotlib 画布宽度
scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例

X_pdf = 12.0 * 0.8                 # 系统标题与模块标题：与正文一致的 12pt (小四)
Y_pdf = 11.0 * 0.8                 # 模块内部子列表文字：11pt

font_title_size = X_pdf / scale_factor
font_box_title_size = X_pdf / scale_factor
font_item_size = Y_pdf / scale_factor

# SimpleDesktop 系统标题
ax.add_patch(patches.FancyBboxPatch((0.25, 0.85), 0.5, 0.08, boxstyle="round,pad=0.02", fc="#0055aa", ec="#004488", lw=5.5))
ax.text(0.5, 0.89, "SimpleDesktop 系统核心功能模块", ha='center', va='center', fontsize=font_title_size, fontweight='bold', color='white')

# 模块定义
# 微调 x 坐标为 0.03, 0.355, 0.68 和 0.20, 0.52 以在宽度为 0.29 的情况下完美对齐连线
modules = [
    {
        "pos": (0.03, 0.44), "size": (0.29, 0.34),
        "title": "适老化界面模块", "color": "#e6f2ff", "edge": "#0066cc",
        "items": ["主屏聚合面板", "大字号与多主题切换", "联系人与应用管理", "设置中心与引导页", "动态高对比度模式"]
    },
    {
        "pos": (0.355, 0.44), "size": (0.29, 0.34),
        "title": "微信自动化直连模块", "color": "#e6ffe6", "edge": "#009900",
        "items": ["七阶段状态机引擎", "双通道节点检索算法", "焦点防冲突退避机制", "异常识别与自动重试", "无障碍事件流转调度"]
    },
    {
        "pos": (0.68, 0.44), "size": (0.29, 0.34),
        "title": "语音辅助模块", "color": "#fff2e6", "edge": "#ff8000",
        "items": ["多场景语音播报", "双层语音指令解析", "四层递进模糊匹配", "本地TTS引擎适配", "低电量/异常播报"]
    },
    {
        "pos": (0.20, 0.04), "size": (0.29, 0.34),
        "title": "联系人管理模块", "color": "#f2e6ff", "edge": "#6600cc",
        "items": ["联系人全生命周期维护", "响应式异步模糊查询", "批量删除与拖拽排序", "跨设备CSV导出迁移", "可视化分组卡片信息"]
    },
    {
        "pos": (0.52, 0.04), "size": (0.29, 0.34),
        "title": "WiFi网络守护模块", "color": "#ffe6eb", "edge": "#cc0044",
        "items": ["前台静默状态守护", "跨版本WiFi自动开启", "三分阶段断网自愈", "无障碍辅助开启网络", "异常排查语音引导"]
    }
]

for m in modules:
    x, y = m["pos"]
    w, h = m["size"]
    # 模块大框
    ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=m["color"], ec=m["edge"], lw=4.5))
    # 模块标题字号大 50%
    ax.text(x + w/2, y + h - 0.04, m["title"], ha='center', va='center', fontsize=font_box_title_size, fontweight='bold', color=m["edge"])
    
    # 内部划线
    ax.plot([x + 0.02, x + w - 0.02], [y + h - 0.07, y + h - 0.07], lw=2.5, color=m["edge"], alpha=0.5)

    # 模块子项字号大 50%
    for i, item in enumerate(m["items"]):
        item_y = y + h - 0.12 - i * 0.05
        ax.plot([x + 0.025], [item_y], marker='o', markersize=9, color=m["edge"])
        ax.text(x + 0.05, item_y, item, ha='left', va='center', fontsize=font_item_size, color="#333333")

# 绘制连线
# 中心线段
ax.plot([0.5, 0.5], [0.85, 0.81], lw=4.5, color="#555555") # 垂直短线
ax.plot([0.175, 0.825], [0.81, 0.81], lw=4.5, color="#555555") # 水平长线

# 第一排的垂直线段及箭头
ax.annotate("", xy=(0.175, 0.78), xytext=(0.175, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))
ax.annotate("", xy=(0.50, 0.78), xytext=(0.50, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))
ax.annotate("", xy=(0.825, 0.78), xytext=(0.825, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))

# 第二排的连线及箭头
ax.annotate("", xy=(0.345, 0.38), xytext=(0.345, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))
ax.annotate("", xy=(0.665, 0.38), xytext=(0.665, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))

plt.savefig(os.path.join(out_dir, 'fig3_1_system_modules.png'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(out_dir, 'fig3_1_system_modules.pdf'), dpi=300, bbox_inches='tight')
plt.close()
print("Generated fig3_1_system_modules.png and .pdf")
