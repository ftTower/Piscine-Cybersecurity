from utils.ainsi import *
from utils.utils import *

from navigation.crawler import *

from detection.get_db_detector import *
from detection.post_db_detector import *

from injection.get_inject import *
from injection.post_inject import *




def main():
    target_url, output_file, request_method = init()
    scrapped_data = simple_crawler(target_url)
    
    
    write_scrapped_data(scrapped_data, output_file)


    if "get" in request_method.lower():
        get_injection(identify_db_get(scrapped_data)) 
    elif "post" in request_method.lower():
        pass
    else:
        print("Wrong method")
        
    
if __name__ == "__main__":
    main()