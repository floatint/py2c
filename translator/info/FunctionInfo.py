# класс описывает информацию о функции
import ast


class FunctionInfo:
    def __init__(self):
        self.__args_name = "args"
        self.__kwargs_name = "kwargs"
        self.__first_parameter_name = "module"
        self.__

    def get_args_name(self) -> str:
        return self.__args_name

    def set_args_name(self, n: str):
        self.__args_name = n

    def get_kwargs_name(self) -> str:
        return self.__kwargs_name

    def set_kwargs_name(self, n: str):
        self.__kwargs_name = n

    def get_first_parameter_name(self) -> str:
        return self.__first_parameter_name

    def set_first_parameter_name(self, n: str):
        self.__first_parameter_name = n

