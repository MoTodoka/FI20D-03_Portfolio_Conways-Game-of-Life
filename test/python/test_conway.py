from unittest import TestCase
from main.python.conways_game_of_life import starte_simulation


class ConwayTest(TestCase):
    def test_three_neighbors_results_in_new_life_less_two_dies(self):
        startkonfiguration = [[0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0],
                              [1, 1, 1, 0, 0],
                              [0, 0, 0, 0, 0]]
        erwartete_folgegeneration = [[0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0],
                                     [0, 1, 0, 0, 0],
                                     [0, 1, 0, 0, 0],
                                     [0, 1, 0, 0, 0]]
        anzahl_schritte = 1
        folgegeneration = starte_simulation(startkonfiguration, anzahl_schritte)
        self.assertListEqual(folgegeneration, erwartete_folgegeneration,
                             msg="{0} liefert nicht das erwartete Ergebnis".format(startkonfiguration))

    def test_dimensions_before_after_are_equal(self):
        startkonfiguration = [[0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0],
                              [1, 1, 1, 0, 0],
                              [0, 0, 0, 0, 0],
                              [0, 0, 1, 0, 1]]
        anzahl_schritte = 1
        folgegeneration = starte_simulation(startkonfiguration, anzahl_schritte)
        self.assertEqual(len(folgegeneration), len(startkonfiguration),
                         msg="Die Anzahl der Zeilen ist nicht gleich bei der Ein- und Ausgabe")
        self.assertEqual(len(folgegeneration[0]), len(startkonfiguration[0]),
                         msg="Die Anzahl der Spalten ist nicht gleich bei der Ein- und Ausgabe")
