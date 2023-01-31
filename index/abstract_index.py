from bs4 import BeautifulSoup
import re
import requests
from abc import ABC, abstractmethod

class AbstractIndex(ABC):
    def __init__(self, documents=None) -> None:
        self.index = dict()
        self.documents = documents

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
        # delete all strings that are not letters or numbers
        text = re.sub(r"(?i)^(?:(?![×Þß÷þø])[-'0-9a-zÀ-ÿ])+$", "", text)
        # remove numbers in between brackets and punctuation in the string
        my_punct = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '.',
                    '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_',
                    '`', '{', '|', '}', '~', '»', '«', '“', '”', '\t', '\n']
        text = re.sub("\[.*?\]|[" + re.escape("".join(my_punct)) + "]", "", text)
        text = re.sub(r"'| - ", " ", text)
        # lowercase, remove leading and trailing whitespace and split the string
        return text.lower().strip().split()

    @abstractmethod
    def create_index(self, doc_id, tokens):
        pass

    def metadata(self):
        pass

