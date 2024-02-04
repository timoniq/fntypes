from __future__ import annotations

import traceback
import typing

class ResultLoggingFactory:
    """Sigleton for logging result errors."""

    def __init__(
        self,
        log: typing.Callable[[str], None] = lambda _: None,
        traceback_formatter: typing.Callable[[], str] | None = None,
    ):
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


class ErrorLogFactoryMixin:

    def __post_init__(self) -> None:
        tb = RESULT_ERROR_LOGGER.format_traceback(self.error)
        self.tb = "Result log\n" + tb

    def __getattribute__(self, __name: str) -> typing.Any:
        """
        If control over .error was passed to another logic 
        (which is considered passed as soon as .error field is accessed) 
        then there is no need to log on event of result deletion."""

        if __name == "error" and self.tb is not None:
            self.is_controlled = True
        
        return super().__getattribute__(__name)
    
    def __del__(self):
        if self.tb and not self.is_controlled:
            RESULT_ERROR_LOGGER(self.tb)


RESULT_ERROR_LOGGER: typing.Final[ResultLoggingFactory] = ResultLoggingFactory()
