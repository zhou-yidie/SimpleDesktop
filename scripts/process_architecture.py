import os
import cv2
import numpy as np

# img_path：原始未处理架构图的绝对物理路径
img_path = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\yuantu\architecture.png"

# out_dir：图像处理完之后的输出目标物理目录
out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures\processed"

os.makedirs(out_dir, exist_ok=True)
# filename：从物理路径中提取出的图片纯文件名（如 "architecture.png"）
filename = os.path.basename(img_path)

try:
    # img_cv：使用 OpenCV 读取得到的架构图原始 BGR 图像数据矩阵 (numpy 数组)
    img_cv = cv2.imread(img_path)
    
    if img_cv is not None:
        # -------------------------------------------------------------
        # 1. 图像背景去黄处理
        # -------------------------------------------------------------
        # light_yellow_mask：定位图像中呈淡黄色背景的所有像素点（RGB各通道均大于阈值）的布尔遮罩矩阵
        light_yellow_mask = (img_cv[:,:,0] > 200) & (img_cv[:,:,1] > 220) & (img_cv[:,:,2] > 220)
        # 将检测出的淡黄色背景像素点全部强制修改为纯白色 [255, 255, 255]，提升打印对比度
        img_cv[light_yellow_mask] = [255, 255, 255]

        # -------------------------------------------------------------
        # 2. 去除残余标题编号“-1”的处理
        # -------------------------------------------------------------
        # height：原始图像的总高度（像素）
        # width：原始图像的总宽度（像素）
        height, width, _ = img_cv.shape
        
        # top_region：裁取图像最上部 20% 高度的子图像区域，用于文字检测以定位“-1”
        top_region = img_cv[0:int(height * 0.20), 0:width]
        
        # gray：转换 top_region 到单通道灰度图
        gray = cv2.cvtColor(top_region, cv2.COLOR_BGR2GRAY)
        
        # thresh：应用反向二值化阈值操作获得的二值图像，方便提取字符轮廓
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # contours：检测出的闭合字符外轮廓列表
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # char_boxes：筛选过后的有效单个字符包围盒列表，存放元素为 (x, y, w, h)
        char_boxes = []
        # c：循环中代表每一个具体轮廓的临时变量
        for c in contours:
            # x, y, w, h：具体轮廓的外接包围盒的起始点横纵坐标、宽、高
            x, y, w, h = cv2.boundingRect(c)
            # 依据文字的一般物理尺寸长宽比进行噪点剔除，只保留真实的字符轮廓包围盒
            if 10 < h < 80 and 5 < w < 80:
                char_boxes.append((x, y, w, h))
        
        # 将提取到的所有有效字符包围盒按其在画面中的横坐标从左到右排序
        char_boxes.sort(key=lambda b: b[0])
        
        if char_boxes:
            # max_gap：最宽的字符间隙宽度（像素）
            max_gap = 0
            # split_idx：用于划分残留图表编号与主要标题文字（“系统三层总体...”）的字符索引边界
            split_idx = 0
            # 遍历前几个字符，通过寻找突然增大的字符间距（Gap）来切分字符
            # i：字符列表遍历中的索引值
            for i in range(1, min(6, len(char_boxes))):
                # gap：当前字符与前一字符右边缘之间的水平间隙距离
                gap = char_boxes[i][0] - (char_boxes[i-1][0] + char_boxes[i-1][2])
                if gap > max_gap:
                    max_gap = gap
                    split_idx = i
            
            # 如果成功定位到了表示标题文字与残存编号分界的间距
            if 1 <= split_idx <= 5:
                # erase_boxes：需要被擦除的残余编号字符（例如 “-1”）的包围盒列表
                erase_boxes = char_boxes[:split_idx]
                
                # 提取这组需要擦除的包围盒的最小 X 坐标、最大 X 坐标、最小 Y 坐标与最大 Y 坐标，合并为统一大包围盒
                min_x = min([b[0] for b in erase_boxes])
                max_x = max([b[0]+b[2] for b in erase_boxes])
                min_y = min([b[1] for b in erase_boxes])
                max_y = max([b[1]+b[3] for b in erase_boxes])
                
                # padding：擦除包围盒四周的安全留白边缘大小
                padding = 8
                # 使用 cv2.rectangle 以纯白色 (255, 255, 255) 覆盖性地画一个实心矩形 (-1)，彻底抹去残余的“-1”文字
                cv2.rectangle(img_cv, 
                              (max(0, min_x - padding), max(0, min_y - padding)), 
                              (min(width, max_x + padding), min(height, max_y + padding)), 
                              (255, 255, 255), -1)

        # -------------------------------------------------------------
        # 3. 去除图像原有的最外圈黑线窄边框
        # -------------------------------------------------------------
        # 用纯白色覆盖图像的最边缘一圈，去除原有的扫描或截图黑边框
        cv2.rectangle(img_cv, (0, 0), (width-1, height-1), (255, 255, 255), 2)

        # out_path：处理后的图片最终保存输出的绝对物理路径
        out_path = os.path.join(out_dir, filename)
        cv2.imwrite(out_path, img_cv)
        print(f"Processed {filename} specially.")

except Exception as e:
    print(f"Error processing {filename}: {e}")
