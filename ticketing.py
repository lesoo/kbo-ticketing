import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# TODO : 더 세세한 모듈화 및 전체적인 refactoring 필요
#       팝업 확인버튼, 팝업 이동해서 캡차 인식후 입력, 자리선정, 결제까지
load_dotenv()

# 크롬 옵션 설정
options = Options()
options.add_argument(f"user-data-dir=C:\\Users\\{os.getenv('OS_USER_PROFILE')}\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("profile-directory=Default")
# TODO : 불필요 옵션 제거 필요
options.add_argument("--disable-infobars")  # 자동화 메시지 제거
# options.add_argument("--headless")          # UI 없이 백그라운드에서 실행
options.add_argument("--no-sandbox")        # 보안 샌드박스 비활성화
options.add_argument("--disable-extensions")  # 확장 프로그램 비활성화
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')  # 일반적인 User-Agent 사용
options.add_argument('--disable-blink-features=AutomationControlled') # 자동화 감지 모드 우회


# 크롬 드라이버 서비스 설정
service = Service()

def setup_driver():
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login_to_payco(driver):
    # PAYCO 로그인 페이지로 이동
    login_url = "https://id.payco.com/oauth2.0/authorize?serviceProviderCode=TKLINK&scope=&response_type=code&state=f2908e118061402fb049299d1d30b90e&client_id=Z9Ur2WLH9rB59Gy4_cJ3&redirect_uri=https://www.ticketlink.co.kr/auth/callback?selfRedirect=N&userLocale=ko_KR"
    driver.get(login_url)

    try:
        # 로그인 폼 로딩 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "id"))
        )

        # 로그인 정보 입력
        driver.find_element(By.ID, "id").send_keys(os.getenv("PAYCO_ID"))  # 사용자 ID 입력
        driver.find_element(By.ID, "pw").send_keys(os.getenv("PAYCO_PW"))  # 사용자 비밀번호 입력

        # 로그인 버튼 클릭
        login_button = driver.find_element(By.ID, "loginButton")
        login_button.click()

        # 로그인 완료 대기 (로그인 후 나타나는 요소 ID로 변경 필요)
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "some_element_after_login"))
        )
        print("로그인 성공.")
    except Exception as e:
        print(f"로그인 오류 발생: ")#{e}") # TODO : 드라이버 오류 처리 or 에러 핸들링

def match_team():
    match os.getenv("HOME_TEAM"):
        case "SAMSUNG":
            return "57"
        case "LG":
            return "59"
        case "KIA":
            return "58"
        case "KT":
            return "62"
        case "SSG":
            return "476"
        case "HANHWA":
            return "63"

def navigate_to_ticket_page(driver):
    team_link = match_team()
    ticket_page_url = f"https://www.ticketlink.co.kr/sports/137/{team_link}"

    driver.get(ticket_page_url)

    try:
        # 예약 페이지 로딩 대기
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "planTitle"))  # 예약 페이지의 특정 요소 class로 변경
        )
        print("예약 페이지 접근 성공.")
    except Exception as e:
        print(f"예약 페이지 접근 오류 발생: ")#{e}") # TODO : 드라이버 오류 처리 or 에러 핸들링

def select_date(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="reservation"]/div[2]/ul/li[6]/div[3]'))# TODO :수정 필요
        )
        # 클릭
        element.click()

    except Exception as e:
        print(f"오류 발생: {e}")


def wait_until_target_time_and_refresh(driver, target_hour, target_minute, target_second):
    while True:
        # 현재 시간 구하기
        now = datetime.datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        current_second = now.second

        # 목표 시간이 되면 새로고침
        if current_hour == target_hour and current_minute == target_minute and current_second == target_second:
            print(f"목표 시간 ({target_hour}:{target_minute}:{target_second}) 도달! 페이지 새로고침 중...")
            driver.refresh()  # 페이지 새로고침
            select_date(driver)  # 날짜 선택 함수 실행
            break

        # 목표 시간이 아닐 경우 잠시 대기 (0.1초마다 확인)
        time.sleep(0.1)

def main():
    driver = setup_driver()

    try:
        login_to_payco(driver)  # PAYCO 로그인
        navigate_to_ticket_page(driver)  # 티켓 페이지로 이동
        # select_date(driver)
        wait_until_target_time_and_refresh(driver, 10, 59, 59) # 목표 시간까지 대기/페이지 새로고침/예매버튼 클릭
        # TODO : 시간은 main함수에 입력하도록 수정
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        input("창을 닫으려면 엔터 키를 누르세요...")
        driver.quit()

if __name__ == "__main__":
    main()