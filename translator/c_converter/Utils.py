import ast
import symtable

class Utils:
    # возвращает развернутую сигнатуру метода
    @staticmethod
    def get_def_signature(namespace: [symtable.SymbolTable], func: ast.FunctionDef) -> str:
        def_name = ""
        for i in namespace:
            if i.get_name() != "top":
                def_name += i.get_name() + "."
        def_name += func.name

        # параметры

        pass

