import re
import os

contents_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\contents"
chapters = ["chapter1.tex", "chapter2.tex", "chapter3.tex", "chapter4.tex", "chapter5.tex"]

report = []

def log_issue(chapter, line_no, issue_type, line_content, detail):
    report.append({
        "chapter": chapter,
        "line": line_no,
        "type": issue_type,
        "content": line_content.strip(),
        "detail": detail
    })

for chap in chapters:
    file_path = os.path.join(contents_dir, chap)
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    in_verbatim = False
    in_comment = False
    
    for idx, line in enumerate(lines):
        line_no = idx + 1
        stripped = line.strip()
        
        # Track block environments that might contain raw text/code
        if "\\begin{verbatim}" in line or "\\begin{lstlisting}" in line:
            in_verbatim = True
            continue
        if "\\end{verbatim}" in line or "\\end{lstlisting}" in line:
            in_verbatim = False
            continue
            
        # Ignore comments or code environments
        if stripped.startswith("%") and not stripped.startswith("% \\"):
            continue
            
        if in_verbatim:
            continue
            
        # 1. Check for raw double quotes "..."
        # In LaTeX, raw "..." can lead to backward quotes on the left.
        # It's better to use `` and '' for quotes, or Chinese “” for Chinese text.
        if '"' in line:
            # Check if it's an image name or path or standard macro option
            if not any(x in line for x in ["width=", "height=", "scale=", "\\includegraphics", "\\subfigure"]):
                log_issue(chap, line_no, "Raw Quote", line, "检测到直双引号 '\"'，建议中文使用 ‘和’/“和”，英文使用 `` 和 ''")
                
        # 2. Check for Chinese punctuation mixed in math/code macros
        if "\\texttt{" in line or "\\upcite{" in line or "\\ref{" in line:
            # extract content inside macros
            matches = re.findall(r"\\[a-zA-Z]+\{([^{}]+)\}", line)
            for match in matches:
                if any(cp in match for cp in ["，", "。", "（", "）", "：", "；", "！"]):
                    log_issue(chap, line_no, "Macro Punctuation Mix", line, f"在 LaTeX 宏定义包中检测到中文标点符号: '{match}'")
                    
        # 3. Check for empty or broken citations
        if "\\upcite{}" in line or "\\cite{}" in line:
            log_issue(chap, line_no, "Empty Citation", line, "检测到空的文献引用 \\upcite{} 或 \\cite{}")
            
        # 4. Check for hardcoded footnotesize or small inside main body text
        # (excluding tables and figures which are allowed, but even tables are styled by xuptThesis.cls)
        if any(fs in line for fs in ["\\footnotesize", "\\scriptsize", "\\tiny"]) and not ("\\begin{table}" in line or "\\begin{figure}" in line):
            # Check if this is within a table/figure context by checking previous lines (approximate)
            log_issue(chap, line_no, "Hardcoded Font Size", line, "检测到正文中使用了硬编码的字号指令 (如 \\footnotesize)，可能会破坏模板一致性")
            
        # 5. Check for TODO or placeholder text
        if any(ph in line.upper() for ph in ["TODO", "XXX", "待定", "暂缺"]):
            log_issue(chap, line_no, "Placeholder Text", line, "检测到 TODO 或待定占位符")
            
        # 6. Check for unescaped special characters
        # For example, unescaped & inside normal text
        if "&" in line:
            # Tables and matrices use &, so exclude them
            if not any(x in line for x in ["\\begin{tabular", "\\end{tabular", "\\begin{matrix", "\\begin{array", "\\begin{table", "grid"]):
                # check if there is an unescaped &
                # (preceded by backslash is escaped: \&)
                escaped_amp = re.findall(r"(?<!\\)&", line)
                if escaped_amp:
                    # check if this line is part of a table or list
                    log_issue(chap, line_no, "Unescaped Ampersand", line, "检测到未转义的字符 '&'，在 LaTeX 正文中必须使用 '\\&'")
                    
        # 7. Check for consecutive Chinese punctuation typos (like "。。" or "，，")
        if "。。" in line:
            log_issue(chap, line_no, "Punctuation Typo", line, "检测到连续重复的中文句号 '。。'")
        if "，，" in line:
            log_issue(chap, line_no, "Punctuation Typo", line, "检测到连续重复的中文逗号 '，，'")
        if "、，" in line or "，、" in line:
            log_issue(chap, line_no, "Punctuation Typo", line, "检测到顿号和逗号连用")

print(f"Audit completed. Found {len(report)} issues.")
# Save report to a text file for review
report_path = r"C:\Users\22613\.gemini\antigravity\brain\ba4af961-c500-4698-b1e1-acbae826aa20\audit_report.txt"
with open(report_path, "w", encoding="utf-8") as rf:
    rf.write("==================================================\n")
    rf.write("               THESIS AUDIT REPORT                \n")
    rf.write("==================================================\n\n")
    for item in report:
        rf.write(f"[{item['chapter']} - Line {item['line']}] [{item['type']}]\n")
        rf.write(f"Detail: {item['detail']}\n")
        rf.write(f"Line:   {item['content']}\n")
        rf.write("-" * 50 + "\n")

print(f"Audit report saved to {report_path}")
