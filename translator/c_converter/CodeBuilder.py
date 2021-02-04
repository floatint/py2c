import ast
import symtable
from xml.etree import ElementTree as et

from .xml.XMLNodes import XMLNodes
from .xml.XMLStatements import XMLStatements
from .Utils import Utils

# TODO: check

module_info = {

}

# по этой информации можно построить
# сигнатуру функции, ее PyMethodDef, и др
func_info = {
    # разрешенное имя
    "resolved_name": "top$sub",
    # тип функции (имя первого аргумента)
    # global - глобальная функция
    # local - вложенная функция
    # method - метод
    "type": "global",
    # имя объекта со всеми параметрами
    "vararg": "args",
    # имя кейвордных параметров
    "kwarg": "kwargs",
    # документация
    "doc": "This function converted from pure Python to pure C",
    # сгенерированный код
    "code_dom": None,
    
    # Дальше поля относятся к методам классов
    # Имя класса, которому принадлежит метод
    "class_name": None,
    # Статичный ли метод
    "is_static": False,
    # свойство ли
    "is_property": False
}

class CodeBuilder:

    def __init__(self, source_info: {}):
        self._mod_ast = source_info["module_ast"]
        self._sym_tbl = source_info["sym_table"]
        self._source_code = source_info["source_code"]
        # стек областей видимости
        self._scope_stack = list()
        # самый первый - модуль, он же глобал
        self._scope_stack.append(self._sym_tbl)

        # сопоставление (parent_sym_table, symbol) -> {}
        self._defs_info = dict()

    # корневой метод генерации кода
    def build(self) -> [et.Element]:
        # проход по модулю
        for s in self._mod_ast.body:
            self._dispatch(s)
        # тут уже мы получили всю необходимую информацию
        # сначала опищем forward declaration
        # потом тела всех функций
        # также допишем процедуру инициализации модуля
        code_dom = list()
        for i in self._scope_stack[-1].get_children():
                # выберем информацию о функции
                def_info = self._defs_info[(self._scope_stack[-1], i)]
                def_name = def_info["resolved_name"]
                def_ret_type = "PyObject*"
                def_vararg = def_info["vararg"]
                def_kwarg = def_info["kwarg"]
                # пишем forward declaration функции
                # пояснительный комментарий
                def_comment = XMLNodes.line_comment_node()
                code_dom.append(XMLNodes.line_comment_node(self._source_code[i.get_lineno() - 1]))
                def_node = XMLNodes.def_node(def_name, def_ret_type, def_vararg, def_kwarg)
                code_dom.append(def_node)
                #code_dom.extend(self._defs_info[(self._scope_stack[-1], i)]["code_dom"])

        return code_dom

    # диспетчеризация для ast
    def _dispatch(self, node: ast.AST):
        # если объявление функции
        if isinstance(node, ast.FunctionDef):
            # найдем ее таблицу символов
            func_sym_tbl = None
            for i in self._scope_stack[-1].get_children():
                if i.get_name() == node.name:
                    func_sym_tbl = i
            # отдаем на обработку
            self._process_def(node, func_sym_tbl)

    # обработка функции
    def _process_def(self, func: ast.FunctionDef, sym: symtable.Function):
        # сначала получим описание функции
        def_info = dict()
        # разрешенное имя (с учетом неймспейсов)
        def_info["resolved_name"] = self._resolve_name(sym)
        # определяем тип функции
        if sym.is_nested():
            # если функция вложенная, а пред неймспейс - класс
            if self._scope_stack[-1].get_type() == "class":
                def_info["type"] = "method"
            else:
                def_info["type"] = "local"
        else:
            def_info["type"] = "global"
        # смотрим параметры
        params = sym.get_parameters()
        if len(params) != 0:
            # если есть параметры

            # если есть vararg
            if func.args.vararg:
                def_info["vararg"] = func.args.vararg.arg
            else:
                # если позиционные параметры
                # по умолчанию
                def_info["vararg"] = "args"

            if func.args.kwarg:
                def_info["kwarg"] = func.args.kwarg
            elif len(func.args.kwonlyargs) > 0:
                def_info["kwarg"] = "kwargs"
            else:
                def_info["kwarg"] = None

        else:
            # если параметров нет
            def_info["vararg"] = None
            def_info["kwarg"] = None

        # теперь нужно сгенерировать код

        # кладем на вершину стека неймспейс
        self._scope_stack.append(sym)
        # получаем список блоков кода
        def_info["code_dom"] = self._build_def(def_info, func)
        # снимаем с вершины стека неймспейс
        self._scope_stack.pop(-1)
        # помещаем всю информацию в хранилище
        self._defs_info[(self._scope_stack[-1], sym)] = def_info

    # разрешение имени функции
    def _resolve_name(self, sym: symtable.Function) -> str:
        resolved_name = ""
        for i in self._scope_stack:
            resolved_name += i.get_name() + "$"
        # докидываем имя функции
        resolved_name += sym.get_name()
        return resolved_name

    # сборка тела функции
    # считаем, что мы находимся в неймспейсе этой функции
    def _build_def(self, def_info: {}, func: ast.FunctionDef) -> [et.Element]:

        # модель кода
        code_dom = list()

        # выберем текущий контекст
        curr_scope = self._scope_stack[-1]

        # загружаем имена. сначала аргументы

        # если параметры есть
        if def_info["vararg"] or def_info["kwarg"]:
            # декларирем их
            for i in curr_scope.get_parameters():
                code_dom.append(XMLNodes.declaration_node(i, "PyObject", sub_type="*"))
            code_dom.append(XMLNodes.newline_node())
            # попробуем распарсить их

            # получим строку для парсинга
            args_fmt = self._get_args_format(func.args)


        # инициализируем глобальные имена

        return code_dom

    # собирает строку формата для парсинга кортежей
    def _get_args_format(self, args: ast.arguments) -> str:
        return ""