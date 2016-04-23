# -*- coding: utf-8 -*-

import random
from circuit import Circuit

class Sensor(Circuit):
    def __init__(self,pin_no):
        Circuit.__init__(self)

    def get_status(self):
        return random.randint(0,1)
