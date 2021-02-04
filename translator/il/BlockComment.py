from .Comment import Comment


class BlockComment(Comment):
    def __init__(self, text: str):
        super().__init__(text)
