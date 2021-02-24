from .Node import Node


class BitwiseOr(Node):
    def __init__(self, l: Node, r: Node):
        self.__left = l
        self.__right = r

    def get_left(self) -> Node:
        return self.__left

    def get_right(self) -> Node:
        return self.__right

