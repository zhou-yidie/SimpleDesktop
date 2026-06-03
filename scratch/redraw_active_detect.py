import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_active_detect():
    # Set canvas to massive size to fit giant fonts comfortably
    fig, ax = plt.subplots(figsize=(28, 14), dpi=300)
    ax.axis('off')
    
    # Set explicit coordinate system (0 to 1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # === 学术图表字体缩放数学模型 (方案一) ===
    # 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
    latex_scale = 0.9            # LaTeX 中的 width=0.9\textwidth 缩放因子
    latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
    canvas_width_inch = 28.0     # Matplotlib 画布宽度
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例
    
    X_pdf = 12.0 * 0.8                 # 大层级标题：与正文一致的 12pt (小四)
    Y_pdf = 11.0 * 0.8                 # 内部具体模块文字：11pt
    Z_pdf = 10.0 * 0.8                 # 较小标注文字：10pt
    
    font_large_size = X_pdf / scale_factor
    font_mid_size = Y_pdf / scale_factor
    font_small_size = Z_pdf / scale_factor
    
    # Colors matching original layout
    grey_fill = "#f5f5f5"
    grey_border = "#9e9e9e"
    orange_fill = "#fff3e0"
    orange_border = "#fb8c00"
    green_fill = "#e8f5e9"
    green_border = "#43a047"
    yellow_fill = "#fffde7"
    yellow_border = "#c0ca33"
    
    # Top Titles
    ax.text(0.03, 0.94, "步骤一：混淆隔离态 (Ghost Nodes)", ha='left', va='center', fontsize=font_large_size, fontweight='bold', color="#212121")
    ax.text(0.97, 0.94, "步骤二：真实树挂载与特征定位", ha='right', va='center', fontsize=font_large_size, fontweight='bold', color="#212121")
    
    # Row Y ranges
    row_height = 0.18
    r1_y = 0.68
    r2_y = 0.44
    r3_y = 0.20
    
    # --- 1. Left Column (Grey Dashed Boxes) ---
    left_boxes = [
        {"y": r1_y, "text": "透明占位节点"},
        {"y": r2_y, "text": "混淆资源 ID"},
        {"y": r3_y, "text": "隐藏真实控件"}
    ]
    for item in left_boxes:
        box = patches.FancyBboxPatch(
            (0.04, item["y"]), 0.24, row_height,
            boxstyle="round,pad=0.005",
            fc=grey_fill, ec=grey_border, lw=3, ls="--",
            zorder=2
        )
        ax.add_patch(box)
        ax.text(
            0.16, item["y"] + row_height/2.0, item["text"],
            ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#424242"
        )
        
    # --- 2. Center Column (Orange Box) ---
    center_y = 0.39
    center_height = 0.28
    center_box = patches.FancyBboxPatch(
        (0.37, center_y), 0.26, center_height,
        boxstyle="round,pad=0.015",
        fc=orange_fill, ec=orange_border, lw=4,
        zorder=2
    )
    ax.add_patch(center_box)
    ax.text(
        0.50, center_y + center_height/2.0, "窗口内容震荡\n(微位移滑动 1-2px)",
        ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#e65100",
        multialignment='center'
    )
    
    # --- 3. Right Column (Green Boxes) ---
    right_boxes = [
        {"y": r1_y, "text": "真实控件子树暴露"},
        {"y": r2_y, "text": "拓扑深度提取"},
        {"y": r3_y, "text": "计算包围盒重心"}
    ]
    for item in right_boxes:
        box = patches.FancyBboxPatch(
            (0.72, item["y"]), 0.24, row_height,
            boxstyle="round,pad=0.005",
            fc=green_fill, ec=green_border, lw=3,
            zorder=2
        )
        ax.add_patch(box)
        ax.text(
            0.84, item["y"] + row_height/2.0, item["text"],
            ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#1b5e20"
        )
        
    # --- 4. Red Dashed Arrow (Left to Center) ---
    # Draw arrow line slightly longer to give room
    ax.annotate(
        "", xy=(0.37, 0.53), xytext=(0.28, 0.53),
        arrowprops=dict(arrowstyle="-|>", color="#d32f2f", lw=4.5, ls="--", mutation_scale=25),
        zorder=3
    )
    # Red label centered over the arrow
    ax.text(
        0.325, 0.56, "触发更新",
        ha='center', va='bottom', fontsize=font_small_size, fontweight='bold', color="#d32f2f"
    )
    
    # --- 5. Blue Arrow (Center to Right) ---
    # Draw arrow line starting slightly more inside the orange box
    ax.annotate(
        "", xy=(0.72, 0.53), xytext=(0.63, 0.53),
        arrowprops=dict(arrowstyle="-|>", color="#1976d2", lw=4.5, mutation_scale=25),
        zorder=3
    )
    # Blue label centered over the arrow
    ax.text(
        0.675, 0.56, "强制重绘\n(Remount)",
        ha='center', va='bottom', fontsize=font_small_size, fontweight='bold', color="#1976d2",
        multialignment='center'
    )
    
    # --- 6. Bottom Column (Yellow Box) ---
    bottom_y = 0.04
    bottom_height = 0.11
    bottom_box = patches.FancyBboxPatch(
        (0.015, bottom_y), 0.97, bottom_height,
        boxstyle="round,pad=0.005",
        fc=yellow_fill, ec=yellow_border, lw=3.5,
        zorder=2
    )
    ax.add_patch(bottom_box)
    
    text_content = (
        "UI 特征归一化模型 (Feature Normalization)\n"
        "匹配度 P = w1 × (相对拓扑关系) + w2 × (视觉重心偏移量) > 98%  ->  锁定目标"
    )
    ax.text(
        0.50, bottom_y + bottom_height/2.0,
        text_content,
        ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#827717",
        multialignment='center'
    )
    
    # --- 7. Connector Line (Right Column to Yellow Box) ---
    ax.plot([0.84, 0.50], [0.20, 0.15], color="#212121", lw=3.5, zorder=1)
    
    output_path = os.path.join(out_dir, 'fig2_3_shake_match.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print("Successfully generated active detection mechanism diagram!")

if __name__ == '__main__':
    draw_active_detect()
