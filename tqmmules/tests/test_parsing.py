import unittest
from importlib.resources import files
from pathlib import Path

from tqmmules.app.saveparser import SaveParser
from tqmmules.app.tqmmlogger import initialize_logging


class TestParsing(unittest.TestCase):
    """
    Contains tests for the parsing functions.
    """

    def test_parse_player_name(self) -> None:
        """
        Tests if the player name can be parsed from the save file.
        :return: None
        """
        parser = SaveParser()
        path_save = Path(str(files('tqmmules').joinpath('data/testing/player.chr')))
        parser.parse(path_save)
        self.assertEqual(parser.extract_player_name(), "Kali")

    def test_parse_save(self) -> None:
        """
        Tests the parsing of a save file.
        :return: None
        """
        parser = SaveParser()
        path_save = Path(str(files('tqmmules').joinpath('data/testing/player.chr')))
        parser.parse(path_save)
        items = parser.extract_items()
        self.assertGreater(len(items), 0)


if __name__ == '__main__':
    initialize_logging()
    unittest.main()
