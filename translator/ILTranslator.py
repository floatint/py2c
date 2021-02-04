from .ITranslator import ITranslator
from .il.Module import Module
from .il.Node import Node
from .il.BlockComment import BlockComment
from .il.Include import Include
from .il.Newline import Newline
from .il.If import If
from .il.Call import Call
from .il.Array import Array
from .il.Value import Value
from .il.Implementation import Implementation
from pathlib import Path
import datetime as dt
import ast
import symtable
from .helpers import *


class ILTranslator:
    def __init__(self):
        # Корень IL
        self.__module = None
        # AST представление модуля
        self.__module_ast = None
        # Корневая таблица символов
        self.__module_sym_tbl = None
        # Исходный код
        self.__source_code = None
        # Стек областей видимости
        self.__scope_stack = list()
        # Определения функций и методов
        self.__func_decls = list()
        # Определение реализации функций и методов
        self.__func_impls = dict()
        # Задекларированные символы в текущей функции
        self.__curr_func_declared = list()
        # Что нужно освободить в случае чего
        self.__curr_func_decref = list()

    # принимаем информацию о модуле,
    def translate(self, source_info: {}) -> Node:
        self.__module = Module(Path(source_info["file_name"]).stem, "C")
        self.__module_ast = source_info["module_ast"]
        self.__module_sym_tbl = source_info["sym_table"]
        self.__source_code = source_info["source_code"]
        # сопроводительная информация
        header_comment = BlockComment(f"""
            This file was auto-generated from {source_info["file_name"]}
            Hash: {source_info["hash"]}
            Date: {dt.datetime.now()}
        """)

        # подключение стандартных хедеров
        include_python_h = Include("Python.h", False)
        include_structmember_h = Include("structmember.h", True)

        # докидываем в модуль
        self.__module.add_child(header_comment)
        self.__module.add_child(Newline())
        self.__module.add_child(include_python_h)
        self.__module.add_child(Newline())
        self.__module.add_child(include_structmember_h)
        self.__module.add_child(Newline())
        self.__module.add_child(Newline())
        self.__module.add_child(Declaration(
            "my_arr"
        ).set_type(
            "const char*"
        ).as_arr().set_initializer(
            Array().add_element(
                Value("my str").as_str()
            ).add_element(
                Value("NULL")
            ).add_element(Array().add_element(
                Value("0x45")
            )).add_element(
                Value("string long string").as_str()
            )
        ))

        self.__module.add_child(Newline())
        self.__module.add_child(Newline())



        self.__module.add_child(Call(
            "PyArg_ParseTuple"
        ).add_parameter(
            Declaration(
                "ss"
            ).set_type("PyObject").as_ptr()
        ))
        self.__module.add_child(Newline())
        self.__module.add_child(Function(
            "MyFunc"
        ).set_type("PyObject*").add_parameter(
            Declaration("module").set_type("PyObject").as_ptr()
        ).add_parameter(
            Declaration("args").set_type("PyObject").as_ptr()
        ).set_comment(
            LineComment(" Converted function")
        ))

        self.__module.add_child(Newline())
        self.__module.add_child(Implementation(
            Function(
                "test_func"
            ).set_type("PyObject*").add_parameter(
                Declaration("self").set_type("PyObject").as_ptr()
            ).add_modifier("static"),

            BlockComment("This is function prolog")
        ))

        # конвертируем модуль
        # собираем в IL
        self._convert_module()

        # оформляем итоговое представление

        # возвращаем собранный код в IL
        return self.__module

    # основная функция конвертации модуля
    # на вход принимает исходный код, аст, и таблицу символов
    def _convert_module(self):
        # устанавливаем область видимости модуля
        self.__scope_stack.append(self.__module_sym_tbl)

        # перебираем все функции
        for s in self.__module_ast.body:
            if isinstance(s, ast.FunctionDef):
                # найдем таблицу символов функции
                func_sym_tbl = list(filter(lambda x: x.get_name() == s.name, self.__module_sym_tbl.get_children()))[0]
                self._convert_def(s, func_sym_tbl)
        # снимаем область видимости модуля
        self.__scope_stack.pop(-1)

    # конвертирование функции
    # TODO: а что на счет генераторов ?
    def _convert_def(self, func: ast.FunctionDef, sym: symtable.SymbolTable):
        # тело функции
        func_impl = list()
        # получим описание функции
        decl = get_func_declaration(func, self.__scope_stack, self.__source_code)
        # устанавливаем контекст функции
        self.__scope_stack.append(sym)
        # переменные которые задекларированы
        declared_symbols = list()
        for i in decl.get_parameters():
            declared_symbols.append(i.get_name())
        # декларираем все остальные (параметры и внешние переменные)
        for i in sym.get_symbols():
            if not i.get_name() in declared_symbols and (i.is_parameter() or i.is_free()):
                # проверим символ на статику
                is_static = symbol_is_static(i, sym)
                func_impl.append(Declaration(
                    i.get_name()
                ).set_type("PyObject").add_modifier(
                    "static" if is_static else None
                ).as_ptr().set_initializer(
                    "NULL"
                ))
                declared_symbols.append(i.get_name())

        # проводим инициализацию параметров
        # сначала идут free, потом args
        # и смотрим еще откуда выборку делать
        args_fmt = get_args_fmt(func.args)
        parse_args_if = If()
        parse_args_if.add_true_statement(
            # если параметры разобраны успешно
            None
        )

        # снимаем контекст
        self.__scope_stack.pop(-1)


    #
    def _convert_arguments(self, args: ast.arguments):
        pass
