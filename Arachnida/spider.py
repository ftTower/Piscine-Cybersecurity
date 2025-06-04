import sys
import requests

from bs4 import BeautifulSoup

#! CHECKING ARGV
if (len(sys.argv) < 2) :
    print("ERROR : missing url \n\tpython spider.py [-rlp] URL\n")
    sys.exit()

#! GET URL WITH ARGV
URL = sys.argv[len(sys.argv) - 1]

#! GETTING HTML WITH URL
try:
    page = requests.get(URL)
    print(f"Current URL : {URL}\n")
except requests.exceptions.RequestException as e:
    print(f"ERROR: Failed to fetch the URL.\n\nDetails:\n{e}")
    sys.exit()

#! SOUPIFY IT
soup = BeautifulSoup(page.content, "html.parser")


#! FIND IMG LINKS IN 
result = soup.find_all("div")
for site_img in result:
    links = site_img.find_all("a")
    for link in links:
        link_url = link["href"]
        print(f"Image here: {link_url}")

