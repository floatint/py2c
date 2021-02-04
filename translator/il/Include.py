from .Node import Node


class Include(Node):

    def __init__(self, name: str, local_import: bool):
        self.__name = name
        self.__local_import = local_import

    def get_name(self) -> str:
        return self.__name

    def is_local_import(self) -> bool:
        return self.__local_import
