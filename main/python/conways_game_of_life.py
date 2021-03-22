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
            return 0
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


def starte_simulation(startkonfiguration: [[int]], anzahl_schritte: int, anzeigen=False, sekunden_pro_lebenszyklus=0.3):
    if not (ist_startkonfiguration_in_ordnung(startkonfiguration)):
        return []

    grid = startkonfiguration

    for runde in range(anzahl_schritte):
        grid = runde_spielen(grid)
        if anzeigen:
            ergebnis_ausgeben(grid)
            time.sleep(sekunden_pro_lebenszyklus)

    if anzeigen:
        ergebnis_ausgeben(grid)

    return grid


def lade_dateiinhalt_als_liste(pfad_zur_datei):
    datei = open(pfad_zur_datei, 'r')
    dateiinhalt_als_liste = [zeile for zeile in datei]
    datei.close()
    return dateiinhalt_als_liste


def sind_dimensionen_in_ordnung(dimensionen):
    dimensionen_liste = dimensionen.split()
    laenge_okay = len(dimensionen_liste) == 2
    zeilen_okay = dimensionen_liste[0].isdigit()
    spalten_okay = dimensionen_liste[1].isdigit()
    return laenge_okay and zeilen_okay and spalten_okay


def datei_enthaelt_zeile(pruefstring, dateiinhalt_als_liste):
    for zeile in dateiinhalt_als_liste:
        if zeile.startswith(pruefstring):
            return True
    return False


def ist_dateiinhalt_in_ordnung(dateiinhalt_als_liste):
    header_okay = ist_header_in_ordnung(dateiinhalt_als_liste[0])
    dimensionen_okay = sind_dimensionen_in_ordnung(dateiinhalt_als_liste[1])
    enthaelt_start = datei_enthaelt_zeile("START\n", dateiinhalt_als_liste)
    enthaelt_end = datei_enthaelt_zeile("END", dateiinhalt_als_liste)
    return header_okay and dimensionen_okay and enthaelt_start and enthaelt_end


def ist_header_in_ordnung(header):
    return header == "Conway\n"


def lade_grid_aus_dateiinhalt(dateiinhalt_als_liste):
    gestartet = False
    grid = []
    for zeile in dateiinhalt_als_liste:
        if gestartet:
            if zeile.startswith("END"):
                return grid
            grid.append([char for char in zeile if char != '\n'])
        if zeile.startswith("START"):
            gestartet = True


def stimmen_dimensionen_ueberein(grid, dimensionen):
    erwartete_zeilen = int(dimensionen.split()[0])
    erwartete_spalten = int(dimensionen.split()[1])
    return get_zeilenanzahl(grid) == erwartete_zeilen and get_spaltenanzahl(grid) == erwartete_spalten


def lade_konfiguration(pfad_zur_datei: str):
    dateiinhalt_als_liste = lade_dateiinhalt_als_liste(pfad_zur_datei)
    if ist_dateiinhalt_in_ordnung(dateiinhalt_als_liste):
        grid = lade_grid_aus_dateiinhalt(dateiinhalt_als_liste)
        if stimmen_dimensionen_ueberein(grid, dateiinhalt_als_liste[1]):
            return grid
    return []


def ergebnis_ausgeben(grid):
    for y in grid:
        print(y)
    # Leerzeile zum Trennen der Grids in der Ausgabe
    print("")
