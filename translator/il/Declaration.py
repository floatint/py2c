from .Node import Node


# TODO: сделать общим для VariableDecl и FuncDecl ?
class Declaration(Node):
    def __init__(self, name: str):
        self.__name = name
        self.__type = ""
        self.__ptr_depth = 0
        self.__ref_depth = 0
        self.__arr_depth = 0
        self.__initializer = None
        self.__modifiers = list()

    def get_name(self) -> str:
        return self.__name

    def set_type(self, type: str):
        self.__type = type
        return self

    def get_type(self) -> str:
        return self.__type

    def as_ptr(self):
        self.__ptr_depth += 1
        self.__ref_depth = 0
        return self

    def is_ptr(self) -> bool:
        return True if self.__ptr_depth > 0 else False

    def get_ptr_depth(self) -> int:
        return self.__ptr_depth

    def as_ref(self):
        self.__ref_depth += 1
        self.__ptr_depth = 0
        return self

    def is_ref(self):
        return True if self.__ref_depth > 0 else False

    def get_ref_depth(self) -> int:
        return self.__ref_depth

    def as_arr(self):
        self.__arr_depth += 1
        return self

    def is_arr(self) -> bool:
        return True if self.__arr_depth > 0 else False

    def get_arr_depth(self) -> int:
        return self.__arr_depth

    def set_initializer(self, init: Node):
        self.__initializer = init
        return self

    def has_initializer(self) -> bool:
        return True if self.__initializer else False

    def get_initializer(self) -> Node:
        return self.__initializer

    def has_modifiers(self) -> bool:
        return True if len(self.__modifiers) > 0 else False

    def get_modifiers(self) -> list:
        return self.__modifiers

    def add_modifier(self, mod: str):
        self.__modifiers.append(mod)
        return self
