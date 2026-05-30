import os
from PIL import Image, ImageDraw, ImageFont

img_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\architecture.png"

font_paths = [
    r"C:\Windows\Fonts\msyhbd.ttc",  # Microsoft YaHei Bold
    r"C:\Windows\Fonts\msyh.ttc",    # Microsoft YaHei
    r"C:\Windows\Fonts\simhei.ttf",   # SimHei
    r"C:\Windows\Fonts\arialbd.ttf"  # Arial Bold (fallback)
]

font_path = None
for p in font_paths:
    if os.path.exists(p):
        font_path = p
        break

print(f"Using font path: {font_path}")

try:
    img = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    font_zh = ImageFont.truetype(font_path, 32) if font_path else ImageFont.load_default()
    font_en = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()
    
    center_x = 110  # center of X range 25 to 195
    
    # 1. 插件层
    # Erase the area (including top remnants)
    draw.rectangle([20, 20, 198, 198], fill=(207, 230, 207))
    
    zh_text = "插件层"
    en_text = "PLUGIN LAYER"
    
    zh_w = draw.textlength(zh_text, font=font_zh)
    en_w = draw.textlength(en_text, font=font_en)
    
    draw.text((center_x - zh_w/2, 115), zh_text, fill=(0, 0, 0), font=font_zh)
    draw.text((center_x - en_w/2, 155), en_text, fill=(0, 0, 0), font=font_en)
    
    # 2. 总线层
    draw.rectangle([20, 320, 198, 460], fill=(252, 225, 195))
    
    zh_text = "总线层"
    en_text = "BUS LAYER"
    
    zh_w = draw.textlength(zh_text, font=font_zh)
    en_w = draw.textlength(en_text, font=font_en)
    
    draw.text((center_x - zh_w/2, 375), zh_text, fill=(0, 0, 0), font=font_zh)
    draw.text((center_x - en_w/2, 415), en_text, fill=(0, 0, 0), font=font_en)
    
    # 3. 宿主层
    draw.rectangle([20, 580, 198, 710], fill=(223, 234, 248))
    
    zh_text = "宿主层"
    en_text = "HOST LAYER"
    
    zh_w = draw.textlength(zh_text, font=font_zh)
    en_w = draw.textlength(en_text, font=font_en)
    
    draw.text((center_x - zh_w/2, 625), zh_text, fill=(0, 0, 0), font=font_zh)
    draw.text((center_x - en_w/2, 665), en_text, fill=(0, 0, 0), font=font_en)
    
    img.save(img_path)
    print(f"Successfully processed and updated {img_path}")
except Exception as e:
    print(f"Error: {e}")
