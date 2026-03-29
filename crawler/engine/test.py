from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from io import BytesIO
import json

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

try:
    # 2. Truy cập vào trang tìm việc của TopCV
    driver.get("https://www.topcv.vn")
    
    # 3. Chờ 3 giây để trang tải xong nội dung
    time.sleep(3)

    # 4. Tìm tất cả các thẻ chứa tên ngành nghề
    # Selector này nhắm vào các tiêu đề trong phần "Việc làm theo ngành nghề"
    elements = driver.find_elements(By.CSS_SELECTOR, "a.category-level-1__option-text")

    print(f"Tìm thấy {len(elements)} ngành nghề:\n")
    print(elements)

    # 5. Duyệt qua danh sách và in ra tên
    for i, el in enumerate(elements, 1):
        print(f"{i}. {el.text.strip()}")

finally:
    # 6. Đóng trình duyệt
    driver.quit()