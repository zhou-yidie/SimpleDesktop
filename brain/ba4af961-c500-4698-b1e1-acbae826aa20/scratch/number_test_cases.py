import re

def process_file():
    filepath = r'd:\Graduation_Project\SimpleDesktop\latexpdf\contents\chapter4.tex'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('\\iffalse')
    active_content = parts[0]
    commented_content = '\\iffalse' + '\\iffalse'.join(parts[1:]) if len(parts) > 1 else ''

    # We want to add numbering under each subsection.
    # Let's do exact replaces for active_content to be perfectly safe.

    # 1. 联系人管理功能测试
    active_content = active_content.replace('用例TC-CT-001：', '（1）用例TC-CT-001：')
    active_content = active_content.replace('用例TC-CT-002：', '（2）用例TC-CT-002：')
    active_content = active_content.replace('用例TC-CT-003：', '（3）用例TC-CT-003：')

    # 2. 应用管理功能测试
    active_content = active_content.replace('用例TC-AP-001：', '（1）用例TC-AP-001：')
    active_content = active_content.replace('用例TC-AP-002：', '（2）用例TC-AP-002：')
    active_content = active_content.replace('用例TC-AP-003：', '（3）用例TC-AP-003：')

    # 3. 微信一键直拨功能测试
    active_content = active_content.replace('用例TC-WX-001：', '（1）用例TC-WX-001：')
    active_content = active_content.replace('用例TC-WX-002：', '（2）用例TC-WX-002：')
    active_content = active_content.replace('用例TC-WX-003：', '（3）用例TC-WX-003：')
    active_content = active_content.replace('用例TC-WX-004：', '（4）用例TC-WX-004：')

    # 4. 网络守护功能测试
    active_content = active_content.replace('用例TC-WF-001：', '（1）用例TC-WF-001：')
    active_content = active_content.replace('用例TC-WF-002：', '（2）用例TC-WF-002：')

    # 5. 语音助手功能测试
    active_content = active_content.replace('用例TC-VC-001：', '（1）用例TC-VC-001：')
    active_content = active_content.replace('用例TC-VC-002：', '（2）用例TC-VC-002：')
    active_content = active_content.replace('用例TC-VC-003：', '（3）用例TC-VC-003：')

    # 6. 设置功能测试
    active_content = active_content.replace('用例TC-ST-001：', '（1）用例TC-ST-001：')
    active_content = active_content.replace('用例TC-ST-002：', '（2）用例TC-ST-002：')
    active_content = active_content.replace('用例TC-ST-003：', '（3）用例TC-ST-003：')

    new_content = active_content + commented_content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully numbered all active test cases in chapter4.tex!")

if __name__ == '__main__':
    process_file()
