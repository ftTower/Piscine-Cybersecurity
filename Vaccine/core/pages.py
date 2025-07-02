import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager

from input import Input_obj

class Page:
    def __init__(self, url):
        self.url = url
        self.inputs = []
        self.find_input()
        
        
    def return_inputs(self):
        return self.inputs    
    
    def parse_input(self, input_elements):
        if input_elements:
            for input_html in input_elements: 
                if '<input type="text"' in input_html or '<input type="password"' in input_html:
                    self.inputs.append(Input_obj(input_html, self.url, True))
                else:
                    self.inputs.append(Input_obj(input_html, self.url))
        else:
            print("No input elements found.")
    
    def find_input(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=options)
        
        try:
            driver.get(self.url)
            time.sleep(2)
            
            input_elements = [element.get_attribute('outerHTML') for element in driver.find_elements(By.TAG_NAME, "input")]
            self.parse_input(input_elements)
        except Exception as e:
            print(f"Error finding input elements: {e}")
        finally:
            driver.quit()
            
    def __str__(self):
        
        len = 0
        for input in self.inputs:
            if input.usable == True:
                len+=1
        
        return f"\033[1;31m[{self.url}]\033[0m : found {len} sqli entry"