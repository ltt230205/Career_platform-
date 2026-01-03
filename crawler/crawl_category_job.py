from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.topcv.vn/viec-lam")

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.category-level-1__option-text")
        )
    )

    all_items = {}

    for _ in range(5):
        items = driver.find_elements(By.CSS_SELECTOR, "a.category-level-1__option-text")

        for item in items:
            title = item.text.strip()
            href = item.get_attribute("href")
            if title:
                all_items[title] = href

        try:
            next_btn = driver.find_element(
                By.CSS_SELECTOR,
                "i.category-level-1__header-pagination-action-icon.next"
            )
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(2)
        except Exception:
            break

finally:
    driver.quit()

with open("job_category.json", "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=4)
