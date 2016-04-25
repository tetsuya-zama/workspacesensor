# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import circuit
from pubnub import Pubnub
from resistance import Resistance

CNS_DEFAULT_SETTING_FILE=os.path.join(os.path.dirname(__file__), 'setting.json')

class WorkspaceSensor:
    def __init__(self,setting_file_path):
        with open(setting_file_path) as f:
            self._setting = json.load(f,"utf-8")

        self._circuit = circuit.parse(self._setting["GPIO"])
        self._current_status = self._circuit.get_status()

        self._on_resistance = Resistance(self._setting["on_resistance"],1,self._update_status)
        self._off_resistance = Resistance(self._setting["off_resistance"],0,self._update_status)

        self._pubnub = Pubnub(publish_key=self._setting["publish_key"], subscribe_key=self._setting["subscribe_key"])
        self._pubnub.subscribe(channels='plzcast_' + self._setting["group"], callback=self._callback_plzcast,connect=self._callback_connect, reconnect=self._callback_connect)

    def run(self):
        while True:
            sensor_status = self._circuit.get_status()
            if(sensor_status == 1):
                self._on_resistance.load()
                self._off_resistance.clear()
            else:
                self._off_resistance.load()
                self._on_resistance.clear()

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

    def _update_status(self,new_status):
        if(new_status != self._current_status):
            self._current_status = new_status
            self._send()

if __name__ == '__main__':
    if(len(sys.argv) == 2):
        setting_file_path = sys.argv[1]
    else:
        setting_file_path = CNS_DEFAULT_SETTING_FILE

    workspace_sensor = WorkspaceSensor(setting_file_path)
    workspace_sensor.run()
