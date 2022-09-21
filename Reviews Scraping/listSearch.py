from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd    

# Gets list of restaurants links from Google Maps

def get_links(address, num):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    #London Victoria & Albert Museum URL
    driver.get(address)
    
    time.sleep(2)

    n = 0
    links_list = []
    while n < num:
        x = 0
        while x < 2:
            try:
                last_div = driver.find_element_by_css_selector("[jsan='t-WPtQSFf6msE,7.lXJj5c,7.Hk4XGb']")
                driver.implicitly_wait(5)
                ActionChains(driver).move_to_element(last_div).perform()
                x+=1
            except: 
                break
        time.sleep(2)
        all_elements = driver.find_elements_by_css_selector("[jsan='7.hfpxzc,0.aria-label,8.href,0.jsaction']")
        for element in all_elements:
            links_list.append(element.get_attribute('href'))

        element = driver.find_element_by_id('ppdPk-Ej1Yeb-LgbsSe-tJiF1e')
        element.click()
        time.sleep(2)
        n+=1
    driver.quit()
    return links_list
