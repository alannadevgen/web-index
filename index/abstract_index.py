from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import logging
import re
import requests
import string


class AbstractIndex(ABC):
    def __init__(self, index={}, urls=None, delete_stopwords=False) -> None:
        self.index = index
        self.urls = urls
        self.tokens = []
        self.nb_tokens = 0
        self.nb_documents = len(self.urls)
        self.visited_urls = []
        self.nb_visited_urls = 0
        self.failed_urls = []
        self.nb_failed_urls = 0
        if delete_stopwords == True:
            self.stopwords = stopwords.words('french')
        else:
            self.stopwords = None

    def download_url(self, url):
        try:
            req = requests.get(url)
            if req.status_code == 200:
                return req.text
            else:
                return None
        except Exception:
            logging.warning(f'Failed to reach {url}')

    def get_text_from_url(self, url):
        html = self.download_url(url=url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            raw_text = ''
            for paragraph in soup.find_all([f'h{i}' for i in range(1, 7)]):
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
        text = re.sub(r"(?i)^(?:(?![×Þß÷þø])[-'0-9a-zÀ-ÿ])+$", "", text)
        text = re.sub(r"’|…", " ", text)
        tokens = ''.join(
            ' ' if char in string.punctuation else char for char in text).lower().strip('').split()
        # compute some statistics
        for token in tokens:
            if token not in self.tokens:
                self.tokens.append(token)
                self.nb_tokens += 1
        # delete stopwords
        if self.stopwords:
            tokens = [token for token in tokens if not token.lower()
                      in self.stopwords]
        return tokens

    @abstractmethod
    def create_index(self, doc_id, tokens):
        pass

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
        )
