# Created by Catborisovv (c) 2020-2023

# Импорт модулей
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time # модуль тайм, нужен для установки задержек

# Конфигурация
QuestionMsg = "Здравствуйте, у меня вопрос по Вашему товару" # Сообщение для вопроса

DelaySend = 30 # переменная задержки между отправками вопросов (в секундах)

url = "https://www.wildberries.ru/" # не забыть перенести настройку URL в конфиг
category_url = "https://www.wildberries.ru/catalog/obuv/muzhskaya/botinki-i-polubotinki" # начальная страница рассылки
driver = webdriver.Chrome(executable_path="/Users/Catborisovv/Documents/Freelance/Current/wildberries-python-script/drivers/chromedriver") # не забыть перенести строку в конфиг для просмотра

# Main (основной код)
driver.implicitly_wait(5) # ставим задержку на 5 секунд, чтобы дождаться загрузки окна

try: # тут мы пробуем выполнить действие, чтобы если скрипт поломается, он вывел ошибку
    driver.get(url=url)
    driver.set_window_size(1080,800) 
    print("✓ Было созданно окно браузера")
    time.sleep(10)
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "j-main-login"))
        )
        element.click()
        print("✓ Переход на страницу авторизации")

        cycle_true = 1
        print("✓ Ожидание авторизации пользователя")
        while cycle_true == 1: # цикл происходит для того, чтобы определять, авторизован ли пользователь
            try:
                element1 = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "requestCode"))
                )
            except:
                cycle_true = 0
                print("✓ Пользователь авторизовался или выполнение скрипта пошло не по плану")

        driver.get(url=category_url) # перебрасываем пользователя скрипта на страницу категории товара
        print("✓ Пользователь был перенаправлен на страницу с категорией")

        print("✓ Был запущен поиск всех карточек товара")

        cards = 0
        pages = 0
        try:
            cards = driver.find_elements(By.CLASS_NAME, "product-card");
            print("✓ Карточки были найдены")
        except:
            print("[!] Возникла ошибка при поиске карточек")

        try:
            pages = driver.find_elements(By.CLASS_NAME, "pagination-item");
            print(f"✓ Колличество страниц было определенно")
        except:
            print("[!] Возникла ошибка при попытке получения колличества страниц с карточками")

        sheetOfCards = 0 # переменная текущей карточки
        totalCards = len(cards) # получаем общее колличество карточек из массива

        cycleCards = 1 # переменная действия цикла

        totalPages = len(pages)
        sheetOfPages = 0 # текущая страница
        while cycleCards == 1:
            if(sheetOfCards > 0):
                driver.get(url=category_url) # переходим на категорию (это сделанно, чтобы при повторе цикла мы переходили заново)

            if(sheetOfCards >= totalCards):
                if(sheetOfPages >= totalPages): # проверяем страницы
                    cycleCards = 0
                else:
                    sheetOfCards = 0 # устанавливаем количество текущих карточек на 0
                    totalPages += 1;
                    page[totalPages].click() # перехоим на следующую страницу с карточками категории
                    print("✓ Переход на следующую страницу")

            cards = driver.find_elements(By.CLASS_NAME, "product-card");
            cards[sheetOfCards].click() # переходим на страницу карточки

            questions_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "a-Questions"))
            )
            questions_element.click()

            new_question_element = WebDriverWait(driver, 5).until( # нажимаем на инпут создания товара
                EC.presence_of_element_located((By.ID, "new-question"))
            )
            new_question_element.click()
            new_question_element.send_keys(QuestionMsg)

            time.sleep(3) # ставим задержку на 5 секунд для использования кнопки

            btn_qerstion_submit = WebDriverWait(driver, 5).until( # нажимаем на инпут создания товара
                EC.presence_of_element_located((By.CLASS_NAME, "textarea-block__submit"))
            )
            btn_qerstion_submit.click() # нажимаем на кнопку отправки вопроса
            print(f"✓ #{sheetOfCards}: Вопрос был отправлен")

            sheetOfCards += 1 # тут мы добавляем одно число к переменной карточки
            time.sleep(DelaySend)
    except:
        print("[!]: Выполнение скрипта пошло не по плану")
    time.sleep(50) # тут устанавливаем 50 секунд до завершения скрипта

except Exception as ex:
    print(f"[!] Возникла ошибка выполнения скрипта: {ex}");
finally:
    driver.close()
    driver.quit()
