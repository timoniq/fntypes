import typing

class SingletonMeta(type):
    pass

class Singleton(metaclass=SingletonMeta):
    _instance: typing.Self | None
