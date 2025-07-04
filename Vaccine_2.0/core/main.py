from utils.ainsi import *
from utils.utils import *

from navigation.crawler import *

def main():
    target_url, output_file, request_method = init()
    scrapped_data = simple_crawler(target_url)

    # from pprint import pprint
    # pprint(scrapped_data)
    
    for url, data in scrapped_data.items():
        print(f"Titre : {data.get('title', 'N/A')}")
        print(f"URL   : {url}\n")
    
if __name__ == "__main__":
    main()