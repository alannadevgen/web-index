from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import logging
import re
import requests
import string

TYPES = {
    "title": 'title',
    "header": [f'h{i}' for i in range(1, 7)],
    "paragraph": 'p'
}


class AbstractIndex(ABC):
    def __init__(
            self,
            index={},
            urls=None,
            type: str = "title",
            print_logs=False,
            print_metadata=False,
            delete_stopwords=False,
            use_stemmer=False
    ) -> None:
        self.__index = index
        self.urls = urls
        self.tokens = []
        self.nb_tokens = 0
        self.nb_documents = len(self.urls)
        self.visited_urls = []
        self.nb_visited_urls = 0
        self.failed_urls = []
        self.nb_failed_urls = 0
        self.type = type
        self.print_logs = print_logs
        self.print_metadata = print_metadata
        self.stopwords = stopwords.words('french') if delete_stopwords else None
        self.use_stemmer = use_stemmer
        self.stemmer = SnowballStemmer('french') if use_stemmer else None

    def download_url(self, url):
        try:
            req = requests.get(url)
            if req.status_code == 200:
                if self.print_logs:
                    logging.info(f'Getting URL {url}')
                return req.text
            else:
                return None
        except Exception:
            if self.print_logs:
                logging.warning(f'Failed to reach {url}')

    def get_text_from_url(self, url):
        html = self.download_url(url=url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            raw_text = ''
            for paragraph in soup.find_all(TYPES[self.type]):
                raw_text += " " + paragraph.text
            return raw_text

    def tokenize(self, text):
        """
        In order to tokenize the text we need to:
            - Delete all strings that are not letters or numbers and punctuation in the string
            - Lowercase, remove leading and trailing whitespace and split the string

        Returns
        -------
            list: list of tokens
        """
        # keep all letters (accents included)
        text = re.sub(r"(?i)^(?:(?![×Þß÷þø])[-'0-9a-zÀ-ÿ])+$", "", text)
        # replace anormal punctuation by a whitespace
        text = re.sub(r"’|…", " ", text)
        # delete punctuation and numbers then lowercase and delete trailing whitespaces then split string
        tokens = ''.join(
            ' ' if char in string.punctuation or char.isdigit() else char for char in text
        ).lower().strip('').split()
        # compute some statistics
        for token in tokens:
            if token not in self.tokens:
                self.tokens.append(token)
                self.nb_tokens += 1
        # delete stopwords
        if self.stopwords:
            tokens = [token for token in tokens if not token.lower()
                      in self.stopwords]
        # stem tokens
        if self.stemmer is not None:
            tokens = [self.stemmer.stem(token) for token in tokens]

        return tokens

    @abstractmethod
    def create_index(self, doc_id, tokens):
        pass

    def get_index(self):
        return self.__index

    def get_statistics(self):
        return (
            f"------ Statistics ------\n"
            f"Number of documents: {self.nb_documents}\n"
            f"Number of tokens: {self.nb_tokens}\n"
            f"Mean number of tokens per document: {round(self.nb_tokens/self.nb_documents)}\n"
        )

    def get_metadata(self):
        return (
            f"------- Metadata -------\n"
            f"Number of URLs visited: {self.nb_visited_urls}\n"
            f"Number of failed URLs: {self.nb_failed_urls}\n"
            f"Total number of  URLs: {self.nb_visited_urls + self.nb_failed_urls}"
        )

    def export_metadata(self):
        metadata = {
            "nb_documents": self.nb_documents,
            "nb_tokens": self.nb_tokens,
            "mean_nb_tokens_per_document": round(self.nb_tokens/self.nb_documents),
            "nb_visited_urls": self.nb_visited_urls,
            "nb_failed_urls": self.nb_failed_urls,
            "nb_total_urls": self.nb_visited_urls + self.nb_failed_urls
        }
        return metadata
    
    @abstractmethod
    def run(self):
        pass
