from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pickle
from .top5_macs_testing import *


ticker = 'var'


payload = open("secrets.txt", "r").read().split('\n')
# open the driver
driver = webdriver.Firefox()

# go to the login page
url = 'https://robinhood.com/login'
driver.get(url)

# bring in cookies to login without 2 factor authentication
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies: 
    driver.add_cookie(cookie)


# enter username and password and hit enter
username = driver.find_element_by_name('username')
username.send_keys(payload[0])
password = driver.find_element_by_name('password')
password.send_keys(payload[1])
driver.find_element_by_class_name('css-1l2vicc').click()

# go to the ticker page
url = f'https://robinhood.com/stocks/{ticker}'
driver.get(url)

# click sell
driver.find_element_by_class_name('css-uzlltq').click()

# click sell all
html = driver.page_source
sell_all_class = html.split('5px;">-</span><a class="')[1].split('"')[0]
driver.find_element_by_xpath(f"//a[@class='{sell_all_class}']").click()

# click review order
html = driver.page_source
review_order_class = html.split('"><button type="button" class="')[5].split('"')[0]
driver.find_element_by_xpath(f"//button[@class='{review_order_class}']").click()

# click sell
