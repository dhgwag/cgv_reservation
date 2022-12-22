import os
import time
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from cgv.exceptions import InvalidMovieError
from config import *
import telegram

# Chromedriver 없을 시 처음에는 자동으로 설치합니다.
chromedriver_path = r'C:\workspace\chromedriver.exe'

class CGV:
    def __init__(self):
        # Login
        self.login_id = user_id
        self.login_psw = user_pw

        # Telegram
        self.token = telegram_token
        self.id = telegram_id

        self.driver = None


    def telegram_logging(self, msg):
        if self.token != "" and self.id != "":
            bot = telegram.Bot(token=self.token)
            bot.sendMessage(chat_id=self.id, text=msg)


    def run_driver(self):
        try:
            self.driver = webdriver.Chrome(executable_path=chromedriver_path)
            return True
        except WebDriverException:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            return False


    def login(self):
        self.driver.get('https://www.cgv.co.kr/user/login/?returnURL=https%3a%2f%2fwww.cgv.co.kr%2fdefault.aspx')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'txtUserId'))
        )

        self.driver.find_element(By.ID, 'txtUserId').send_keys(str(self.login_id))
        self.driver.find_element(By.ID, 'txtPassword').send_keys(str(self.login_psw))
        self.driver.find_element(By.ID, 'submit').click()
        self.driver.implicitly_wait(1)
        return True


    def check_login(self):
        self.driver.get('http://www.cgv.co.kr/ticket/')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.header_content"))
        )

        header_text = self.driver.find_element(By.CSS_SELECTOR, "div.header_content").text

        if "로그아웃" in header_text:
            # self.telegram_logging("로그인 성공. 예약을 시도합니다")
            return True
        else:
            self.telegram_logging("로그인 실패. 재시도 해주세요")
            self.driver.quit()
            sys.exit()
            return False


    def find_movie_date(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "ticket_iframe"))
        )
        self.driver.switch_to.frame("ticket_iframe")

        # 영화 이름 클릭
        try:
            self.driver.find_element(By.XPATH, f"//a[@title='{movie}']").click()
        except:
            raise InvalidMovieError(f"영화 이름 오류. '{movie}' 은/는 목록에 없습니다.")
        time.sleep(1)

        # 영화관 타입 클릭
        try:
            self.driver.find_element(By.XPATH, f"//a[@data-type='{movie_type}']").click()
        except:
            raise InvalidMovieError(f"영화관 타입 오류. '{movie_type}' 은/는 목록에 없습니다.")
        time.sleep(1)

        # 영화관 지역 클릭
        try:
            self.driver.find_element(By.XPATH, f"//span[@class='name' and text()='{theater_area}']").click()
        except:
            raise InvalidMovieError(f"영화관 지역 오류. '{theater_area}' 은/는 목록에 없습니다.")
        time.sleep(1)

        # 영화관 이름 클릭
        try:
            self.driver.find_element(By.XPATH, f"//a[contains(text(),'{theater}')]").click()
        except:
            raise InvalidMovieError(f"영화관 이름 오류. '{theater}' 은/는 목록에 없습니다.")
        time.sleep(1)

        # 날짜 클릭
        try:
            self.driver.find_element(By.XPATH, f"//span[@class='day' and text()='{day}']").click()
        except:
            raise InvalidMovieError(f"날짜 오류. '{day}'일은 목록에 없습니다.")
        time.sleep(1)

        # 시간 클릭
        try:
            self.driver.find_element(By.XPATH, f"//span[@class='time']/span[text()='{movie_time}']").click()
        except:
            raise InvalidMovieError(f"시간 오류. '{movie_time}'은 목록에 없습니다.")
        time.sleep(1)

        # 좌석선택 클릭
        try:
            self.driver.find_element(By.XPATH, f"//a[@title='좌석선택']").click()
        except:
            raise InvalidMovieError(f"좌석선택 클릭 오류.")


    def find_seat(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='확인']"))
        )

        time.sleep(5)

        # 팝업 제거
        try:
            cnt = 1
            print(len(self.driver.find_elements(By.XPATH, f"//a[text()='닫기']")))
            print(self.driver.find_elements(By.XPATH, f"//a[text()='닫기']"))
            for item in list(reversed(self.driver.find_elements(By.XPATH, f"//a[text()='닫기']"))):
                item = item.find_element(By.XPATH, f"//a[text()='닫기']")
                print(f"{cnt}  {item.is_displayed()}  {item.is_enabled()}")
                # if item.is_displayed() and item.is_enabled():
                try:
                    item.click()
                except:
                    print("error")
                    pass
                cnt+=1
        except:
            raise InvalidMovieError(f"팝업 제거 오류")


    def run(self):
        self.run_driver()
        self.login()
        self.check_login()
        self.find_movie_date()
        self.find_seat()
        # self.refresh_search_result()

        # print(self.driver.page_source)