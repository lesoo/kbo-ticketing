# kbo-ticketing

## ENV
- OS_USER_PROFILE - chrome 위치 설정할 OS 사용자명
- TEST_MODE - 테스트모드(Y/N) 즉시실행 YN (N일때는 새로고침 시각 설정 필요)
- PAYCO_ID - 페이코 로그인 아이디
- PAYCO_PW - 페이코 로그인 패스워드


- 인터파크?
- 인터파크는 자동로그인 상태라는 가정 하에 개발 진행

- HOME_TEAM - 팀명(SAMSUNG, LG, KIA, KT, SSG, HANHWA)
- MATCH_INDEX - 경기 목록 중 순서
- MINUTE - 새로고침 분
- SECOND - 새로고침 초


## TODO
1. ~~불필요한 크롬 실행 옵션 제거~~
2. 티케팅 사이트 이동 후 실행동작 가능한지 확인
3. 크롬 에러 핸들링
4. ~~실행 모드에서 시간 입력 위치 지정하는 부분 정하기~~
5. ~~모듈 구분(refactoring)~~
6. 팀별로 예매 사이트 구분? 환경변수 추가해서 예매사이트 구분? 할지 결정하고 진행
7. ~~인터파크 예매 개발~~
8. ~~인터파크 캡챠 뚫기~~
    <br>(8-1. captcha 정확도 올리기)
9. 실전 테스트 및 예매순번 대기 페이지 처리 추가
10. 인터파크 좌석 선택 및 예매
11. 인터파크 결제
