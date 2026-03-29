from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from io import BytesIO


class Extractor:

    def get_id(driver,args):
        return driver.find_element(By.ID, args['id'])
    
    def get_class_name(driver,args):
        return driver.find_element(By.CLASS_NAME, args['class_name'])
    
    def get_xpath(driver,args):
        return driver.find_element(By.XPATH, args['xpath'])
    
    def get_css_selector(driver,args):
        return driver.find_element(By.CSS_SELECTOR, args['css_selector'])
    
    def get_tag_name(driver,args):
        return driver.find_element(By.TAG_NAME, args['tag_name'])
    
    def get_link_text(driver,args):
        return driver.find_element(By.LINK_TEXT, args['link_text'])
    
    # ----------------------------------------------
class ExtractorList:
    
    def get_id_list(driver,args):
        return driver.find_elements(By.ID, args['id'])
    
    def get_class_name_list(driver,args):
        return driver.find_elements(By.CLASS_NAME, args['class_name'])
    
    def get_xpath_list(driver,args):
        return driver.find_elements(By.XPATH, args['xpath'])
    
    def get_css_selector_list(driver,args):
        return driver.find_elements(By.CSS_SELECTOR, args['css_selector'])
    
    def get_tag_name_list(driver,args):
        return driver.find_elements(By.TAG_NAME, args['tag_name'])
    
    def get_link_text_list(driver,args):
        return driver.find_elements(By.LINK_TEXT, args['link_text'])
    
    def get_link_css(driver, args):
        selector = args.get('css_selector')
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        links = [el.get_attribute('href') for el in elements if el.get_attribute('href')]
        return links