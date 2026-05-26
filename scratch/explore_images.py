import os
from PIL import Image

src_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu"

for img_name in ["architecture.png", "wechat_state.png", "wifi_daemon.png", "voice_flow.png"]:
    src_path = os.path.join(src_dir, img_name)
    if os.path.exists(src_path):
        img = Image.open(src_path)
        w, h = img.size
        print(f"Image: {img_name}, Size: {w}x{h}")
        # 获取非白像素包围盒
        # 如果是RGB图像，我们可以通过转为灰度图，然后阈值化来找非白包围盒
        gray = img.convert("L")
        # 寻找非255的像素边界
        bbox = gray.getbbox()
        print(f"  bbox: {bbox}")
    else:
        print(f"Image: {img_name} does not exist!")
