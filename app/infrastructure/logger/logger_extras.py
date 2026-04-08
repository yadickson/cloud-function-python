import inspect

from app.infrastructure.logger.logger_extras_interface import LoggerExtrasInterface


class LoggerExtras(LoggerExtrasInterface):
    def get_extras(self) -> dict[str, str]:
        stack = inspect.stack()
        back = 2  # pragma: no mutate
        class_name = stack[back][0].f_locals["self"].__class__.__name__  # pragma: no mutate
        function_name = stack[back][0].f_code.co_name  # pragma: no mutate
        function_line = stack[back][0].f_lineno  # pragma: no mutate
        return {"logger_info": f"{class_name}:{function_name}:{function_line}"}
