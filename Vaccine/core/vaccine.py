from utils.ainsi import *
from utils.utils import *

from GET.navigation.crawler import *

from GET.detection.get_db_detector import *

from GET.injection.get_inject import *




def main():
    target_url, output_file, request_method = init()
    scrapped_data = simple_crawler(target_url)
    
    
    # write_scrapped_data(scrapped_data, output_file)


    if "get" in request_method.lower():
        get_injection(identify_db_get(scrapped_data), output_file) 
    elif "post" in request_method.lower():
        pass
    else:
        print("Wrong method")
        
    
if __name__ == "__main__":
    main()