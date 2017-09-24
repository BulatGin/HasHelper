import requests
import csv

#  Тестовая таблица
response = requests.get('https://docs.google.com/spreadsheet/ccc?key=1SAT8AgSThkyCENdvEVBsTctjLvxgiYLfQ245rXDVrw8&output=csv', verify=False)
#  Настоящая таблица
# response = requests.get('https://docs.google.com/spreadsheet/ccc?key=16U6dbrd4zGhiQW-c3SR4OE2ueUNX4ts8MYjWiT7YqLw&output=csv', verify=False)
assert response.status_code == 200, 'Wrong status code'
with open('new_data.csv', 'w', newline='') as file:
    file.write(response.content.decode("utf-8"))

week_day = ''


def file_generator(filename):
    with open(filename, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            try:
                if row[0] != '':
                    global week_day
                    week_day = row[0]
                if row[12] != '':
                    yield row[12]
            except IndexError:
                pass


for old_row, new_row in zip(file_generator('data_without_changes.csv'), file_generator('new_data.csv')):
    if old_row != new_row:
        print('{} - есть изменения! {}'.format(week_day.title(), new_row))
