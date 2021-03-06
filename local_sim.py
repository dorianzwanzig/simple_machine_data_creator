# machine data creation tool for machine learning project
# dorian zwanzig 2018-11-03
# version 0.3.1811210800

import numpy as np
import sys
import random
import time
from datetime import datetime, timedelta

# Zugriffsversuch auf Ausgabedatei
try:
    d = open("output.txt", "w")
except:
    print("Zugriff nicht erfolgt")
    sys.exit(0)

# Kopfzeile schreiben
d.write("ID;Maschine;Timestamp;Datum;Uhrzeit;Drehzahl;Leistungsaufnahme;Vibration;Lautstaerke;Temperatur;FehlerID;Produktionsprogramm;SollMenge;IstMenge;Ausschuss\n")

# Startwerte (STartData):
std_dz = 100             # Startdrehzahl
std_la = 18.5            # Startleistungsaufnahme
std_vb = 0               # Startvibration
std_ls = 75              # Startlautstärke
data_id_nr = 1000000     # Startwert für die Datensatz ID, wird um "400_1_" am Anfang ergänzt
std_te = 100             # Starttemperatur
fehler_id = "x000"       # Fehlerwert bei Ausfall
time = datetime(2018, 1, 1, 0, 0, 0)   # Startzeit der Simulation
datum = "leer"           # Simuliertes Datum
uhrzeit = "leer"         # Simulierte Uhrzeit
machine_id = "XL400_01"  # Identifikation der Maschine
prod_programm = "PP001"  # Produktionsprogramm
soll_menge = 2350        # Soll-Menge des Produktionsprogramm
ist_menge = 2350         # Tatsächlich produzierte Menge
ausschuss = 0            # Fehlerhafte Teile

# Startzeile setzen
zeile = 1

# Nutzerabfrage: Menge Datensätze
menge = int(input("Bitte Anzahl der gewünschten Datensätze eingeben: ")) + zeile

# Werte in Ausgabedatei schreiben


def write_data():
    global zeile
    zeile = zeile + 1
    d.write("400_1_" + str(data_id_nr) + ";" + str(machine_id) + ";" + str(time) + ";" + str(datum) + ";" + str(uhrzeit) + ";" + str(std_dz) +
            ";" + str(std_la) + ";" + str(std_vb) + ";" + str(std_ls) + ";" + str(std_te) + ";" + str(fehler_id) +
            ";" + str(prod_programm) + ";" + str(soll_menge) + ";" + str(ist_menge) + ";" + str(ausschuss) + "\n")


# Zeitzähler


def timer():
    global time, datum, uhrzeit
    time = time + timedelta(seconds=30)
    now = str(time).split()
    datum = str(now[0])
    uhrzeit = str(now[1])

# Erstellung mehrerer Datensätze durch Schleife (Normalbetrieb)


def normalbetrieb():
    global menge, std_dz, std_la, std_vb, std_ls, data_id_nr, std_te, time, fehler_id, ist_menge, ausschuss
    x = 0
    y = random.randrange(1, 200)
    while x < y:
        std_dz = 100
        std_la = round(np.random.normal(18.5, 0.1), 3)
        std_vb = round(np.random.normal(0, 0.1), 3)
        std_ls = round(np.random.normal(75, 0.1), 3)
        data_id_nr = data_id_nr + 1
        timer()
        std_te = 100
        fehler_id = "x000"
        ist_menge = 2350
        ausschuss = random.randrange(0, 20)
        write_data()
        x = x + 1

# Erstellung mehrerer Datensätze durch Schleife (Wartung)


def wartung():
    global menge, std_dz, std_la, std_vb, std_ls, data_id_nr, std_te, time, fehler_id, ist_menge, ausschuss
    fehler_id = wartung_grund()
    x = 0
    y = random.randrange(10, 50)
    while x < y:
        std_dz = 0
        std_la = round(np.random.normal(2, 0.1), 3)
        std_vb = round(np.random.normal(0, 0.3), 3)
        std_ls = round(np.random.normal(25, 0.1), 3)
        data_id_nr = data_id_nr + 1
        timer()
        std_te = std_te - 1
        ist_menge = 0
        ausschuss = 0
        write_data()
        x = x + 1

# Wartungsgrund auswählen


def wartung_grund():
    random_choice = random.randrange(1, 100)
    if random_choice < 40:
        return "A001"   # Kein Material/ kein Auftrag/ kein Personal (A001)
    elif random_choice < 70:
        return "A002"   # Werkzeugwechsel/ Rüsten (A002)
    elif random_choice < 80:
        return "A003"   # geplante Wartung (A003)
    elif random_choice < 95:
        return "A004"   # geplante Reinigung (A004)
    else:
        return "A000"   # Sonstiger ungeplanter Grund (A000)

# Erstellung mehrerer Datensätze durch Schleife (Ausfall aufgrund zu hoher Motortemperatur)


def ausfall_2():
    global menge, std_dz, std_la, std_vb, std_ls, data_id_nr, std_te, time, fehler_id, ist_menge, ausschuss
    fehler_id = "x000"
    x = 1
    # Motortemperatur steigt bis zum Ausfall
    while std_te < 200:
        std_dz = 100 + random.randrange(-4, 0)
        std_la = round(np.random.normal(18.5*x, 0.2), 3)
        std_vb = round(np.random.normal(0, 0.1), 3)
        std_ls = round(np.random.normal(75, 0.1), 3)
        data_id_nr = data_id_nr + 1
        timer()
        std_te = round(std_te + np.random.normal(1, 0.5), 1)
        ist_menge = int(std_dz * 47 / 2)
        ausschuss = int(round(x * x * random.randrange(5, 20), 0))
        write_data()
        x = x + round(np.random.normal(0.001, 0.002), 3)
    fehler_id = "F002"
    # Abkühlung bis Normaltemperatur bevor Maschine wieder angeschaltet wird
    while std_te > 100:
        std_dz = 0
        std_la = round(np.random.normal(1.5, 0.1), 3)
        std_vb = round(np.random.normal(0, 0.05), 3)
        std_ls = round(np.random.normal(25, 0.1), 3)
        data_id_nr = data_id_nr + 1
        std_te = round(std_te - 1, 1)
        timer()
        ist_menge = 0
        ausschuss = 0
        write_data()
        x = x + 1

# Erstellung mehrerer Datensätze durch Schleife (Ausfall aufgrund zu hoher Leistungsaufnahme)


def ausfall_1():
    global menge, std_dz, std_la, std_vb, std_ls, data_id_nr, std_te, time, fehler_id, ist_menge, ausschuss
    fehler_id = "x000"
    x = 1
    # Strombedarf steigt bis zum Ausfall
    while std_la < 25:
        std_dz = 100 + random.randrange(-3, 1)
        std_la = round(np.random.normal(18.5*x, 0.2), 3)
        std_vb = round(np.random.normal(0, 0.1), 3)
        std_ls = round(np.random.normal(75, 0.1), 3)
        data_id_nr = data_id_nr + 1
        timer()
        std_te = round(std_te + np.random.normal(0.5, 0.2), 1)
        ist_menge = int(std_dz * 47 / 2)
        ausschuss = int(round(x * x * random.randrange(5, 20), 0))
        write_data()
        x = x + round(np.random.normal(0.005, 0.005), 3)
    fehler_id = "F001"
    # zufällige Ausfallzeit
    x = 0
    y = random.randrange(10, 50)
    while x < y:
        std_dz = 0
        std_la = round(np.random.normal(1.5, 0.1), 3)
        std_vb = round(np.random.normal(0, 0.1), 3)
        std_ls = round(np.random.normal(25, 0.1), 3)
        data_id_nr = data_id_nr + 1
        std_te = round(std_te - 1, 1)
        timer()
        ist_menge = 0
        ausschuss = 0
        write_data()
        x = x + 1

# Auswahl zwischen den Events


def choose():
    random_choice = random.randrange(1, 100)
    if random_choice < 80:
        normalbetrieb()
    elif random_choice < 90:
        ausfall_1()
    elif random_choice < 97:
        ausfall_2()
    else:
        wartung()


# Aufruf Auswahl
while zeile < menge:
    choose()

# Erfolgsbestätigung
counter = zeile - 1
print("Datei mit " + str(counter) +
      " Datensätzen wurde erstellt! Programm beendet")

# Schließen der Datei
d.close()
