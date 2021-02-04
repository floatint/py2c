from translator import ITranslator
from codegen import ICodeGen


class IDriver:
    def translate(self, source_code: str) -> str:
        raise NotImplementedError('Not implemented translate() method')
