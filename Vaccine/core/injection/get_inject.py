from utils.ainsi import *


def get_injection_process(success, db_type, vuln_links):
    
    if (success == False):
        print(f"{colored('❌ Error:  ', RED,styles=BOLD)} {colored('Database type not identified. SQL injection is not possible.', RED, styles=BOLD)}\n")
        
    print(f"🔴 {colored('Injection:', RED, styles=BOLD)} {colored('GET Method', CYAN, styles=BOLD)} {colored(' on ', WHITE)} {colored(db_type, MAGENTA, BOLD)}")
        
    
    pass