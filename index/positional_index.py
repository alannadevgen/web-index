from index.abstract_index import AbstractIndex
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
            delete_stopwords=False
    ) -> None:
        super().__init__(
            index=index,
            urls=urls,
            delete_stopwords=delete_stopwords
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
                    # index[token]['count'] = sum([len(index[token][index_doc]['position']) for index_doc in range(len(index[token]))])

                    position += 1
            else:
                self.failed_urls.append(url)
                self.nb_failed_urls += 1
                # logging.warning(f'Failed to reach {url}')

    def get_metadata(self):
        return super().get_metadata()

    def run(self, sort=True):
        self.create_index()
        index = self.get_index()
        if sort:
            print(dict(sorted(index.items())))
        else:
            print(index)
        print()
        print(self.get_statistics())
        print()
        print(self.get_metadata())
