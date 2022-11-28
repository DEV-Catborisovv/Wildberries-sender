# этот скрипт создан для проверки работы каких либо действий выполнения скрипта. Сообщение для работадателя: этот скрипт можно удалить, ведь он не несет какой-либо пользы в использовании

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time # модуль тайм, нужен для установки задержек

driver = webdriver.Chrome(executable_path="/Users/Catborisovv/Documents/Freelance/Current/wildberries-python-script/drivers/chromedriver") # не забыть перенести строку в конфиг для просмотра
driver.get(url="https://www.wildberries.ru/catalog/muzhchinam/odezhda/bryuki-i-shorty")

time.sleep(15)
pages = driver.find_elements(By.CLASS_NAME, "pagination-item");
print(pages)
print("")
print(len(pages))

time.sleep(500)
