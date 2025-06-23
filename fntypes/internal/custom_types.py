import typing

type CastTransformer[T, R] = typing.Callable[[T], R] | type[type[T]]
