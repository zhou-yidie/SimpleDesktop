import os
from PIL import Image

yuantu_path = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu\architecture.png"
current_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\architecture.png"

for name, path in [("yuantu", yuantu_path), ("current", current_path)]:
    if os.path.exists(path):
        img = Image.open(path)
        print(f"{name}: size={img.size}, mode={img.mode}")
    else:
        print(f"{name} does not exist at {path}")
