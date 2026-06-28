import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# out_dir：编译后图表保存的目标物理路径目录
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# plt.rcParams：配置全局中文字体为仿宋（FangSong），确保学术风格一致
plt.rcParams['font.sans-serif'] = ['FangSong', 'SimSun', 'Songti SC', 'STSong', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False 

def draw_wechat_state_machine():
    # 画布高收紧为 6.6 英寸，宽拓宽为 20.0 英寸，为大字号组件拓宽提供充足空间
    fig, ax = plt.subplots(figsize=(20.0, 6.6), dpi=300)
    ax.axis('off')
    
    ax.set_xlim(0, 20.0)
    ax.set_ylim(0.4, 6.8)
    ax.set_aspect('equal')
    
    # 统一字体大小为原来的 1.5 倍 (22.5pt)
    font_size = 22.5
    
    # =============================================================
    # 1. 绘制左侧 3x3 蛇形流主干状态框 (中点平移至 X1=2.8, X2=8.4, X3=14.0, 框宽为 5.2)
    # =============================================================
    # 1.1 Start 框 (框宽 5.2，高度拉升至 1.3，Y轴范围 [5.1, 6.4])
    ax.add_patch(patches.FancyBboxPatch(
        (0.2, 5.1), 5.2, 1.3, boxstyle="round,pad=0.0,rounding_size=0.04",
        fc="#f2f2f2", ec="#595959", lw=2.0, zorder=2
    ))
    ax.text(2.8, 6.08, "开始状态机 (Start)", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#000000")
    ax.text(2.8, 5.75, "用户点击联系人卡片", ha='center', va='center', fontsize=font_size, color="#333333")
    ax.text(2.8, 5.42, "(User taps contact)", ha='center', va='center', fontsize=font_size, color="#333333")
 
    # 1.2 阶段 1 至 阶段 7 框 (各框高 1.4, 宽 5.2, 范围: Y轴分 [5.0, 6.4], [2.8, 4.2], [0.6, 2.0])
    stages = {
        "s1": {"pos": (5.8, 5.0), "title": "阶段1: 微信主界面就位", "desc": "Index=1: 确认进入微信首页", "sub": "点击底部第一个Tab"},
        "s2": {"pos": (11.4, 5.0), "title": "阶段2: 搜索入口触发", "desc": "Index=2: 点击右上角搜索图标", "sub": ""},
        "s3": {"pos": (11.4, 2.8), "title": "阶段3: 联系人姓名输入", "desc": "Index=3: 输入目标微信昵称", "sub": ""},
        "s4": {"pos": (5.8, 2.8), "title": "阶段4: 搜索结果确认", "desc": "Index=4: 点击第一条搜索结果", "sub": ""},
        "s5": {"pos": (0.2, 2.8), "title": "阶段5: 聊天功能展开", "desc": "Index=5: 点击右下角\"+\"", "sub": "展开功能栏"},
        "s6": {"pos": (0.2, 0.6), "title": "阶段6: 通话选项选择", "desc": "Index=6: 定位\"视频通话\"", "sub": "模拟手势点击"},
        "s7": {"pos": (5.8, 0.6), "title": "阶段7: 通话类型确认", "desc": "Index=7: 弹窗中选择", "sub": "视频/语音通话"}
    }
 
    for key, val in stages.items():
        x, y = val["pos"]
        ax.add_patch(patches.FancyBboxPatch(
            (x, y), 5.2, 1.4, boxstyle="round,pad=0.0,rounding_size=0.04",
            fc="#ddebf7", ec="#2f5597", lw=2.0, zorder=2
        ))
        
        # 重构大字号多行行距，间距设为 0.35-0.36，完全消除字体重合
        if val["sub"]:
            ax.text(x + 2.6, y + 1.05, val["title"], ha='center', va='center', fontsize=font_size, fontweight='bold', color="#000000")
            ax.text(x + 2.6, y + 0.70, val["desc"], ha='center', va='center', fontsize=font_size, color="#333333")
            ax.text(x + 2.6, y + 0.35, val["sub"], ha='center', va='center', fontsize=font_size, color="#333333")
        else:
            ax.text(x + 2.6, y + 0.88, val["title"], ha='center', va='center', fontsize=font_size, fontweight='bold', color="#000000")
            ax.text(x + 2.6, y + 0.52, val["desc"], ha='center', va='center', fontsize=font_size, color="#333333")
 
    # 1.3 End 框 (框宽 5.2, 高度拉升至 1.3，Y轴范围 [0.75, 2.05])
    ax.add_patch(patches.FancyBboxPatch(
        (11.4, 0.75), 5.2, 1.3, boxstyle="round,pad=0.0,rounding_size=0.04",
        fc="#e2f0d9", ec="#375623", lw=2.0, zorder=2
    ))
    ax.text(14.0, 1.73, "状态机重置 (End)", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#000000")
    ax.text(14.0, 1.40, "进入视频通话界面", ha='center', va='center', fontsize=font_size, color="#333333")
    ax.text(14.0, 1.07, "状态机重置 Index=0", ha='center', va='center', fontsize=font_size, color="#333333")
 
    # =============================================================
    # 2. 绘制蛇形流程实线连接箭头 (深蓝色, lw=2.2，精确指向组件中线 Y)
    # =============================================================
    # 第一排向右：Start -> s1 -> s2 (Y中线对齐 5.70)
    ax.annotate("", xy=(5.78, 5.7), xytext=(5.42, 5.7), arrowprops=dict(arrowstyle="-|>", color="#2f5597", lw=2.2, mutation_scale=15), zorder=3)
    ax.annotate("", xy=(11.38, 5.7), xytext=(11.02, 5.7), arrowprops=dict(arrowstyle="-|>", color="#2f5597", lw=2.2, mutation_scale=15), zorder=3)
    
    # 拐弯向下：s2 -> s3 (自 14.0, 4.98 下降到 14.0, 4.22)
    ax.annotate("", xy=(14.0, 4.22), xytext=(14.0, 4.98), arrowprops=dict(arrowstyle="-|>", color="#2f5597", lw=2.2, mutation_scale=15), zorder=3)
    
    # 第二排向左：s3 -> s4 -> s5 (Y中线对齐 3.50)
    ax.annotate("", xy=(11.02, 3.5), xytext=(11.38, 3.5), arrowprops=dict(arrowstyle="-|>", color="#2f5597", lw=2.2, mutation_scale=15), zorder=3)
    ax.annotate("", xy=(5.42, 3.5), xytext=(5.78, 3.5), arrowprops=dict(arrowstyle="-|>", color="#2f5597", lw=2.2, mutation_scale=15), zorder=3)
    
    # 拐弯向下：s5 -> s6 (自 2.8, 2.78 下降到 2.8, 2.02)
    ax.annotate("", xy=(2.8, 2.02), xytext=(2.8, 2.78), arrowprops=dict(arrowstyle="-|>", color="#2f5597", lw=2.2, mutation_scale=15), zorder=3)
    
    # 第三排向右：s6 -> s7 -> End (Y中线对齐 1.32)
    ax.annotate("", xy=(5.78, 1.32), xytext=(5.42, 1.32), arrowprops=dict(arrowstyle="-|>", color="#2f5597", lw=2.2, mutation_scale=15), zorder=3)
    ax.annotate("", xy=(11.38, 1.32), xytext=(11.02, 1.32), arrowprops=dict(arrowstyle="-|>", color="#2f5597", lw=2.2, mutation_scale=15), zorder=3)
 
    # =============================================================
    # 3. 绘制右侧独立退避守护层 (Focus Retreat Guard, 新中轴 X_center=18.4)
    # =============================================================
    # 3.1 外部红色虚线大保护外壳
    ax.add_patch(patches.FancyBboxPatch(
        (17.0, 0.6), 2.8, 6.0, boxstyle="round,pad=0.0,rounding_size=0.04",
        fc="#fffbfa", ec="#c00000", lw=1.8, linestyle="--", zorder=1
    ))
    # 守护层大字标题
    ax.text(18.4, 6.36, "异常退避守护", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#c00000")
    ax.text(18.4, 6.08, "(Retreat Guard)", ha='center', va='center', fontsize=font_size, color="#cc3333")
 
    # 3.2 焦点冲突检测判定框 (白色底，高 1.1)
    ax.add_patch(patches.FancyBboxPatch(
        (17.075, 4.5), 2.65, 1.1, boxstyle="round,pad=0.0,rounding_size=0.04",
        fc="#ffffff", ec="#595959", lw=1.8, zorder=2
    ))
    ax.text(18.4, 5.22, "焦点冲突检测", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#000000")
    ax.text(18.4, 4.88, "(Dialog Detect)", ha='center', va='center', fontsize=font_size, color="#333333")
 
    # 3.3 系统退避重试策略框 (由于字数加多，高度从 1.1 增加到 1.35，Y轴范围 [1.45, 2.8])
    ax.add_patch(patches.FancyBboxPatch(
        (17.075, 1.45), 2.65, 1.35, boxstyle="round,pad=0.0,rounding_size=0.04",
        fc="#ffffff", ec="#595959", lw=1.8, zorder=2
    ))
    # “主动返回关闭弹窗”拆分成两行以防溢出
    ax.text(18.4, 2.48, "系统退避策略", ha='center', va='center', fontsize=font_size, fontweight='bold', color="#000000")
    ax.text(18.4, 2.12, "主动返回", ha='center', va='center', fontsize=font_size, color="#333333")
    ax.text(18.4, 1.78, "关闭弹窗", ha='center', va='center', fontsize=font_size, color="#333333")
 
    # 3.4 守护层内垂直指示线 (自 4.48 指向 2.82)
    ax.annotate("", xy=(18.4, 2.82), xytext=(18.4, 4.48), arrowprops=dict(arrowstyle="-|>", color="#c00000", ls="--", lw=1.6, mutation_scale=12), zorder=3)
 
    # =============================================================
    # 4. 绘制状态机主干与右侧守护层之间的异常触发连线
    # =============================================================
    # 4.1 触发异常回路
    ax.annotate("", xy=(17.05, 5.05), xytext=(16.6, 3.5), arrowprops=dict(arrowstyle="-|>", color="#c00000", ls="--", lw=1.6, mutation_scale=12), zorder=3)
    ax.text(16.8, 4.45, "触发异常", ha='center', va='center', fontsize=font_size, color="#c00000", rotation=70, fontweight='bold')
 
    # 保存图片
    save_path = os.path.join(out_dir, "wechat_state.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.savefig(os.path.join(out_dir, "wechat_state.pdf"), dpi=300, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print(f"Successfully generated clean snaking wechat_state.png and .pdf to {save_path}!")

if __name__ == "__main__":
    draw_wechat_state_machine()
