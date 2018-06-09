# -*- coding: utf-8 -*-
# __author__ = 'Gz'

import sys
import requests
import json
from bs4 import BeautifulSoup
import os

PATH = os.path.dirname(os.path.abspath(__file__))


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


s = requests.session()


def GetToken():
    gettokenurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wx9aa61050f274999a&corpsecret=aTCK74QW3RNPoUEI5JYSoeVsoHZjs8GKmtwg0RoSjhuVo9S0BwxnAbSwYpk3A55S'
    r = s.get(gettokenurl)
    gettoken = r.text
    access_token_value = json.loads(gettoken, object_hook=JSONObject).access_token
    # print(access_token_value)
    return access_token_value


def parameter(touser, toparty, totag, msgtype, agentid, text, safe):
    # 客户端崩溃的是3
    url = '{\"touser\": \"' + touser + '\",' + '\"toparty\": \"' + toparty + '\",' + '\"totag\": \"' + totag + '\",' + '\"msgtype\": \"' + msgtype + '\",' + '\"agentid\": \"' + agentid + '\",' + '\"text\": {\"content\": \"' + text + '\"},' + '\"safe\": \"' + safe + '\"}'
    return url


def SendInfo(user, content):
    ret_val = parameter(user, '', '', 'text', '3', content, '0')
    # print(ret_val)
    access_token_value = GetToken()
    sendurl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token_value
    r = s.post(sendurl, data=ret_val)
    # print(r.text)


if __name__ == '__main__':
    text = 'ip_group Fail !!!!!!'
    text1 = 'test'
    with open(PATH + '/../report/Api_test_report.html') as f:
        soup = BeautifulSoup(f)
        # all_data = soup.prettify()
        try:
            fail_count = soup.find_all('tr', class_='failClass')
            SendInfo('guanzhao', text)
        except:
            SendInfo('guanzhao', text1)
