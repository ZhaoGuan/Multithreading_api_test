# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from gsheets import Sheets
import csv
import json
from tag_list_check.doc_reader import get_doc_data
import sys
import os

csv.field_size_limit(sys.maxsize)
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH)
sys.path.append(PATH + '/../')
os.path.join(PATH + '/.credentials')


def get_sheet():
    sheet = Sheets.from_files(secrets=PATH + '/client_secret-sheet.json', storage=PATH + '/storage.json')
    url = 'https://docs.google.com/spreadsheets/d/1oS7en09vBpXiwJjs9zto16US4tfU_bLxdy5EHk32Rsc/edit'
    # url = 'https://docs.google.com/document/d/1YBB75VQWERNKhvT-A9vUh0I-r_ZLPukAnVeXnj2e5SU/edit'
    s = sheet.get(url)
    sheet_list = []
    for i in s:
        sheet_list.append(i)
    print(sheet_list[0])
    sheet_list[0].to_csv(PATH + '/app_config_sicker2.csv')


def get_doc_data_to_csv():
    get_sheet()
    data = []
    with open(PATH + '/app_config_sicker2.csv') as csv_data:
        dict_data = csv.DictReader(csv_data)
        # print(dict_data)
        for i in dict_data:
            if i['老版本appconfig'] != None:
                if ('drive.google.com' in i['老版本appconfig']) or ('docs.google.com' in i['老版本appconfig']):
                    i['老版本appconfig'] = get_doc_data(i['策略']).replace('﻿{', '{')
                    # print(i['appconfig'])
            data.append(i)
    with open(PATH + '/app_config_sicker2_get_doc.csv', 'w') as new_csv:
        writer = csv.DictWriter(new_csv, ['产品', '语言地区', '取模', '分组', '策略', '文档链接', '新版本appconfig', '老版本appconfig', '备注'])
        writer.writeheader()
        for e in data:
            # print(e)
            writer.writerow(e)


def appconfig_data():
    # get_sheet()
    get_doc_data_to_csv()
    data = []
    result = []
    screen_data = []
    new_screen_data = []
    with open(PATH + '/app_config_sicker2_get_doc.csv') as csv_data:
        dict_data = csv.DictReader(csv_data)
        for i in dict_data:
            data.append(i)
            # 筛选数据
    for f in data:
        if f['老版本appconfig'] == None:
            pass
        else:
            screen_data.append(f)
    # 老版本appconfig数据整理
    for e in screen_data:
        try:
            value = json.loads(e['老版本appconfig'])
        except:
            pass
            # print(e['策略'])
        duid = e['取模'].replace('%', '').split('==')
        if duid == ['']:
            duid = 'random'
        if e['老版本appconfig'] != '':
            temp = {'data': {'product': e['产品'], 'language': e['语言地区'], 'duid': duid, 'style': 'old'},
                    'check_value': value}
            result.append(temp)
    # 新数据整理
    for n_f in data:
        if n_f['新版本appconfig'] == None:
            pass
        else:
            new_screen_data.append(n_f)
    # 老版本appconfig数据整理
    for n_e in new_screen_data:
        try:
            value = json.loads(n_e['新版本appconfig'])
        except:
            pass
            # print(n_e['策略'])
        duid = n_e['取模'].replace('%', '').split('==')
        if duid == ['']:
            duid = 'random'
        temp = {'data': {'product': n_e['产品'], 'language': n_e['语言地区'], 'duid': duid, 'style': 'new'},
                'check_value': value}
        result.append(temp)
    print(len(result))
    return result


if __name__ == "__main__":
    # get_sheet()
    result = appconfig_data()
    # print(result)
    # get_doc_data_to_csv()
