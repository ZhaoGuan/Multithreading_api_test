# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import binascii
import hashlib
import random
import yaml
import copy
from multiprocessing import Process, Pipe, Manager, Queue
import threading
import requests
import json
import time
from data_sqlite import *


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


class Http_Test:
    def __init__(self, config):
        self.config = config
        self.cycle_times = self.config['cycle_times']
        self.url = self.config['url']
        try:
            self.keys = self.config['keys']
        except:
            self.keys = None
        try:
            self.data = self.config['data']
        except:
            self.data = None
        try:
            self.other = self.config['other']
        except:
            self.version = 2043
            self.way = 'online'
            self.host = 'api.kikakeyboard.com'
        # try:
        #     self.other = self.config['other']
        #     self.version = self.other['version']
        #     if self.version == None:
        #         self.version = 2043
        # except:
        #     self.version = 2043
        try:
            self.other = self.config['other']
            self.way = self.other['way']
            if self.way == None:
                self.way = 'online'
        except:
            self.way = 'online'
        try:
            self.other = self.config['other']
            self.host = self.other['host']
        except:
            if self.way == 'test':
                self.host = 'api-dev.kikakeyboard.com'
            else:
                self.host = 'api.kikakeyboard.com'
        try:
            self.Assert = self.config['assert']
        except:
            self.Assert = None
        # 默认version
        self.version = 2043

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
    def set_header(self, duid, lang='en_AU', app='kika', version=2043, way='online'):
        lange_en = ['en_AU', 'AU', 'en']
        lange_pt = ['pt_BR', 'BR', 'pt']
        lange_es = ['es_AR', 'AR', 'es']
        lange_in = ['in_ID', 'ID', 'in']
        lange_us = ['en_US', 'US', 'en']
        lange_ca = ['en_CA', 'CA', 'en']
        lange_e_in = ['en_IN', 'IN', 'en']
        lange_nz = ['en_NZ', 'NZ', 'en']
        lange_ph = ['en_PH', 'PH', 'en']
        lange_uk = ['en_UK', 'UK', 'en']
        if lang == 'en_AU':
            use_lang = lange_en
        elif lang == 'en_US':
            use_lang = lange_us
        elif lang == 'en_CA':
            use_lang = lange_ca
        elif lang == 'en_IN':
            use_lang = lange_e_in
        elif lang == 'en_NZ':
            use_lang = lange_nz
        elif lang == 'en_PH':
            use_lang = lange_ph
        elif lang == 'en_UK':
            use_lang = lange_uk
        elif lang == 'pt_BR':
            use_lang = lange_pt
        elif lang == 'es_AR':
            use_lang = lange_es
        else:
            use_lang = lange_in
        # print('@@@@@@@@')
        # print(use_lang)
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
                      'Host': self.host,
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

    # url key 数据整理
    def url_keys_data(self):
        all_data = []
        config_data = self.data
        data_keys = self.data.keys()
        for i in data_keys:
            if len(all_data) == 0:
                for f in config_data[i]:
                    all_data.append({i: f})
            else:
                temp_all = []
                for e in config_data[i]:
                    temp = copy.deepcopy(all_data)
                    for f in temp:
                        f.update({i: e})
                        if 'version' not in f.keys():
                            f.update({'version':self.version})
                    for g in temp:
                        temp_all.append(g)
                all_data = temp_all
        # print(all_data)
        # print(len(all_data))
        return all_data

    # url 重新拼接
    def url_mosaic(self, data):
        url = self.url
        keys = self.keys
        for i in keys:
            if i != keys[-1]:
                url = url + i + '=' + data[i] + '&'
            else:
                url = url + i + '=' + data[i]
        if 'duid' in url:
            sign = self.get_sign(version=self.version, duid=data['duid'], app=data['app'])
            re_sign = 'sign=' + sign
            duid = 'duid=' + data['duid']
            url = url.replace(duid, re_sign)
        # print(url)
        return url

    # http资源验证
    def Http_Resources(self, url):
        # resources = request.
        resources = requests.request('get', url)
        # print(resources.status_code)
        if resources.status_code == 200:
            resources_result = True
        else:
            resources_result = False
        return resources_result

    # 返回数据校验
    def response_data_check(self, case, response):
        if case == '&&&':
            print('有值进行了忽略')
            result = True
        else:
            if case == 'HTTP':
                if self.Http_Resources(response) == True:
                    result = True
                else:
                    result = False
            elif case == 'Bool':
                result = isinstance(response, bool)
            elif case == 'Str':
                # 判断字符串是否为空字符串
                result = isinstance(response, str) and response != ''
            elif case == 'Int':
                result = isinstance(response, int)
            else:
                # None处理
                if response == None:
                    response = '$$$'
                else:
                    # print('存在非None的值')
                    pass
                if case == response:
                    result = True
                else:
                    result = False
                    # print(result)
        return result

    # 返回不同检查数据处理
    # 遇到list不检查list的数量去case中的第一个模板跟response中的内容最对比
    def response_diff_list(self, case, response):
        diff_result = True
        diff = []
        if isinstance(case, list):
            model = case[0]
            for i in case:
                for e in response:
                    if isinstance(i, str):
                        diff.append(self.response_data_check(model, e))
                    else:
                        self.response_diff_list(i, e)
        if isinstance(case, dict):
            if case.keys() == response.keys():
                for key in case.keys():
                    # 值得类型是list进行忽略检查
                    if isinstance(case[key], list):
                        # dict value检查有&&&忽略(强制转化了下期中的内容），这里是对list数量不对称的处理
                        if '&&&' in str(case[key]):
                            continue
                        else:
                            self.response_diff_list(case[key], response[key])
                    else:
                        if isinstance(case[key], str):
                            diff.append(self.response_data_check(case[key], response[key]))
                        else:
                            self.response_diff_list(case[key], response[key])
            else:
                diff.append(self.response_data_check(case, response))
        if False in diff:
            diff_result = False
        return diff_result

    # response字段获取
    def response_value(self, key_value, response):
        if "&" in str(key_value):
            key_value = key_value.split('&')
        else:
            pass
        for i in key_value:
            # 遇到list进行处理
            try:
                i = int(i)
            except:
                pass
            # 对层级错误进行报错
            try:
                response = response[i]
            except Exception as e:
                print('不存在字段，内容报错:')
                print(i)
                print(e)
        return response

    # 对应字段返回对应值
    def data_content(self, data, Assert_data_content, response):
        data_content_result = True
        for i in list(Assert_data_content.keys()):
            if '&' in i:
                i_ = i.split('&')
                keys = [f for f in i_]
                data_list = list(data.values())
                key_result = [g for g in keys if g in str(data_list)]
                if len(key_result) == len(keys):
                    check = Assert_data_content[i]
                    check_key_get = json.loads(check).keys()
                    check_key = [g for g in check_key_get][0]
                    check_data_get = json.loads(check).values()
                    check_value = [z for z in check_data_get][0]
                    if check_value == self.response_value(check_key, response):
                        data_content_result = True
                    else:
                        print(str(check))
                        print(str(response))
                        data_content_result = False
            else:
                for e in data.values():
                    if i in e:
                        check = Assert_data_content[i]
                        check_key_get = json.loads(check).keys()
                        check_key = [g for g in check_key_get][0]
                        check_data_get = json.loads(check).values()
                        check_value = [z for z in check_data_get][0]
                        if check_value == self.response_value(check_key, response):
                            data_content_result = True
                        else:
                            print(str(check))
                            print(str(response))
                            data_content_result = False
        return data_content_result

    # 检查
    def asser_api(self, data, response, fail):
        Assert = self.Assert
        try:
            Assert_code = Assert['code']
        except:
            Assert_code = None
        try:
            Assert_data_format = Assert['data_format']
        except:
            Assert_data_format = None
        try:
            Assert_data_content = Assert['data_content']
        except:
            Assert_data_content = None
        fail_data = {}
        reason = []
        if response.status_code != 200:
            reason.append('接口返回值不等于200')
        try:
            response_data = json.loads(response.text)
            if Assert_code != None:
                code = response_data[Assert['code']['key']]
                if code != int(Assert['code']['value']):
                    reason.append('接口对应code' + Assert['code']['key'] + '值错误,返回内容为' + str(code))
            if Assert_data_format != None:
                case = Assert['data_format']
                data_format_result = self.response_diff_list(case, response_data)
                if data_format_result == False:
                    reason.append('接口数据格式错误,返回格式为:' + response.text)
            if Assert_data_content != None:
                data_content_result = self.data_content(data, Assert_data_content, response_data)
                if data_content_result == False:
                    reason.append('接口数据错误,返回数据为:' + response.text)
        except:
            # print('非JSON')
            pass
        if len(reason) > 0:
            fail_data.update({'data': data, 'reason': reason})
            fail.append(fail_data)

    # 请求内容集合
    def all_response(self, data, response):
        instet_table(data, response.text)

    # 发送请求
    def url_request(self, data, fail):
        if self.data == None or self.keys == None:
            url = self.url
            response = requests.request('get', url)
        else:
            lang = data['kb_lang']
            duid = data['duid']
            app = data['app']
            version = data['version']
            header = self.set_header(duid, app=app, version=version, lang=lang, way=self.way)
            url = self.url_mosaic(data)
            # print(header)
            response = requests.request('get', url, headers=header)
        self.asser_api(data, response, fail)
        self.all_response(data, response)

    # 图片统计
    def pic_statistics(self, all_pic):
        pic = {}
        for i in all_pic:
            # print(i)
            i = json.loads(i['response'])['data']['stickers'][0]['key']
            if i not in pic.keys():
                pic.update({i: 1})
            else:
                pic[i] += 1
        return pic

    # 多线程处理,单个用例
    def Multithreading_api(self):
        try:
            create_table()
        except:
            delete_table()
            create_table()
        start_time = time.time()
        if self.data != None:
            all_test = self.url_keys_data()
        else:
            all_test = range(1)
        proc_record = []
        fail = []
        for g in range(self.cycle_times):
            for i in all_test:
                th = threading.Thread(target=self.url_request, args=(i, fail))
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
        print(fail)
        print('所有返回内容:')
        all_data = reader_table()
        print('所有返回内容数量:' + str(len(all_data)))
        print(all_data)

    # 线程
    def threading(self, fail, queue, single_quantity):
        # 多少组测试数据
        if self.data != None:
            all_test = self.url_keys_data()
        else:
            all_test = range(1)
        proc_record = []
        # print(all_test)
        if len(all_test) > 1:
            for i in all_test:
                th = threading.Thread(target=self.url_request, args=(i, fail))
                # print(th)
                th.setDaemon(True)
                th.start()
                proc_record.append(th)
            for f in proc_record:
                f.join()
        else:
            for i in range(single_quantity):
                th = threading.Thread(target=self.url_request, args=(all_test[0], fail))
                th.setDaemon(True)
                th.start()
                proc_record.append(th)
            for f in proc_record:
                f.join()
        queue.put(fail, timeout=2)

    # 进程+线程(总返回内容会有问题）
    def process(self, single_quantity=1, process_number=4):
        try:
            create_table()
        except:
            delete_table()
            create_table()
        queue = Queue(4)
        start_time = time.time()
        fail = []
        proc = []
        cycle = int(self.cycle_times / process_number)
        if cycle < 1:
            cycle = 1
            process_number = self.cycle_times
        for g in range(cycle):
            p_start_time = time.time()
            for i in range(process_number):
                th = Process(target=self.threading, args=(fail, queue, single_quantity))
                print(th)
                proc.append(th)
                th.start()
            for e in proc:
                e.join()
            for g in range(process_number):
                for f in queue.get():
                    fail.append(f)
            print('结束时间:')
            print(int(time.time() - p_start_time))
        print('共用时:')
        print(int(time.time() - start_time))
        print('有误的配置内容数量:')
        print(len(fail))
        print('有误的配置内容:')
        print(fail)
        print('所有返回的数量:')
        all_data = reader_table()
        print(len(all_data))
        print('所有返回内容:')
        print(all_data)

    # 策略C测试
    def c_process(self, single_quantity=1, process_number=4):
        try:
            create_table()
        except:
            delete_table()
            create_table()
        q = Queue()
        start_time = time.time()
        fail = []
        all_pic = []
        p = []
        cycle = int(self.cycle_times / process_number)
        if cycle < 1:
            cycle = 1
            process_number = 1
        for g in range(cycle):
            p_start_time = time.time()
            for i in range(process_number):
                th = Process(target=self.threading, args=(fail, q, single_quantity))
                p.append(th)
                print(th)
                th.start()
            for e in p:
                e.join()
            for g in range(process_number):
                for f in q.get():
                    fail.append(f)
            print(len(all_pic))
            print(all_pic)
            print('结束时间:')
            print(int(time.time() - p_start_time))
        print('共用时:')
        print(int(time.time() - start_time))
        print('有误的配置内容:')
        print(fail)
        all_pic = reader_table()
        print(len(all_pic))
        pic = self.pic_statistics(all_pic)
        print('图片统计结果:')
        print(pic)


if __name__ == "__main__":
    # config = config_reader('./c')
    config = config_reader('./test_case')
    # config = config_reader('./tag_test')
    # print(config)
    test = Http_Test(config)
    test.c_process(10)
    # print(time.time())
    # test.process(single_quantity=10)
    # test.Multithreading_api()
