import os
from PIL import Image, ImageDraw, ImageFont

# img_path：裁剪后在 latexpdf 目录下的最终架构图图片物理路径
img_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\architecture.png"

# font_paths：优先选择仿宋体，依次递补
font_paths = [
    r"C:\Windows\Fonts\simfang.ttf",  # 仿宋体 (FangSong)
    r"C:\Windows\Fonts\msyh.ttc",    # 微软雅黑常规 (Microsoft YaHei)
    r"C:\Windows\Fonts\simhei.ttf",   # 黑体 (SimHei)
    r"C:\Windows\Fonts\arialbd.ttf"  # Arial 粗体 (Arial Bold, 备用)
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
    
    # 将字号调整为 21px 中文 / 13px 英文，与其他组件字号保持视觉一致性
    font_zh = ImageFont.truetype(font_path, 21) if font_path else ImageFont.load_default()
    font_en = ImageFont.truetype(font_path, 13) if font_path else ImageFont.load_default()
    
    # 精确测得的三层左侧标题栏的物理 X 轴几何中点
    center_x = 191  
    
    # -------------------------------------------------------------
    # 1. 插件层 (Plugin Layer) 局部修改
    # -------------------------------------------------------------
    # 用淡绿色 (207, 230, 207) 填充擦除区域，左右和上下各收窄 2 像素以防破坏大边框
    draw.rectangle([69, 116, 313, 333], fill=(207, 230, 207))
    
    zh_text = "插件层"
    en_text = "PLUGIN LAYER"
    
    zh_w = draw.textlength(zh_text, font=font_zh)
    en_w = draw.textlength(en_text, font=font_en)
    
    # 垂直居中排版中文与英文
    draw.text((center_x - zh_w/2, 185), zh_text, fill=(0, 0, 0), font=font_zh)
    draw.text((center_x - en_w/2, 230), en_text, fill=(0, 0, 0), font=font_en)
    
    # -------------------------------------------------------------
    # 2. 总线层 (Bus Layer) 局部修改
    # -------------------------------------------------------------
    # 用淡橙色 (252, 225, 195) 填充擦除区域，防止破坏大边框
    draw.rectangle([69, 408, 313, 645], fill=(252, 225, 195))
    
    zh_text = "总线层"
    en_text = "BUS LAYER"
    
    zh_w = draw.textlength(zh_text, font=font_zh)
    en_w = draw.textlength(en_text, font=font_en)
    
    draw.text((center_x - zh_w/2, 485), zh_text, fill=(0, 0, 0), font=font_zh)
    draw.text((center_x - en_w/2, 530), en_text, fill=(0, 0, 0), font=font_en)
    
    # -------------------------------------------------------------
    # 3. 宿主层 (Host Layer) 局部修改
    # -------------------------------------------------------------
    # 用淡蓝色 (223, 234, 248) 填充擦除区域，防止破坏大边框
    draw.rectangle([69, 701, 313, 838], fill=(223, 234, 248))
    
    zh_text = "宿主层"
    en_text = "HOST LAYER"
    
    zh_w = draw.textlength(zh_text, font=font_zh)
    en_w = draw.textlength(en_text, font=font_en)
    
    draw.text((center_x - zh_w/2, 730), zh_text, fill=(0, 0, 0), font=font_zh)
    draw.text((center_x - en_w/2, 770), en_text, fill=(0, 0, 0), font=font_en)
    
    img.save(img_path)
    print(f"Successfully processed and updated {img_path}")
except Exception as e:
    print(f"Error: {e}")
