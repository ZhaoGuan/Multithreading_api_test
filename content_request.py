# -*- coding: utf-8 -*-
# __author__ = 'Gz'

import json

import requests
import random
import copy

from base_function.Inspection_method import InspectionMethod
from base_function.kika_base_request import Kika_base_request
from base_function.golable_function import config_reader

Inspection_method = InspectionMethod()


class HttpTest:
    def __init__(self, config, source='online'):
        self.config = config
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
        # version处理
        try:
            if self.data['version'] == None:
                self.data.pop('version')
        except:
            pass
        try:
            self.check_way = self.config['source'][source]['check_way']
        except:
            self.check_way = None
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
            self.assert_data = self.config['assert']
        except:
            self.assert_data = None
        # 默认version
        self.version = 1477
        self.kika_request = Kika_base_request(self.host)
        try:
            self.content = self.config['content']
        except:
            self.content = None

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
        print(keys)
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
            else:
                pass
        # print(url)
        return url

    # 检查
    def asser_api(self, data, response, fail):
        assert_data = self.assert_data
        try:
            assert_data_code = assert_data['code']
        except:
            assert_data_code = None
        try:
            assert_data_data_format = assert_data['data_format']
        except:
            assert_data_data_format = None
        try:
            assert_data_data_content = assert_data['data_content']
        except:
            assert_data_data_content = None
        try:
            assert_data_data_response_header = assert_data['response_header']
        except:
            assert_data_data_response_header = None
        fail_data = {}
        reason = []
        if response.status_code != 200:
            reason.append('接口返回值不等于200')
        try:
            response_data = json.loads(response.text)
            if assert_data_code != None:
                code = response_data[assert_data['code']['key']]
                if code != int(assert_data['code']['value']):
                    reason.append('接口对应code' + assert_data['code']['key'] + '值错误,返回内容为' + str(code))
            if assert_data_data_format != None:
                case = assert_data['data_format']
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
            if assert_data_data_content != None:
                data_content_result = Inspection_method.data_content(data, assert_data_data_content, response_data)
                if data_content_result == False:
                    reason.append('接口数据错误,返回数据为:' + response.text)
            if assert_data_data_response_header != None:
                data_response_header_result = Inspection_method.response_headers_check(data,
                                                                                       assert_data_data_response_header,
                                                                                       response)
                if data_response_header_result == False:
                    reason.append('接口response header数据错误,headers数据为:' + str(response.headers))
        except Exception as e:
            print(e)
            print('非JSON')
        if len(reason) > 0:
            fail_data.update({'data': data, 'reason': reason})
            fail.append(fail_data)

    # 请求内容集合
    def all_response(self, data, response, all_data_respone):
        # instet_table(data, response.text)
        all_data_respone.append({'data': data, 'response': response.text})

    # 获取list中的value
    def content_list_value(self, content, key):
        content_value = []
        for i in content:
            content_value.append(i[key])
        return content_value

    # 获取传给下文的信息
    def get_content(self, response):
        content_keys = self.content.split('&')
        for i in content_keys:
            if i == '[]':
                if i != content_keys[-1]:
                    content = self.content_list_value(response, content_keys[-1])
                    break
                else:
                    content = response
            else:
                response = response[i]
                if isinstance(response, str):
                    content = response
        return content

    # 上文请求
    def above_url_request(self, data, fail, all_data_respone):
        if self.data == None or self.keys == None:
            url = self.url
            response = requests.request('get', url)
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
            if ('check' in list(data.keys())):
                header = self.kika_request.set_new_header(duid, app=app, version=version, lang=lang, way=self.way,
                                                          android_level=android_level)
            else:
                header = self.kika_request.set_header(duid, app=app, version=version, lang=lang, way=self.way,
                                                      android_level=android_level)
            url = self.url_mosaic(data, header)
            response = requests.request('get', url, headers=header)
        print(response.text)
        self.asser_api(data, response, fail)
        self.all_response(data, response, all_data_respone)
        if len(fail) == 0:
            content = self.get_content(json.loads(response.text))
        else:
            content = fail
        return content

    # 下文请求
    def below_url_request(self, content, data, fail, all_data_respone):
        # print(content)
        if self.data == None or self.keys == None:
            url = self.url
            response = requests.request('get', url)
        else:
            # 上文内容替换
            for key, value in data.items():
                if value == 'content':
                    data[key] = random.choice(content)
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
            if ('check' in list(data.keys())):
                header = self.kika_request.set_new_header(duid, app=app, version=version, lang=lang, way=self.way,
                                                          android_level=android_level)
            else:
                header = self.kika_request.set_header(duid, app=app, version=version, lang=lang, way=self.way,
                                                      android_level=android_level)
            url = self.url_mosaic(data, header)
            # print(url)
            # 为了package的临时方案
            if 'content=' in url:
                url = url.replace('content=', '').replace('&', '?').replace('/?', '/')
            print(url)
            response = requests.request('get', url, headers=header)
        print(response.text)
        self.asser_api(data, response, fail)
        self.all_response(data, response, all_data_respone)
        return response.text


def content_request(path, source='online'):
    config = config_reader(path)
    # print(config)
    above_config = config['above']
    below_config = config['below']
    above_fail = []
    above_all_data_respone = []
    below_fail = []
    below_all_data_respone = []
    above_test = HttpTest(above_config, source)
    below_test = HttpTest(below_config, source)
    content = above_test.above_url_request(above_test.url_keys_data()[0], above_fail, above_all_data_respone)
    # print(content)
    if len(above_fail) == 0:
        below_test.below_url_request(content, below_test.url_keys_data()[0], below_fail, below_all_data_respone)
        if len(below_fail) > 0:
            print('上文结果通过,下文结果错误，错位内容:\n' + str(below_fail))
            result = False
        else:
            print('测试通过!!!!!!!!!')
            result = True
    else:
        print('上文接口错误，访问内容为:\n' + str(above_fail))
        result = False
    return result


if __name__ == "__main__":
    # content_request('./case/backend-picture/sticker_case', 'online')
    # content_request('./case/backend-picture/gif_case_new.yml', 'test')
    # content_request('./case/backend-picture/sticker2_all_new.yml', 'test')
    content_request('./case/backend-picture/sticker2_package', 'online')
