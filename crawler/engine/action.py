from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from io import BytesIO
from selenium.webdriver.common.keys import Keys

class Action:
    def click(driver, args):
        element = driver.find_element(By.XPATH, args['xpath'])
        element.click()

    def click_css(driver, args):
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, args['css_selector'])
            driver.execute_script("arguments[0].click();", next_btn)  # Dùng JS click để tránh bị che khuất
            time.sleep(2)  # Đợi trang load danh mục mới
        except Exception as e:
            print("Hết trang hoặc không tìm thấy nút mũi tên:", e)
        
    def send_keys(driver, args):
        element = driver.find_element(By.XPATH, args['xpath'])
        element.send_keys(args['keys'])
        
    def wait_for_element(driver, args):
        wait = WebDriverWait(driver, args.get('timeout', 10))
        wait.until(EC.presence_of_element_located((By.XPATH, args['xpath'])))

    def wait_for_css_element(driver, args):
        wait = WebDriverWait(driver, args.get('timeout', 10))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, args['css_selector'])))
        
    def delete_text(driver, args):  
        element = driver.find_element(By.XPATH, args['xpath'])
        element.clear()
        
    def enter_key(driver, args):
        element = driver.find_element(By.XPATH, args['xpath'])
        element.send_keys(Keys.ENTER)
        
    def hover_over(driver, args):
        from selenium.webdriver import ActionChains
        element = driver.find_element(By.XPATH, args['xpath'])
        action = ActionChains(driver)
        action.move_to_element(element).perform()
        
