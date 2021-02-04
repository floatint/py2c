# класс содержит информацию о переменной


class VariableInfo:
    def __init__(self):
        self.__is_declared = False
        self.__ref_cnt = 0
        self.__lifetime = 0  # 0 - local, 1 - static (for extern vars)

    def is_declared(self) -> bool:
        return self.__is_declared

    # for debug ?
    def inc_ref_count(self):
        self.__ref_cnt += 1

    def dec_ref_count(self):
        self.__ref_cnt -= 1

    def is_referenced(self) -> bool:
        return True if self.__ref_cnt > 0 else False

    def is_static(self) -> bool:
        return True if self.__lifetime == 1 else False
