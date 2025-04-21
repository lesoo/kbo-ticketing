# from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import base64
import io
# from PIL import Image
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import pytesseract
import pandas as pd
import cv2
import numpy as np

def get_image(driver):
    WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "imgCaptcha"))  # 예약 페이지의 특정 요소 class로 변경
        )
    img_element = driver.find_element(By.ID, "imgCaptcha")

    # 이미지 src 속성 추출
    img_src = img_element.get_attribute("src")
    return img_src
    # print(f"이미지 src: {img_src}")

def pass_captcha(driver):
    img_src = get_image(driver)
    print(img_src)

    # Base64 이미지 문자열 (예: data:image/jpeg;base64,... 형태라면 'data:image/jpeg;base64,' 부분 제거)
    base64_string = img_src #"여기에_캡챠_이미지_base64_문자열_전체_붙여넣기"

    # 필요시 접두사 제거
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]

    # # 2. 디코딩 및 PIL 이미지 객체로 변환
    # image_data = base64.b64decode(base64_string)
    # image = Image.open(io.BytesIO(image_data))

    # # 3. 이미지 전처리 (OCR 성능 향상용)
    # image = image.convert("L")  # 흑백 변환
    # image = image.resize((image.width * 2, image.height * 2))  # 해상도 업
    # image = image.filter(ImageFilter.SHARPEN)  # 선명하게
    # image = ImageEnhance.Contrast(image).enhance(2.0)  # 대비 증가

    # 1. Base64 디코딩 및 PIL 이미지 객체로 변환
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))

    # 2. PIL 이미지 → OpenCV로 변환
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # # ▶ 노이즈 제거 (가우시안 블러 + Otsu 임계값 + Morph Open)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # kernel = np.ones((2, 2), np.uint8)
    # cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # 1. 블러링
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 2. 이진화 (Otsu 또는 적응형)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # 3. 모폴로지 연산
    kernel = np.ones((3,3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel, iterations=1)

    # 4. 미디안 블러
    denoised = cv2.medianBlur(closed, 3)

    # 5. 작은 연결 요소 제거
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(denoised, 8, cv2.CV_32S)
    min_size = 50  # 이 값은 이미지에 따라 조정 필요
    result = np.zeros_like(denoised)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            result[labels == i] = 255

    # 3. 다시 PIL 이미지로 변환
    image = Image.fromarray(result)

    # 4. 추가 전처리 (PIL 방식)
    image = image.resize((image.width * 2, image.height * 2))  # 확대
    image = image.filter(ImageFilter.SHARPEN)  # 선명화
    image = ImageEnhance.Contrast(image).enhance(2.0)  # 대비 증가

    # 5. OCR 실행
    # text = pytesseract.image_to_string(image, lang='eng')  # 필요 시 lang='kor+eng'


    # OCR 분석 결과를 딕셔너리로 반환
    ocr_data = pytesseract.image_to_data(image, lang='eng', output_type=pytesseract.Output.DATAFRAME)

    # 유효한 텍스트만 필터링
    ocr_data = ocr_data[ocr_data.conf != -1]

    # 결과 보기
    print(ocr_data[['text', 'left', 'top', 'width', 'height', 'conf']])
    # 4. OCR 실행 (한글이 포함되어 있다면 lang='kor+eng' 등으로 설정)
    # text = pytesseract.image_to_string(image, lang='eng')

    # print("📌 인식된 텍스트:", text.strip())

    plt.imshow(image, cmap='gray')
    plt.axis('off')
    # plt.title("전처리된 이미지(OCR 대상)")
    plt.show()

