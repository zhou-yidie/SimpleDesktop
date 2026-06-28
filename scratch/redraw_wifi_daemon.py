import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# =========================================================================
# 🎓 流程图 2: WiFi网络守护与自愈机制流程 (WiFi Daemon)
# =========================================================================
# 本脚本生成图表保存的目标物理路径，执行后会生成 wifi_daemon.png 和 wifi_daemon.pdf
# =========================================================================

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# 配置全局中文字体，确保在 Windows 环境下能正常渲染中文
plt.rcParams['font.sans-serif'] = ['FangSong', 'SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# =========================================================================
# ⚙️ 核心几何与排版参数配置区 (您可以在这里修改数值来自定义图形大小和位置)
# =========================================================================
FONT_SIZE = 22.0       # 核心节点的主标题字号
FONT_SIZE_SUB = 18.0   # 核心节点的辅助/子标题字号
FONT_SIZE_LABEL = 20.0 # 线条上的判断标签字号

# 🔹 普通矩形方框尺寸（可在此增加宽度以容纳更长的文字）
BOX_WIDTH = 3.6        # 矩形方框的宽度（若文字溢出，可调大为 3.8 或 4.0）
BOX_HEIGHT = 1.6       # 矩形方框的高度

# 🔸 判定菱形尺寸
DIA_HALF_W = 2.0       # 菱形的半宽度（从中心到左/右顶点的距离，总宽为 2 * DIA_HALF_W）
DIA_HALF_H = 1.0       # 菱形的半高度（从中心到上/下顶点的距离，总高为 2 * DIA_HALF_H）

# 📍 5 列的中心 X 坐标（通过调大间距可以彻底拉开框与框之间的物理空隙）
COL_1 = 2.2   # 第一列中心
COL_2 = 6.8   # 第二列中心
COL_3 = 11.4  # 第三列中心
COL_4 = 16.0  # 第四列中心
COL_5 = 20.6  # 第五列中心

# 📍 3 排的中心 Y 坐标
ROW_1 = 11.0  # 第一排中心（顶排）
ROW_2 = 6.6   # 第二排中心（中排）
ROW_3 = 2.2   # 第三排中心（底排）

def draw_diamond(ax, xc, yc, w_d, h_d, fc, ec, lw=2.5):
    """
    辅助函数：给定中心坐标 (xc, yc)、半宽 w_d、半高 h_d 绘制判定菱形
    """
    vertices = [
        (xc, yc + h_d),      # 上顶点
        (xc + w_d, yc),      # 右顶点
        (xc, yc - h_d),      # 下顶点
        (xc - w_d, yc)       # 左顶点
    ]
    poly = patches.Polygon(vertices, closed=True, fc=fc, ec=ec, lw=lw, zorder=2)
    ax.add_patch(poly)

def draw_wifi_daemon_flow():
    # 创建超大画布 (24.0 x 13.0 英寸) 保证高分辨率
    fig, ax = plt.subplots(figsize=(24.0, 13.0), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 24.0)
    ax.set_ylim(0.2, 12.8)
    ax.set_aspect('equal')

    # 快捷绘制矩形方框的辅助函数
    def draw_box(x, y, fc, ec):
        ax.add_patch(patches.FancyBboxPatch(
            (x - BOX_WIDTH/2, y - BOX_HEIGHT/2), BOX_WIDTH, BOX_HEIGHT,
            boxstyle="round,pad=0.0,rounding_size=0.06",
            fc=fc, ec=ec, lw=2.5, zorder=2
        ))

    # 快捷绘制两行文字的辅助函数
    def draw_node_text(x, y, line1, line2=None, is_bold=True, text_color="#000000", sub_color="#333333"):
        if line2:
            ax.text(x, y + 0.28, line1, ha='center', va='center', fontsize=FONT_SIZE, fontweight='bold' if is_bold else 'normal', color=text_color, zorder=3)
            ax.text(x, y - 0.28, line2, ha='center', va='center', fontsize=FONT_SIZE_SUB, color=sub_color, zorder=3)
        else:
            ax.text(x, y, line1, ha='center', va='center', fontsize=FONT_SIZE, fontweight='bold' if is_bold else 'normal', color=text_color, zorder=3)

    # =========================================================================
    # 🧱 1. 核心流程节点绘制
    # =========================================================================

    # ------------------ 第一排 (ROW_1 = 11.0, 顶部) ------------------
    # 开始守护
    draw_box(COL_1, ROW_1, "#f2f2f2", "#595959")
    draw_node_text(COL_1, ROW_1, "开始守护", "注册网络监听")

    # 网络状态监听
    draw_box(COL_2, ROW_1, "#ddebf7", "#2f5597")
    draw_node_text(COL_2, ROW_1, "网络状态监听", "(Connectivity)")

    # 判定 1: WiFi状态是否已断开?
    draw_diamond(ax, COL_3, ROW_1, DIA_HALF_W, DIA_HALF_H, "#fff2e6", "#ff8000")
    draw_node_text(COL_3, ROW_1, "WiFi状态", "是否已断开?", text_color="#843c0c", sub_color="#843c0c")

    # 阶段一
    draw_box(COL_4, ROW_1, "#ddebf7", "#2f5597")
    draw_node_text(COL_4, ROW_1, "阶段一：", "自动开启WiFi")

    # 系统页面模拟
    draw_box(COL_5, ROW_1, "#ddebf7", "#2f5597")
    draw_node_text(COL_5, ROW_1, "系统页面模拟", "点击并返回桌面")

    # ------------------ 第二排 (ROW_2 = 6.6, 中部, 顺序从右到左流向) ------------------
    # 阶段二
    draw_box(COL_5, ROW_2, "#ddebf7", "#2f5597")
    draw_node_text(COL_5, ROW_2, "阶段二：", "宽限等待监测")

    # 判定 2: WiFi网络已恢复连接?
    draw_diamond(ax, COL_4, ROW_2, DIA_HALF_W, DIA_HALF_H, "#fff2e6", "#ff8000")
    draw_node_text(COL_4, ROW_2, "WiFi网络", "已恢复连接?", text_color="#843c0c", sub_color="#843c0c")

    # 判定 3: 自愈宽限是否已超时?
    draw_diamond(ax, COL_3, ROW_2, DIA_HALF_W, DIA_HALF_H, "#fff2e6", "#ff8000")
    draw_node_text(COL_3, ROW_2, "自愈宽限", "是否已超时?", text_color="#843c0c", sub_color="#843c0c")

    # 阶段三
    draw_box(COL_2, ROW_2, "#ddebf7", "#2f5597")
    draw_node_text(COL_2, ROW_2, "阶段三：", "超时通知播报")

    # ------------------ 第三排 (ROW_3 = 2.2, 底部) ------------------
    # 判定 4: 手动连接WiFi成功?
    draw_diamond(ax, COL_3, ROW_3, DIA_HALF_W, DIA_HALF_H, "#fff2e6", "#ff8000")
    draw_node_text(COL_3, ROW_3, "手动连接", "WiFi成功?", text_color="#843c0c", sub_color="#843c0c")

    # 关闭提示框
    draw_box(COL_4, ROW_3, "#e2f0d9", "#375623")
    draw_node_text(COL_4, ROW_3, "关闭提示框", "网络重置返回", text_color="#375623", sub_color="#375623")

    # =========================================================================
    # 🏹 2. 流程走线与箭头连接
    # =========================================================================
    arrow_blue = dict(arrowstyle="-|>", color="#2f5597", lw=3.5, mutation_scale=24)
    arrow_orange = dict(arrowstyle="-|>", color="#ff8000", lw=3.5, mutation_scale=24)

    # --- 2.1 第一排水平方向流向 ---
    # Start -> Network Monitor
    ax.annotate("", xy=(COL_2 - BOX_WIDTH/2 - 0.05, ROW_1), xytext=(COL_1 + BOX_WIDTH/2, ROW_1), arrowprops=arrow_blue, zorder=3)
    # Monitor -> 判定1
    ax.annotate("", xy=(COL_3 - DIA_HALF_W - 0.05, ROW_1), xytext=(COL_2 + BOX_WIDTH/2, ROW_1), arrowprops=arrow_blue, zorder=3)
    # 判定1 --Yes--> 阶段一
    ax.annotate("", xy=(COL_4 - BOX_WIDTH/2 - 0.05, ROW_1), xytext=(COL_3 + DIA_HALF_W, ROW_1), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_3 + COL_4)/2, ROW_1 + 0.3, "Yes", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center', fontweight='bold')
    # 阶段一 -> 系统页面模拟
    ax.annotate("", xy=(COL_5 - BOX_WIDTH/2 - 0.05, ROW_1), xytext=(COL_4 + BOX_WIDTH/2, ROW_1), arrowprops=arrow_blue, zorder=3)

    # 判定1 --No--> 网络状态监听 (顶端闭环)
    ax.plot([COL_3, COL_3, COL_2, COL_2], [ROW_1 + DIA_HALF_H, ROW_1 + 1.5, ROW_1 + 1.5, ROW_1 + BOX_HEIGHT/2 + 0.05], color="#ff8000", lw=3.0, zorder=1)
    ax.annotate("", xy=(COL_2, ROW_1 + BOX_HEIGHT/2 + 0.05), xytext=(COL_2, ROW_1 + BOX_HEIGHT/2 + 0.15), arrowprops=arrow_orange, zorder=3)
    ax.text(COL_3 - 0.9, ROW_1 + 1.7, "No (未断开)", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center')

    # --- 2.2 系统页面模拟 -> 阶段二 (垂直下降) ---
    ax.annotate("", xy=(COL_5, ROW_2 + BOX_HEIGHT/2 + 0.05), xytext=(COL_5, ROW_1 - BOX_HEIGHT/2), arrowprops=arrow_blue, zorder=3)

    # --- 2.3 第二排从右到左水平方向流向 ---
    # 阶段二 -> 判定2
    ax.annotate("", xy=(COL_4 + DIA_HALF_W + 0.05, ROW_2), xytext=(COL_5 - BOX_WIDTH/2, ROW_2), arrowprops=arrow_orange, zorder=3)
    # 判定2 --No--> 判定3
    ax.annotate("", xy=(COL_3 + DIA_HALF_W + 0.05, ROW_2), xytext=(COL_4 - DIA_HALF_W, ROW_2), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_3 + COL_4)/2, ROW_2 + 0.3, "No", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center', fontweight='bold')
    # 判定3 --Yes--> 阶段三
    ax.annotate("", xy=(COL_2 + BOX_WIDTH/2 + 0.05, ROW_2), xytext=(COL_3 - DIA_HALF_W, ROW_2), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_2 + COL_3)/2, ROW_2 + 0.3, "Yes", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center', fontweight='bold')

    # 判定3 --No--> 阶段二 (未超时回路)
    ax.plot([COL_3, COL_3, COL_5, COL_5], [ROW_2 + DIA_HALF_H, ROW_2 + 1.5, ROW_2 + 1.5, ROW_2 + BOX_HEIGHT/2 + 0.05], color="#ff8000", lw=3.0, zorder=1)
    ax.annotate("", xy=(COL_5, ROW_2 + BOX_HEIGHT/2 + 0.05), xytext=(COL_5, ROW_2 + BOX_HEIGHT/2 + 0.15), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_3 + COL_5)/2, ROW_2 + 1.7, "No (未超时)", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center')

    # 判定2 --Yes--> 网络状态监听 (左侧超大闭环回路)
    ax.plot([COL_4, COL_4, 1.0, 1.0, COL_2 - BOX_WIDTH/2 - 0.4, COL_2 - BOX_WIDTH/2 - 0.4, COL_2 - BOX_WIDTH/2], 
            [ROW_2 + DIA_HALF_H, ROW_2 + 2.4, ROW_2 + 2.4, ROW_1, ROW_1, ROW_1, ROW_1], 
            color="#ff8000", lw=3.0, zorder=1)
    ax.annotate("", xy=(COL_2 - BOX_WIDTH/2, ROW_1), xytext=(COL_2 - BOX_WIDTH/2 - 0.3, ROW_1), arrowprops=arrow_orange, zorder=3)
    ax.text(COL_4, ROW_2 + 2.6, "Yes (恢复)", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center')

    # --- 2.4 阶段三 -> 判定4 (垂直下降折线) ---
    mid_y_23 = (ROW_2 + ROW_3) / 2
    ax.plot([COL_2, COL_2, COL_3 - DIA_HALF_W], [ROW_2 - BOX_HEIGHT/2, mid_y_23, mid_y_23], color="#2f5597", lw=3.0, zorder=1)
    ax.annotate("", xy=(COL_3 - DIA_HALF_W, ROW_3), xytext=(COL_3 - DIA_HALF_W, mid_y_23), arrowprops=arrow_blue, zorder=3)

    # --- 2.5 第三排水平方向流向 ---
    # 判定4 --Yes--> 关闭提示框
    ax.annotate("", xy=(COL_4 - BOX_WIDTH/2 - 0.05, ROW_3), xytext=(COL_3 + DIA_HALF_W, ROW_3), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_3 + COL_4)/2, ROW_3 + 0.3, "Yes", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center', fontweight='bold')

    # 判定4 --No--> 挂起并寻网状态机 (向下折线挂起回路)
    ax.plot([COL_3, COL_3, 1.0, 1.0, COL_2, COL_2], [ROW_3 - DIA_HALF_H, 0.6, 0.6, ROW_2 - BOX_HEIGHT/2 - 0.5, ROW_2 - BOX_HEIGHT/2 - 0.5, ROW_2 - BOX_HEIGHT/2],
            color="#ff8000", lw=3.0, zorder=1)
    ax.annotate("", xy=(COL_2, ROW_2 - BOX_HEIGHT/2), xytext=(COL_2, ROW_2 - BOX_HEIGHT/2 - 0.15), arrowprops=arrow_orange, zorder=3)
    ax.text(6.0, 0.35, "No (挂起等待手动开启/寻找网络)", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center')

    # 关闭提示框 -> 网络监听 (右侧大回路)
    ax.plot([COL_4 + BOX_WIDTH/2, 23.2, 23.2, COL_2 + BOX_WIDTH/2 + 0.4, COL_2 + BOX_WIDTH/2 + 0.4, COL_2 + BOX_WIDTH/2],
            [ROW_3, ROW_3, ROW_1, ROW_1, ROW_1, ROW_1],
            color="#2f5597", lw=3.0, zorder=1)
    ax.annotate("", xy=(COL_2 + BOX_WIDTH/2, ROW_1), xytext=(COL_2 + BOX_WIDTH/2 + 0.3, ROW_1), arrowprops=arrow_blue, zorder=3)

    # =========================================================================
    # 💾 3. 图片输出保存
    # =========================================================================
    save_path = os.path.join(out_dir, "wifi_daemon.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.savefig(os.path.join(out_dir, "wifi_daemon.pdf"), dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print(f"Successfully generated wifi_daemon.png and .pdf to {save_path}!")

if __name__ == "__main__":
    draw_wifi_daemon_flow()
