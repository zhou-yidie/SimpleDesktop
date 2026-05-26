from PIL import Image, ImageDraw
import os
import glob
import re
import cv2
import numpy as np
import pytesseract

in_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu"
out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\processed"

os.makedirs(out_dir, exist_ok=True)
images = glob.glob(os.path.join(in_dir, "*.png"))

for img_path in images:
    filename = os.path.basename(img_path)
    try:
        # We will use OpenCV to detect and remove just the "图X-X" part while keeping size the same
        img_cv = cv2.imread(img_path)
        
        # 1. Background removal (replace yellowish with white)
        # BGR format
        light_yellow_mask = (img_cv[:,:,0] > 200) & (img_cv[:,:,1] > 220) & (img_cv[:,:,2] > 220)
        img_cv[light_yellow_mask] = [255, 255, 255]

        # 2. To remove just "图X-X", we can find text using contours in the top part of the image
        height, width, _ = img_cv.shape
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Threshold to get text
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Dilate slightly to connect characters into words
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Look for the title which usually is at the top (y < height * 0.15)
        # We will erase contours that are at the top and look like text lines.
        # But wait, "图X-X" might be just part of a line. We want to erase JUST "图X-X".
        # If we just erase the top 12% by drawing a white rectangle over it, we keep the size!
        
        # Instead of cropping, we draw a white rectangle over the top 10-12% area
        # This keeps the original image dimensions.
        erase_height = int(height * 0.10)
        cv2.rectangle(img_cv, (0, 0), (width, erase_height), (255, 255, 255), -1)

        # Save the result
        out_path = os.path.join(out_dir, filename)
        cv2.imwrite(out_path, img_cv)
        print(f"Processed {filename}")
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")
