import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures"
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

def draw_fig1_3():
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('off')
    
    # 传统方案
    ax.add_patch(patches.FancyBboxPatch((0.1, 0.6), 0.25, 0.2, boxstyle="round,pad=0.05", fc="#f0f0f0", ec="#888888", lw=2))
    ax.text(0.225, 0.7, "传统极简桌面\n(大字体)", ha='center', va='center', fontsize=22, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.65, 0.6), 0.25, 0.2, boxstyle="round,pad=0.05", fc="#ffe6e6", ec="#cc0000", lw=2))
    ax.text(0.775, 0.7, "微信原生界面\n(极其复杂)", ha='center', va='center', fontsize=22, fontweight='bold')
    
    # Arrow
    ax.annotate("", xy=(0.65, 0.7), xytext=(0.35, 0.7), arrowprops=dict(arrowstyle="->", lw=2.5, color="#888888", ls="dashed"))
    ax.text(0.5, 0.76, "点击跳转", ha='center', va='center', fontsize=20, fontweight='bold', color="#555555")
    ax.text(0.5, 0.63, "体验割裂", ha='center', va='center', fontsize=20, fontweight='bold', color="#cc0000")
    
    # 本课题方案
    ax.add_patch(patches.FancyBboxPatch((0.1, 0.1), 0.25, 0.2, boxstyle="round,pad=0.05", fc="#e6f2ff", ec="#0066cc", lw=2))
    ax.text(0.225, 0.2, "SimpleDesktop\n适老桌面", ha='center', va='center', fontsize=22, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.65, 0.1), 0.25, 0.2, boxstyle="round,pad=0.05", fc="#e6ffe6", ec="#009900", lw=2))
    ax.text(0.775, 0.2, "微信视频通话\n(直达)", ha='center', va='center', fontsize=22, fontweight='bold')
    
    # Arrow
    ax.annotate("", xy=(0.65, 0.2), xytext=(0.35, 0.2), arrowprops=dict(arrowstyle="->", lw=3.5, color="#0066cc"))
    ax.text(0.5, 0.26, "无障碍 FSM 引擎", ha='center', va='center', fontsize=20, color="#0066cc", fontweight='bold')
    ax.text(0.5, 0.13, "全自动跨应用流转", ha='center', va='center', fontsize=20, color="#0066cc")
    
    thesis_fig_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
    os.makedirs(thesis_fig_dir, exist_ok=True)
    
    plt.savefig(os.path.join(out_dir, 'fig1_3_architecture_compare.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, 'fig1_3_architecture_compare.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(thesis_fig_dir, 'fig1_3_architecture_compare.png'), dpi=300, bbox_inches='tight')
    plt.close()

def draw_fig1_4():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Layer 1: 底层守护层
    ax.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.2, fc="#f2f2f2", ec="#888888", lw=2))
    ax.text(0.12, 0.26, "底层守护层", fontsize=22, fontweight='bold', color="#666666")
    
    ax.add_patch(patches.FancyBboxPatch((0.15, 0.13), 0.18, 0.1, boxstyle="round,pad=0.02", fc="white", ec="#888888", lw=1.5))
    ax.text(0.24, 0.18, "网络自愈卫士", ha='center', va='center', fontsize=20, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.41, 0.13), 0.18, 0.1, boxstyle="round,pad=0.02", fc="white", ec="#888888", lw=1.5))
    ax.text(0.5, 0.18, "微内核插件引擎", ha='center', va='center', fontsize=20, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.67, 0.13), 0.18, 0.1, boxstyle="round,pad=0.02", fc="white", ec="#888888", lw=1.5))
    ax.text(0.76, 0.18, "无障碍事件调度", ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Layer 2: 业务核心层
    ax.add_patch(patches.Rectangle((0.1, 0.4), 0.8, 0.2, fc="#e6f2ff", ec="#0066cc", lw=2))
    ax.text(0.12, 0.56, "业务核心层", fontsize=22, fontweight='bold', color="#0066cc")
    
    ax.add_patch(patches.FancyBboxPatch((0.15, 0.43), 0.18, 0.1, boxstyle="round,pad=0.02", fc="white", ec="#0066cc", lw=1.5))
    ax.text(0.24, 0.48, "联系人解析\n(Room)", ha='center', va='center', fontsize=20, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.41, 0.43), 0.18, 0.1, boxstyle="round,pad=0.02", fc="white", ec="#0066cc", lw=1.5))
    ax.text(0.5, 0.48, "微信7态状态机", ha='center', va='center', fontsize=20, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.67, 0.43), 0.18, 0.1, boxstyle="round,pad=0.02", fc="white", ec="#0066cc", lw=1.5))
    ax.text(0.76, 0.48, "语音语义解析\n(NLP)", ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Layer 3: 表现交互层
    ax.add_patch(patches.Rectangle((0.1, 0.7), 0.8, 0.2, fc="#fff2e6", ec="#ff8000", lw=2))
    ax.text(0.12, 0.86, "表现交互层", fontsize=22, fontweight='bold', color="#cc6600")
    
    ax.add_patch(patches.FancyBboxPatch((0.25, 0.73), 0.2, 0.1, boxstyle="round,pad=0.02", fc="white", ec="#ff8000", lw=1.5))
    ax.text(0.35, 0.78, "Compose 极简UI", ha='center', va='center', fontsize=20, fontweight='bold')
    
    ax.add_patch(patches.FancyBboxPatch((0.55, 0.73), 0.2, 0.1, boxstyle="round,pad=0.02", fc="white", ec="#ff8000", lw=1.5))
    ax.text(0.65, 0.78, "动态高对比度引擎", ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Arrows between layers
    ax.annotate("", xy=(0.5, 0.4), xytext=(0.5, 0.3), arrowprops=dict(arrowstyle="->", lw=2, color="#888888", ls="dashed"))
    ax.annotate("", xy=(0.5, 0.7), xytext=(0.5, 0.6), arrowprops=dict(arrowstyle="->", lw=2, color="#888888", ls="dashed"))
    
    thesis_fig_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
    
    plt.savefig(os.path.join(out_dir, 'fig1_4_system_overview.png'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, 'fig1_4_system_overview.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(thesis_fig_dir, 'fig1_4_system_overview.png'), dpi=300, bbox_inches='tight')
    plt.close()

draw_fig1_3()
draw_fig1_4()
print("Successfully generated images for 1.3 and 1.4.")
