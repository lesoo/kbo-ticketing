from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import base64
import io
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import pytesseract
import pandas as pd
import cv2
import numpy as np
import testocr as ocr
import time

import traceback

# TODO : 예매 순번 대기 페이지 처리해야함

# 예매대기 페이지 1시간까지 대기하는 임시코드(쓸지 안쓸지 모름)
def wait_for_page_load(driver):
    WebDriverWait(driver, 3600).until(EC.presence_of_element_located((By.ID, "imgCaptcha")))  # body 태그가 로드될 때까지 대기

# captcha 이미지 base64로 가져오기기
def get_image(driver):
    WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "imgCaptcha"))
        )
    img_element = driver.find_element(By.ID, "imgCaptcha")

    # 이미지 src 속성 추출
    img_src = img_element.get_attribute("src")
    return img_src

# captcha 이미지 엘리먼트 존재하는지 판별
def get_is_passed(driver):
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "imgCaptcha"))
        )
        return True
    except Exception:
        return False  # 요소를 찾을 수 없거나 오류 발생 시 False 반환

# 얘가 main
# captcha 처리 func
# - captcha 이미지 존재 여부로 성공/실패 판단하고 실패 시 재시도
def pass_captcha(driver):
    wait_for_page_load(driver) # captcha 이미지 뜰때까지 최대 1시간 대기
    # 1. is_passed 판별
    #  > T > captcha 진행
    #  > F > break
    is_passed = get_is_passed(driver)
    while is_passed:
        try:
            is_passed = get_is_passed(driver)
            print(is_passed)
            img_src = get_image(driver)
            captcha_ele = driver.find_element(By.ID, "txtCaptcha")
            captcha_text = ocr.pre_image(img_src)
            captcha_ele.clear()  # 기존 입력값 삭제
            captcha_ele.send_keys(captcha_text + '\n')
        except Exception as e:
            if 'stale element reference: stale element not found in the current frame' in str(e):
                break
        finally:
            time.sleep(0.2) # 이전 이미지 중복인식 문제로 추가
            is_passed = get_is_passed(driver)
