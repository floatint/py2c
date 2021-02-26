# Класс реализует конвертацию инструкции присваивания
import ast
from translator.info.FunctionInfo import FunctionInfo
from .ValueILTranslator import ValueASTTranslator
from translator.il import *


class AssignILTranslator:

    # присваивание значения аргументу
    @staticmethod
    def assign_to_arg(target: ast.arg, value: ast.AST, func_ctx: FunctionInfo):
        # TODO: сначала нужно выполнить проверку на декларирование
        # TODO: потом вызывать целевой метод
        AssignILTranslator.__assign_to_sym(target.arg, value, func_ctx)
        # для начала проверим, задекларирован ли аргумент
        target_info = func_ctx.get_variable(target.arg)
        if not target_info.is_declared():
            # декларируем аргумент
            pass
        # получаем блок кода функции
        func_impl = func_ctx.get_implementation()
        # начинаем обработку value
        value_il_node = ValueASTTranslator.get_value(value, func_ctx)
        # после того как получили IL представление значения
        # определим тип узла значения
        if isinstance(value_il_node, Call):
            # если значение - результат вызова функции
            func_impl.add_impl_node(
                Assign()
            )
        elif isinstance(value_il_node, If):
            # если значение - цепочка условий,
            # то код присваивания нужно в самом внутреннем блоке true
            if_node = value_il_node
            while len(if_node.get_true_body()) > 0:
                # берем последний узел
                if_node = if_node.get_true_body()[-1]
            # нашли нужный блок if
            # выполняем присваивание
            if_node.add_true_statement(
                Assign()
            )
            pass
        pass

    @staticmethod
    def assign_to_name(target: ast.Name, value: ast.AST, func_ctx: FunctionInfo):
        pass


    # внутренний метод
    @staticmethod
    def __assign_to_sym(target_name: str, value: ast.AST, func_ctx: FunctionInfo):
        pass
