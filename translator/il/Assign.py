from .Node import Node


class Assign(Node):
    def __init__(self):
        self.__left = None
        self.__right = None

    def get_left(self) -> Node:
        return self.__left

    def set_left(self, n: Node):
        self.__left = n
        return self

    def get_right(self) -> Node:
        return self.__right

    def set_right(self, n: Node):
        self.__right = n
        return self
