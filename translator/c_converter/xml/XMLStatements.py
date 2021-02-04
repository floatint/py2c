# класс для генерации сложных xml-конструкций

import ast
from xml.etree import ElementTree as et
from .XMLNodes import XMLNodes


class XMLStatements:

    # генерация кода по выборке аргументов
    @staticmethod
    def parse_args(args: ast.arguments) -> et.Element:

        # соберем строку для выполнения PyArg_ParseTupleAndKeywords()
        fmt = ""
        positional_cnt = len(args.args) - len(args.defaults)
        optional_cnt = len(args.defaults)
        kwargs_cnt = len(args.kwonlyargs)

        for i in range(positional_cnt):
            fmt += "O"
        if optional_cnt > 0 or kwargs_cnt > 0:
            fmt += "|"
            if optional_cnt > 0:
                for i in range(optional_cnt):
                    fmt += "O"
            if kwargs_cnt > 0:
                fmt += "$"
                for i in range(kwargs_cnt):
                    fmt += "O"

        return et.Element("NONE")

    @staticmethod
    def call(name: str, args: [et.Element]) -> et.Element:
        call_node = et.Element("call")
        call_node.set("name", name)
        for a in args:
            call_node.append(a)

        return call_node

    @staticmethod
    def safe_call():
        pass