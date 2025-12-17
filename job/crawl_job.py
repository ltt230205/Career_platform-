
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json

# Cấu hình Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options().add_argument("--start-maximized"))
driver.get("https://www.topcv.vn/tim-viec-lam-nhom-nghe-khac-cr899?category_family=r899")
# Chờ trang tải danh sách job
WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job-item-search-result"))
)

# Lấy tổng số trang
page_text_element = driver.find_element(By.CSS_SELECTOR, "span#job-listing-paginate-text")
page_text = page_text_element.text
match = re.search(r"(\d+)\s*trang", page_text)
total_pages = int(match.group(1)) if match else 1
print(f"Tổng số trang: {total_pages}")

all_jobs = []

# Lặp qua từng trang
for i in range(total_pages):
    print(f"📄 Đang xử lý trang {i+1}/{total_pages}...")
    jobs = driver.find_elements(By.CSS_SELECTOR, "div.job-item-search-result")

    for job in jobs:
        try:
            # --- Lấy title và link ---
            title_el = job.find_element(By.CSS_SELECTOR, "h3.title a")
            title = title_el.text.strip()
            href = title_el.get_attribute("href")

            # --- Lấy tên công ty ---
            company_el = job.find_element(By.CSS_SELECTOR, "a.company span.company-name")
            company_name = company_el.text.strip()

            # --- Lấy lương ---
            salary_el = job.find_element(By.CSS_SELECTOR, "label.title-salary")
            salary = salary_el.text.strip()

            # --- Lấy địa điểm ---
            city_el = job.find_element(By.CSS_SELECTOR, "span.city-text")
            city = city_el.text.strip()

            # --- Lấy kinh nghiệm ---
            exp_el = job.find_element(By.CSS_SELECTOR, "label.exp span")
            exp = exp_el.text.strip()

            all_jobs.append({
                "title": title,
                "company": company_name,
                "salary": salary,
                "location": city,
                "experience": exp,
                "href": href
            })

        except Exception as e:
            print("⚠️ Lỗi khi lấy job:", e)
            continue

    # --- Sang trang tiếp theo ---
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next »']")
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)
    except Exception:
        print("✅ Hết trang.")
        break

driver.quit()

# --- Lưu ra file JSON ---
with open("job.json", "a", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=4)

print(f"✅ Hoàn tất! Đã lưu {len(all_jobs)} job vào job.json")

