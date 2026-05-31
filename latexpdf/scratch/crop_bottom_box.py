import os
from PIL import Image

figures_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\figures"
img_path = os.path.join(figures_dir, "tech_stack.png")
img = Image.open(img_path)
width, height = img.size

# Bottom box is at y = 1843 to 2131
# Let's crop it and save to scratch
box = img.crop((0, 1840, width, 2135))
scratch_dir = r"d:\Graduation_Project\SimpleDesktop\latexpdf\scratch"
os.makedirs(scratch_dir, exist_ok=True)
box.save(os.path.join(scratch_dir, "bottom_box.png"))
print("Saved bottom_box.png!")
