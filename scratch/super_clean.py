import os
import subprocess
import time

# 1. 强力杀死所有可能的编译引擎和中间进程
processes = ["xelatex.exe", "miktex-dvipdfmx.exe", "miktex-pdftex.exe", "bibtex.exe", "perl.exe"]
for p in processes:
    try:
        subprocess.run(["taskkill", "/F", "/IM", p, "/T"], capture_output=True)
        print(f"Taskkilled {p}")
    except Exception as e:
        print(f"Failed to kill {p}: {e}")

time.sleep(1)

# 2. 物理扫描并删除所有辅助缓存文件
pdf_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf"
extensions = [".aux", ".toc", ".out", ".log", ".blg", ".bbl", ".synctex", ".synctex(busy)", ".lof", ".lot"]

for root, dirs, files in os.walk(pdf_dir):
    for f in files:
        if any(f.endswith(ext) for ext in extensions) or f.startswith("main_new"):
            path = os.path.join(root, f)
            try:
                os.remove(path)
                print(f"Successfully deleted: {path}")
            except Exception as e:
                # 如果删除失败，我们尝试将其重命名或截断为 0 字节
                try:
                    open(path, "w").close()
                    print(f"Locked but successfully truncated: {path}")
                except Exception as e2:
                    print(f"CRITICAL: Failed to delete or truncate {path}. Error: {e2}")

print("Super clean completed!")
