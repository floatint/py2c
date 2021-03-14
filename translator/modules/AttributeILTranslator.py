# класс, предоставляющий методы по обработке аттрибутов
import ast
from translator.info.FunctionInfo import FunctionInfo, VariableInfo
from translator.il import *
from utils.exceptions import SourceError
import translator.helpers as hlp


class AttributeILTranslator:

    @staticmethod
    def get_attribute(attr: ast.Attribute, func_ctx: FunctionInfo):
        # если требуется аттрибут переменной
        if isinstance(attr.value, ast.Name):
            value_info = func_ctx.get_variable(attr.value.id)
            # если не понимаем откуда брать аттрибут
            if value_info is None:
                raise SourceError(attr.lineno, attr.col_offset, f"name \'{attr.value.id}\' not defined")
            # выбираем аттрибут
            return Call(
                "Py2C_GetAttrString"
            ).add_parameter(
                Value(attr.value.id)
            ).add_parameter(
                Value(attr.attr).as_str()
            )
        # цепочка аттрибутов
        elif isinstance(attr.value, ast.Attribute):
            prev_attr = AttributeILTranslator.get_attribute(attr.value, func_ctx)
            return Call(
                "Py2C_GetAttrStringSafe"
            ).add_parameter(
                Value(prev_attr)
            ).add_parameter(
                Value(attr.attr).as_str()
            )
        pass
    # генерация кода для получения значения аттрибута
    # если на входе цепочка аттрибутов a.b.c - то вернет вложенные блоки
    # if. Последний из которых будет содержать Call с выборкой аттрибута
    # проверка которого будет лежать в вызывающем коде
    # Если на входе a.b, то вернет Call с выборкой аттрибута
    # @staticmethod
    # def get_attribute(attr: ast.Attribute, func_ctx: FunctionInfo):
    #     # если берем аттрибут какой-либо переменной
    #     if isinstance(attr.value, ast.Name):
    #         # проверим, известно ли что-то о attr.value
    #         # TODO: проверка на is_static
    #         value_info = func_ctx.get_variable(attr.value.id)
    #         if value_info is None:
    #             raise SourceError(attr.lineno, attr.col_offset, f"name \'{attr.value.id}\' not defined")
    #         # иначе
    #         return Call(
    #             "PyObject_GetAttrString"
    #         ).add_parameter(
    #             Value(attr.value.id)
    #         ).add_parameter(
    #             Value(attr.attr).as_str()
    #         )
    #     # цепочка аттрибутов
    #     elif isinstance(attr.value, ast.Attribute):
    #         func_impl = func_ctx.get_implementation()
    #         prev_attr = AttributeILTranslator.get_attribute(attr.value, func_ctx)
    #         # проверяем, задекларирована ли переменная
    #         var_info = func_ctx.get_variable(hlp.get_mangled_name(None, attr.value.attr))
    #         if var_info is None:
    #             var_info = VariableInfo(hlp.get_mangled_name(None, attr.value.attr))
    #             func_impl.add_impl_node(
    #                 Declaration(
    #                     hlp.get_mangled_name(None, attr.value.attr)
    #                 ).set_type("PyObject").as_ptr().set_initializer(
    #                     prev_attr
    #                 )
    #             )
    #             var_info.as_declared()
    #             var_info.inc_ref()
    #             func_ctx.add_variable(var_info)
    #         else:
    #             func_impl.add_impl_node(
    #                 Assign().set_left(
    #                     Value(hlp.get_mangled_name(None, attr.value.attr))
    #                 ).set_right(
    #                     prev_attr
    #                 )
    #             )
    #
    #         # получить список отслеживаемых переменных
    #         prev_attr_name = hlp.get_mangled_name(None, attr.value.attr)
    #         tracked_vars = [i for i in func_ctx.get_tracked_variables() if i.get_name() != prev_attr_name]
    #         # список очистки
    #         clean_list = list()
    #         for i in tracked_vars:
    #             clean_list.append(
    #                 Call(
    #                     "Py_XDECREF"
    #                 ).add_parameter(
    #                     Value(i.get_name())
    #                 )
    #             )
    #         # формируем проверку
    #         func_impl.add_impl_node(
    #             If(Compare("==").set_left(
    #                 Value(hlp.get_mangled_name(None, attr.value.attr))
    #             ).set_right(
    #                 Value("NULL")
    #             )).add_true_statements(
    #                 clean_list
    #             ).add_true_statement(
    #                 Return(
    #                     Call(
    #                         "PyErr_Occurred"
    #                     )
    #                 )
    #             )
    #         )
    #
    #         return Call(
    #             "PyObject_GetAttrString"
    #         ).add_parameter(
    #             Value(hlp.get_mangled_name(None, attr.value.attr))
    #         ).add_parameter(
    #             Value(attr.attr).as_str()
    #         )



    @staticmethod
    def set_attribute(attr: ast.Attribute, value: ast.AST, func_ctx: FunctionInfo):
        pass
