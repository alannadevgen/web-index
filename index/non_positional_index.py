from abstract_index import AbstractIndex
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
                tokens_count = Counter(tokens)
                for token in tokens_count:
                    if token not in self.index.keys():
                        self.index[token] = [
                            {'doc_id': doc_id, 'count': tokens_count[token]}]
                    else:
                        self.index[token].append(
                            {'doc_id': doc_id, 'count': tokens_count[token]})
            else:
                self.failed_urls.append(url)
                self.nb_failed_urls += 1
                logging.warning(f'Failed to reach {url}')

    def get_metadata(self):
        return super().get_metadata()

    def run(self):
        self.create_index()
        print(self.index)
        print()
        print(self.get_metadata())
        print()
        print(self.get_status())

