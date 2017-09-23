# TODO сделать рефакторинг кода
from bs4 import BeautifulSoup
import requests
import json

settings = {
    'number_of_downloaded_presentations': 0
}

login_url = 'http://shelly.kpfu.ru/e-ksu/private_office.authscript'
url = 'http://shelly.kpfu.ru/e-ksu/'

authentication_data = {
    'p_login': '',
    'p_pass': ''
}
with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)['settings']
session = requests.Session()

res = session.post(login_url, data=authentication_data)
text = session.get(
    'http://shelly.kpfu.ru/e-ksu/site_student_services.study_tasks?p_menu=6&p_type_menu=3&p_discipline=18925').text
text = text.replace('<!--', '')
text = text.replace('-->', '')
soup = BeautifulSoup(text, 'html.parser')
text = soup.find_all('ul')[-1]
number_of_presentations = len(text.find_all('li')) - 1
if number_of_presentations == settings['number_of_downloaded_presentations']:
    print('Новых презентаций нет =)')
else:
    last_li = text.find_all('li')[-1]
    for nobr in last_li.find_all('nobr'):
        name = nobr.a.string
        response = session.get(url + nobr.a.get('href'))
        with open(name, 'bw') as outfile:
            outfile.write(response.content)
    settings['number_of_downloaded_presentations'] = number_of_presentations
with open('settings.json', 'w') as settings_file:
    json.dump(settings, settings_file)
