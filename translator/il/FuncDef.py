# класс описывает объявление и реализацию функции или метода

from .Node import Node
from .Declaration import Declaration


class FuncDef(Node):
    def __init__(self, name: str):
        self.__name = name
        self.__ret_type = "void"
        self.__parameters = list()
        self.__modifiers = list()
        self.__impl_block = list()

    def get_name(self) -> str:
        return self.__name

    def get_ret_type(self) -> str:
        return self.__ret_type

    def set_ret_type(self, ret_type: str):
        self.__ret_type = ret_type
        return self

    def has_modifiers(self) -> bool:
        return True if len(self.__modifiers) > 0 else False

    def get_modifiers(self) -> list:
        return self.__modifiers

    def add_modifier(self, modifier: str) -> object:
        self.__modifiers.append(modifier)
        return self

    def get_parameters(self) -> list:
        return self.__parameters

    def add_parameter(self, param: Declaration):
        self.__parameters.append(param)
        return self

    def has_implementation(self) -> bool:
        return True if len(self.__impl_block) > 0 else False

    def get_implementation_nodes(self) -> list:
        return self.__impl_block

    def add_implementation_node(self, n: Node):
        self.__impl_block.append(n)
        return self
