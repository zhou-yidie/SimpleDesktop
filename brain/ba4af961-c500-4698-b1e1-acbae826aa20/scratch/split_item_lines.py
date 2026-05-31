import re

def process_file():
    filepath = r'd:\Graduation_Project\SimpleDesktop\latexpdf\contents\chapter3.tex'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('\\iffalse')
    active_content = parts[0]
    commented_content = '\\iffalse' + '\\iffalse'.join(parts[1:]) if len(parts) > 1 else ''

    # Let's replace "（1）宿主层：宿主层是" with "（1）宿主层：\n宿主层是"
    # We want to do this for all active items
    
    # 1. Host/Bus/Plugin layers
    active_content = active_content.replace('（1）宿主层：宿主层是', '（1）宿主层：\n宿主层是')
    active_content = active_content.replace('（2）总线层：总线层是', '（2）总线层：\n总线层是')
    active_content = active_content.replace('（3）插件层：插件层承', '（3）插件层：\n插件层承')

    # 2. Subsection 适老化界面模块 (Wait, the user already did this manually!)
    
    # 3. Subsection 微信自动化直连模块
    active_content = active_content.replace('（a）模块功能概述：微信自动化直连模块是', '（a）模块功能概述：\n微信自动化直连模块是')
    active_content = active_content.replace('（b）业务流程难点分析：一键直拨方案的实现', '（b）业务流程难点分析：\n一键直拨方案的实现')

    # 4. Subsection WiFi网络守护模块
    active_content = active_content.replace('（1）模块功能概述：WiFi网络守护模块旨在', '（1）模块功能概述：\nWiFi网络守护模块旨在')
    active_content = active_content.replace('（2）前台守护服务：为实现网络状态', '（2）前台守护服务：\n为实现网络状态')
    active_content = active_content.replace('（3）跨版本WiFi自动开启：在Android 9', '（3）跨版本WiFi自动开启：\n在Android 9')
    active_content = active_content.replace('（4）断网自愈与引导面板：断网自愈策略由', '（4）断网自愈与引导面板：\n断网自愈策略由')

    # 5. Subsection 语音辅助模块
    active_content = active_content.replace('（1）模块功能概述：语音辅助模块由语音播报', '（1）模块功能概述：\n语音辅助模块由语音播报')
    active_content = active_content.replace('（2）语音播报子模块：语音播报基于', '（2）语音播报子模块：\n语音播报基于')
    active_content = active_content.replace('（3）语音指令解析子模块：语音指令解析采用', '（3）语音指令解析子模块：\n语音指令解析采用')
    active_content = active_content.replace('（4）联系人模糊匹配：在识别出打电话', '（4）联系人模糊匹配：\n在识别出打电话')

    # 6. Subsection 联系人管理模块
    active_content = active_content.replace('（a）模块功能概述：联系人管理模块为', '（a）模块功能概述：\n联系人管理模块为')
    active_content = active_content.replace('（b）联系人新增与编辑：联系人新增界面', '（b）联系人新增与编辑：\n联系人新增界面')
    active_content = active_content.replace('（c）联系人查询：联系人查询支持', '（c）联系人查询：\n联系人查询支持')
    active_content = active_content.replace('（d）联系人删除与排序：联系人删除支持', '（d）联系人删除与排序：\n联系人删除支持')
    active_content = active_content.replace('（e）联系人导出：为方便老年用户', '（e）联系人导出：\n为方便老年用户')

    new_content = active_content + commented_content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully split item headings with single newline in chapter3.tex!")

if __name__ == '__main__':
    process_file()
