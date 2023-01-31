from index.abstract_index import AbstractIndex

class NonPositionalIndex(AbstractIndex):
    def __init__(self, documents=None) -> None:
        super().__init__(documents)

    
    def create_index(self, doc_id, tokens):
        appeared_words = dict()
        # compute the frequency by token
        for token in tokens:
            token_frequency = appeared_words[token] if token in appeared_words else 0
            appeared_words[token] = token_frequency + 1
        # print(appeared_words, '\n\n\n')

        # update the inverted index for each token
        update_dict = {
            key: appearance
            if key not in self.index
            else self.index[key] + [appearance]
            for (key, appearance) in appeared_words.items()
        }
        # sort the tokens by appearance
        update_dict = sorted(update_dict.items(), key=lambda kv: kv[1], reverse=True)
        # update the index
        self.index.update(update_dict)