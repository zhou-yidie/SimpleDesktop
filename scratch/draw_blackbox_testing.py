import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# out_dir：编译后图表保存的目标物理路径目录
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# plt.rcParams：配置全局中文字体为仿宋（FangSong），确保与前面图表的学术风格高度一致
plt.rcParams['font.sans-serif'] = ['FangSong', 'SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False 

def draw_blackbox():
    # 画布高为 7.0 英寸，宽为 16.0 英寸
    fig, ax = plt.subplots(figsize=(16.0, 7.0), dpi=300)
    ax.axis('off')
    
    ax.set_xlim(0.5, 15.5)
    ax.set_ylim(0.2, 5.8)
    ax.set_aspect('equal')
    
    # 统一将正文字号设为非常清晰醒目的 20.0pt，重要标题设为 22.0pt
    font_size = 20.0
    title_font_size = 22.0
    
    # =============================================================
    # 1. 绘制核心框体 (圆角矩形和虚线矩形)
    # =============================================================
    
    # 1.1 中间：被测系统 (黑盒) (虚线框，中点 X=8.0, Y=3.6, 宽 4.8, 高 3.6)
    # x: 5.6 -> 10.4, y: 1.8 -> 5.4
    ax.add_patch(patches.Rectangle(
        (5.6, 1.8), 4.8, 3.6,
        fc="#f5f5f5", ec="#7f7f7f", lw=2.5, linestyle="--", zorder=2
    ))
    ax.text(8.0, 5.0, "被测系统 (黑盒)", ha='center', va='center', fontsize=title_font_size, fontweight='bold', color="#000000")
    ax.text(8.0, 3.5, "SimpleDesktop\n适老化桌面系统\n(内部代码逻辑不可见)", ha='center', va='center', fontsize=font_size, color="#333333", linespacing=1.3)

    # 1.2 左侧：测试输入条件 (淡绿色圆角矩形，中点 X=2.3, Y=3.6, 宽 3.0, 高 1.2)
    # x: 0.8 -> 3.8
    ax.add_patch(patches.FancyBboxPatch(
        (0.8, 3.0), 3.0, 1.2, boxstyle="round,pad=0.0,rounding_size=0.04",
        fc="#e8f5e9", ec="#2e7d32", lw=2.5, zorder=2
    ))
    ax.text(2.3, 3.6, "测试输入条件", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#1b5e20")
    
    # 输入条件上面的具体说明文本 (Y=5.2)
    ax.text(2.3, 5.2, "语音点击指令\n界面触控操作\n模拟断网事件", ha='center', va='center', fontsize=font_size, color="#333333", linespacing=1.3)

    # 1.3 右侧上部：实际系统输出 (淡橙色圆角矩形，中点 X=13.7, Y=3.6, 宽 3.0, 高 1.2)
    # x: 12.2 -> 15.2
    ax.add_patch(patches.FancyBboxPatch(
        (12.2, 3.0), 3.0, 1.2, boxstyle="round,pad=0.0,rounding_size=0.04",
        fc="#fff3e0", ec="#ef6c00", lw=2.5, zorder=2
    ))
    ax.text(13.7, 3.6, "实际系统输出", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#e65100")
    
    # 系统输出上面的具体说明文本 (Y=5.2)
    ax.text(13.7, 5.2, "拉起微信视频\n跳转联系人面板\n弹窗并语音报警", ha='center', va='center', fontsize=font_size, color="#333333", linespacing=1.3)

    # 1.4 右侧下部：预期规范与需求 (淡红色圆角矩形，中点 X=13.7, Y=1.0, 宽 3.0, 高 1.2)
    # x: 12.2 -> 15.2
    ax.add_patch(patches.FancyBboxPatch(
        (12.2, 0.4), 3.0, 1.2, boxstyle="round,pad=0.0,rounding_size=0.04",
        fc="#ffebee", ec="#c62828", lw=2.5, zorder=2
    ))
    ax.text(13.7, 1.0, "预期规范与需求", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#b71c1c")

    # =============================================================
    # 2. 绘制连接箭头和文字
    # =============================================================
    arrow_green = dict(arrowstyle="-|>", color="#2e7d32", lw=3.5, mutation_scale=20)
    arrow_orange = dict(arrowstyle="-|>", color="#ef6c00", lw=3.5, mutation_scale=20)
    arrow_red_dashed = dict(arrowstyle="-|>", color="#c62828", ls="--", lw=2.5, mutation_scale=15)

    # 2.1 激励箭头 (从输入框边缘 3.8 指向黑盒左侧 5.6，预留 0.02)
    ax.annotate("", xy=(5.58, 3.6), xytext=(3.8, 3.6), arrowprops=arrow_green, zorder=3)
    ax.text(4.7, 3.9, "激励", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#1b5e20")

    # 2.2 响应箭头 (从黑盒右侧 10.4 指向输出框边缘 12.2，预留 0.02)
    ax.annotate("", xy=(12.18, 3.6), xytext=(10.4, 3.6), arrowprops=arrow_orange, zorder=3)
    ax.text(11.3, 3.9, "响应", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#e65100")

    # 2.3 一致性比对验证箭头 (从输出框底部 3.0 指向预期框顶部 1.6，预留 0.02)
    ax.annotate("", xy=(13.7, 1.62), xytext=(13.7, 3.0), arrowprops=arrow_red_dashed, zorder=3)
    ax.text(13.9, 2.3, "一致性比对验证", ha='left', va='center', fontsize=font_size, color="#c62828")

    # 保存图片
    save_path = os.path.join(out_dir, "fig4_1_blackbox_testing.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print(f"Successfully generated clean academic fig4_1_blackbox_testing.png to {save_path}!")

if __name__ == "__main__":
    draw_blackbox()
