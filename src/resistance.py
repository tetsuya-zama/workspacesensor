# -*- coding: utf-8 -*-

class Resistance:
    def __init__(self,length,value,on_through):
        self._initial_length = length
        self._length = length
        self._value = value
        self._on_through = on_through

    def load(self):
        self._length = self._length - 1
        if(self._length == 0):
            self._on_through(self._value)
            self.clear()

    def clear(self):
        self._length = self._initial_length
