import json
import re
from importlib.resources import files
from pathlib import Path
from typing import Dict, Optional, Union, List

from tqmmules.app.tqmmlogger import logger


KEYS = [
    'name',
    'category',
    'classification',
    'levelRequirement',
    'strengthRequirement',
    'dexterityRequirement',
    'intelligenceRequirement',
    'set'
]


class ItemDB(object):
    """
    Database for TQM items.
    """

    def __init__(self) -> None:
        """
        Initializes the database.
        :return: None
        """
        self._item_by_key = None # type: Optional[Dict[str, Dict]]
        self.load_content()

    def load_content(self) -> None:
        """
        Reads the database content.
        :return: None
        """
        # Read the JSON file
        path_db = str(files('tqmmules').joinpath('data/db.json'))
        with Path(path_db).open(encoding='utf-8') as handle:
            content = json.load(handle)['equipment']

        # Create dictionary
        self._item_by_key = {}
        for category, items in content.items():
            for item in items:
                key = re.sub(r'\\+', '__', item['path']).lower()
                if key in self._item_by_key:
                    logger.warning(f'Duplicate key: {key}')
                self._item_by_key[key] = {**item, 'category': category}
        logger.info(f'Database loaded successfully ({len(self._item_by_key):,} items).')

    def get_item(self, key: str) -> Union[Dict, None]:
        """
        Retrieves the item with the given key.
        :param key: Item key
        :return: Item data
        """
        if key not in self._item_by_key:
            logger.debug(f"Item with key '{key}' not found")
            return None
        return self._item_by_key[key]

    def annotate_all(self, records_in: List[Dict]) -> List[Dict]:
        """
        Annotates the input items.
        :param records_in: Input records
        :return: Annotated item records
        """
        records_full = []
        for record in records_in:
            key_sanitized = re.sub(r'\\+', '__', record['key']).lower()
            item_info = self.get_item(key_sanitized)
            if item_info is not None:
                for key in KEYS:
                    record[key] = item_info.get(key, None)
                record['properties'] = str(item_info.get('properties', {}))
            records_full.append(record)
        logger.info(f'Annotated {sum(KEYS[0] in r for r in records_full):,}/{len(records_full):,} items')
        return records_full
