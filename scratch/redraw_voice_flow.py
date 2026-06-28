import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# =========================================================================
# 🎓 流程图 1: 语音辅助模块工作流程 (Voice Flow)
# =========================================================================
# 本脚本生成图表保存的目标物理路径，执行后会生成 voice_flow.png 和 voice_flow.pdf
# =========================================================================

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# 配置全局中文字体，确保在 Windows 环境下能正常渲染中文
plt.rcParams['font.sans-serif'] = ['FangSong', 'SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# =========================================================================
# ⚙️ 核心几何与排版参数配置区 (您可以在这里修改数值来自定义图形大小和位置)
# =========================================================================
FONT_SIZE = 22.0       # 核心节点的主标题字号（例如：“语音转文本”、“开始语音辅助”）
FONT_SIZE_SUB = 18.0   # 核心节点的辅助/子标题字号（例如：“(ASR)”、“(Success End)”）
FONT_SIZE_LABEL = 20.0 # 线条上的判断标签字号（例如：“Yes”、“No”）

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

def draw_voice_flow():
    # 创建超大画布 (24.0 x 13.0 英寸) 保证高分辨率
    fig, ax = plt.subplots(figsize=(24.0, 11.0), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 24.0)
    ax.set_ylim(1.0, 12.2)
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
    # Start 节点
    draw_box(COL_1, ROW_1, "#f2f2f2", "#595959")
    draw_node_text(COL_1, ROW_1, "开始语音辅助", "长按/按键触发")

    # ASR 语音识别
    draw_box(COL_2, ROW_1, "#ddebf7", "#2f5597")
    draw_node_text(COL_2, ROW_1, "语音转文本", "(ASR)")

    # 判定 1: 命中预设关键词?
    draw_diamond(ax, COL_3, ROW_1, DIA_HALF_W, DIA_HALF_H, "#fff2e6", "#ff8000")
    draw_node_text(COL_3, ROW_1, "命中预设", "关键词?", text_color="#843c0c", sub_color="#843c0c")

    # 判定 2: 编辑距离纠错成功?
    draw_diamond(ax, COL_4, ROW_1, DIA_HALF_W, DIA_HALF_H, "#fff2e6", "#ff8000")
    draw_node_text(COL_4, ROW_1, "编辑距离", "纠错成功?", text_color="#843c0c", sub_color="#843c0c")

    # 异常退出：未识别
    draw_box(COL_5, ROW_1, "#fce4d6", "#c00000")
    draw_node_text(COL_5, ROW_1, "TTS播报未识别", "退出流程并重试", text_color="#c00000", sub_color="#663333")

    # ------------------ 第二排 (ROW_2 = 6.6, 中部) ------------------
    # 解析目标姓名
    draw_box(COL_2, ROW_2, "#ddebf7", "#2f5597")
    draw_node_text(COL_2, ROW_2, "解析目标姓名", "检索Room数据库")

    # 判定 3: 模糊匹配?
    draw_diamond(ax, COL_3, ROW_2, DIA_HALF_W, DIA_HALF_H, "#fff2e6", "#ff8000")
    draw_node_text(COL_3, ROW_2, "模糊拼音/", "首字母匹配?", text_color="#843c0c", sub_color="#843c0c")

    # 判定 4: 拼音纠错?
    draw_diamond(ax, COL_4, ROW_2, DIA_HALF_W, DIA_HALF_H, "#fff2e6", "#ff8000")
    draw_node_text(COL_4, ROW_2, "编辑距离", "拼音纠错?", text_color="#843c0c", sub_color="#843c0c")

    # 异常退出：联系人未找到
    draw_box(COL_5, ROW_2, "#fce4d6", "#c00000")
    draw_node_text(COL_5, ROW_2, "TTS播报未找到", "提示用户手动维护", text_color="#c00000", sub_color="#663333")

    # ------------------ 第三排 (ROW_3 = 2.2, 底部) ------------------
    # 执行拨号动作
    draw_box(COL_2, ROW_3, "#ddebf7", "#2f5597")
    draw_node_text(COL_2, ROW_3, "执行一键直拨/微信", "启动底层无障碍状态机")

    # TTS 播报状态
    draw_box(COL_3, ROW_3, "#ddebf7", "#2f5597")
    draw_node_text(COL_3, ROW_3, "TTS播报呼叫状态", "(如'正在呼叫大儿子')")

    # 流程成功结束
    draw_box(COL_4, ROW_3, "#e2f0d9", "#375623")
    draw_node_text(COL_4, ROW_3, "流程成功结束", "(Success End)", text_color="#375623", sub_color="#375623")

    # =========================================================================
    # 🏹 2. 流程走线与箭头连接
    # =========================================================================
    arrow_blue = dict(arrowstyle="-|>", color="#2f5597", lw=3.5, mutation_scale=24)
    arrow_orange = dict(arrowstyle="-|>", color="#ff8000", lw=3.5, mutation_scale=24)

    # --- 2.1 第一排水平方向流向 ---
    # Start -> ASR
    ax.annotate("", xy=(COL_2 - BOX_WIDTH/2 - 0.05, ROW_1), xytext=(COL_1 + BOX_WIDTH/2, ROW_1), arrowprops=arrow_blue, zorder=3)
    # ASR -> 判定1
    ax.annotate("", xy=(COL_3 - DIA_HALF_W - 0.05, ROW_1), xytext=(COL_2 + BOX_WIDTH/2, ROW_1), arrowprops=arrow_blue, zorder=3)
    # 判定1 --No--> 判定2
    ax.annotate("", xy=(COL_4 - DIA_HALF_W - 0.05, ROW_1), xytext=(COL_3 + DIA_HALF_W, ROW_1), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_3 + COL_4)/2, ROW_1 + 0.3, "No", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center', fontweight='bold')
    # 判定2 --No--> 异常退出
    ax.annotate("", xy=(COL_5 - BOX_WIDTH/2 - 0.05, ROW_1), xytext=(COL_4 + DIA_HALF_W, ROW_1), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_4 + COL_5)/2, ROW_1 + 0.3, "No", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center', fontweight='bold')

    # --- 2.2 第一排折线流向第二排 (Yes) ---
    mid_y_12 = (ROW_1 + ROW_2) / 2
    # 判定1 --Yes--> 解析姓名
    ax.plot([COL_3, COL_3, COL_2, COL_2], [ROW_1 - DIA_HALF_H, mid_y_12, mid_y_12, ROW_2 + BOX_HEIGHT/2 + 0.05], color="#ff8000", lw=3.0, zorder=1)
    ax.annotate("", xy=(COL_2, ROW_2 + BOX_HEIGHT/2 + 0.05), xytext=(COL_2, ROW_2 + BOX_HEIGHT/2 + 0.2), arrowprops=arrow_orange, zorder=3)
    ax.text(COL_3 - 0.6, mid_y_12 + 0.4, "Yes (命中)", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center')
    # 判定2 --Yes--> 解析姓名
    ax.plot([COL_4, COL_4, COL_3], [ROW_1 - DIA_HALF_H, mid_y_12, mid_y_12], color="#ff8000", lw=3.0, zorder=1)
    ax.text(COL_4 - 0.7, mid_y_12 + 0.4, "Yes (纠错成功)", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center')

    # --- 2.3 第二排水平方向流向 ---
    # 解析姓名 -> 判定3
    ax.annotate("", xy=(COL_3 - DIA_HALF_W - 0.05, ROW_2), xytext=(COL_2 + BOX_WIDTH/2, ROW_2), arrowprops=arrow_blue, zorder=3)
    # 判定3 --No--> 判定4
    ax.annotate("", xy=(COL_4 - DIA_HALF_W - 0.05, ROW_2), xytext=(COL_3 + DIA_HALF_W, ROW_2), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_3 + COL_4)/2, ROW_2 + 0.3, "No", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center', fontweight='bold')
    # 判定4 --No--> 异常退出
    ax.annotate("", xy=(COL_5 - BOX_WIDTH/2 - 0.05, ROW_2), xytext=(COL_4 + DIA_HALF_W, ROW_2), arrowprops=arrow_orange, zorder=3)
    ax.text((COL_4 + COL_5)/2, ROW_2 + 0.3, "No", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center', fontweight='bold')

    # --- 2.4 第二排折线流向第三排 (Yes) ---
    mid_y_23 = (ROW_2 + ROW_3) / 2
    # 判定3 --Yes--> 执行直拨/微信
    ax.plot([COL_3, COL_3, COL_2, COL_2], [ROW_2 - DIA_HALF_H, mid_y_23, mid_y_23, ROW_3 + BOX_HEIGHT/2 + 0.05], color="#ff8000", lw=3.0, zorder=1)
    ax.annotate("", xy=(COL_2, ROW_3 + BOX_HEIGHT/2 + 0.05), xytext=(COL_2, ROW_3 + BOX_HEIGHT/2 + 0.2), arrowprops=arrow_orange, zorder=3)
    ax.text(COL_3 - 0.6, mid_y_23 + 0.4, "Yes (命中)", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center')
    # 判定4 --Yes--> 执行直拨/微信
    ax.plot([COL_4, COL_4, COL_3], [ROW_2 - DIA_HALF_H, mid_y_23, mid_y_23], color="#ff8000", lw=3.0, zorder=1)
    ax.text(COL_4 - 0.7, mid_y_23 + 0.4, "Yes (拼音匹配)", fontsize=FONT_SIZE_LABEL, color="#843c0c", ha='center')

    # --- 2.5 第三排水平方向流向 ---
    # 执行直拨/微信 -> TTS播报状态
    ax.annotate("", xy=(COL_3 - BOX_WIDTH/2 - 0.05, ROW_3), xytext=(COL_2 + BOX_WIDTH/2, ROW_3), arrowprops=arrow_blue, zorder=3)
    # TTS播报状态 -> 流程成功结束
    ax.annotate("", xy=(COL_4 - BOX_WIDTH/2 - 0.05, ROW_3), xytext=(COL_3 + BOX_WIDTH/2, ROW_3), arrowprops=arrow_blue, zorder=3)

    # =========================================================================
    # 💾 3. 图片输出保存
    # =========================================================================
    save_path = os.path.join(out_dir, "voice_flow.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.savefig(os.path.join(out_dir, "voice_flow.pdf"), dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print(f"Successfully generated voice_flow.png and .pdf to {save_path}!")

if __name__ == "__main__":
    draw_voice_flow()
