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
    data = '''{"errorCode":0,"errorMsg":"ok","data":{"key":"1","name":"Kmoji","icon":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/icon_small.png","icon_big":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/icon_big.png","column_count":4,"stickers":[{"key":"ef829d0cf939185ac82e59c4f629a6dd","name":"Despise","tags":["Despise"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/01.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"d5bdad5ba2c345022a8dddd06515c73","name":"Unhappy","tags":["Unhappy","Feeling Sad"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/02.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"ea6d643677615db1cd2c112260be370b","name":"Sigh","tags":["Sigh"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/03.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"1b9d656500c0b80d15ef2a0f9d2be394","name":"F*ck","tags":["F*ck","Fuck","Middle Finger"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/04.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"931f00be426795fd82cb195d58493bb2","name":"Worried","tags":["Worried","Nervous"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/05.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"52e4e746a9135590878c0c15f932ac90","name":"Look Forward To","tags":["Look Forward To","Expected"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/06.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"e31800d3f8a36dc4535a72537d213071","name":"Happy","tags":["Happy","Smile","Ultra Happy - Heart Eyes","1F600"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/07.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"d82dcaaedf8dbced6ce6537b1df35c0a","name":"Nervous","tags":["Nervous","Sweating","1F613"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/08.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"ebb3e526ab1fd853307f3ec551220a1","name":"My Eyes!","tags":["My Eyes!","Lol"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/09.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"4354477a16a7391c3d9bfdefdac38cf8","name":"Appalled","tags":["Appalled","Disgust","1F61D"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/10.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"f31979d24a0c0afd7081b59d68c0c520","name":"Shy","tags":["Shy"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/11.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"6cbbc9ea30530dad7fe5dced6579d156","name":"Lol","tags":["Lol","LOL","Laugh","1F604"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/12.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"1dd6be388e3c7600806b8ba58c45c951","name":"Love","tags":["Love","Love You","Iloveyou","Love You Too","1F60D"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/13.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"b57add84bdc7ee90ed047460d4586612","name":"Smile","tags":["Smile","Smiley"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/14.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"34d6d3cb70089e607af550d9cc1b2008","name":"F*ck","tags":["F*ck","Fuck","Fvck","Middle Finger"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/15.png","width":458,"height":270},"mp4":null,"scale_type":0},{"key":"acd766e17648992a38140f8c641f543e","name":"Love","tags":["Love","Hearteyes","Ultra Happy - Heart Eyes","1F60D"],"type":1,"image":{"url":"http://cdn.kikakeyboard.com/sticker_partnerKMOJI3/16.png","width":458,"height":270},"mp4":null,"scale_type":0}],"author":{"key":"","name":"","avatar":""},"description":""}}'''
    print(data_clear(data))
