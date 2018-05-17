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
    data = '''{"errorCode":0,"errorMsg":"ok","data":{"stickers":[{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/01.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/01.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/756465f3-3a4c-45e8-9fcb-d4921e31b28d.webp","width":240,"height":240},"index":0,"id":"c2fd92e21dc2974c671996599ea82391","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/01.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/02.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/02.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/34af94eb-7879-4d46-aff1-d10df0013330.webp","width":240,"height":240},"index":1,"id":"45cb06f7413d39afd86184dadd9cbf5e","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/02.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/03.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/03.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/0b3dc78f-0a5f-4568-bfe9-baadbbae7d00.webp","width":240,"height":240},"index":2,"id":"ff9b197bba4cf8bc0267c42fad780315","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/03.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/04.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/04.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/4dc2d2f6-4625-4084-a2f7-6410702180ee.webp","width":240,"height":240},"index":3,"id":"2bfd783afc0c181accfd55860dd883f7","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/04.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/05.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/05.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/1cdd314e-ede9-4469-878c-44624ac4c642.webp","width":240,"height":240},"index":4,"id":"bd83688308940c46bf1d3bb79994384e","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/05.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/06.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/06.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/fef97508-9b5f-4466-aaf0-5f9c3fc06f40.webp","width":240,"height":240},"index":5,"id":"6ef639233db13f0c2254603640e27179","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/06.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/07.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/07.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/1dc7737d-bd3b-40fa-b590-eaee967e8e0c.webp","width":240,"height":240},"index":6,"id":"b9a323392da091a2123ea18aa555fcd0","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/07.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/08.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/08.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/9accbb61-bd1f-42ee-bd19-d9ed33e78c99.webp","width":240,"height":240},"index":7,"id":"95309615d3bb87e036d5eb0f3fd89e62","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/08.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/09.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/09.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/f9a2aa93-d314-4d6a-81df-21ec75907849.webp","width":240,"height":240},"index":8,"id":"ba96f4f19c3589d7f26edc4b1589671","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/09.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/10.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/10.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/d2102970-b5b3-446d-be98-aab6556d76b3.webp","width":240,"height":240},"index":9,"id":"cd4f370f9ba43569b68733bdff6adf4b","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/10.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/11.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/11.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/9b4d960d-0cf1-4554-aeff-f2e385677e26.webp","width":240,"height":240},"index":10,"id":"9cb6e834cc08fc10dd1c85c55c446911","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/11.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/12.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/12.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/e470cb8d-fdf3-474c-b562-5db0a0f17984.webp","width":240,"height":240},"index":11,"id":"1ad0a18c0b2f28b08b87fba29a0310d4","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/12.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/13.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/13.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/67d996ba-30f0-4a69-bbd4-4f8a63bdb7d5.webp","width":240,"height":240},"index":12,"id":"6ea7e8645f2bb87ed9f466103c933f90","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/13.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/14.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/14.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/93276596-2a6c-4f1a-acc7-9327d891edb8.webp","width":240,"height":240},"index":13,"id":"c2c55cfb14e1a25255b8c84af8fb0377","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/14.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/15.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/15.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/4610b984-3a37-4fed-b314-e4b546c723fe.webp","width":240,"height":240},"index":14,"id":"ef7e139f75f9b5e6743f64c3c0988108","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/15.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/16.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/16.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/70492d84-acc1-4ce0-afb0-64ab28d4a70d.webp","width":240,"height":240},"index":15,"id":"71eb8aac6694a0638448d880e8b92a40","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/16.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/17.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/17.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/598339a8-d409-4137-844a-c56e55346d58.webp","width":240,"height":240},"index":16,"id":"7dd12b4e084b7fe9931fdb9783eefaf3","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/17.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/18.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/18.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/d6085515-d060-4a7e-a182-fd521b09dc56.webp","width":240,"height":240},"index":17,"id":"af0fc3a85b7446941489e165bd7c501f","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/18.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/19.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/19.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/92c17e43-7611-4b0d-9958-e5ea93848c9b.webp","width":240,"height":240},"index":18,"id":"952ec7d20e68fad98dcee11830f27f7e","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/19.png","tags":[]},{"small":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/20.png","width":240,"height":240},"large":{"url":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/20.png","width":240,"height":240},"webp":{"url":"http://cdn.kikakeyboard.com/backend-picture/6f4d6e00-8349-48e1-a079-3b65833047fe.webp","width":240,"height":240},"index":19,"id":"8bbb47a6da16b321b3ac469ec119cfd7","source":"kikatech.com","preview":"http://cdn.kikakeyboard.com/sticker_partnerLoveFace/20.png","tags":[]}]}}'''
    print(data_clear(data))
