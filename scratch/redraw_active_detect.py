import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# out_dir：图表导出的绝对路径目录（对应 LaTeX 项目的 figures 文件夹）
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# plt.rcParams：配置 Matplotlib 的全局字体参数，防止中文字符渲染时乱码
plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_active_detect():
    # fig：Matplotlib 顶层图像窗口对象 (Figure)
    # ax：Matplotlib 坐标轴绘图区对象 (Axes)，所有的形状和文本都绘制在其上
    # figsize=(28, 14)：画布物理尺寸为宽 28 英寸，高 14 英寸
    # dpi=300：设置 300 DPI 分辨率，提供高清晰度学术导出效果
    fig, ax = plt.subplots(figsize=(28, 14), dpi=300)
    ax.axis('off') # 关闭坐标轴的刻度线、标签和边框
    
    # 显式设定 X 轴与 Y 轴的坐标范围为归一化区间 [0, 1]，方便使用相对比例定位图形
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # === 学术图表字体缩放数学模型 ===
    # 目标：使导出的 PNG 插入 LaTeX 后，图内的物理字号与 PDF 正文字号严格对齐
    
    # latex_scale：图片在 LaTeX 正文排版中通过 [width=0.9\textwidth] 设定的缩放系数
    latex_scale = 0.9            
    
    # latex_textwidth_inch：LaTeX A4 页面排版文字区域的物理宽度（16厘米，换算为约 6.3 英寸）
    latex_textwidth_inch = 6.3   
    
    # canvas_width_inch：Matplotlib 画布物理宽度，与前面 figsize 设置的 28 英寸一致
    canvas_width_inch = 28.0     
    
    # scale_factor：物理缩放因子（图片插入 LaTeX 后被整体压缩的物理比例，约 0.2025）
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  
    
    # X_pdf：大层级标题字号期望值（设置为 11pt，对应小四与五号字号之间）
    X_pdf = 10.0                  
    
    # Y_pdf：内部具体模块文字字号期望值（设置为 11pt）
    Y_pdf = 10.0                 
    
    # Z_pdf：较小标注文字字号期望值（设置为 11pt）
    Z_pdf = 10.0                  
    
    # font_large_size：转换回 Matplotlib 空间的大号字体渲染字号大小（约 54.3pt）
    font_large_size = X_pdf / scale_factor
    
    # font_mid_size：转换回 Matplotlib 空间的中号字体渲染字号大小（约 54.3pt）
    font_mid_size = Y_pdf / scale_factor
    
    # font_small_size：转换回 Matplotlib 空间的小号字体渲染字号大小（约 54.3pt）
    font_small_size = Z_pdf / scale_factor
    
    # grey_fill：步骤一“混淆隔离态”方框的填充颜色（浅灰色，代表静态黑盒）
    grey_fill = "#f5f5f5"
    
    # grey_border：步骤一“混淆隔离态”方框的边框颜色（中灰色）
    grey_border = "#9e9e9e"
    
    # orange_fill：中间核心动作“窗口内容震荡”方框的填充颜色（警示性浅橙色）
    orange_fill = "#fff3e0"
    
    # orange_border：中间核心动作“窗口内容震荡”方框的边框颜色（深橙色）
    orange_border = "#fb8c00"
    
    # green_fill：步骤二“真实树挂载与定位”方框的填充颜色（健康浅绿色，代表恢复解析）
    green_fill = "#e8f5e9"
    
    # green_border：步骤二“真实树挂载与定位”方框的边框颜色（深绿色）
    green_border = "#43a047"
    
    # yellow_fill：底部“特征归一化模型”公式框的填充颜色（淡黄色）
    yellow_fill = "#fffde7"
    
    # yellow_border：底部“特征归一化模型”公式框的边框颜色（橄榄绿/黄绿色）
    yellow_border = "#c0ca33"
    
    # row_height：侧边各个小方框在 Y 轴上的归一化高度（高度占画布总高的 18%）
    row_height = 0.18
    
    # r1_y：最上排（第一行）方框的 Y 轴起始坐标
    r1_y = 0.68
    
    # r2_y：中间排（第二行）方框的 Y 轴起始坐标
    r2_y = 0.44
    
    # r3_y：最下排（第三行）方框的 Y 轴起始坐标
    r3_y = 0.20
    
    # left_boxes：步骤一（左侧）各方框的纵向定位 Y 坐标及显示文案字典列表
    left_boxes = [
        {"y": r1_y, "text": "透明占位节点"},
        {"y": r2_y, "text": "混淆资源 ID"},
        {"y": r3_y, "text": "隐藏真实控件"}
    ]
    for item in left_boxes:
        # box：使用 FancyBboxPatch 构建的左侧圆角矩形方框（X轴范围为 0.04 到 0.28，宽 0.24）
        # ls="--"：使用虚线表示“隐藏和混淆”的不确定性
        box = patches.FancyBboxPatch(
            (0.04, item["y"]), 0.24, row_height,
            boxstyle="round,pad=0.005",
            fc=grey_fill, ec=grey_border, lw=3, ls="--",
            zorder=2
        )
        ax.add_patch(box)
        # 在方框中心位置（X=0.16，Y 轴中点）渲染文本
        ax.text(
            0.16, item["y"] + row_height/2.0, item["text"],
            ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#424242"
        )
        
    # center_y：中间橙色动作框的 Y 轴起始坐标
    center_y = 0.39
    
    # center_height：中间橙色动作框的高度（0.28 占画布高度的 28%）
    center_height = 0.28
    
    # center_box：中间“窗口内容震荡”圆角矩形方框（X轴范围为 0.345 到 0.655，宽 0.31）
    center_box = patches.FancyBboxPatch(
        (0.345, center_y), 0.31, center_height,
        boxstyle="round,pad=0.015",
        fc=orange_fill, ec=orange_border, lw=4,
        zorder=2
    )
    ax.add_patch(center_box)
    ax.text(
        0.50, center_y + center_height/2.0, "窗口内容震荡\n(微位移滑动 1-2px)",
        ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#e65100",
        multialignment='center'
    )
    
    # right_boxes：步骤二（右侧）各方框的纵向定位 Y 坐标及显示文案字典列表
    right_boxes = [
        {"y": r1_y, "text": "真实控件子树暴露"},
        {"y": r2_y, "text": "拓扑深度提取"},
        {"y": r3_y, "text": "计算包围盒重心"}
    ]
    for item in right_boxes:
        # box：右侧成功的实线圆角矩形方框（X轴范围为 0.72 到 0.96，宽 0.24）
        box = patches.FancyBboxPatch(
            (0.70, item["y"]), 0.28, row_height,
            boxstyle="round,pad=0.005",
            fc=green_fill, ec=green_border, lw=3,
            zorder=2
        )
        ax.add_patch(box)
        # 在方框中心位置（X=0.84，Y 轴中点）渲染文本
        ax.text(
            0.84, item["y"] + row_height/2.0, item["text"],
            ha='center', va='center', fontsize=font_mid_size, fontweight='bold', color="#1b5e20"
        )
        
    # 使用 ax.annotate 绘制左列指向中间列的红色虚线指示箭头，代表震荡机制被触发
    # xy=(0.345, 0.53)：指示箭头的终点坐标（中间框新左边缘 0.345）
    # xytext=(0.28, 0.53)：指示箭头的起点坐标（左列右边缘）
    ax.annotate(
        "", xy=(0.345, 0.53), xytext=(0.28, 0.53),
        arrowprops=dict(arrowstyle="-|>", color="#d32f2f", lw=4.5, ls="--", mutation_scale=25),
        zorder=3
    )
    ax.text(
        0.3125, 0.56, "触发更新",
        ha='center', va='bottom', fontsize=font_small_size, fontweight='bold', color="#d32f2f"
    )
    
    # 使用 ax.annotate 绘制中间列指向右列的蓝色实线指示箭头，代表重绘行为产生物理结果
    # xy=(0.70, 0.53)：指示箭头的终点坐标（右列新左边缘 0.70）
    # xytext=(0.655, 0.53)：指示箭头的起点坐标（中间框新右边缘 0.655）
    ax.annotate(
        "", xy=(0.70, 0.53), xytext=(0.655, 0.53),
        arrowprops=dict(arrowstyle="-|>", color="#1976d2", lw=4.5, mutation_scale=25),
        zorder=3
    )
    ax.text(
        0.6775, 0.56, "强制重绘\n(Remount)",
        ha='center', va='bottom', fontsize=font_small_size, fontweight='bold', color="#1976d2",
        multialignment='center'
    )
    
    # bottom_y：底部归一化公式框的 Y 轴起始坐标
    bottom_y = 0.04
    
    # bottom_height：底部公式框的高（从 0.11 调大 10% 到 0.12，占画布总高度的 12%）
    bottom_height = 0.12
    
    # bottom_box：底部横向通栏公式框（X轴范围为 0.015 到 0.985，宽 0.97）
    bottom_box = patches.FancyBboxPatch(
        (0.015, bottom_y), 0.97, bottom_height,
        boxstyle="round,pad=0.005",
        fc=yellow_fill, ec=yellow_border, lw=3.5,
        zorder=2
    )
    ax.add_patch(bottom_box)
    
    # text_content：存储要渲染的两行学术数学公式和机制说明文本
    text_content = (
        "UI 特征归一化模型 (Feature Normalization)\n"
        "匹配度P=w1×(相对拓扑关系)+w2×(视觉重心偏移量)>98%->锁定目标"
    )
    # font_formula_size：底部公式框文字期望在 PDF 中以 10.0pt 大小呈现，换算为 Matplotlib 画布上的实际字号
    font_formula_size = 10.0 / scale_factor
    ax.text(
        0.50, bottom_y + bottom_height/2.0,
        text_content,
        ha='center', va='center', fontsize=font_formula_size, fontweight='bold', color="#827717",
        multialignment='center'
    )
    
    # 使用 ax.plot 绘制一条连接右下角“计算包围盒重心”框 (0.84, 0.20) 与底部公式计算框顶部中心 (0.50, 0.16) 的黑色实线
    # 终点 Y 坐标由于黄框高度增加至 0.12，顶边变更为 bottom_y + bottom_height = 0.04 + 0.12 = 0.16，故同步调整
    ax.plot([0.84, 0.50], [0.20, 0.16], color="#212121", lw=3.5, zorder=1)
    
    # output_path：生成的图片保存的完整物理路径
    output_path = os.path.join(out_dir, 'fig2_3_shake_match.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    
    print("Successfully generated active detection mechanism diagram!")

if __name__ == '__main__':
    draw_active_detect()


if __name__ == '__main__':
    draw_active_detect()
