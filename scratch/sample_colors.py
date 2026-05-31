from PIL import Image

img_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\architecture.png"

try:
    img = Image.open(img_path)
    # Convert to RGB if it isn't
    img = img.convert("RGB")
    
    # Sample background color
    green_bg = img.getpixel((100, 130))
    orange_bg = img.getpixel((100, 390))
    blue_bg = img.getpixel((100, 630))
    
    print(f"Green BG color: {green_bg} -> hex: #{green_bg[0]:02x}{green_bg[1]:02x}{green_bg[2]:02x}")
    print(f"Orange BG color: {orange_bg} -> hex: #{orange_bg[0]:02x}{orange_bg[1]:02x}{orange_bg[2]:02x}")
    print(f"Blue BG color: {blue_bg} -> hex: #{blue_bg[0]:02x}{blue_bg[1]:02x}{blue_bg[2]:02x}")
except Exception as e:
    print(f"Error: {e}")
