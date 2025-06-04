import sys
import requests

from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.parse import urlparse
from urllib.parse import urljoin

#! CHECKING ARGV
if (len(sys.argv) < 2) :
    print("ERROR : missing url \n\tpython spider.py [-rlp] URL\n")
    sys.exit()

#! GET URL AND SITE NAME WITH ARGV
URL = sys.argv[len(sys.argv) - 1]
parsed_url = urlparse(URL)
site_name = parsed_url.netloc

#! GETTING HTML WITH URL
try:
    page = requests.get(URL)
    # print(f"[+] working on {URL}\n")
except requests.exceptions.RequestException as e:
    print(f"ERROR: Failed to fetch the URL.\n\nDetails:\n{e}")
    sys.exit()

#! SOUPIFY IT
soup = BeautifulSoup(page.content, "html.parser")

#! FIND IMG LINKS IN 
result = soup.find_all("img")
nb_img = 0
for img in result:
    if "src" in img.attrs:
        img_url = img["src"]
        full_img_url = urljoin(URL, img_url)
        nb_img += 1
        name_img = ".data/" + site_name + "_"  + str(nb_img) + ".png"
        try:
            urlretrieve(full_img_url, name_img)
        except Exception as e:
            print(f"Erreur lors du téléchargement de {full_img_url}: {e}")

print(f"Found {nb_img} images on {URL}")

