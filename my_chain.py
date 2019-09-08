E_int, E_float, E_str = 'E_int', 'E_float', 'E_str'

import copy

class Object:
    def __init__(self):
        self.i = 0
        self.f = 0.0
        self.s = ""


class EventGet:
    def __init__(self, type):
        self.type = type
        self.kind = None
        if (self.type == str):
            self.kind = E_str
        elif (self.type == int):
            self.kind = E_int
        elif (self.type == float):
            self.kind = E_float



class EventSet:
    def __init__(self, value):
        self.value = value
        self.kind = None
        if isinstance(value, str):
            self.kind = E_str
        elif isinstance(value, int):
            self.kind = E_int
        elif isinstance(value, float):
            self.kind = E_float


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == E_int:
            if isinstance(event, EventGet):
                return obj.i
            elif isinstance(event, EventSet):
                obj.i = event.value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == E_float:
            if isinstance(event, EventGet):
                return obj.f
            elif isinstance(event, EventSet):
                obj.f = event.value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.kind == E_str:
            if isinstance(event, EventGet):
                return obj.s
            elif isinstance(event, EventSet):
                obj.s = event.value
        else:
            return super().handle(obj, event)