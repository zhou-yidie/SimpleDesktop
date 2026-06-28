import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# out_dir：编译后图表保存的目标物理路径目录
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# plt.rcParams：配置全局中文字体为仿宋（FangSong），确保无乱码
plt.rcParams['font.sans-serif'] = ['FangSong', 'SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False 

def add_double_arrow(ax, xc, yc, height=0.36, arrow_span=0.18, stem_w=0.07, head_h=0.10, color="#70ad47"):
    """
    绘制完美的 10 顶点空心双向垂直箭头 (白底彩色描边，高保真还原学术格式)
    """
    half_h = height / 2.0
    vertices = [
        (xc, yc + half_h),                              # 1. 最顶端尖角点
        (xc - arrow_span/2.0, yc + half_h - head_h),     # 2. 上左翼角点
        (xc - stem_w/2.0, yc + half_h - head_h),         # 3. 上左竖杆转折点
        (xc - stem_w/2.0, yc - half_h + head_h),         # 4. 下左竖杆转折点
        (xc - arrow_span/2.0, yc - half_h + head_h),     # 5. 下左翼角点
        (xc, yc - half_h),                              # 6. 最底端尖角点
        (xc + arrow_span/2.0, yc - half_h + head_h),     # 7. 下右翼角点
        (xc + stem_w/2.0, yc - half_h + head_h),         # 8. 下右竖杆转折点
        (xc + stem_w/2.0, yc + half_h - head_h),         # 9. 上右竖杆转折点
        (xc + arrow_span/2.0, yc + half_h - head_h)      # 10. 上右翼角点
    ]
    poly = patches.Polygon(vertices, closed=True, fc="#ffffff", ec=color, lw=1.8, zorder=3)
    ax.add_patch(poly)

def draw_clean_architecture():
    # 画布大小 (进一步横向拓宽至 13.6，提供更宽广的物理空间)
    fig, ax = plt.subplots(figsize=(13.6, 7.8), dpi=300)
    ax.axis('off')
    
    # 限制 x, y 坐标，并设置等比例缩放，确保圆角绝不拉伸变形
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.8)
    ax.set_aspect('equal')
    
    # 根据用户要求，主字号统一提升为学术规范的 17.0，英文微调为 13.0
    title_zh_size = 17.0
    title_en_size = 13.0
    comp_size = 17.0
    
    # -------------------------------------------------------------
    # 1. 插件层 (Plugin Layer) - 绿色
    # -------------------------------------------------------------
    # 大容器圆角框 (宽度从 12.2 进一步拓宽至 12.8)
    ax.add_patch(patches.FancyBboxPatch(
        (0.4, 5.4), 12.8, 2.0, boxstyle="round,pad=0.0,rounding_size=0.15",
        fc="#e2f0d9", ec="#70ad47", lw=2.5, zorder=1
    ))
    # 垂直分割线
    ax.plot([2.1, 2.1], [5.4, 7.4], color="#70ad47", lw=1.5, zorder=2)
    
    # 左侧层级大字标题
    ax.text(
        1.25, 6.55, "插件层", ha='center', va='center',
        fontsize=title_zh_size, fontweight='bold', color="#375623"
    )
    ax.text(
        1.25, 6.15, "PLUGIN LAYER", ha='center', va='center',
        fontsize=title_en_size, fontweight='bold', color="#375623", fontname="sans-serif"
    )
    
    # 右侧 3 个小组件圆角白底框 (白框宽度大幅拓宽至 3.0，完全容纳文字，中点分别重定位在 4.0, 7.85, 11.7)
    plugin_items = [
        {"x": 4.0, "text": "联系人插件\n(Contact Plugin)"},
        {"x": 7.85, "text": "应用插件\n(App Plugin)"},
        {"x": 11.7, "text": "天气插件\n(Weather Plugin)"}
    ]
    for item in plugin_items:
        ax.add_patch(patches.FancyBboxPatch(
            (item["x"] - 1.5, 5.7), 3.0, 1.4, boxstyle="round,pad=0.0,rounding_size=0.1",
            fc="#ffffff", ec="#70ad47", lw=1.5, zorder=2
        ))
        ax.text(
            item["x"], 6.4, item["text"], ha='center', va='center',
            fontsize=comp_size, color="#000000", linespacing=1.4
        )
        
    # -------------------------------------------------------------
    # 2. 总线层 (Bus Layer) - 橙色
    # -------------------------------------------------------------
    # 大容器圆角框 (宽度从 12.2 进一步拓宽至 12.8)
    ax.add_patch(patches.FancyBboxPatch(
        (0.4, 2.9), 12.8, 2.0, boxstyle="round,pad=0.0,rounding_size=0.15",
        fc="#fce4d6", ec="#ed7d31", lw=2.5, zorder=1
    ))
    # 垂直分割线
    ax.plot([2.1, 2.1], [2.9, 4.9], color="#ed7d31", lw=1.5, zorder=2)
    
    ax.text(
        1.25, 4.05, "总线层", ha='center', va='center',
        fontsize=title_zh_size, fontweight='bold', color="#843c0c"
    )
    ax.text(
        1.25, 3.65, "BUS LAYER", ha='center', va='center',
        fontsize=title_en_size, fontweight='bold', color="#843c0c", fontname="sans-serif"
    )
    
    # 右侧 4 个小组件圆角白底框 (白框宽度自 2.25 进一步拓宽至 2.5，中点重定位在 3.8, 6.5, 9.2, 11.9)
    bus_items = [
        {"x": 3.8, "text": "插件管理器\n(Plugin Manager)"},
        {"x": 6.5, "text": "消息总线\n(Message Bus)"},
        {"x": 9.2, "text": "配置存储\n(Config Store)"},
        {"x": 11.9, "text": "事件分发\n(Event Dispatcher)"}
    ]
    for item in bus_items:
        ax.add_patch(patches.FancyBboxPatch(
            (item["x"] - 1.25, 3.2), 2.5, 1.4, boxstyle="round,pad=0.0,rounding_size=0.1",
            fc="#ffffff", ec="#ed7d31", lw=1.5, zorder=2
        ))
        ax.text(
            item["x"], 3.9, item["text"], ha='center', va='center',
            fontsize=comp_size - 1.5, color="#000000", linespacing=1.4
        )
        
    # 绘制组件间的右向数据流单向箭头 (Gap定位在白框左右间，sx=5.05->ex=5.25，以此类推)
    gaps = [(5.05, 5.25), (7.75, 7.95), (10.45, 10.65)]
    for sx, ex in gaps:
        ax.annotate(
            "", xy=(ex, 3.9), xytext=(sx, 3.9),
            arrowprops=dict(arrowstyle="-|>", color="#ed7d31", lw=2.2, mutation_scale=14),
            zorder=3
        )
        
    # -------------------------------------------------------------
    # 3. 宿主层 (Host Layer) - 蓝色
    # -------------------------------------------------------------
    # 大容器圆角框 (宽度从 12.2 进一步拓宽至 12.8)
    ax.add_patch(patches.FancyBboxPatch(
        (0.4, 0.4), 12.8, 2.0, boxstyle="round,pad=0.0,rounding_size=0.15",
        fc="#d9e1f2", ec="#4472c4", lw=2.5, zorder=1
    ))
    # 垂直分割线
    ax.plot([2.1, 2.1], [0.4, 2.4], color="#4472c4", lw=1.5, zorder=2)
    
    ax.text(
        1.25, 1.55, "宿主层", ha='center', va='center',
        fontsize=title_zh_size, fontweight='bold', color="#1f3864"
    )
    ax.text(
        1.25, 1.15, "HOST LAYER", ha='center', va='center',
        fontsize=title_en_size, fontweight='bold', color="#1f3864", fontname="sans-serif"
    )
    
    # 右侧 3 个小组件圆角白底框 (白框宽度大幅拓宽至 3.0，完全包容文字，中点定位在 4.0, 7.85, 11.7)
    host_items = [
        {"x": 4.0, "text": "应用入口\n(Application Entry)"},
        {"x": 7.85, "text": "主界面容器\n(Main UI Container)"},
        {"x": 11.7, "text": "依赖注入容器\n(DI Container)"}
    ]
    for item in host_items:
        ax.add_patch(patches.FancyBboxPatch(
            (item["x"] - 1.5, 0.7), 3.0, 1.4, boxstyle="round,pad=0.0,rounding_size=0.1",
            fc="#ffffff", ec="#4472c4", lw=1.5, zorder=2
        ))
        ax.text(
            item["x"], 1.4, item["text"], ha='center', va='center',
            fontsize=comp_size, color="#000000", linespacing=1.4
        )
        
    # -------------------------------------------------------------
    # 4. 跨层双向垂直空心箭头绘制 (x 坐标重定位对齐中点 4.0, 7.85, 11.7)
    # -------------------------------------------------------------
    v_xs = [4.0, 7.85, 11.7]
    
    # 插件层与总线层之间 (绿色)
    for vx in v_xs:
        add_double_arrow(ax, xc=vx, yc=5.15, color="#70ad47")
        
    # 总线层与宿主层之间 (蓝色)
    for vx in v_xs:
        add_double_arrow(ax, xc=vx, yc=2.65, color="#4472c4")
        
    save_path = os.path.join(out_dir, "architecture.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print(f"Generated clean system architecture diagram to {save_path}!")

if __name__ == "__main__":
    draw_clean_architecture()
