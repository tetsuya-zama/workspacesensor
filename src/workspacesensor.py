# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import sensorstub as sensor
from pubnub import Pubnub

CNS_DEFAULT_SETTING_FILE=os.path.join(os.path.dirname(__file__), 'setting.json')

class WorkspaceSensor:
    def __init__(self,setting_file_path):
        with open(setting_file_path) as f:
            self._setting = json.load(f,"utf-8")

        self._sensor = sensor.Sensor(self._setting["GPIO"])
        self._current_status = self._sensor.get_status()

        self._pubnub = Pubnub(publish_key=self._setting["publish_key"], subscribe_key=self._setting["subscribe_key"])
        self._pubnub.subscribe(channels='plzcast_' + self._setting["group"], callback=self._callback_plzcast,connect=self._callback_connect, reconnect=self._callback_connect)

    def run(self):
        while True:
            new_status = self._sensor.get_status()
            if(new_status != self._current_status):
                self._current_status = new_status
                self._send()

            time.sleep(self._setting["duration"])

    def _send(self):
        message=json.dumps({
            "floor":self._setting["floor"],
            "id":self._setting["id"],
            "name":self._setting["name"],
            "status":self._current_status
        })

        self._pubnub.publish(channel='wkstatus_' + self._setting["group"],message=message)

    def _callback_plzcast(self,message,channel):
        self._send()

    def _callback_connect(self,message):
        self._send()

if __name__ == '__main__':
    if(len(sys.argv) == 2):
        setting_file_path = sys.argv[1]
    else:
        setting_file_path = CNS_DEFAULT_SETTING_FILE

    workspace_sensor = WorkspaceSensor(setting_file_path)
    workspace_sensor.run()
