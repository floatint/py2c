from .ICodeGen import ICodeGen
from translator.il import *


class CLangCodeGen(ICodeGen):

    def generate(self, n: Node) -> str:
        return self._dispacth_node(n, 0, True)

    # принимает единицу кода, уровень вложенности
    # и флаг - самостоятельная единица или к контексте
    def _dispacth_node(self, n: Node, indent: int, standalone=True) -> str:
        if isinstance(n, Module):
            return self._generate_module(n)
        elif isinstance(n, Comment):
            return self._generate_comment(n, indent)
        elif isinstance(n, Include):
            return self._generate_include(n, indent)
        elif isinstance(n, Newline):
            return self._generate_newline(n)
        elif isinstance(n, Call):
            return self._generate_call(n, indent)
        elif isinstance(n, Declaration):
            return self._generate_declaration(n, indent, standalone)
        elif isinstance(n, Function):
            return self._generate_function(n, standalone)
        elif isinstance(n, Implementation):
            return self._generate_func_impl(n, indent)
        elif isinstance(n, Array):
            return self._generate_array(n, indent)
        elif isinstance(n, Value):
            return self._generate_value(n)
        else:
            return ""

    def _generate_module(self, m: Module) -> str:
        res = ""
        for i in m.get_children():
            res += self._dispacth_node(i, 0)
        return res

    def _generate_comment(self, c: Comment, indent: int) -> str:
        if isinstance(c, LineComment):
            return self._generate_line_comment(c, indent)
        elif isinstance(c, BlockComment):
            return self._generate_block_comment(c, indent)
        else:
            return ""
        # return f"/*\n{c.get_text()}\n*/"

    def _generate_line_comment(self, c: LineComment, indent: int) -> str:
        return self.__get_indent_str(indent) + c.get_text()

    def _generate_block_comment(self, c: BlockComment, indent: int) -> str:
        indent_str = self.__get_indent_str(indent)
        comm_text = indent_str + "/*\n"
        for i in c.get_text().splitlines():
            comm_text += f"{indent_str}\t{i}\n"

        comm_text += indent_str + "*/"

        return comm_text

    def _generate_include(self, i: Include, indent: int) -> str:
        indent_str = self.__get_indent_str(indent)
        if i.is_local_import():
            return f"{indent_str}#import \"{i.get_name()}\""
        else:
            return f"{indent_str}#import <{i.get_name()}>"

    def _generate_newline(self, n: Newline) -> str:
        return "\n"

    def _generate_call(self, c: Call, indent: int) -> str:
        indent_str = self.__get_indent_str(indent)
        args = ", ".join([self._dispacth_node(i, 0, False) for i in c.get_parameters()])
        return f"{indent_str}{c.get_name()}({args})"

    def _generate_declaration(self, d: Declaration, indent: int, standalone: bool) -> str:
        decl = self.__get_indent_str(indent)
        # собираем модификаторы
        if d.has_modifiers():
            decl += " ".join([i for i in d.get_modifiers()])

        decl += d.get_type() + " "
        if d.is_ptr():
            for i in range(d.get_ptr_depth()):
                decl += "*"
        if d.is_ref():
            for i in range(d.get_ref_depth()):
                decl += "&"

        decl += d.get_name()
        if d.is_arr():
            for i in range(d.get_arr_depth()):
                decl += "[]"

        # проверяем инициализацию
        if d.has_initializer():
            initializer = self._dispacth_node(d.get_initializer(), indent + 1, False)
            decl += f" = {initializer}"

        if standalone:
            decl += ";"

        return decl

    def _generate_function(self, f: Function, standalone: bool) -> str:
        mods = " ".join([i for i in f.get_modifiers()])
        params = ", ".join([self._dispacth_node(i, 0, False) for i in f.get_parameters()])
        if standalone:
            return f"{mods} {f.get_type()} {f.get_name()}({params});".strip(" ")
        else:
            return f"{mods} {f.get_type()} {f.get_name()}({params})".strip(" ")

    def _generate_func_impl(self, i: Implementation, indent: int) -> str:
        impl = self._dispacth_node(i.get_function(), indent, standalone=False)
        impl = f"{impl} {{\n{self._dispacth_node(i.get_implementation(), indent + 1)}\n}}"

        return impl

    # генерация массива с элементами
    # mode отвечает за стиль генерации
    # mode="compact" - элементы на одной строке
    # mode="full" - каждый элемент с новой строки
    def _generate_array(self, a: Array, indent: int) -> str:
        indent_str = self.__get_indent_str(indent)
        elements = f",\n{indent_str}".join([self._dispacth_node(i, indent + 1) for i in a.get_elements()])
        return f"{{\n{indent_str}{elements}\n{self.__get_indent_str(indent - 1)}}}"

    def _generate_value(self, v: Value) -> str:
        if v.is_str():
            return f"\"{str(v.get_value())}\""
        else:
            return f"{str(v.get_value())}"

    def __get_indent_str(self, n: int) -> str:
        return "".join(["\t" for i in range(n)])
