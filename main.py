import os
import module.common as cm
import module.ticketing as tk

# TODO : 팝업 이동해서 캡차 인식후 입력, 자리선정, 결제까지 - 접근 불가
#       인터파크 추가

def main():
    booking_site = cm.get_booking_site(os.getenv("HOME_TEAM"))
    match(booking_site):
        case "ticket_link": # TODO : 아래 내용 function으로 만들기
            tk.ticketing_with_ticket_link()
        case "interpark":
            try:
                tk.ticketing_with_interpark()
            except Exception as e:
                print(f"오류 : {e}")

if __name__ == "__main__":
    main()