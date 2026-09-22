# GEV-Wahlhelfer

Wahlen der Gesamtelternvertretung an einer Berliner Schule: Kandidaturen und Ergebnisse
an der Wand, danach die Wahlniederschrift.

`index.html` doppelklicken. Kein Server, keine Installation, kein Netz.
`papaparse.min.js` gehört daneben. Fehlt sie, holt die Seite sie von cdnjs; ohne Netz
geht dann alles außer dem Lesen der Vertreterliste.

## Ablauf

1. Einrichtung: Kopfdaten, Fachkonferenzen, Liste laden
2. Wahlgang wählen, Kandidaturen aufnehmen, Stimmen eintragen
3. Stand sichern
4. Niederschrift: drucken, dabei die Kopf- und Fußzeilen des Browsers abschalten

Die Seitenzahl im unteren Seitenrand setzen nur Chromium, Chrome und Edge. Firefox lässt
sie weg.

## Wahlleitung

In den Kopf der Niederschrift kommt, wer die meisten Wahlgänge geleitet hat; jeder
abweichende Wahlgang nennt seine Leitung selbst. Unterschrieben wird von allen, die
mindestens einen Wahlgang geleitet haben.

## Fachkonferenzen

Fachkonferenzen werden kommagetrennt eingetragen. Sie lassen sich durch Semikolon in
Blöcke mit eigener Überschrift gliedern. Ein Blockname kann mit Doppelpunkt vor den
Block gesetzt werden, Beispiel:

```
Schiene 1: Ma, Ph, Inf; Schiene 2: De, En/Frz; Sp, Mu
```

Wird jemand als beratendes Mitglied in zwei Fachkonferenzen desselben Blocks
aufgestellt, erscheint ein Hinweis — bei Stellvertretungen nicht.

## Liste und Stand

Zwei Dateien, zwei Zwecke:

* **Vertreterliste**, eine CSV — der Namensvorrat, aus dem die Kandidaturen kommen.
  Laden lässt Kopfdaten, Kandidaturen und Stimmen unberührt.
* **Stand**, eine JSON — die ganze Sitzung, ggf. inklusive Mitgliederliste.

Für ein neues Schuljahr nimmt man die Liste, nicht den Stand.

### Vertreterliste

CSV, UTF-8. Pflicht ist nur `Name`.

```
Klasse;Vorname;Name;E-Mail
5.1;Annika;Sonnenberg;annika.sonnenberg@example.org
11;Olga;Lerchenfeld;olga.lerchenfeld@example.org
```

Beispiele liegen in `beispiel/`.

Wer mehrere Klassen vertritt, darf in mehreren Zeilen stehen: Bei gleichem Namen und
gleicher Adresse werden sie zu einer Person mit allen Klassen zusammengefasst. Gleiche
Namen mit verschiedenen Adressen bleiben getrennt — das sind Namensvettern.

Ohne Adresse ist beides nicht zu unterscheiden; solche Zeilen bleiben getrennt, und die
Seite sagt es beim Laden. Vollständig gleiche Zeilen werden als Erfassungsfehler
gemeldet.

## Lizenz

MIT, siehe `LICENSE`. `papaparse.min.js` ebenfalls MIT, Copyright (c) 2023 Matthew Holt.
