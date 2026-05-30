import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_focus_retreat():
    # Set canvas to (22, 12) for a perfectly proportioned sequence diagram
    fig, ax = plt.subplots(figsize=(22, 12), dpi=300)
    ax.axis('off')
    
    # Explicit coordinate system
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # === 学术图表字体缩放数学模型 (方案一) ===
    # 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
    latex_scale = 0.85           # LaTeX 中的 width=0.85\textwidth 缩放因子
    latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
    canvas_width_inch = 22.0     # Matplotlib 画布宽度
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例
    
    X_pdf = 12.0 * 0.8                 # 大层级和步骤文字：与正文一致的 12pt (小四)
    Y_pdf = 11.0 * 0.8                 # 内部具体模块与小标题文字：11pt
    
    font_header_size = X_pdf / scale_factor
    font_step_size = X_pdf / scale_factor
    font_box_size = Y_pdf / scale_factor
    
    # 3 Lifelines x-coordinates
    x_left = 0.17
    x_mid = 0.47
    x_right = 0.77
    
    # --- 1. Draw Lifeline Dashed Lines ---
    for x in [x_left, x_mid, x_right]:
        ax.plot([x, x], [0.06, 0.80], color="#757575", lw=2.5, ls="--", zorder=1)
        
    # --- 2. Draw Lifeline Header Boxes ---
    headers = [
        {"x_center": x_left, "text": "老年用户（干扰源）"},
        {"x_center": x_mid, "text": "桌面主程序"},
        {"x_center": x_right, "text": "无障碍服务引擎"}
    ]
    
    for h in headers:
        box_width = 0.23
        box_height = 0.13
        box = patches.FancyBboxPatch(
            (h["x_center"] - box_width/2.0, 0.80), box_width, box_height,
            boxstyle="round,pad=0.005",
            fc="#e3f2fd", ec="#1976d2", lw=3.5,
            zorder=3
        )
        ax.add_patch(box)
        ax.text(
            h["x_center"], 0.865, h["text"],
            ha='center', va='center', fontsize=font_header_size, fontweight='bold', color="#0d47a1",
            zorder=4
        )
        
    # --- 3. Step 1: 1. 自动化任务发起 (桌面主程序 -> 无障碍服务引擎) ---
    y1 = 0.71
    # Arrow
    ax.annotate(
        "", xy=(x_right, y1), xytext=(x_mid, y1),
        arrowprops=dict(arrowstyle="-|>", color="#212121", lw=4, mutation_scale=25),
        zorder=2
    )
    # Text
    ax.text(
        (x_mid + x_right)/2.0, y1 + 0.015, "1.  自动化任务发起",
        ha='center', va='bottom', fontsize=font_step_size, fontweight='bold', color="#212121"
    )
    
    # --- 4. Step 2: 2. 释放焦点 隐藏悬浮窗 (桌面主程序 Self-call) ---
    y2_center = 0.58
    box2_w = 0.18
    box2_h = 0.12
    box2_x = x_mid + 0.01
    box2_y = y2_center - box2_h/2.0
    
    # Orange Box
    box2 = patches.FancyBboxPatch(
        (box2_x, box2_y), box2_w, box2_h,
        boxstyle="round,pad=0.005",
        fc="#fff3e0", ec="#fb8c00", lw=3,
        zorder=3
    )
    ax.add_patch(box2)
    ax.text(
        box2_x + box2_w/2.0, y2_center, "2. 释放焦点\n隐藏悬浮窗",
        ha='center', va='center', fontsize=font_box_size, fontweight='bold', color="#e65100",
        multialignment='center', zorder=4
    )
    
    # Self-call dotted curve (arc) from lifeline to box top/bottom
    ax.annotate(
        "", xy=(box2_x, y2_center - 0.04), xytext=(box2_x, y2_center + 0.04),
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=1.3", color="#fb8c00", lw=3.5, ls="--", mutation_scale=15),
        zorder=2
    )
    
    # --- 5. Step 3: 3. 误触屏幕 / 系统权限弹窗干扰 (老年用户 -> 无障碍服务引擎) ---
    y3 = 0.43
    # Arrow
    ax.annotate(
        "", xy=(x_right, y3), xytext=(x_left, y3),
        arrowprops=dict(arrowstyle="-|>", color="#d32f2f", lw=4, mutation_scale=25),
        zorder=2
    )
    # Text
    ax.text(
        (x_left + x_right)/2.0, y3 + 0.015, "3.  误触屏幕  /  系统权限弹窗干扰",
        ha='center', va='bottom', fontsize=font_step_size, fontweight='bold', color="#d32f2f"
    )
    
    # --- 6. Step 4: 4. 状态机停滞 > 5秒触发死锁 (无障碍服务引擎 Self-call) ---
    y4_center = 0.28
    box4_w = 0.17
    box4_h = 0.12
    box4_x = x_right + 0.01
    box4_y = y4_center - box4_h/2.0
    
    # Red Box
    box4 = patches.FancyBboxPatch(
        (box4_x, box4_y), box4_w, box4_h,
        boxstyle="round,pad=0.005",
        fc="#ffebee", ec="#c62828", lw=3,
        zorder=3
    )
    ax.add_patch(box4)
    ax.text(
        box4_x + box4_w/2.0, y4_center, "4. 状态机停滞\n> 5秒触发死锁",
        ha='center', va='center', fontsize=font_box_size, fontweight='bold', color="#b71c1c",
        multialignment='center', zorder=4
    )
    
    # Self-call dotted curve
    ax.annotate(
        "", xy=(box4_x, y4_center - 0.04), xytext=(box4_x, y4_center + 0.04),
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=1.3", color="#c62828", lw=3.5, ls="--", mutation_scale=15),
        zorder=2
    )
    
    # --- 7. Step 5: 5. 强制模拟返回键重置（自回归） (无障碍服务引擎 -> 桌面主程序) ---
    y5 = 0.13
    # Arrow
    ax.annotate(
        "", xy=(x_mid, y5), xytext=(x_right, y5),
        arrowprops=dict(arrowstyle="-|>", color="#1976d2", lw=4, mutation_scale=25),
        zorder=2
    )
    # Text
    ax.text(
        (x_mid + x_right)/2.0, y5 + 0.015, "5.  强制模拟返回键重置（自回归）",
        ha='center', va='bottom', fontsize=font_box_size, fontweight='bold', color="#1976d2"
    )
    
    output_path = os.path.join(out_dir, 'fig2_4_focus_retreat.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print("Successfully generated focus retreat sequence diagram with 1.2x scale fonts!")

if __name__ == '__main__':
    draw_focus_retreat()
