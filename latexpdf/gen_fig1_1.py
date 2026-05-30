"""
生成图 1.1：中国60岁及以上老年人口数量与占比趋势 (2010-2025)
字体规范：小四宋体（12pt SimSun）
数据来源：
  2010-2022：国家统计局历年统计公报
  2024：2024年国民经济和社会发展统计公报
  2025：2025年全国1%人口抽样调查主要数据公报（2026年5月22日发布）
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# ── 字体配置：小四宋体 = 13pt ──
FONT_SIZE = 13  # 调大以确保在PDF中极为清晰
LEGEND_FONT_SIZE = 11.5
VALUE_FONT_SIZE = 11.5

zh_fonts = ['SimSun', 'Microsoft YaHei', 'SimHei', 'KaiTi', 'FangSong']
font_found = None
for f in zh_fonts:
    if any(f.lower() in fp.name.lower() for fp in fm.fontManager.ttflist):
        font_found = f
        break

if font_found:
    plt.rcParams['font.sans-serif'] = [font_found]
    plt.rcParams['font.family'] = 'sans-serif'
else:
    plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

# 全局字号设置
plt.rcParams.update({
    'font.size': FONT_SIZE,
    'axes.labelsize': FONT_SIZE,
    'axes.titlesize': FONT_SIZE,
    'xtick.labelsize': FONT_SIZE,
    'ytick.labelsize': FONT_SIZE,
    'legend.fontsize': LEGEND_FONT_SIZE,
})

# ── 数据（全部为官方公布数据）──
years      = ['2010', '2015', '2020', '2022', '2024', '2025']
population = [1.77,   2.22,   2.64,   2.80,   3.10,   3.21]   # 亿人
percentage = [13.26,  16.15,  18.70,  19.80,  22.00,  22.86]   # %

# ── 绘图 ──
fig, ax1 = plt.subplots(figsize=(7.5, 4.6), dpi=300) # 使用更平衡的画布，让缩放后的文字大小与正文非常接近

# 学术蓝色柱状图
bar_color = '#6C8EBF'
x = np.arange(len(years))
bar_width = 0.45
bars = ax1.bar(x, population, width=bar_width, color=bar_color, alpha=0.85, zorder=2)

# 柱状图顶部标注人口数量（黑色，在柱子正上方）
for i, (xi, val) in enumerate(zip(x, population)):
    ax1.text(xi, val + 0.08, f'{val:.2f}', ha='center', va='bottom',
             fontsize=VALUE_FONT_SIZE, color='#333333', fontweight='normal')

ax1.set_xlabel('年份', fontsize=FONT_SIZE)
ax1.set_ylabel('60岁及以上人口数量（亿人）', fontsize=FONT_SIZE, color='#4A6A96')
ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=FONT_SIZE)
ax1.set_ylim(0, 4.2)
ax1.tick_params(axis='y', labelcolor='#4A6A96', labelsize=FONT_SIZE)

# 红色折线图（占比）
ax2 = ax1.twinx()
line_color = '#C0504D'
ax2.plot(x, percentage, color=line_color, marker='o', markersize=6,
         linewidth=2.2, zorder=3)

# 折线标注百分比（红色斜体，放在折线点下方，避免与柱状数字重叠）
for i, (xi, pct) in enumerate(zip(x, percentage)):
    # 前两个点放下方，后面的点放上方偏右
    if i <= 1:
        # 前两个年份：百分比放在折线点的正下方
        ax2.text(xi, pct - 1.1, f'{pct:.2f}%', ha='center', va='top',
                 fontsize=VALUE_FONT_SIZE, color=line_color, fontstyle='italic')
    else:
        # 后面的年份：百分比放在折线点的左下方，避免与柱顶数字碰撞
        ax2.text(xi - 0.22, pct - 0.3, f'{pct:.2f}%', ha='right', va='top',
                 fontsize=VALUE_FONT_SIZE, color=line_color, fontstyle='italic')

ax2.set_ylabel('占全国总人口比例（%）', fontsize=FONT_SIZE, color=line_color)
ax2.set_ylim(10, 27)
ax2.tick_params(axis='y', labelcolor=line_color, labelsize=FONT_SIZE)

# 图例
lines_legend = [
    plt.Rectangle((0, 0), 1, 1, fc=bar_color, alpha=0.85),
    plt.Line2D([0], [0], color=line_color, marker='o', markersize=6, linewidth=2)
]
ax1.legend(lines_legend, ['人口数量（亿）', '人口占比（%）'],
           loc='upper left', fontsize=LEGEND_FONT_SIZE, framealpha=0.9)

# 网格
ax1.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
ax1.set_axisbelow(True)

plt.tight_layout()

# 保存
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures', 'fig1_1_aging_population_trend.png')
fig.savefig(out_path, bbox_inches='tight', pad_inches=0.15)
print(f'图表已保存至: {out_path}')
plt.close()
