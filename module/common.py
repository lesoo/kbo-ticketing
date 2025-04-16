import time
import datetime

def get_booking_site(home_team):
    match home_team:
        case "SAMSUNG" | "LG" | "KIA" | "KT" | "SSG" | "HANHWA":
            return "ticket_link"
        case "DOOSAN" | "KIWOOM":
            return "interpark"
        case "LOTTE":
            return "lotte"
        case _:
            return "-1"# unknown team

def match_team(home_team):
    match home_team:
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


def wait_until_target_time_and_refresh(driver, function, target_minute, target_second):
    while True:
        # 현재 시간 구하기
        now = datetime.datetime.now()
        current_minute = now.minute
        current_second = now.second

        # 목표 시간이 되면 새로고침
        if current_minute == target_minute and current_second == target_second:
            print(f"목표 시간 ({now.hour}:{target_minute}:{target_second}) 도달! 페이지 새로고침 중...")
            driver.refresh()  # 페이지 새로고침
            function(driver)
            break

        # 목표 시간이 아닐 경우 잠시 대기 (0.1초마다 확인)
        time.sleep(0.1)