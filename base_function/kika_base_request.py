# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import hashlib
import random
import os
import sys
import time
from base_function.golable_function import config_reader

PATH = os.path.dirname(os.path.abspath(__file__))


class Kika_base_request:
    def __init__(self, host):
        self.host = host

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

    def get_new_sign(self, app, version, duid, requestime):
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
            base = 'app_key' + app_key + 'app_version' + str(version) + 'request_time' + str(requestime)
            m = hashlib.md5()
            m.update(base.encode('utf-8'))
            sign = m.hexdigest()
        # print(sign)
        return sign

    # 设定header
    def set_header(self, duid, lang='en_AU', app='kika', version=1477, way='online', android_level=23):
        lange_config = config_reader(PATH + '/../config/lange')
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
                      'Host': self.host,
                      'Accept-Language': '%s' % use_lang[0],
                      'User-Agent': '%s/%s (%s/%s) Country/%s Language/%s System/android Version/%s Screen/480' % (
                          package_name, version, duid, app_key, use_lang[1], use_lang[2], android_level),
                      'X-Model': 'D6603', 'Accept-Encoding': 'gzip'}
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

    def set_new_header(self, duid, lang='en_AU', app='kika', version=1477, way='online', android_level=23):
        lange_config = config_reader(PATH + '/../config/lange')
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
                      'Host': self.host,
                      'Accept-Language': '%s' % use_lang[0],
                      'User-Agent': '%s/%s (/%s) Country/%s Language/%s System/android Version/%s Screen/480' % (
                          package_name, version, app_key, use_lang[1], use_lang[2], android_level),
                      'X-Model': 'D6603', 'Accept-Encoding': 'gzip',
                      'Request-Time': str(int(str(int(time.time())) + '000'))}
        else:
            # 测试
            header = {'Accept-Charset': 'UTF-8',
                      'Kika-Install-Time': '1505198889124',
                      'Connection': 'Keep-Alive',
                      'Host': self.host,
                      'Accept-Language': '%s' % use_lang[0],
                      'User-Agent': '%s/%s (/%s) Country/%s Language/%s System/android Version/23 Screen/480' % (
                          package_name, version, app_key, use_lang[1], use_lang[2]),
                      'X-Model': 'D6603', 'Accept-Encoding': 'gzip',
                      'Request-Time': str(int(str(int(time.time())) + '000'))}

        return header

    # 随机udid值
    def random_duid(self):
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
    def sum_duid(self, duid):
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
    def which_group(self, way, duid):
        duid_value = self.sum_duid(duid)
        group = duid_value % int(way)
        return group

    # 获取对应取模值的duid
    def get_duid_in_way(self, way, result):
        while True:
            duid = self.random_duid()
            if self.which_group(way, duid) == result:
                break
        return duid


if __name__ == "__main__":
    print(int(str(int(time.time())) + '000'))
