import time
import os
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup

# 경로 설정
BASE_DIR = os.path.expanduser("~/Documents")  # 저장 위치
TODAY = datetime.now().strftime("%Y%m%d")  # 날짜별 파일 생성
CSV_FILE = os.path.join(BASE_DIR, f"login_test_results_{TODAY}.csv")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

# 스크린샷 폴더 생성 (없으면 생성)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# 테스트할 사용자 리스트
users = [
    {"email": "email_1@example.com", "password": "password_1"},
    {"email": "email_2@example.com", "password": "password_2"},
    {"email": "email_3@example.com", "password": "password_3"}
]

# Selenium 브라우저 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# 로그인 관련 URL 설정
LOGIN_URL = "https://url.co.kr/login"
DASHBOARD_URL = "https://url.co.kr/login"


def save_test_result(user_email, test_name, expected, actual, result, screenshot_path):
    """테스트 결과를 CSV 파일에 저장"""
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([user_email, test_name, expected, actual, result, screenshot_path])


def capture_screenshot(user_email, status):
    """로그인 성공/실패 시 스크린샷 저장"""
    filename = f"{user_email}_{status}.png"
    screenshot_path = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(screenshot_path)
    return screenshot_path


def login_user(email, password):
    """사용자 로그인 및 테스트 실행"""
    driver.get(LOGIN_URL)
    time.sleep(3)  # 페이지 로드 대기

    try:
        # 이메일 입력
        email_input = driver.find_element(By.NAME, "email")
        email_input.clear()
        email_input.send_keys(email)

        # 비밀번호 입력
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(password)

        # 로그인 버튼 클릭
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        time.sleep(5)  # 로그인 처리 대기

        # 로그인 성공 여부 확인 (URL 기반)
        if DASHBOARD_URL in driver.current_url:
            login_result = "로그인 성공"
            login_status = "Pass"
        else:
            login_result = "로그인 실패"
            login_status = "Fail"

        # BeautifulSoup을 활용하여 UI 요소 확인
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        welcome_text = soup.find("h1")

        actual_result = f"{login_result}, UI 요소: {welcome_text.text.strip() if welcome_text else 'N/A'}"
        screenshot_path = capture_screenshot(email, "success" if login_status == "Pass" else "fail")

        save_test_result(email, "로그인 테스트", "대시보드 이동", actual_result, login_status, screenshot_path)
        print(f"{email} - {login_result} (스크린샷 저장됨: {screenshot_path})")

    except (NoSuchElementException, TimeoutException) as e:
        error_message = f"오류 발생: {str(e)}"
        screenshot_path = capture_screenshot(email, "error")
        save_test_result(email, "로그인 테스트", "대시보드 이동", error_message, "Fail", screenshot_path)
        print(f"{email} - {error_message} (스크린샷 저장됨: {screenshot_path})")


# CSV 파일 헤더 추가 (처음 실행 시)
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["사용자 이메일", "테스트 명", "기대 결과", "실제 결과", "Pass/Fail", "스크린샷"])

# 모든 사용자 로그인 테스트 실행
for user in users:
    login_user(user["email"], user["password"])

# 브라우저 종료
driver.quit()
print(f"\n 로그인 테스트 완료. 결과가 {CSV_FILE} 파일에 저장되었습니다.")
