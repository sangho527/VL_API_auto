# API 자동화 Tool 

### 🧩 프로젝트 개요
`splitVideo`는 영상 데이터를 자동으로 이미지로 분리 (API 테스트 첨부용) <br>
`VL_API_auto`는 각 이미지를 대상으로 API 호출 및 응답 상태를 자동으로 검증하기 위한 스크립트 입니다.

#### 주요 구성
| 파일명 | 설명 |
|--------|------|
| **API_Auto.py** | 추출된 이미지를 지정된 API에 자동 업로드하고 응답 결과를 CSV로 정리 |
| **splitVideo.py** | 영상 파일을 일정 간격으로 분리하여 가장 선명한 프레임만 추출 |

### 🚀 실행 환경

#### 1️⃣ 요구 사항
- Python 3.8 이상
- 패키지 의존성:
  ```bash
  pip install requests opencv-python numpy

## 1. [VL_API_auto](https://github.com/sangho527/VL_API_auto/blob/main/API%20테스트%20자동화/API_Auto.py)

> 각 이미지에 대해 API 응답을 자동 테스트하는 QA/테스트 자동화 도구입니다.

### 기능
	•	지정한 이미지 폴더 내 모든 이미지에 대해 API를 자동 호출
	•	요청 성공 여부, 응답 JSON 파싱 결과를 자동 분류 (PASS / FAIL / ERROR)
	•	결과 요약 및 실패 이미지 복사 기능 포함
	•	CSV로 결과 자동 저장 (통계 포함)

---

## 2. [splitVideo](https://github.com/sangho527/VL_API_auto/blob/main/스캔%20영상%20split/splitVideo.py)

> 영상 데이터를 자동으로 이미지 파일로 분리(split)하는 자동화 도구입니다.

### 기능
    •	지정한 영상(.mp4, .mov 등)을 일정 간격(초 단위)으로 프레임 분리
    •	각 구간(interval)마다 가장 선명한 이미지(Sharpness 기준) 를 자동 선택
    •	추출된 이미지를 지정된 폴더에 저장
