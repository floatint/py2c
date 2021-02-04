from .Node import Node


class Module(Node):
    def __init__(self, name: str, lang: str):
        self.__children = list()
        self.__name = name
        self.__lang = lang

    def get_name(self) -> str:
        return self.__name

    def get_lang(self) -> str:
        return self.__lang

    def get_children(self) -> list:
        return self.__children

    def add_child(self, n: Node):
        self.__children.append(n)

    def add_children(self, ns: [Node]):
        self.__children.extend(ns)
