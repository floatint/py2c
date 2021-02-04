from .Node import Node
from .Function import Function


class Implementation(Node):
    def __init__(self, func: Function, impl: Node):
        self.__function = func
        self.__implementation = impl

    def get_function(self) -> Function:
        return self.__function

    def get_implementation(self) -> Node:
        return self.__implementation
