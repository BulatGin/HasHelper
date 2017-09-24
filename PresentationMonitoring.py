from bs4 import BeautifulSoup
import requests
import json
import os

login_url = 'http://shelly.kpfu.ru/e-ksu/private_office.authscript'
list_of_presentations_url = \
    'http://shelly.kpfu.ru/e-ksu/site_student_services.study_tasks?p_menu=6&p_type_menu=3&p_discipline=18925'
base_url = 'http://shelly.kpfu.ru/e-ksu/'

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

session = requests.Session()

session.post(login_url, data=settings['authentication_data'])
response = session.get(list_of_presentations_url)
assert response.status_code == 200, 'Site is not available now'

response_text = response.text
response_text = response_text.replace('<!--', '')
response_text = response_text.replace('-->', '')
soup = BeautifulSoup(response_text, 'html.parser')
last_ul = soup.find_all('ul')[-1]
list_of_li = last_ul.find_all('li')
number_of_presentations = len(list_of_li) - 1
if number_of_presentations == settings['number_of_downloaded_presentations']:
    print('Новых презентаций нет =)')
else:
    last_li = list_of_li[-1]
    for nobr in last_li.find_all('nobr'):
        path = os.path.join(settings['files_path'], nobr.a.string)
        response = session.get(base_url + nobr.a.get('href'))
        with open(path, 'bw') as outfile:
            outfile.write(response.content)
    settings['number_of_downloaded_presentations'] = number_of_presentations

with open('settings.json', 'w') as settings_file:
    json.dump(settings, settings_file)
