import sys
import requests
import os
import mimetypes

from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.parse import urlparse
from urllib.parse import urljoin

class   image:
    def __init__(self, URL, site_name, img, index):
        #! DATA
        self.URL = URL
        self.img_URL = img["src"]
        self.full_URL = urljoin(URL, self.img_URL)
        
        self.index = index
        #! DL PATH
        self.img_path = ".data" + "/" + site_name
        os.makedirs(self.img_path, exist_ok=True) #* MAKE A DIRECTORY TO SORT SITE
        
        #! GUESS EXTENSION
        self.extension = mimetypes.guess_type(self.full_URL)[0]
        if self.extension:
            self.extension = self.extension.split('/')[-1]
        else:
            self.extension = "png"
        
        #!NAMES x PATHS
        self.img_name = site_name + "_" + str(index) 
        self.img_full_path = self.img_path + "/" + self.img_name + "." + self.extension #* PATH + NAME + EXT
  
        
    def __str__(self):
        return f"{self.index:03} - {self.img_full_path}"
        
def display_loading (image, index):
    if index > 1:
        print("\033[F\033[K", end='')
    print(f"\t{image}")

def crawl(URL, site_name, visited, depth, max_depth, index):
    if depth > max_depth or URL in visited:
        return index
    visited.add(URL)
    

def get_internal_links(URL, soup):
    domain = urlparse(URL).netloc
    links = set()
    for a_tag in soup.find_all("a", href=True):
        link = urljoin(URL, a_tag['href'])
        if urlparse(link).netloc == domain:
            links.add(link)
    return links

def process_page(URL, site_name, visited, index):
    if URL in visited:
        return index
    visited.add(URL)
    
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    imgs = soup.find_all('img')
    for img in imgs:
        i = image(URL, site_name, img, index)
        urlretrieve(i.full_URL, i.img_full_path)
        display_loading(i, index)
        index+=1
    return index, soup

URL = sys.argv[-1]
recursive = "-r" in sys.argv
visited = set()
site_name = urlparse(URL).netloc.replace(".", "-")
index = 1

index, soup = process_page(URL, site_name, visited, index)

if recursive :
        links = get_internal_links(URL, soup)
        for link in links:
            index, _ = process_page(link, site_name, visited, index)

# #! CHECKING ARGV
# if (len(sys.argv) < 2) :
#     print("ERROR : missing url \n\tpython spider.py [-rlp] URL\n")
#     sys.exit()

# #! GET URL AND SITE NAME WITH ARGV
# URL = sys.argv[len(sys.argv) - 1]
# parsed_url = urlparse(URL)
# site_name = parsed_url.netloc

# #! GETTING HTML WITH URL
# try:
#     page = requests.get(URL)
#     print(f"\033[92m[+] working on {site_name}\033[0m")
# except requests.exceptions.RequestException as e:
#     print(f"\033[91m[-] ERROR : failed to join {site_name}\033[0m")
#     sys.exit()

# #! SOUPIFY IT
# soup = BeautifulSoup(page.content, "html.parser")

# #! FIND ALL IMG
# result = soup.find_all("img")

# index = 0
# for img in result:
#     if "src" in img.attrs:
        
        
#             current = image(URL, site_name, img, index)
            
#             if current.extension not in ["jpg", "jpeg", "png", "gif", "bmp"]:
#                 if index == 0 and img == result[-1]:
#                     print("No images were downloaded.")
#                 continue
            
#             index += 1
            
#             urlretrieve(current.full_URL, current.img_full_path)
            
            
#             display_loading(current, index)

    
# print("\033[F\033[K", end='')
# print(f"\tDownloaded {index} images")

 
