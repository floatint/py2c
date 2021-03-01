# класс описывает информацию о функции
# по сути ее профиль из которого можно получить
# сигнатуру, список переменных, информацию о них и т.д.
import ast
import symtable
import translator.helpers as hlp
from .VariableInfo import VariableInfo
from translator.il.FuncImpl import FuncImpl, FuncDef
from translator.il.Declaration import Declaration


class FunctionInfo:
    # name - имя функции
    # ast_node - ast узел функции
    # sym_tbl - твблица символов функции
    # scope - стек таблиц символов (вложенность функции). Передавать копию !
    def __init__(self, name: str, ast_node: ast.FunctionDef, sym_tbl: symtable.SymbolTable, scope_stack: list):
        # исходное имя функции
        self.__name = name
        # есть ли аргументы
        self.__has_args = False
        # есть ли "ключевые" аргументы
        self.__has_kwargs = False
        # название контекста
        self.__context = None
        # словарь переменных
        self.__variables = dict()
        # таблица символов функции
        self.__sym_tbl = sym_tbl
        # ast узел
        self.__ast_node = ast_node
        # уровень вложенности
        self.__scope_stack = scope_stack
        # объявление функции
        self.__func_def = self.__generate_func_def()
        # реализация функции
        self.__func_impl = FuncImpl(self.__func_def)
        # список задекларированных переменных (имена)
        self.__declared_vars = list()

        # обработаем переменные функции
        self.__process_symbols()

    def get_name(self) -> str:
        return self.__name

    def get_mangled_name(self) -> str:
        return hlp.get_mangled_name(self.__scope_stack, self.__name)

    def has_args(self) -> bool:
        return self.__has_args

    def has_kwargs(self) -> bool:
        return self.__has_kwargs

    def get_context(self) -> str:
        return self.__context

    def set_context(self, ctx: str):
        self.__context = ctx
        return self

    def get_symbol_table(self) -> symtable.SymbolTable:
        return self.__sym_tbl

    def get_ast_node(self) -> ast.FunctionDef:
        return self.__ast_node

    def get_implementation(self) -> FuncImpl:
        return self.__func_impl

    def set_implementation(self, func_impl: FuncImpl):
        self.__func_impl = func_impl
        return self

    def get_definition(self) -> FuncDef:
        return self.__func_def

    # получить переменную по имени
    def get_variable(self, name: str) -> VariableInfo:
        try:
            return self.__variables[name]
        except KeyError:
            return None

    # зарегистрировать переменную в контексте функции
    def add_variable(self, v: VariableInfo):
        if v.get_name() in self.__variables:
            raise RuntimeError(f"Variable {v.get_name()} already exists in {self} context")
        self.__variables[v.get_name()] = v
        return self

    def get_tracked_variables(self):
        for i in self.__variables:
            var_info = self.__variables[i]
            if var_info.is_tracked():
                yield var_info

    # генерация сигнатуры функции
    def __generate_func_def(self):
        func_def = FuncDef(hlp.get_mangled_name(self.__scope_stack, self.__sym_tbl.get_name()))
        func_def.set_ret_type("PyObject*")
        func_def.add_modifier("static")
        # если функция глобальная (модуль)
        if not self.__sym_tbl.is_nested():
            func_def.add_parameter(
                Declaration(
                    hlp.MODULE_CONTEXT_NAME
                ).set_type(
                    "PyObject"
                ).as_ptr()
            )
        # если функция вложенная или метод
        elif self.__sym_tbl.is_nested() and self.__scope_stack[-1].get_type() == "function":
            func_def.add_parameter(
                Declaration(
                    hlp.FUNCTION_CONTEXT_NAME
                ).set_type(
                    "PyObject"
                ).as_ptr()
            )

        # теперь нужно понять сколько и какие переменные принимает функция
        args = self.__ast_node.args
        if len(args.args) > 0 or args.vararg is not None:
            func_def.add_parameter(
                Declaration(hlp.ARGS_VAR_NAME).set_type("PyObject").as_ptr()
            )

        if len(args.kwonlyargs) > 0 or args.kwarg is not None:
            if len(func_def.get_parameters()) < 2:
                func_def.add_parameter(
                    Declaration(hlp.ARGS_VAR_NAME).set_type("PyObject").as_ptr()
                )
            func_def.add_parameter(
                Declaration(hlp.KWARGS_VAR_NAME).set_type("PyObject").as_ptr()
            )

        return func_def

    # обработка переменных функции
    def __process_symbols(self):
        # проходимся по всем символам
        for s in self.__sym_tbl.get_symbols():
            # если это не вложенная функция или класс
            if not s.is_namespace():
                var_info = VariableInfo(s.get_name())
                if s.is_parameter():
                    var_info.as_parameter()
                if s.is_local():
                    var_info.as_local()
                if hlp.symbol_is_static(s, self.__sym_tbl):
                    var_info.as_static()
                # TODO: неверное определение когда находимся в top level функции
                if s.is_free():
                    var_info.as_static()
                self.__variables[s.get_name()] = var_info
