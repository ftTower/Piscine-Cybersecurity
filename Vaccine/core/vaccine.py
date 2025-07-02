import argparse

from crawler import Crawler

class Vaccine:
    def __init__(self, target_url, output_file, request_method):
        
        self.url = target_url
        self.output_file = output_file
        self.request_method = request_method
        
        self.pages = Crawler(self.url).return_pages()
        
        
        
        
        
        self.display_pages()

    def display_pages(self):
        print(f"[+] Found {len(self.pages)} pages !\n")
        for page in self.pages:
            print(page)
            for input in page.inputs:
                print(f"\t{input}")
        print()
                
    
        

def main():
    
    parser = argparse.ArgumentParser(description="Vaccine: SQL Injection Detection Tool")
    parser.add_argument("url", help="The target URL to test for SQL injection.")
    parser.add_argument("-o", "--outut", dest="output_file", default="vaccine_results.txt",
                        help="Archive file to store results. Defaults to 'vaccine_results.txt'.")
    parser.add_argument("-X", "--method", dest="request_method", default="GET",
                        choices=["GET", "POST"], help="HTTP request method (GET or POST). Defaults to GET.")

    args = parser.parse_args()
    
    target_url = args.url
    output_file = args.output_file
    request_method = args.request_method.upper()

    Vaccine(target_url, output_file, request_method)


if __name__ == "__main__":
    main()