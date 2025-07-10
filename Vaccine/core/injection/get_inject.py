from utils.ainsi import *
from objects.vuln_link import vuln_link 

import sys, requests


# def error_based_injection_get(query_params, param, original_value, parsed_url):
#     for db_type, payloads in error_based_db_payloads.items():
#         for payload in payloads:
#             temp_params = query_params.copy()
#             temp_params[param] = [original_value + payload]
#             test_url = urlunparse(parsed_url._replace(query=urlencode(temp_params, doseq=True)))

#             try:
#                 response = requests.get(test_url, timeout=10)
#                 response_text_lower = response.text.lower()
                
#                 for signature in db_error_signatures.get(db_type, []):
#                     if signature in response_text_lower:
#                         return True, db_type, "error-based"
#             except requests.exceptions.RequestException:
#                 pass
#             except Exception as e:
#                 print(f"    Une erreur inattendue s'est produite: {e}")
#     return False, None, None

def get_injection(vulns_links):
    
    # if (vulns_links.success == False):
        # print(f"{colored('❌ Error:  ', RED,styles=BOLD)} {colored('Database type not identified. SQL injection is not possible.', RED, styles=BOLD)}\n")
        # sys.exit(1)
    
    # print(f"{colored('Query Parameters:', GREEN, styles=BOLD)} {query_params}")
    
    for vuln_link in vulns_links:
        query_parser(vuln_link)
        
        

def query_parser(vuln_link):
    identified_db, link, query_params, success = vuln_link.get_infos()
    
    print(f"🔴 {colored('Injection:', RED, styles=BOLD)} {colored('GET Method', CYAN, styles=BOLD)} {colored(' with ', WHITE)} {colored(identified_db, MAGENTA, BOLD)} {colored(' on ', WHITE)} {colored(link, MAGENTA, ITALIC)}")
    
    response = requests.get(link)
        
    if response:
        response.encoding = "utf-8"
        first_page = response.text
        base_url = link
        
        
        
        
            
    else:
        print(f"{colored('❌ Error:  ', RED,styles=BOLD)} {colored('no response to get the url', RED, styles=BOLD)}\n")
            
            
                        
            

            
            
        
        # print(response.text)
    
    


