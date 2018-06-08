# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import yaml
import os

PATH = os.path.dirname(os.path.abspath(__file__))


def case_list(folder_name):
    folder_path = PATH + '/../case/' + folder_name
    try:
        folder_list = os.listdir(folder_path)
    except:
        print('文件夹填写错误')
        assert False
    result = [folder_name + '/' + folder for folder in folder_list]
    return result


def create_case_list(folder_name, source='online'):
    case_result = {}
    caselist = case_list(folder_name)
    for case in caselist:
        case_result.update({case: {'path': case, 'source': source}})
    with open(PATH + '/../temp/cases.yaml', 'w') as case:
        yaml.dump(case_result, case, default_flow_style=False)


if __name__ == '__main__':
    # case_list('backend-content-sending')
    # create_case_list('backend-content-sending', 'online')
    # create_case_list('backend-content-sending', 'web0')
    # create_case_list('backend-content-sending', 'test')
    # create_case_list('gifsearch', 'online')
    # create_case_list('backend-picture', 'online')
    create_case_list('ip_group', 'test')
