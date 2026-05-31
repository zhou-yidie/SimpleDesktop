import os
from PIL import Image

def process_image():
    # 路径配置
    img_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\mvvm.png"
    backup_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\mvvm_backup.png"
    
    if not os.path.exists(img_path):
        print(f"Error: {img_path} 不存在！")
        return
        
    # 备份原图
    if not os.path.exists(backup_path):
        img_orig = Image.open(img_path)
        img_orig.save(backup_path)
        print(f"已将原图备份至: {backup_path}")
    
    # 重新读取原图进行处理
    img = Image.open(backup_path)
    w, h = img.size
    
    # 将图像转换为 RGB 模式
    img_rgb = img.convert("RGB")
    pixels = img_rgb.load()
    
    print(f"原图尺寸: {w}x{h}")
    
    # 1. 精准寻找三个彩色背景框的顶部 y 坐标，作为裁剪顶部
    # 在 y 范围 [120, 300] 内，从上往下扫描
    # 我们知道左侧 View Layer 的框是蓝色的 (R < 230, B > 240) 左右
    # 我们逐行扫描，如果某行检测到了明显的背景蓝、背景橙或背景绿，就认为是三栏的起点
    y_start = 180 # 预设安全起点
    for y in range(120, 300):
        found_color = False
        for x in range(100, w - 100):
            r, g, b = pixels[x, y]
            # 检测蓝色 (View Layer): e.g. R=212, G=226, B=244
            is_blue = (r < 225 and b > 235 and abs(r - g) < 20)
            # 检测橙色 (ViewModel Layer): e.g. R=255, G=233, B=214
            is_orange = (r > 245 and g > 220 and b < 225 and g > b)
            # 检测绿色 (Model Layer): e.g. R=213, G=232, B=212
            is_green = (r < 225 and g > 225 and b < 225 and abs(r - b) < 15)
            
            if is_blue or is_orange or is_green:
                print(f"在 y={y}, x={x} 处检测到主体图表背景色 (RGB: {r},{g},{b})")
                y_start = y
                found_color = True
                break
        if found_color:
            break
            
    print(f"自动定位到的主体顶部坐标 y_start = {y_start}")
    
    # 2. 定位左右下的黑色边框线
    # 黑线像素通常 R, G, B 都极低 (例如 < 50)
    # 我们分别从左、右、下向中心扫描，找到最外围的那根黑线位置
    
    left_border = 10
    for x in range(0, 50):
        # 扫描某列，如果有很多黑色像素，说明是左黑框
        black_count = 0
        for y in range(y_start, h - 50):
            r, g, b = pixels[x, y]
            if r < 80 and g < 80 and b < 80:
                black_count += 1
        if black_count > (h - y_start) * 0.5: # 超过50%的像素为黑
            left_border = x
            print(f"在 x={x} 处找到左侧外黑框线 (黑色像素数={black_count})")
            
    right_border = w - 10
    for x in range(w - 1, w - 51, -1):
        black_count = 0
        for y in range(y_start, h - 50):
            r, g, b = pixels[x, y]
            if r < 80 and g < 80 and b < 80:
                black_count += 1
        if black_count > (h - y_start) * 0.5:
            right_border = x
            print(f"在 x={x} 处找到右侧外黑框线 (黑色像素数={black_count})")
            
    bottom_border = h - 10
    for y in range(h - 1, h - 51, -1):
        black_count = 0
        for x in range(100, w - 100):
            r, g, b = pixels[x, y]
            if r < 80 and g < 80 and b < 80:
                black_count += 1
        if black_count > (w - 200) * 0.5:
            bottom_border = y
            print(f"在 y={y} 处找到底部外黑框线 (黑色像素数={black_count})")

    # 3. 设定精确的裁剪区间
    # 顶端：为了完全删除“MVVM架构模式与单向数据流示意图”和它的黑框，并保留足够的美观间距，
    # 裁剪顶边设置为 y_start - 25。
    # 左右下边界：直接裁剪到黑线内侧 3 个像素，从而彻底切掉黑框。
    crop_top = max(0, y_start - 25)
    crop_left = left_border + 3
    crop_right = right_border - 3
    crop_bottom = bottom_border - 3
    
    print(f"裁剪区域：Left={crop_left}, Top={crop_top}, Right={crop_right}, Bottom={crop_bottom}")
    
    # 裁剪图像
    cropped_img = img.crop((crop_left, crop_top, crop_right, crop_bottom))
    
    # 为了让图片看起来清爽大气，我们给它四周补一圈 20 像素的纯白色边框！
    final_w = cropped_img.width + 40
    final_h = cropped_img.height + 40
    final_img = Image.new("RGB", (final_w, final_h), "white")
    final_img.paste(cropped_img, (20, 20))
    
    # 保存覆盖原文件
    final_img.save(img_path, format="PNG")
    print(f"处理成功！已覆盖保存至: {img_path}")

if __name__ == "__main__":
    process_image()
