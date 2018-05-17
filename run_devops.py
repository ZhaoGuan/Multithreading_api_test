# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from base_function.create_case_yaml import create_case_list
from base_function.running_template import case_runner
import sys, getopt


def run(argv):
    try:
        opts, args = getopt.getopt(argv, "h:f:s:", ["foldername=", "source="])
    except getopt.GetoptError:
        print('run_devops.py -f <foldername> -s <source>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_devops.py -f <foldername> -s <source>')
            sys.exit()
        elif opt in ("-f", "--foldername"):
            foldername = arg
        elif opt in ("-s", "--source"):
            source = arg
    print('测试用例:' + foldername)
    print('测试源:' + source)
    create_case_list(folder_name=foldername, source=source)
    case_runner()


if __name__ == '__main__':
    run(sys.argv[1:])
