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
    data = '''{"errorCode":0,"errorMsg":"ok","data":{"tagList":[{"id":0,"key":"trending","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#trending"},{"id":1,"key":"crazy","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#crazy"},{"id":2,"key":"sassy","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#sassy"},{"id":3,"key":"sorry","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#sorry"},{"id":4,"key":"happy","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#happy"},{"id":5,"key":"kiss","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#kiss"},{"id":6,"key":"no","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#no"},{"id":7,"key":"hello","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#hello"},{"id":8,"key":"sleepy","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#sleepy"},{"id":9,"key":"cuddle","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#cuddle"},{"id":10,"key":"angry","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#angry"},{"id":11,"key":"party","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#party"},{"id":12,"key":"wink","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#wink"},{"id":13,"key":"bye","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#bye"},{"id":14,"key":"yes","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#yes"},{"id":15,"key":"relaxed","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#relaxed"},{"id":16,"key":"panda","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#panda"},{"id":17,"key":"love","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#love"},{"id":18,"key":"lol","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#lol"},{"id":19,"key":"sad","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#sad"},{"id":20,"key":"excited","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#excited"},{"id":21,"key":"scared","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#scared"},{"id":22,"key":"shocked","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#shocked"},{"id":23,"key":"tired","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#tired"},{"id":24,"key":"drunk","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#drunk"},{"id":25,"key":"hungry","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#hungry"},{"id":26,"key":"bored","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#bored"},{"id":27,"key":"surprised","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#surprised"},{"id":28,"key":"frustrated","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#frustrated"},{"id":29,"key":"sick","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#sick"},{"id":30,"key":"nervous","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#nervous"},{"id":31,"key":"relaxed","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#relaxed"},{"id":32,"key":"inspired","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#inspired"},{"id":33,"key":"disappointed","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#disappointed"},{"id":34,"key":"beauty","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#beauty"},{"id":35,"key":"dancing","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#dancing"},{"id":36,"key":"win","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#win"},{"id":37,"key":"laughing","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#laughing"},{"id":38,"key":"crying","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#crying"},{"id":39,"key":"dreaming","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#dreaming"},{"id":40,"key":"smiling","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#smiling"},{"id":41,"key":"eating","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#eating"},{"id":42,"key":"funny","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#funny"},{"id":43,"key":"cute","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#cute"},{"id":44,"key":"hot","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#hot"},{"id":45,"key":"pretty","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#pretty"},{"id":46,"key":"dark","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#dark"},{"id":47,"key":"confused","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#confused"},{"id":48,"key":"please","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#please"},{"id":49,"key":"unimpressed","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#unimpressed"},{"id":50,"key":"lonely","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#lonely"},{"id":51,"key":"rainbow","path":"http://api.tenor.co/v1/search?tag=sorry","image":"http://media.tenor.co/images/f8fbfe0c2460cb851616b4d91ca0fb5e/tenor.gif","name":"#rainbow"}]}}'''
    print(data_clear(data))
