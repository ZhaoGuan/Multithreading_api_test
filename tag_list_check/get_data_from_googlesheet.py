# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from gsheets import Sheets
import csv
import json


def get_sheet():
    sheet = Sheets.from_files('./client_secret.json')
    url = 'https://docs.google.com/spreadsheets/d/1oS7en09vBpXiwJjs9zto16US4tfU_bLxdy5EHk32Rsc/edit'
    s = sheet.get(url)
    sheet_list = []
    for i in s:
        sheet_list.append(i)
    print(sheet_list[0])
    sheet_list[0].to_csv('./app_config_sicker2.csv')


def appconfig_data():
    get_sheet()
    data = []
    result = []
    screen_data = []
    with open('./app_config_sicker2.csv') as csv_data:
        dict_data = csv.DictReader(csv_data)
        for i in dict_data:
            data.append(i)
    # 筛选数据
    for f in data:
        if f['appconfig'] == None:
            pass
        else:
            screen_data.append(f)
    # 数据整理
    for e in screen_data:
        value = json.loads(e['appconfig'])
        duid = e['取模'].replace('%', '').split('==')
        if duid == ['']:
            duid = 'random'
        temp = {'data': {'product': e['产品'], 'language': e['语言地区'], 'duid': duid}, 'check_value': value}
        result.append(temp)
    # print(result)
    return result


if __name__ == "__main__":
    # get_sheet()
    result = appconfig_data()
    print(result)
