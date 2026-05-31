import os

ch2_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\contents\chapter2.tex"

if os.path.exists(ch2_path):
    with open(ch2_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 截取前 162 行（1-indexed 即 0 到 162 索引）
    # 在 lines[162] 开始是 \iffalse, 我们只需要保留 lines[0] 到 lines[161] (也就是前 161 行，加上一个结尾空行)
    clean_lines = lines[:161]
    
    with open(ch2_path, "w", encoding="utf-8") as f:
        f.writelines(clean_lines)
    print(f"Successfully truncated chapter2.tex to first 161 lines. Total lines now: {len(clean_lines)}")
else:
    print(f"Error: {ch2_path} not found!")
