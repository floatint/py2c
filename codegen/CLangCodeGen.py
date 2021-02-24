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
            return self._generate_call(n, indent, standalone)
        elif isinstance(n, Declaration):
            return self._generate_declaration(n, indent, standalone)
        elif isinstance(n, Function):
            return self._generate_function(n, standalone)
        # elif isinstance(n, Implementation):
        #     return self._generate_func_impl(n, indent)
        elif isinstance(n, Array):
            return self._generate_array(n, indent, standalone)
        elif isinstance(n, Value):
            return self._generate_value(n)
        elif isinstance(n, FuncDef):
            return self._generate_func_def(n, standalone)
        elif isinstance(n, FuncImpl):
            return self.__generate_func_impl(n, indent)
        elif isinstance(n, LogicNot):
            return self.__generate_logic_not(n, indent)
        elif isinstance(n, If):
            return self.__generate_if(n, indent)
        elif isinstance(n, Return):
            return self.__generate_return(n, indent)
        elif isinstance(n, BitwiseOr):
            return self.__generate_bitwise_or(n)
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
        return self.__get_indent_str(indent) + "//" + "\t" + c.get_text()

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

    def _generate_call(self, c: Call, indent: int, standalone=True) -> str:
        if standalone:
            indent_str = self.__get_indent_str(indent)
        else:
            indent_str = ""
        args = ""
        for (i, v) in enumerate(c.get_parameters()):
            if isinstance(v, Node):
                args += self._dispacth_node(v, 0, False)
            elif isinstance(v, str):
                args += f"\"{str(v)}\""
            else:
                args += str(v)

            if i < len(c.get_parameters()) - 1:
                args += ", "
        # args = ", ".join([self._dispacth_node(i, 0, False) for i in c.get_parameters()])
        return f"{indent_str}{c.get_name()}({args})"

    def _generate_declaration(self, d: Declaration, indent: int, standalone: bool) -> str:
        decl = self.__get_indent_str(indent)
        # собираем модификаторы
        if d.has_modifiers():
            decl += " ".join([i for i in d.get_modifiers()]) + " "

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

    # генерация массива с элементами
    # mode отвечает за стиль генерации
    # mode="compact" - элементы на одной строке
    # mode="full" - каждый элемент с новой строки
    def _generate_array(self, a: Array, indent: int, standalone=True) -> str:
        if standalone:
            indent_str = self.__get_indent_str(indent)
            elements = f",\n{indent_str}".join([self._dispacth_node(i, indent + 1) for i in a.get_elements()])
            return f"{{\n{indent_str}{elements}\n{self.__get_indent_str(indent - 1)}}}"
        else:
            elements = ", ".join([self._dispacth_node(i, indent, False) for i in a.get_elements()])
            return f"{{ {elements} }}"

    def _generate_value(self, v: Value) -> str:
        if v.is_str():
            return f"\"{str(v.get_value())}\""
        elif v.is_ref():
            return f"&{str(v.get_value())}"
        elif v.is_deref():
            deref_str = "".join(["*" for i in range(v.get_deref_depth())])
            return f"{deref_str}{str(v.get_value())}"
        else:
            return f"{str(v.get_value())}"

    def _generate_func_def(self, f: FuncDef, standalone=True) -> str:
        mods = " ".join([i for i in f.get_modifiers()])
        params = ", ".join([self._dispacth_node(i, 0, False) for i in f.get_parameters()])
        if standalone:
            return f"{mods} {f.get_ret_type()} {f.get_name()}({params});".strip(" ")
        else:
            return f"{mods} {f.get_ret_type()} {f.get_name()}({params})".strip(" ")

    def __generate_func_impl(self, func_impl: FuncImpl, indent: int) -> str:
        indent_str = self.__get_indent_str(indent)
        impl = self._dispacth_node(func_impl.get_func_def(), indent, False)
        code_block = ""
        for i in func_impl.get_impl():
            code_block += f"{indent_str}" + self._dispacth_node(i, indent + 1, True) + "\n"
        impl_block = f" {{\n{code_block}\n}};"
        return impl + impl_block

    def __generate_logic_not(self, logic_not: LogicNot, indent: int) -> str:
        return f"!({self._dispacth_node(logic_not.get_value(), indent, False)})"

    def __generate_if(self, if_stmt: If, indent: int) -> str:
        indent_str = self.__get_indent_str(indent)
        cond = self._dispacth_node(if_stmt.get_condition(), indent, False)
        true_body = ""
        for i in if_stmt.get_true_body():
            true_body += f"{self._dispacth_node(i, indent + 1, False)}\n"
        return f"{indent_str}if ({cond}) {{\n{true_body}\n{indent_str}}}"

    def __generate_return(self, ret: Return, indent: int) -> str:
        return f"{self.__get_indent_str(indent)}return {self._dispacth_node(ret.get_value(), indent, False)};"

    def __generate_bitwise_or(self, b_or: BitwiseOr) -> str:
        return f"{self._dispacth_node(b_or.get_left(), 0, False)} | {self._dispacth_node(b_or.get_right(), 0, False)}"
    # для выравнивания кода
    def __get_indent_str(self, n: int) -> str:
        return "".join(["\t" for i in range(n)])
