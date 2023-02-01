from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import re
import requests
import string


class AbstractIndex(ABC):
    def __init__(self, urls=None) -> None:
        self.index = dict()
        self.urls = urls
        self.visited_urls = {}

    def download_url(self, url):
        return requests.get(url).text

    def get_text_from_url(self, url):
        html = self.download_url(url=url)
        soup = BeautifulSoup(html, 'html.parser')
        raw_text = ''
        for paragraph in soup.find_all('p'):
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
        return ''.join(' ' if char in string.punctuation else char for char in text).lower().strip('').split(sep=" ")

    @abstractmethod
    def create_index(self, doc_id, tokens):
        pass

    def metadata(self):
        pass
