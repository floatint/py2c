from .Node import Node


class If(Node):
    def __init__(self, cond: Node):
        self.__true_body = list()
        self.__false_body = list()
        self.__condition = cond

    def get_condition(self) -> Node:
        return self.__condition

    def has_false_body(self) -> bool:
        return True if len(self.__false_body) > 0 else False

    def get_false_body(self) -> list:
        return self.__false_body

    def add_false_statement(self, s: Node):
        self.__false_body.append(s)
        return self

    def add_false_statements(self, sl: list):
        self.__false_body.extend(sl)
        return self

    def has_true_body(self) -> bool:
        return True if len(self.__true_body) > 0 else False

    def get_true_body(self) -> list:
        return self.__true_body

    def add_true_statement(self, s: Node):
        self.__true_body.append(s)
        return self

    def add_true_statements(self, sl: list):
        self.__true_body.extend(sl)
        return self
