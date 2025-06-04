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

# job_cards = result.find_all("div", class_="card-content")

#!Find a list with html
# print(result.prettify())
# for job_cards in job_cards:
#     title_element = job_cards.find("h2", class_="title")
#     compagny_element = job_cards.find("h3", class_="company")
#     location_element = job_cards.find("p", class_="location")
    
    
    # print(title_element.text.strip())
    # print(compagny_element.text.strip())
    # print(location_element.text.strip())
    # print()
    
#!Find a list whith string 
python_jobs = result.find_all("h2", string=lambda text : "python" in text.lower())
python_jobs_cards = [h2_element.parent.parent.parent for h2_element in python_jobs]

# for job_cards in python_jobs_cards:
#     title_element = job_cards.find("h2", class_="title")
#     company_element = job_cards.find("h3", class_="company")
#     location_element = job_cards.find("p", class_="location") 
       
#     # print(python_jobs.text.strip())
#     print(title_element.text.strip())
#     print(company_element.text.strip())
#     print(location_element.text.strip())
#     print()
    
# !Interact with the website

#? get all links
# for job_card in python_jobs_cards:
#     links = job_card.find_all("a") #! find all buttons
#     for link in links:
#         link_url = link["href"] #! looking for the value of href
#         print(f"Apply here: {link_url}\n")

#? get and filter links
# for job_card in python_jobs_cards:
#     link_url = job_card.find_all("a")[1]["href"]
#     print(link_url)
