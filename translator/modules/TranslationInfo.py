# TODO: предусмотреть возможность возвращать состояние трансляции
# TODO: т.е. нужно ли оборачивать сгенерированный код в вызывающем блоке
# TODO: что модуль сгенерировал и другую информацию
from translator.il import *


# класс, содержащий информацию о произведенной трансляции
class TranslationInfo:

    def __init__(self):
        # сгенерированный код
        self.__code = list()
        # список отслеживаемых ссылок
        self.__check_list = list()

    def get_code(self) -> list:
        return self.__code

    def add_code_node(self, n: Node):
        self.__code.append(n)
        return self

    def add_code_nodes(self, nl: list):
        self.__code.extend(nl)
        return self

    # является ли сгенерированный код
    # просто вызовом функции или значением
    def is_value(self) -> bool:
        pass

    # требуется ли проверить на NULL
    def is_checked(self):
        return False
