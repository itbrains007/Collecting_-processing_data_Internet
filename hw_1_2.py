import json
import requests
from pprint import pprint

API_key='1185ab9a5a0084943472b32b467bf78b'

def get_city():
    city=input('Введите название города: ')
    return city

def get_weather(city,key):
    url='https://api.openweathermap.org/data/2.5/weather'
    url_params={'q':city, 'appid':key, 'lang':'ru'}
    weath_json=requests.get(url,params=url_params).json()
    return weath_json

city=get_city()
weath_json=get_weather(city,API_key)
print(weath_json['main'])
