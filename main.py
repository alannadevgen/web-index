from index.utils import Utils
from index.non_positional_index import NonPositionalIndex
from index.positional_index import PositionalIndex
import os
import click


@click.command()
@click.option('--index-data', default="title", help='Type of data to retreive to create the index.', type=click.Choice(['title', 'paragraph', 'header'], case_sensitive=True), nargs=1)
@click.option('--index-type', default="non-positional", help='Type of index to create.', type=click.Choice(['non-positional', 'positional'], case_sensitive=True), nargs=1)
@click.option('--input-file', default="data/crawled_urls.json", help='Path to the list of URLs to index.', type=str, nargs=1)
@click.option('--print-logs', default=False, help='Show the logs for fetching URLs.', type=bool)
@click.option('--print-metadata', default=False, help='Show the metadata.', type=bool)
@click.option('--use-stemmer', default=False, help='Use the stemmer for the tokens.', type=bool)
def main(
        input_file,
        index_data,
        index_type,
        print_logs,
        print_metadata,
        use_stemmer
):

    utils = Utils()
    urls = utils.read_json_file(input_file)

    # creating the index
    if index_type == "positional":
        pos_index = PositionalIndex(
            urls=urls,
            type=index_data,
            print_logs=print_logs,
            print_metadata=print_metadata,
            use_stemmer=use_stemmer
        )
        pos_index.run(sort=True)
    else:
        non_pos_index = NonPositionalIndex(
            urls=urls,
            type=index_data,
            print_logs=print_logs,
            print_metadata=print_metadata,
            use_stemmer=use_stemmer
        )
        non_pos_index.run(sort=True)


if __name__ == '__main__':
    main()
