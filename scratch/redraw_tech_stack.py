import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_tech_stack():
    # Expand canvas to 15.0 inches width to provide ample horizontal spacing for long texts
    fig, ax = plt.subplots(figsize=(15.0, 5.0), dpi=300)
    ax.set_xlim(0, 15.0)
    ax.set_ylim(0, 5.0)
    ax.axis('off')
    
    # 6 Layers from top to bottom
    layers = [
        {
            "title": "UI 界面层",
            "details": "Jetpack Compose 1.5  |  Material Design 3  |  Compose Navigation",
            "fc": "#e6f2ff", "ec": "#1e88e5", "tc": "#0d47a1"
        },
        {
            "title": "业务逻辑层",
            "details": "ViewModel + StateFlow  |  Kotlin Coroutines  |  七阶段状态机  |  插件管理器",
            "fc": "#f3e5f5", "ec": "#8e24aa", "tc": "#4a148c"
        },
        {
            "title": "数据持久化层",
            "details": "Room 2.6 (SQLite)  |  DataStore Preferences",
            "fc": "#e8f5e9", "ec": "#43a047", "tc": "#1b5e20"
        },
        {
            "title": "网络/注入层",
            "details": "Retrofit 2 + OkHttp  |  Dagger-Hilt 2.56  |  Coil图片加载",
            "fc": "#fff8e1", "ec": "#ffb300", "tc": "#e65100"
        },
        {
            "title": "系统能力层",
            "details": "Android Accessibility Service  |  TTS引擎  |  ConnectivityManager  |  PackageManager",
            "fc": "#ffebee", "ec": "#e53935", "tc": "#b71c1c"
        },
        {
            "title": "Android系统",
            "details": "Android 7.0 (API 24) ~ Android 14 (API 35)  |  Kotlin 2.0.21  |  Gradle 8.6",
            "fc": "#eceff1", "ec": "#546e7a", "tc": "#263238"
        }
    ]
    
    # 1. Draw background vertical integration dashed line (perfectly aligned with 1/3 point of details area)
    ax.plot([6.2, 6.2], [0.1, 4.9], color="#b0bec5", lw=2.5, ls="--", zorder=1)
    
    # 2. Coordinates configuration
    y_positions = [3.95, 3.20, 2.45, 1.70, 0.95, 0.20]
    box_height = 0.65
    
    font_title_size = 23
    font_details_size = 17.5
    
    # 3. Render boxes and texts
    for idx, layer in enumerate(layers):
        y = y_positions[idx]
        
        # FancyBboxPatch for modern rounded corner blocks spanning from 0.2 to 14.8
        box = FancyBboxPatch(
            (0.2, y), 14.6, box_height,
            boxstyle="round,pad=0.02",
            fc=layer["fc"], ec=layer["ec"], lw=2.5,
            zorder=2
        )
        ax.add_patch(box)
        
        # Vertical divider within the box at x=2.5
        ax.plot([2.5, 2.5], [y + 0.03, y + box_height - 0.03], color=layer["ec"], lw=2.0, ls="-", zorder=3)
        
        # Layer Title (bold, centered in left column)
        ax.text(
            1.35, y + box_height / 2.0, layer["title"],
            ha='center', va='center', fontsize=font_title_size, fontweight='bold', color=layer["tc"],
            zorder=4
        )
        
        # Layer Details (bold, left-aligned in right column with safe margins)
        ax.text(
            2.75, y + box_height / 2.0, layer["details"],
            ha='left', va='center', fontsize=font_details_size, fontweight='bold', color="#2c3e50",
            zorder=4
        )
        
    plt.tight_layout()
    output_path = os.path.join(out_dir, 'tech_stack.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print("Successfully generated Tech Stack diagram with optimized massive 2x fonts!")

if __name__ == '__main__':
    draw_tech_stack()
