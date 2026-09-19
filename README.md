# GEV-Wahlhelfer

Wahlen der Gesamtelternvertretung an einer Berliner Schule: Kandidaturen und
Ergebnisse an der Wand, danach die Wahlniederschrift.

`index.html` doppelklicken. Kein Server, keine Installation, kein Netz.

## Ablauf

1. Einrichtung: Kopfdaten, Fachkonferenzen, Liste laden
2. Wahlgang wählen, Kandidaturen aufnehmen, Stimmen eintragen
3. Stand sichern
4. Niederschrift: Ansicht öffnen, drucken, im Druckdialog „Als PDF speichern“ wählen
   und die Kopf- und Fußzeilen des Browsers abschalten

Die Seitenzahl im unteren Seitenrand setzen nur Chromium, Chrome und Edge. Firefox
lässt sie weg.

## Liste und Stand

Zwei Dateien, zwei Zwecke:

* **Vertreterliste**, eine CSV — der Namensvorrat, aus dem die Kandidaturen kommen.
  Laden lässt Kopfdaten, Kandidaturen und Stimmen unberührt.
* **Stand**, eine JSON — die ganze Sitzung. Laden ersetzt sie vollständig; stehen
  schon Stimmen, wird vorher gefragt.

Ein Stand enthält den Namensvorrat mit, die Liste ist dann nicht mehr nötig. Für das
nächste Schuljahr nimmt man die Liste, nicht den Stand.

### Vertreterliste

CSV, UTF-8. Pflicht ist nur `Name`.

```
Klasse;Vorname;Name;E-Mail
5.1;Annika;Sonnenberg;annika.sonnenberg@example.org
11;Olga;Lerchenfeld;olga.lerchenfeld@example.org
```

Beispiele liegen in `beispiel/`.

Wer zwei Klassen vertritt, darf in zwei Zeilen stehen: Bei gleichem Namen und gleicher
Adresse werden sie zu einer Person mit beiden Klassen zusammengefasst. Gleiche Namen
mit verschiedenen Adressen bleiben getrennt — das sind Namensvettern.

Ohne Adresse ist beides nicht zu unterscheiden; solche Zeilen bleiben getrennt, und die
Seite sagt es beim Laden. Vollständig gleiche Zeilen werden als Erfassungsfehler gemeldet.

## Lizenz

MIT, siehe `LICENSE`. `papaparse.min.js` ebenfalls MIT, Copyright (c) 2023 Matthew Holt.
