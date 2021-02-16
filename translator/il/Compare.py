from .Node import Node


class Compare(Node):

    def __init__(self, op: str):
        self.__op = op
        self.__left = None
        self.__right = None

    def get_op(self) -> str:
        return self.__op

    def get_left(self) -> Node:
        return self.__left

    def set_left(self, l: Node):
        self.__left = l
        return self

    def get_right(self) -> Node:
        return self.__right

    def set_right(self, r: Node):
        self.__right = r
        return self
