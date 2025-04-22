import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import module.common as cm
import module.move_page as mp
import module.captcha as cc

import traceback

# TODO : 팝업 이동해서 캡차 인식후 입력, 자리선정, 결제까지 - 접근 불가
#       인터파크 추가
load_dotenv()

# 크롬 옵션 설정
options = Options()
options.add_argument(f"user-data-dir=C:\\Users\\{os.getenv('OS_USER_PROFILE')}\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("profile-directory=Default")
options.add_argument('--disable-blink-features=AutomationControlled') # 자동화 감지 모드 우회

# 크롬 드라이버 서비스 설정
service = Service()

def setup_driver():
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def ticketing_with_ticket_link():
    driver = setup_driver()
    try:
        mp.login_to_payco(driver)  # PAYCO 로그인
        mp.navigate_to_ticket_page(driver)  # 티켓 페이지로 이동

        test_mode = os.getenv("TEST_MODE")
        if test_mode == 'Y':
            mp.select_date(driver)
        else :
            cm.wait_until_target_time_and_refresh(driver, mp.select_date, int(os.getenv("MINUTE")), int(os.getenv("SECOND"))) # 목표 시간까지 대기/페이지 새로고침/예매버튼 클릭

    except Exception as e:
        print(f"오류 발생: {e}")
        traceback.print_exc()
    finally:
        input("창을 닫으려면 엔터 키를 누르세요...")
        driver.quit()

def ticketing_with_interpark():
    driver = setup_driver()
    try:
        mp.move_to_interpark(driver)  # PAYCO 로그인
        mp.navigate_to_interpark_ticket_page(driver)  # 티켓 페이지로 이동

        test_mode = os.getenv("TEST_MODE")
        if test_mode == 'Y':
            mp.select_date_interpark(driver)
        else :
            cm.wait_until_target_time_and_refresh(driver, mp.select_date_interpark, int(os.getenv("MINUTE")), int(os.getenv("SECOND"))) # 목표 시간까지 대기/페이지 새로고침/예매버튼 클릭

        captcha = cc.pass_captcha(driver)


    except Exception as e:
        print(f"오류 발생: {e}")
        traceback.print_exc()
    finally:
        input("창을 닫으려면 엔터 키를 누르세요...")
        driver.quit()


# if __name__ == "__main__":
#     main()