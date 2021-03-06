# класс, генерирующий код сборки константных значений True, False, None, etc
import ast
from translator.il import *


class ConstsILTranslator:

    @staticmethod
    def get_const(const: ast.NameConstant):
        if isinstance(const.value, type(None)):
            return Value("Py_None")
        elif isinstance(const.value, bool):
            if const.value:
                return Value("Py_True")
            else:
                return Value("Py_False")
