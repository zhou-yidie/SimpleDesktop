import os
import cv2
import numpy as np

out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\processed"

def process_image(img_path):
    filename = os.path.basename(img_path)
    try:
        img_cv = cv2.imread(img_path)
        if img_cv is not None:
            # Background removal
            light_yellow_mask = (img_cv[:,:,0] > 200) & (img_cv[:,:,1] > 220) & (img_cv[:,:,2] > 220)
            img_cv[light_yellow_mask] = [255, 255, 255]

            height, width, _ = img_cv.shape
            top_region = img_cv[0:int(height * 0.20), 0:width]
            
            gray = cv2.cvtColor(top_region, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            char_boxes = []
            for c in contours:
                x, y, w, h = cv2.boundingRect(c)
                if 10 < h < 80 and 5 < w < 80:
                    char_boxes.append((x, y, w, h))
            
            char_boxes.sort(key=lambda b: b[0])
            
            if char_boxes:
                max_gap = 0
                split_idx = 0
                for i in range(1, min(6, len(char_boxes))):
                    gap = char_boxes[i][0] - (char_boxes[i-1][0] + char_boxes[i-1][2])
                    if gap > max_gap:
                        max_gap = gap
                        split_idx = i
                
                if 1 <= split_idx <= 5:
                    erase_boxes = char_boxes[:split_idx]
                    min_x = min([b[0] for b in erase_boxes])
                    max_x = max([b[0]+b[2] for b in erase_boxes])
                    min_y = min([b[1] for b in erase_boxes])
                    max_y = max([b[1]+b[3] for b in erase_boxes])
                    
                    padding = 8
                    cv2.rectangle(img_cv, 
                                  (max(0, min_x - padding), max(0, min_y - padding)), 
                                  (min(width, max_x + padding), min(height, max_y + padding)), 
                                  (255, 255, 255), -1)

            cv2.rectangle(img_cv, (0, 0), (width-1, height-1), (255, 255, 255), 2)

            out_path = os.path.join(out_dir, filename)
            cv2.imwrite(out_path, img_cv)
            print(f"Processed {filename} specially.")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

process_image(r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu\wechat_state.png")
process_image(r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu\mvvm.png")
process_image(r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu\wifi_daemon.png")
