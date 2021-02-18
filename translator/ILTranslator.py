from .ITranslator import ITranslator
from .il import *

from pathlib import Path
import datetime as dt
from .ASTToILMapper import ASTToILMapper
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
        # TODO: Список функций и методов модуля
        self.__func_defs = list()
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
        # self.__module.add_child(Declaration(
        #     "my_arr"
        # ).set_type(
        #     "const char*"
        # ).as_arr().set_initializer(
        #     Array().add_element(
        #         Value("my str").as_str()
        #     ).add_element(
        #         Value("NULL")
        #     ).add_element(Array().add_element(
        #         Value("0x45")
        #     )).add_element(
        #         Value("string long string").as_str()
        #     )
        # ))
        #
        # self.__module.add_child(Newline())
        # self.__module.add_child(Newline())
        #
        #
        #
        # self.__module.add_child(Call(
        #     "PyArg_ParseTuple"
        # ).add_parameter(
        #     Declaration(
        #         "ss"
        #     ).set_type("PyObject").as_ptr()
        # ))
        # self.__module.add_child(Newline())
        # self.__module.add_child(Function(
        #     "MyFunc"
        # ).set_type("PyObject*").add_parameter(
        #     Declaration("module").set_type("PyObject").as_ptr()
        # ).add_parameter(
        #     Declaration("args").set_type("PyObject").as_ptr()
        # ).set_comment(
        #     LineComment(" Converted function")
        # ))
        #
        # self.__module.add_child(Newline())
        # self.__module.add_child(Implementation(
        #     Function(
        #         "test_func"
        #     ).set_type("PyObject*").add_parameter(
        #         Declaration("self").set_type("PyObject").as_ptr()
        #     ).add_modifier("static"),
        #
        #     BlockComment("This is function prolog")
        # ))

        # конвертируем модуль
        # собираем в IL
        self._translate_module()

        # оформляем итоговое представление
        # сначала наполним модуль декларациями функций
        for i in self.__func_decls:
            self.__module.add_child(i)
            self.__module.add_child(Newline())
        # далее наполним реализациями
        for i in self.__func_decls:
            self.__module.add_child(self.__func_impls[i.get_name()])
        # возвращаем собранный код в IL
        return self.__module

    # основная функция конвертации модуля
    # на вход принимает исходный код, аст, и таблицу символов
    def _translate_module(self):
        # устанавливаем область видимости модуля
        self.__scope_stack.append(self.__module_sym_tbl)

        # перебираем все функции
        for s in self.__module_ast.body:
            if isinstance(s, ast.FunctionDef):
                # найдем таблицу символов функции
                func_sym_tbl = list(filter(lambda x: x.get_name() == s.name, self.__module_sym_tbl.get_children()))[0]
                # транслируем функцию
                self.__translate_func_def(s, func_sym_tbl)
        # снимаем область видимости модуля
        self.__scope_stack.pop(-1)

    # трансляция функции
    def __translate_func_def(self, func: ast.FunctionDef, st: symtable.SymbolTable):
        func_def = FuncDef(get_resolved_name(self.__scope_stack, st.get_name()))
        # имплементация функции
        func_impl = FuncImpl(func_def)
        func_def.set_ret_type("PyObject*")
        func_def.add_modifier("static")
        # если функция глобальная (модуль)
        if not st.is_nested():
            func_def.add_parameter(
                Declaration(
                    "module"
                ).set_type(
                    "PyObject"
                ).as_ptr()
            )
        # если функция вложенная или метод
        elif st.is_nested() and self.__scope_stack[-1].get_type() == "function":
            func_def.add_parameter(
                Declaration(
                    "context"
                ).set_type(
                    "PyObject"
                ).as_ptr()
            )

        # декларируем аргументы функции
        for a in st.get_symbols():
            if a.is_parameter():
                func_impl.add_impl_node(self.__declare_var(a.get_name()))

        # попробуем подгрузить аргументы
        arg_load_block = If(Call(
            get_system_name("parse_args")
        ).add_parameter(

        ))

        a = 6

    # трансляция функции
    # TODO: а что на счет генераторов ?
    # TODO: как вариант, сначала определить что перед нами
    # TODO: чистая функция или генератор
    def _translate_func(self, func: ast.FunctionDef, s: symtable.SymbolTable) -> FuncDef:
        # создаем узел с описанием функции
        func_def = FuncDef(get_resolved_name(self.__scope_stack, s.get_name()))
        func_def.set_ret_type("PyObject*")
        func_def.add_modifier("static")
        # если функция глобальная (модуль)
        if not s.is_nested():
            func_def.add_parameter(
                Declaration(
                    "module"
                ).set_type(
                    "PyObject"
                ).as_ptr()
            )
        # если функция вложенная или метод
        elif s.is_nested() and self.__scope_stack[-1].get_type() == "function":
            func_def.add_parameter(
                Declaration(
                    "context"
                ).set_type(
                    "PyObject"
                ).as_ptr()
            )

        # далее нужно обработать аргументы
        # задекларировать их
        for a in s.get_symbols():
            if a.is_parameter():
                param_decl = Declaration(
                    a.get_name()
                ).set_type("PyObject").as_ptr()

                if symbol_is_static(a, self.__scope_stack[-1]):
                    param_decl.add_modifier("static")

                self.__curr_func_declared.append(param_decl)

        # сигнатура функции
        if len(func.args.args) > 0:
            func_def.add_parameter(
                Declaration(
                    "args"
                ).set_type("PyObject").as_ptr()
            )
        if len(func.args.kwonlyargs) > 0:
            if len(func_def.get_parameters()) == 0:
                func_def.add_parameter(
                    Declaration(
                        "args"
                    ).set_type("PyObject").as_ptr()
                )
            func_def.add_parameter(
                Declaration(
                    "kwargs"
                ).set_type("PyObject").as_ptr()
            )
        # попытка инициализации аргументов
        # получим строку форматирования для PyArg_ParseTupleAndKeywords

        # добавляем декларацию в общий список
        self.__func_decls.append(func_def)
        # устанавливаем контекст текущей функции
        self.__scope_stack.append(s)
        # создаем блок имплементации
        func_impl = FuncImpl(func_def)
        # попытка инициализации аргументов
        # получим строку форматирования для PyArg_ParseTupleAndKeywords

        # теперь приступаем к обработки тела функции
        for i in func.body:
            if isinstance(i, ast.Assign):
                func_impl.add_impl_node_block(self._translate_assign(i))
        # добавляем в список реализацию
        self.__func_impls[func_def.get_name()] = func_impl
        # снимаем контекст
        self.__scope_stack.pop(-1)
        return func_def

    # TODO: трансляция регулярной функции
    def _translate_module_def_func(self):
        pass

    # TODO: трансляция вложенной функции
    def _translate_nested_def_func(self):
        pass

    # TODO: трансляция именованного генератора
    def _translate_generator_def_func(self):
        pass

    # трансляция присваивания
    # возвращает список IL нод
    def _translate_assign(self, a: ast.Assign) -> list:
        # готовый код
        il_code = list()
        # добавим информацию о транслируемой строке
        il_code.append(
            LineComment(
                f"\tBegin(line: {a.lineno}, pos: {a.col_offset}) --> {self.__source_code[a.lineno - 1].strip()}"
            )
        )

        # начинаем трансляцию
        # какие бывают варианты:
        # 1) a, b = 1, 2 (множественное)
        # 2) a = 10 (простое присваивание)
        # 3) a.b = 10 (установка аттрибута)

        target = a.targets[0]
        value = a.value
        # случай, когда нужно присвоить значение переменной
        if isinstance(target, ast.Name):
            il_code.extend(self._translate_assign_to_variable(target, value))

        # информируем о том, какая инструкция завершена
        il_code.append(
            LineComment(
                f"\tEnd(line: {a.lineno}, pos: {a.col_offset}) --> {self.__source_code[a.lineno - 1].strip()}"
            )
        )
        # возвращаем собранный код
        return il_code

    # простое присваиваиние переменной (проверка на глобальность и т.д)
    def _translate_assign_to_variable(self, target: ast.Name, value: ast.AST) -> list:
        code_list = list()
        # получим символ переменной
        var_sym = None
        for s in self.__scope_stack[-1].get_symbols():
            if s.get_name() == target.id:
                var_sym = s
        # проверяем, задекларирована переменная или нет
        if not var_sym.get_name() in self.__curr_func_declared:
            # значит тут декларация с инициализацией
            # но что делать зависит от правой части присваивания
            var_decl = Declaration(
                var_sym.get_name()
            ).set_type("PyObject").as_ptr()
            # смотрим что стоит справа
            # если просто число
            if isinstance(value, ast.Num):
                var_decl.set_initializer(ASTToILMapper.get_num_value(value))
            # если строка
            elif isinstance(value, ast.Str):
                var_decl.set_initializer(ASTToILMapper.get_str_value(value))
            # если аттрибут
            elif isinstance(value, ast.Attribute):
                # получаем код выборки аттрибута
                # это список IL узлов
                # полсдений узел - If
                # в его true body происходит присваивание
                hh = self.__translate_attribute(value, None)
                # то здесь логика уже сложнее
                # var_decl.set_initializer(ASTToILMapper.get_tuple_value(value))
            code_list.append(var_decl)
        else:
            # переменная уже была задекларирована
            # TODO: тут еще стоит учесть что за переменная
            # TODO: ибо может потребоваться разыменование
            pass
        # создаем

        return code_list

    # выборка аттрибута из объекта
    # возвращает If() узел
    # чтобы вызывающий код мог управлять
    # поведением в случае, если аттрибут не найден
    def __translate_attribute(self, attr: ast.Attribute, prev_il_code: list) -> list:
        if prev_il_code is None:
            prev_il_code = list()
        # get_attr_node = If()
        if isinstance(attr.value, ast.Attribute):
            # сначала собираем цепочку
            self.__translate_attribute(attr.value, prev_il_code)
            get_attr_call = Call(
                "PyObject_GetAttrString"
            ).add_parameter(
                Value(get_attr_name(attr.value))
            ).add_parameter(
                Value(attr.attr).as_str()
            )
            attr_name = get_attr_name(attr)
            attr_decl = self.__declare_var(attr_name, get_attr_call)

            if attr_decl is None:
                attr_decl = Assign().set_left(
                    Value(attr_name)
                ).set_right(
                    get_attr_call
                )

            get_attr_node = If(
                    Compare("!=").set_left(
                        Value(attr_name)
                    ).set_right(Value("NULL"))
                )

            if len(prev_il_code) == 0:
                prev_il_code.append(attr_decl)
                prev_il_code.append(get_attr_node)
            else:
                prev_il_code[-1].add_true_statement(attr_decl)
                prev_il_code[-1].add_true_statement(get_attr_node)

        else:
            # декларируем имя аттрибута
            attr_name = get_attr_name(attr)
            # выбираем аттрибут у какой-либо сущности
            # для начала поймем что за сущность
            # имя, строка или результат вызова
            if isinstance(attr.value, ast.Name):
                get_attr_call = Call(
                    "PyObject_GetAttrString"
                ).add_parameter(
                    Value(attr.value)
                ).add_parameter(
                    Value(attr.attr).as_str()
                )
                attr_decl = self.__declare_var(attr_name, get_attr_call)
                if attr_decl is None:
                    attr_decl = Assign().set_left(
                        Value(attr_name)
                    ).set_right(
                        get_attr_call
                    )
                get_attr_node = If(
                    Compare("!=").set_left(
                        Value(attr_name)
                    ).set_right(Value("NULL"))
                )
                if len(prev_il_code) == 0:
                    prev_il_code.append(attr_decl)
                    prev_il_code.append(get_attr_node)
                else:
                    prev_il_code[-1].add_true_statement(attr_decl)
                    prev_il_code[-1].add_true_statement(get_attr_node)
            elif isinstance(attr.value, ast.Call):
                pass
            elif isinstance(attr.value, ast.Str):
                pass
        return prev_il_code

    # декларирует если нужно переменную с именем sym_name
    # и возвращает код ее инициализации
    # если переменная уже задекларирована, то возвращает None
    def __declare_var(self, sym_name: str, default_value: Node = None) -> Node:
        if sym_name not in self.__curr_func_declared:
            self.__curr_func_declared.append(sym_name)
            var_decl_node = Declaration(
                sym_name
            ).set_type("PyObject").as_ptr()
            if default_value is not None:
                var_decl_node.set_initializer(
                    default_value
                )
            else:
                var_decl_node.set_initializer(
                    Value("NULL")
                )

            return var_decl_node
        else:
            return None
