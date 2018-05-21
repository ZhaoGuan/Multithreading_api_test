# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from kafka import KafkaProducer
import requests
import json
import time
import uuid
import pymysql
import sys
import os

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + '/../../')
from base_function.golable_function import source_input

producer = KafkaProducer(bootstrap_servers='172.31.31.80:9092')


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


def bucket_url(mysql_data):
    result = {}
    base_url = 'http://{ip}/model-sticker/recommend/popup?sessionId={sessionId}&tag={tag}&userId={duid}&'
    for scenario_data in mysql_data:
        temp_properties = scenario_data['parameter']['properties']
        temp_properties = json.loads(temp_properties)
        bucket_config = json.loads(scenario_data['bucket_config'])['configList']
        bucket_list = [str(bucket['bucketId']) + ':' + bucket['bucketName'] for bucket in bucket_config]
        temp_url = base_url
        for key, value in temp_properties.items():
            temp_url += key + '=' + value + '&'
        temp_url = temp_url[:-1]
        for bucket in bucket_list:
            result.update({bucket: temp_url})
    return result


def create_kafka_log(url, ip, duid, tag, kb_lang, sessionId_list):
    sessionId = 'sticker' + str(uuid.uuid1()).replace('-', '')
    url = url.format(ip=ip, duid=duid, tag=tag, sessionId=sessionId)
    response = requests.get(url)
    print(url)
    print(response.text)
    response = json.loads(response.text)
    sticker_id = response['md5']
    model = response['model']
    lang = response['extra']['language']
    bucketname = response['extra']['bucketName']
    scenario = response['extra']['scenario']
    hit = response['extra']['taghit']
    # app
    kika = '78472ddd7528bcacc15725a16aeec190'
    ikey = 'e2934742f9d3b8ef2b59806a041ab389'
    if 'kika' in url:
        app = kika
    else:
        app = ikey
    # 埋点第二个extra
    extra_template = '''{\\"taghit\\":\\"''' + hit + '''\\",\\"bucketName\\":\\"''' + bucketname + '''\\",\\"product\\":\\"\\",\\"thresholdScore\\":\\"0.1\\",\\"language\\":\\"''' + lang + '''\\",\\"recommend\\":\\"''' + model + '''\\",\\"source\\":\\"CF\\",\\"sessionId\\":\\"''' + sessionId + '''\\",\\"bucket\\":\\"''' + model + '''\\",\\"alg_hit\\":\\"1\\",\\"scenario\\":\\"''' + scenario + '''\\",\\"cf_score\\":\\"0.9766543\\",\\"gbdt_threshold\\":\\"0.095\\"}'''
    # 正样本
    keyboard_sticker2_suggestion_pop_template = app + ',' + duid + ',172.58.75.133,,1523333340,{"oid":"f8e87d8719babe02c284e18707d1284d","tp":"event","l":"keyboard_sticker2_suggestion_pop","iid":"send","otp":"item","value":0,"extra":{"package_name":"com.snapchat.android","realtime_event":"1","pop_delay":"0","kb_lang":"' + kb_lang + '","source":"recommend","kb_current_time":"1523333338","kb_time_zone":"-8","tags":"' + tag + '","extra":"' + extra_template + '","key_word":"' + tag + '","pop_type":"sticker","item_id":"' + sticker_id + '","lang":"' + lang + '","na":"us","app":"4.8.2.1638","app_vcode":"163801","aid":"b75f9a2e689c576423f6f70f384615369177f1a3","os":"7.1.1","net":0},"ts":1523333338953}'
    # 负样本？
    sticker2_suggestion_template = app + ',' + duid + ',105.112.112.197,,1522654278,{"oid":"74470b3ee5df24a22926ff40da806454","tp":"event","l":"sticker2_suggestion","iid":"pop","otp":"show","value":0,"extra":{"package_name":"com.whatsapp","realtime_event":"1","pop_delay":"300","sticker_id":"' + sticker_id + '","kb_lang":"' + kb_lang + '","source":"recommend","kb_current_time":"1522654268","kb_time_zone":"1","tag":"' + tag + '","extra":' + extra_template + ',"current_text":"Go","lang":"' + lang + '","na":"ng","app":"4.8.2.1871","app_vcode":"187101","aid":"77ef8c15afba3d6793a0a67946a7d5ebe3906e16","os":"5.1","net":0},"ts":1522654268411}'
    # kafka
    # train
    item = 'emoji_appstore'
    message = keyboard_sticker2_suggestion_pop_template
    print(message)
    print('sessionId为:')
    print(sessionId)
    producer.send(item, bytes(message, 'utf-8'))
    producer.flush()
    sessionId_list.append({'sessionId': sessionId, 'data': {'duid': duid, 'tag': tag, 'kb_lang': kb_lang}})


def predict_train(duid, tag, which_bucket, kb_lang, source):
    sessionId_list = []
    if source == 'ip':
        ip = '172.31.23.134:10010'
    elif source == 'pt_online':
        # 线上
        # pt
        ip = '172.31.21.95:8080'
    elif source == 'en_online':
        # en
        # 0
        ip0 = '172.31.17.179:8080'
        # 1
        ip1 = '172.31.28.21:8080'
        # 2
        ip2 = '172.31.18.118:8080'
        ip = [ip0, ip1, ip2]
    mysql_data = get_test_data(source)
    url_dicet = bucket_url(mysql_data)
    try:
        url = url_dicet[which_bucket]
        if isinstance(ip, list):
            for ip_ in ip:
                create_kafka_log(url, ip_, duid, tag, kb_lang, sessionId_list)
        else:
            create_kafka_log(url, ip, duid, tag, kb_lang, sessionId_list)
        return sessionId_list
    except:
        pass


def run_predict_create_kafka(data, source, p_t_time=1):
    sessionId_list = []
    for bucket, duid_tag_kb in data.items():
        which_bucket = bucket
        duid = duid_tag_kb['duid']
        tag = duid_tag_kb['tag']
        kb_lang = duid_tag_kb['kb_lang']
        for i in range(p_t_time):
            sessionId = predict_train(duid, tag, which_bucket, kb_lang, source)
            try:
                for sessionId_ in sessionId:
                    sessionId_list.append(sessionId_)
            except:
                pass
    print(sessionId_list)
    return sessionId_list


def get_train_sessionId():
    url = 'http://172.31.23.134:8000/get_sessionId'
    response = requests.get(url)
    sessionID_list = json.loads(response.text)['data']
    return sessionID_list


def check(data, source, p_t_time=1):
    fail = []
    created_sessionId = run_predict_create_kafka(data, source, p_t_time=1)
    time.sleep(30)
    train_sessionId_list = get_train_sessionId()
    print(train_sessionId_list)
    for sessionId in created_sessionId:
        if sessionId['sessionId'] not in str(train_sessionId_list):
            fail.append(sessionId)
    if len(fail) > 0:
        print('没有找到的sessionId')
        print(fail)
        print('失败')


if __name__ == "__main__":
    data = {'2:PtBeforeBucket': {'duid': '25ad4b27c4c3410784ee7fab223f3a98', 'tag': 'eita', 'kb_lang': 'pt_BR'},
            '15:EnUsBeforeNotMod2GBDTBucket': {'duid': 'bc21bc8ea7ea480d85a0b6df109a0159', 'tag': 'morning',
                                               'kb_lang': 'en_US'},
            '16:KikaEnUsBeforeBucket': {'duid': '37dfbe888ef147c8a83b60588dc2da21', 'tag': 'no', 'kb_lang': 'en_US'},
            '5:EnUsBeforeMod2Bucket': {'duid': '32b4256f0c934e91aaf5f9201ccf4f54', 'tag': 'yea', 'kb_lang': 'en_US'},
            '7:EnUsBeforeNotMod2GBDTMLeapBucket': {'duid': '7bfe28fb712c4b2c9873d0b53458f6a8', 'tag': 'thanks',
                                                   'kb_lang': 'en_US'},
            '11:EnNotUsBeforeGBDTBucket': {'duid': '269145da9def4d52b85c7a4f2893678a', 'tag': 'haha',
                                           'kb_lang': 'ms_MY'},
            }
    # print(run_predict_create_kafka(data=data, source=source_input()))
    check(data=data, source=source_input())
