import cv2
import os
import numpy as np
# 5,6 line 코드만 수정하면 됨
video_path = "/Users/user/Downloads/2F_TestPic/mov/2층박스2.MOV" # split할 비디오 경로 및 비디오 이름
output_dir = "/Users/user/Downloads/2F_TestPic/2F_Box" # split 한 사진이 저장될 경로
interval = 0.3  # 0.3초마다 1장 (≈ 3프레임 간격)

os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 30

frame_window = max(1, int(fps * interval))  # 최소 1프레임 이상
frame_buffer = []
frame_count = 0
saved_count = 0

def sharpness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_buffer.append((frame.copy(), sharpness(frame)))

    # interval(0.3초) 동안 가장 선명한 프레임 선택
    if len(frame_buffer) >= frame_window:
        best_frame = max(frame_buffer, key=lambda x: x[1])[0]
        filename = f"{output_dir}/frame_{saved_count:04d}.jpg"
        cv2.imwrite(filename, best_frame)
        saved_count += 1
        frame_buffer = []

cap.release()
print(f"✅ {interval}초 간격으로 {saved_count}장의 이미지가 저장되었습니다.")