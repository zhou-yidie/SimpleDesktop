import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"

for name in ["tech_stack.png", "wechat_state.png", "wifi_daemon.png"]:
    path = os.path.join(figures_dir, name)
    if os.path.exists(path):
        img = Image.open(path)
        print(f"{name}: size={img.size}, mode={img.mode}")
    else:
        print(f"{name} does not exist!")
