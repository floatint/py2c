from .Node import Node


class Value(Node):
    def __init__(self, value):
        self.__value = value
        self.__as_str = False

    def as_str(self):
        self.__as_str = True
        return self

    def is_str(self) -> bool:
        return self.__as_str

    def get_value(self):
        return self.__value
