import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_tech_stack():
    # Expand canvas to 15.0 inches width to provide ample horizontal spacing for long texts
    fig, ax = plt.subplots(figsize=(16.0, 7.5), dpi=300)
    ax.set_xlim(0, 16.0)
    ax.set_ylim(0, 7.5)
    ax.axis('off')
    
    # 6 Layers from top to bottom
    layers = [
        {
            "title": "UI 界面层",
            "details": "Jetpack Compose 1.5  |  Material Design 3\nCompose Navigation",
            "fc": "#e6f2ff", "ec": "#1e88e5", "tc": "#0d47a1"
        },
        {
            "title": "业务逻辑层",
            "details": "ViewModel + StateFlow  |  Kotlin Coroutines\n七阶段状态机  |  插件管理器",
            "fc": "#f3e5f5", "ec": "#8e24aa", "tc": "#4a148c"
        },
        {
            "title": "数据持久化层",
            "details": "Room 2.6 (SQLite)  |  DataStore Preferences",
            "fc": "#e8f5e9", "ec": "#43a047", "tc": "#1b5e20"
        },
        {
            "title": "网络/注入层",
            "details": "Retrofit 2 + OkHttp  |  Dagger-Hilt 2.56\nCoil图片加载",
            "fc": "#fff8e1", "ec": "#ffb300", "tc": "#e65100"
        },
        {
            "title": "系统能力层",
            "details": "Android Accessibility Service  |  TTS引擎\nConnectivityManager  |  PackageManager",
            "fc": "#ffebee", "ec": "#e53935", "tc": "#b71c1c"
        },
        {
            "title": "Android系统",
            "details": "Android 7.0 (API 24) ~ Android 16 (API 36)\nKotlin 2.0.21  |  Gradle 8.6",
            "fc": "#eceff1", "ec": "#546e7a", "tc": "#263238"
        }
    ]
    
    # 1. Draw background vertical integration dashed line (perfectly aligned in details area)
    # Centered in the details area: 5.2 + (15.8 - 5.2)/2 = 10.5
    ax.plot([10.5, 10.5], [0.1, 7.4], color="#b0bec5", lw=2.5, ls="--", zorder=1)
    
    # 2. Coordinates configuration
    y_positions = [6.2, 5.0, 3.8, 2.6, 1.4, 0.2]
    box_height = 1.0
    
    # === 学术图表字体缩放数学模型 (方案一) ===
    # 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
    latex_scale = 0.95           # LaTeX 中的 width=0.95\textwidth 缩放因子
    latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
    canvas_width_inch = 16.0     # Matplotlib 画布宽度
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例
    
    X_pdf = 11.0                  # 左侧层级大标题：与正文一致的 12pt (小四)
    Y_pdf = 11.0                  # 右侧细节技术栈文字：11pt
    
    font_title_size = X_pdf / scale_factor
    font_details_size = Y_pdf / scale_factor
    
    # 3. Render boxes and texts
    for idx, layer in enumerate(layers):
        y = y_positions[idx]
        
        # FancyBboxPatch for modern rounded corner blocks spanning from 0.2 to 15.8
        box = FancyBboxPatch(
            (0.2, y), 15.6, box_height,
            boxstyle="round,pad=0.02",
            fc=layer["fc"], ec=layer["ec"], lw=2.5,
            zorder=2
        )
        ax.add_patch(box)
        
        # Vertical divider within the box at x=5.2 (widen left column to prevent text overflow)
        ax.plot([5.2, 5.2], [y + 0.03, y + box_height - 0.03], color=layer["ec"], lw=2.0, ls="-", zorder=3)
        
        # Layer Title (bold, centered in left column of width 5.0, centered at 2.7)
        ax.text(
            2.7, y + box_height / 2.0, layer["title"],
            ha='center', va='center', fontsize=font_title_size, fontweight='bold', color=layer["tc"],
            zorder=4
        )
        
        # Layer Details (bold, left-aligned in right column with safe margins starting at 5.5)
        ax.text(
            5.5, y + box_height / 2.0, layer["details"],
            ha='left', va='center', fontsize=font_details_size, color="#2c3e50",
            zorder=4
        )
        
    plt.tight_layout()
    output_path = os.path.join(out_dir, 'tech_stack_v2.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    # Also save as the original for latex integration
    plt.savefig(os.path.join(out_dir, 'tech_stack.png'), dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print("Successfully generated Tech Stack diagram with academic fonts and proper layout!")

if __name__ == '__main__':
    draw_tech_stack()
