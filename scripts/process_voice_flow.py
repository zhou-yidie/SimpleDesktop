import os
import cv2
import numpy as np

img_path = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu\voice_flow.png"
out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\processed"

os.makedirs(out_dir, exist_ok=True)
filename = os.path.basename(img_path)

try:
    img_cv = cv2.imread(img_path)
    if img_cv is not None:
        # 1. Background removal (replace yellowish with white)
        light_yellow_mask = (img_cv[:,:,0] > 200) & (img_cv[:,:,1] > 220) & (img_cv[:,:,2] > 220)
        img_cv[light_yellow_mask] = [255, 255, 255]

        # 2. Specifically for voice_flow.png, we want to erase "图3-4"
        # Since contour detection might fail on some images if they have different spacing, 
        # let's be very specific: The title is in the top 25% of the image.
        height, width, _ = img_cv.shape
        top_region = img_cv[0:int(height * 0.25), 0:width]
        
        gray = cv2.cvtColor(top_region, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        char_boxes = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # Find reasonably sized character contours
            if 10 < h < 80 and 5 < w < 80:
                char_boxes.append((x, y, w, h))
        
        char_boxes.sort(key=lambda b: b[0])
        
        # We assume the first word is "图3-4" (contains about 4 characters)
        if char_boxes:
            groups = []
            current_group = [char_boxes[0]]
            for i in range(1, len(char_boxes)):
                prev_x, prev_y, prev_w, prev_h = char_boxes[i-1]
                curr_x, curr_y, curr_w, curr_h = char_boxes[i]
                
                # Check distance
                if curr_x - (prev_x + prev_w) < 20: # 20 px gap
                    current_group.append(char_boxes[i])
                else:
                    groups.append(current_group)
                    current_group = [char_boxes[i]]
            groups.append(current_group)
            
            # For voice_flow.png, the first group might be exactly "图3-4"
            # Let's forcefully erase the bounding box of the first few characters.
            # We want to erase the first 4-5 characters, regardless of grouping.
            num_chars_to_erase = min(5, len(char_boxes))
            
            # Find the gap after the first 4 characters. Usually the space between "图3-4" and the title is noticeable.
            # Let's look at the gaps between the first 8 characters.
            max_gap = 0
            split_idx = 0
            for i in range(1, min(8, len(char_boxes))):
                gap = char_boxes[i][0] - (char_boxes[i-1][0] + char_boxes[i-1][2])
                if gap > max_gap:
                    max_gap = gap
                    split_idx = i
            
            # Usually the split is after 4 chars ("图", "3", "-", "4")
            # If split_idx is reasonable (around 3 to 5), use it
            if 3 <= split_idx <= 5:
                erase_boxes = char_boxes[:split_idx]
            else:
                erase_boxes = groups[0] # Fallback to first group
                
            min_x = min([b[0] for b in erase_boxes])
            max_x = max([b[0]+b[2] for b in erase_boxes])
            min_y = min([b[1] for b in erase_boxes])
            max_y = max([b[1]+b[3] for b in erase_boxes])
            
            padding = 8
            cv2.rectangle(img_cv, 
                          (max(0, min_x - padding), max(0, min_y - padding)), 
                          (min(width, max_x + padding), min(height, max_y + padding)), 
                          (255, 255, 255), -1)

        # Remove outer border
        cv2.rectangle(img_cv, (0, 0), (width-1, height-1), (255, 255, 255), 2)

        out_path = os.path.join(out_dir, filename)
        cv2.imwrite(out_path, img_cv)
        print(f"Processed {filename} specially.")

except Exception as e:
    print(f"Error processing {filename}: {e}")
