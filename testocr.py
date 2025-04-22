import base64
import io
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import pytesseract
import pandas as pd
import cv2
import numpy as np
import re

def pre_image(img_src):
    base64_string = img_src

    # 접두사 제거
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]

    # 1. Base64 디코딩 및 PIL 이미지 객체로 변환
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))

    # 2. PIL 이미지 → OpenCV로 변환
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # ▶ 노이즈 제거 (가우시안 블러 + Otsu 임계값 + Morph Open)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # 3. 다시 PIL 이미지로 변환
    image = Image.fromarray(cleaned)

    # # 4. 추가 전처리 (PIL 방식)
    image = image.resize((image.width * 2, image.height * 2))  # 확대
    # image = image.filter(ImageFilter.SHARPEN)  # 선명화
    # image = ImageEnhance.Contrast(image).enhance(2.0)  # 대비 증가

    # OCR 분석 결과를 딕셔너리로 반환
    ocr_data = pytesseract.image_to_data(image, lang='eng', output_type=pytesseract.Output.DATAFRAME)

    # 유효한 텍스트만 필터링
    ocr_data = ocr_data[ocr_data.conf != -1]

    # 결과 보기
    print(ocr_data[['text', 'left', 'top', 'width', 'height', 'conf']])
    # 4. OCR 실행 (한글이 포함되어 있다면 lang='kor+eng' 등으로 설정)
    text = pytesseract.image_to_string(image, lang='eng')

    print("📌 인식된 텍스트:", text.strip())

    # # 결과물 이미지 확인용
    # plt.imshow(image, cmap='gray')
    # plt.axis('off')
    # plt.title("fin")
    # plt.show()

    # 6자리 넘치면 자르고, 모자라면 'A'로 채우기
    result = re.sub(r'[^a-zA-Z]', '', text.strip())[:6].ljust(6, 'A')

    print(result)
    return result

# # 실행 테스트
# img_src='data:image/jpeg;base64,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'
# pre_image(img_src)