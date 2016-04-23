# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from circuit import Circuit

class Sensor(Circuit):
    def __init__(self,pin_no):
        Circuit.__init__(self)
        self._pin_no = pin_no
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin_no, GPIO.IN)

    def get_status(self):
        inputValue = GPIO.input(self._pin_no)
        if (inputValue == True):
            return 1
        else:
            return 0
