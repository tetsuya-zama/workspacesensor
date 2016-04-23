# -*- coding: utf-8 -*-

def parse(dict):
    keys = dict.keys()
    key = keys[0]

    if key == "sensor_pin":
        if(dict[key] == -1):
            from sensorstub import Sensor as SensorStub
            return SensorStub(dict[key])
        else:
            from sensor import Sensor
            return Sensor(dict[key])
    elif(key == "and"):
        return AndCircuit(dict[key])
    elif(key == "or"):
        return OrCircuit(dict[key])
    else:
        return NULL

class Circuit :
    def __init__(self):
        pass

    def get_status(self):
        pass

class AndCircuit(Circuit) :
    def __init__(self,children):
        Circuit.__init__(self)
        self._children = map(lambda c: parse(c), children)

    def get_status(self) :
        results = map(lambda c: c.get_status(), self._children)
        if(0 not in results):
            return 1
        else:
            return 0

class OrCircuit(Circuit) :
    def __init__(self,children):
        Circuit.__init__(self)
        self._children = map(lambda c: parse(c), children)

    def get_status(self):
        results = map(lambda c: c.get_status(), self._children)
        if(1 in results):
            return 1
        else:
            return 0
