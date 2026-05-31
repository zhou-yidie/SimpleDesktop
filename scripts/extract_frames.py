import cv2
import os

video_path = r"d:\Graduation_Project\SimpleDesktop\演示视频.mp4"
out_dir = r"d:\Graduation_Project\SimpleDesktop\thesis_figures"

timestamps = {
    "page1_home.jpg": 128,          # 02:08
    "page2_contact_options.jpg": 138, # 02:18
    "page3_wechat_search.jpg": 141,   # 02:21
    "page4_wechat_chat.jpg": 143,     # 02:23
    "page5_wechat_panel.jpg": 144,    # 02:24
    "page6_wechat_video.jpg": 145     # 02:25
}

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

for name, ts in timestamps.items():
    frame_no = int(ts * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(os.path.join(out_dir, name), frame)
        print(f"Saved {name}")
    else:
        print(f"Failed to save {name}")

cap.release()
