import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager

from pages import Page

class Crawler:
    def __init__(self, url):
        self.pages = []
        self.initial_url = url


        self.pages.append(Page(self.initial_url))
        
    def return_pages(self):
        return self.pages
        
    
    
    
