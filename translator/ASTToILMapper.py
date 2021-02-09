# класс маппит числа, строки и другие объкты в формат IL
import ast
from .il import *


# TODO: все что возвращают методы этого класс - новые интсансы
# TODO: нужно учитывать ref count
class ASTToILMapper:

    # функция возвращает IL узел, который представляет собой числовое значение
    @staticmethod
    def get_num_value(ast_num: ast.Num) -> Node:
        # простое число
        if isinstance(ast_num.n, int):
            return Call(
                "PyLong_FromLong"
            ).add_parameter(
                ast_num.n
            )
        elif isinstance(ast_num.n, float):
            return Call(
                "PyFloat_FromDouble"
            ).add_parameter(
                ast_num.n
            )
        else:
            raise ValueError(f"Can't dispatch {ast_num.n} value")

    @staticmethod
    def get_str_value(ast_str: ast.Str) -> Node:
        return Call(
            "PyUnicode_FromString"
        ).add_parameter(
            ast_str.s
        )

    # функция, возвращающая IL узел кортежа
    @staticmethod
    def get_tuple_value(ast_tuple: ast.Tuple) -> Node:
        pass