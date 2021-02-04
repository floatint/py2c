from .il import Node


class ITranslator:

    def translate(self, source_info: {}) -> Node:
        raise NotImplementedError('')
