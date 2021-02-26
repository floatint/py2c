# класс для работы с числами
import ast
from translator.il import *


class NumberILTranslator:

    @staticmethod
    def number(num: ast.Num) -> Node:
        if isinstance(num.n, int):
            return NumberILTranslator.int(num.n)
        elif isinstance(num.n, float):
            return NumberILTranslator.double(num.n)
        else:
            raise RuntimeError(f"Couldn't dispatch object {num}")

    @staticmethod
    def int(i_num: int) -> Node:
        return Call("PyLong_FromLong").add_parameter(i_num)

    @staticmethod
    def double(d_num: int) -> Node:
        return Call("PyDouble_FromDouble").add_parameter(d_num)
