import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import module.module as md

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


def navigate_to_ticket_page(driver):
    team_link = md.match_team(os.getenv("HOME_TEAM"))
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
        xpath = f'//*[@id="reservation"]/div[2]/ul/li[{os.getenv("MATCH_INDEX")}]/div[3]'
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()

    except Exception as e:
        print(f"예매버튼 클릭 오류 발생: {e}")
    finally:
        try:
            confirm = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[3]/button'))
            )
            confirm.click()
        except Exception as e:
            print(f"예매버튼 확인 클릭 오류 발생: {e}")

