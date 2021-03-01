# Базовый класс исключений


class SourceError(Exception):

    def __init__(self, line, pos, message):
        self.__line = line
        self.__pos = pos
        self.__message = message

    def __str__(self):
        return f"line: {self.__line}, pos: {self.__pos} -> {self.__message}"
