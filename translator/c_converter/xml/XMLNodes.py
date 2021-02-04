#   Класс для генерации базовых xml-блоков

from xml.etree import ElementTree as et


class XMLNodes:

    # root block
    @staticmethod
    def module_node(name: str, lang: str) -> et.Element:
        module_node = et.Element("module")
        module_node.set("name", name)
        module_node.set("lang", lang)
        return module_node

    # include directive
    @staticmethod
    def include_node(file_name: str, is_global: bool) -> et.Element:
        include_node = et.Element("include")
        include_node.set("file_name", file_name)
        include_node.set("is_global", str(is_global))
        return include_node

    # new line
    @staticmethod
    def newline_node() -> et.Element:
        newline_node = et.Element("newline")
        return newline_node

    # line comment
    @staticmethod
    def line_comment_node(text: str) -> et.Element:
        line_comment_node = et.Element("line-comment")
        line_comment_node.text = text
        return line_comment_node

    # block comment
    @staticmethod
    def block_comment_node(text: str) -> et.Element:
        block_comment_node = et.Element("block-comment")
        block_comment_node.text = text
        return block_comment_node

    @staticmethod
    def def_node(name: str, ret_type: str, args: str, kwargs: str, body: [] = None) -> et.Element:
        def_node = et.Element("def")
        def_node.set("name", name)
        if args is not None:
            def_node.set("args", args)
        if kwargs is not None:
            def_node.set("kwargs", kwargs)
        def_node.set("return", ret_type)

        # проверяем, есть ли тело
        if body:
            body_node = XMLNodes.block_node(';', True)
            body_node.extend(body)
            def_node.append(body_node)
        return def_node

    @staticmethod
    def declaration_node(name: str, type: str, **opt) -> et.Element:
        declaration_node = et.Element("declaration")
        declaration_node.set("name", name)
        declaration_node.set("type", type)
        # optional info
        if "static" in opt:
            declaration_node.set("static", str(opt["static"]))
        if "sub_type" in opt:
            declaration_node.set("sub_type", str(opt["sub_type"]))
        return declaration_node

    # TODO: добавить множество вариантов форматирования
    # разделитель между дочерними элементами
    # начинать ли с новой строки
    @staticmethod
    def block_node(separator: str, with_newline: bool) -> et.Element:
        block_node = et.Element("block")
        block_node.set("separator", separator)
        block_node.set("with_newline", str(with_newline))
        return block_node

    @staticmethod
    def arg_node(val: str, as_: str = "") -> et.Element:
        arg_node = et.Element("arg")
        if as_ == "&":
            arg_node.set("as_ref", str(True))
        elif as_ == "*":
            arg_node.set("as_ptr", str(True))
        arg_node.text = val
        return arg_node

    @staticmethod
    def assign_node(target: str) -> et.Element:
        pass

    @staticmethod
    def value_node(val: str) -> et.Element:
        val_node = et.Element("value")
        val_node.text = val
        return val_node

    @staticmethod
    def if_node() -> et.Element:
        if_node = et.Element("if")
        return if_node

    @staticmethod
    def condition_node() -> et.Element:
        condition_node = et.Element("condition")
        return condition_node

    @staticmethod
    def true_body_node() -> et.Element:
        true_body_node = et.Element("true-body")
        return true_body_node

    @staticmethod
    def else_body_node() -> et.Element:
        else_body_node = et.Element("else-body")
        return else_body_node


