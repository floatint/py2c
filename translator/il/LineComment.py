from .Comment import Comment


class LineComment(Comment):
    def __init__(self, text: str):
        super().__init__(text)
