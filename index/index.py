from bs4 import BeautifulSoup
import re
import requests


class Index:
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

    def create_inverted_index(self, doc_id, tokens):
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

    def metadata(self):
        pass


if __name__ == "__main__":
    import json
    with open("crawled_urls.json") as json_file:
        json_data = json.loads(json_file.read())

    link = json_data[8]
    # print(link)
    index = Index()
    raw_text = index.get_text_from_url(link)
    tokens = index.tokenize(raw_text)
    # print(raw_text)
    index.create_inverted_index(doc_id=1, tokens=tokens)
    print(index.index)
