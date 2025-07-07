from utils.ainsi import *
from utils.utils import *

from navigation.crawler import *

from injection.get_db_detector import *
from injection.post_db_detector import *

from injection.get_inject import *
from injection.post_inject import *

def main():
    target_url, output_file, request_method = init()
    scrapped_data = simple_crawler(target_url)
    


    write_scrapped_data(scrapped_data, output_file)

    if "get" in request_method.lower():
        success, db_type, vuln_links = identify_db_get(scrapped_data)
        get_injection_process(success, db_type, vuln_links)
    elif "post" in request_method.lower():
        pass
    else:
        print("Wrong method")
        
    
    
        

    
if __name__ == "__main__":
    main()