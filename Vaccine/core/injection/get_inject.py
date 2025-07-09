from utils.ainsi import *


import sys, requests

class Injector:
    
    def __init__(self, success, db_type, vuln_links, params):
        if (success == False):
            print(f"{colored('❌ Error:  ', RED,styles=BOLD)} {colored('Database type not identified. SQL injection is not possible.', RED, styles=BOLD)}\n")
            sys.exit(1)
        print(f"🔴 {colored('Injection:', RED, styles=BOLD)} {colored('GET Method', CYAN, styles=BOLD)} {colored(' on ', WHITE)} {colored(db_type, MAGENTA, BOLD)}")
            
        self.db_type = db_type
        self.vuln_links = vuln_links
        self.params = params
        
        for url in vuln_links:
            self.run(url)

    def run(self, url):
        response = requests.get(url)
        response.encoding = "utf-8"
        first_page = response.text
        
        
        
        type(response.json)
        # print(response.text)
    
    


