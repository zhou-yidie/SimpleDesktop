import matplotlib.pyplot as plt
import numpy as np
import os

out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures"
os.makedirs(out_dir, exist_ok=True)

# 设置 Windows 下的兼容中文字体，优先黑体，其次微软雅黑、宋体
plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

print("开始生成图1.1: 中国60岁及以上老年人口数量与占比趋势图...")
# --- Figure 1.1 ---
years = ['2010', '2015', '2020', '2022', '2024', '2025\n(预测)']
pop = [1.77, 2.22, 2.64, 2.80, 3.10, 3.23]
pct = [13.26, 16.15, 18.70, 19.80, 22.00, 23.00]

fig, ax1 = plt.subplots(figsize=(12, 7.5))

# === 学术图表字体缩放数学模型 (方案一) ===
# 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
latex_scale = 0.85           # LaTeX 中的 width=0.85\textwidth 缩放因子
latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
canvas_width_inch = 12.0     # Matplotlib 画布宽度
scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例

X_pdf = 12.0 * 0.8                 # 主要轴标签与图例文字：12pt (小四)
Y_pdf = 11.0 * 0.8                 # 轴刻度与数据标签文字：11pt

font_label_size = X_pdf / scale_factor
font_tick_size = Y_pdf / scale_factor
font_value_size = Y_pdf / scale_factor

color1 = '#4C72B0' # 稳重的学术蓝
ax1.set_xlabel('年份', fontsize=font_label_size, fontweight='bold', labelpad=15)
ax1.set_ylabel('60岁及以上人口数量 (亿人)', color=color1, fontsize=font_label_size, fontweight='bold', labelpad=15)
bars = ax1.bar(years, pop, color=color1, alpha=0.8, width=0.45, label='人口数量 (亿)')
ax1.tick_params(axis='y', labelcolor=color1, labelsize=font_tick_size)
ax1.tick_params(axis='x', labelsize=font_tick_size)
ax1.set_ylim(0, 4.0)

# 在柱状图上方添加数值标签
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.08, f'{yval}', ha='center', va='bottom', color=color1, fontsize=font_value_size, fontweight='bold')

ax2 = ax1.twinx()
color2 = '#C44E52' # 学术红
ax2.set_ylabel('占全国总人口比例 (%)', color=color2, fontsize=font_label_size, fontweight='bold', labelpad=15)
line = ax2.plot(years, pct, color=color2, marker='o', linewidth=3.5, markersize=10, label='人口占比 (%)')
ax2.tick_params(axis='y', labelcolor=color2, labelsize=font_tick_size)
ax2.set_ylim(10, 26)

# 在折线图上方添加数值标签
for i, txt in enumerate(pct):
    ax2.text(years[i], pct[i] + 0.8, f'{txt}%', ha='center', va='bottom', color=color2, fontsize=font_value_size, fontweight='bold')

# 已删除图片内部多余的顶部标题，以符合 LaTeX 学术规范
ax1.grid(axis='y', linestyle='--', alpha=0.4)
fig.tight_layout()

# 合并图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=font_tick_size)

# 保存为 PDF 和 PNG (输出到原目录与 thesis/figures 目录)
thesis_fig_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(thesis_fig_dir, exist_ok=True)

plt.savefig(os.path.join(out_dir, 'fig1_1_aging_population_trend.pdf'), format='pdf', dpi=600, bbox_inches='tight')
plt.savefig(os.path.join(out_dir, 'fig1_1_aging_population_trend.png'), format='png', dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(thesis_fig_dir, 'fig1_1_aging_population_trend.png'), format='png', dpi=300, bbox_inches='tight')
plt.close()
print("图1.1 生成完成！")


print("开始生成图1.2: 老年人智能手机使用核心痛点分布图...")
# --- Figure 1.2 ---
pain_points = [
    '需要他人指导\n才能掌握新功能',
    '复杂广告及\n无意跳转困扰',
    '视觉障碍\n(字体/图标太小)',
    '操作步骤过于复杂',
    '害怕遭遇网络诈骗'
]
percentages = [77.0, 68.8, 67.5, 63.3, 47.0]

fig, ax = plt.subplots(figsize=(14, 8))
y_pos = np.arange(len(pain_points))

# === 学术图表字体缩放数学模型 (方案一) ===
# 目标：使 PDF 中最终呈现的字体大小与 LaTeX 正文 (12pt 小四) 完美一致！
latex_scale = 0.85           # LaTeX 中的 width=0.85\textwidth 缩放因子
latex_textwidth_inch = 6.3   # xuptThesis 中的 A4 页面排版宽度 16cm 约合 6.3 英寸
canvas_width_inch = 14.0     # Matplotlib 画布宽度
scale_factor = (latex_textwidth_inch * latex_scale) / canvas_width_inch  # 物理缩放比例

X_pdf = 12.0 * 0.8                 # 主要轴标签文字：12pt (小四)
Y_pdf = 11.0 * 0.8                 # 轴刻度与数值标签文字：11pt

font_label_size = X_pdf / scale_factor
font_tick_size = Y_pdf / scale_factor
font_value_size = Y_pdf / scale_factor

# 翻转数组使得比例最高的在最上方
pain_points = pain_points[::-1]
percentages = percentages[::-1]

# 使用渐变/不同的颜色增强学术感
colors = ['#55A868', '#EAE509', '#DD8452', '#C44E52', '#8172B3']
bars = ax.barh(y_pos, percentages, color='#DD8452', alpha=0.85, height=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(pain_points, fontsize=font_tick_size, fontweight='bold')
ax.set_xlabel('占受访老年群体比例 (%)', fontsize=font_label_size, fontweight='bold', labelpad=15)
# 已删除图片内部多余的顶部标题，以符合 LaTeX 学术规范
ax.set_xlim(0, 100)
ax.tick_params(axis='x', labelsize=font_tick_size)
ax.xaxis.grid(True, linestyle='--', alpha=0.5)

# 添加数值标签
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1.5, bar.get_y() + bar.get_height()/2, f'{width}%', ha='left', va='center', fontsize=font_value_size, fontweight='bold')

# 去除右侧和上侧的边框线
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
thesis_fig_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"

plt.savefig(os.path.join(out_dir, 'fig1_2_usage_pain_points.pdf'), format='pdf', dpi=600, bbox_inches='tight')
plt.savefig(os.path.join(out_dir, 'fig1_2_usage_pain_points.png'), format='png', dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(thesis_fig_dir, 'fig1_2_usage_pain_points.png'), format='png', dpi=300, bbox_inches='tight')
plt.close()
print("图1.2 生成完成！")

# --- 图1.3和1.4 的 TikZ 源码生成 ---
print("正在生成图1.3和1.4的 LaTeX TikZ 源码文件...")
tikz_fig1_3 = r"""\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    node distance=2cm,
    box/.style={draw, rectangle, rounded corners, minimum width=3cm, minimum height=1cm, text centered, font=\sffamily\small},
    arrow/.style={thick,->,>=stealth}
]

% 传统方案
\node[box, fill=gray!20] (trad_launcher) {传统极简桌面 (大字体)};
\node[box, fill=red!20, right of=trad_launcher, xshift=3.5cm] (trad_wechat) {微信原生界面 (极其复杂)};
\draw[arrow, dashed] (trad_launcher) -- node[above] {点击跳转} node[below] {\textcolor{red}{体验割裂}} (trad_wechat);

% 本课题方案
\node[box, fill=blue!20, below of=trad_launcher, yshift=-1cm] (our_launcher) {SimpleDesktop 适老桌面};
\node[box, fill=green!20, right of=our_launcher, xshift=3.5cm] (our_wechat) {微信视频通话 (直达)};
\draw[arrow, thick, blue] (our_launcher) -- node[above] {无障碍 FSM 引擎} node[below] {全自动跨应用流转} (our_wechat);

\end{tikzpicture}
\caption{传统适老化桌面与本系统自动化直达通道的体验对比}
\label{fig:arch_compare}
\end{figure}
"""

with open(os.path.join(out_dir, 'fig1_3_architecture_compare.tex'), 'w', encoding='utf-8') as f:
    f.write(tikz_fig1_3)

tikz_fig1_4 = r"""\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    layer/.style={draw, rectangle, minimum width=8cm, minimum height=1.2cm, text centered, font=\sffamily\bfseries},
    module/.style={draw, rectangle, rounded corners, fill=white, minimum width=2.2cm, minimum height=0.8cm, text centered, font=\sffamily\small}
]

% 基础守护层
\node[layer, fill=gray!10] (layer1) {};
\node[above left, xshift=0.2cm, yshift=-0.4cm] at (layer1.north east) {底层守护层};
\node[module, xshift=-2.5cm] at (layer1.center) {网络自愈卫士};
\node[module, xshift=0cm] at (layer1.center) {微内核插件引擎};
\node[module, xshift=2.5cm] at (layer1.center) {无障碍事件调度};

% 业务逻辑层
\node[layer, fill=blue!10, above of=layer1, yshift=0.5cm] (layer2) {};
\node[above left, xshift=0.2cm, yshift=-0.4cm] at (layer2.north east) {业务核心层};
\node[module, xshift=-2.5cm] at (layer2.center) {联系人解析(Room)};
\node[module, xshift=0cm] at (layer2.center) {微信7态状态机};
\node[module, xshift=2.5cm] at (layer2.center) {语音语义解析(NLP)};

% 交互展示层
\node[layer, fill=orange!10, above of=layer2, yshift=0.5cm] (layer3) {};
\node[above left, xshift=0.2cm, yshift=-0.4cm] at (layer3.north east) {表现交互层};
\node[module, xshift=-2cm] at (layer3.center) {Compose 极简UI};
\node[module, xshift=2cm] at (layer3.center) {动态高对比度引擎};

% 连接线
\draw[->, thick, dashed] (layer1.north) -- (layer2.south);
\draw[->, thick, dashed] (layer2.north) -- (layer3.south);

\end{tikzpicture}
\caption{SimpleDesktop 系统技术全景架构图}
\label{fig:system_overview}
\end{figure}
"""
with open(os.path.join(out_dir, 'fig1_4_system_overview.tex'), 'w', encoding='utf-8') as f:
    f.write(tikz_fig1_4)

print("全部生成任务圆满完成！")
