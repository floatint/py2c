from .Node import Node
from .Declaration import Declaration


class Call(Node):
    def __init__(self, name: str):
        self.__name = name
        self.__param_decls = list()

    def get_name(self) -> str:
        return self.__name

    def add_parameter(self, p: Declaration):
        self.__param_decls.append(p)
        return self

    def has_parameters(self) -> bool:
        return True if len(self.__param_decls) > 0 else False

    def get_parameters(self) -> list:
        return self.__param_decls
