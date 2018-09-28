# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sigle_request import sigle_request_runner
from content_request import content_request
from base_function.HTMLTestRunner import HTMLTestRunner
from base_function.golable_function import config_reader
from ddt import ddt, data, file_data, unpack
import os
import unittest
from sigle_request import sigle_request_runner
from content_request import content_request
import subprocess

PATH = os.path.dirname(os.path.abspath(__file__))


@ddt
class ApiTest(unittest.TestCase):
    def setUp(self):
        print('Test Begin')

    @file_data(PATH + '/../temp/cases.yaml')
    @unpack
    def test_http_api(self, path, source):
        # print(path, source)
        file_path = PATH + '/../case/' + path
        try:
            run_way = config_reader(file_path)['operation_mode']
        except:
            run_way = 'py'
        if run_way == 'sigle_request':
            result = sigle_request_runner(file_path, source)
            assert result
        elif run_way == 'content_request':
            result = content_request(file_path, source)
            assert result
        else:
            p = subprocess.Popen('python3 ' + file_path + ' -s ' + source, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            result = str(p.stdout.read().decode())
            print(result)
            if ('失败' in result) or ('AssertionError' in result) or ('Traceback' in result) or ('SyntaxError' in result):
                assert False

    def tearDown(self):
        print('Test Over')


def case_runner():
    # 编辑用例
    # unittest.main()
    a = ApiTest()
    suite = unittest.TestSuite()
    # DDT的坑
    discover = unittest.defaultTestLoader.discover(PATH, pattern='running_template.py', top_level_dir=None)
    for test_suit in discover:
        for case in test_suit:
            suite.addTest(case)
    # 执行用例
    # runner = unittest.TextTestRunner()
    filename = PATH + '/../report/Api_test_report.html'
    try:
        os.mkdir(PATH + '/../report')
    except:
        pass
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='接口自动化测试报告', description='接口自动化测试报告')
    runner.run(suite)
    fp.close()


if __name__ == "__main__":
    case_runner()
