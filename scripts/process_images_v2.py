from PIL import Image
import os
import glob

in_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu"
out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\processed"

os.makedirs(out_dir, exist_ok=True)
images = glob.glob(os.path.join(in_dir, "*.png"))

for img_path in images:
    filename = os.path.basename(img_path)
    try:
        img = Image.open(img_path).convert("RGBA")
        datas = img.getdata()
        
        new_data = []
        # Background is a beige/yellowish color. 
        # Typically #fdf5e6 (253, 245, 230) or similar. 
        # We replace any pixel with R>220, G>220, B>200 with pure white (255, 255, 255, 255)
        for item in datas:
            if item[0] > 220 and item[1] > 220 and item[2] > 200:
                new_data.append((255, 255, 255, 255))
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        
        # To remove the title, we crop the top part of the image. 
        # Looking at typical flowchart screenshots, the title "图3-3 xxx" takes up the top ~8% to 15% of the image.
        # Let's crop out the top 10% or a fixed pixel amount (e.g., top 80 pixels).
        width, height = img.size
        
        # Crop 12% of the top to ensure the title is removed
        crop_amount = int(height * 0.12)
        cropped_img = img.crop((0, crop_amount, width, height))
        
        # Save the result
        out_path = os.path.join(out_dir, filename)
        cropped_img.save(out_path, "PNG")
        print(f"Processed {filename}")
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")
