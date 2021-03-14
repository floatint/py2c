# генератор кусков кода, которые используются в разных частях
from translator.info.VariableInfo import VariableInfo
from translator.il import *


class SharedILTranslator:

    # код очистки ссылок
    @staticmethod
    def cleanup(tracked_vars: list, exclude_list: list) -> list:
        cleanup_code = list()
        for tv in tracked_vars:
            for el in exclude_list:
                if tv.get_name() != el.get_name():
                    cleanup_code.append(
                        Call(
                            "Py_XDECREF"
                        ).add_parameter(
                            Value(tv.get_name())
                        )
                    )
        return cleanup_code
