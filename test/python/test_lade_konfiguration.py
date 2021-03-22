import unittest

from main.python.conways_game_of_life import lade_konfiguration


class LadeKonfigurationTest(unittest.TestCase):
    def test_test_4_6_valid_file(self):
        pfad = "../resources/conway_4_6_valid_file.txt"
        expected_result = [
            ['1', '0', '0', '0', '1', '0'],
            ['0', '0', '1', '0', '1', '0'],
            ['0', '1', '0', '0', '1', '0'],
            ['0', '0', '0', '0', '1', '0']
        ]
        result = lade_konfiguration(pfad)
        self.assertEqual(expected_result, result)

    def test_4_6_wrong_header(self):
        pfad = "../resources/conway_4_6_wrong_header.txt"
        expected_result = []
        result = lade_konfiguration(pfad)
        self.assertEqual(expected_result, result)

    def test_4_6_less_lines(self):
        pfad = "../resources/conway_4_6_less_lines.txt"
        expected_result = []
        result = lade_konfiguration(pfad)
        self.assertEqual(expected_result, result)

    def test_4_6_less_columns(self):
        pfad = "../resources/conway_4_6_less_columns.txt"
        expected_result = []
        result = lade_konfiguration(pfad)
        self.assertEqual(expected_result, result)
