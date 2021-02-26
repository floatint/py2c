# класс для начальной работы с различными значениями: числа, кортежи, аттрибуты
import ast
from translator.info.FunctionInfo import FunctionInfo
from translator.il.Node import Node
from .NumberILTranslator import NumberILTranslator


class ValueASTTranslator:

    @staticmethod
    def get_value(value: ast.AST, func_ctx: FunctionInfo) -> Node:
        if isinstance(value, ast.Num):
            return NumberILTranslator.number(value)

