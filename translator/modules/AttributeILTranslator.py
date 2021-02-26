# класс, предоставляющий методы по обработке аттрибутов
import ast
from translator.info.FunctionInfo import FunctionInfo


class AttributeILTranslator:

    @staticmethod
    def get_attribute(attr: ast.Attribute, func_ctx: FunctionInfo):
        pass

    @staticmethod
    def set_attribute(attr: ast.Attribute, value: ast.AST, func_ctx: FunctionInfo):
        pass
