# класс содержит информацию о переменной функции

IS_PARAMETER = 1
IS_LOCAL = 2
IS_STATIC = 4


class VariableInfo:
    def __init__(self, name: str):
        self.__name = name
        self.__is_declared = False
        self.__ref_cnt = 0
        self.__type = 0
        self.__is_initialized = False

    def get_name(self) -> str:
        return self.__name

    def is_declared(self) -> bool:
        return self.__is_declared

    def as_declared(self):
        self.__is_declared = True
        return

    def inc_ref(self):
        self.__ref_cnt += 1
        return self

    def dec_ref(self):
        self.__ref_cnt -= 1
        if self.__ref_cnt < 0:
            raise RuntimeError(f"{self} reference counter already is negative")
        return self

    def is_tracked(self) -> bool:
        return True if self.__ref_cnt > 0 else False

    def is_parameter(self) -> bool:
        return True if self.__type & IS_PARAMETER > 0 else False
        # return True if self.__type == IS_PARAMETER else False

    def as_parameter(self):
        self.__type |= IS_PARAMETER
        return self

    def is_local(self) -> bool:
        return True if self.__type & IS_LOCAL > 0 else False
        # return True if self.__type == IS_LOCAL else False

    def as_local(self):
        self.__type |= IS_LOCAL
        return self

    def is_static(self) -> bool:
        return True if self.__type & IS_STATIC > 0 else False
        # return True if self.__type == IS_STATIC else False

    def as_static(self):
        self.__type |= IS_STATIC
        return self

    def is_initialized(self) -> bool:
        return self.__is_initialized

    def as_initialized(self):
        self.__is_initialized = True
        return self

