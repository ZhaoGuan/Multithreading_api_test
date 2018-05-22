# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import requests
from sanic import Sanic
from sanic.response import json as sanic_json
import json
import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + '/../')
app = Sanic()
from tag_list_check.get_data_from_googlesheet import appconfig_data


def get_appconfig_tags():
    tag_list = []
    appconfig_list = appconfig_data()
    new_appconfig = []
    for appconfig in appconfig_list:
        if appconfig['data']['style'] == 'new':
            temp_config = appconfig['check_value']['tags_config_url']
            if temp_config not in new_appconfig:
                new_appconfig.append(temp_config)
    for url in new_appconfig:
        response = requests.get(url)
        temp_tags = json.loads(response.text)['tags']
        for tag in temp_tags:
            if tag not in tag_list:
                tag_list.append(tag)
    return tag_list


@app.route("/get_tags")
async def get_tags(request):
    return sanic_json({"data": get_appconfig_tags()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
