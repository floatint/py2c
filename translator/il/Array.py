from .Node import Node


class Array(Node):
    def __init__(self):
        self.__elements = list()

    def get_elements_count(self) -> int:
        return len(self.__elements)

    def get_elements(self) -> list:
        return self.__elements

    def add_element(self, n: Node):
        self.__elements.append(n)
        return self
