import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import json

def input_vac():
    in_vacancy=input("Введите вакансию: ")
    return in_vacancy

def input_page():
    in_page = input("Введите число страниц: ")
    try:
        in_page = int(in_page)
    except Exception as err:
        print(err)
    return in_page

def vacancy_items(vac, page):
    vacancy_items_all = []
    base_url = 'https://hh.ru/search/vacancy'
    last_page=0

    params = {
        'text': vac,
        'items_on_page': '20',
        'page': ''
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
    }
    html = requests.get(base_url, params=params, headers=headers)

    if html.ok:
        pars_html = bs(html.text, 'html.parser')

        page_block = pars_html.find(attrs = {'data-qa': 'pager-block'})
        if not page_block:
            print("Вакансий нет")
        else:
            last_page = int(page_block.find_all(attrs = {"class":"pager-item-not-in-short-range"})[-1].text)
        if last_page>page:
            last_page=page

    for page in range(0, last_page):
        params['page'] = page
        html = requests.get(base_url, params=params, headers=headers)
        if html.ok:
            parsed_html = bs(html.text, 'html.parser')
            vacancy_items_html = parsed_html.find_all('div',{'class': 'vacancy-serp-item'})
        vacancy_items_all.append(vacancy_items_html)
        print()
    return vacancy_items_all

def pars_vacancy(vacancy_items_all):
    vacancy_data_all=[]
    for j in range(0,len(vacancy_items_all)):
        for i in vacancy_items_all[j]:
            vacancy_data = {}
            vacancy_data['name'] = i.find(attrs={'class': 'resume-search-item__name'}).text
            link = i.find('a', {'data-qa':'vacancy-serp__vacancy-title'})
            vacancy_data['url']=link.get('href')
            vacancy_data['site'] = 'https://hh.ru/'
            sal_html=i.find('span',{'data-qa': 'vacancy-serp__vacancy-compensation'})
            if not sal_html:
                vacancy_data['salary']=None
            else:
                vacancy_data['salary'] =sal_html.text
            vacancy_data_all.append(vacancy_data)
    return vacancy_data_all


#Ввод данных
vacancy=input_vac()
page=input_page()

#Собрать данные со страницы
vac_html=vacancy_items(vacancy,page)

#Обраброка данных
vac_list=pars_vacancy(vac_html)

df = pd.DataFrame(vac_list)

#Записать данные в файл json
with open('vacancy.json', 'w') as f:
    json.dump(vac_list, f)