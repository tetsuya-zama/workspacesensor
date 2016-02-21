# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

class Sensor:
    def __init__(self,setting):
        self._setting = setting
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._setting["sensor_pin"], GPIO.IN)

    def get_status():
        inputValue = GPIO.input(self._setting["sensor_pin"])
        if (inputValue == True):
            return 1
        else:
            return 0
