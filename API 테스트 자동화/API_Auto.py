import os
import requests
import csv
import json
import shutil
from datetime import datetime

# === API 테스트 시, 10, 11, 12번 줄의 API URL, Secret Key, 이미지가 들어있는 폴더 경로 만 수정하면 됩니다. ===
# 추가로, 오류 발생 시 22번 줄의 datasetInfo 값이 정확하게 입력됐는지 확인!
API_URL = "URL 주소 입력"
SECRET = "발급 받은 Key 값"
IMG_DIR = "image 디렉토리 지정"

headers = {"SECRET 키 요청 값": SECRET}

extra_data = {
    "cameraParameters": "null", # 입력 값 넣기
    "withGlobal": "null", # 입력 값 넣기
    "lastPose": "null", # 입력 값 넣기
    "odometry": "null", # 입력 값 넣기
    "withInlier": "null", # 입력 값 넣기
    "datasetInfo": "null" # error 발생 시, datasetInfo 도 맞는지 확인! / 입력 값 넣기
}

# === 실행 시마다 새로운 결과 폴더 생성 ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
RESULT_DIR = os.path.join(os.getcwd(), f"API_Results_{timestamp}")
FAILED_DIR = os.path.join(RESULT_DIR, "failed_images")
os.makedirs(FAILED_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

csv_file = os.path.join(RESULT_DIR, "api_test_results.csv")

# === 테스트 결과 저장을 위한 리스트 ===
results = []

count_pass = count_fail = count_error = 0

# === 이미지 처리 ===
for filename in os.listdir(IMG_DIR):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(IMG_DIR, filename)
        with open(img_path, "rb") as img:
            files = {"image": (filename, img, "image/jpeg")}
            try:
                response = requests.post(API_URL, headers=headers, files=files, data=extra_data)
                resp_text = response.text[:120].replace("\n", " ")

                if response.status_code != 200:
                    status = "ERROR"
                else:
                    try:
                        resp_json = response.json()
                        result_value = str(resp_json.get("result", "")).upper()
                        status = "FAIL" if result_value == "FAILURE" else "PASS"
                    except json.JSONDecodeError:
                        status = "FAIL"

            except Exception as e:
                status = "ERROR"
                resp_text = str(e)

            # 카운터 증가
            if status == "PASS":
                count_pass += 1
            elif status == "FAIL":
                count_fail += 1
            else:
                count_error += 1

            print(f"[{filename}] → {status}")
            results.append([filename, status, resp_text])

            # 실패한 이미지 복사
            if status in ["FAIL", "ERROR"]:
                shutil.copy(img_path, os.path.join(FAILED_DIR, filename))

# === Summary 계산 ===
total = count_pass + count_fail + count_error
pass_rate = (count_pass / total * 100) if total > 0 else 0
summary_row = ["=== Summary ===", f"Total: {total}", f"PASS: {count_pass}", f"FAIL: {count_fail}", f"ERROR: {count_error}", f"PASS Rate: {pass_rate:.2f}%"]

# === CSV 작성 (Summary → 첫 줄) ===
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(summary_row)
    writer.writerow(["Filename", "Status", "Message"])
    writer.writerows(results)

# === 콘솔 요약 출력 ===
print("\n✅ API 자동화 테스트 완료!")
print(f"📄 결과 CSV: {csv_file}")
print(f"🖼️ 실패 이미지 폴더: {FAILED_DIR}")
print(f"📊 Summary → Total: {total} | PASS: {count_pass} | FAIL: {count_fail} | ERROR: {count_error} | PASS Rate: {pass_rate:.2f}%")