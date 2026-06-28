import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# out_dir：图表导出的绝对路径目录（对应 LaTeX 项目的 figures 文件夹）
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# plt.rcParams：配置 Matplotlib 的全局字体参数，防止中文字符渲染时乱码
plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_focus_retreat():
    # fig：Matplotlib 顶层图像窗口对象 (Figure)
    # ax：Matplotlib 坐标轴绘图区对象 (Axes)，所有的形状和文本都绘制在其上
    # figsize=(22, 12)：画布物理尺寸为宽 22 英寸，高 12 英寸，是完美的时序图长宽比
    # dpi=300：设置 300 DPI 分辨率，提供高清晰度学术导出效果
    fig, ax = plt.subplots(figsize=(22, 12), dpi=300)
    ax.axis('off') # 关闭坐标轴的刻度线、标签和边框
    
    # 显式设定 X 轴与 Y 轴的坐标范围为归一化区间 [0, 1]，方便使用相对比例定位时序线和生命线
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # === 学术图表字体缩放数学模型 ===
    # 目标：使导出的 PNG 插入 LaTeX 后，图内的物理字号与 PDF 正文字号严格对齐
    
    # latex_scale：图片在 LaTeX 正文排版中通过 [width=0.85\textwidth] 设定的缩放系数
    latex_scale = 0.85           
    
    # latex_textwidth_inch：LaTeX A4 页面排版文字区域的物理宽度（16厘米，换算为约 6.3 英寸）
    latex_textwidth_inch = 6.3   
    
    # canvas_width_inch：Matplotlib 画布物理宽度，与前面 figsize 设置的 22 英寸一致
    canvas_width_inch = 22.0     
    
    # scale_factor：物理缩放因子（图片插入 LaTeX 后被整体压缩的物理比例，约 0.243）
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  
    
    # X_pdf：大层级和步骤说明文字的期望物理字号（小四号字 12.0pt，引入 0.8 倍微调防显粗笨）
    X_pdf = 10                 
    
    # Y_pdf：具体圆角矩形内动作说明文字的期望物理字号（五号字 11.0pt，引入 0.8 倍微调）
    Y_pdf = 10                
    
    # font_header_size：转换回 Matplotlib 空间的头部生命线大字渲染字号大小
    font_header_size = X_pdf / scale_factor
    
    # font_step_size：转换回 Matplotlib 空间的步骤顺序文案渲染字号大小
    font_step_size = X_pdf / scale_factor
    
    # font_box_size：转换回 Matplotlib 空间的圆角动作框内文案渲染字号大小
    font_box_size = Y_pdf / scale_factor
    
    # x_left：左侧生命线（代表老年用户/干扰源）的 X 轴归一化位置
    x_left = 0.17
    
    # x_mid：中间生命线（代表桌面主程序）的 X 轴归一化位置，从 0.47 调至 0.44 以支持右侧框体加宽
    x_mid = 0.44
    
    # x_right：右侧生命线（代表无障碍服务引擎）的 X 轴归一化位置，从 0.77 调至 0.71，给右侧框体向右扩展腾出空间
    x_right = 0.71
    
    # -------------------------------------------------------------
    # 1. 绘制 3 条生命线垂直虚线
    # x：临时循环变量，用于定位三条垂直虚线的横坐标
    # -------------------------------------------------------------
    for x in [x_left, x_mid, x_right]:
        # 从 Y 坐标 0.06 贯穿延伸至 0.80 的中灰色虚线 (lw=2.5, ls="--")
        ax.plot([x, x], [0.06, 0.80], color="#757575", lw=2.5, ls="--", zorder=1)
        
    headers = [
        {"x_center": x_left, "text": "老年用户（干扰源）", "width": 0.28},
        {"x_center": x_mid, "text": "桌面主程序", "width": 0.20},
        {"x_center": x_right, "text": "无障碍服务引擎", "width": 0.25}
    ]
    
    # h：临时循环变量，用于绘制每一个生命线标题框
    for h in headers:
        # box_width：标题框在画布上的相对宽度（根据不同文本的长度独立配置其框宽）
        box_width = h["width"]
        # box_height：标题框在画布上的相对高度
        box_height = 0.13
        # box：标题框的 FancyBboxPatch 蓝边框圆角矩形对象，居中于 h["x_center"]，Y 轴在 0.80
        box = patches.FancyBboxPatch(
            (h["x_center"] - box_width/2.0, 0.80), box_width, box_height,
            boxstyle="round,pad=0.005",
            fc="#e3f2fd", ec="#1976d2", lw=3.5,
            zorder=3
        )
        ax.add_patch(box)
        # 在标题框的几何中心 (h["x_center"], 0.865) 处添加居中对齐文本
        ax.text(
            h["x_center"], 0.865, h["text"],
            ha='center', va='center', fontsize=font_header_size, fontweight='bold', color="#0d47a1",
            zorder=4
        )
        
    # -------------------------------------------------------------
    # 3. 步骤一：自动化任务发起（桌面主程序 -> 无障碍服务引擎）
    # y1：步骤一的 Y 轴归一化高度坐标值
    # -------------------------------------------------------------
    y1 = 0.71
    # 绘制从 x_mid 指向 x_right 的黑色实线带箭头指示线
    ax.annotate(
        "", xy=(x_right, y1), xytext=(x_mid, y1),
        arrowprops=dict(arrowstyle="-|>", color="#212121", lw=4, mutation_scale=25),
        zorder=2
    )
    # 在指示线上方添加动作说明文本
    ax.text(
        (x_mid + x_right)/2.0, y1 + 0.015, "1.  自动化任务发起",
        ha='center', va='bottom', fontsize=font_step_size, fontweight='bold', color="#212121"
    )
    
    # -------------------------------------------------------------
    # 4. 步骤二：释放焦点隐藏悬浮窗（桌面主程序自调用 Self-call 框）
    # y2_center：步骤二动作框的 Y 轴垂直中心坐标
    # -------------------------------------------------------------
    y2_center = 0.58
    # box2_w：动作框在画布上的相对宽度（从 0.18 调宽至 0.23，防止 11pt 的中文字体溢出）
    box2_w = 0.23
    # box2_h：动作框在画布上的相对高度（Y轴高度占比）
    box2_h = 0.12
    # box2_x：动作框的左下角起始 X 轴坐标（放在 x_mid 右移 0.01 的位置，作自调用展示）
    box2_x = x_mid + 0.01
    # box2_y：动作框的左下角起始 Y 轴坐标
    box2_y = y2_center - box2_h/2.0
    
    # box2：用于步骤二的 FancyBboxPatch 橙色圆角动作矩形方框
    box2 = patches.FancyBboxPatch(
        (box2_x, box2_y), box2_w, box2_h,
        boxstyle="round,pad=0.005",
        fc="#fff3e0", ec="#fb8c00", lw=3,
        zorder=3
    )
    ax.add_patch(box2)
    # 在该圆角动作框的中心位置渲染文字描述，支持换行
    ax.text(
        box2_x + box2_w/2.0, y2_center, "2. 释放焦点\n隐藏悬浮窗",
        ha='center', va='center', fontsize=font_box_size, fontweight='bold', color="#e65100",
        multialignment='center', zorder=4
    )
    
    # 绘制表示桌面主程序自调用的弧形虚线箭头连接线 (connectionstyle="arc3,rad=1.3")
    ax.annotate(
        "", xy=(box2_x, y2_center - 0.04), xytext=(box2_x, y2_center + 0.04),
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=1.3", color="#fb8c00", lw=3.5, ls="--", mutation_scale=15),
        zorder=2
    )
    
    # -------------------------------------------------------------
    # 5. 步骤三：误触屏幕/权限弹窗干扰（老年用户 -> 无障碍服务引擎）
    # y3：步骤三的 Y 轴归一化高度坐标值
    # -------------------------------------------------------------
    y3 = 0.43
    # 绘制从 x_left 直接指向 x_right 的红色警示实线带箭头指示线，指示发生了误触强占
    ax.annotate(
        "", xy=(x_right, y3), xytext=(x_left, y3),
        arrowprops=dict(arrowstyle="-|>", color="#d32f2f", lw=4, mutation_scale=25),
        zorder=2
    )
    # 在指示线上方添加红色动作说明文本
    ax.text(
        (x_left + x_right)/2.0, y3 + 0.015, "3.  误触屏幕  /  系统权限弹窗干扰",
        ha='center', va='bottom', fontsize=font_step_size, fontweight='bold', color="#d32f2f"
    )
    
    # -------------------------------------------------------------
    # 6. 步骤四：状态机停滞超时触发死锁（无障碍引擎自监测超时动作框）
    # y4_center：步骤四动作框的 Y 轴垂直中心坐标
    # -------------------------------------------------------------
    y4_center = 0.28
    # box4_w：动作框在画布上的相对宽度（从 0.21 调宽至 0.25，防止 11pt 的中文字体溢出）
    box4_w = 0.25
    # box4_h：动作框在画布上的相对高度
    box4_h = 0.12
    # box4_x：动作框的左下角起始 X 轴坐标（放在 x_right 右侧 0.01 处）
    box4_x = x_right + 0.01
    # box4_y：动作框的左下角起始 Y 轴坐标
    box4_y = y4_center - box4_h/2.0
    
    # box4：表示超时死锁的 FancyBboxPatch 红色报警圆角矩形方框
    box4 = patches.FancyBboxPatch(
        (box4_x, box4_y), box4_w, box4_h,
        boxstyle="round,pad=0.005",
        fc="#ffebee", ec="#c62828", lw=3,
        zorder=3
    )
    ax.add_patch(box4)
    # 框内居中渲染多行死锁超时报警的文字
    ax.text(
        box4_x + box4_w/2.0, y4_center, "4. 状态机停滞\n> 5秒触发死锁",
        ha='center', va='center', fontsize=font_box_size, fontweight='bold', color="#b71c1c",
        multialignment='center', zorder=4
    )
    
    # 绘制表示无障碍引擎自身进行超时心跳监测的自调用红虚线弧形箭头
    ax.annotate(
        "", xy=(box4_x, y4_center - 0.04), xytext=(box4_x, y4_center + 0.04),
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=1.3", color="#c62828", lw=3.5, ls="--", mutation_scale=15),
        zorder=2
    )
    
    # -------------------------------------------------------------
    # 7. 步骤五：强制模拟返回键重置自回归（无障碍服务引擎 -> 桌面主程序）
    # y5：步骤五的 Y 轴归一化高度坐标值
    # -------------------------------------------------------------
    y5 = 0.13
    # 绘制从 x_right 指向 x_mid 的蓝色反馈重置实线指示箭头，表示执行了状态机的自回归复位
    ax.annotate(
        "", xy=(x_mid, y5), xytext=(x_right, y5),
        arrowprops=dict(arrowstyle="-|>", color="#1976d2", lw=4, mutation_scale=25),
        zorder=2
    )
    # 在蓝色箭头上方渲染回归说明文本
    ax.text(
        (x_mid + x_right)/2.0, y5 + 0.015, "5.  强制模拟返回键重置（自回归）",
        ha='center', va='bottom', fontsize=font_box_size, fontweight='bold', color="#1976d2"
    )
    
    # output_path：图表最终保存的完整导出路径
    output_path = os.path.join(out_dir, 'fig2_4_focus_retreat.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    
    print("Successfully generated focus retreat sequence diagram with 1.2x scale fonts!")

if __name__ == '__main__':
    draw_focus_retreat()


if __name__ == '__main__':
    draw_focus_retreat()
