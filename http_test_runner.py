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
# from base_function.data_sqlite import *
from base_function.kika_base_request import Kika_base_request

Inspection_method = Inspection_method()
PATH = os.path.dirname(os.path.abspath(__file__))


class Http_Test:
    def __init__(self, config, source='online'):
        self.config = config
        # url
        self.url = self.config['source'][source]['url']
        # url参数
        try:
            self.keys = self.config['source'][source]['parameters']
        except:
            self.keys = None
        # url参数的值
        try:
            self.data = self.config['source'][source]['parameters_data']
            # 如果data中有为空的默认data为空
            if 'None' in str(self.data):
                self.data = None
        except:
            self.data = None
        # headers
        try:
            self.keys = self.config['source'][source]['headers']
        except:
            self.keys = None
        self.fail_list = []
        self.all_list = []

    # url key 数据整理
    def url_parameters_data(self):
        all_data = []
        config_data = self.data
        copy_data = copy.deepcopy(self.data)
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
        return all_data

    # url 重新拼接
    def url_mosaic(self, data, header):
        url = self.url
        keys = self.keys
        if keys == None:
            pass
        else:
            if ('&' == url[-1]) or ('?' == url[-1]):
                for i in keys:
                    if i != keys[-1]:
                        url = url + i + '=' + data[i] + '&'
                    else:
                        url = url + i + '=' + data[i]
            else:
                pass
        # print(url)
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

    # 多线程处理,单个用例
    def Multithreading_api(self):
        result = True
        start_time = time.time()
        if self.data != None:
            all_test = self.url_parameters_data()
        else:
            all_test = range(1)
        pool = threadpool.ThreadPool(200)
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


def sigle_request_runner(path, source='test'):
    config = config_reader(path)
    test = Http_Test(config, source)
    result = test.Multithreading_api()
    return result


if __name__ == "__main__":
    sigle_request_runner('./case/backend-content-sending/test_case', 'test')
