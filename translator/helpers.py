# набор вспомогательных функций
import ast
import symtable

from .il.LineComment import LineComment
from .il.Node import Node

# системные имена некоторых переменных
MODULE_CONTEXT_NAME = "module$$"
CLASS_CONTEXT_NAME = "self$$"
FUNCTION_CONTEXT_NAME = "context$$"
ARGS_VAR_NAME = "args$$"
KWARGS_VAR_NAME = "kwargs$$"


# манглинг имен
def get_mangled_name(scope_stack: list, name: str) -> str:
    if scope_stack is None:
        return f"{name}$"
    else:
        return "$".join([s.get_name() for s in scope_stack]) + "$" + name


# получить имя аттрибута
def get_attr_name(attr: ast.Attribute) -> str:
    return attr.attr + "$"


# функция генерирует комментарий с пояснением
# какая инструкция начинает транслироваться
def statement_prologue(stmt: ast.AST, source_code: list) -> Node:
    return LineComment(
        f"\tBegin(line: {stmt.lineno}, pos: {stmt.col_offset}) --> {source_code[stmt.lineno - 1].strip()}"
    )


# функция генерирует комментарий с пояснением
# какая инструкция окончила трансляцию
def statement_epilogue(stmt: ast.AST, source_code: list) -> Node:
    return LineComment(
        f"\tEnd(line: {stmt.lineno}, pos: {stmt.col_offset}) --> {source_code[stmt.lineno - 1].strip()}"
    )


# определяет, нужно ли символ помечать как статический
# чтобы была возможность манипулировать им из вложенных блоков
# на входе символ который нужно проверить и таблица, в которой он определен
def symbol_is_static(s: symtable.Symbol, table: symtable.SymbolTable) -> bool:
    # получаем вложенные функции
    inner_scops = table.get_children()
    # если они есть
    if len(inner_scops) > 0:
        for i in inner_scops:
            return symbol_is_static(s, i)
    else:
        # если вложенных функций нет
        # получаем все символы
        scope_symbols = table.get_symbols()
        for i in scope_symbols:
            if i.is_free() and s.get_name() == i.get_name():
                return True

    return False
