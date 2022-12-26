# Python program for booking CGV movie ticket.


매진된 CGV 영화표의 예매를 도와주는 파이썬 프로그램입니다.  
원하는 자리에 표가 나올 때 까지 새로고침하여 예약을 시도합니다.


## 다운
```cmd
git clone https://github.com/dhgwag/cgv_reservation.git
```
  
## 필요
- 파이썬 3.8에서 테스트 했습니다.

```py
pip install -r requirements.txt
```


## Configuration
**Config.py를 항목에 맞춰 변경**  
```text
user_id = ""                # CGV 회원번호
user_pw = ""                # CGV 비밀번호

movie = '아바타-물의길'        # 영화 이름
movie_type = 'IMAX'         # 상영관 종류
theater_area = '서울'         # 지역
theater = '용산아이파크몰'     # 영화관
day = '7'                   # 날짜 (일)
movie_time = '26:10'        # 영화 시간
adult = '2'                 # 일반 인원
youth = '0'                 # 청소년 인원
row_from = 5                # 검색할 row 시작, A = 1
row_to = 8                  # 검색할 row 끝
column_from = 10            # 검색할 column 시작
column_to = 20              # 검색할 column 끝

telegram_token = ""
telegram_id = ""

# 예약 성공 여부 텔레그램 수신 시 아래 정보 필요, 비워두면 텔레그램 무시
telegram_token = "" #"123456789:SDBn-Kn2fdze1eEAL7fefawa1yLo0pjRAUc"
telegram_id = "" #"123548689"
```


**Telegram으로 알림 받기**
token과 id는 아래 링크 참조하여 생성

https://gabrielkim.tistory.com/entry/Telegram-Bot-Token-%EB%B0%8F-Chat-Id-%EC%96%BB%EA%B8%B0

## 간단 사용법

```cmd
python main.py
```