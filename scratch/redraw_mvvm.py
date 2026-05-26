import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

# Set up Chinese font support
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# Create figure - slightly taller canvas (11.5x9.0) to give titles complete vertical breathing room
fig, ax = plt.subplots(figsize=(11.5, 9.0), dpi=300)
ax.set_xlim(-1.0, 12.6)
ax.set_ylim(-0.2, 10.6)
ax.axis('off')

# Font size settings optimised for high-readability matching standard body text size
font_title_size = 28
font_box_size = 25
font_arrow_size = 21

col_width = 3.2
col_height = 9.8
col_y = 0.4

box_width = 2.8

# 1. Column Backgrounds (View, ViewModel, Model)
# Column 1: View Layer
rect_col1 = FancyBboxPatch((0.2, col_y), col_width, col_height, boxstyle="round,pad=0.03",
                            ec="#0288d1", fc="#e1f5fe", lw=3.0)
ax.add_patch(rect_col1)
# Move titles up to y=9.4 to guarantee no overlap with the highest boxes
ax.text(1.8, 9.4, "View Layer\n视图层", fontsize=font_title_size, fontweight='bold',
        ha='center', va='center', color='#01579b', linespacing=1.2)

# Column 2: ViewModel Layer
rect_col2 = FancyBboxPatch((4.5, col_y), col_width, col_height, boxstyle="round,pad=0.03",
                            ec="#f57c00", fc="#fff3e0", lw=3.0)
ax.add_patch(rect_col2)
ax.text(6.1, 9.4, "ViewModel Layer\n视图模型层", fontsize=font_title_size - 1, fontweight='bold',
        ha='center', va='center', color='#e65100', linespacing=1.2)

# Column 3: Model Layer
rect_col3 = FancyBboxPatch((8.8, col_y), col_width, col_height, boxstyle="round,pad=0.03",
                            ec="#388e3c", fc="#e8f5e9", lw=3.0)
ax.add_patch(rect_col3)
ax.text(10.4, 9.4, "Model / Repository\n模型与数据层", fontsize=font_title_size - 2, fontweight='bold',
        ha='center', va='center', color='#1b5e20', linespacing=1.2)


# 2. Add Inner Boxes (perfectly aligned with wider dimensions)
def add_inner_box(x, y, h, text):
    box = FancyBboxPatch((x, y), box_width, h, boxstyle="round,pad=0.05",
                          ec="#757575", fc="#ffffff", lw=2.0)
    ax.add_patch(box)
    ax.text(x + box_width/2, y + h/2, text, fontsize=font_box_size,
            ha='center', va='center', color='#212121', fontweight='bold', linespacing=1.2)

# Column 1 Boxes (with larger heights and perfect vertical symmetry)
add_inner_box(0.4, 7.0, 1.5, "Jetpack\nCompose\n界面组件")
add_inner_box(0.4, 4.05, 1.4, "用户输入事件\nUser Events")
add_inner_box(0.4, 1.0, 1.5, "界面状态渲染\nUI State\nRendering")

# Column 2 Boxes
add_inner_box(4.7, 7.25, 1.15, "ViewModel")
add_inner_box(4.7, 5.25, 1.15, "StateFlow /\nLiveData")
add_inner_box(4.7, 3.25, 1.15, "业务逻辑处理")
add_inner_box(4.7, 1.25, 1.15, "状态管理")

# Column 3 Boxes
add_inner_box(9.0, 7.25, 1.15, "Repository\n数据仓库")
add_inner_box(9.0, 5.25, 1.15, "Room\n数据库")
add_inner_box(9.0, 3.25, 1.15, "DataStore\n偏好存储")
add_inner_box(9.0, 1.25, 1.15, "Retrofit\n网络请求")


# 3. Add Intermediate Connectors (Arrows between Col 1 and Col 2)
# User Actions Downward Arrow
ax.annotate("", xy=(3.95, 4.6), xytext=(3.95, 7.9),
            arrowprops=dict(facecolor='#0288d1', edgecolor='#01579b', width=14, headwidth=28, shrink=0.05))
ax.text(3.95, 6.25, "用户操作事件\nUser Actions", fontsize=font_arrow_size, fontweight='bold',
        ha='center', va='center', color='#01579b', rotation=270, linespacing=1.2)

# UI State Upward Arrow
ax.annotate("", xy=(3.95, 4.2), xytext=(3.95, 0.9),
            arrowprops=dict(facecolor='#e53935', edgecolor='#b71c1c', width=14, headwidth=28, shrink=0.05))
ax.text(3.95, 2.55, "UI 状态更新\nUI State", fontsize=font_arrow_size, fontweight='bold',
        ha='center', va='center', color='#b71c1c', rotation=90, linespacing=1.2)


# 4. Add Intermediate Connectors (Arrows between Col 2 and Col 3)
# Data Request Downward Arrow
ax.annotate("", xy=(8.25, 4.6), xytext=(8.25, 7.9),
            arrowprops=dict(facecolor='#43a047', edgecolor='#1b5e20', width=14, headwidth=28, shrink=0.05))
ax.text(8.25, 6.25, "数据请求\nData Request", fontsize=font_arrow_size, fontweight='bold',
        ha='center', va='center', color='#1b5e20', rotation=270, linespacing=1.2)

# Flow/LiveData Upward Arrow
ax.annotate("", xy=(8.25, 4.2), xytext=(8.25, 0.9),
            arrowprops=dict(facecolor='#fb8c00', edgecolor='#e65100', width=14, headwidth=28, shrink=0.05))
ax.text(8.25, 2.55, "Flow / LiveData\n数据流", fontsize=font_arrow_size, fontweight='bold',
        ha='center', va='center', color='#e65100', rotation=90, linespacing=1.2)


# 5. Add Left Unidirectional Data Flow Curved Arrow
style = "Simple, tail_width=14, head_width=28, head_length=22"
kw = dict(arrowstyle=style, color="#546e7a", ec="#37474f", shrinkA=5, shrinkB=5)
arrow = patches.FancyArrowPatch((0.0, 1.6), (0.0, 7.9), connectionstyle="arc3,rad=-0.38", **kw)
ax.add_patch(arrow)

# Label shifted slightly left to x=-0.55 to match the new xlim perfectly
ax.text(-0.55, 4.75, "单向数据流\nUnidirectional Data Flow", fontsize=font_arrow_size + 1, fontweight='bold',
        ha='center', va='center', color='#37474f', rotation=90, linespacing=1.2)


# Tight layout and save over original
plt.tight_layout()
output_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\mvvm.png"
plt.savefig(output_path, bbox_inches='tight', transparent=True)
plt.close()
print("Successfully generated beautifully optimized high-readability MVVM diagram!")
