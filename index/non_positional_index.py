from index.abstract_index import AbstractIndex
from index.utils import Utils
from collections import Counter
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class NonPositionalIndex(AbstractIndex):
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
        '''
        Build the non positional index for all URLs
        '''
        for doc_id, url in enumerate(self.urls):
            text = self.get_text_from_url(url=url)
            if text:
                self.visited_urls.append(url)
                self.nb_visited_urls += 1
                tokens = self.tokenize(text=text)
                tokens_count = Counter(tokens)
                index = self.get_index()
                for token in tokens_count:
                    if token not in index.keys():
                        index[token] = [
                            {'doc_id': doc_id, 'count': tokens_count[token]}]
                    else:
                        index[token].append(
                            {'doc_id': doc_id, 'count': tokens_count[token]})
            else:
                self.failed_urls.append(url)
                self.nb_failed_urls += 1

    def run(self, sort=True):
        '''
        Process the indexing by building the index.
        This method prints some information (logs, statistics) if the user requests it.
        Eventually, the results (index and metadata) are written in two separate documents

        Parameters
        ----------
        sort: boolean
            Should the index be sorted by key?
        '''
        self.create_index()
        index = self.get_index()
        if sort:
            index = dict(sorted(index.items()))

        if self.print_metadata:
            print(
                "\n------------------------------------------------------------------------------------")
            print(
                "------------------------------- NON POSITIONAL INDEX -------------------------------")
            print(
                "------------------------------------------------------------------------------------\n")
            print(self.get_statistics())
            print()
            print(self.get_metadata())
        metadata = self.export_metadata()
        utils = Utils()
        utils.write_index(
            index=index,
            is_positional=False,
            index_type=self.type,
            use_stemmer=self.use_stemmer
        )
        utils.write_metadata(
            metadata=metadata,
            is_positional=False,
            index_type=self.type,
            use_stemmer=self.use_stemmer
        )
