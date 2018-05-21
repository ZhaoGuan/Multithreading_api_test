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
    data = '''{"errorCode": 0, "errorMsg": "ok", "data": {"resourceList": [{"mp4": {
        "url": "https://media1.giphy.com/media/HEBsq3fwU5R6w/200.mp4?cid=029136eb5b024b88485954552e79212c",
        "width": 377, "height": 200, "duration": -1.0}, "gif": {
        "url": "https://media1.giphy.com/media/HEBsq3fwU5R6w/200.gif?cid=029136eb5b024b88485954552e79212c",
        "width": 377, "height": 200}, "tinygif": {
        "url": "https://media1.giphy.com/media/HEBsq3fwU5R6w/200.gif?cid=029136eb5b024b88485954552e79212c",
        "width": 377, "height": 200}, "tiny_gif": {
        "url": "https://media1.giphy.com/media/HEBsq3fwU5R6w/200.gif?cid=029136eb5b024b88485954552e79212c",
        "width": 377, "height": 200}, "title": "", "source_id": "HEBsq3fwU5R6w",
                                                                         "preview": "https://media1.giphy.com/media/HEBsq3fwU5R6w/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 0, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media1.giphy.com/media/OzJQu5BSqk2sM/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 400, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media1.giphy.com/media/OzJQu5BSqk2sM/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 400, "height": 200}, "tinygif": {
                                                                            "url": "https://media1.giphy.com/media/OzJQu5BSqk2sM/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 400, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media1.giphy.com/media/OzJQu5BSqk2sM/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 400, "height": 200}, "title": "",
                                                                         "source_id": "OzJQu5BSqk2sM",
                                                                         "preview": "https://media1.giphy.com/media/OzJQu5BSqk2sM/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 1, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media0.giphy.com/media/9GwMAnEOFlbUs/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 306, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media0.giphy.com/media/9GwMAnEOFlbUs/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 306, "height": 200}, "tinygif": {
                                                                            "url": "https://media0.giphy.com/media/9GwMAnEOFlbUs/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 306, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media0.giphy.com/media/9GwMAnEOFlbUs/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 306, "height": 200}, "title": "",
                                                                         "source_id": "9GwMAnEOFlbUs",
                                                                         "preview": "https://media0.giphy.com/media/9GwMAnEOFlbUs/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 2, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media0.giphy.com/media/4j5Snpwt6zGpy/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media0.giphy.com/media/4j5Snpwt6zGpy/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "tinygif": {
                                                                            "url": "https://media0.giphy.com/media/4j5Snpwt6zGpy/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media0.giphy.com/media/4j5Snpwt6zGpy/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "title": "",
                                                                         "source_id": "4j5Snpwt6zGpy",
                                                                         "preview": "https://media0.giphy.com/media/4j5Snpwt6zGpy/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 3, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media2.giphy.com/media/RqbkeCZGgipSo/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 261, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media2.giphy.com/media/RqbkeCZGgipSo/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 261, "height": 200}, "tinygif": {
                                                                            "url": "https://media2.giphy.com/media/RqbkeCZGgipSo/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 261, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media2.giphy.com/media/RqbkeCZGgipSo/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 261, "height": 200}, "title": "",
                                                                         "source_id": "RqbkeCZGgipSo",
                                                                         "preview": "https://media2.giphy.com/media/RqbkeCZGgipSo/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 4, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media3.giphy.com/media/vXeeHUPxgBtp6/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 284, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media3.giphy.com/media/vXeeHUPxgBtp6/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 284, "height": 200}, "tinygif": {
                                                                            "url": "https://media3.giphy.com/media/vXeeHUPxgBtp6/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 284, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media3.giphy.com/media/vXeeHUPxgBtp6/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 284, "height": 200}, "title": "",
                                                                         "source_id": "vXeeHUPxgBtp6",
                                                                         "preview": "https://media3.giphy.com/media/vXeeHUPxgBtp6/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 5, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media3.giphy.com/media/JDC5Q6RdyuSdO/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 356, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media3.giphy.com/media/JDC5Q6RdyuSdO/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 356, "height": 200}, "tinygif": {
                                                                            "url": "https://media3.giphy.com/media/JDC5Q6RdyuSdO/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 356, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media3.giphy.com/media/JDC5Q6RdyuSdO/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 356, "height": 200}, "title": "",
                                                                         "source_id": "JDC5Q6RdyuSdO",
                                                                         "preview": "https://media3.giphy.com/media/JDC5Q6RdyuSdO/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 6, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media0.giphy.com/media/d2Z7wetTpiqlmjq8/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 200, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media0.giphy.com/media/d2Z7wetTpiqlmjq8/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 200, "height": 200}, "tinygif": {
                                                                            "url": "https://media0.giphy.com/media/d2Z7wetTpiqlmjq8/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 200, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media0.giphy.com/media/d2Z7wetTpiqlmjq8/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 200, "height": 200}, "title": "",
                                                                         "source_id": "d2Z7wetTpiqlmjq8",
                                                                         "preview": "https://media0.giphy.com/media/d2Z7wetTpiqlmjq8/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 7, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media1.giphy.com/media/13pAkBEHHTkSgo/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media1.giphy.com/media/13pAkBEHHTkSgo/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "tinygif": {
                                                                            "url": "https://media1.giphy.com/media/13pAkBEHHTkSgo/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media1.giphy.com/media/13pAkBEHHTkSgo/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "title": "",
                                                                         "source_id": "13pAkBEHHTkSgo",
                                                                         "preview": "https://media1.giphy.com/media/13pAkBEHHTkSgo/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 8, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media0.giphy.com/media/Ps4qnGfj46w8w/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media0.giphy.com/media/Ps4qnGfj46w8w/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "tinygif": {
                                                                            "url": "https://media0.giphy.com/media/Ps4qnGfj46w8w/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media0.giphy.com/media/Ps4qnGfj46w8w/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "title": "",
                                                                         "source_id": "Ps4qnGfj46w8w",
                                                                         "preview": "https://media0.giphy.com/media/Ps4qnGfj46w8w/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 9, "tags": []},
                                                                        {"mp4": {
                                                                            "url": "https://media0.giphy.com/media/K7w37sbZqmsqQ/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200,
                                                                            "duration": -1.0}, "gif": {
                                                                            "url": "https://media0.giphy.com/media/K7w37sbZqmsqQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "tinygif": {
                                                                            "url": "https://media0.giphy.com/media/K7w37sbZqmsqQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "tiny_gif": {
                                                                            "url": "https://media0.giphy.com/media/K7w37sbZqmsqQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "width": 267, "height": 200}, "title": "",
                                                                         "source_id": "K7w37sbZqmsqQ",
                                                                         "preview": "https://media0.giphy.com/media/K7w37sbZqmsqQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                         "source": "giphy.com", "index": 10,
                                                                         "tags": []}, {"mp4": {
            "url": "https://media1.giphy.com/media/xy60clllaPMti/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 333, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media1.giphy.com/media/xy60clllaPMti/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 333, "height": 200}, "tinygif": {
            "url": "https://media1.giphy.com/media/xy60clllaPMti/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 333, "height": 200}, "tiny_gif": {
            "url": "https://media1.giphy.com/media/xy60clllaPMti/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 333, "height": 200}, "title": "", "source_id": "xy60clllaPMti",
                                                                                       "preview": "https://media1.giphy.com/media/xy60clllaPMti/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                       "source": "giphy.com",
                                                                                       "index": 11, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media0.giphy.com/media/lIytbm3T9siFW/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 394, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media0.giphy.com/media/lIytbm3T9siFW/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 394, "height": 200}, "tinygif": {
                "url": "https://media0.giphy.com/media/lIytbm3T9siFW/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 394, "height": 200}, "tiny_gif": {
                "url": "https://media0.giphy.com/media/lIytbm3T9siFW/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 394, "height": 200}, "title": "", "source_id": "lIytbm3T9siFW",
                                                                            "preview": "https://media0.giphy.com/media/lIytbm3T9siFW/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 12,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media3.giphy.com/media/aDhD39d2UZYsM/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 556, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media3.giphy.com/media/aDhD39d2UZYsM/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 556, "height": 200}, "tinygif": {
            "url": "https://media3.giphy.com/media/aDhD39d2UZYsM/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 556, "height": 200}, "tiny_gif": {
            "url": "https://media3.giphy.com/media/aDhD39d2UZYsM/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 556, "height": 200}, "title": "", "source_id": "aDhD39d2UZYsM",
                                                                                          "preview": "https://media3.giphy.com/media/aDhD39d2UZYsM/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 13, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media2.giphy.com/media/3o8doTrOWoQMV8h74k/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 265, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media2.giphy.com/media/3o8doTrOWoQMV8h74k/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 265, "height": 200}, "tinygif": {
                "url": "https://media2.giphy.com/media/3o8doTrOWoQMV8h74k/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 265, "height": 200}, "tiny_gif": {
                "url": "https://media2.giphy.com/media/3o8doTrOWoQMV8h74k/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 265, "height": 200}, "title": "", "source_id": "3o8doTrOWoQMV8h74k",
                                                                            "preview": "https://media2.giphy.com/media/3o8doTrOWoQMV8h74k/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 14,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media0.giphy.com/media/3o7Zeq71i5w0vOnAZy/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media0.giphy.com/media/3o7Zeq71i5w0vOnAZy/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "tinygif": {
            "url": "https://media0.giphy.com/media/3o7Zeq71i5w0vOnAZy/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "tiny_gif": {
            "url": "https://media0.giphy.com/media/3o7Zeq71i5w0vOnAZy/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "title": "", "source_id": "3o7Zeq71i5w0vOnAZy",
                                                                                          "preview": "https://media0.giphy.com/media/3o7Zeq71i5w0vOnAZy/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 15, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media2.giphy.com/media/oRlbEkkJtKGLS/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 343, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media2.giphy.com/media/oRlbEkkJtKGLS/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 343, "height": 200}, "tinygif": {
                "url": "https://media2.giphy.com/media/oRlbEkkJtKGLS/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 343, "height": 200}, "tiny_gif": {
                "url": "https://media2.giphy.com/media/oRlbEkkJtKGLS/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 343, "height": 200}, "title": "", "source_id": "oRlbEkkJtKGLS",
                                                                            "preview": "https://media2.giphy.com/media/oRlbEkkJtKGLS/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 16,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media2.giphy.com/media/WSYE5mSEyGP3G/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 266, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media2.giphy.com/media/WSYE5mSEyGP3G/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 266, "height": 200}, "tinygif": {
            "url": "https://media2.giphy.com/media/WSYE5mSEyGP3G/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 266, "height": 200}, "tiny_gif": {
            "url": "https://media2.giphy.com/media/WSYE5mSEyGP3G/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 266, "height": 200}, "title": "", "source_id": "WSYE5mSEyGP3G",
                                                                                          "preview": "https://media2.giphy.com/media/WSYE5mSEyGP3G/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 17, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media0.giphy.com/media/3oEjHBa34dVLv0jnoc/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 200, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media0.giphy.com/media/3oEjHBa34dVLv0jnoc/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 200, "height": 200}, "tinygif": {
                "url": "https://media0.giphy.com/media/3oEjHBa34dVLv0jnoc/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 200, "height": 200}, "tiny_gif": {
                "url": "https://media0.giphy.com/media/3oEjHBa34dVLv0jnoc/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 200, "height": 200}, "title": "", "source_id": "3oEjHBa34dVLv0jnoc",
                                                                            "preview": "https://media0.giphy.com/media/3oEjHBa34dVLv0jnoc/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 18,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media3.giphy.com/media/HhRGUdBJ5RVT2/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 355, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media3.giphy.com/media/HhRGUdBJ5RVT2/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 355, "height": 200}, "tinygif": {
            "url": "https://media3.giphy.com/media/HhRGUdBJ5RVT2/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 355, "height": 200}, "tiny_gif": {
            "url": "https://media3.giphy.com/media/HhRGUdBJ5RVT2/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 355, "height": 200}, "title": "", "source_id": "HhRGUdBJ5RVT2",
                                                                                          "preview": "https://media3.giphy.com/media/HhRGUdBJ5RVT2/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 19, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media3.giphy.com/media/3o7bu3wN9CbDWEzeGQ/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 300, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media3.giphy.com/media/3o7bu3wN9CbDWEzeGQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 300, "height": 200}, "tinygif": {
                "url": "https://media3.giphy.com/media/3o7bu3wN9CbDWEzeGQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 300, "height": 200}, "tiny_gif": {
                "url": "https://media3.giphy.com/media/3o7bu3wN9CbDWEzeGQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 300, "height": 200}, "title": "", "source_id": "3o7bu3wN9CbDWEzeGQ",
                                                                            "preview": "https://media3.giphy.com/media/3o7bu3wN9CbDWEzeGQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 20,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media0.giphy.com/media/fqtANo0OmU5Y4/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 267, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media0.giphy.com/media/fqtANo0OmU5Y4/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 267, "height": 200}, "tinygif": {
            "url": "https://media0.giphy.com/media/fqtANo0OmU5Y4/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 267, "height": 200}, "tiny_gif": {
            "url": "https://media0.giphy.com/media/fqtANo0OmU5Y4/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 267, "height": 200}, "title": "", "source_id": "fqtANo0OmU5Y4",
                                                                                          "preview": "https://media0.giphy.com/media/fqtANo0OmU5Y4/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 21, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media0.giphy.com/media/xUPJPlFxssGpmLemru/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 266, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media0.giphy.com/media/xUPJPlFxssGpmLemru/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 266, "height": 200}, "tinygif": {
                "url": "https://media0.giphy.com/media/xUPJPlFxssGpmLemru/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 266, "height": 200}, "tiny_gif": {
                "url": "https://media0.giphy.com/media/xUPJPlFxssGpmLemru/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 266, "height": 200}, "title": "", "source_id": "xUPJPlFxssGpmLemru",
                                                                            "preview": "https://media0.giphy.com/media/xUPJPlFxssGpmLemru/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 22,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media2.giphy.com/media/GrB9uThYsoU3C/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 267, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media2.giphy.com/media/GrB9uThYsoU3C/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 267, "height": 200}, "tinygif": {
            "url": "https://media2.giphy.com/media/GrB9uThYsoU3C/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 267, "height": 200}, "tiny_gif": {
            "url": "https://media2.giphy.com/media/GrB9uThYsoU3C/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 267, "height": 200}, "title": "", "source_id": "GrB9uThYsoU3C",
                                                                                          "preview": "https://media2.giphy.com/media/GrB9uThYsoU3C/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 23, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media0.giphy.com/media/dQCmKY4IgywFy/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 356, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media0.giphy.com/media/dQCmKY4IgywFy/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 356, "height": 200}, "tinygif": {
                "url": "https://media0.giphy.com/media/dQCmKY4IgywFy/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 356, "height": 200}, "tiny_gif": {
                "url": "https://media0.giphy.com/media/dQCmKY4IgywFy/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 356, "height": 200}, "title": "", "source_id": "dQCmKY4IgywFy",
                                                                            "preview": "https://media0.giphy.com/media/dQCmKY4IgywFy/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 24,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media1.giphy.com/media/l2JI6lmMX4WIO8waQ/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media1.giphy.com/media/l2JI6lmMX4WIO8waQ/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "tinygif": {
            "url": "https://media1.giphy.com/media/l2JI6lmMX4WIO8waQ/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "tiny_gif": {
            "url": "https://media1.giphy.com/media/l2JI6lmMX4WIO8waQ/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "title": "", "source_id": "l2JI6lmMX4WIO8waQ",
                                                                                          "preview": "https://media1.giphy.com/media/l2JI6lmMX4WIO8waQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 25, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media2.giphy.com/media/CfVkPSj1rSxVe/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 281, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media1.giphy.com/media/CfVkPSj1rSxVe/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 281, "height": 200}, "tinygif": {
                "url": "https://media1.giphy.com/media/CfVkPSj1rSxVe/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 281, "height": 200}, "tiny_gif": {
                "url": "https://media1.giphy.com/media/CfVkPSj1rSxVe/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 281, "height": 200}, "title": "", "source_id": "CfVkPSj1rSxVe",
                                                                            "preview": "https://media1.giphy.com/media/CfVkPSj1rSxVe/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 26,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media0.giphy.com/media/11K24SfwRuabuw/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media0.giphy.com/media/11K24SfwRuabuw/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "tinygif": {
            "url": "https://media0.giphy.com/media/11K24SfwRuabuw/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "tiny_gif": {
            "url": "https://media0.giphy.com/media/11K24SfwRuabuw/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "title": "", "source_id": "11K24SfwRuabuw",
                                                                                          "preview": "https://media0.giphy.com/media/11K24SfwRuabuw/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 27, "tags": []}, {
                                                                            "mp4": {
                                                                                "url": "https://media2.giphy.com/media/vQqeOtyIBn5MQ/200.mp4?cid=029136eb5b024b88485954552e79212c",
                                                                                "width": 267, "height": 200,
                                                                                "duration": -1.0}, "gif": {
                "url": "https://media2.giphy.com/media/vQqeOtyIBn5MQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 267, "height": 200}, "tinygif": {
                "url": "https://media2.giphy.com/media/vQqeOtyIBn5MQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 267, "height": 200}, "tiny_gif": {
                "url": "https://media2.giphy.com/media/vQqeOtyIBn5MQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                "width": 267, "height": 200}, "title": "", "source_id": "vQqeOtyIBn5MQ",
                                                                            "preview": "https://media2.giphy.com/media/vQqeOtyIBn5MQ/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                            "source": "giphy.com", "index": 28,
                                                                            "tags": []}, {"mp4": {
            "url": "https://media0.giphy.com/media/l2SpUc5nqKBG79Mti/200.mp4?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200, "duration": -1.0}, "gif": {
            "url": "https://media0.giphy.com/media/l2SpUc5nqKBG79Mti/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "tinygif": {
            "url": "https://media0.giphy.com/media/l2SpUc5nqKBG79Mti/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "tiny_gif": {
            "url": "https://media0.giphy.com/media/l2SpUc5nqKBG79Mti/200.gif?cid=029136eb5b024b88485954552e79212c",
            "width": 200, "height": 200}, "title": "", "source_id": "l2SpUc5nqKBG79Mti",
                                                                                          "preview": "https://media0.giphy.com/media/l2SpUc5nqKBG79Mti/200.gif?cid=029136eb5b024b88485954552e79212c",
                                                                                          "source": "giphy.com",
                                                                                          "index": 29, "tags": []}]}}'''

    print(data_clear(data))
