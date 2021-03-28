import unittest

from main.python.conways_game_of_life import lade_konfiguration, ist_dateiinhalt_in_ordnung, \
    dimensionen_stimmen_ueberein, lade_grid_aus_dateiinhalt


class LadeKonfigurationTest(unittest.TestCase):
    def test_valid_file(self):
        pfad = "../resources/conway_valid_file.txt"
        expected_result = [
            ['1', '0', '0', '0', '1', '0'],
            ['0', '0', '1', '0', '1', '0'],
            ['0', '1', '0', '0', '1', '0'],
            ['0', '0', '0', '0', '1', '0']
        ]
        result = lade_konfiguration(pfad)
        self.assertEqual(expected_result, result, "test_valid_file")

    def test_invalid_file(self):
        pfad = "../resources/conway_invalid_file.txt"
        expected_result = list()
        result = lade_konfiguration(pfad)
        self.assertEqual(expected_result, result, "test_invalid_file")

    def test_missing_file(self):
        pfad = "../resources/conway_missing_file.txt"
        expected_result = list()
        result = lade_konfiguration(pfad)
        self.assertEqual(expected_result, result, "test_invalid_file")

    def test_file_content_valid_content(self):
        file_content = [
            "Conway\n",
            "4 6\n",
            "START\n",
            "100010\n",
            "001010\n",
            "010010\n",
            "000010\n",
            "END",
        ]
        expected_result = True
        result = ist_dateiinhalt_in_ordnung(file_content)
        self.assertEqual(expected_result, result, "test_file_content_valid_content")

    def test_file_content_wrong_header(self):
        file_content = [
            "Cornelius\n",
            "4 6\n",
            "START\n",
            "100010\n",
            "001010\n",
            "010010\n",
            "000010\n",
            "END",
        ]
        expected_result = False
        result = ist_dateiinhalt_in_ordnung(file_content)
        self.assertEqual(expected_result, result, "test_file_content_wrong_header")

    def test_file_content_no_start(self):
        file_content = [
            "Conway\n",
            "4 6\n",
            "100010\n",
            "001010\n",
            "010010\n",
            "000010\n",
            "END",
        ]
        expected_result = False
        result = ist_dateiinhalt_in_ordnung(file_content)
        self.assertEqual(expected_result, result, "test_file_content_no_start")

    def test_file_content_no_end(self):
        file_content = [
            "Conway\n",
            "4 6\n",
            "START\n",
            "100010\n",
            "001010\n",
            "010010\n",
            "000010",
        ]
        expected_result = False
        result = ist_dateiinhalt_in_ordnung(file_content)
        self.assertEqual(expected_result, result, "test_file_content_no_end")

    def test_file_content_less_lines(self):
        file_content = [
            "Conway\n",
            "4 6\n",
            "START\n",
            "100010\n",
            "001010\n",
            "010010\n",
            "END",
        ]
        expected_result = False
        result = dimensionen_stimmen_ueberein(lade_grid_aus_dateiinhalt(file_content), file_content[1])
        self.assertEqual(expected_result, result, "test_file_content_less_lines")

    def test_file_content_more_lines(self):
        file_content = [
            "Conway\n",
            "4 6\n",
            "START\n",
            "100010\n",
            "001010\n",
            "010010\n",
            "000010\n",
            "000010\n",
            "END",
        ]
        expected_result = False
        result = dimensionen_stimmen_ueberein(lade_grid_aus_dateiinhalt(file_content), file_content[1])
        self.assertEqual(expected_result, result, "test_file_content_more_lines")

    def test_file_content_less_columns(self):
        file_content = [
            "Conway\n",
            "4 6\n",
            "START\n",
            "10001\n",
            "00101\n",
            "01001\n",
            "00001\n",
            "END",
        ]
        expected_result = False
        result = dimensionen_stimmen_ueberein(lade_grid_aus_dateiinhalt(file_content), file_content[1])
        self.assertEqual(expected_result, result, "test_file_content_less_columns")

    def test_file_content_more_columns(self):
        file_content = [
            "Conway\n",
            "4 6\n",
            "START\n",
            "1000100\n",
            "0010100\n",
            "0100100\n",
            "0000100\n",
            "END",
        ]
        expected_result = False
        result = dimensionen_stimmen_ueberein(lade_grid_aus_dateiinhalt(file_content), file_content[1])
        self.assertEqual(expected_result, result, "test_file_content_more_columns")

    def test_file_content_different_line_length(self):
        file_content = [
            "Conway\n",
            "4 6\n",
            "START\n",
            "100010\n",
            "0010\n",
            "01\n",
            "00001\n",
            "END",
        ]
        expected_result = False
        result = dimensionen_stimmen_ueberein(lade_grid_aus_dateiinhalt(file_content), file_content[1])
        self.assertEqual(expected_result, result, "test_file_content_different_line_length")
