import argparse
from   utils.ainsi import *

def init():
     #! ARGUMENT
    parser = argparse.ArgumentParser(description="Vaccine: SQL Injection Detection Tool")
    parser.add_argument("url", help="The target URL to test for SQL injection.")
    parser.add_argument("-o", "--output", dest="output_file", default="vaccine_results.txt",
                        help="Archive file to store results. Defaults to 'vaccine_results.txt'.")
    parser.add_argument("-X", "--method", dest="request_method", default="GET",
                        choices=["GET", "POST"], help="HTTP request method (GET or POST). Defaults to GET.")

    args = parser.parse_args()    
    target_url = args.url
    output_file = args.output_file
    request_method = args.request_method.upper()

    #! PRINT ARGUMENT
    print(f"\n{colored('             VACCINE             ', BLACK, BG_BRIGHT_WHITE, BOLD)}")
    print(f"{colored('   URL   : ', BLACK, BG_WHITE, BOLD)}" 
          + f"  {colored(target_url, RED, styles=BOLD)}")
    print(f"{colored(' OUTFILE : ', BLACK, BG_WHITE, BOLD )}"
          + f"  {colored(output_file, RED, styles=BOLD)}")
    print(f"{colored('  METHOD : ', BLACK, BG_WHITE, BOLD )}"
          + f"  {colored(request_method, RED, styles=BOLD)}\n")
    
    return target_url, output_file, request_method
    