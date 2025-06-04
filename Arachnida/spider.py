# import sys
# import os


# class Spider:
#     def __init__(self, test = 0):
#         self.test = 10

# if __name__ == '__main__':
#     my_spider = Spider()
#     print(f"spider test! {my_spider.test}")
    
import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# print(page.text)
result = soup.find(id="ResultsContainer")


job_cards = result.find_all("div", class_="card-content")

# print(result.prettify())
for job_cards in job_cards:
    title_element = job_cards.find("h2", class_="title")
    compagny_element = job_cards.find("h3", class_="company")
    location_element = job_cards.find("p", class_="location")
    print(title_element.text.strip())
    print(compagny_element.text.strip())
    print(location_element.text.strip())
    print()
    
    
    
    # print(job_cards, end="\n" * 2)

# print(job_cards)