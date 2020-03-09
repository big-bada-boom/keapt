import requests
import re
from bs4 import BeautifulSoup


# https://www.avito.ru/yoshkar-ola/kvartiry/prodam/2-komnatnye/novostroyka/kirpichnyy_dom-ASgBAQICAUSSA8YQA0DmBxSOUuQHFPhRyggUglk?cd=1&p=1
#   План:
#   1. Запросим страницу.                                        (готово)
#   2. Определим колличество страниц.                            (готово)
#   3. Добавим генератор для перехода на следующую страницу.     (готово)
#   4. Спарсим цены квартир.                                     (готово)
#   5. Определим среднюю цену квартир.                           (готово)
#   6. Добавить возможность корректировки                       (в процессе)
#      URLа для выбора города.
#   7. Добавить возможность корректировки                       (в процессе)
#      URLа для изменения количества комнат.
#   8. Добавить график изменения цен.                           (в процессе)


def get_html(url): # Запрашиваем страницу
    r = requests.get(url)
    r = r.text
    return r

def get_total_pages(html):  # Вытянем общее количество страниц
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_=
                        'pagination-root-2oCjZ').find_all('span', class_=
                        'pagination-item-1WyVp')[-2].text
    pages = int(pages)
    return pages

def get_next_page(url, pages): # Запрашиваем следущую старицу
    for num in range(1,pages + 1):
        page = url
        page = page.strip(page[-1]) + str(num)
        yield page

def get_price(page): # Парсим цены квартир и заносим в список в виде чисел
    r = requests.get(page)
    r = r.text
    soup = BeautifulSoup(r, 'lxml')
    prices = soup.find_all('div', class_='snippet-price-row')
    p = re.compile(r'[0-9][ ][0-9][0-9][0-9][ ][0-9][0-9][0-9]')
    prices = p.findall(str(prices))
    str_to_int = []
    for n in prices:
        n = n.split(' ')
        if '0' in n[0]:
            pass
        elif len(n) == 3:
            n = str('{0}{1}{2}'.format(n[0],n[1],n[2]))
            if len(n) >= 7:
                n = int(n)
                str_to_int.append(n)
    return str_to_int

def full_list(page, get_price): # Получим полный список
    fullprice = []
    for n in page:
        to_extend = get_price(n)
        fullprice.extend(to_extend)
    return fullprice

def average_value(fullprice): # Получим среднее значение 
    len_ = len(fullprice)
    values = 0
    for n in fullprice:
        values += n
    average = int(values/len_)
    return average

def display_message(average): # Вывод текста 
    print('Средняя цена двухкомнатных квартир в Йошкар-Оле (на сегодняшний день):', average, 'руб.')

cities = {} # Кортеж транслита городов для возможности их выбора

print('Добрый день!')
print('Добро пожаловать в программу анализатор цен на квартиры в вашем городе.')
print('Пожалуйста подождите...\n')

url = 'https://www.avito.ru/yoshkar-ola/kvartiry/prodam/2-komnatnye/novostroyka/kirpichnyy_dom-ASgBAQICAUSSA8YQA0DmBxSOUuQHFPhRyggUglk?cd=1&p=1'
html = get_html(url)
pages = get_total_pages(html)
page = get_next_page(url, pages)
fullprice = full_list(page, get_price)
average = average_value(fullprice)
print('---------------------------------------------------------------------------------------')
display_message(average)
print('---------------------------------------------------------------------------------------')