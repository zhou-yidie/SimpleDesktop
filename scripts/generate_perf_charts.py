import matplotlib.pyplot as plt
import numpy as np
import os

# 确保输出目录存在
os.makedirs('thesis_figures', exist_ok=True)

# 设置中文字体，兼容 Windows 和 macOS
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

def draw_response_time():
    # 数据来源于 4.3.2 响应时间测试
    labels = [
        '联系人卡片\n操作面板', 
        '高对比度\n模式切换', 
        '字号档位\n切换', 
        '主题模式\n切换', 
        '语音助手\n对话框', 
        '应用启动\n响应'
    ]
    times = [45, 76, 82, 91, 210, 480]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # === 学术图表字体缩放数学模型 (方案一) ===
    # 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
    latex_scale = 0.85           # LaTeX 中的 width=0.85\textwidth 缩放因子
    latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
    canvas_width_inch = 8.0      # Matplotlib 画布宽度
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例
    
    X_pdf = 12.0 * 0.8                 # 主要标题与坐标轴标签：12pt (小四)
    Y_pdf = 11.0 * 0.8                 # 轴刻度、图例与数据标注：11pt
    
    font_label_size = X_pdf / scale_factor
    font_tick_size = Y_pdf / scale_factor
    
    bars = ax.barh(labels, times, color='#4A90E2', height=0.5)
    
    # 添加数据标签
    ax.bar_label(bars, padding=3, fmt='%d ms', fontsize=font_tick_size)
    
    # 绘制参考线
    ax.axvline(x=100, color='#E74C3C', linestyle='--', alpha=0.7, label='即时反馈阈值 (100ms)')
    ax.axvline(x=500, color='#F39C12', linestyle='--', alpha=0.7, label='流畅感知阈值 (500ms)')
    
    ax.set_xlabel('响应时间 (毫秒)', fontsize=font_label_size, fontweight='bold')
    ax.tick_params(axis='both', labelsize=font_tick_size)
    # 删除图形内多余标题以符合 LaTeX 规范，但此处可根据原设计微调
    ax.set_title('关键操作响应时间测试结果', fontsize=font_label_size, fontweight='bold')
    ax.legend(loc='lower right', fontsize=font_tick_size)
    
    # 去除边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
    plt.savefig('thesis_figures/fig4_response_time.png', dpi=300)
    plt.savefig('thesis_figures/fig4_response_time.pdf')
    plt.savefig(os.path.join(out_dir, 'fig4_response_time.png'), dpi=300)
    plt.close()

def draw_load_speed():
    # 数据来源于 4.3.3 页面加载速度测试
    labels = [
        '50条联系人列表\n初次渲染',
        '主屏至设置中心\n切换',
        '主屏至联系人界面\n切换',
        '200条应用列表\n初次渲染',
        '应用热启动',
        '主屏至应用管理\n切换',
        '应用冷启动'
    ]
    times = [120, 280, 320, 350, 420, 450, 1780]
    
    fig, ax = plt.subplots(figsize=(9, 6))
    
    # === 学术图表字体缩放数学模型 (方案一) ===
    # 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
    latex_scale = 0.85           # LaTeX 中的 width=0.85\textwidth 缩放因子
    latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
    canvas_width_inch = 9.0      # Matplotlib 画布宽度
    scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例
    
    X_pdf = 12.0 * 0.8                 # 主要标题与坐标轴标签：12pt (小四)
    Y_pdf = 11.0 * 0.8                 # 轴刻度、图例与数据标注：11pt
    
    font_label_size = X_pdf / scale_factor
    font_tick_size = Y_pdf / scale_factor
    
    bars = ax.barh(labels, times, color='#50E3C2', height=0.5)
    
    ax.bar_label(bars, padding=3, fmt='%d ms', fontsize=font_tick_size)
    
    ax.axvline(x=500, color='#E74C3C', linestyle='--', alpha=0.7, label='页面切换/热启动流畅阈值 (500ms)')
    ax.axvline(x=2000, color='#F39C12', linestyle='--', alpha=0.7, label='冷启动设计目标阈值 (2000ms)')
    
    ax.set_xlabel('耗时 (毫秒)', fontsize=font_label_size, fontweight='bold')
    ax.tick_params(axis='both', labelsize=font_tick_size)
    ax.set_title('关键场景页面加载与切换速度测试结果', fontsize=font_label_size, fontweight='bold')
    ax.legend(loc='lower right', fontsize=font_tick_size)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
    plt.savefig('thesis_figures/fig4_load_speed.png', dpi=300)
    plt.savefig('thesis_figures/fig4_load_speed.pdf')
    plt.savefig(os.path.join(out_dir, 'fig4_load_speed.png'), dpi=300)
    plt.close()

if __name__ == '__main__':
    draw_response_time()
    draw_load_speed()
    print("图表已成功生成并同步至 latexpdf 目录下。")
