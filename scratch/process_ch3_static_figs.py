import os
from PIL import Image

# 新版论文的图片物理存储目录
out_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
os.makedirs(out_dir, exist_ok=True)

# 原图目录
src_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu"

def process_and_crop(img_name, top_crop_ratio, border_px=3):
    src_path = os.path.join(src_dir, img_name)
    dst_path = os.path.join(out_dir, img_name)
    
    if not os.path.exists(src_path):
        print(f"Error: source path {src_path} does not exist!")
        return

    try:
        img = Image.open(src_path)
        w, h = img.size
        
        # 裁剪掉顶部的顶端文字汉字标题和上方空白
        # top_crop_ratio 指定要裁剪掉的顶部比例，例如 0.15 表示剪掉顶部 15% 的高度
        top_y = int(h * top_crop_ratio)
        
        # 裁剪边界以剥离最外层的黑色大边框
        # 左右底各剥离 border_px 像素
        left_x = border_px
        right_x = w - border_px
        bottom_y = h - border_px
        
        cropped_img = img.crop((left_x, top_y, right_x, bottom_y))
        
        # 为了美观，四周补白 20 像素的纯白留白
        padding = 20
        cw, ch = cropped_img.size
        new_img = Image.new("RGB", (cw + padding * 2, ch + padding * 2), "white")
        new_img.paste(cropped_img, (padding, padding))
        
        new_img.save(dst_path, "PNG", dpi=(300, 300))
        print(f"Successfully cropped and saved {img_name} -> {dst_path}")
        
    except Exception as e:
        print(f"Failed to process {img_name}: {e}")

# 1. 图 3.1 architecture.png (顶端标题占比较高，裁剪顶部 18% 并剥离黑边框)
process_and_crop("architecture.png", top_crop_ratio=0.18, border_px=3)

# 2. 图 3.4 wechat_state.png (裁剪顶部 14% 汉字标题并剥离黑边框)
process_and_crop("wechat_state.png", top_crop_ratio=0.14, border_px=3)

# 3. 图 3.5 wifi_daemon.png (裁剪顶部 14% 汉字标题并剥离黑边框)
process_and_crop("wifi_daemon.png", top_crop_ratio=0.14, border_px=3)

# 4. 图 3.6 voice_flow.png (裁剪顶部 14% 汉字标题并剥离黑边框)
process_and_crop("voice_flow.png", top_crop_ratio=0.14, border_px=3)

print("All static figures processed successfully!")
