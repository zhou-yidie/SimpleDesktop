import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_pill(ax, x, y, w, h, text, style):
    # Style definitions
    styles = {
        "green":  {"fc": "#e8f5e9", "ec": "#43a047", "tc": "#1b5e20"},
        "yellow": {"fc": "#fff8e1", "ec": "#ffb300", "tc": "#e65100"},
        "blue":   {"fc": "#e6f2ff", "ec": "#1e88e5", "tc": "#0d47a1"},
        "device": {"fc": "#f8f9fa", "ec": "#cfd8dc", "tc": "#37474f"},
        "header": {"fc": "#eceff1", "ec": "#78909c", "tc": "#263238"}
    }
    s = styles[style]
    
    # Draw rounded pill box
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.01",
        fc=s["fc"], ec=s["ec"], lw=1.5,
        zorder=3
    )
    ax.add_patch(box)
    
    # Draw centered text
    ax.text(
        x + w / 2.0, y + h / 2.0, text,
        ha='center', va='center', fontsize=12, fontweight='bold', color=s["tc"],
        zorder=4
    )

def draw_compatibility():
    fig, ax = plt.subplots(figsize=(11.65, 6.2), dpi=300)
    ax.set_xlim(0, 11.65)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    
    # 1. Background board
    board = FancyBboxPatch(
        (0.1, 0.1), 11.45, 6.0,
        boxstyle="round,pad=0.02",
        fc="#ffffff", ec="#e0e0e0", lw=2,
        zorder=1
    )
    ax.add_patch(board)
    
    # 2. Draw Column Headers at Y=5.3
    headers = [
        ("测试设备与平台", 0.4, 2.8),
        ("显示布局自适应", 3.4, 1.9),
        ("无障碍一键拨号", 5.5, 1.9),
        ("网络守护与自愈", 7.6, 1.9),
        ("后台常驻与自启", 9.7, 1.9)
    ]
    for text, x, w in headers:
        draw_pill(ax, x, 5.3, w, 0.5, text, "header")
        
    # 3. Row data
    rows = [
        {
            "device": "一加 13 (Android 16)",
            "cells": [("完美适配", "green"), ("强化引导", "yellow"), ("辅助自愈", "blue"), ("引导授权", "yellow")]
        },
        {
            "device": "荣耀 WinRT (Android 15)",
            "cells": [("完美适配", "green"), ("完美适配", "green"), ("辅助自愈", "blue"), ("引导授权", "yellow")]
        },
        {
            "device": "华为 Pura 80 Pro (HOS NEXT)",
            "cells": [("完美适配", "green"), ("强化引导", "yellow"), ("辅助自愈", "blue"), ("引导授权", "yellow")]
        },
        {
            "device": "一加 Ace (Android 12)",
            "cells": [("完美适配", "green"), ("完美适配", "green"), ("辅助自愈", "blue"), ("引导授权", "yellow")]
        },
        {
            "device": "荣耀 70 (Android 12)",
            "cells": [("完美适配", "green"), ("完美适配", "green"), ("辅助自愈", "blue"), ("引导授权", "yellow")]
        },
        {
            "device": "iQOO 8 (Android 11)",
            "cells": [("完美适配", "green"), ("完美适配", "green"), ("辅助自愈", "blue"), ("完美适配", "green")]
        },
        {
            "device": "小米 8 青春版 (Android 9)",
            "cells": [("完美适配", "green"), ("完美适配", "green"), ("接口自愈", "blue"), ("完美适配", "green")]
        }
    ]
    
    y_positions = [4.5, 3.8, 3.1, 2.4, 1.7, 1.0, 0.3]
    
    for idx, row in enumerate(rows):
        y = y_positions[idx]
        
        # Draw device column cell
        draw_pill(ax, 0.4, y, 2.8, 0.5, row["device"], "device")
        
        # Draw other cells
        col_xs = [3.4, 5.5, 7.6, 9.7]
        for cell_idx, (cell_text, style) in enumerate(row["cells"]):
            draw_pill(ax, col_xs[cell_idx], y, 1.9, 0.5, cell_text, style)
            
    plt.tight_layout()
    output_path = os.path.join(out_dir, 'compatibility_matrix.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print("Successfully generated Compatibility Matrix scorecard!")

if __name__ == '__main__':
    draw_compatibility()
