from __future__ import annotations

import collections.abc
import linecache
import sys
from types import FrameType
import typing


PREPEND_RESULT_LOG_MESSAGE: typing.Final[str] = "Result traceback log (error value is not controlled):\n\n"


def base_traceback_formatter() -> str:
    trace = []
    frame: FrameType | None = sys._getframe(4)
    count = 0

    while frame and count <= 15:
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        funcname = frame.f_code.co_name

        line = linecache.getline(filename, lineno).strip()
        trace.append(f'  File "{filename}", line {lineno}, in {funcname}\n    {line}\n')

        frame = frame.f_back
        count += 1

    return "\n".join(trace[::-1])


class ResultLoggingFactory:
    """Sigleton for logging result errors."""

    __slots__ = ("_log", "_traceback_formatter")

    def __init__(
        self,
        log: typing.Callable[[str], None] | None = None,
        traceback_formatter: typing.Callable[[], str] = base_traceback_formatter,
    ) -> None:
        self._log = log
        self._traceback_formatter = traceback_formatter

    def __call__(self, err: typing.Any) -> None:
        if self._log is not None:
            self._log(str(err))

    @property
    def used(self) -> bool:
        return self._log is not None

    def format_traceback(self, error: typing.Any, /) -> str:
        return self._traceback_formatter() + "\n\n" + repr(error)

    def set_log(self, log: typing.Callable[[str], None], /) -> typing.Self:
        self._log = log
        return self

    def set_traceback_formatter(self, formatter: typing.Callable[[], str], /) -> typing.Self:
        self._traceback_formatter = formatter
        return self


class ErrorLogFactoryMixin[Error]:
    _error: Error
    _tb: str | None
    _is_controlled: bool

    __slots__ = ("_error", "_tb", "_is_controlled")

    def __init__(self) -> None:
        self._tb = None if not RESULT_ERROR_LOGGER.used else PREPEND_RESULT_LOG_MESSAGE + RESULT_ERROR_LOGGER.format_traceback(self.error)
        self._is_controlled = False

    if not typing.TYPE_CHECKING:

        def __getattribute__(self, name, /):
            """If control over `.error` was passed to another logic
            (which is considered passed as soon as .error field is accessed)
            then there is no need to log on event of result deletion."""

            if name == "_error" and super().__getattribute__("_tb") is not None:
                self._is_controlled = True

            return super().__getattribute__(name)

    def __del__(self) -> None:
        if self._tb and not self._is_controlled:
            RESULT_ERROR_LOGGER(self._tb)

    @property
    def error(self) -> Error:
        return self._error


RESULT_ERROR_LOGGER: typing.Final[ResultLoggingFactory] = ResultLoggingFactory()


__all__ = ("RESULT_ERROR_LOGGER", "ErrorLogFactoryMixin", "ResultLoggingFactory")
