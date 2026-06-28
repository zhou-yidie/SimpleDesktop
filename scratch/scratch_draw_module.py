import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# out_dir：编译后图表保存的目标物理路径目录（指向 LaTeX 的 figures 目录）
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# plt.rcParams：配置全局中文字体为仿宋、宋体、微软雅黑等，以防中文字符乱码
plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示为方块的问题

# fig, ax：Matplotlib 的画布 Figure 和坐标轴 Axes 对象
fig, ax = plt.subplots(figsize=(28, 18))
ax.axis('off') # 隐去坐标轴标签和网格刻度，保持图表画面纯净

# === 学术图表字体缩放数学模型 ===
# latex_scale：LaTeX 编译中该图片的 width=\textwidth 缩放比例因子
latex_scale = 1.0            
# latex_textwidth_inch：A4 页面排版纸张的文本排版物理宽度，通常为 16cm 约合 6.3 英寸
latex_textwidth_inch = 6.3   
# canvas_width_inch：Matplotlib 画布的实际物理宽度 (28.0 英寸)
canvas_width_inch = 28.0     
# scale_factor：物理缩放比例因子，用于在超大画布上还原真实 PDF 最终呈现的字号感
scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  

# X_pdf：标题与模块标题设计在 PDF 中呈现的字号大小 (与正文一致的 12pt 小四字号，再乘以 0.8 适当避让)
X_pdf = 12.0 * 0.8                 
# Y_pdf：模块内部子列表文字设计在 PDF 中呈现的字号大小 (微调 10% 缩小以保障中文字句绝不溢出)
Y_pdf = 11.0 * 0.72                 

# font_title_size：主标题在超大画布上渲染的绝对字体大小
font_title_size = X_pdf / scale_factor
# font_box_title_size：模块矩形框标题渲染 of 绝对字体大小
font_box_title_size = X_pdf / scale_factor
# font_item_size：模块内部子功能条目渲染 of 绝对字体大小
font_item_size = Y_pdf / scale_factor

# -------------------------------------------------------------
# 1. 绘制 SimpleDesktop 系统主标题
# -------------------------------------------------------------
ax.add_patch(patches.FancyBboxPatch((0.25, 0.85), 0.5, 0.08, boxstyle="round,pad=0.02", fc="#0055aa", ec="#004488", lw=5.5))
ax.text(0.5, 0.89, "SimpleDesktop 系统核心功能模块", ha='center', va='center', fontsize=font_title_size, fontweight='bold', color='white')

# -------------------------------------------------------------
# 2. 绘制 5 大核心功能模块矩形框 (宽度扩宽至 0.30，消除 pad, 横向空间增加 12.2%)
# -------------------------------------------------------------
modules = [
    {
        "pos": (0.02, 0.44), "size": (0.30, 0.34),
        "title": "适老化界面模块", "color": "#e6f2ff", "edge": "#0066cc",
        "items": ["主屏卡片聚合面板", "响应式多档字号切换", "多主题与高对比度模式", "极简设置中心与引导", "卡片式应用快捷启动"]
    },
    {
        "pos": (0.35, 0.44), "size": (0.30, 0.34),
        "title": "微信自动化直连模块", "color": "#e6ffe6", "edge": "#009900",
        "items": ["七阶段状态机引擎", "双通道节点检索算法", "焦点防冲突退避机制", "异常识别与自动重试", "无障碍事件流转调度"]
    },
    {
        "pos": (0.68, 0.44), "size": (0.30, 0.34),
        "title": "语音辅助模块", "color": "#fff2e6", "edge": "#ff8000",
        "items": ["多场景语音播报", "双层语音指令解析", "四层递进模糊匹配", "本地TTS引擎适配", "低电量/异常播报"]
    },
    {
        "pos": (0.18, 0.04), "size": (0.30, 0.34),
        "title": "联系人管理模块", "color": "#f2e6ff", "edge": "#6600cc",
        "items": ["联系人全生命周期维护", "响应式异步模糊查询", "批量删除与拖拽排序", "跨设备CSV导出迁移", "可视化分组卡片信息"]
    },
    {
        "pos": (0.52, 0.04), "size": (0.30, 0.34),
        "title": "WiFi网络守护模块", "color": "#ffe6eb", "edge": "#cc0044",
        "items": ["前台静默状态守护", "跨版本WiFi自动开启", "三分阶段断网自愈", "无障碍辅助开启网络", "异常排查语音引导"]
    }
]

for m in modules:
    x, y = m["pos"] 
    w, h = m["size"] 
    
    # 2.1 绘制子模块圆角外框 (pad=0.0，使范围精确对齐坐标)
    ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.015", fc=m["color"], ec=m["edge"], lw=4.5))
    
    # 2.2 绘制子模块标题，在框内完美居中
    ax.text(x + w/2, y + h - 0.04, m["title"], ha='center', va='center', fontsize=font_box_title_size, fontweight='bold', color=m["edge"])
    
    # 2.3 绘制标题下分割线
    ax.plot([x + 0.02, x + w - 0.02], [y + h - 0.07, y + h - 0.07], lw=2.5, color=m["edge"], alpha=0.5)

    # 2.4 循环绘制该模块的子功能点 (小圆点及文字起点整体左移，留空横向长度)
    for i, item in enumerate(m["items"]):
        item_y = y + h - 0.12 - i * 0.05
        # 圆点设在 x + 0.02
        ax.plot([x + 0.02], [item_y], marker='o', markersize=9, color=m["edge"])
        # 文字设在 x + 0.042
        ax.text(x + 0.042, item_y, item, ha='left', va='center', fontsize=font_item_size, color="#333333")

# -------------------------------------------------------------
# 3. 绘制系统模块间的树状拓扑连线与方向箭头 (根据新中心点 0.17, 0.50, 0.83 精确对齐)
# -------------------------------------------------------------
# 3.1 绘制主标题垂下主干线
ax.plot([0.5, 0.5], [0.85, 0.81], lw=4.5, color="#555555") 
ax.plot([0.17, 0.83], [0.81, 0.81], lw=4.5, color="#555555") 

# 3.2 垂直分支指向第一排模块中轴线 (0.17, 0.50, 0.83)
ax.annotate("", xy=(0.17, 0.78), xytext=(0.17, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))
ax.annotate("", xy=(0.50, 0.78), xytext=(0.50, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))
ax.annotate("", xy=(0.83, 0.78), xytext=(0.83, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))

# 3.3 倾斜分支指向第二排模块中轴线 (0.33, 0.67)
ax.annotate("", xy=(0.33, 0.38), xytext=(0.33, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))
ax.annotate("", xy=(0.67, 0.38), xytext=(0.67, 0.81), arrowprops=dict(arrowstyle="->", lw=4.5, color="#555555"))

# -------------------------------------------------------------
# 4. 导出高清图表
# -------------------------------------------------------------
plt.savefig(os.path.join(out_dir, 'fig3_1_system_modules.png'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(out_dir, 'fig3_1_system_modules.pdf'), dpi=300, bbox_inches='tight')
plt.close()

print("Generated fig3_1_system_modules.png and .pdf successfully!")
