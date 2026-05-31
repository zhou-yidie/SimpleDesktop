import os
from PIL import Image, ImageDraw, ImageFont

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "wechat_state.png")
img = Image.open(img_path)

if img.mode != "RGBA":
    img = img.convert("RGBA")

draw = ImageDraw.Draw(img)

# Font selection
font_paths = [
    r"C:\Windows\Fonts\msyhbd.ttc", # Microsoft YaHei Bold
    r"C:\Windows\Fonts\msyh.ttc",   # Microsoft YaHei
    r"C:\Windows\Fonts\arial.ttf"
]
font_path = None
for p in font_paths:
    if os.path.exists(p):
        font_path = p
        break

# We need a bold font for "Start" and "End" and a regular one for details
if font_path:
    font_title = ImageFont.truetype(font_path, 22)  # Bold/Regular depending on what's available
    font_detail = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc" if os.path.exists(r"C:\Windows\Fonts\msyh.ttc") else font_path, 18)
else:
    font_title = ImageFont.load_default()
    font_detail = ImageFont.load_default()

# ----------------- Start Box -----------------
# Start box bounds: x = 47 to 506, y = 113 to 144
# Actually, the start box might be slightly taller, let's look at y=109 to 148
# Let's cover the interior of the start box: y=111 to 147, x=49 to 504
bg_start = (200, 222, 245, 255)
draw.rectangle([49, 111, 504, 147], fill=bg_start)

# Redraw the text for the start box
# Text 1: "Start" (bold/larger)
# Text 2: "用户点击联系人卡片 (User taps contact)"
t1_start = "Start"
t2_start = "用户点击联系人卡片 (User taps contact)"

# Center them horizontally in x = [49, 504]
start_box_w = 504 - 49
try:
    w1 = draw.textbbox((0, 0), t1_start, font=font_title)[2]
    w2 = draw.textbbox((0, 0), t2_start, font=font_detail)[2]
except AttributeError:
    w1, _ = draw.textsize(t1_start, font=font_title)
    w2, _ = draw.textsize(t2_start, font=font_detail)

x1 = 49 + (start_box_w - w1) // 2
x2 = 49 + (start_box_w - w2) // 2

# Draw:
draw.text((x1, 112), t1_start, fill=(0, 0, 0, 255), font=font_title)
draw.text((x2, 134), t2_start, fill=(0, 0, 0, 255), font=font_detail)

# ----------------- End Box -----------------
# End box bounds: x = 125 to 407, y = 821 to 859
# Let's cover the interior of the end box: y=816 to 863, x=127 to 405
# Wait, let's see. The text of end box contains three lines!
# Let's make sure we have enough height.
bg_end = (210, 232, 209, 255)
draw.rectangle([127, 816, 405, 863], fill=bg_end)

# Redraw the text for the end box
t1_end = "End"
t2_end = "进入通话界面"
t3_end = "状态机重置 Index=0"

end_box_w = 405 - 127
try:
    we1 = draw.textbbox((0, 0), t1_end, font=font_title)[2]
    we2 = draw.textbbox((0, 0), t2_end, font=font_detail)[2]
    we3 = draw.textbbox((0, 0), t3_end, font=font_detail)[2]
except AttributeError:
    we1, _ = draw.textsize(t1_end, font=font_title)
    we2, _ = draw.textsize(t2_end, font=font_detail)
    we3, _ = draw.textsize(t3_end, font=font_detail)

xe1 = 127 + (end_box_w - we1) // 2
xe2 = 127 + (end_box_w - we2) // 2
xe3 = 127 + (end_box_w - we3) // 2

draw.text((xe1, 815), t1_end, fill=(0, 0, 0, 255), font=font_title)
draw.text((xe2, 836), t2_end, fill=(0, 0, 0, 255), font=font_detail)
draw.text((xe3, 854), t3_end, fill=(0, 0, 0, 255), font=font_detail)

img.save(img_path)
print("Successfully fixed wechat_state.png!")
