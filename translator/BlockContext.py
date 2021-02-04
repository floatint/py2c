# Класс содержит имена переменных, которые нужно отслеживать в
# текущем блоке, чтобы освобождать при необходимости
# так же содержит счетчик ссылок для каждой переменной


class BlockContext:

    def get_variables(self) -> dict:
        return None

    def free_variable(self):
        pass

    def add_variable(self):
        pass

    def inc_ref_variable(self):
        pass

    def dec_ref_variable(self):
        pass
