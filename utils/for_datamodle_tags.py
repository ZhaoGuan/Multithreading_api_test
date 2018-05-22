# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import requests
from sanic import Sanic
from sanic.response import json as sanic_json
import json
import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + '/../')

from beaker.cache import cache_regions


app = Sanic()

# google_sheet部分
# 权限
# 只允许读sheet
# scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# sheet读写权限
scope = 'https://www.googleapis.com/auth/spreadsheets'
# for spark
client_id = '264584935389-b7l2ogdjqgs362o7qtilmlvdm2tk12ij.apps.googleusercontent.com'
client_secret = "h2MoUfqxY2wDY3CaEygOaqnn"
authorization_code = 'refresh_token'
# authorization_code = 'authorization_code'
redirect_uri = 'http://localhost'
# 读写权限code
code = '4/AACDx-2x8jaISdRTmW0ctm7vReyty1lP-J7e_wNLkrTNTQ77NNY-0Wv0abXnXysIIL87zSyivseEGpeT5hvVjdg'
URL = 'https://accounts.google.com/o/oauth2/v2/auth?scope={}&' \
      'access_type=offline&' \
      'include_granted_scopes=true&' \
      'redirect_uri={}&' \
      'response_type=code&' \
      'client_id={}&' \
      'prompt=consent'.format(scope, redirect_uri, client_id)

get_token_data_body = 'code=%s&' \
                      'client_id=%s&' \
                      'client_secret=%s&' \
                      'redirect_uri=%s&' \
                      'grant_type=%s' % (code, client_id, client_secret, redirect_uri, 'authorization_code')

refresh_token = '1/tjpnv6htQUb-51PkJZVeSx_FBoroUOb7WRuD6zKRH9Q'
refresh_token_data = 'client_id={}&' \
                     'client_secret={}&' \
                     'refresh_token={}&' \
                     'grant_type=refresh_token'.format(client_id, client_secret, refresh_token)
sheet_id = '1oS7en09vBpXiwJjs9zto16US4tfU_bLxdy5EHk32Rsc'


def get_token_data():
    # 授权页拿去code
    # 授权后在url中取code
    print(URL)
    # 获取token data等
    header = {'Host': 'www.googleapis.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    get_token_url = 'https://www.googleapis.com/oauth2/v4/token'
    # 获取token
    # response = requests.post(url=get_token_url, data=get_token_data_body, headers=header)
    # 刷新token
    response = requests.post(url=get_token_url, data=refresh_token_data, headers=header)
    print(get_token_url)
    print(response)
    print(response.text)
    return json.loads(response.text)['access_token']


def get_all_sheet(sheet_header):
    sheet_list = []
    url = 'https://sheets.googleapis.com/v4/spreadsheets/' + sheet_id
    response = requests.get(url, headers=sheet_header)
    # print(response.text)
    sheet_data_list = json.loads(response.text)['sheets']
    for sheet_data in sheet_data_list:
        sheet_list.append({'sheetId': sheet_data['properties']['sheetId'], 'title': sheet_data['properties']['title']})
    # print(sheet_list)
    return sheet_list


def get_sheet_data(sheet_title, sheet_header, begin_cell='A1', end_column='L'):
    sheet = sheet_title + '!'
    bengein = begin_cell
    row_end = end_column
    url = 'https://sheets.googleapis.com/v4/spreadsheets/' + sheet_id + '/values:batchGet?ranges=' + sheet + bengein + ':' + row_end
    response = requests.get(url, headers=sheet_header)
    # print(response.text)
    sheet_data = json.loads(response.text)['valueRanges'][0]['values']
    # print(sheet_data)
    return sheet_data


def get_tag_data(data):
    appconfig_list = []
    data = data[1:]
    for i in data:
        temp_url = json.loads(i[6])['tags_config_url']
        if temp_url not in appconfig_list:
            appconfig_list.append(json.loads(i[6])['tags_config_url'])
    # print(appconfig_list)
    return appconfig_list


def get_appconfig_tags():
    tag_list = []
    token = get_token_data()
    # 登录token
    sheet_header = {'Authorization': 'Bearer ' + token}
    sheet_title = get_all_sheet(sheet_header)[0]['title']
    sheet_data = get_sheet_data(sheet_title, sheet_header)
    new_appconfig = get_tag_data(sheet_data)
    for url in new_appconfig:
        response = requests.get(url)
        temp_tags = json.loads(response.text)['tags']
        for tag in temp_tags:
            if tag not in tag_list:
                tag_list.append(tag)
    return tag_list


@app.route("/get_tags")
async def get_tags(requset):
    data = get_appconfig_tags()
    return sanic_json({"data": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
