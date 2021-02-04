# базовый класс для единицы промежуточного кода
# любой потомок этого класс не проихводит никаки вычислений
# только сериализует/десериализует в различные представления
# для генерации кода другими инструментами
# Однако код на Си можно получить и из вот таких Node


class Node:

    def serialize(self, serializer: ISerializer) -> object:
        raise NotImplementedError()

    @staticmethod
    def deserialize(deserializer: IDeserializer):
        raise NotImplementedError()
