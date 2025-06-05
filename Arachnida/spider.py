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
        self.img_path = path + "/" + site_name
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
        return f"\033[93m{self.index:03}\033[0m - {self.img_full_path}"
        
        
def display_loading (image, index):
    if index > 0:
        print("\033[F\033[K", end='')
    print(f"\t{image}")


def crawl(URL, site_name, visited, depth, max_depth, index):
    if depth > max_depth or URL in visited:
        return index
    visited.add(URL)

    try:
        response = requests.get(URL, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error loading {URL}: {e}")
        return index

    imgs = soup.find_all('img')
    for img in imgs:
        if ("src" not in img.attrs):
            continue
        img_obj = image(URL, site_name, img, index)
        if img_obj.extension not in ["jpg", "jpeg", "png", "gif", "bmp"]:
            if img == imgs[-1] and index == 0:
                print("No images were downloaded.")
                return index
            continue
        try:
            urlretrieve(img_obj.full_URL, img_obj.img_full_path)
        except Exception as e:
            print(f"Error downloading {img_obj.full_URL}: {e}")
            continue
        display_loading(img_obj, index)
        index += 1

    for a in soup.find_all('a', href=True):
        link = urljoin(URL, a['href'])
        link = link.split('#')[0].split('?')[0]
        if urlparse(link).netloc == urlparse(URL).netloc:
            index = crawl(link, site_name, visited, depth + 1, max_depth, index)

    return index





if (len(sys.argv) < 2) :
    print("\033[91mERROR: Missing URL\n\tUsage: python spider.py [-rlp] URL\033[0m")
    sys.exit()

URL = sys.argv[-1]

is_path = "-p" in sys.argv
recursive = "-r" in sys.argv
is_max_depth = "-l" in sys.argv

path = "./data"

if is_path and (sys.argv.index("-p") + 1 < len(sys.argv)):
    path = sys.argv[sys.argv.index("-p") + 1]
        

if is_max_depth and recursive:
    if sys.argv.index("-l") + 1 < len(sys.argv):
        try:
            max_depth = int(sys.argv[sys.argv.index("-l") + 1])
        except ValueError:
            print("\033[91mERROR: Invalid depth value after '-l'\033[0m")
            sys.exit()
    else:
        print("\033[91mERROR: Missing depth value after '-l'\033[0m")
        sys.exit()
elif recursive and not is_max_depth:
    max_depth = 6
else:
    max_depth = 1
    
visited = set()
site_name = urlparse(URL).netloc.replace(".", "-")
print(f"\033[92m[+] working on {site_name}\033[0m")

index = 0
index = crawl(URL, site_name, visited, 1, max_depth, index)

print("\033[F\033[K", end='')
print(f"\tDownloaded {index} images")
