from .Node import Node


class If(Node):
    def __init__(self):
        self.__true_body = list()
        self.__false_body = list()
        self.__condition = None

    def has_false_body(self) -> bool:
        return True if len(self.__false_body) > 0 else False

    def get_false_body(self) -> list:
        return self.__false_body

    def add_true_statement(self, s: Node):
        self.__true_body.append(s)
        return self
