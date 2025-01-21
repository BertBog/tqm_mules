import re
from pathlib import Path
from typing import Optional, List

from tqmmules.app.tqmmlogger import logger
from tqmmules.app.utils import parsingutils


class SaveParser(object):
    """
    Parser for TQM saves.
    """

    def __init__(self) -> None:
        """
        Initializes the parser.
        :return: None
        """
        self._data_as_str = None  # type: Optional[str]
        self._data_raw = None  # type: Optional[bytes]

    def parse(self, path_save: Path) -> None:
        """
        Parses the target save file.
        :param path_save: TQM save file
        :return: None
        """
        logger.debug(f'Parsing save: {path_save}')
        with path_save.open(mode='rb') as handle:
            self._data_raw = handle.read()
            self._data_as_str = self._data_raw.decode('latin1')

    def extract_player_name(self) -> str:
        """
        Extracts the player name from the save file.
        :return: Player name
        """
        m = re.search('myPlayerName(.*)isIn', self._data_as_str)
        return parsingutils.read_utf16(self._data_raw[m.start() + 12:m.end() - 4])

    def extract_items(self) -> List[str]:
        """
        Extracts the items from the save file.
        :return: None
        """
        all_records = []
        for i, match in enumerate(re.finditer(parsingutils.RE_PATTERN, self._data_as_str, re.DOTALL)):
            try:
                all_records.append(parsingutils.extract_record_from_match(match, self._data_as_str, self._data_raw))
            except TypeError:
                continue

        # Extract item base names
        return [parsingutils.read_string(record['baseName'].value_as_bytes) for record in all_records]

    @staticmethod
    def parse_all(paths_saves: List[Path]) -> List:
        """
        Parses the list of saves.
        :param paths_saves: Paths to several save files
        :return: List of parsed items
        """
        records_out = []
        player_name_by_dir = {'Sys': 'SHARED'}
        for path_save in paths_saves:
            # Parse the save
            parser = SaveParser()
            parser.parse(path_save)

            # Extract player name
            if path_save.name == 'Player.chr':
                try:
                    player_name_by_dir[path_save.parent.name] = parser.extract_player_name()
                except AttributeError:
                    logger.warning(f'Cannot parse player name from: {path_save}')

            # Save the items
            try:
                items = parser.extract_items()
                for item in items:
                    records_out.append({'key': item, 'save': str(path_save)})
                logger.info(f'Parsed {len(items):,} items from save: {path_save}')
            except TypeError:
                logger.error(f'Error parsing: {path_save}')
                continue

        # Add the player names
        for row in records_out:
            row['character'] = player_name_by_dir.get(Path(row['save']).parent.name, 'n/a')
        return records_out
