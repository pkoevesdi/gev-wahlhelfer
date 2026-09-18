# GEV-Wahlhelfer

Wahlen der Gesamtelternvertretung an einer Berliner Schule: Kandidaturen und
Ergebnisse für den Beamer, danach das ausgefüllte amtliche Wahlprotokoll.

`index.html` doppelklicken. Kein Server, keine Installation, kein Netz.

## Ablauf

1. Einrichtung: Kopfdaten, Fachkonferenzen, Liste laden
2. Wahlgang wählen, Kandidaturen aufnehmen, Stimmen eintragen
3. Stand sichern
4. Protokoll erzeugen:

```sh
sudo apt install python3-reportlab python3-pypdf   # einmalig
python3 protokoll.py wahlstand.json
```

## Liste

CSV, UTF-8. Pflicht ist nur `Name`.

```
Klasse;Vorname;Name;E-Mail
5.1;Annika;Sonnenberg;annika.sonnenberg@example.org
11;Olga;Lerchenfeld;olga.lerchenfeld@example.org
```

Eine Zeile mit `Typ` = `Fachkonferenz` nimmt zusätzlich Fächer auf.
Beispiele liegen in `beispiel/`.

## Vorlage

`vorlage.pdf` nennt keine Lizenz und liegt deshalb nicht im Repository. `protokoll.py`
holt sie beim ersten Lauf von den
[Berliner Elternfortbildner*innen](https://www.berliner-elternvideos.de/elternfortbildner/)
und prüft, ob die Feldkoordinaten noch passen.

Die Koordinaten in `pdfkarte.json` sind an der Fassung vom 21.08.2026 gemessen,
13 Seiten, SHA-256 `8719bef2aa674a3a6b404b3310a6637bc9544ee4771df7535d05152f8b972227`.

## Lizenz

MIT, siehe `LICENSE`. `papaparse.min.js` ebenfalls MIT, Copyright (c) 2023 Matthew Holt.
