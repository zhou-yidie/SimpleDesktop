import os
from PIL import Image

def process_tech_stack():
    img_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\tech_stack.png"
    backup_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\tech_stack_backup.png"
    
    if not os.path.exists(img_path):
        print(f"Error: {img_path} 不存在！")
        return
        
    # 备份原图
    if not os.path.exists(backup_path):
        img_orig = Image.open(img_path)
        img_orig.save(backup_path)
        print(f"已将 tech_stack.png 原图备份至: {backup_path}")
    
    # 重新读取原图进行处理
    img = Image.open(backup_path)
    w, h = img.size
    
    # 转换 RGB
    img_rgb = img.convert("RGB")
    pixels = img_rgb.load()
    
    print(f"原图尺寸: {w}x{h}")
    
    # 1. 扫描主体框顶部起点 y_start
    # 主体是三层框：粉红 (#ffe6eb)、蓝色 (#e6f2ff)、橙色 (#fff2e6) 等
    y_start = 180
    for y in range(120, 300):
        found_color = False
        for x in range(100, w - 100):
            r, g, b = pixels[x, y]
            # 检测浅橙/浅粉/浅蓝/浅绿等
            is_pastel = (r < 245 and g > 210 and b > 210 and abs(r - g) < 25) or \
                        (r > 240 and g > 210 and b < 235 and g > b) or \
                        (r < 230 and g < 240 and b > 235 and abs(r - g) < 20)
            if is_pastel:
                print(f"在 y={y}, x={x} 处检测到主体技术栈背景色 (RGB: {r},{g},{b})")
                y_start = y
                found_color = True
                break
        if found_color:
            break
            
    print(f"定位到的主体顶部坐标 y_start = {y_start}")
    
    # 2. 定位左右下的黑色边框线
    left_border = 10
    for x in range(0, 50):
        black_count = 0
        for y in range(y_start, h - 50):
            r, g, b = pixels[x, y]
            if r < 80 and g < 80 and b < 80:
                black_count += 1
        if black_count > (h - y_start) * 0.5:
            left_border = x
            print(f"在 x={x} 处找到左侧外黑框线")
            
    right_border = w - 10
    for x in range(w - 1, w - 51, -1):
        black_count = 0
        for y in range(y_start, h - 50):
            r, g, b = pixels[x, y]
            if r < 80 and g < 80 and b < 80:
                black_count += 1
        if black_count > (h - y_start) * 0.5:
            right_border = x
            print(f"在 x={x} 处找到右侧外黑框线")
            
    bottom_border = h - 10
    for y in range(h - 1, h - 51, -1):
        black_count = 0
        for x in range(100, w - 100):
            r, g, b = pixels[x, y]
            if r < 80 and g < 80 and b < 80:
                black_count += 1
        if black_count > (w - 200) * 0.5:
            bottom_border = y
            print(f"在 y={y} 处找到底部外黑框线")

    # 3. 设定精确裁剪区域
    # 为了完全删除顶端文字及黑框，我们设定 Top = y_start - 25 像素
    crop_top = max(0, y_start - 25)
    crop_left = left_border + 3
    crop_right = right_border - 3
    crop_bottom = bottom_border - 3
    
    print(f"裁剪区域：Left={crop_left}, Top={crop_top}, Right={crop_right}, Bottom={crop_bottom}")
    
    # 裁剪
    cropped_img = img.crop((crop_left, crop_top, crop_right, crop_bottom))
    
    # 补白边，使之美观排版
    final_w = cropped_img.width + 40
    final_h = cropped_img.height + 40
    final_img = Image.new("RGB", (final_w, final_h), "white")
    final_img.paste(cropped_img, (20, 20))
    
    # 保存覆盖
    final_img.save(img_path, format="PNG")
    print(f"处理成功！已覆盖保存至: {img_path}")

if __name__ == "__main__":
    process_tech_stack()
