import os
import glob
import cv2
import numpy as np

in_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu"
out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\processed"

os.makedirs(out_dir, exist_ok=True)
images = glob.glob(os.path.join(in_dir, "*.png"))

for img_path in images:
    filename = os.path.basename(img_path)
    try:
        img_cv = cv2.imread(img_path)
        
        # 1. Background removal (replace yellowish with white)
        # BGR format
        light_yellow_mask = (img_cv[:,:,0] > 200) & (img_cv[:,:,1] > 220) & (img_cv[:,:,2] > 220)
        img_cv[light_yellow_mask] = [255, 255, 255]

        # 2. To remove just the title ("图X-X xxx") at the top without changing image size,
        # we will simply draw a white rectangle over the top 10% of the image.
        height, width, _ = img_cv.shape
        erase_height = int(height * 0.10)
        
        # Draw a filled white rectangle over the title area
        cv2.rectangle(img_cv, (0, 0), (width, erase_height), (255, 255, 255), -1)

        # Save the result
        out_path = os.path.join(out_dir, filename)
        cv2.imwrite(out_path, img_cv)
        print(f"Processed {filename}")
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")
