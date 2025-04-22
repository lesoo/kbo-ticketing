import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import module.common as cm

# 티켓링크 페이코 로그인
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

# 인터파크 이동(자동로그인 상태)
def move_to_interpark(driver):
    try:
        url = "https://tickets.interpark.com/"
        driver.get(url)
    except Exception as e:
        print(f"인터파크 오류 발생: ")#{e}") # TODO : 드라이버 오류 처리 or 에러 핸들링

# 티켓링크 야구 예매 페이지 이동
def navigate_to_ticket_page(driver):
    team_link = cm.match_team(os.getenv("HOME_TEAM"))
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

# 인터파크 야구 예매 페이지 이동
def navigate_to_interpark_ticket_page(driver):
    team_link = cm.match_team(os.getenv("HOME_TEAM"))
    ticket_page_url = f"https://ticket.interpark.com/m-ticket/Sports/GoodsInfo?SportsCode=07001&TeamCode={team_link}"

    driver.get(ticket_page_url)

    try:
        # 예약 페이지 로딩 대기
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MobileTimeScheduleList"))  # 예약 페이지의 특정 요소 class로 변경
        )
        print("예약 페이지 접근 성공.")
    except Exception as e:
        print(f"예약 페이지 접근 오류 발생: ")#{e}") # TODO : 드라이버 오류 처리 or 에러 핸들링

# 티켓링크 경기 일정 선택
def select_date(driver):
    try:
        #env에서 경기 순서로 선태 TODO : 날짜로 선택하도록
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

# 인터파크 경기 일정 선택
def select_date_interpark(driver):
    try:
        # TODO : 경기 날짜로 선택하도록 수정
        xpath = f'//*[@id="contents"]/div[6]/div[{os.getenv("MATCH_INDEX")}]/div[3]/a'

        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

        driver.execute_script("arguments[0].click();", element) #강제 클릭

    except Exception as e:
        print(f"예매버튼 클릭 오류 발생: {e}")

    finally:
        try:
            # 새로 생성된 탭으로 전환
            tabs = driver.window_handles
            driver.switch_to.window(tabs[-1])

            # 알림창 전환 후 confirm
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = Alert(driver)
            alert.accept()

        except Exception as e:
            print(f"예매버튼 확인 클릭 오류 발생: {e}")

