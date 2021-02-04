from .Node import Node
from .Declaration import Declaration
from .Comment import Comment


# TODO: добавить кол-во параметров, их тип и имена
class Function(Node):
    def __init__(self, name: str):
        self.__name = name
        self.__type = ""
        self.__parameters = list()
        self.__modifiers = list()
        self.__comment = None

    def get_name(self) -> str:
        return self.__name

    def set_type(self, type: str):
        self.__type = type
        return self

    def get_type(self) -> str:
        return self.__type

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

    def get_comment(self) -> Comment:
        return self.__comment

    def set_comment(self, comment: Comment):
        self.__comment = comment
        return self
