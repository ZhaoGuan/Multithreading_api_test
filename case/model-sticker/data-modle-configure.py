# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import pymysql
import random
import hashlib
import json
import requests
import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + '/../../')
from base_function.golable_function import source_input
from base_function.Inspection_method import Inspection_method

config = ''


# 获取数据库信息作为用例准备
def get_test_data(source):
    if 'online' in source:
        # 线上数据库
        db = pymysql.connect("kika-backend-sticker-mysql1.intranet.com", "stickeruser0", "sw3JobOT96#0",
                             "kika_sticker_model")
    else:
        # 测试服数据库
        db = pymysql.connect("kika-backend-test1.intranet.com", "rwuser", "xinmei365", "kika_sticker_model")
    cursor = db.cursor()
    sql_r_scenario = "SELECT id, name , create_time,properties FROM r_scenario"
    sql_r_bucket_strategy = "SELECT scenario_id, config  FROM r_bucket_strategy"
    # 查询r_scenario表
    cursor.execute(sql_r_scenario)
    r_scenario_results = cursor.fetchall()
    # print(r_scenario_results)
    parameter = {}
    for row in r_scenario_results:
        table_id = row[0]
        name = row[1]
        create_time = row[2]
        properties = row[3]
        # 打印结果
        # print("id=%s,name=%s,properties=%s,properties=%s" % (table_id, name, create_time, properties))
        parameter.update({table_id: {'properties': properties, 'scenario': name}})
    # 查询r_bucket_strategy表
    cursor.execute(sql_r_bucket_strategy)
    r_scenario_results = cursor.fetchall()
    data = []
    for row in r_scenario_results:
        scenario_id = row[0]
        config = row[1]
        # print("scenario_id=%s,config=%s" % (scenario_id, config))
        data.append({'parameter': parameter[scenario_id], 'bucket_config': config})
    # print(data)
    db.close()
    return data


def random_duid():
    all_world = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    world = random.sample(all_world, 5)
    result_world = ''
    for i in world:
        result_world += i
    m = hashlib.md5()
    m.update(result_world.encode('utf-8'))
    MD5 = m.hexdigest()
    # print(MD5)
    return MD5


def duid_to_number(duid):
    # 转十进制
    duid = int(duid, 16)
    # print(duid)
    # 取小于100000000的尾部
    duid = str(duid)[-9:]
    if int(duid) < 10000000:
        pass
    else:
        duid = duid[-8:]
    return int(duid)


def duid_for_bucket(configList):
    duid_list = []
    bucket_name = []
    configList = json.loads(configList)['configList']
    print(configList)
    all_weight = 0
    for i in configList:
        all_weight += i['weight']
    while True:
        temp_duid = ''
        temp_bucketName = ''
        duid = random_duid()
        duid_number = duid_to_number(duid) % 100
        for e in configList:
            v = e['weight'] * 100 / all_weight
            if duid_number >= v:
                duid_number -= v
                continue
            else:
                temp_duid = {'duid': duid, 'bucketName': e['bucketName'], 'weight': e['weight']}
                temp_bucketName = e['bucketName']
                break
        if (temp_bucketName != '') and (temp_bucketName not in bucket_name):
            bucket_name.append(temp_bucketName)
            duid_list.append(temp_duid)
        if len(bucket_name) == len(configList):
            break
    print(duid_list)
    return duid_list


def constitute_test_case(data):
    test_case = []
    for case in data:
        parameter = json.loads(case['parameter']['properties'])
        scenario = case['parameter']['scenario']
        duid_list = duid_for_bucket(case['bucket_config'])
        for duid_data in duid_list:
            temp = {'parameter': {}, 'result': {}}
            temp['result'].update({'scenario': scenario})
            buckname = duid_data['bucketName']
            weight = duid_data['weight']
            duid = duid_data['duid']
            temp['result'].update({'bucketName': buckname, 'weight': weight})
            temp['parameter'].update({'userId': duid})
            for key, value in parameter.items():
                temp['parameter'].update({key: value})
                if ('Giphy' in str(temp)) or ('Tenor' in str(temp)):
                    pass
                elif 'SilentUserBucket' in str(temp):
                    pass
                else:
                    test_case.append(temp)
    print(test_case)
    # print(len(test_case))
    return test_case


def case_runner(test_case, url):
    print(url)
    for key, value in test_case['parameter'].items():
        url = url + key + '=' + value + '&'
    url = url[:-1]
    print(url)
    response = requests.get(url)
    try:
        response = json.loads(response.text)
        print(response)
        # config_diff = Inspection_method().response_diff_list(config, response.text, diff)
        # if config_diff == False:
        #     print('数据结构有误')
        #     print('失败')
        if response['extra']['scenario'] != test_case['result']['scenario']:
            print(test_case)
            print('失败')
            print('scenario错误 ' + '预期为 ' + test_case['result']['scenario'])
        if response['extra']['bucketName'] != test_case['result']['bucketName']:
            print(test_case)
            print(response)
            print('bucketName错误 ' + '预期为 ' + test_case['result']['bucketName'])
            print('失败')
    except Exception as e:
        print(e)
        print('失败')
        print(url)
        print(test_case)


def request_test(test_case, source):
    if source == 'test':
        # 测试
        # 外网
        url = 'http://52.43.155.219:8080/model-sticker/recommend/popup?sessionId=123&tag=ok&'
    elif source == 'ip':
        # 内网
        url = 'http://172.31.23.134:8080/model-sticker/recommend/popup?sessionId=123&tag=ok&'
    elif source == 'spring':
        # 内网
        url = 'http://172.31.23.134:10010/model-sticker/recommend/popup?sessionId=123&tag=ok&'
    elif source == 'pt_online':
        # 线上
        # pt
        url = 'http://172.31.21.95:8080/recommend/popup?sessionId=123&tag=ok&'
    elif source == 'en_online':
        # en
        # 0
        url0 = 'http://172.31.17.179:8080/recommend/popup?sessionId=123&tag=ok&'
        # 1
        url1 = 'http://172.31.28.21:8080/recommend/popup?sessionId=123&tag=ok&'
        # 2
        url2 = 'http://172.31.18.118:8080/recommend/popup?sessionId=123&tag=ok&'
        url = [url0, url1, url2]
    elif source == 'kika_online':
        # kika
        # url = 'http://kika-en.recommend.model.intranet.com/recommend/popup?sessionId=123&tag=ok&'
        url = 'http://172.31.21.219:8080/recommend/popup?sessionId=123&tag=ok&'
    elif source == 'business':
        url = 'http://172.31.31.224:8080/recommend/popup?sessionId=123&tag=ok&'
    if isinstance(url, list):
        for url_ in url:
            case_runner(test_case, url_)
    else:
        case_runner(test_case, url)
        # print(url)


def run(source):
    test_case = get_test_data(source)
    for case in constitute_test_case(test_case):
        request_test(case, source)


if __name__ == "__main__":
    run(source_input())
