import json
import os
from typing import Dict


class Utils:
    def __init__(self) -> None:
        pass

    def read_json_file(self, path):
        with open(path, 'r') as json_file:
            json_data = json.loads(json_file.read())
            return json_data

    def write_index(
            self,
            index: Dict,
            path: str = None,
            file_name: str = None,
            index_type: str = 'title',
            is_positional: bool = True,
            use_stemmer: bool = False
    ):
        sufix = ".pos_index" if is_positional else ".non_pos_index"
        path = '' if path is None else str(path)
        file_name = '' if file_name is None else str(file_name)
        prefix = 'mon_stemmer.' if use_stemmer else ''
        path_to_file = os.path.join(
            path, prefix + file_name + index_type + sufix + '.json'
        )
        with open(path_to_file, 'w') as file:
            file.write(
                json.dumps(
                    index,
                    ensure_ascii=False,
                    indent=4
                )
            )

    def write_metadata(
        self,
            metadata: Dict,
            path: str = None,
            file_name: str = None,
            index_type: str = 'title',
            is_positional: bool = True,
            use_stemmer: bool = False
    ):
        sufix = ".pos_metadata" if is_positional else ".non_pos_metadata"
        path = '' if path is None else str(path)
        file_name = '' if file_name is None else str(file_name)
        prefix = 'mon_stemmer.' if use_stemmer else ''
        path_to_file = os.path.join(
            path, prefix + file_name + index_type + sufix + '.json'
        )
        with open(path_to_file, 'w') as file:
            file.write(
                json.dumps(
                    metadata,
                    ensure_ascii=False,
                    indent=4
                )
            )
