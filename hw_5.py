import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument('start-maximized')

# Авторизация на сайте
driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
driver.get('https://mail.ru/')

elem = driver.find_element_by_class_name('body').find_element_by_class_name('email-input')
elem.send_keys('study.ai_172@mail.ru')

button = driver.find_element_by_class_name('body').find_element_by_class_name('button')
button.click()

elem = driver.find_element_by_class_name('body').find_element_by_class_name('password-input')
elem.send_keys('NextPassword172!!')

button = driver.find_element_by_class_name('body').find_element_by_class_name('second-button')
button.click()
time.sleep(5)

# Перелистывание страниц и сбор ссылок на письма
emails=[]
action = ActionChains(driver)

links = []
#Ограничение в 3  страниц/ Если убрать, то будет просмотр до последней страницы
for i in range(3):
    email_links = driver.find_elements_by_xpath('//*/a[@class="llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal"]')
    for i in range(0,len(email_links )):
        link = email_links [i].get_attribute('href')
        links.append(link)
    action.move_to_element(email_links[-1])
    action.perform()
    time.sleep(5)

#Сбор информации из писем
mail_info = []
element={}
for j in links:
    driver.get(j)
    page=WebDriverWait(driver,5)
    page.until(expected_conditions.presence_of_element_located((By.CLASS_NAME,'letter-contact')))
    sender = driver.find_element_by_class_name('letter__author').find_element_by_class_name('letter-contact').text
    send_data = driver.find_element_by_class_name('letter__author').find_element_by_class_name('letter__date').text
    title = driver.find_element_by_class_name('thread__header').find_element_by_class_name('thread__subject').text
    body = driver.find_element_by_class_name('letter-body__body').text
    element = {'sender': sender,
               'send_data': send_data,
               'title': title,
               'body':body
               }
    mail_info.append(element)


#Запись информации в БД
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mydb"
MONGO_COLLECTION = "mail"

client = MongoClient (MONGO_HOST,MONGO_PORT)
db = client[MONGO_DB]
collection = db.MONGO_COLLECTION

db.inventory.insert_many(mail_info)
driver.close ()