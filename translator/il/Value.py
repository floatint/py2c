from .Node import Node


class Value(Node):
    def __init__(self, value):
        self.__value = value
        self.__as_str = False
        self.__as_ref = False
        self.__deref_depth = 0

    def as_str(self):
        self.__as_str = True
        self.__as_ref = False
        self.__deref_depth = 0
        return self

    def is_str(self) -> bool:
        return self.__as_str

    def as_ref(self):
        self.__as_ref = True
        self.__as_str = False
        self.__deref_depth = 0
        return self

    def is_ref(self) -> bool:
        return self.__as_ref

    def as_deref(self):
        self.__as_str = False
        self.__as_ref = False
        self.__deref_depth += 1
        return self

    def is_deref(self) -> bool:
        return self.__deref_depth > 0

    def get_deref_depth(self) -> int:
        return self.__deref_depth

    def get_value(self):
        return self.__value
