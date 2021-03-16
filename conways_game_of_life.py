import time

MIN_ZEILEN = 5
MAX_ZEILEN = 100
MIN_SPALTEN = 5
MAX_SPALTEN = 100


def get_zeilenanzahl(grid):
    return len(grid)


def get_spaltenanzahl(grid):
    spaltenanzahl_liste = []
    for zeile in grid:
        spaltenanzahl_liste.append(len(zeile))
    for i in range(len(spaltenanzahl_liste)):
        if spaltenanzahl_liste[0] != spaltenanzahl_liste[i]:
            print(f"Unterschiedlich lange Zeilen:")
            print(f"Zeile 0 = {spaltenanzahl_liste[0]}")
            print(f" Zeile {i} = {spaltenanzahl_liste[i]}")
            return None
    return spaltenanzahl_liste[0]


def ist_spaltenanzahl_in_ordnung(grid):
    return MIN_SPALTEN <= get_spaltenanzahl(grid) <= MAX_SPALTEN


def ist_zeilenanzahl_in_ordnung(grid):
    return MIN_ZEILEN <= get_zeilenanzahl(grid) <= MAX_ZEILEN


def ist_startkonfiguration_in_ordnung(grid):
    return ist_zeilenanzahl_in_ordnung(grid) and ist_spaltenanzahl_in_ordnung(grid)


def get_anzahl_lebende_nachbarn(grid, y, x):
    anzahl_lebende_nachbarn = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            y_nachbar = y + i
            x_nachbar = x + j
            if i == j == 0:
                # aktuelles Feld überspringen
                continue
            elif not (0 <= y_nachbar < get_zeilenanzahl(grid) and 0 <= x_nachbar < get_spaltenanzahl(grid)):
                # Felder außerhalb unseres grid überspringen
                continue
            else:
                anzahl_lebende_nachbarn += grid[y_nachbar][x_nachbar]
    return anzahl_lebende_nachbarn


def get_status_neu(status_alt, anzahl_lebende_nachbarn):
    if status_alt == 0 and anzahl_lebende_nachbarn == 3:
        # Geburt
        return 1
    if status_alt == 1:
        if anzahl_lebende_nachbarn < 2:
            # Tod durch Einsamkeit
            return 0
        if anzahl_lebende_nachbarn > 3:
            # Tod durch Überbevölkerung
            return 0

    return status_alt


def runde_spielen(grid):
    neues_grid = []

    for y in range(get_zeilenanzahl(grid)):
        neues_grid.append([])
        for x in range(get_spaltenanzahl(grid)):
            status_alt = grid[y][x]
            anzahl_lebende_nachbarn = get_anzahl_lebende_nachbarn(grid, y, x)
            status_neu = get_status_neu(status_alt, anzahl_lebende_nachbarn)
            neues_grid[y].append(status_neu)

    return neues_grid


def starte_simulation(startkonfiguration, anzahl_schritte, anzeigen=False, sekunden_pro_lebenszyklus=0.3):
    if not (ist_startkonfiguration_in_ordnung(startkonfiguration)):
        return [[]]

    grid = startkonfiguration

    for runde in range(anzahl_schritte):
        grid = runde_spielen(grid)
        if anzeigen:
            ergebnis_ausgeben(grid)
            time.sleep(sekunden_pro_lebenszyklus)

    if anzeigen:
        ergebnis_ausgeben(grid)

    return grid


def ergebnis_ausgeben(grid):
    for y in grid:
        print(y)
    # Leerzeile zum Trennen der Grids in der Ausgabe
    print("")