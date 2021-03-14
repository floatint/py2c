# генерация кода вызова функции
from translator.info.FunctionInfo import FunctionInfo
from translator.il import *
from .TranslationInfo import TranslationInfo
import ast


class CallILTranslator:

    # TODO: скорее всего нудно ввести Py2C_Call()
    @staticmethod
    def call(call_node: ast.Call, func_ctx: FunctionInfo) -> TranslationInfo:
        code_list = list()
        # вызов функции
        if isinstance(call_node.func, ast.Name):
            # получаем таблицу символов функции
            func_sym_tbl = func_ctx.get_symbol_table()
            func_sym = [i for i in func_sym_tbl.get_symbols() if i.get_name() == call_node.func.id][0]
            # если вызываемая функция глобальна
            if func_sym.is_global():
                # подгрузим ее из глобального контекста
                code_list.append(
                    Call(
                        "PyObject_Call"
                    ).add_parameter(
                        Call(
                            "PyDict_GetItemString"
                        ).add_parameter(
                            Call("PyEval_GetGlobals")
                        ).add_parameter(
                            Value(func_sym.get_name()).as_str()
                        )
                    )
                )
                pass
        pass
