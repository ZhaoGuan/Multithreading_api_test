# coding=utf-8
# __author__ = 'Gz'
import json


# 根据数据类型生成校验参数
def data_type_case(data):
    if isinstance(data, str) and 'http' in data:
        data_type = 'HTTP'
    elif isinstance(data, bool):
        data_type = 'Bool'
    elif isinstance(data, str):
        data_type = 'Str'
    elif isinstance(data, int):
        data_type = 'Int'
    else:
        # 处理了None
        data_type = '$$$'
    return data_type


# content数据清洗
# 把接口中的值清理了
# 如果遇到的是一个LIST那么默认其中所有的内容都是一致的只保留一个模板内容
def ergodic_list(data):
    if isinstance(data, list):
        for i in range(len(data)):
            if i == 0:
                if isinstance(data[i], str) or isinstance(data[i], int) or isinstance(data[i], bool) or data[i] == None:
                    data[i] = data_type_case(data[i])
                    print('list中存放的不是dict')
                else:
                    ergodic_list(data[i])
            else:
                data[i] = None
    elif isinstance(data, dict):
        for key in data.keys():
            if isinstance(data[key], str) or isinstance(data[key], int) or isinstance(data[key], bool) or data[
                key] == None:
                data[key] = data_type_case(data[key])
            else:
                ergodic_list(data[key])
    return data


def ergodic_new(data):
    if isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], str) or isinstance(data[i], int) or isinstance(data[i], bool) or data[i] == None:
                data[i] = data_type_case(data[i])
            else:
                ergodic_new(data[i])
    elif isinstance(data, dict):
        for key in data.keys():
            if isinstance(data[key], str) or isinstance(data[key], int) or isinstance(data[key], bool) or data[
                key] == None:
                data[key] = data_type_case(data[key])
            else:
                ergodic_new(data[key])
    return data


# 异常数据处理
# 需要根据具体情况添加主要解决不识别问题
def data_clear(data):
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    data = json.loads(data)
    data = ergodic_list(data)
    return data


if __name__ == "__main__":
    # data内容为response返回内容
    data = '{"errorCode":0,"errorMsg":"ok","data":{"stickers":[{"key":"005552bfc17585560f68ff108148aab4","name":null,"tags":["sticker"],"source_text":"kikatech.com","image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveEmoji/01.png","width":458,"height":270},"mp4":null,"scale_type":1,"mark":"random","popup_duration":5000,"package_id":"38","icon_url":"http://cdn.kikakeyboard.com/sticker_partnerLoveEmoji/icon.png"}],"magics":null,"type":"sticker","popup_duration":5000,"extra":"{}"}}'
    print(data_clear(data))
