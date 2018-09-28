# -*- coding: utf-8 -*-
# __author__ = 'Gz'

import copy
import json
import threading
import time
from multiprocessing import Process, Queue
from base_function.golable_function import config_reader
import requests
import yaml
import os
import threadpool
import http.client
from base_function.Inspection_method import Inspection_method
from base_function.kika_base_request import Kika_base_request

Inspection_method = Inspection_method()
PATH = os.path.dirname(os.path.abspath(__file__))


class Http_Test:
    def __init__(self, config, source='online'):
        self.config = config
        self.cycle_times = self.config['source'][source]['cycle_times']
        self.url = self.config['source'][source]['url']
        try:
            self.keys = self.config['source'][source]['keys']
        except:
            self.keys = None
        try:
            self.data = self.config['source'][source]['data']
            # 如果data中有为空的默认data为空
            if 'None' in str(self.data):
                self.data = None
        except:
            self.data = None
        try:
            self.check_way = self.config['source'][source]['check_way']
        except:
            self.check_way = None
        # version处理
        try:
            if self.data['version'] == None:
                self.data.pop('version')
        except:
            pass
        try:
            self.other = self.config['other']
        except:
            self.version = 1477
            self.way = 'online'
            self.host = 'api.kikakeyboard.com'
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
            self.host = None
        try:
            self.Assert = self.config['assert']
        except:
            self.Assert = None
        # 默认version
        # self.version = 1477
        # ikey 1477以上支持magictext
        self.version = 2732
        self.kika_request = Kika_base_request(self.host)
        self.fail_list = []
        self.all_list = []

    # version处理
    def handle_version(self, version_data, keys_data):
        if '&' in str(version_data):
            data = version_data.split('&')
            condition = data[:-1]
            version = data[-1]
            condition_count = 0
            for i in condition:
                if i in keys_data.values():
                    condition_count += 1
            if condition_count == len(condition):
                keys_data.update({'version': version})
        else:
            keys_data.update({'version': version_data})

    # now_way
    def check_the_way(self, all_data):
        if (self.check_way == None) or (self.check_way == []):
            return all_data
        else:
            temp = []
            for check in self.check_way:
                for data in all_data:
                    if check in str(data):
                        data.update({'check': 'new'})
                        temp.append(data)
                    else:
                        temp.append(data)
                return temp

    # url key 数据整理
    def url_keys_data(self):
        all_data = []
        config_data = self.data
        copy_data = copy.deepcopy(self.data)
        try:
            copy_data.pop('version')
        except:
            pass
        data_keys = list(list(copy_data.keys()))
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
                    for g in temp:
                        temp_all.append(g)
                all_data = temp_all
        all_data = self.check_the_way(all_data)
        # 处理version
        temp_all_data = []
        for data in all_data:
            if 'version' not in config_data.keys():
                data.update({'version': self.version})
            else:
                for v in config_data['version']:
                    copy_data = copy.deepcopy(data)
                    self.handle_version(v, copy_data)
                    if 'version' not in list(copy_data.keys()):
                        copy_data.update({'version': self.version})
                    temp_all_data.append(copy_data)
                all_data = temp_all_data
        return all_data

    # url 重新拼接
    def url_mosaic(self, data, header):
        url = self.url
        keys = self.keys
        if keys != None:
            if ('&' == url[-1]) or ('?' == url[-1]):
                for i in keys:
                    if i != keys[-1]:
                        url = url + i + '=' + data[i] + '&'
                    else:
                        url = url + i + '=' + data[i]
                if 'duid' in url:
                    if ('check' in list(data.keys())):
                        sign = self.kika_request.get_new_sign(version=data['version'], duid=data['duid'],
                                                              app=data['app'],
                                                              requestime=header['Request-Time'])
                    else:
                        sign = self.kika_request.get_sign(version=data['version'], duid=data['duid'], app=data['app'])
                    re_sign = 'sign=' + sign
                    duid = 'duid=' + data['duid']
                    url = url.replace(duid, re_sign)
        return url

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
        try:
            Assert_data_response_header = Assert['response_header']
        except:
            Assert_data_response_header = None
        fail_data = {}
        reason = []
        if response.status_code != 200:
            reason.append('接口返回值不等于200,返回内容为:' + str(response.status_code))
        try:
            response_data = json.loads(response.text)
            if Assert_code != None:
                code = response_data[Assert['code']['key']]
                if code != int(Assert['code']['value']):
                    reason.append('接口对应code' + Assert['code']['key'] + '值错误,返回内容为' + str(code))
            if Assert_data_format != None:
                case = Assert['data_format']
                if '&' in str(case.keys()):
                    for i in case.keys():
                        condition = json.loads(i)
                        if Inspection_method.response_value(list(condition.keys())[0], response_data) == \
                                list(condition.values())[0]:
                            case = case[i]
                            break
                    data_format_result = Inspection_method.response_diff_list(case, response_data, [])
                else:
                    data_format_result = Inspection_method.response_diff_list(case, response_data, [])
                if data_format_result == False:
                    reason.append('接口数据格式错误,返回格式为:' + response.text)
            if Assert_data_content != None:
                data_content_result = Inspection_method.data_content(data, Assert_data_content, response_data)
                if data_content_result == False:
                    reason.append('接口数据错误,返回数据为:' + response.text)
            if Assert_data_response_header != None:
                data_response_header_result = Inspection_method.response_headers_check(data,
                                                                                       Assert_data_response_header,
                                                                                       response)
                if data_response_header_result == False:
                    reason.append('接口response header数据错误,headers数据为:' + str(response.headers))
        except Exception as e:
            print(e)
            print('非JSON')
            pass
        if len(reason) > 0:
            fail_data.update({'data': data, 'reason': reason})
            fail.append(fail_data)

    # 请求内容集合
    def all_response(self, data, response, all_data_respone):
        # instet_table(data, response.text)
        all_data_respone.append({'data': data, 'response': response.text})

    # 发送请求
    def url_request(self, data):
        if self.data == None or self.keys == None:
            url = self.url
            header = {'Accept-Charset': 'UTF-8',
                      'Content-type': 'application / json'}
            response = requests.request('get', url, headers=header, timeout=60)
            response.encoding = 'utf-8'

        else:
            lang = data['kb_lang']
            if '%' in data['duid']:
                duid = data['duid'].replace('%', '').split('==')
                duid = self.kika_request.get_duid_in_way(int(duid[0]), int(duid[1]))
                data['duid'] = duid
            else:
                duid = data['duid']
            app = data['app']
            version = int(data['version'])
            try:
                android_level = int(data['android_level'])
            except:
                android_level = 23
            print(data)
            if ('check' in list(data.keys())):
                header = self.kika_request.set_new_header(duid, app=app, version=version, lang=lang, way=self.way,
                                                          android_level=android_level)
            else:
                header = self.kika_request.set_header(duid, app=app, version=version, lang=lang, way=self.way,
                                                      android_level=android_level)
            url = self.url_mosaic(data, header)
            print(header)
            print(url)
            response = requests.request('get', url, headers=header)
            response.encoding = 'utf-8'
            # print(response.headers)
        self.asser_api(data, response, self.fail_list)
        self.all_response(data, response, self.all_list)

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
        result = True
        start_time = time.time()
        if self.data != None:
            all_test = self.url_keys_data()
        else:
            all_test = range(1)
        pool = threadpool.ThreadPool(200)
        for g in range(self.cycle_times):
            pool_requests = threadpool.makeRequests(self.url_request, all_test)
            [pool.putRequest(req) for req in pool_requests]
            pool.wait()
        print('所用时间:')
        print(time.time() - start_time)
        print('有误的配置内容:')
        print('有误数量:' + str(len(self.fail_list)))
        print('所有误解返回内容:')
        for data in self.fail_list:
            print(str(data)[0:1000])
        print('所有返回内容数量:' + str(len(self.all_list)))
        for data in self.all_list:
            print(str(data)[0:1000])
        if len(self.fail_list) != 0 or len(self.all_list) == 0:
            print('有失败的内容！！！！！！！！！')
            result = False
        else:
            print('测试通过！！！！')
        return result

    # 以下弃用
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
        print('所有返回内容:')
        if len(fail) != 0:
            print('有失败的内容！！！！！！！！！')
        else:
            print('测试通过！！！！')

    # 策略C测试
    def c_process(self, single_quantity=1, process_number=4):
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
        print(len(all_pic))
        pic = self.pic_statistics(all_pic)
        print('图片统计结果:')
        print(pic)


def sigle_request_runner(path, source='test'):
    config = config_reader(path)
    test = Http_Test(config, source)
    result = test.Multithreading_api()
    return result


if __name__ == "__main__":
    sigle_request_runner('./case/backend-content-sending/test_case', 'test')
    # sigle_request_runner('./case/backend-content-sending/sentence-popup_type=1.yml', 'web0')
    # sigle_request_runner('./case/backend-content-sending/cache_control')
    # sigle_request_runner('./case/backend-content-sending/Magictext_all', 'web0')
    # sigle_request_runner('./case/backend-content-sending/pro_Tenor_API_test_pt')
    # sigle_request_runner('./case/backend-content-sending/Magictext_all')
    # sigle_request_runner('./case/gifsearch/gif_search', 'test')
    # sigle_request_runner('./case/gifsearch/voice', 'online')
    # sigle_request_runner('./case/backend-content-sending/for_data_modle')
    # sigle_request_runner('./case/backend-picture/sticker2_trending')
    # sigle_request_runner('./case/backend-picture/sticker2_all', 'online')
    # sigle_request_runner('./case/backend-picture/sticker2_all', 'online')
    # sigle_request_runner('./case/ip_group/zk.yml', 'online')
    # sigle_request_runner('./case/advertising/advertising.yml', 'online')
    # sigle_request_runner('./case/advertising/recommendconfig_magictext_list.yml', 'online')
    # sigle_request_runner('./case/advertising/game.yml', 'online')
    # sigle_request_runner('./case/gifkeyboard/tag.yml', 'online')
    # sigle_request_runner('./case/gifsearch/social', 'test')
