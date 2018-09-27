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


def run_wechat(project):
    text = project + ' Fail !!!!!!\r\n'
    fail_case = 'fail_case:'
    with open(PATH + '/../report/Api_test_report.html') as f:
    # with open(
    #         './Api_test_report.html') as f:
        soup = BeautifulSoup(f)
        fail_cases = soup.find_all('td', class_='failCase')
        for case in fail_cases:
            case_test = case.string.split(':')[1]
            fail_case += case_test + '\r\n'
        fail_count = len(fail_cases)
        print('failClass数量:')
        print(fail_count)
        if len(fail_cases) > 0:
            print('发送失败结果')
            text += fail_case
            SendInfo('guanzhao|zhangtong', text + ' FailCount:' + str(fail_count))


if __name__ == '__main__':
    # run_wechat('test')
    # content = 'test'
    # SendInfo('guanzhao', content)
    run_wechat('112312')
