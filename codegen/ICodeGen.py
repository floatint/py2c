from translator import il


class ICodeGen:

    def generate(self, il_root: il.Node) -> str:
        raise NotImplementedError()
