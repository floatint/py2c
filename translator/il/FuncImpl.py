from .Node import Node
from .FuncDef import FuncDef


# класс содержит реализацию функции
class FuncImpl(Node):
    def __init__(self, func_def: FuncDef):
        self.__func_def = func_def
        self.__impl_body = list()

    def get_func_def(self) -> FuncDef:
        return self.__func_def

    def add_impl_node(self, n: Node):
        self.__impl_body.append(n)
        return self

    def add_impl_node_block(self, b: list):
        self.__impl_body.extend(b)
        return self

    def insert_impl_node(self, idx: int, node: Node):
        self.__impl_body.insert(idx, node)
        return self

    def insert_impl_node_block(self, idx: int, block: list):
        self.__impl_body[idx:idx] = block
        return self

    def get_impl(self) -> list:
        return self.__impl_body
