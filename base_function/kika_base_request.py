# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import hashlib
import random
import os
import sys
from utils.Utils import *


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

    # 设定header
    def set_header(self, duid, lang='en_AU', app='kika', version=1477, way='online'):
        lange_config = config_reader('./congif/lange')
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
        # print('取模结果：')
        # print(group)
        return group

    # 获取对应取模值的duid
    def get_duid_in_way(self, way, result):
        while True:
            duid = self.random_duid()
            if self.which_group(way, duid) == result:
                break
        return duid
