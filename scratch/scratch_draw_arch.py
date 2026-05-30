import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures"
plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_fig1_3():
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('off')
    
    # Set explicit limits for predictable layouts
    ax.set_xlim(0.05, 0.95)
    ax.set_ylim(0.02, 0.98)
    
    # === 学术图表字体缩放数学模型 (方案一) ===
    # 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
    latex_scale = 0.9            # LaTeX 中的 width=0.9\textwidth 缩放因子
    latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
    canvas_width_inch = 12.0     # Matplotlib 画布宽度
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例
    
    X_pdf = 12.0 * 0.8                 # 大字体：与正文一致的 12pt (小四)
    Y_pdf = 11.0 * 0.8                 # 小小字体：X - 1 pt = 11pt
    
    font_title_size = X_pdf / scale_factor
    font_details_size = Y_pdf / scale_factor
    font_arrow_size = Y_pdf / scale_factor
    
    # 传统方案
    ax.add_patch(patches.FancyBboxPatch((0.1, 0.6), 0.25, 0.2, boxstyle="round,pad=0.05", fc="#f0f0f0", ec="#888888", lw=2))
    ax.text(0.225, 0.7, "传统极简桌面\n(大字体)", ha='center', va='center', fontsize=font_title_size, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.65, 0.6), 0.25, 0.2, boxstyle="round,pad=0.05", fc="#ffe6e6", ec="#cc0000", lw=2))
    ax.text(0.775, 0.7, "微信原生界面\n(极其复杂)", ha='center', va='center', fontsize=font_title_size, fontweight='bold')
    
    # Arrow
    ax.annotate("", xy=(0.65, 0.7), xytext=(0.35, 0.7), arrowprops=dict(arrowstyle="->", lw=2.5, color="#888888", ls="dashed"))
    ax.text(0.5, 0.76, "点击跳转", ha='center', va='center', fontsize=font_arrow_size, fontweight='bold', color="#555555")
    ax.text(0.5, 0.63, "体验割裂", ha='center', va='center', fontsize=font_arrow_size, fontweight='bold', color="#cc0000")
    
    # 本课题方案
    ax.add_patch(patches.FancyBboxPatch((0.1, 0.1), 0.25, 0.2, boxstyle="round,pad=0.05", fc="#e6f2ff", ec="#0066cc", lw=2))
    ax.text(0.225, 0.2, "SimpleDesktop\n适老桌面", ha='center', va='center', fontsize=font_title_size, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.65, 0.1), 0.25, 0.2, boxstyle="round,pad=0.05", fc="#e6ffe6", ec="#009900", lw=2))
    ax.text(0.775, 0.2, "微信视频通话\n(直达)", ha='center', va='center', fontsize=font_title_size, fontweight='bold')
    
    # Arrow
    ax.annotate("", xy=(0.65, 0.2), xytext=(0.35, 0.2), arrowprops=dict(arrowstyle="->", lw=3.5, color="#0066cc"))
    ax.text(0.5, 0.26, "无障碍 FSM 引擎", ha='center', va='center', fontsize=font_arrow_size, color="#0066cc", fontweight='bold')
    ax.text(0.5, 0.13, "全自动跨应用流转", ha='center', va='center', fontsize=font_arrow_size, color="#0066cc")
    
    thesis_fig_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
    os.makedirs(thesis_fig_dir, exist_ok=True)
    
    plt.savefig(os.path.join(out_dir, 'fig1_3_architecture_compare.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, 'fig1_3_architecture_compare.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(thesis_fig_dir, 'fig1_3_architecture_compare.png'), dpi=300, bbox_inches='tight')
    plt.close()
 
def draw_fig1_4():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Set explicit limits so Matplotlib handles bounding boxes predictably
    ax.set_xlim(0.08, 0.92)
    ax.set_ylim(0.02, 0.98)
    
    # === 学术图表字体缩放数学模型 (方案一) ===
    # 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
    latex_scale = 0.9            # LaTeX 中的 width=0.9\textwidth 缩放因子
    latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
    canvas_width_inch = 12.0     # Matplotlib 画布宽度
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例
    
    X_pdf = 12.0 * 0.8                 # 大层级标题：与正文一致的 12pt (小四)
    Y_pdf = 11.0 * 0.8                 # 内部具体模块文字：11pt
    
    font_title_size = X_pdf / scale_factor
    font_details_size = Y_pdf / scale_factor
    
    # Layer 1: 底层守护层
    ax.add_patch(patches.Rectangle((0.1, 0.05), 0.8, 0.25, fc="#f2f2f2", ec="#888888", lw=2))
    ax.text(0.12, 0.245, "底层守护层", fontsize=font_title_size, fontweight='bold', color="#666666", va='center')
    
    ax.add_patch(patches.FancyBboxPatch((0.15, 0.08), 0.18, 0.11, boxstyle="round,pad=0.015", fc="white", ec="#888888", lw=1.5))
    ax.text(0.24, 0.135, "网络自愈卫士", ha='center', va='center', fontsize=font_details_size, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.41, 0.08), 0.18, 0.11, boxstyle="round,pad=0.015", fc="white", ec="#888888", lw=1.5))
    ax.text(0.5, 0.135, "微内核插件引擎", ha='center', va='center', fontsize=font_details_size, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.67, 0.08), 0.18, 0.11, boxstyle="round,pad=0.015", fc="white", ec="#888888", lw=1.5))
    ax.text(0.76, 0.135, "无障碍事件调度", ha='center', va='center', fontsize=font_details_size, fontweight='bold')
    
    # Layer 2: 业务核心层
    ax.add_patch(patches.Rectangle((0.1, 0.38), 0.8, 0.25, fc="#e6f2ff", ec="#0066cc", lw=2))
    ax.text(0.12, 0.575, "业务核心层", fontsize=font_title_size, fontweight='bold', color="#0066cc", va='center')
    
    ax.add_patch(patches.FancyBboxPatch((0.15, 0.41), 0.18, 0.11, boxstyle="round,pad=0.015", fc="white", ec="#0066cc", lw=1.5))
    ax.text(0.24, 0.465, "联系人解析\n(Room)", ha='center', va='center', fontsize=font_details_size, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.41, 0.41), 0.18, 0.11, boxstyle="round,pad=0.015", fc="white", ec="#0066cc", lw=1.5))
    ax.text(0.5, 0.465, "微信7态状态机", ha='center', va='center', fontsize=font_details_size, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.67, 0.41), 0.18, 0.11, boxstyle="round,pad=0.015", fc="white", ec="#0066cc", lw=1.5))
    ax.text(0.76, 0.465, "语音语义解析\n(NLP)", ha='center', va='center', fontsize=font_details_size, fontweight='bold')
    
    # Layer 3: 表现交互层
    ax.add_patch(patches.Rectangle((0.1, 0.70), 0.8, 0.25, fc="#fff2e6", ec="#ff8000", lw=2))
    ax.text(0.12, 0.895, "表现交互层", fontsize=font_title_size, fontweight='bold', color="#cc6600", va='center')
    
    ax.add_patch(patches.FancyBboxPatch((0.25, 0.73), 0.2, 0.11, boxstyle="round,pad=0.015", fc="white", ec="#ff8000", lw=1.5))
    ax.text(0.35, 0.785, "Compose 极简UI", ha='center', va='center', fontsize=font_details_size, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.55, 0.73), 0.2, 0.11, boxstyle="round,pad=0.015", fc="white", ec="#ff8000", lw=1.5))
    ax.text(0.65, 0.785, "动态高对比度引擎", ha='center', va='center', fontsize=font_details_size, fontweight='bold')
    
    # Arrows between layers (perfectly aligned with container boundaries)
    ax.annotate("", xy=(0.5, 0.38), xytext=(0.5, 0.30), arrowprops=dict(arrowstyle="->", lw=2.5, color="#888888", ls="dashed"))
    ax.annotate("", xy=(0.5, 0.70), xytext=(0.5, 0.63), arrowprops=dict(arrowstyle="->", lw=2.5, color="#888888", ls="dashed"))
    
    thesis_fig_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
    
    plt.savefig(os.path.join(out_dir, 'fig1_4_system_overview.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, 'fig1_4_system_overview.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(thesis_fig_dir, 'fig1_4_system_overview.png'), dpi=300, bbox_inches='tight')
    plt.close()
draw_fig1_3()
draw_fig1_4()
print("Successfully generated images for 1.3 and 1.4.")
