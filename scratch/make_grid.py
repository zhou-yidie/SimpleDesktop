import os
from PIL import Image, ImageDraw

img_path = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures\architecture.png"
out_path = r"C:\Users\22613\.gemini\antigravity\brain\ba4af961-c500-4698-b1e1-acbae826aa20\grid_architecture.png"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

try:
    img = Image.open(img_path)
    w, h = img.size
    draw = ImageDraw.Draw(img)
    
    # Draw vertical grid lines
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill="red", width=1)
        if x % 100 == 0:
            draw.text((x, 5), str(x), fill="red")
            
    # Draw horizontal grid lines
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill="red", width=1)
        if y % 100 == 0:
            draw.text((5, y), str(y), fill="red")
            
    img.save(out_path)
    print(f"Grid image saved successfully to {out_path}")
    print(f"Dimensions: {w}x{h}")
except Exception as e:
    print(f"Error: {e}")
