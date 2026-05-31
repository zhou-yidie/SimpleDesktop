import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# 将输出目标直接配置为新版 LaTeX 论文目录
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_shake_match():
    # 图2.5：字体在原有基础上再大100% (翻倍！)，画布尺寸从 (18, 9) 扩充至 (32, 16)
    fig, ax = plt.subplots(figsize=(32, 16))
    ax.axis('off')
    
    # 步骤一：混淆隔离态
    ax.text(0.18, 0.92, "步骤一：混淆隔离态 (Ghost Nodes)", ha='center', va='center', fontsize=40, fontweight='bold')
    ax.add_patch(patches.Rectangle((0.03, 0.68), 0.30, 0.18, fc="#f2f2f2", ec="#aaaaaa", ls="dashed", lw=4.5))
    ax.text(0.18, 0.77, "透明占位节点", ha='center', va='center', fontsize=35, color="#555555", fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0.03, 0.46), 0.30, 0.18, fc="#f2f2f2", ec="#aaaaaa", ls="dashed", lw=4.5))
    ax.text(0.18, 0.55, "混淆资源 ID", ha='center', va='center', fontsize=35, color="#555555", fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0.03, 0.24), 0.30, 0.18, fc="#f2f2f2", ec="#aaaaaa", ls="dashed", lw=4.5))
    ax.text(0.18, 0.33, "隐藏真实控件", ha='center', va='center', fontsize=35, color="#555555", fontweight='bold')
    
    # 窗口内容震荡 (中间橙色框宽度设为 0.28 宽以容纳超大号文字)
    ax.add_patch(patches.FancyBboxPatch((0.36, 0.42), 0.28, 0.20, boxstyle="round,pad=0.03", fc="#fff2e6", ec="#ff8000", lw=5.5))
    ax.text(0.5, 0.52, "窗口内容震荡\n(微位移滑动 1-2px)", ha='center', va='center', fontsize=36, fontweight='bold', color="#cc6600")
    ax.annotate("", xy=(0.36, 0.52), xytext=(0.33, 0.52), arrowprops=dict(arrowstyle="->", lw=5.0, color="#cc0000", ls="dashed"))
    ax.text(0.345, 0.56, "触发更新", ha='center', va='center', fontsize=32, fontweight='bold', color="#cc0000")
    
    # 步骤二：真实树挂载
    ax.text(0.82, 0.92, "步骤二：真实树挂载与特征定位", ha='center', va='center', fontsize=40, fontweight='bold')
    ax.add_patch(patches.Rectangle((0.67, 0.68), 0.30, 0.18, fc="#e6ffe6", ec="#009900", lw=4.5))
    ax.text(0.82, 0.77, "真实控件子树暴露", ha='center', va='center', fontsize=35, fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0.67, 0.46), 0.30, 0.18, fc="#e6ffe6", ec="#009900", lw=4.5))
    ax.text(0.82, 0.55, "拓扑深度提取", ha='center', va='center', fontsize=35, fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0.67, 0.24), 0.30, 0.18, fc="#e6ffe6", ec="#009900", lw=4.5))
    ax.text(0.82, 0.33, "计算包围盒重心", ha='center', va='center', fontsize=35, fontweight='bold')
    
    ax.annotate("", xy=(0.67, 0.52), xytext=(0.64, 0.52), arrowprops=dict(arrowstyle="->", lw=5.0, color="#0066cc"))
    ax.text(0.655, 0.56, "强制重绘\n(Remount)", ha='center', va='center', fontsize=32, fontweight='bold', color="#0066cc")
    
    # 特征指纹模型
    ax.add_patch(patches.Rectangle((0.03, 0.04), 0.94, 0.14, fc="#ffffe6", ec="#cccc00", lw=5.5))
    ax.text(0.5, 0.11, "UI 特征归一化模型 (Feature Normalization)", ha='center', va='center', fontsize=36, fontweight='bold')
    formula = "匹配度 P = w1 × (相对拓扑关系) + w2 × (视觉重心偏移量) > 98%  ->  锁定目标"
    ax.text(0.5, 0.07, formula, ha='center', va='center', fontsize=32, fontweight='bold')
    
    ax.annotate("", xy=(0.5, 0.18), xytext=(0.82, 0.24), arrowprops=dict(arrowstyle="->", lw=4.0, color="black"))
    
    plt.savefig(os.path.join(out_dir, 'fig2_3_shake_match.png'), dpi=300, bbox_inches='tight')
    plt.close()

def draw_focus_retreat():
    # 图2.6：字体大150% (乘以2.5)，figsize 从 (10, 5.5) 扩充至 (18, 10.5)
    fig, ax = plt.subplots(figsize=(18, 10.5))
    ax.axis('off')
    
    # Actors (大框和字号相应增加)
    ax.add_patch(patches.Rectangle((0.06, 0.82), 0.24, 0.12, fc="#e6f2ff", ec="#0066cc", lw=2.5))
    ax.text(0.18, 0.88, "老年用户 (干扰源)", ha='center', va='center', fontsize=24, fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0.38, 0.82), 0.24, 0.12, fc="#e6f2ff", ec="#0066cc", lw=2.5))
    ax.text(0.50, 0.88, "桌面主程序", ha='center', va='center', fontsize=24, fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0.70, 0.82), 0.24, 0.12, fc="#e6f2ff", ec="#0066cc", lw=2.5))
    ax.text(0.82, 0.88, "无障碍服务引擎", ha='center', va='center', fontsize=24, fontweight='bold')
    
    # Timelines
    ax.plot([0.18, 0.18], [0.08, 0.82], color="gray", ls="--", lw=2.5)
    ax.plot([0.50, 0.50], [0.08, 0.82], color="gray", ls="--", lw=2.5)
    ax.plot([0.82, 0.82], [0.08, 0.82], color="gray", ls="--", lw=2.5)
    
    # Messages
    # 1. 自动化发起
    ax.annotate("", xy=(0.82, 0.72), xytext=(0.50, 0.72), arrowprops=dict(arrowstyle="->", lw=2.5))
    ax.text(0.66, 0.75, "1. 自动化任务发起", ha='center', va='center', fontsize=22, fontweight='bold')
    
    # 2. 焦点退避
    ax.add_patch(patches.FancyBboxPatch((0.52, 0.58), 0.16, 0.08, boxstyle="round,pad=0.015", fc="#fff2e6", ec="#ff8000", lw=2.0))
    ax.text(0.60, 0.62, "2. 释放焦点\n隐藏悬浮窗", ha='center', va='center', fontsize=20, fontweight='bold')
    ax.annotate("", xy=(0.50, 0.56), xytext=(0.50, 0.67), arrowprops=dict(arrowstyle="->", lw=2.5, color="#ff8000", connectionstyle="arc3,rad=-0.5"))
    
    # 3. 干扰
    ax.annotate("", xy=(0.82, 0.44), xytext=(0.18, 0.44), arrowprops=dict(arrowstyle="->", lw=3.0, color="#cc0000"))
    ax.text(0.50, 0.48, "3. 误触屏幕 / 系统权限弹窗干扰", ha='center', va='center', fontsize=22, color="#cc0000", fontweight='bold')
    
    # 4. 防死锁
    ax.add_patch(patches.FancyBboxPatch((0.83, 0.30), 0.15, 0.08, boxstyle="round,pad=0.015", fc="#ffe6e6", ec="#cc0000", lw=2.0))
    ax.text(0.905, 0.34, "4. 状态机停滞\n> 5秒触发死锁", ha='center', va='center', fontsize=18, color="#cc0000", fontweight='bold')
    ax.annotate("", xy=(0.82, 0.26), xytext=(0.82, 0.39), arrowprops=dict(arrowstyle="->", lw=2.5, ls="dashed", color="#cc0000", connectionstyle="arc3,rad=0.5"))
    
    # 5. 自回归
    ax.annotate("", xy=(0.50, 0.14), xytext=(0.82, 0.14), arrowprops=dict(arrowstyle="->", lw=3.0, color="#0066cc"))
    ax.text(0.66, 0.18, "5. 强制模拟返回键重置 (自回归)", ha='center', va='center', fontsize=22, color="#0066cc", fontweight='bold')
    
    plt.savefig(os.path.join(out_dir, 'fig2_4_focus_retreat.png'), dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    draw_shake_match()
    draw_focus_retreat()
    print("WeChat Shake Match (图2.5) & Focus Retreat (图2.6) 大字号图片生成成功！")
