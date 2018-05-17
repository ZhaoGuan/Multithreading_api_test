# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml
import sys, getopt


def config_reader(Yaml_file):
    yf = open(Yaml_file)
    yx = yaml.load(yf)
    yf.close()
    return yx


def source_input():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "h:s:", ["source="])
    except getopt.GetoptError:
        print('xxx.py  -s <source>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('xx.py -s <source>')
            sys.exit()
        elif opt in ("-s", "--source"):
            source = arg
        else:
            print('失败,未填写source')
    return source
