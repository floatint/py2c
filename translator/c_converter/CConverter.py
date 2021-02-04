from translator import ITranslator
from pathlib import Path
from xml.etree import ElementTree as et
from .xml import XMLNodes
import datetime as dt

from .CodeBuilder import CodeBuilder


class CTranslator(ITranslator):

    def __init__(self):
        self.__code_dom__ = et.Element("module")

    def translate(self, source_info: {}) -> et.Element:
        self.__code_dom__.set("name", Path(source_info["file_name"]).stem)
        self.__code_dom__.set("lang", "C")

        header_comment = XMLNodes.block_comment_node(f"""
            This file was auto-generated from {source_info["file_name"]}
            Hash: {source_info["hash"]}
            Date: {dt.datetime.now()}
""")

        include_python_h = XMLNodes.include_node("Python.h", True)
        include_structmember_h = XMLNodes.include_node("structmember.h", False)

        # add to root
        self.__code_dom__.append(header_comment)
        self.__code_dom__.append(XMLNodes.newline_node())
        self.__code_dom__.append(include_python_h)
        self.__code_dom__.append(include_structmember_h)
        self.__code_dom__.append(XMLNodes.newline_node())

        # get code
        code_nodes = CodeBuilder(source_info).build()
        self.__code_dom__.extend(code_nodes)

        return self.__code_dom__
