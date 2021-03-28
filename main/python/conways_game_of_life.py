from matplotlib import pyplot

MIN_ZEILEN = 5
MAX_ZEILEN = 100
MIN_SPALTEN = 5
MAX_SPALTEN = 100


def starte_simulation(startkonfiguration: [[int]], anzahl_schritte: int, anzeigen: bool = False,
                      sekunden_pro_lebenszyklus: float = 0.3) -> [[int]]:
    """Gibt die Zellenanordnung nach dem letzten Schritt als geschachtelte Liste aus. Bei Fehler wird eine leere
    Liste ausgegeben."""
    if not (ist_startkonfiguration_in_ordnung(startkonfiguration)):
        return list()

    grid = startkonfiguration

    if anzeigen:
        fig, ax = pyplot.subplots()
        ax.imshow(grid, cmap='gist_gray_r', vmin=0, vmax=1)
        fig.canvas.draw()

    for _ in range(anzahl_schritte):
        grid = runde_spielen(grid)
        if anzeigen:
            ax.cla()
            ax.imshow(grid, cmap='gist_gray_r', vmin=0, vmax=1)
            fig.canvas.draw()
            pyplot.pause(sekunden_pro_lebenszyklus)

    return grid


def ist_startkonfiguration_in_ordnung(grid) -> bool:
    return ist_zeilenanzahl_in_ordnung(grid) and ist_spaltenanzahl_in_ordnung(grid)


def ist_zeilenanzahl_in_ordnung(grid) -> bool:
    return MIN_ZEILEN <= get_zeilenanzahl(grid) <= MAX_ZEILEN


def get_zeilenanzahl(grid) -> int:
    return len(grid)


def ist_spaltenanzahl_in_ordnung(grid) -> bool:
    return MIN_SPALTEN <= get_spaltenanzahl(grid) <= MAX_SPALTEN


def get_spaltenanzahl(grid) -> int:
    laenge_erste_zeile = len(grid[0])
    for zeile in grid:
        if laenge_erste_zeile != len(zeile):
            return 0
    return laenge_erste_zeile


def runde_spielen(grid) -> [[int]]:
    neues_grid = list()
    zeilenanzahl = get_zeilenanzahl(grid)
    spaltenanzahl = get_spaltenanzahl(grid)

    for y in range(zeilenanzahl):
        neues_grid.append(list())
        for x in range(spaltenanzahl):
            status_alt = grid[y][x]
            anzahl_lebende_nachbarn = get_anzahl_lebende_nachbarn(grid, y, x)
            status_neu = get_status_neu(status_alt, anzahl_lebende_nachbarn)
            neues_grid[y].append(status_neu)

    return neues_grid


def get_anzahl_lebende_nachbarn(grid, y, x) -> int:
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


def get_status_neu(status_alt, anzahl_lebende_nachbarn) -> int:
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


def lade_konfiguration(pfad_zur_datei: str) -> [[int]]:
    """Gibt die Zellenanordnung als geschachtelte Liste aus. Bei Fehler wird eine leere Liste ausgegeben."""
    dateiinhalt_als_liste = lade_dateiinhalt_als_liste(pfad_zur_datei)
    if ist_dateiinhalt_in_ordnung(dateiinhalt_als_liste):
        grid = lade_grid_aus_dateiinhalt(dateiinhalt_als_liste)
        if dimensionen_stimmen_ueberein(grid, dateiinhalt_als_liste[1]):
            return grid
    return list()


def lade_dateiinhalt_als_liste(pfad_zur_datei) -> [str]:
    datei = open(pfad_zur_datei, 'r')
    dateiinhalt_als_liste = [zeile for zeile in datei]
    datei.close()
    return dateiinhalt_als_liste


def ist_dateiinhalt_in_ordnung(dateiinhalt_als_liste) -> bool:
    header_okay = ist_header_in_ordnung(dateiinhalt_als_liste[0])
    dimensionen_okay = sind_dimensionen_in_ordnung(dateiinhalt_als_liste[1])
    enthaelt_start = datei_enthaelt_zeile("START\n", dateiinhalt_als_liste)
    enthaelt_end = datei_enthaelt_zeile("END", dateiinhalt_als_liste)
    return header_okay and dimensionen_okay and enthaelt_start and enthaelt_end


def ist_header_in_ordnung(header) -> bool:
    return header == "Conway\n"


def sind_dimensionen_in_ordnung(dimensionen) -> bool:
    dimensionen_liste = dimensionen.split()
    laenge_okay = len(dimensionen_liste) == 2
    zeilen_okay = dimensionen_liste[0].isdigit()
    spalten_okay = dimensionen_liste[1].isdigit()
    return laenge_okay and zeilen_okay and spalten_okay


def datei_enthaelt_zeile(pruefstring, dateiinhalt_als_liste) -> bool:
    for zeile in dateiinhalt_als_liste:
        if zeile.startswith(pruefstring):
            return True
    return False


def lade_grid_aus_dateiinhalt(dateiinhalt_als_liste) -> [[int]]:
    gestartet = False
    grid = list()
    for zeile in dateiinhalt_als_liste:
        if gestartet:
            if zeile.startswith("END"):
                return grid
            grid.append([char for char in zeile if char != '\n'])
        if zeile.startswith("START"):
            gestartet = True


def dimensionen_stimmen_ueberein(grid, dimensionen) -> bool:
    erwartete_zeilen = int(dimensionen.split()[0])
    erwartete_spalten = int(dimensionen.split()[1])
    return get_zeilenanzahl(grid) == erwartete_zeilen and get_spaltenanzahl(grid) == erwartete_spalten
