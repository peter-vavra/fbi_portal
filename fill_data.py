import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin INTEGER DEFAULT 0,
    meno VARCHAR(255) NOT NULL,
    priezvisko VARCHAR(255) NOT NULL,
    krycie_meno VARCHAR(255) NOT NULL,
    vyska INTEGER NOT NULL,
    vaha INTEGER NOT NULL,
    stav VARCHAR(255) NOT NULL,
    pozicia VARCHAR(255) NOT NULL,
    kontaktna_osoba VARCHAR(255) NOT NULL,
    vek INTEGER NOT NULL,
    miesto_narodenia VARCHAR(255) NOT NULL,
    bydlisko VARCHAR(255) NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS dochadzka (
    id_pouzivatela INTEGER,
    meno VARCHAR(255) NOT NULL,
    priezvisko VARCHAR(255) NOT NULL,
    krycie_meno VARCHAR(255) NOT NULL,
    datum VARCHAR(255) NOT NULL,
    pocet_hodin INTEGER NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS akcie (
    id_pouzivatela INTEGER,
    krycie_meno VARCHAR(255) NOT NULL,
    nazov_akcie VARCHAR(255) NOT NULL,
    ucastnici VARCHAR(255) NOT NULL,
    miesto VARCHAR(255) NOT NULL,
    okruh_sledovanych VARCHAR(255) NOT NULL,
    datum_od_do VARCHAR(255) NOT NULL
)
''')

username1, password1, meno1, priezvisko1, is_admin1, krycie_meno1, vyska1, vaha1, stav1, pozicia1, kontaktna_osoba1, vek1, miesto_narodenia1, bydlisko1 = "admin", hashlib.sha3_256("admin".encode()).hexdigest(), "Administrátor", "Systému", 1, "Admin", 180, 80, "In office", "Správca systému", "IT oddelenie", 35, "Neznáme", "Adresa zamestnávateľa"
username2, password2, meno2, priezvisko2, is_admin2, krycie_meno2, vyska2, vaha2, stav2, pozicia2, kontaktna_osoba2, vek2, miesto_narodenia2, bydlisko2 = "john", hashlib.sha3_256("john".encode()).hexdigest(), "John", "Smith", 0, "Steel", 175, 70, "Out of office", "Secret Agent", "Jane Smith (manželka)", 40, "New York, USA", "123 Main Street, New York, USA"
username3, password3, meno3, priezvisko3, is_admin3, krycie_meno3, vyska3, vaha3, stav3, pozicia3, kontaktna_osoba3, vek3, miesto_narodenia3, bydlisko3 = "melvin", hashlib.sha3_256("melvin".encode()).hexdigest(), "Melvin", "Miller", 0, "Shadow", 185, 90, "Secret", "Weapon of FBI", "Linda Miller (manželka)", 45, "Chicago, USA", "456 Oak Street, Chicago, USA"
username4, password4, meno4, priezvisko4, is_admin4, krycie_meno4, vyska4, vaha4, stav4, pozicia4, kontaktna_osoba4, vek4, miesto_narodenia4, bydlisko4 = "joseph", hashlib.sha3_256("joseph".encode()).hexdigest(), "Joseph", "Taylor", 1, "Phoenix", 170, 75, "In office", "Hacker", "Susan Taylor (sestra)", 30, "Los Angeles, USA", "789 Elm Avenue, Los Angeles, USA"
username5, password5, meno5, priezvisko5, is_admin5, krycie_meno5, vyska5, vaha5, stav5, pozicia5, kontaktna_osoba5, vek5, miesto_narodenia5, bydlisko5 = "liam", hashlib.sha3_256("liam".encode()).hexdigest(), "Liam", "Johnson", 0, "Phantom", 183, 80, "In office", "Terénny operátor", "Emma Carter", 32, "New York City, USA", "781 Avenue, London, Spojené kráľovstvo"
username6, password6, meno6, priezvisko6, is_admin6, krycie_meno6, vyska6, vaha6, stav6, pozicia6, kontaktna_osoba6, vek6, miesto_narodenia6, bydlisko6 = "sofia", hashlib.sha3_256("sofia".encode()).hexdigest(), "Sofia", "Rodriguez", 1, "Viper", 170, 60, "Secret", "Technologický expert", "Alejandro Perez", 28, "Madrid, Španielsko", "781 Street, Barcelona, Španielsko"
username7, password7, meno7, priezvisko7, is_admin7, krycie_meno7, vyska7, vaha7, stav7, pozicia7, kontaktna_osoba7, vek7, miesto_narodenia7, bydlisko7 = "ethan", hashlib.sha3_256("ethan".encode()).hexdigest(), "Ethan", "Lee", 0, "Falcon", 190, 90, "Out of office", "Veliteľ taktického tímu", "Olivia Thompson", 35, "Sydney, Austrália", "380 Street, Canberra, Austrália"
username8, password8, meno8, priezvisko8, is_admin8, krycie_meno8, vyska8, vaha8, stav8, pozicia8, kontaktna_osoba8, vek8, miesto_narodenia8, bydlisko8 = "ava", hashlib.sha3_256("ava".encode()).hexdigest(), "Ava", "Wilson", 0, "Serpent", 175, 65, "Out of office", "Infiltračný špecialista", "Ryan Davis", 31, "Toronto, Kanada", "420 Street, Vancouver, Kanada"
username9, password9, meno9, priezvisko9, is_admin9, krycie_meno9, vyska9, vaha9, stav9, pozicia9, kontaktna_osoba9, vek9, miesto_narodenia9, bydlisko9 = "benjamin", hashlib.sha3_256("benjamin".encode()).hexdigest(), "Benjamin", "Martin", 1, "Havoc", 180, 75, "Secret", "Hacker", "Lily Wilson", 29, "Los Angeles, USA", "42 Bulvar Street, San Francisco, USA"
username10, password10, meno10, priezvisko10, is_admin10, krycie_meno10, vyska10, vaha10, stav10, pozicia10, kontaktna_osoba10, vek10, miesto_narodenia10, bydlisko10 = "isabella", hashlib.sha3_256("isabella".encode()).hexdigest(), "Isabella", "Rossi", 1, "Tigeress", 165, 55, "In office", "Lingvistický analytik", "Marco Bianchi", 33, "Rím, Taliansko", "4 Pizza Street, Miláno, Taliansko"

cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username1, password1, is_admin1, meno1, priezvisko1, krycie_meno1, vyska1, vaha1, stav1, pozicia1, kontaktna_osoba1, vek1, miesto_narodenia1, bydlisko1))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username2, password2, is_admin2, meno2, priezvisko2, krycie_meno2, vyska2, vaha2, stav2, pozicia2, kontaktna_osoba2, vek2, miesto_narodenia2, bydlisko2))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username3, password3, is_admin3, meno3, priezvisko3, krycie_meno3, vyska3, vaha3, stav3, pozicia3, kontaktna_osoba3, vek3, miesto_narodenia3, bydlisko3))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username4, password4, is_admin4, meno4, priezvisko4, krycie_meno4, vyska4, vaha4, stav4, pozicia4, kontaktna_osoba4, vek4, miesto_narodenia4, bydlisko4))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username5, password5, is_admin5, meno5, priezvisko5, krycie_meno5, vyska5, vaha5, stav5, pozicia5, kontaktna_osoba5, vek5, miesto_narodenia5, bydlisko5))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username6, password6, is_admin6, meno6, priezvisko6, krycie_meno6, vyska6, vaha6, stav6, pozicia6, kontaktna_osoba6, vek6, miesto_narodenia6, bydlisko6))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username7, password7, is_admin7, meno7, priezvisko7, krycie_meno7, vyska7, vaha7, stav7, pozicia7, kontaktna_osoba7, vek7, miesto_narodenia7, bydlisko7))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username8, password8, is_admin8, meno8, priezvisko8, krycie_meno8, vyska8, vaha8, stav8, pozicia8, kontaktna_osoba8, vek8, miesto_narodenia8, bydlisko8))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username9, password9, is_admin9, meno9, priezvisko9, krycie_meno9, vyska9, vaha9, stav9, pozicia9, kontaktna_osoba9, vek9, miesto_narodenia9, bydlisko9))
cur.execute("INSERT INTO userdata (username, password, is_admin, meno, priezvisko, krycie_meno, vyska, vaha, stav, pozicia, kontaktna_osoba, vek, miesto_narodenia, bydlisko) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username10, password10, is_admin10, meno10, priezvisko10, krycie_meno10, vyska10, vaha10, stav10, pozicia10, kontaktna_osoba10, vek10, miesto_narodenia10, bydlisko10))

cur.execute("INSERT INTO dochadzka (id_pouzivatela, meno, priezvisko, krycie_meno, datum, pocet_hodin) VALUES (?,?,?,?,?,?)", (1, "Administrátor", "Systému", "admin", "27.6.2023", 8))

cur.execute("INSERT INTO akcie (id_pouzivatela, krycie_meno, nazov_akcie, ucastnici, miesto, okruh_sledovanych, datum_od_do) VALUES (?,?,?,?,?,?,?)", (1, "Admin", "Shadow Strike", "Shadow, Karen", "Irak", "ISIS", "27.6.2023-teraz"))

conn.commit()
