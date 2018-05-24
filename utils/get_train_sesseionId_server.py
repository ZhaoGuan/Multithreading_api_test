# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sanic import Sanic
from sanic.response import json as sanic_json
import json

app = Sanic()

path = '/home/pubsrv/logs/java/model-nearline/monitor.log'


def line_log_reader(line_log):
    log = line_log.split(' RecommendMonitor:11 - ')
    dict_log = json.loads(log[1].replace('"{', '{').replace('}"', '}'))
    timestamp = int(dict_log['timestamp'])
    sessionId = dict_log['sessionId']
    return {'timestamp': timestamp, 'sessionId': sessionId}


def log_result():
    result = []
    with open(path) as f:
        for line in f:
            line_data = line_log_reader(line.replace('\n', '').replace('\\', ''))
            result.append(line_data)
    print(result)
    return result


@app.route("/get_sessionId")
async def get_sessionId(request):
    return sanic_json({"data": log_result()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
