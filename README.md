## 📌 프로젝트 개요
이 프로젝트는 **Selenium과 BeautifulSoup을 활용하여 웹사이트 자동 로그인 테스트를 수행**하고,  
테스트 결과를 **CSV 파일**과 **스크린샷**으로 저장하는 Python 기반의 자동화 테스트 스크립트입니다.

## 📌 주요 기능
- **Selenium을 활용한 자동 로그인 테스트**
- **BeautifulSoup을 이용한 UI 요소 검증**
- **로그인 성공/실패 결과를 CSV로 저장**
- **테스트 실행 시 스크린샷 자동 저장**
- **다중 사용자 로그인 테스트 지원**
- **ChromeDriver 기반 브라우저 자동 실행**

---

## 📌 설치 방법

### 필수 패키지 설치
```sh
pip install selenium beautifulsoup4 requests


### 실행 방법

1. 필요한 패키지 설치
```sh
pip install selenium beautifulsoup4 requests


2. 테스트 실행

```sh
python selenium_multi_login_test.py

 - CSV 파일: ~/Documents/login_test_results_YYYYMMDD.csv
 - 스크린샷 저장 (로그인 실패 시만 저장됨): ~/Documents/screenshots/
