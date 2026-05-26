import os
from PIL import Image

out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)
src_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu"

def crop_precise(img_name, top_y, bottom_y, border_px=4):
    src_path = os.path.join(src_dir, img_name)
    dst_path = os.path.join(out_dir, img_name)
    
    if not os.path.exists(src_path):
        print(f"Error: source path {src_path} does not exist!")
        return

    try:
        img = Image.open(src_path)
        w, h = img.size
        
        # 剥离外围边框
        left_x = border_px
        right_x = w - border_px
        
        cropped_img = img.crop((left_x, top_y, right_x, bottom_y))
        
        # 四周增补 20 像素的纯白留白
        padding = 20
        cw, ch = cropped_img.size
        new_img = Image.new("RGB", (cw + padding * 2, ch + padding * 2), "white")
        new_img.paste(cropped_img, (padding, padding))
        
        new_img.save(dst_path, "PNG", dpi=(300, 300))
        print(f"Saved precise crop: {img_name} [y: {top_y} to {bottom_y}] -> {dst_path}")
        
    except Exception as e:
        print(f"Failed to process {img_name}: {e}")

# 1. 图 3.1 architecture.png: 顶部汉字只占 y<80, 绿色方框在 y>=80 开始；底部空白在 y>900 裁切
crop_precise("architecture.png", top_y=80, bottom_y=900, border_px=4)

# 2. 图 3.4 wechat_state.png: 上方不要裁切过多 (y=60 开始)，底部在 y=960 裁切
crop_precise("wechat_state.png", top_y=60, bottom_y=960, border_px=4)

# 3. 图 3.5 wifi_daemon.png: 上方不要裁切过多 (y=60 开始)，底部在 y=960 裁切
crop_precise("wifi_daemon.png", top_y=60, bottom_y=960, border_px=4)

# 4. 图 3.6 voice_flow.png: 上方标题文字很大，需要裁切到 y=230 开始，底部在 y=960 裁切
crop_precise("voice_flow.png", top_y=230, bottom_y=960, border_px=4)

print("All Chapter 3 static figures precisely cropped and updated!")
