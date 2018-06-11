# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from base_function.create_case_yaml import create_case_list
from base_function.running_template import case_runner
import sys, getopt
from utils.wechat import run_wechat


def run(argv):
    try:
        opts, args = getopt.getopt(argv, "h:f:s:w:", ["foldername=", "source="])
    except getopt.GetoptError:
        print('run_devops.py -f <foldername> -s <source> -w <project>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_devops.py -f <foldername> -s <source> -w <project>')
            sys.exit()
        elif opt in ("-f", "--foldername"):
            foldername = arg
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("-w", "--project_name_in_wechat"):
            project = arg
    print('测试用例:' + foldername)
    print('测试源:' + source)
    # print('微信发送工程名:' + project)
    create_case_list(folder_name=foldername, source=source)
    case_runner()
    try:
        run_wechat(project)
    except:
        pass


if __name__ == '__main__':
    run(sys.argv[1:])
