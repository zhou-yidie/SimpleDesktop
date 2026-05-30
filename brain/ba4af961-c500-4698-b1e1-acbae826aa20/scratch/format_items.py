import re

def process_file():
    filepath = r'd:\Graduation_Project\SimpleDesktop\latexpdf\contents\chapter3.tex'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split active content from commented out block (if \iffalse exists)
    parts = content.split('\\iffalse')
    active_content = parts[0]
    commented_content = '\\iffalse' + '\\iffalse'.join(parts[1:]) if len(parts) > 1 else ''

    # Let's perform precise regex replacements on active_content
    # Find patterns like (1) 宿主层 \n\n 宿主层是整个系统...
    # We want to change them to (1) 宿主层：宿主层是整个系统...
    
    # 1. Host/Bus/Plugin layers (lines 49-68 approx)
    # Target:
    # （1）宿主层
    # 
    # 宿主层是整个系统...
    active_content = re.sub(
        r'（1）宿主层\s*\n\s*\n\s*宿主层是',
        '（1）宿主层：宿主层是',
        active_content
    )
    active_content = re.sub(
        r'（2）总线层\s*\n\s*\n\s*总线层是',
        '（2）总线层：总线层是',
        active_content
    )
    active_content = re.sub(
        r'（3）插件层\s*\n\s*\n\s*插件层承',
        '（3）插件层：插件层承',
        active_content
    )

    # 2. Subsection 适老化界面模块 (lines 122-139 approx)
    active_content = re.sub(
        r'（1）模块功能概述\s*\n\s*\n\s*适老化界面模块负责',
        '（1）模块功能概述：适老化界面模块负责',
        active_content
    )
    active_content = re.sub(
        r'（2）主屏聚合面板设计\s*\n\s*\n\s*主屏作为老年用户',
        '（2）主屏聚合面板设计：主屏作为老年用户',
        active_content
    )
    active_content = re.sub(
        r'（3）字号与主题动态切换\s*\n\s*\n\s*考虑到不同老年用户',
        '（3）字号与主题动态切换：考虑到不同老年用户',
        active_content
    )
    active_content = re.sub(
        r'（4）实现要点\s*\n\s*\n\s*适老化界面模块基于',
        '（4）实现要点：适老化界面模块基于',
        active_content
    )

    # 3. Subsection 微信自动化直连模块 (lines 142-192 approx)
    active_content = re.sub(
        r'（a）模块功能概述\s*\n\s*\n\s*微信自动化直连模块是',
        '（a）模块功能概述：微信自动化直连模块是',
        active_content
    )
    active_content = re.sub(
        r'（b）业务流程难点分析\s*\n\s*\n\s*一键直拨方案的实现',
        '（b）业务流程难点分析：一键直拨方案的实现',
        active_content
    )

    # 4. Subsection WiFi网络守护模块 (lines 240-264 approx)
    active_content = re.sub(
        r'（1）模块功能概述\s*\n\s*\n\s*WiFi网络守护模块旨在',
        '（1）模块功能概述：WiFi网络守护模块旨在',
        active_content
    )
    active_content = re.sub(
        r'（2）前台守护服务\s*\n\s*\n\s*为实现网络状态',
        '（2）前台守护服务：为实现网络状态',
        active_content
    )
    active_content = re.sub(
        r'（3）跨版本WiFi自动开启\s*\n\s*\n\s*在Android 9',
        '（3）跨版本WiFi自动开启：在Android 9',
        active_content
    )
    active_content = re.sub(
        r'（4）断网自愈与引导面板\s*\n\s*\n\s*断网自愈策略由',
        '（4）断网自愈与引导面板：断网自愈策略由',
        active_content
    )

    # 5. Subsection 语音辅助模块 (lines 267-285 approx)
    # Wait, line 267 had no newline in source code but let's make it inline with colon as well
    active_content = re.sub(
        r'（1）模块功能概述\s*\n\s*语音辅助模块由语音播报',
        '（1）模块功能概述：语音辅助模块由语音播报',
        active_content
    )
    active_content = re.sub(
        r'（2）语音播报子模块\s*\n\s*\n\s*语音播报基于',
        '（2）语音播报子模块：语音播报基于',
        active_content
    )
    active_content = re.sub(
        r'（3）语音指令解析子模块\s*\n\s*\n\s*语音指令解析采用',
        '（3）语音指令解析子模块：语音指令解析采用',
        active_content
    )
    active_content = re.sub(
        r'（4）联系人模糊匹配\s*\n\s*\n\s*在识别出打电话',
        '（4）联系人模糊匹配：在识别出打电话',
        active_content
    )

    # 6. Subsection 联系人管理模块 (lines 294-317 approx)
    active_content = re.sub(
        r'（a）模块功能概述\s*\n\s*\n\s*联系人管理模块为',
        '（a）模块功能概述：联系人管理模块为',
        active_content
    )
    active_content = re.sub(
        r'（b）联系人新增与编辑\s*\n\s*\n\s*联系人新增界面',
        '（b）联系人新增与编辑：联系人新增界面',
        active_content
    )
    active_content = re.sub(
        r'（c）联系人查询\s*\n\s*\n\s*联系人查询支持',
        '（c）联系人查询：联系人查询支持',
        active_content
    )
    active_content = re.sub(
        r'（d）联系人删除与排序\s*\n\s*\n\s*联系人删除支持',
        '（d）联系人删除与排序：联系人删除支持',
        active_content
    )
    active_content = re.sub(
        r'（e）联系人导出\s*\n\s*\n\s*为方便老年用户',
        '（e）联系人导出：为方便老年用户',
        active_content
    )

    new_content = active_content + commented_content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully formatted all active item lists in chapter3.tex!")

if __name__ == '__main__':
    process_file()
