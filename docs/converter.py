import re
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def set_font_style(run, font_name="宋体", size=12):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size)

def convert_md_to_docx(md_path, docx_path):
    doc = Document()
    
    # 全局样式设置：首行缩进与行间距（简单设置）
    # 这里我们直接按行解析
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 处理标题
        if line.startswith('# '):
            p = doc.add_heading(line[2:], level=0)
        elif line.startswith('## '):
            p = doc.add_heading(line[3:], level=1)
        elif line.startswith('### '):
            p = doc.add_heading(line[4:], level=2)
        elif line.startswith('#### '):
            p = doc.add_heading(line[5:], level=3)
        elif line.startswith('- ') or line.startswith('* '):
            p = doc.add_paragraph(line[2:], style='List Bullet')
        elif line.startswith('|') and '|' in line:
            # 简单表格处理（只取文字，不画真实表格，因为MD表格解析较复杂）
            p = doc.add_paragraph(line.strip('|').replace('|', ' | '))
        else:
            # 普通正文
            # 处理加粗 (这里只是简单字符串过滤)
            clean_text = line.replace('**', '').replace('__', '')
            p = doc.add_paragraph(clean_text)
            
        # 为段落中的所有 runs 设置字体（中文支持）
        for run in p.runs:
            set_font_style(run)

    doc.save(docx_path)
    print(f"Conversion complete: {docx_path}")

if __name__ == "__main__":
    convert_md_to_docx(r'd:\Graduation_Project\SimpleDesktop\docs\THESIS_FULL_V2.md', r'd:\Graduation_Project\SimpleDesktop\docs\THESIS_V2_40K.docx')
