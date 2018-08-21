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
        resources = requests.request('head', url)
        print(resources.status_code)
        if resources.status_code == 200:
            resources_result = True
        else:
            resources_result = False
        return resources_result

    # 返回数据详细校验
    def response_data_check_(self, case, response):
        if case == '@@@':
            print('有值进行了忽略')
            result = True
        else:
            if case == 'HTTP':
                try:
                    if self.Http_Resources(response) == True:
                        result = True
                    else:
                        result = False
                except:
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
                # None处理
                if response == None:
                    response = '$$$'
                else:
                    # print('存在非None的值')
                    # print(response)
                    pass
                if case == response:
                    result = True
                else:
                    result = False
                    # print(result)
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
        # print(response)
        # if response == None:
        #     pass
        # else:
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
                if case.keys() == response.keys():
                    for key in case.keys():
                        # 值得类型是list进行忽略检查
                        if isinstance(case[key], list):
                            if isinstance(case[key][0], dict):
                                self.response_diff_list(case[key], response[key], diff)
                            else:
                                # dict value检查有@@@忽略(强制转化了下期中的内容），这里是对list数量不对称的处理
                                if '@@@' in case[key]:
                                    continue
                                else:
                                    self.response_diff_list(case[key], response[key], diff)
                        else:
                            if isinstance(case[key], str):
                                diff.append(self.response_data_check(case[key], response[key]))
                            else:
                                if case[key] == response[key]:
                                    pass
                                else:
                                    self.response_diff_list(case[key], response[key], diff)
                else:
                    diff.append(False)
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
                print(response)
                print(e)
        return response

    # 数据判断
    def content_check(self, data_content_result_False, check, data_content_key_, response):
        check_key_get = check.keys()
        check_key = [g for g in check_key_get][0]
        check_value_get = check.values()
        check_value = [z for z in check_value_get][0]
        data_content_result_False = 0
        # 多种结果可能性
        if '&' in check_value:
            check_value = check_value.split('&')
        response_value = self.response_value(check_key, response)
        # 字段包括在内的判断
        if '~' in check_value:
            check_value = check_value.split('~')[1]
            if check_value in str(response_value):
                pass
            else:
                print('数据错误:')
                print(data_content_key_)
                print(str(check))
                print(response)
                data_content_result_False += 1
                print(data_content_result_False)
        else:
            if isinstance(check_value, str):
                if (str(response_value) == str(check_value)) or (str(check_value) == "#"):
                    pass
                else:
                    print(data_content_key_)
                    print(str(check))
                    print(response_value)
                    data_content_result_False += 1
            else:
                if (str(response_value) in list(check_value)) or (response_value == check_value):
                    pass
                else:
                    print(data_content_key_)
                    print(str(check))
                    print(response_value)
                    data_content_result_False += 1
        return data_content_result_False

    # 有条件数据判断
    def content_check_condition(self, data_content_result_False, check, condition, data_content_key_, response):
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
                if isinstance(str(check_value), str):
                    # 有条件数据类型检查
                    if str(response_value) == str(check_value) or str(check_value) == "#":
                        pass
                    else:
                        print('对应条件判断值有误：')
                        print(data_content_key_)
                        print(str(check))
                        print(response_value)
                        data_content_result_False += 1
                else:
                    if (str(response_value) in list(check_value)) or (response_value == check_value):
                        pass
                    else:
                        print('对应条件判断值有误：')
                        print(data_content_key_)
                        print(str(check))
                        print(response_value)
                        data_content_result_False += 1
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
            data_content_result_False += 1
        return data_content_result_False

    # data_content无条件判断
    def data_content_check(self, data, data_content_key_, check_data, response):
        # 多检查内容时例如ikey@1 ikey@2
        if '@' in data_content_key_:
            data_content_key = data_content_key_.split('@')[0]
        else:
            data_content_key = data_content_key_
        data_content_result_False = 0
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
                    data_content_result_False = self.content_check(data_content_result_False, check, data_content_key_,
                                                                   response)
            else:
                if data_content_key in list(data.values()):
                    data_content_result_False = self.content_check(data_content_result_False, check, data_content_key_,
                                                                   response)
        except Exception as e:
            print('data_content数据检查,数据格式有误')
            print(check_data)
            print(e)
            data_content_result_False += 1
        if data_content_result_False > 0:
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
        data_content_result_False = 0
        try:
            condition = json.loads(condition)
            check_data = json.loads(check_data)
            for key, value in condition.items():
                if self.response_value(key, response) != value:
                    pass
                else:
                    for check_data_key, check_data_value in check_data.items():
                        result = self.response_diff_list(check_data_value,
                                                         self.response_value(str(check_data_key), response), diff=[])
                        if result:
                            pass
                        else:
                            data_content_result_False += 1
        except Exception as e:
            print('data_format数据检查,数据格式有误')
            print(data_content_key_)
            print(data)
            print(str(condition))
            print(str(check_data))
            print(response)
            print(e)
            data_content_result_False += 1
        if data_content_result_False > 0:
            return False
        else:
            return True

    # 检查数据值
    def data_content_check_condition_content(self, data, data_content_key_, condition, check_data, response):
        if '@' in data_content_key_:
            data_content_key = data_content_key_.split('@')[0]
        else:
            data_content_key = data_content_key_
        data_content_result_False = 0
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
                    data_content_result_False = self.content_check_condition(data_content_result_False, check,
                                                                             condition, data_content_key_, response)
            else:
                if data_content_key in list(data.values()):
                    data_content_result_False = self.content_check_condition(data_content_result_False, check,
                                                                             condition, data_content_key_, response)

        except Exception as e:
            print('data_content数据检查,数据格式有误')
            print(check_data)
            print(e)
            data_content_result_False += 1
        if data_content_result_False > 0:
            return False
        else:
            return True

    # 对应字段返回对应值
    def data_content(self, data, Assert_data_content, response):
        data_content_result_false = 0
        for key, value in Assert_data_content.items():
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
                    data_content_result_false += 1
                else:
                    pass
            # 无条件
            else:
                check_data = value
                data_content_result = self.data_content_check(data, key, check_data, response)
                if data_content_result == False:
                    data_content_result_false += 1
                else:
                    pass
        if data_content_result_false > 0:
            return False
        else:
            return True

    # 检查是否有对应的key有检查是否相等,不得或没有添加到result中
    def key_not_existence_value_not_equal(self, key, value, response_header, result):
        if key in response_header.keys():
            # 只坚持key
            if value == '@@@':
                pass
            else:
                if response_header[key] == value:
                    pass
                else:
                    result.append(False)
        else:
            result.append(False)

    # response返回内容检查
    def response_headers_check(self, data, Assert_data_herader, response):
        response_header = eval(str(response.headers))
        result = []
        for key, value in Assert_data_herader.items():
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
