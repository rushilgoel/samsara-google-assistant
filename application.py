from flask import Flask, render_template, request, flash, url_for, redirect, abort, make_response
import json
import os

import samsara
from samsara.apis import SamsaraClient

application = Flask(__name__)


## Values are hard-coded for a specific group for Rushil Goel
## To make this more generic, need to implement OAuth in server & manage more sensor names

SAMSARA_GROUP_ID = 1154
SAMSARA_ROOM_SENSOR_ID = 212014918096236
SAMSARA_FRIDGE_SENSOR_ID = 212014918083943
SAMSARA_FREEZER_SENSOR_ID = 212014918083902

if 'DEBUG' in os.environ and os.environ['DEBUG'] == '1':
    application.debug = True

@application.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") == "list_sensors":
        res = listSensors()
    elif req.get("result").get("action") == "get_temperature":
        res = getTemperature(req)
    else:
        res = {}

    return res

def listSensors():
    client = SamsaraClient()
    try:
        response = client.get_sensors(os.environ['SAMSARA_ACCESS_TOKEN'], samsara.GroupParam(SAMSARA_GROUP_ID))
    except ApiException as e:
        return {}

    speech = "The sensors in your group are "

    for sensor in response.sensors[:-1]:
        speech += sensor.name + ", "

    speech += "and " + response.sensors[-1].name

    print speech
    return {
        "speech" : speech,
        "displayText" : speech,
        "source" : "Samsara"
    }

def getTemperature(req):
    client = SamsaraClient()

    sensor_name = req.get("result").get("parameters").get("sensor_name")

    if sensor_name == "Room":
        sensor_id = SAMSARA_ROOM_SENSOR_ID
    elif sensor_name == "Fridge":
        sensor_id = SAMSARA_FRIDGE_SENSOR_ID
    elif sensor_name == "Freezer":
        sensor_id = SAMSARA_FREEZER_SENSOR_ID
    else:
        sensor_id = SAMSARA_ROOM_SENSOR_ID

    try:
        response = client.get_sensors_temperature(os.environ['SAMSARA_ACCESS_TOKEN'], samsara.SensorParam(SAMSARA_GROUP_ID, [sensor_id]))
    except ApiException as e:
        return {}

    temperature = response.sensors[0].ambient_temperature / 1000

    speech = "The temperature is "+str(temperature)+" degrees Celsius"

    return {
        "speech" : speech,
        "displayText" : speech,
        "source" : "Samsara"
    }



@application.route('/admin/healthcheck')
def healthcheck():
    return "Hello World!"

if __name__ == '__main__':
        if 'LOCALHOST' in os.environ and os.environ['LOCALHOST'] == '1':
                application.run('0.0.0.0', use_reloader=False)
        else:
                application.run('0.0.0.0')