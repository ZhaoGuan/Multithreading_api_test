# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import requests
import json


class Inspection_method():
    # http资源验证
    def Http_Resources(self, url):
        # resources = request.
        url = str(url)
        print(str(url))
        if 'http' in url:
            resources = requests.request('head', url).status_code
        else:
            resources = 200
        print(resources)
        if resources == 200:
            resources_result = True
        else:
            resources_result = False
        return resources_result

    # 返回数据详细校验
    def response_data_check_(self, case, response):
        # None处理
        result = True
        if response == None:
            response = '$$$'
        if case == 'HTTP':
            if self.Http_Resources(response) is False:
                result = False
        elif case == 'Bool':
            result = isinstance(response, bool)
        elif case == 'Str':
            # 判断字符串是否为空字符串
            if response != '':
                result = isinstance(response, str)
            else:
                result = False
        elif case == 'Int':
            result = isinstance(response, int)
        elif case == 'Float':
            result = isinstance(response, float)
        else:
            if case != response and case != '@@@':
                result = False
        return result

    # 返回数据校验
    def response_data_check(self, case, response):
        result = []
        if '&' in case:
            case = case.split('&')
            for i in case:
                result.append(self.response_data_check_(i, response))
        else:
            result.append(self.response_data_check_(case, response))
        if True in result:
            return True
        else:
            print(result)
            print('返回数据校验错误,错误内容:')
            print('case:' + str(case))
            print('response:' + str(response))
            return False

    # 返回不同检查数据处理
    # 遇到list不检查list的数量去case中的第一个模板跟response中的内容最对比
    def response_diff_list(self, case, response, diff=[]):
        if isinstance(case, list):
            model = case[0]
            try:
                for i in case:
                    if response != []:
                        for e in response:
                            if isinstance(i, str):
                                diff.append(self.response_data_check(model, e))
                            else:
                                self.response_diff_list(i, e, diff)
                    else:
                        diff.append(False)
                        print('错误内容:')
                        print('case:' + str(case))
                        print('response:' + str(response))
            except Exception as e:
                diff.append(False)
                print(e)
                print('错误内容:')
                print('case:' + str(case))
                print('response:' + str(response))
        elif isinstance(case, dict):
            try:
                # if case.keys() == response.keys():
                for key in case.keys():
                    # 值得类型是list进行忽略检查
                    if isinstance(case[key], list):
                        if isinstance(case[key][0], dict) and ('@@@' not in case[key]):
                            self.response_diff_list(case[key], response[key], diff)
                        else:
                            continue
                    else:
                        if isinstance(case[key], str):
                            diff.append(self.response_data_check(case[key], response[key]))
                        else:
                            if case[key] != response[key]:
                                self.response_diff_list(case[key], response[key], diff)
            except Exception as e:
                diff.append(False)
                print(e)
                print('错误内容:')
                print('case:' + str(case))
                print('response:' + str(response))
        else:
            diff.append(self.response_data_check(case, response))
        if False in diff:
            return False
        else:
            return True

    # response字段获取
    def response_value(self, key_value, response):
        if "&" in str(key_value):
            key_value = key_value.split('&')
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
                print(response)
                print(e)
        return response

    # 数据判断
    def content_check(self, check, data_content_key_, response):
        check_key_get = check.keys()
        check_key = [g for g in check_key_get][0]
        check_value_get = check.values()
        check_value = [z for z in check_value_get][0]
        result_false_count = 0
        # 多种结果可能性
        if '&' in check_value:
            check_value = check_value.split('&')
        response_value = self.response_value(check_key, response)
        # 字段包括在内的判断
        if '~' in check_value:
            check_value = check_value.split('~')[1]
            if check_value not in str(response_value):
                print('数据错误:')
                print(data_content_key_)
                print(str(check))
                print(response)
                result_false_count += 1
                print(result_false_count)
        else:
            if (isinstance(check_value, str) and (
                        (str(response_value) != str(check_value)) or (str(check_value) != "#"))) or (
                        str(response_value) not in list(check_value)):
                print(data_content_key_)
                print(str(check))
                print(response_value)
                result_false_count += 1
        print(result_false_count)
        return result_false_count

    # 有条件数据判断
    def content_check_condition(self, check, condition, data_content_key_, response):
        result_false_count = 0
        check_key_get = check.keys()
        check_key = [g for g in check_key_get][0]
        check_value_get = check.values()
        check_value = [z for z in check_value_get][0]
        if '&' in check_value:
            check_value = check_value.split('&')
        # condition
        condition_key_get = condition.keys()
        condition_key = [g for g in condition_key_get][0]
        condition_value_get = condition.values()
        condition_value = [z for z in condition_value_get][0]
        if '&' in condition_value:
            condition_value = condition.split('&')
        response_value = self.response_value(check_key, response)
        try:
            if str(self.response_value(condition_key, response)) == str(condition_value):
                if (isinstance(str(check_value), str) and (
                                str(response_value) != str(check_value) or str(check_value) != "#")) or (
                            (str(response_value) not in list(check_value)) or (response_value != check_value)):
                    print('对应条件判断值有误：')
                    print(data_content_key_)
                    print(str(check))
                    print(response_value)
                    result_false_count += 1
            else:
                print('数据内容错误:')
                print(data_content_key_ + '对应条件值不存在')
                print('对应判断条件值为：' + str(self.response_value(condition_key, response)))
        except Exception as e:
            print('条件路径有误')
            print(e)
            print(data_content_key_)
            print(str(check))
            print(response_value)
            result_false_count += 1
        return result_false_count

    # data_content无条件判断
    def data_content_check(self, data, data_content_key_, check_data, response):
        # 多检查内容时例如ikey@1 ikey@2
        if '@' in data_content_key_:
            data_content_key = data_content_key_.split('@')[0]
        else:
            data_content_key = data_content_key_
        result_false_count = 0
        try:
            check = check_data
            check = json.loads(check)
            # 解析各个层级
            if '&' in data_content_key:
                data_content_key_ = data_content_key.split('&')
                keys = [f for f in data_content_key_]
                data_list = list(data.values())
                key_result = [g for g in keys if g in str(data_list)]
                if len(key_result) == len(keys):
                    result_false_count = self.content_check(check, data_content_key_,
                                                            response)
            else:
                if data_content_key in list(data.values()):
                    result_false_count = self.content_check(check, data_content_key_,
                                                            response)
        except Exception as e:
            print('data_content数据检查,数据格式有误')
            print(check_data)
            print(e)
            result_false_count += 1
        if result_false_count > 0:
            return False
        else:
            return True

    # data_content有条件判断
    def data_content_check_condition(self, data, data_content_key_, condition, check_data, response):
        # 格式检查
        if '*' in data_content_key_:
            data_content_check_condition_result = self.data_content_check_condition_format(data, data_content_key_,
                                                                                           condition, check_data,
                                                                                           response)
            return data_content_check_condition_result
        else:
            data_content_check_condition_result = self.data_content_check_condition_content(data, data_content_key_,
                                                                                            condition, check_data,
                                                                                            response)
            return data_content_check_condition_result

    # 检查数据结构
    def data_content_check_condition_format(self, data, data_content_key_, condition, check_data, response):
        result_false_count = 0
        try:
            condition = json.loads(condition)
            check_data = json.loads(check_data)
            for key, value in condition.items():
                if self.response_value(key, response) == value:
                    for check_data_key, check_data_value in check_data.items():
                        result = self.response_diff_list(check_data_value,
                                                         self.response_value(str(check_data_key), response), diff=[])
                        if result is False:
                            result_false_count += 1
        except Exception as e:
            print('data_format数据检查,数据格式有误')
            print(data_content_key_)
            print(data)
            print(str(condition))
            print(str(check_data))
            print(response)
            print(e)
            result_false_count += 1
        if result_false_count > 0:
            return False
        else:
            return True

    # 检查数据值
    def data_content_check_condition_content(self, data, data_content_key_, condition, check_data, response):
        if '@' in data_content_key_:
            data_content_key = data_content_key_.split('@')[0]
        else:
            data_content_key = data_content_key_
        result_false_count = 0
        try:
            check = check_data
            check = json.loads(check)
            condition = json.loads(condition)
            if '^' in data_content_key:
                data_content_key_ = data_content_key.split('^')
                keys = [f for f in data_content_key_]
                data_list = list(data.values())
                key_result = [g for g in keys if g in str(data_list)]
                if len(key_result) == len(keys):
                    result_false_count = self.content_check_condition(check,
                                                                      condition, data_content_key_, response)
            else:
                if data_content_key in list(data.values()):
                    result_false_count = self.content_check_condition(check,
                                                                      condition, data_content_key_, response)

        except Exception as e:
            print('data_content数据检查,数据格式有误')
            print(check_data)
            print(e)
            result_false_count += 1
        if result_false_count > 0:
            return False
        else:
            return True

    # 对应字段返回对应值
    def data_content(self, data, content, response):
        result_false_count = 0
        for key, value in content.items():
            # 有条件
            if '^' in value:
                check_data_all = value.split('^')
                # 条件
                check_condition = check_data_all[0]
                # 判断内容
                check_data = check_data_all[-1]
                data_content_result = self.data_content_check_condition(data, key, check_condition, check_data,
                                                                        response)
                if data_content_result == False:
                    result_false_count += 1
                else:
                    pass
            # 无条件
            else:
                check_data = value
                data_content_result = self.data_content_check(data, key, check_data, response)
                if data_content_result is False:
                    result_false_count += 1
        if result_false_count > 0:
            return False
        else:
            return True

    # 检查是否有对应的key有检查是否相等,不得或没有添加到result中
    def key_not_existence_value_not_equal(self, key, value, response_header, result):
        if key in response_header.keys():
            # 只坚持key
            if value == '@@@' and response_header[key] != value:
                result.append(False)
        else:
            result.append(False)

    # response返回内容检查
    def response_headers_check(self, data, herader, response):
        response_header = eval(str(response.headers))
        result = []
        for key, value in herader.items():
            if isinstance(value, str):
                # 检查是否有对应的key有检查是否相等没有为错误
                self.key_not_existence_value_not_equal(key, value, response_header, result)
            else:
                condition = key
                if '&' in condition:
                    condition_ = condition.split('&')
                    condition_key = [f for f in condition_]
                    data_list = list(data.values())
                    key_result = [g for g in condition_key if g in str(data_list)]
                    if len(key_result) == len(condition_key):
                        for header_key, header_value in value.items():
                            self.key_not_existence_value_not_equal(header_key, header_value, response_header, result)
                else:
                    if condition in data.values():
                        for header_key, header_value in value.items():
                            self.key_not_existence_value_not_equal(header_key, header_value, response_header, result)
        if len(result) > 0:
            return False
        else:
            return True
