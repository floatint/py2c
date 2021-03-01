from .Node import Node


class LogicNot(Node):
    def __init__(self, value: Node):
        self.__value = value

    def get_value(self) -> Node:
        return self.__value
