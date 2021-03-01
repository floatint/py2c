# Класс реализует конвертацию инструкции присваивания
import ast
from translator.info.FunctionInfo import FunctionInfo, VariableInfo
from .ValueILTranslator import ValueASTTranslator
from translator.il import *


class AssignILTranslator:

    # основной метод
    @staticmethod
    def assign(targets: ast.AST, values: ast.AST, func_ctx: FunctionInfo):
        if isinstance(targets, ast.arg):
            AssignILTranslator.__assign_to_sym(targets.arg, values, func_ctx)

    # внутренний метод
    @staticmethod
    def __assign_to_sym(target_name: str, value: ast.AST, func_ctx: FunctionInfo):

        # для начала вычислим IL узел(ы) для value
        value_il = ValueASTTranslator.get_value(value, func_ctx)
        # проверяем, задекларирована переменная или нет
        target_info = func_ctx.get_variable(target_name)
        # получаем хранилище кода функции
        func_code = func_ctx.get_implementation()
        # если переменная не задекларирована
        if target_info is None:
            target_info = VariableInfo(target_name)
            func_code.add_impl_node(
                Declaration(
                    target_name
                ).set_type("PyObject").as_ptr().set_initializer(
                    value_il
                )
            )
            target_info.as_declared()
            target_info.inc_ref()
        else:
            # отвязались от старого значения
            if target_info.is_tracked():
                target_info.dec_ref()
                func_code.add_impl_node(
                    Call(
                        "Py_XDECREF"
                    ).add_parameter(
                        Value(target_info.get_name())
                    )
                )
            # привязались к новому
            if target_info.is_static():
                left_value = Value(target_name).as_deref()
            else:
                left_value = Value(target_name)

            func_code.add_impl_node(
                Assign().set_left(left_value).set_right(value_il)
            )

        # проверка на NULL
        tracked_vars = [i for i in func_ctx.get_tracked_variables() if i.get_name() != target_info.get_name()]
        clean_list = list()
        for i in tracked_vars:
            clean_list.append(
                Call(
                    "Py_XDECREF"
                ).add_parameter(
                    Value(i.get_name())
                )
            )
        cmp_node = Compare("==")
        if target_info.is_static():
            cmp_node.set_left(
                Value(target_info.get_name()).as_deref()
            )
        else:
            cmp_node.set_left(
                Value(target_info.get_name())
            )

        cmp_node.set_right(
            Value("NULL")
        )
        if_node = If(cmp_node).add_true_statements(
            clean_list
        ).add_true_statement(
            Return(
                Call(
                    "PyErr_Occurred"
                )
            )
        )

        func_code.add_impl_node(
            if_node
        )
