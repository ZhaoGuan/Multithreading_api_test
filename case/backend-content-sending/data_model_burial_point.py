# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import binascii
import hashlib
import random
import requests
import json
import time
import yaml
import os
import sys, getopt

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + '/../../')
from base_function.golable_function import source_input


def config_reader(Yaml_file):
    yf = open(Yaml_file)
    yx = yaml.load(yf)
    yf.close()
    return yx


# popup分组计算
def sum_duid(duid):
    sum_result = 0
    a_ = []
    for i in duid:
        # print(i)
        d = int(i, 16)
        # print(d)
        a_.append(d)
        sum_result += int(d)
        # print(sum_result)
    return sum_result


def which_group(duid, way):
    duid_value = sum_duid(duid)
    group = duid_value % way
    # print('取模结果：')
    # print(group)
    return group


# 随机udid值
def random_duid():
    all_world = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    world = random.sample(all_world, 5)
    result_world = ''
    for i in world:
        result_world += i
    m = hashlib.md5()
    m.update(result_world.encode('utf-8'))
    MD5 = m.hexdigest()
    # print(MD5)
    return MD5


# 根据udid获取sign
def get_sign(app, version, duid):
    if app == None or version == None or duid == None:
        sign = False
    else:
        if 'pro' == app:
            app_key = '4e5ab3a6d2140457e0423a28a094b1fd'
            security_key = '58d71c3fd1b5b17db9e0be0acc1b8048'
            # package_name =

        elif 'ikey' == app:
            app_key = 'e2934742f9d3b8ef2b59806a041ab389'
            security_key = '2c7cd6555d6486c2844afa0870aac5d6'
            # package_name =
        else:
            app_key = '78472ddd7528bcacc15725a16aeec190'
            security_key = '6f43e445f47073c4272603990e9adf54'
            # package_name =
        base = 'app_key' + app_key + 'app_version' + str(version) + 'duid' + str(duid)
        m = hashlib.md5()
        m.update(base.encode('utf-8'))
        sign = m.hexdigest()
    # print(sign)
    return sign


# 设定header
def set_header(duid, lang='en_AU', app='kika', version=2043, way='online'):
    lange_config = config_reader(PATH + '/../../config/lange')
    use_lang = lange_config[lang]
    # print('@@@@@@@@')
    # print(use_lang)
    if 'pro' == app:
        app_key = '4e5ab3a6d2140457e0423a28a094b1fd'
        security_key = '58d71c3fd1b5b17db9e0be0acc1b8048'
        # 这个错误的
        package_name = 'com.emoji.coolkeyboard'

    elif 'ikey' == app:
        app_key = 'e2934742f9d3b8ef2b59806a041ab389'
        security_key = '2c7cd6555d6486c2844afa0870aac5d6'
        # 这个错误的
        package_name = 'com.emoji.ikeyboard'
    else:
        app_key = '78472ddd7528bcacc15725a16aeec190'
        security_key = '6f43e445f47073c4272603990e9adf54'
        package_name = 'com.qisiemoji.inputmethod'
    if way == 'online':
        # 线上
        # User-Agent package_name/app_version (udif/app_key)
        header = {'Accept-Charset': 'UTF-8',
                  'Kika-Install-Time': '1505198889124',
                  'Connection': 'Keep-Alive',
                  # 'Host': 'api.kikakeyboard.com',
                  'Accept-Language': '%s' % use_lang[0],
                  'User-Agent': '%s/%s (%s/%s) Country/%s Language/%s System/android Version/23 Screen/480' % (
                      package_name, version, duid, app_key, use_lang[1], use_lang[2]),
                  'X-Model': 'D6603',
                  'Accept-Encoding': 'gzip'
                  }
        # header = {
        #     'User-Agent': '%s/%s (%s/%s) Country/%s Language/%s System/android Version/23 Screen/480' % (
        #         package_name, version, duid, app_key, use_lang[1], use_lang[2])}
    else:
        # 测试
        header = {
            # {'Accept-Charset': 'UTF-8',
            'Kika-Install-Time': '1505198889124',
            'Connection': 'Keep-Alive',
            # 'Host': 'api-dev.kikakeyboard.com',
            'Accept-Language': '%s' % use_lang[0],
            'User-Agent': '%s/%s (%s/%s) Country/%s Language/%s System/android Version/23 Screen/480' % (
                package_name, version, duid, app_key, use_lang[1], use_lang[2]),
            'X-Model': 'D6603',
            'Accept-Encoding': 'gzip'}

    return header


# 获取分组duid
def set_group_get_duid(way, which):
    while True:
        duid = random_duid()
        group = which_group(duid, way)
        if group == which:
            print('希望的duid:')
            print(duid)
            break
    return duid


# popup
def popup(tag, duid, lang='en_AU', app='kika', version=2043, way='online'):
    print(duid)
    header = set_header(duid, app=app, version=version, lang=lang, way=way)
    print(header)
    sign = get_sign(app, version, duid)
    if way == 'online':
        # 线上
        url = 'https://api.kikakeyboard.com/v1/stickers2/popup?tag=%s&kb_lang=%s&sign=%s' % (
            tag, lang, sign)
    # 测试
    elif way == 'test':
        # web0
        # url = 'http://sticker.pre.kikakeyboard.com/backend-content-sending/popup?kb_lang=%s&tag=%s&sign=%s' % (
        #     lang, tag, sign)
        url = 'http://34.214.222.244:9090/backend-content-sending/popup?tag=%s&kb_lang=%s&sign=%s&type=0' % (
            tag, lang, sign)
    else:
        url = 'http://172.31.23.134:9090/backend-content-sending/popup?tag=%s&kb_lang=%s&sign=%s&type=0' % (
            tag, lang, sign)
    print(url)
    response = requests.request('get', url, headers=header)
    print('输出')
    print(response.headers)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        assert False == True, 'popup接口有误'
    if json.loads(response.text)['errorCode'] != 0:
        assert False == True, 'popup接口有误'
    print(json.loads(response.text))
    return response.text
    # return response.headers


def molde4():
    duid_list = []
    modulo_four_zero = []
    with open('./pt_duid') as f:
        for duid in f:
            duid_list.append(duid.replace('\n', ''))
    for duid in duid_list:
        if which_group(duid, 4) != 3:
            # if which_group(duid, 8) == 0:
            # if which_group(duid, 16) == 0:
            modulo_four_zero.append(duid)
    print(modulo_four_zero)
    return modulo_four_zero


def run(source):
    app = ['kika', 'ikey', 'pro']
    lang = ['en_US', 'en_AU', 'es_AR', 'pt_BR', 'in_ID']
    gs = ['5a215835df204115ee3d2d4ec0c528aa', 'adad79631d9339915e3be1c9e783e82d', 'a2bb5434f3541bf5aa64186ec8c2b77f',
          '920b56e9cadd743bfbbcb4126937e789']
    pt_duid = ['c55f64b78df14008adbaeff615e35c4c', '50a4ecbbb8474a1cbd7737a029e155ac',
               'cc8a440f70aa44779559627be07ff59f',
               'd91ea26a9b6d4e8885cb2acace4c30a1', '7b3dc5a04dd0469abc8bde1764160899',
               '8224c2c0c5aa442f99586a57cd35133d',
               'c782bb7a9f524a568cfd81d6666e417c', '4ff328c8b4d7445facd8d9532116205c',
               'beca0c0ed31e4552b791dd5f2136e903',
               '215c3a6f41c84d0a817ad69f2a4bc495', '06d6333e6e6a492883bb30ddff775d81',
               '70a2997ed6a0483a86df23ba7b99d07c',
               '82b5a6c28475925607e397a998a3374b', 'dcde17e6275947ce99ac3f47b19a326d',
               'd8383ac9fd7444b281f049b15ca1e276',
               '19ce03fa4f464e2f836a5d7a345297ee', 'a24883f83e944299bdc6d38d923076ac',
               '8c0ee25aa3382c8e9ac7530495eaeec3',
               '81f7ea63fae38de326937b0b7ea895bf', '68445cd1869e46a0ad4a6e25e9198603',
               '0dadbf8949554ffd954a981a40c3b724',
               '2ee7fe857ee540838b87a946c0953158', '652db7139b204b8db1c49f059242db93',
               '86936561d6e64bc9b3431558dd5691e4',
               '5f2686bcfe914b6a8eb4dd282c5ed17a', 'cc0e2b3a5a434968ba655da5594d525b',
               '0c744ea5f75b46f58d4abea791df8188',
               '30981c13d3534020bd8645644201b08a', 'a55f136291d74b73843887a8812f97f1',
               '6196ee370d2f474ba779462e8540f216',
               '84451f451dc44685bb1aeb47fab9c151', '965a39c29ab2477f9c3c512696b022ad',
               '09c9c7739eee4b2f8da7ab36d8b214da',
               '8e57a2d1970949bba90c3ab35f14f63d', 'dbbde590248c4651b5f05b3d660c5411',
               'cea99385e252418a9d534ed26cf4f386',
               '3cfc950bd565419ab731c9ecca138fa0', 'd66f594226dd427bac13c67a8a5aee71',
               '38acff2aba14464ab44ac840b9b032b7',
               'e742947f1f614ebd894e1a58f42ea368', 'f7dbd671bbf7455f9c99f1e37c83c327',
               'b67063377b004dd0a8dc90e31dc6b768',
               'c96c34c1eaa548c88513808feda26935', '51e9638cc420400cae83d00071768007',
               '555ebb7c3bc34a449d2293b712c3b3a5',
               '89659bfd34d04e0eab140984c213dd85', '49674aea545841b1a015ccc7eff6ae66',
               'a8a8feaa2c6e4ab2b94c53caa49150da',
               'b50a0cd9d6b4446bb3073bf7138a2161', 'a53d0916c5434aaab61f27bd2901c74a',
               '5d11e386e5784d1581b64ce0c77203ef',
               'ea6a2a9e8d984a5489f35abd5e6ca7cc', '4c470e6fba4a4da8800304cd96083190',
               '5df7aa33e70b4d1698e1706dc2419f3e']
    en_duid = ['6937bca96d48484bb1810d45c59004c0', 'df52e3169dd84a8caa981511f642389a',
               'f0407d4c69dd7fbf8daac40ae50c2aee', 'ddcb60542e5546c0b6f41a0795c869cf',
               'aebb5a4c9a3eecd9249ecf8ec3664e51', '598af9a35e774da789c2e14d4ada0037',
               '782ce59ba74c4140868adaac90c28fcf', 'a31adf67fbb54a91adfcb16f4f906ba9',
               '005657fc1f0d47d897b8a7caf341ab36', '2121bb1d9a944451a073660426516954',
               '4f1924e1f3564708a999c8015398bb0b', '687eef6fc3d5432da788d9a5508876e6',
               'e68ebe030f50400486d1f63224f5074b', '7e23cc44660c4a6b996d1f2bd002447c',
               '43caa3dacd204c5581aac5120cef60b8', '9f739ffedd754a54aee666a3f010e95d',
               '8d9ee07e6e99484cbc6e4f2011963c78', 'fbebddc6215e4e72bf68843cd3bf2ce0',
               'c122eaeec2c9093a8b0d1373f713d3f8', '09361675440345d8b7e5368e8151b041',
               'a6b08547722b44699785687c20c00225', '2d0f154d063d494e86dedb81f09baed9',
               '3a60cafa877f40a387e9dde0642a1c16', '1cbf7128f37f41ee93f37de5e8de9345',
               '9e13e989de83465d891957f0b7fa0ef5', '734a4e8e02551a7b1eea534e91575c63',
               '8944d2c8604a47618cd86b9d25d2f968', '28ed46ce2310471a80fbc813e8a029b5',
               '5e92812451bffe374cb5ae6e443683fe', '9b1cd18ebece47ae8c5ecfbf36585f5a',
               'ae552aba6bcc4c228a2024c43793359b', '84edca3bc99e480ab5a50b5c89d21f44']
    kika_en_duid = ['6ae42a8ae1614f639dd62d772afa0b80', 'd8fb7bef2e374d249e59216c2980fc67',
                    '1a87325ae12941399edc8347dcdf4aa4', 'b44e76a3daf04c8e8746660d9efea10c',
                    '39a1a5f6ec2a4c02b39e45e77147e73f', '70b9140d-58f9-4f7a-ac4d-8e5cbd1eecf0',
                    'd0169f8f0d85408ab16118cf19859fad', '2178065e8c8e4b48ac7ea6b43b31e63d',
                    '1aa4404c34794d199eab4967813e33da', '5b16eec04b734d09b82086e4eb5ab8e0',
                    'b64db6a151634e2a9e082d7618f62589', '84055c36-b2e2-47fb-90d7-c734f24a7ec7',
                    '7bdcafe4c8ef4784b9c0f9e5dc72aa85', '3469c41adae04c2dabdada8058301218',
                    '58010cc3b1984612955aa64d0cf4253e', '0a4bb08bcdbe4be0a3ea57bf59009a99',
                    '8d903d5bed4d4afcb1e0690e8c77171f', '9d6da10862934ab88d18fe2cecc55132',
                    'fa7dfd551a5a4d689374739de3972217', '2b6758c3bb02460f8d76a6382dfb6bf3',
                    '2587aacb183b4e67942558af4a2f6998', '8355902bf96cfd3544d97d97baf3b5d5',
                    '7c5ff79990a240bf8ac25aec895b5a36', '1437bcacb7a84fb3a2d7431167997e8a',
                    'dbab49c1c16f4373afa2b5613b2089fa', '13893e51ef724d9c80f64ced2b2f8253',
                    '465807d5-ddbe-41aa-8f10-95e87d6dbb92', '4f16a00d7c4a4109b983b06f6fccbe38',
                    'c848f9289eaf42bc96146ddb3cea7f49', '4f16a00d7c4a4109b983b06f6fccbe38',
                    '5a0bacd16c5a43bd8616427569caafb2', '42077538a4a744a0aa06e4497456be29',
                    '3817290a587d445da498b0fbcb72344a', '3817290a587d445da498b0fbcb72344a',
                    '39f08f68808185e094bac791b144bb07', 'f59f1be30fe84c37a46360c580de363b',
                    'f59f1be30fe84c37a46360c580de363b', 'dc621c2c13e242d2ba0e8beb6a58c33d',
                    '15cb6904-7256-4779-9308-bf94818fdadc', '221e303c6a2040ff997ab5df0c8a362b',
                    'b1ef5a08e0704a9a9a43f6e20fbb181c', '97b82f9df09c4ab5bf3825a1f408bb97',
                    '5b2a27241d1341b596e41376df72e1a6', '7e52cc01f7c04e7ab3d1c1d187a6c893',
                    'c65b79dc15a64735b17f2968ff3136bb', '13893e51ef724d9c80f64ced2b2f8253',
                    '546f4e66f2144d558e7d1f36d2197e8a', '019cc11b1e654756aeccec4b28509732',
                    '6c6db651783841f9b75f233f0561c91a', '128910b7e74647129e492a8fb9dfe7f1',
                    'e83cad9dc0454bfcbcba16b625eadb1b', 'e83cad9dc0454bfcbcba16b625eadb1b',
                    'b89e0bd4af6940e19a11f246c4d70d68', 'f8302234f04b450f83dd35bb76e77849',
                    '69d24cb0cee54b26993987ce00f3afd8', 'bb1a808aaa744e8982400466267a3d31',
                    'bd865e20ce1c44dca56a77d712fd0841', 'eae4a626-8d94-4026-b815-fac44219f730',
                    'ff2ac7c0d0104b61874b111cbb00e9d8', '004f2ba81bd045649526d8acd9a800f6',
                    '004f2ba81bd045649526d8acd9a800f6', '7c5ff79990a240bf8ac25aec895b5a36',
                    '974d3cd70f71450e8baf9e204a04c78c', '382b7c9d-1a38-43f1-ab98-9e9e1ba614b3',
                    '96cf6f3bc966474eaea8a0f06a509da1', 'bcd2139f7c5046a992dc181fe514697e',
                    'ea99bf47-704e-46f5-903f-80f4cacb530f', 'e6ff0cde13864dceb64b40b9fe2b0426',
                    '118528544468448183b6d43305fc3d35', 'cddf4236c7da4d6980349dc0637f3753',
                    '4dd44435f4034113b6a942a022899bdd', 'f78c1b6c2a2b446992494b35f8f10608',
                    '0f9684de06c24f028385e25c0c6347e7', '39018821823244d0915165d85d1235f0',
                    '39018821823244d0915165d85d1235f0', 'd0ec2be6d1cc4d468ce4447e2e84f8dc',
                    '2f97f97a3b7e4b94a91b2b8289a1650a', '0ed4d6d8ea2549dea5734f15ff89e75f',
                    '102e6317c2d041f8a69a2474b655a994', '30e6ea13e5d44969af3e5ee3f80124b6',
                    '9d339d1ec55e462d9fbe7c2fedfd4cc6', '15cb6904-7256-4779-9308-bf94818fdadc',
                    'c8262cbbaea749a39617d36f62cc3cbb', 'c9fb1c5e690142d9ae94ccc72773d76c',
                    'c9fb1c5e690142d9ae94ccc72773d76c', '5b6c6a1a0a4bca75ed619d593a7ddbb2',
                    '20b8d099afea45568e2c6dcc532c9cb6', '479df0d3172f432ba9605c1b2a691054',
                    '6436552650b24d3a987d25d6ca7779b9', 'f8442932ebd544cab5314b1aa9a3043f',
                    '798c7f5878b345e7a60bee3c56a1201f', '39bda473-b362-484b-8d74-e08503fcb7c5',
                    'f7cc8d0b9cfe4d19ae1e9c7187d313d9', 'cd448a85be4c4a6fbc0cc0d87daef076',
                    'feecfcd64a9242218364756df2ad60cf', 'b94297f65cae4e139ad1699fe06774db',
                    '89cc2b4552ee4b178fc8e8e0df315a67', 'a164c62548fe4c92a594072b2907b513',
                    'a164c62548fe4c92a594072b2907b513', '26f677d5-bd41-4ac2-a32d-79f98cb4c40d',
                    '0e023dfa689c4c40a4d3eb58ea1aa3a2', '9d339d1ec55e462d9fbe7c2fedfd4cc6',
                    '2662880ab1f59aa7c02ec9e565ecd8db', '54aa9ef8d74c4bc5a58575c8a7f7d87a',
                    '3c8bb373352d4f1b984f346fd28fcee6', '1c21648ce95d4aedaa76a4ce2232b5d1',
                    'b7eed09830cf4952a0f596b0bc0043fd', 'ced9a60dcbc44092966bc9e0caf62980',
                    '24530122184045e18d31f17e8d6948b3', 'c00d2982ef4c43588bd53c66342d9ee6',
                    '26a2363784054bc4bcc95a39f7f55bae', '509b592d36a94881b25f32480f1ad67f',
                    '26a2363784054bc4bcc95a39f7f55bae', '290089b230344e859dc88f20e2e56280',
                    '5f27997372254324b006bd7ccdedb218', '72dcac016a2d47a3880220dde8020bde',
                    '419e5a9d9e494c1dae6fdc01a4df869d', 'f3d28b5fec7c4d30b9ef10588a273145',
                    '0e023dfa689c4c40a4d3eb58ea1aa3a2', '1328facd9ff04327abb60a00229cacfb',
                    '236a450f-129c-4b18-8aa6-25450d0809b3', '2e0c57e6e08e4aa18db38b8038002f36',
                    '036f812e9f2a4053bf1bf20edb159582', '036f812e9f2a4053bf1bf20edb159582',
                    'bfa875af6a7643fb9269ac7beb8d139c', '0c29fe899ab04cf687e2b0659899ae1b',
                    '0c29fe899ab04cf687e2b0659899ae1b', 'b50b749cc3894255af58c4f0c99d0e61',
                    'a399bceba57d4a5e91c7674c2bae0a71', 'd69471a5049d45e680e9ceee99164ccc',
                    '3668a2ec747d4795b466f1363d8c1bf8', 'd0b25479981941cc9d2c818ec5ab429d',
                    'bdce4450616741d793b979278941d4b5', '8b6915a27cb34927b29f922abe87eeaf',
                    'c7bf0539-93ca-46d7-ab00-815b69f747c5', 'db0b55c7f26549c6bb903ec8b6861782',
                    '8d903d5bed4d4afcb1e0690e8c77171f', '81d02fbbb1ad4bd6aee13a56283c0ba1',
                    'df39b3b1d8aa4e229524d8f98cc21db7', '47a06486db10401a89a55c73188eb31a',
                    '2a5515ca-e689-4b05-95b0-51f934cc15a8', 'c35db3222bf64c479a9c1dfeb4026f16',
                    'c35db3222bf64c479a9c1dfeb4026f16', '8ff4151d822a4aa0b1fa482056494e4f',
                    'd804c0a15d18493cb450a05a746f0d61', '0d3adb3688594d1d9757d2f8660ab27c',
                    '8c11db86cbf84da99c656b1ade8f5b93', 'e481837b2d9f442c80817fd4a6befec5',
                    '2a96ac68a8b1428fa24da87b650edd02', '13cdc8f4622946d9a931696f23359695',
                    '13cdc8f4622946d9a931696f23359695', '4c5265683ad846a699dd6baec655b8c8',
                    '942fd37992fa404994af33dad9fb097e', '26158fe522b245ab9abd3538c16aa6a0',
                    '0f9684de06c24f028385e25c0c6347e7', '3f56fdddd7d6490897b0a0bfd47f97e5',
                    'cf230a21d1ca4f00a6aaa3de52e4431b', 'cf230a21d1ca4f00a6aaa3de52e4431b',
                    'd7e19233ac3a4e1cadb9e0f235a78519', '30b3ab049abb4fd08e80b3b980c88b59',
                    'c848f9289eaf42bc96146ddb3cea7f49', '4ba3cf30c21f47778739acecdae20fd5',
                    'd761bdbc5ca84a99a4af32088361584c', 'cca8d629f7c04c04966b33065684c762',
                    'cdb9ebcd2c984ecc9fae5a976150ac9a', '0c202f5b32694b24a72fff98fedc20a5',
                    '171af96975484b2688a769600140ea0c', '3c8bb373352d4f1b984f346fd28fcee6',
                    'a5e8b38ad6f949d19d421d6545916111', '78896f55-a4b2-498e-a420-386b0af579b8',
                    '61523f99d3db5d03492e00d0fac9dd3c', '61523f99d3db5d03492e00d0fac9dd3c',
                    '2b6758c3bb02460f8d76a6382dfb6bf3', 'da1789941b754742addde4fdb4d3f22d',
                    'e7f459445b51488c85b1ecc9a84c1caf', 'fa8b0d09b2be43aa86ff47c0d4460447',
                    'e846d73179014f6f8bd507b44064a3c9', 'a48e0ccae02742f2a9fb7628ca2bcbb7',
                    '1395b9f3151f45d88214ec5da72e9335', 'cd448a85be4c4a6fbc0cc0d87daef076',
                    'd55d9c9d41134092bb30c297afea639f', '33f87741df162c30780882d72284ebce',
                    'c848f9289eaf42bc96146ddb3cea7f49', 'be95cdbac57649268677a85d390372c4',
                    '75cc13685ecd40079b53d4e96859fe51', 'b50b749cc3894255af58c4f0c99d0e61',
                    'f5b2aeb9bef5450da818fcd29c472706', 'ef73ea5e3d2640b4aa43296f984b5b26',
                    '47575784401740cd8f5778f28e95827c', 'd6f47d83aa134fcfbdabe260611ba8f2',
                    '6755ab18-5010-46ef-82fd-a9ccc92f8c9a', '047d2cf2-fd0f-443a-9305-5213ae51bb9e',
                    '21c36bfbb0344dcc96bb7c1f168a6c14', 'f8442932ebd544cab5314b1aa9a3043f',
                    '18f7ae6eceaf4921a81492c30ea76ed5', '875e543c89a141fb85213e8f5b7ee02e',
                    '875e543c89a141fb85213e8f5b7ee02e', 'e3037aec-7e63-4f60-99ac-e7283e2b4bc2',
                    '41e1facbc5da419b8bf08faf0a9d93e7', '06b21df6f80b4e87a50818edf3d2a719',
                    '2a5a211a-c82e-434f-a1cc-aca554f26b06', '2a96ac68a8b1428fa24da87b650edd02',
                    'd031cf1e044f4787aa69744cb16500cf', '7adfc661bd324726a8c540ef8daa5da5',
                    'cdabbdade79e435fbd2b5dc87d2f3f06', '252efe46a5f24651af44ffc11cdbf110',
                    'a164c62548fe4c92a594072b2907b513', 'a164c62548fe4c92a594072b2907b513',
                    'b3faf925302a4fe5b8db6d5c2da64d0a', '4fe3143928ae449e82416c9141795436',
                    '2a5a211a-c82e-434f-a1cc-aca554f26b06', 'b9b10a45b6f24852ac8485d64c9d71ae',
                    '192c1346429c4103963a6a4c198b5a03', 'baf22db5b3b6447c90575ceffd46fdaa',
                    '23a8304212fb4daea70c66b0e806a2dd', 'ee9eaeb31fcf4e759d6fdbd6fd5827d9',
                    'cbb50aa7ed77414881ec927bb6b2235c', 'cbb50aa7ed77414881ec927bb6b2235c',
                    '1c55f8d26118435aabd6c726d78022d9', '07087911a5554ea889a08c3b9ec222cc',
                    'f529d7d3e6294ebcbf9a4cefb3354997', '3c8bb373352d4f1b984f346fd28fcee6',
                    '1f236eeef7ce45b0b4b4a3894a67c4d7', '2a5a211a-c82e-434f-a1cc-aca554f26b06',
                    '93b7b34c5f53492cb1b6622ba4b4ead9', '09982f6d2b62417db110c0b35eae46b9',
                    'fa722f15295740a89dacaf7cc0e2bae7', '2587aacb183b4e67942558af4a2f6998',
                    'd48b7b20cc0d43269c4125b6521f5cbb', '13893e51ef724d9c80f64ced2b2f8253',
                    '7a503bd3791b4cfba866b177567254d0', 'ce64e26c7a44454384791427eae45938',
                    '2a5a211a-c82e-434f-a1cc-aca554f26b06', '23a8304212fb4daea70c66b0e806a2dd',
                    '035da41db1294964958f12463140259b', '4bf630f860ae4e3fbad4f02a9f63f4b4',
                    '3171b9ec8f7c449eb2fd5ac70d25d696', '7b3ad4a055e543dc90c41728d270e011',
                    '32f73e1c-d292-4f13-89e7-d027c484ae94', '5df9e529ea80461cb3d59c22e9873b04',
                    '2a5a211a-c82e-434f-a1cc-aca554f26b06', '3d7aeee4a61c4c5e862dddf10456c81a',
                    '2a256810a0cb43a09d0bc274587f7cbd', '9fa6b65f12434c93894c0300d87dea04',
                    'df39b3b1d8aa4e229524d8f98cc21db7', '13893e51ef724d9c80f64ced2b2f8253',
                    '2a5a211a-c82e-434f-a1cc-aca554f26b06', 'c4bf3fd0ad654255b6c92a997f645480',
                    '770ed396934943309e28d172e530099a', '72defab07d7549d98f1ebda574b34546',
                    '66b12629687f4e2ba22ce72da9ae264d', '2a5a211a-c82e-434f-a1cc-aca554f26b06',
                    '7d3456a244df44e3a4db207860d3c25d', '54579f09b16d4f0bb8dd8df592a9285e',
                    'ab84e024-a6ea-4d57-bbfb-6e6e4945b9b4', '85694056f3864750b2c268005d7de097',
                    '4dd25b45-1d1e-4a87-8e34-0a6e2376a1ce', 'a7c9b78249f64594b1ad20b8f87c6167',
                    'a7c9b78249f64594b1ad20b8f87c6167', '137aba478ac345b4986ae212cc0e4277',
                    '9539771123504b6ab4eb018a68c23313', '26535acfd1ea41dba3934de27f16dcf8',
                    'd08dd40208c0414fb51508955d4ad743', '6f9810307e1a4b9ba01bc391e547b689',
                    '319b1f68d14e45eea24006275d428365', '63c7755ce1a646f88c30542964405ee9',
                    '335990fcd7e1428bbccb82e17cd53814', '91240cb302994e6bb8b235b1e6ba24ae',
                    'a24c15a6b653444bad95da3e6d28fc09', '789e3ea92ae041ffb923674c6bbf7ab0',
                    'f94e204d9bf6456c8e543313f4db4d0a', '2053c75ec8994d5ab8f1b75807fef29e',
                    '252efe46a5f24651af44ffc11cdbf110', 'd8754b8c244a4f3bb3ce91869fdefbd5',
                    '7089b1fe4cd048a2b7f057364f13de99', 'ba672168b6d84fc69e44628a82c39c29',
                    '1f12ebfff62047d09f992b3d6c7679c9', 'f4d7a495-d4b8-48d7-9046-00ab9873e4a0',
                    '01c3b456-3195-4d0a-83f2-7c3486bf442e', '075ff083a7fb4f77affd5525c4edf689',
                    '835bd40fe4403786450ce121ba2d6914', '54c97e2071f741a9a61eedb5bd9fd882',
                    '55530b652b0a45b6b366ad2967e0b01c', 'ebe53a41755e43efaef5e18b99fe8eae',
                    '756ef1589bbf4a4492c30fe6f696c101', '6109082fb5f8435b81d0e284e58f2959',
                    '77389105f274467eab96b416c52505d1', 'c8262cbbaea749a39617d36f62cc3cbb',
                    '1c9427bb0a9c45ce94406f50d32ce4dd', '0dec6278850c49b29917013e6e128804',
                    'b50b749cc3894255af58c4f0c99d0e61', 'b7c4af9b5e1c439aafe60159c71f1106',
                    '5100a6f3134c4ccdb3a854fdca301220', '62e7161e9ed240688b00fd3112a89291',
                    '1a87325ae12941399edc8347dcdf4aa4', '8a36c58e5bcc478bbecc4050f71a5e86',
                    '26158fe522b245ab9abd3538c16aa6a0', '030c01dc-5265-4864-adec-ea39174cd461',
                    '030c01dc-5265-4864-adec-ea39174cd461', 'f75d50e837874c7ea0476388feeb1e1f',
                    '2377fd290a644bb8b44f02a8bb27d190', 'b60ab8e601a245d09e204f6e8ef0a170',
                    'd0e3738c2cf043939076da98773d9ec5', 'fa722f15295740a89dacaf7cc0e2bae7',
                    'd2f83575f86442069a7cb2bc2685fe1c', 'b3faf925302a4fe5b8db6d5c2da64d0a',
                    '6b23cc1fa4c141988d4df4de014826bd', '030c01dc-5265-4864-adec-ea39174cd461',
                    '030c01dc-5265-4864-adec-ea39174cd461', 'dd493d7c196447a3b56277d90db150c0',
                    'e27d6ec7093649a6a92dae6bade66257', 'e27d6ec7093649a6a92dae6bade66257',
                    '9ed79d0c129d439ca81ab131a7c498f0', 'a866d00e99c549948d51bd35c3c3c47a',
                    '4af3915e81fa44cebf2494321c293518', 'b5bfd0ff0e4542a29cfa463ab5e9ce00',
                    '9d6e79f1615347629556677488c0cb84', 'e3822ae6d7284343b8963323d072bbfd',
                    '075ff083a7fb4f77affd5525c4edf689', 'eaca9790d62241df9b28cb35485ae344',
                    'c00d2982ef4c43588bd53c66342d9ee6', 'c6931a0e561e48308ed0b2837e431aec',
                    'e4881f3b439d43cdb6fafaf5fb0d8ffb', 'e4881f3b439d43cdb6fafaf5fb0d8ffb',
                    'b5778ae7191445d19f89b849605a77af', '6fbb5b26d3ab40fd9277fdb4ecfbe1fe',
                    '7f093db3b9ab4c3eb0bd7487463bada7', 'dd493d7c196447a3b56277d90db150c0',
                    '91240cb302994e6bb8b235b1e6ba24ae', 'a93b74ab58f544709d7d5cbc5f6eb482',
                    '49fb0fd8d1e048a78d3e1057c7df2c4c', 'd049aad5b19a47eabe3962e0e45efedc',
                    '5100a6f3134c4ccdb3a854fdca301220', 'd049aad5b19a47eabe3962e0e45efedc',
                    '7c97bed25433415cb1978037ffac1eb4', 'cfc2f4604058e4edf9ba9a99ac3de7b0',
                    '5d3fdd554b8a43aca0c1cc05d7529b43', '62e7161e9ed240688b00fd3112a89291',
                    '6991d2b9f4f04a1799fa4ba1ed3b0905', '787cc026907643ec92b50abeefb82dce',
                    '787cc026907643ec92b50abeefb82dce', 'f3ea56dff9ae4b08ac00ab7cbcf54eeb',
                    'ba50f83a5e4349ae9bdf793a91f10147', '2a5e9d296fb44a3c856f5a8c1eea8708',
                    'b7eed09830cf4952a0f596b0bc0043fd', '62e7161e9ed240688b00fd3112a89291',
                    '17e8f8b545c14e6a868aaf2f8da210ed', '17e8f8b545c14e6a868aaf2f8da210ed',
                    '854a5b2e335247b2acea21f17c724f84', 'c018ced8899d48989544ea8d6753c75c',
                    'a46d6e4d0d054d56810252ba9a3bb6b4', '749d7f6065384822819110d65a4da668',
                    '4af3915e81fa44cebf2494321c293518', 'cbb50aa7ed77414881ec927bb6b2235c',
                    'cbb50aa7ed77414881ec927bb6b2235c', 'ba240a6a8a4a45108a2b019f0de90ea9',
                    '0c859c5cd26b4926ad28e3ad5c708757', '2f97f97a3b7e4b94a91b2b8289a1650a',
                    '5b6c6a1a0a4bca75ed619d593a7ddbb2', '0923b5484189407eaab7a49a9568776c',
                    '6df1ae86cec742f69a0750987f4ec8de', '0ceb08df42614af28bafda80e8f1fe9c',
                    '7072edad-4d4c-4ba7-beac-2adc1514f652', '78ea3531277748b78e847136b34532a7',
                    '3df15ecb-6643-488f-baf9-06c621ecc46a', '5b16eec04b734d09b82086e4eb5ab8e0',
                    'ab66d93284294717a5cb2daa368b10d3', 'c6931a0e561e48308ed0b2837e431aec',
                    '3ee39b7902e847cb820426213a89a520', '6df1ae86cec742f69a0750987f4ec8de',
                    'c747aec7e7094acc96f40c1063a5bcbe', '957a715c6bb84b27b8655570688a4939',
                    '6109082fb5f8435b81d0e284e58f2959', '4fdb3db06d9c43a3ae04c1679158a3c8',
                    '2f964f42bf894af49cd1defa4a2389bd', 'b662fbe7424c4bd2b13aaacc49f88986',
                    '57b7bb4df351402d8eb65fb58260789d', '57b7bb4df351402d8eb65fb58260789d',
                    '30b3ab049abb4fd08e80b3b980c88b59', 'c4a79a9e46e34ffc9c99c3cce981c8f7',
                    '34d21ef2570343a1ac8af57a8b52f8cf', '25372406-6e5b-4708-9a68-bbb5eaea5576',
                    '4fc42745e9144bc38bc47b31c52882e1', '2f97f97a3b7e4b94a91b2b8289a1650a',
                    '7cf8a0f2496f4bf4a9f7ff6e337c940e', '92216367bba041708ef221c19eae79d9',
                    '2bf91ab7aced4f2a81cfd265191ccf9d', '81ef213ebd61412cb27391cfe598b3ac',
                    'e52ae6eb1b2f47c2b8dfe32b813ca964', '39a1a5f6ec2a4c02b39e45e77147e73f',
                    'dcfe743241e9407d9338b707107f147f', 'a338471780104a6f912af3e7b258d8be',
                    'a338471780104a6f912af3e7b258d8be', '9539771123504b6ab4eb018a68c23313',
                    '5341378a-c59e-4fc2-a9f8-7f3001f4f67d', '5341378a-c59e-4fc2-a9f8-7f3001f4f67d',
                    '42a29b76b8da498da732dcfce18c0b0d', '25372406-6e5b-4708-9a68-bbb5eaea5576',
                    '9d583b700822459da5e2bc8a5f4d5bb5', '29d331d6-d2d4-4a10-9ab4-3d9a54d957d4',
                    'f8442932ebd544cab5314b1aa9a3043f', '5af539bca42947758d24fc74bdc7a9c3',
                    'a3adeba2ec8c4b3faaa4d9a4e177ccfa', '69d24cb0cee54b26993987ce00f3afd8',
                    '5df699f310ad44d69996cc6310184bda', '6a9e4365b31448b39ef58f37bb1cd9dc',
                    '6a9e4365b31448b39ef58f37bb1cd9dc', '9b65d7f7231d4ff2bf19da7871f6c638',
                    'eaec4028a2e84cac99724abc69d3a08b', 'b3faf925302a4fe5b8db6d5c2da64d0a',
                    '56d014b8c7c948eaac27e60d9003fe83', 'f4d7a495-d4b8-48d7-9046-00ab9873e4a0',
                    'dd2efde1969d400591f7dc4f726a58f0', 'db66d953938f4ce1b42ecd0d3195ff56',
                    'b2deb560d63b47feb43cedfaf1da941a', '9916e60972c54b7588fa1dae85089987',
                    'e7bf2efb3bff468989e8f01042080ef2', '1c55f8d26118435aabd6c726d78022d9',
                    'cefaa8c46458420ba97cda51c9f9be8a', 'e91920d087cd4a588388c029825e17b7',
                    'fe79659803e24cd7aab60176f21af495', 'd86ac04d74ca4d9aba5478a1e4eaabec',
                    '13e2111e5f8a6e692da8b7d8d905838c', '2aa51b32c3ec4de3b116ae5ded6b3616',
                    'af9333478dfd4d71b94cad9813867f79', '49a5a23df345411a8ba4aea7b5c55c3e',
                    '55f135dae00449e2bd1763d1859db942', 'c013c422677d422fb7a629e1304c1f85',
                    '37905389c9314f7aafff31e682680813', '6cb1b1463d6b4eb184d23b499d6e673d',
                    'b824b73e-362f-482b-a7f9-d8789b566bb8', '49fb0fd8d1e048a78d3e1057c7df2c4c',
                    '67cfc13e22bc46449e190a77e12a7932', '68b82e8b3dc74931a37ded3e93b6ba49',
                    '1c21648ce95d4aedaa76a4ce2232b5d1', 'a24c15a6b653444bad95da3e6d28fc09',
                    '9592cfd08b4a4497a94414c185e23984', 'bcd2139f7c5046a992dc181fe514697e',
                    '7072edad-4d4c-4ba7-beac-2adc1514f652', '4d2e95dc92ad401aa3585c987f4b82a2',
                    '41e1facbc5da419b8bf08faf0a9d93e7', '6c6db651783841f9b75f233f0561c91a',
                    '2b612f554e1f4fa4b1ed3b88dd237d15', '465807d5-ddbe-41aa-8f10-95e87d6dbb92',
                    '932c85be117f477a84aab22f199872ec', '78896f55-a4b2-498e-a420-386b0af579b8',
                    'd5f629591f154fc2836ea809903b330e', '49a5a23df345411a8ba4aea7b5c55c3e',
                    '98fe25b5d6fc41138f76422a0488f007', '49fb0fd8d1e048a78d3e1057c7df2c4c',
                    '14ba32858c0a4d489dca04435cad5908', '6436552650b24d3a987d25d6ca7779b9',
                    'c6931a0e561e48308ed0b2837e431aec', '67ed9f13-83da-46be-8ab2-a076e5dc0f05',
                    'c50dd558e7914de792cbd7c633477581', '2053c75ec8994d5ab8f1b75807fef29e',
                    '5600e8743b324c2f9c7d44ab753676f5', 'e01bdfdc76b444c5b0341ff39ea09275',
                    '98c0b619a205472fabe888ac35783e6c', '34d21ef2570343a1ac8af57a8b52f8cf',
                    'cab22a983b694884bdc60141f05ea920', 'd5528f14ce174e218c9364893e771e52',
                    'dbf75383c63843bba5a663171acbc968', 'dbf75383c63843bba5a663171acbc968',
                    '92216367bba041708ef221c19eae79d9', '18fa008d3e8047479427d3b7e83e2c54',
                    '2d360c6db3f046e49299d54e6031e847', 'e27d6ec7093649a6a92dae6bade66257',
                    'e27d6ec7093649a6a92dae6bade66257', '20ec27bc78f14b25a6b3dcaa9ac242b2']
    for duid in pt_duid:
        p = popup('ok', duid, lang='en_US', app='ikey', version='2541',
                  way=source)
        p_extra = json.loads(p)
        try:
            extra_data = json.loads(p_extra['data']['extra'])
            print(extra_data['alg_hit'])
        except:
            extra_data = {'alg_hit': '3'}
        # try:
        if extra_data['alg_hit'] == '1':
            '''目前'thresholdScore', 'source'不统计'''
            # shall_be_keys = ['bucket', 'taghit', 'scenario', 'status',
            #                  'recommend', 'sessionId', 'alg_hit']
            shall_be_keys = ['bucket', 'taghit', 'scenario',
                             'recommend', 'sessionId', 'alg_hit']
            for key in shall_be_keys:
                if key not in extra_data.keys():
                    print("缺少字段:" + key)
                    print('失败')
                    assert False
                    break
                    # if extra_data['status'] != 'alg_resp':
                    #     print("status字段错误")
                    #     assert False
                    #     break
        elif extra_data['alg_hit'] == '0':
            # shall_be_keys = ['bucket', 'scenario', 'sessionId', 'alg_hit', 'status']
            shall_be_keys = ['bucket', 'scenario', 'sessionId', 'alg_hit']
            for key in shall_be_keys:
                if key not in extra_data.keys():
                    print("缺少字段:" + key)
                    print('失败')
                    assert False
                    break
                    # if (extra_data['status'] != 'alg_miss_random'):
                    #     print("status字段错误")
                    #     assert False
                    #     break
                    # except:
                    #     print('非算法')
                    # 资源内容统计
        elif extra_data['alg_hit'] == '4':
            '''目前'thresholdScore', 'source'不统计'''
            shall_be_keys = ['status']
            for key in shall_be_keys:
                if key not in extra_data.keys():
                    print("缺少字段:" + key)
                    print('失败')
                    assert False
                    break
            if extra_data['status'] == 'alg_timeout':
                print('算法超时')
            if (extra_data['status'] != 'random_resp') or (extra_data['status'] != 'alg_timeout'):
                print("status字段错误")
                print('失败')
                assert False
                break


if __name__ == '__main__':
    run(source_input())
