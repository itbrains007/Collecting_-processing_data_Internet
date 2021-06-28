import requests
import json

def get_user():
    user=input('Введите пользователя: ')
    return user

def get_repos(user):
    url = 'https://api.github.com/users/'+user+'/repos'
    repos=requests.get(url).json()
    return repos

def write_repos(file_path, repos):
    with open(file_path,'w') as f:
        json.dump(repos,f)

def print_repos(file_path):
    with open(file_path) as f:
        json_repos=json.load(f)
    for i in json_repos:
        print(i['name'])

url='https://api.github.com'
user=get_user()
write_repos(user+'_repos.json',get_repos(user))
print_repos(user+'_repos.json')