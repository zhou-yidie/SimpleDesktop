import cv2
import numpy as np
import os
import glob

in_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu"
out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\processed"

os.makedirs(out_dir, exist_ok=True)
images = glob.glob(os.path.join(in_dir, "*.png"))

for img_path in images:
    filename = os.path.basename(img_path)
    img = cv2.imread(img_path)
    if img is None:
        continue
    
    # Create a mask for off-white background colors
    # We will turn these into pure white (255, 255, 255)
    # The background seems to be a light beige color, e.g., #fdf5e6 or similar.
    # We can convert pixels that are very bright and slightly yellowish to white.
    # Convert to HSV to easily identify background
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # The background is likely high value, low saturation.
    # Let's say Value > 200, Saturation < 50
    lower_bg = np.array([0, 0, 200])
    upper_bg = np.array([180, 50, 255])
    bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
    
    # We can also just threshold the image if the background is light
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # But since the background has a specific color, let's target that.
    # It seems to be around (R:246, G:238, B:224) roughly.
    lower_beige = np.array([200, 210, 220]) # BGR
    upper_beige = np.array([245, 255, 255])
    # Actually, simpler way: if pixel is close to background color, make it white.
    # The background is [224, 238, 246] or something in BGR.
    # Let's just turn anything that is very light into pure white.
    light_pixels = (img[:, :, 0] > 200) & (img[:, :, 1] > 200) & (img[:, :, 2] > 200)
    img[light_pixels] = [255, 255, 255]

    # For removing "图3-3", we can use OCR or template matching, or we can just 
    # crop the top part of the image, or simply white out the title.
    # Looking at the sample image, the title is at the very top.
    # "图X-X" is part of the title. If we want to remove just the text "图X-X", 
    # or the whole title, the user says "图片的“图几点几”的汉字去掉".
    # Since I don't have easy OCR without installing tesseract, I can do a simple 
    # heuristic: find the top-most black text and erase it, or crop the image to 
    # remove the title completely. Usually in LaTeX, the figure caption is 
    # added by LaTeX anyway, so removing the entire title from the image is the best approach.
    
    # Let's find the first row with non-white pixels
    # Since we made the background white, let's find the bounding box of the non-white content
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours to identify the title text at the top
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by y-coordinate
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    bounding_boxes = sorted(bounding_boxes, key=lambda b: b[1])
    
    # The title is usually at the top. We can just draw a white rectangle over the top 
    # 5-10% of the image, but only where the title is.
    # A safer approach: the title is the topmost connected components that are wide and short.
    # We will find the top Y coordinate of the main diagram. The main diagram is usually 
    # much larger than the text.
    
    # Let's just crop out the top part where the title resides.
    # Or find the highest large component (the main flowchart) and crop above it.
    
    # Another approach: find all text at the top and white it out.
    if bounding_boxes:
        # Get the y coordinate of the top-most large box (the diagram)
        # Diagram is usually a very large box.
        max_area = 0
        main_diagram_y = img.shape[0]
        for x, y, w, h in bounding_boxes:
            if w * h > max_area:
                max_area = w * h
        
        # Any box that is above the main diagram (with some margin) and relatively small is probably title.
        # But wait, the diagram is composed of many boxes, so RETR_EXTERNAL might give many boxes.
        
        # Let's just use an assumption: the title is in the top 10% or so.
        # But to be safe, I'll use a specific logic:
        # Find the top y coordinate of the diagram. The title text has a height of around 20-40 pixels.
        # The flowchart nodes are much bigger.
        pass

    # A simpler and very robust way to remove the "图X-X" and title is just to crop the image
    # to the bounding box of the actual graph, but wait, the title IS part of the image content.
    # If I just want to remove "图X-X", I can search for the text. Without OCR, it's hard to find *just* "图X-X".
    # BUT, the user's screenshot shows the title is centered at the top: "图3-3 WiFi网络守护模块工作流程图"
    # To remove just "图3-3", I can find the first horizontal line of text, and black out the first few characters.
    # Or, even better, I can remove the entire title line, because in LaTeX, the caption is added via \caption{}.
    # Let's remove the entire topmost line of components.
    
    y_coords = [y for x,y,w,h in bounding_boxes if w > 5 and h > 5]
    if y_coords:
        top_y = min(y_coords)
        # Find all boxes that are roughly on the same line as the top_y
        title_bottom_y = top_y
        for x, y, w, h in bounding_boxes:
            if w > 5 and h > 5 and y < top_y + 60: # Assuming title height is within 60 pixels
                title_bottom_y = max(title_bottom_y, y + h)
        
        # White out the title area
        cv2.rectangle(img, (0, 0), (img.shape[1], title_bottom_y + 10), (255, 255, 255), -1)

    # Save the processed image
    out_path = os.path.join(out_dir, filename)
    cv2.imwrite(out_path, img)
    print(f"Processed {filename}")
