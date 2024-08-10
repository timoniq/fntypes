from __future__ import annotations

import traceback
import typing

Error = typing.TypeVar("Error", covariant=True)


class ResultLoggingFactory:
    """Sigleton for logging result errors."""

    __slots__ = ("_log", "_traceback_formatter")

    def __init__(
        self,
        log: typing.Callable[[str], None] = lambda _: None,
        traceback_formatter: typing.Callable[[], str] | None = None,
    ) -> None:
        self._log = log
        self._traceback_formatter = traceback_formatter or self.base_traceback_formatter
 
    def __call__(self, err: typing.Any) -> None:
        self._log(str(err))
    
    @staticmethod
    def base_traceback_formatter() -> str:
        summary = traceback.extract_stack()
        while len(summary) > 2:
            if summary[-1].filename in (__file__, "<string>", "<module>"):
                summary.pop()
            else:
                break
        trace = traceback.format_list(summary)
        return "\n".join(trace)

    def format_traceback(self, error: typing.Any) -> str: 
        return self._traceback_formatter() + "\n\n  " + repr(error)
    
    def set_log(self, log: typing.Callable[[str], None]) -> None:
        self._log = log
    
    def set_traceback_formatter(self, formatter: typing.Callable[[], str]) -> None:
        self._traceback_formatter = formatter


class ErrorLogFactoryMixin(typing.Generic[Error]):
    _error: Error
    _tb: str | None
    _is_controlled: bool

    __slots__ = ("_error", "_tb", "_is_controlled")

    def __init__(self) -> None:
        self._tb = "Result log\n" + RESULT_ERROR_LOGGER.format_traceback(self.error)

    def __getattribute__(self, name: str, /) -> typing.Any:
        """If control over `.error` was passed to another logic 
        (which is considered passed as soon as .error field is accessed) 
        then there is no need to log on event of result deletion."""

        if name == "error" and self._tb is not None:
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
