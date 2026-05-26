import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# 将输出目标直接配置为新版 LaTeX 论文目录
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

def draw_room_er():
    # 字体放大150% (变为原先的2.5倍)，将 figsize 从 (10, 5) 扩充至 (18, 9)
    fig, ax = plt.subplots(figsize=(18, 9))
    ax.axis('off')
    
    # Entities (适当微调宽度与高度以完美容纳大字号)
    ax.add_patch(patches.Rectangle((0.08, 0.4), 0.28, 0.18, fc="#e6f2ff", ec="#0066cc", lw=3.5, zorder=2))
    ax.text(0.22, 0.49, "ContactEntity\n(联系人)", ha='center', va='center', fontsize=26, fontweight='bold', zorder=3)
    
    ax.add_patch(patches.Rectangle((0.64, 0.4), 0.28, 0.18, fc="#e6f2ff", ec="#0066cc", lw=3.5, zorder=2))
    ax.text(0.78, 0.49, "AppEntity\n(应用)", ha='center', va='center', fontsize=26, fontweight='bold', zorder=3)
    
    # Relationship
    diamond = patches.Polygon([(0.5, 0.58), (0.60, 0.49), (0.5, 0.4), (0.40, 0.49)], fc="#e6ffe6", ec="#009900", lw=3.5, zorder=2)
    ax.add_patch(diamond)
    ax.text(0.5, 0.49, "持久化仓库\n(Repository)", ha='center', va='center', fontsize=22, fontweight='bold', zorder=3)
    
    # Connect Entity to Relationship
    ax.plot([0.36, 0.40], [0.49, 0.49], color="black", lw=3.0, zorder=1)
    ax.text(0.38, 0.52, "1:N", ha='center', fontsize=20, fontweight='bold')
    ax.plot([0.60, 0.64], [0.49, 0.49], color="black", lw=3.0, zorder=1)
    ax.text(0.62, 0.52, "1:N", ha='center', fontsize=20, fontweight='bold')
    
    # Attributes for Contact
    # 左侧属性限制在 x=-0.06, 0.16, 0.38，与右侧属性分開足够距离
    attrs_contact = [
        ("id (主键)", (0.1, 0.76), True),
        ("name (姓名)", (-0.06, 0.13), False),
        ("phone (电话)", (0.16, 0.13), False),
        ("wechat (微信)", (0.38, 0.13), False)
    ]
    for text, (x, y), is_primary in attrs_contact:
        ax.add_patch(patches.Ellipse((x, y), 0.22, 0.10, fc="#f2f2f2", ec="gray", lw=2.5, zorder=2))
        fontweight = 'bold' if is_primary else 'normal'
        ax.text(x, y, text, ha='center', va='center', fontsize=22, fontweight=fontweight, zorder=3)
        ax.plot([0.22, x], [0.4, y] if y < 0.4 else [0.58, y], color="black", lw=2.0, zorder=1)
        
    # Attributes for App
    # 右侧属性从 x=0.62 开始，主键 x=0.79，最右 x=0.97
    attrs_app = [
        ("packageName (主键)", (0.79, 0.76), True),
        ("label (应用名)", (0.63, 0.13), False),
        ("enabled (状态)", (0.97, 0.13), False)
    ]
    for text, (x, y), is_primary in attrs_app:
        # 主键椭圆宽度 0.35，普通属性 0.22，高度 0.10
        width_ellipse = 0.35 if is_primary else 0.22
        ax.add_patch(patches.Ellipse((x, y), width_ellipse, 0.10, fc="#f2f2f2", ec="gray", lw=2.5, zorder=2))
        fontweight = 'bold' if is_primary else 'normal'
        ax.text(x, y, text, ha='center', va='center', fontsize=22, fontweight=fontweight, zorder=3)
        ax.plot([0.78, x], [0.4, y] if y < 0.4 else [0.58, y], color="black", lw=2.0, zorder=1)
        
    plt.savefig(os.path.join(out_dir, 'fig2_1_room_er.png'), dpi=300, bbox_inches='tight')
    plt.close()

def draw_hilt_di():
    # 字体放大150% (变为原先的2.5倍)，将 figsize 从 (10, 6) 扩充至 (18, 11)
    fig, ax = plt.subplots(figsize=(18, 11))
    ax.axis('off')
    
    # Hilt Container
    ax.add_patch(patches.Rectangle((0.03, 0.23), 0.94, 0.72, fc="#f9f9f9", ec="#aaaaaa", ls="--", lw=3.5, zorder=1))
    ax.text(0.5, 0.91, "Dagger-Hilt 依赖注入全局容器", ha='center', va='center', fontsize=32, fontweight='bold', color="#444444", zorder=2)
    
    # Modules (Providers)
    ax.add_patch(patches.FancyBboxPatch((0.12, 0.72), 0.32, 0.11, boxstyle="round,pad=0.02", fc="#e6ffe6", ec="#009900", lw=3.5, zorder=2))
    ax.text(0.28, 0.775, "@Module\nDatabaseModule (提供数据库实例)", ha='center', va='center', fontsize=24, fontweight='bold', zorder=3)
    
    ax.add_patch(patches.FancyBboxPatch((0.56, 0.72), 0.32, 0.11, boxstyle="round,pad=0.02", fc="#e6ffe6", ec="#009900", lw=3.5, zorder=2))
    ax.text(0.72, 0.775, "@Module\nDataStoreModule (提供偏好实例)", ha='center', va='center', fontsize=24, fontweight='bold', zorder=3)
    
    # Singleton Component
    ax.add_patch(patches.FancyBboxPatch((0.26, 0.42), 0.48, 0.13, boxstyle="round,pad=0.02", fc="#fff2e6", ec="#ff8000", lw=3.5, zorder=2))
    ax.text(0.5, 0.485, "@SingletonComponent\n(单例组件调度中心)", ha='center', va='center', fontsize=26, fontweight='bold', zorder=3)
    
    # Arrows from Modules to Component
    ax.annotate("", xy=(0.38, 0.56), xytext=(0.28, 0.72), arrowprops=dict(arrowstyle="->", lw=3.5, color="#0066cc"), zorder=2)
    ax.annotate("", xy=(0.62, 0.56), xytext=(0.72, 0.72), arrowprops=dict(arrowstyle="->", lw=3.5, color="#0066cc"), zorder=2)
    
    # Consumers
    ax.add_patch(patches.FancyBboxPatch((0.08, 0.05), 0.38, 0.13, boxstyle="round,pad=0.02", fc="#e6f2ff", ec="#0066cc", lw=3.5, zorder=2))
    ax.text(0.27, 0.115, "DesktopViewModel\n(@HiltViewModel 消费者)", ha='center', va='center', fontsize=24, fontweight='bold', zorder=3)
    
    ax.add_patch(patches.FancyBboxPatch((0.54, 0.05), 0.38, 0.13, boxstyle="round,pad=0.02", fc="#e6f2ff", ec="#0066cc", lw=3.5, zorder=2))
    ax.text(0.73, 0.115, "AccessibilityService\n(@AndroidEntryPoint 消费者)", ha='center', va='center', fontsize=24, fontweight='bold', zorder=3)
    
    # Arrows from Component to Consumers
    ax.annotate("", xy=(0.27, 0.19), xytext=(0.4, 0.42), arrowprops=dict(arrowstyle="->", lw=3.5, ls="dashed", color="#cc0000"), zorder=2)
    ax.text(0.26, 0.30, "@Inject\n自动注入", ha='center', va='center', fontsize=22, fontweight='bold', color="#cc0000", zorder=3)
    
    ax.annotate("", xy=(0.73, 0.19), xytext=(0.6, 0.42), arrowprops=dict(arrowstyle="->", lw=3.5, ls="dashed", color="#cc0000"), zorder=2)
    ax.text(0.74, 0.30, "@Inject\n自动注入", ha='center', va='center', fontsize=22, fontweight='bold', color="#cc0000", zorder=3)
    
    plt.savefig(os.path.join(out_dir, 'fig2_2_hilt_di.png'), dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    draw_room_er()
    draw_hilt_di()
    print("Room ER (图2.2) & Dagger-Hilt (图2.3) 大字号图片生成成功！")
