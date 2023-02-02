# Web index :round_pushpin:

The aim of this project is to create a web index using a file input containing a list of crawled URLs. In order to do this, we used a JSON file `crawled_urls.json` to build our index.

Several options are posible to build the index. It can be based on the title page, the headers or even on the paragraphs, each building a separate index.

Then, the text is split into tokens. Once again, they are multiple options such as deleting stop words (available only for French words) or stem the tokens. Each token is then the starting point for the construction of the index which can be **positional** or **non positional** 

## Quick start

First, you will need to clone the repo.
```bash
git clone https://github.com/alannagenin/web-index.git
cd web-index
```

Then, we will set a virtual environment.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Once everything is set up, we can run the indexing process through the CLI. Multiple options can be used, you can see them through the following command.

```bash
python3 main.py --help
# Usage: main.py [OPTIONS]
#
# Options:
#   --index-data [title|paragraph|header]       Type of data to retreive to create the index.
#   --index-type [non-positional|positional]    Type of index to create.
#   --input-file TEXT                           Path to the list of URLs to index.
#   --print-logs BOOLEAN                        Show the logs for fetching URLs.
#   --print-metadata BOOLEAN                    Show the metadata.
#   --use-stemmer BOOLEAN                       Use the stemmer for the tokens.
#   --help                                      Show this message and exit.
  ```

By default, the values are:
* `--index-data "title"` $\rightarrow$ retreive the titles from URLs
* `--index-type "non-positional"` $\rightarrow$ create a non positional index
* `--input-file "data/crawled_urls.json"` $\rightarrow$ use predefined URL list in the `data` folder
* `--print-logs False` $\rightarrow$ do not print the logs
* `--print-metadata False` $\rightarrow$ do not print the metadata
* `--use-stemmer False` $\rightarrow$ do not use any stemming process

If you wish you can set differents parameters like:

```bash
# default values
python3 main.py
# index build on the headers
python3 main.py --index-data "header"
# index build on the paragraphs
python3 main.py --index-data "paragraph"
# positional index with headers
python3 main.py --index-data "header" --index-type "positional"
# positional index with headers and output logs
python3 main.py --index-data "header" --index-type "positional" --print-logs True
# positional index with headers and output logs and metadata
python3 main.py --index-data "header" --index-type "positional" --print-logs True --print-metadata True
# positional index with headers and output logs and metadata and stemmer
python3 main.py --index-data "header" --index-type "positional" --print-logs True --print-metadata True --use-stemmer True
```

## Contributors

[Alanna DEVLIN-GENIN](https://github.com/alannagenin/)