from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd    
import logging
import time

def get_reviews(address):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    PATH = "chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=chrome_options)
    #London Victoria & Albert Museum URL
    driver.get(address)

    import time
    
    try:
        # get number of reviews
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'HHrUdb')))
        total_number_of_reviews = driver.find_element(By.CLASS_NAME, "HHrUdb")
        print(total_number_of_reviews.get_attribute('innerHTML').strip())
    except BaseException:
        print('webpage not found')
        logging.exception("Except")
        pass

    try:
        # get type
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[jsan='7.DkEaL,0.jsaction']")))
        rest_type = driver.find_element(By.CSS_SELECTOR, "[jsan='7.DkEaL,0.jsaction']")
        type = rest_type.get_attribute('innerHTML').strip().lower()
    except BaseException:
        print('type not found')
        logging.exception("Except")
        type =""
        pass

    try:
        # get more keywords
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[jsan='7.tXNTee,7.LCTIRd,7.L6Bbsd,0.aria-label,0.data-tooltip,0.jsaction']")))
        element = driver.find_element(By.CSS_SELECTOR,"[jsan='7.tXNTee,7.LCTIRd,7.L6Bbsd,0.aria-label,0.data-tooltip,0.jsaction']")
        ActionChains(driver).move_to_element(element).perform()
        #driver.implicitly_wait(5)
        element.click()
        print("+ button found")
    except BaseException:
        print('more keyword button not found')
        logging.exception("Except")
        pass

    try:
        # click sort button
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Sort reviews']")))
        driver.implicitly_wait(3)
        element = driver.find_element(By.CSS_SELECTOR,"[aria-label='Sort reviews']")
        ActionChains(driver).move_to_element(element).perform()
        #driver.implicitly_wait(5)
        element.click()
    except BaseException:
        print('sort button not found')
        logging.exception("Except")
        pass

    try:
        # click newest button
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//li[@data-index='1']")))
        element = driver.find_element(By.XPATH, "//li[@data-index='1']")
        #driver.implicitly_wait(5)
        element.click()
    except BaseException:
        print('button not found')
        logging.exception("Except")
        pass

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "jftiEf")))
        print('reviews found')
    except:
        print('reviews not found')
        logging.exception("Except")
        pass

    time.sleep(1)
    n = 0
    
    while n < 2:
        try:
            last_div = driver.find_element(By.CLASS_NAME, "lXJj5c")
            ActionChains(driver).move_to_element(last_div).perform()
            n+=1
        except: 
            print("cant scroll")
            logging.exception("Except")
            break
            
    time.sleep(1)
    
    response = BeautifulSoup(driver.page_source, 'html.parser')
    reviews = response.find_all('div', class_='jftiEf')
    keywords = response.find_all('div', class_='e2moi')
    driver.quit()
    
    return get_review_summary(reviews, keywords, type)

def get_review_summary(result_set, keyword_set, type):
    num = 0
    rev_dict = {'Review Text' : [],
        'Phrase': []}
    for result in result_set:
        review_text = result.find('span',class_='wiI7pd').text
        rev_dict['Review Text'].append(review_text)

        if review_text !="":
            num +=1
            review_text=""

        if num == 20:
            break

    print(len(rev_dict['Review Text']))
    rev_dict['Review Text'] = list(filter(None, rev_dict['Review Text']))
    print(len(rev_dict['Review Text']))

    for keyword in keyword_set:
        phrase = keyword.find('span',class_='uEubGf').text
        rev_dict['Phrase'].append(phrase)
    
    try:
        ind = rev_dict['Phrase'].index("All")
    except:
        ind = -1
        rev_dict["Phrase"] = []

    ind+=1
    rev_dict['Phrase'] = rev_dict['Phrase'][ind:-1]
    rev_dict['Phrase'].insert(0, type)
    rev_dict['Phrase'] = ' '.join(rev_dict['Phrase'])
    print(rev_dict['Phrase'])
    print(str(num) + " reviews added")
    return rev_dict

start = time.time()
get_reviews("https://www.google.com/maps/place/Nomiya+Izakaya+%26+Sake+Bar/@1.2830168,103.844223,17z/data=!3m1!5s0x31da197334487039:0x9498c1839e31e20a!4m5!3m4!1s0x0:0xcff17c5fe8df99c1!8m2!3d1.2830168!4d103.844223")

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
