# набор вспомогательных функций
import ast
import symtable
from .il.Function import Function
from .il.Declaration import Declaration
from .il.LineComment import LineComment


# собирает строку формата для
# PyArgs_ParseTupleAndKeywords()
def get_args_fmt(args: ast.arguments) -> str:
    args_fmt = ""
    pos_args_count = len(args.args) - len(args.defaults)
    optional_args_count = len(args.defaults)
    kw_args_count = len(args.kwonlyargs)
    for i in range(pos_args_count):
        args_fmt += "O"
    if (optional_args_count > 0 or args.vararg) or (kw_args_count > 0 or args.kwarg):
        args_fmt += "|"
        for i in range(optional_args_count):
            args_fmt += "O"
        if kw_args_count > 0 or args.kwarg:
            args_fmt += "$"
        for i in range(kw_args_count):
            args_fmt += "O"

    return args_fmt


# резолв имени
# с учетом вложенности неймспесов
# например: top_outer_inner
def get_resolved_name(scope_stack: [], symbol: symtable.Symbol) -> str:
    return ""


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


# получает декларацию функции
def get_func_declaration(func: ast.FunctionDef, scope_stack: list, src_code: list) -> Function:
    # для начала получим разрешенное имя
    resolved_name = ""
    for i in scope_stack:
        resolved_name += i.get_name() + "$"
    resolved_name += func.name

    func_decl_comment = f"line: {func.lineno}, pos: {func.col_offset} |--> {src_code[func.lineno - 1]}"

    func_decl = Function(
        resolved_name
    ).set_type(
        "PyObject"
    ).set_comment(
        LineComment(func_decl_comment)
    ).add_modifier(
        "static"
    )

    # далее определяем параметры
    # функция принимает минимум 1 параметр, а что в нем, зависит от контекста
    func_sym = list(filter(lambda x: x.get_name() == func.name, scope_stack[-1].get_children()))[0]
    if not func_sym.is_nested() and scope_stack[-1].get_type() == "module":
        func_decl.add_parameter(Declaration(
            "module"
        ).set_type("PyObject").as_ptr())
    elif func_sym.is_nested() and scope_stack[-1].get_type() == "class":
        func_decl.add_parameter(Declaration(
            "self"
        ).set_type("PyObject").as_ptr())
    elif func_sym.is_nested() and scope_stack[-1].get_type() == "function":
        func_decl.add_parameter(Declaration(
            "context"
        ).set_type("PyObject").as_ptr())
    else:
        raise ValueError("Couldn't determine first parameter")

    # дальше смотрим список параметров
    if len(func.args.args) > 0 or func.args.vararg:
        func_decl.add_parameter(Declaration(
            "args"
        ).set_type("PyObject").as_ptr())

    if len(func.args.kwonlyargs) > 0 or func.args.kwarg:
        func_decl.add_parameter(Declaration(
            "kwargs"
        ).set_type("PyObject").as_ptr())

    return func_decl
