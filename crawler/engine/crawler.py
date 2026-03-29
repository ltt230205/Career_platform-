from unittest import result
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from io import BytesIO
# from .action import Action
# from .extract import Extractor, ExtractorList
from action import Action
from extract import Extractor, ExtractorList




class SeleniumCrawler:

    @staticmethod
    def action(driver, args):
        func=args.get('action')
        if hasattr(Action, func):
            method = getattr(Action, func)
            method(driver ,args)

    def close(self):
        self.driver.quit()  

    @staticmethod
    def extract(driver, args):
        if args.keys() == 'extract':
            name_element=args.get('name_element')
            func=args.get('extract')
            if hasattr(Extractor, func):
                method = getattr(Extractor, func)
                elements = method(driver ,args)
                return {name_element: elements.text.strip()}
            
        
        if 'extract_list' in args:
            dict_element = {}
            func=args.get('extract_list')
            name_element=args.get('name_element')
            if hasattr(ExtractorList, func):
                method = getattr(ExtractorList, func)
                elements = method(driver, args)
                for i, el in enumerate(elements, 1):
                    if isinstance(el, str):
                        val = el.strip()
                    # Nếu el là đối tượng Selenium - trường hợp lấy text
                    else:
                        val = el.text.strip()
                    dict_element[f"{i}"] = {name_element: val}
                return dict_element
        return {}

    @staticmethod
    def read_file_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def write_file_json(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def merge_dict(dict_element_src, dict_element_dst):
        """
        Gộp dữ liệu từ dict_src vào dict_dst dựa trên key (ví dụ key '1', '2'...)
        """
        # Duyệt qua từng item trong dictionary nguồn
        for key, value in dict_element_src.items():
            if key in dict_element_dst:
                # Nếu key '1' đã tồn tại ở dict đích, ta gộp dict con bên trong
                # dict_element_dst['1'].update({'link': 'abcd'})
                dict_element_dst[key].update(value)
            else:
                # Nếu key '1' chưa có ở dict đích, tạo mới hoàn toàn
                dict_element_dst[key] = value
        return dict_element_dst
        

    @staticmethod
    def run_category(json_path):
        data_json = SeleniumCrawler.read_file_json(json_path)
        repeat= data_json.pop('repeat')
        driver_path = data_json.pop('url')
        steps = data_json.pop('steps') # Lấy danh sách các bước

        list_names = []
        for step in steps:
            if step.get('type') == 'extract':
                args = step.get('args', {})
                name = args.get('name_element')
                if name:
                    list_names.append(name)

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(data_json['url_web'])  # Sử dụng url từ data_json
        for i in range(repeat):
            dict_element = {}
            index=0
            for step in steps:
                if step['type'] == 'action':   
                    SeleniumCrawler.action(driver, step['args'])
                elif step['type'] == 'extract':
                    index += 1
                    if index == 1:
                        dict_element = SeleniumCrawler.extract(driver, step['args'])
                    if index > 1:
                        final_dict = SeleniumCrawler.merge_dict(dict_element, SeleniumCrawler.extract(driver, step['args']))
                        dict_element = final_dict
                    # Lưu dict vào file json        
            SeleniumCrawler.write_file_json(f'output/topcv_category_output_trang_{i+1}.json', dict_element)
        driver.quit()

        # for i in range(repeat):
        #     # 1. QUAN TRỌNG: Khởi tạo dict rỗng ở đầu mỗi lượt lặp i
        #     dict_element = {} 
        #     index = 0
            
        #     for step in steps:
        #         # Tạo bản sao args để tránh lỗi pop dữ liệu khi repeat > 1
        #         current_args = step['args'].copy() 
                
        #         if step['type'] == 'action':   
        #             SeleniumCrawler.action(driver, current_args)
        #         elif step['type'] == 'extract':
        #             index += 1
        #             extracted_data = SeleniumCrawler.extract(driver, current_args)
                    
        #             if index == 1:
        #                 dict_element = extracted_data
        #             else:
        #                 # Gộp dữ liệu mới vào dữ liệu đã có
        #                 dict_element = SeleniumCrawler.merge_dict(dict_element, extracted_data)
            
        #     # 2. QUAN TRỌNG: Đẩy lệnh lưu file ra ngoài vòng lặp 'for step in steps'
        #     # Chỉ lưu sau khi đã thực hiện XONG tất cả các bước của 1 trang
        #     if dict_element: # Chỉ lưu nếu có dữ liệu
        #         SeleniumCrawler.write_file_json(
        #             f'output/topcv_category_output_trang_{i+1}.json', 
        #             dict_element
        #         )
        #         print(f"Đã lưu trang {i+1}")

        # driver.quit()
        
        
    
def run_category(json_path):
    return SeleniumCrawler.run_category(json_path)
        