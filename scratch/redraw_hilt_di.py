import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_hilt_di():
    # Make canvas wide and high for massive readable text
    fig, ax = plt.subplots(figsize=(24, 13), dpi=300)
    ax.axis('off')
    
    # Coordinates limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # === 学术图表字体缩放数学模型 (方案一) ===
    # 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
    latex_scale = 0.9            # LaTeX 中的 width=0.9\textwidth 缩放因子
    latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
    canvas_width_inch = 24.0     # Matplotlib 画布宽度
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例
    
    X_pdf = 12.0 * 0.8                 # 大层级标题：与正文一致的 12pt (小四)
    Y_pdf = 11.0 * 0.8                 # 内部具体模块文字：11pt
    
    font_large_size = X_pdf / scale_factor
    font_mid_size = Y_pdf / scale_factor
    font_small_size = Y_pdf / scale_factor
    
    # Color palette
    container_border = "#9e9e9e"
    green_fill = "#e8f5e9"
    green_border = "#43a047"
    orange_fill = "#fff3e0"
    orange_border = "#fb8c00"
    blue_fill = "#e3f2fd"
    blue_border = "#1976d2"
    
    # --- 1. Large Outer Container (Grey dashed) ---
    container = patches.FancyBboxPatch(
        (0.02, 0.22), 0.96, 0.75,
        boxstyle="round,pad=0.005",
        fc="none", ec=container_border, lw=3, ls="--",
        zorder=1
    )
    ax.add_patch(container)
    
    # Top title inside container
    ax.text(
        0.50, 0.92, "Dagger-Hilt 依赖注入全局容器",
        ha='center', va='center', fontsize=font_large_size, fontweight='bold', color="#37474f"
    )
    
    # --- 2. Two Top Module Green Boxes ---
    # Left Module
    box_lm = patches.FancyBboxPatch(
        (0.05, 0.67), 0.42, 0.18,
        boxstyle="round,pad=0.005",
        fc=green_fill, ec=green_border, lw=3.5,
        zorder=2
    )
    ax.add_patch(box_lm)
    ax.text(
        0.26, 0.79, "@Module",
        ha='center', va='center', fontsize=font_large_size, fontweight='bold', color="#1b5e20"
    )
    ax.text(
        0.26, 0.72, "DatabaseModule (提供数据库实例)",
        ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#1b5e20"
    )
    
    # Right Module
    box_rm = patches.FancyBboxPatch(
        (0.53, 0.67), 0.42, 0.18,
        boxstyle="round,pad=0.005",
        fc=green_fill, ec=green_border, lw=3.5,
        zorder=2
    )
    ax.add_patch(box_rm)
    ax.text(
        0.74, 0.79, "@Module",
        ha='center', va='center', fontsize=font_large_size, fontweight='bold', color="#1b5e20"
    )
    ax.text(
        0.74, 0.72, "DataStoreModule (提供偏好实例)",
        ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#1b5e20"
    )
    
    # --- 3. Center Component Orange Box ---
    box_cc = patches.FancyBboxPatch(
        (0.20, 0.38), 0.60, 0.20,
        boxstyle="round,pad=0.005",
        fc=orange_fill, ec=orange_border, lw=4,
        zorder=2
    )
    ax.add_patch(box_cc)
    ax.text(
        0.50, 0.51, "@SingletonComponent",
        ha='center', va='center', fontsize=font_large_size, fontweight='bold', color="#e65100"
    )
    ax.text(
        0.50, 0.44, "(单例组件调度中心)",
        ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#e65100"
    )
    
    # --- 4. Solid Blue Arrows (Modules to Component) ---
    # Left solid blue arrow
    ax.annotate(
        "", xy=(0.38, 0.58), xytext=(0.26, 0.67),
        arrowprops=dict(arrowstyle="-|>", color="#1976d2", lw=5, mutation_scale=25),
        zorder=3
    )
    # Right solid blue arrow
    ax.annotate(
        "", xy=(0.62, 0.58), xytext=(0.74, 0.67),
        arrowprops=dict(arrowstyle="-|>", color="#1976d2", lw=5, mutation_scale=25),
        zorder=3
    )
    
    # --- 5. Two Bottom Consumer Blue Boxes ---
    # Left Bottom Box
    box_lb = patches.FancyBboxPatch(
        (0.02, 0.03), 0.46, 0.16,
        boxstyle="round,pad=0.005",
        fc=blue_fill, ec=blue_border, lw=3.5,
        zorder=2
    )
    ax.add_patch(box_lb)
    ax.text(
        0.25, 0.13, "DesktopViewModel",
        ha='center', va='center', fontsize=font_large_size, fontweight='bold', color="#0d47a1"
    )
    ax.text(
        0.25, 0.07, "(@HiltViewModel 消费者)",
        ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#0d47a1"
    )
    
    # Right Bottom Box
    box_rb = patches.FancyBboxPatch(
        (0.52, 0.03), 0.46, 0.16,
        boxstyle="round,pad=0.005",
        fc=blue_fill, ec=blue_border, lw=3.5,
        zorder=2
    )
    ax.add_patch(box_rb)
    ax.text(
        0.75, 0.13, "AccessibilityService",
        ha='center', va='center', fontsize=font_large_size, fontweight='bold', color="#0d47a1"
    )
    ax.text(
        0.75, 0.07, "(@AndroidEntryPoint 消费者)",
        ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#0d47a1"
    )
    
    # --- 6. Red Dashed Arrows (Component to Bottom Consumers) ---
    # Left red dashed arrow
    ax.annotate(
        "", xy=(0.25, 0.19), xytext=(0.40, 0.38),
        arrowprops=dict(arrowstyle="-|>", color="#d32f2f", lw=5, ls="--", mutation_scale=25),
        zorder=3
    )
    # Right red dashed arrow
    ax.annotate(
        "", xy=(0.75, 0.19), xytext=(0.60, 0.38),
        arrowprops=dict(arrowstyle="-|>", color="#d32f2f", lw=5, ls="--", mutation_scale=25),
        zorder=3
    )
    
    # Labels near red arrows, placed to the sides to prevent overlapping the lines
    ax.text(
        0.18, 0.28, "@Inject\n自动注入",
        ha='center', va='center', fontsize=font_small_size, fontweight='bold', color="#c62828",
        multialignment='center'
    )
    ax.text(
        0.82, 0.28, "@Inject\n自动注入",
        ha='center', va='center', fontsize=font_small_size, fontweight='bold', color="#c62828",
        multialignment='center'
    )
    
    output_path = os.path.join(out_dir, 'fig2_2_hilt_di.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print("Successfully generated Dagger-Hilt dependency injection diagram!")

if __name__ == '__main__':
    draw_hilt_di()
