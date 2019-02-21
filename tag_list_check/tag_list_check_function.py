# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import hashlib
import random
import yaml
import threading
import requests
import json
import time
from tag_list_check.get_data_from_googlesheet import appconfig_data
from base_function.Inspection_method import Inspection_method


def config_reader(Yaml_file):
    yf = open(Yaml_file)
    yx = yaml.load(yf)
    yf.close()
    return yx


# 随机udid值
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


# popup分组计算
def sum_duid(duid):
    sum_result = 0
    a_ = []
    for i in duid:
        # print(i)
        d = int(i, 16)
        # print(d)
        a_.append(d)
        sum_result += int(d)
        # print(sum_result)
    return sum_result


# 根据取模数确认分组
def which_group(way, duid):
    duid_value = sum_duid(duid)
    group = duid_value % int(way)
    # print('取模结果：')
    # print(group)
    return group


# 获取对应取模值的duid
def get_duid_in_way(way, result):
    while True:
        duid = random_duid()
        if which_group(way, duid) == result:
            break
    return duid


class Tag_list_check:
    def __init__(self):
        self.version = 1477
        self.old_ikey = 1844
        self.new_ikey = 1845
        self.old_kika = 2484
        self.new_kika = 2485
        self.old_pro = 370
        self.new_pro = 371
        self.new2_kika = 2879
        self.new2_ikey = 2879
        self.new2_pro = 2879
        self.host = 'api.kikakeyboard.com'
        self.way = 'online'
        self.tags_config_format = {
            "tags": ['@@@'],
            "tags_after_send": ['@@@'],
            "delay_when_typing": 'Int',
            "delay_configs": [{
                "delay": 'Int',
                "tags": ['@@@']
            }]
        }

    # 根据udid获取sign
    def get_sign(self, app, version, duid):
        if app == None or version == None or duid == None:
            sign = False
        else:
            if 'pro' == app:
                app_key = '4e5ab3a6d2140457e0423a28a094b1fd'
                security_key = '58d71c3fd1b5b17db9e0be0acc1b8048'
                # package_name =

            elif 'ikey' == app:
                app_key = 'e2934742f9d3b8ef2b59806a041ab389'
                security_key = '2c7cd6555d6486c2844afa0870aac5d6'
                # package_name =
            else:
                app_key = '78472ddd7528bcacc15725a16aeec190'
                security_key = '6f43e445f47073c4272603990e9adf54'
                # package_name =
            base = 'app_key' + app_key + 'app_version' + str(version) + 'duid' + str(duid)
            m = hashlib.md5()
            m.update(base.encode('utf-8'))
            sign = m.hexdigest()
        # print(sign)
        return sign

    # 设定header
    def set_header(self, duid, lang='en', app='kika', version=1477, way='online'):
        lange_config = config_reader('./lange')
        use_lang = lange_config[lang]
        if 'pro' == app:
            app_key = '4e5ab3a6d2140457e0423a28a094b1fd'
            security_key = '58d71c3fd1b5b17db9e0be0acc1b8048'
            # 这个错误的
            package_name = 'com.emoji.coolkeyboard'

        elif 'ikey' == app:
            app_key = 'e2934742f9d3b8ef2b59806a041ab389'
            security_key = '2c7cd6555d6486c2844afa0870aac5d6'
            # 这个错误的
            package_name = 'com.emoji.ikeyboard'
        else:
            app_key = '78472ddd7528bcacc15725a16aeec190'
            security_key = '6f43e445f47073c4272603990e9adf54'
            package_name = 'com.qisiemoji.inputmethod'
        if way == 'online':
            # 线上
            # User-Agent package_name/app_version (udif/app_key)
            header = {'Accept-Charset': 'UTF-8',
                      'Kika-Install-Time': '1505198889124',
                      'Connection': 'Keep-Alive',
                      'Accept-Language': '%s' % use_lang[0],
                      'User-Agent': '%s/%s (%s/%s) Country/%s Language/%s System/android Version/23 Screen/480' % (
                          package_name, version, duid, app_key, use_lang[1], use_lang[2]),
                      'X-Model': 'D6603', 'Accept-Encoding': 'gzip'}
            # header = {
            #     'User-Agent': '%s/%s (%s/%s) Country/%s Language/%s System/android Version/23 Screen/480' % (
            #         package_name, version, duid, app_key, use_lang[1], use_lang[2])}
        else:
            # 测试
            header = {'Accept-Charset': 'UTF-8',
                      'Kika-Install-Time': '1505198889124',
                      'Connection': 'Keep-Alive',
                      'Host': self.host,
                      'Accept-Language': '%s' % use_lang[0],
                      'User-Agent': '%s/%s (%s/%s) Country/%s Language/%s System/android Version/23 Screen/480' % (
                          package_name, version, duid, app_key, use_lang[1], use_lang[2]),
                      'X-Model': 'D6603', 'Accept-Encoding': 'gzip'}

        return header

    def google_sheet_data(self):
        data = appconfig_data()
        for i in data:
            if i['data']['style'] == 'new':
                if i['data']['product'] == 'ikey':
                    i['data'].update({'version': self.new_ikey})
                elif i['data']['product'] == 'kika':
                    i['data'].update({'version': self.new_kika})
                elif i['data']['product'] == 'pro':
                    i['data'].update({'version': self.new_pro})
            elif i['data']['style'] == 'new2':
                if i['data']['product'] == 'ikey':
                    i['data'].update({'version': self.new2_ikey})
                elif i['data']['product'] == 'kika':
                    i['data'].update({'version': self.new2_kika})
                elif i['data']['product'] == 'pro':
                    i['data'].update({'version': self.new2_pro})
            else:
                if i['data']['product'] == 'ikey':
                    i['data'].update({'version': self.old_ikey})
                elif i['data']['product'] == 'kika':
                    i['data'].update({'version': self.old_kika})
                elif i['data']['product'] == 'pro':
                    i['data'].update({'version': self.old_pro})
            if i['data']['duid'] == 'random':
                i['data']['duid'] = random_duid()
            else:
                i['data']['duid'] = get_duid_in_way(int(i['data']['duid'][0]), int(i['data']['duid'][1]))
        return data

    # url 重新拼接
    def url_mosaic(self, data):
        url = 'https://api.kikakeyboard.com/v1/utils/get_app_config?key=sticker2&'
        url = url + 'sign=' + self.get_sign(version=data['data']['version'], duid=data['data']['duid'],
                                            app=data['data']['product'])
        # print(url)
        return url

    def data_content(self, check_value, response):
        fail_key = []
        keys = list(check_value.keys())
        response = response['data']
        if set(keys) == set(response.keys()):
            for i in keys:
                if response[i] == check_value[i]:
                    pass
                else:
                    # print(response[i])
                    # print(check_value[i])
                    fail_key.append(i)
        else:
            fail_key.append('response中key值不正确')
        return fail_key

    # 检查
    def asser_api(self, data, check_value, response, fail):
        fail_data = {}
        reason = []
        if response.status_code != 200:
            reason.append('接口返回值不等于200')
        try:
            response_data = json.loads(response.text)
            data_content_result = self.data_content(check_value, response_data)
            if len(data_content_result) > 0:
                print(response_data)
                reason.append('接口数据错误,错误key为:' + str(data_content_result))
        except Exception as e:
            print(e)
            print('非JSON')
            print(data)
            print(json.loads(response.text))
            fail_data.update({'data': data, 'reason': '返回内容错误非JSON'})
            fail.append(fail_data)
        if len(reason) > 0:
            fail_data.update({'data': data, 'reason': reason})
            fail.append(fail_data)

            # 检查

    # cdn下载内容格式检查
    def new_cdn_check(self, data, check_value, response, fail_data):
        tags_config_url = json.loads(response.text)['data']['tags_config_url']
        tags_config_url_response = requests.get(tags_config_url)
        tags_config_url_response.encoding = 'utf-8'
        json_tags_config_url_response = json.loads(tags_config_url_response.text)
        Im = Inspection_method().response_diff_list(check_value, json_tags_config_url_response, diff=[])
        if Im == False:
            fail_data.update({'data': data, 'reason': 'tags_config_url文件中内容格式有误'})

    # 发送请求
    def url_request(self, data, fail, all_response):
        lang = data['data']['language']
        duid = data['data']['duid']
        app = data['data']['product']
        version = int(data['data']['version'])
        header = self.set_header(duid, app=app, version=version, lang=lang, way=self.way)
        url = self.url_mosaic(data)
        response = requests.request('get', url, headers=header)
        response.encoding = 'utf-8'
        # print(response.text)
        self.asser_api(data['data'], data['check_value'], response, fail)
        if version == self.new_ikey or version == self.new_kika or version == self.new_pro:
            self.new_cdn_check(data, self.tags_config_format, response=response, fail_data=fail)
        all_response.append({'data': 'data', 'response': response.text})

    # 多线程处理,单个用例
    def Multithreading_api(self):
        all_response = []
        fail = []
        start_time = time.time()
        proc_record = []
        all_test = self.google_sheet_data()
        for i in all_test:
            th = threading.Thread(target=self.url_request, args=(i, fail, all_response))
            print(th)
            th.setDaemon(True)
            th.start()
            proc_record.append(th)
        for e in proc_record:
            e.join()
        print('所用时间:')
        print(time.time() - start_time)
        print('有误的配置内容:')
        print('有误数量:' + str(len(fail)))
        print('所有误解返回内容:')
        print(fail)
        print('所有返回结果:')
        # print(all_response)
        if len(fail) != 0:
            print('有失败的内容！！！！！！！！！')
            print(len(fail))
        else:
            print('测试通过！！！！')


if __name__ == "__main__":
    tag_check = Tag_list_check()
    tag_check.Multithreading_api()
