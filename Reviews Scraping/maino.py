import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from listSearch import get_links
from web import get_reviews
import concurrent.futures

start = time.time()
google_links = [
                'https://www.google.com/maps/search/Restaurants/@1.2801832,103.8457181,17z/data=!3m1!4b1!4m8!2m7!3m5!2s10+Stanley+Street!3s0x31da19f82958fa25:0x71f91b6073be4094!4m2!1d103.8479053!2d1.280184!6e5'
                ]
# To scrape https://www.google.com/maps/search/Restaurants/@1.3328409,103.9400363,14z/data=!3m1!4b1!4m2!2m1!6e5
# https://www.google.com/maps/search/Restaurants/@1.3734444,103.8490616,14z/data=!3m1!4b1!4m2!2m1!6e5
rest_links = []

for link in google_links:
    rest_links += (get_links(link, 2))

pd.set_option("display.max_rows", None, "display.max_columns", None)

print(len(rest_links))

rest_links = list(set(rest_links))

print(len(rest_links))

reviews = pd.DataFrame({'Review Rate': [],
        'Review Text' : []}) 
rev_dict = {'Review Rate': [],
        'Review Text' : []}

def add(url):
    dict = get_reviews(url)
    for item in dict['Review Rate']:
        rev_dict['Review Rate'].append(item)
    for item in dict['Review Text']:
        rev_dict['Review Text'].append(item)

num = 0
for link in rest_links:
    reviews = reviews.append(get_reviews(link))
    print(str(num) +" / " + str(len(rest_links)))
    num +=1

reviews = reviews.reset_index(drop=True)
reviews.to_csv('rs_other.csv')
print(len(reviews))
print(reviews)
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


