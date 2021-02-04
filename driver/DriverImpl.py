from driver import IDriver
from translator import ITranslator
from codegen import ICodeGen
import ast
import hashlib
import symtable


class DriverImpl(IDriver):

    def __init__(self, conv: ITranslator, codegen: ICodeGen):
        self.__translator = conv
        self.__generator = codegen

    def translate(self, file_name: str) -> str:

        # get full info about source file
        source_file_info = {
            "file_name": file_name
        }

        with open(file_name, 'rb') as f:
            buff = f.read()
            source_file_info["hash"] = hashlib.md5(buff).hexdigest()

        source_code = buff.decode("utf-8")
        source_file_info["module_ast"] = ast.parse(source_code, file_name)
        source_file_info["sym_table"] = symtable.symtable(source_code, file_name, "exec")
        source_file_info["source_code"] = source_code.splitlines()
        return self.__generator.generate(self.__translator.translate(source_file_info))
