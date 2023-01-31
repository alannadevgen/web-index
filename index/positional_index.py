from index.abstract_index import AbstractIndex


class PositionalIndex(AbstractIndex):
    def __init__(self, documents=None) -> None:
        super().__init__(documents)

    def create_index(self, doc_id, tokens):
        pass