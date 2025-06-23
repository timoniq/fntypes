import typing


type _SingletonInstance = typing.Any


class SingletonMeta(type):
    _instance: _SingletonInstance = None

    @typing.override
    def __call__(cls, *args: typing.Any, **kwargs: typing.Any) -> _SingletonInstance:
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Singleton(metaclass=SingletonMeta):
    pass
