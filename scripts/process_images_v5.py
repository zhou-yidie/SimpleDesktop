import os
import glob
import cv2
import numpy as np
import re

in_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu"
out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\processed"

os.makedirs(out_dir, exist_ok=True)
images = glob.glob(os.path.join(in_dir, "*.png"))

for img_path in images:
    filename = os.path.basename(img_path)
    try:
        img_cv = cv2.imread(img_path)
        if img_cv is None: continue
        
        # 1. Background removal (replace yellowish with white)
        # The background is a specific beige, but there might also be a thin black border.
        # Let's replace the light yellow/beige with pure white.
        # Also let's replace any color very close to white/beige to white.
        gray_val = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Find pixels that are light colored but not strictly white, and not inside the diagram boxes
        # We can just threshold the beige color. BGR values around [224, 238, 246]
        # More general: if B>200, G>220, R>220
        light_yellow_mask = (img_cv[:,:,0] > 200) & (img_cv[:,:,1] > 220) & (img_cv[:,:,2] > 220)
        img_cv[light_yellow_mask] = [255, 255, 255]

        # 2. Find and erase just "图X-X"
        # We will use simple contour detection to find the title text characters.
        # "图3-1" is usually the first few characters on the top line.
        # It's located horizontally before the main title string.
        # The title is usually at the top 10% of the image.
        
        height, width, _ = img_cv.shape
        top_region = img_cv[0:int(height * 0.15), 0:width]
        
        # Convert top region to grayscale
        gray = cv2.cvtColor(top_region, cv2.COLOR_BGR2GRAY)
        
        # Threshold to get dark text
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Find individual character contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size to get text characters (ignore noise or huge boxes)
        char_boxes = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # Text characters are usually between 10 and 50 pixels high and wide
            if 10 < h < 60 and 5 < w < 60:
                char_boxes.append((x, y, w, h))
        
        # Sort boxes left-to-right, then top-to-bottom. 
        # Or better: find lines of text.
        # Since it's a single line of title, sorting by x coordinate is enough.
        char_boxes.sort(key=lambda b: b[0])
        
        # The first few characters (usually 4 characters: "图", "3", "-", "1") belong to "图3-1"
        # They will have small gaps between them. The gap between "图X-X" and the rest of the title 
        # might be slightly larger, or we can just erase the first N characters.
        # "图3-1" is exactly 4 connected components (or more if they are disconnected, but usually 4-5).
        
        # Let's group characters that are close to each other
        if char_boxes:
            groups = []
            current_group = [char_boxes[0]]
            for i in range(1, len(char_boxes)):
                prev_x, prev_y, prev_w, prev_h = char_boxes[i-1]
                curr_x, curr_y, curr_w, curr_h = char_boxes[i]
                
                # If the horizontal distance is small, they are in the same word
                gap = curr_x - (prev_x + prev_w)
                if gap < 15: # 15 pixels is a reasonable threshold for characters in the same word
                    current_group.append(char_boxes[i])
                else:
                    groups.append(current_group)
                    current_group = [char_boxes[i]]
            groups.append(current_group)
            
            # The first group should be "图X-X"
            # Sometimes "图" and "X-X" might be split if the gap is slightly larger.
            # Let's find the bounding box of the first few characters.
            # Usually "图3-1" spans around 80-120 pixels in width.
            # Let's find all characters whose x coordinate is less than a certain value relative to the start.
            
            start_x = char_boxes[0][0]
            # Erase all contours that belong to the first "word" or the first few chars
            # Actually, "图3-1" takes about 4 characters. 
            # We can find the bounding box of the first 4-6 characters, or find a large gap.
            # Let's find the first gap that is larger than the average character gap.
            
            erase_end_x = start_x
            for i in range(1, len(char_boxes)):
                gap = char_boxes[i][0] - (char_boxes[i-1][0] + char_boxes[i-1][2])
                if gap > 8: # A space between "图3-1" and the rest of the title
                    erase_end_x = char_boxes[i-1][0] + char_boxes[i-1][2]
                    break
            
            # If no obvious gap was found, just erase the first 120 pixels from start_x
            if erase_end_x == start_x:
                erase_end_x = start_x + 100
                
            # To be safer and cover the whole "图3-1" regardless of gap:
            # We know "图3-1" contains 4 characters. If we erase up to the 4th or 5th contour:
            # Let's just find the bounding box of all characters up to the first space.
            # And draw a white rectangle over them.
            
            # We will use the first group
            first_group = groups[0]
            # If the first group is too short (e.g., just "图"), we include the second group.
            first_group_width = first_group[-1][0] + first_group[-1][2] - first_group[0][0]
            if first_group_width < 50 and len(groups) > 1:
                first_group.extend(groups[1])
                
            min_x = min([b[0] for b in first_group])
            max_x = max([b[0]+b[2] for b in first_group])
            min_y = min([b[1] for b in first_group])
            max_y = max([b[1]+b[3] for b in first_group])
            
            # Add a small padding
            padding = 5
            cv2.rectangle(img_cv, 
                          (max(0, min_x - padding), max(0, min_y - padding)), 
                          (min(width, max_x + padding), min(height, max_y + padding)), 
                          (255, 255, 255), -1)

        # 3. Handle the outer black border if it exists
        # Some images have a black border around the whole image, we can just replace the outer 2 pixels with white
        cv2.rectangle(img_cv, (0, 0), (width-1, height-1), (255, 255, 255), 2)

        # Save the result
        out_path = os.path.join(out_dir, filename)
        cv2.imwrite(out_path, img_cv)
        print(f"Processed {filename}")
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")
