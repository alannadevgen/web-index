from index.abstract_index import AbstractIndex
from index.utils import Utils
from collections import Counter, OrderedDict
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class PositionalIndex(AbstractIndex):
    def __init__(
            self,
            index={},
            urls=None,
            type='title',
            print_logs=False,
            print_metadata=False,
            delete_stopwords=False,
            use_stemmer=False
    ) -> None:
        super().__init__(
            index=index,
            urls=urls,
            type=type,
            print_logs=print_logs,
            print_metadata=print_metadata,
            delete_stopwords=delete_stopwords,
            use_stemmer=use_stemmer
        )

    def create_index(self):
        for doc_id, url in enumerate(self.urls):
            text = self.get_text_from_url(url=url)
            if text:
                self.visited_urls.append(url)
                self.nb_visited_urls += 1
                tokens = self.tokenize(text=text)
                index = self.get_index()

                position = 0

                for token in tokens:
                    if token in index.keys():
                        doc_ids = [index[token][item]['doc_id']
                                   for item in range(len(index[token]))]
                        # token found multiple times in same document
                        if doc_id in doc_ids:
                            for document_index, document in enumerate(index[token]):
                                if index[token][document_index]['doc_id'] == doc_id:
                                    index[token][document_index]['position'].append(
                                        position)
                                    index[token][document_index]['count'] += 1
                        # token found in another document
                        else:
                            index[token].append(
                                {
                                    'doc_id': doc_id,
                                    'position': [position],
                                    'count': 1
                                }
                            )
                    # add new token
                    else:
                        index[token] = [
                            {
                                'doc_id': doc_id,
                                'position': [position],
                                'count': 1
                            }
                        ]
                    # update position in document
                    position += 1
            else:
                self.failed_urls.append(url)
                self.nb_failed_urls += 1

    def get_metadata(self):
        return super().get_metadata()

    def run(self, sort=True):
        self.create_index()
        index = self.get_index()
        if sort:
            index = dict(sorted(index.items()))

        if self.print_metadata:
            print(
                "\n------------------------------------------------------------------------------------")
            print(
                "--------------------------------- POSITIONAL INDEX ---------------------------------")
            print(
                "------------------------------------------------------------------------------------\n")
            print(self.get_statistics())
            print()
            print(self.get_metadata())
        metadata = self.export_metadata()
        utils = Utils()
        utils.write_index(
            index=index,
            is_positional=True,
            index_type=self.type,
            use_stemmer=self.use_stemmer
        )
        utils.write_metadata(
            metadata=metadata,
            is_positional=True,
            index_type=self.type,
            use_stemmer=self.use_stemmer
        )
