import os
import shutil

pdf_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf"

# 1. 物理删除 build 文件夹
build_dir = os.path.join(pdf_dir, "build")
if os.path.exists(build_dir):
    try:
        shutil.rmtree(build_dir)
        print("Successfully removed build directory!")
    except Exception as e:
        print(f"Failed to remove build directory: {e}")

# 2. 物理清除所有临时缓存文件
extensions = [".aux", ".toc", ".out", ".log", ".blg", ".bbl", ".synctex", ".synctex(busy)", ".lof", ".lot"]
for root, dirs, files in os.walk(pdf_dir):
    for f in files:
        if any(f.endswith(ext) for ext in extensions) or f.startswith("main_new"):
            path = os.path.join(root, f)
            try:
                os.remove(path)
                print(f"Purged: {path}")
            except Exception as e:
                print(f"Could not remove {path}: {e}")

print("All temporary build files and directory purges complete!")
