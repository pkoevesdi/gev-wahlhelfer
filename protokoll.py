#!/usr/bin/env python3
"""Erzeugt das Wahlprotokoll aus dem Zwischenstand des Werkzeugs.

    python3 protokoll.py wahlstand.json [Wahlprotokoll.pdf]

Ohne Zielnamen entsteht die PDF neben der Eingabedatei.
Die amtliche Vorlage wird beim ersten Lauf geholt.
"""
import hashlib, json, sys, io, os, urllib.request
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import white, black
    from pypdf import PdfReader, PdfWriter
except ModuleNotFoundError as e:
    sys.exit('Es fehlt: %s\n\n'
             'Unter Debian und Ubuntu:\n'
             '    sudo apt install python3-reportlab python3-pypdf\n\n'
             'Sonst in einer virtuellen Umgebung:\n'
             '    python3 -m venv .venv && .venv/bin/pip install reportlab pypdf\n'
             '    .venv/bin/python protokoll.py ...' % e.name)

HIER = os.path.dirname(os.path.abspath(__file__))
VORLAGE = os.path.join(HIER, 'vorlage.pdf')
KARTE   = json.load(open(os.path.join(HIER, 'pdfkarte.json')))
H = 841.89
def y(top): return H - top

# Das amtliche Wahlprotokoll der Berliner Elternfortbildner*innen. Es nennt keine
# Lizenz und liegt deshalb nicht im Repository.
VORLAGE_URL = ('https://www.berliner-elternvideos.de/elternfortbildner/downloads/'
               'wahlprotokoll-fuer-die-gev.pdf')
# Fassung, aus der die Feldkoordinaten in pdfkarte.json gemessen sind
VORLAGE_SHA256 = '8719bef2aa674a3a6b404b3310a6637bc9544ee4771df7535d05152f8b972227'

def vorlage_bereitstellen():
    if not os.path.exists(VORLAGE):
        print('hole %s' % VORLAGE_URL)
        try:
            with urllib.request.urlopen(VORLAGE_URL, timeout=60) as r, open(VORLAGE, 'wb') as f:
                f.write(r.read())
        except Exception as e:
            sys.exit('Die Vorlage liess sich nicht laden (%s).\n'
                     'Von Hand herunterladen und als %s ablegen:\n  %s' % (e, VORLAGE, VORLAGE_URL))
    ist = hashlib.sha256(open(VORLAGE, 'rb').read()).hexdigest()
    if ist != VORLAGE_SHA256:
        print('ACHTUNG  vorlage.pdf weicht von der vermessenen Fassung ab.\n'
              '         erwartet %s\n         gefunden %s\n'
              '         Das Protokoll vor dem Gebrauch ansehen: Felder koennen verrutscht sein.'
              % (VORLAGE_SHA256, ist))

# vorstand_weitere: None = offen, die Zahl wird in der Versammlung beschlossen
SITZE = {'vorsitz':1,'stellv_vorsitz':3,'vorstand_weitere':None,'sk':4,'sk_stellv':8,'bea':2,
         'bea_stellv':4,'gk':2,'gk_stellv':4,'gsv':2,'gsv_stellv':4,'tk':1,'tk_stellv':2}

def txt(c, s, x, top, size=9, fett=False):
    """top ist die Oberkante der Linie im Formular; der Text sitzt 3 Punkt darueber."""
    if s in (None, ''): return
    c.setFont('Helvetica-Bold' if fett else 'Helvetica', size)
    c.setFillColor(black); c.drawString(x, y(top) + 3, str(s))

def zelle(c, s, z, size=9, rechts=False):
    if s in (None, ''): return
    x0, t0, x1, t1 = z
    c.setFont('Helvetica', size); c.setFillColor(black)
    yy = y(t1) + (t1-t0-size)/2 + size*0.25
    (c.drawRightString(x1-6, yy, str(s)) if rechts else c.drawString(x0+6, yy, str(s)))

def overlay(bauen):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(595.28, H))
    bauen(c); c.showPage(); c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]

def main(quellpfad, ziel):
    vorlage_bereitstellen()
    S = json.load(open(quellpfad))
    kopf, wg, faecher = S.get('kopf', {}), S.get('wahlgaenge', {}), S.get('faecher', [])
    w = PdfWriter()

    def nimm(idx, bauen):
        p = w.add_page(PdfReader(VORLAGE).pages[idx])   # je Ausgabeseite frisch, sonst stapeln sich die Overlays
        p.merge_page(overlay(bauen))

    def sortiert(wid):
        k = (wg.get(wid) or {}).get('kandidaten', [])
        return sorted(k, key=lambda x: -(int(x.get('stimmen') or 0)))

    def stempeln(c, pdfkey, wid, sitze):
        m = KARTE['wahlgaenge'].get(pdfkey)
        if not m: return
        d = wg.get(wid) or {}
        if d.get('sitze'): sitze = int(d['sitze'])
        if sitze is None: sitze = len(reihen)
        reihen = sortiert(wid)
        for i, k in enumerate(reihen):
            if i >= len(m['kand']): break
            zelle(c, k.get('name'), m['kand'][i][0])
            zelle(c, k.get('stimmen'), m['kand'][i][1], rechts=True)
        gew = [k for k in reihen if int(k.get('stimmen') or 0) > 0][:sitze]
        for i, k in enumerate(gew):
            if i >= len(m['erg']): break
            z = m['erg'][i]
            zelle(c, k.get('name'), z[0], 8.5)
            if len(z) > 1: zelle(c, k.get('mail'), z[1], 8.5)
        if d.get('abgegeben') and m.get('abg'):
            txt(c, d['abgegeben'], m['abg'][0], m['abg'][1])

    K = KARTE['kopf']
    def s1(c):
        txt(c, kopf.get('schule'),     K['schule'][0],     K['schule'][1],     10)
        txt(c, kopf.get('datum'),      K['datum'][0],      K['datum'][1],      10)
        txt(c, kopf.get('anwesendW'),  K['anwesend_w'][0], K['anwesend_w'][1], 10)
        txt(c, kopf.get('anwesendS'),  K['anwesend_s'][0], K['anwesend_s'][1], 10)
        txt(c, kopf.get('wahlleitung'),K['wahlleitung'][0],K['wahlleitung'][1],10)
        stempeln(c, 'vorsitz', 'vorsitz', SITZE['vorsitz'])
    nimm(0, s1)
    nimm(1, lambda c: stempeln(c, 'stellv_vorsitz', 'stellv_vorsitz', SITZE['stellv_vorsitz']))

    zw = wg.get('vorstand_weitere') or {}
    if zw.get('kandidaten'):
        Z = KARTE['zusatz']; m = KARTE['wahlgaenge']['stellv_vorsitz']
        reihen = sortiert('vorstand_weitere')
        grenze = int(zw['sitze']) if zw.get('sitze') else None
        gew = [k for k in reihen if int(k.get('stimmen') or 0) > 0]
        if grenze: gew = gew[:grenze]
        pro = len(m['erg'])
        blaetter = max(1, -(-len(gew) // pro))
        for bi in range(blaetter):
            def zusatz(c, bi=bi):
                for t0, t1 in Z['deckel']:
                    c.setFillColor(white); c.rect(50, y(t1), 510, t1-t0, stroke=0, fill=1)
                zusatzt = ' (%d von %d)' % (bi+1, blaetter) if blaetter > 1 else ''
                txt(c, 'Kandidierende für weitere Mitglieder im Vorstand der GEV' + zusatzt,
                    Z['titel_kand'][0], Z['titel_kand'][1], 8)
                txt(c, 'Wahlergebnis weitere Mitglieder im Vorstand der GEV',
                    Z['titel_erg'][0], Z['titel_erg'][1], 10, fett=True)
                if bi == 0:
                    for i, k in enumerate(reihen):
                        if i >= len(m['kand']): break
                        zelle(c, k.get('name'), m['kand'][i][0])
                        zelle(c, k.get('stimmen'), m['kand'][i][1], rechts=True)
                    if zw.get('abgegeben') and m.get('abg'):
                        txt(c, zw['abgegeben'], m['abg'][0], m['abg'][1])
                for i, k in enumerate(gew[bi*pro:(bi+1)*pro]):
                    z = m['erg'][i]
                    zelle(c, k.get('name'), z[0], 8.5)
                    if len(z) > 1: zelle(c, k.get('mail'), z[1], 8.5)
            nimm(1, zusatz)

    for idx, wid in ((2,'sk'),(3,'sk_stellv'),(4,'bea'),(5,'bea_stellv'),
                     (6,'gk'),(7,'gk_stellv'),(8,'gsv'),(9,'gsv_stellv')):
        nimm(idx, (lambda wid=wid: lambda c: stempeln(c, wid, wid, SITZE[wid]))())

    for fach in faecher:
        def fkseite(c, fach=fach):
            txt(c, fach, K['fach'][0], K['fach'][1], 10)
            stempeln(c, 'fk',        'fk::'  + fach, 2)
            stempeln(c, 'fk_stellv', 'fks::' + fach, 4)
        nimm(10, fkseite)

    def tkseite(c):
        if kopf.get('teilkonferenz'):
            txt(c, kopf['teilkonferenz'], K['tk_fuer'][0],  K['tk_fuer'][1], 10)
            txt(c, kopf['teilkonferenz'], K['tk_fuer2'][0], K['tk_fuer2'][1], 10)
        stempeln(c, 'tk',        'tk',        SITZE['tk'])
        stempeln(c, 'tk_stellv', 'tk_stellv', SITZE['tk_stellv'])
    nimm(11, tkseite)
    nimm(12, lambda c: None)

    with open(ziel, 'wb') as f: w.write(f)
    print('%s — %d Seiten' % (ziel, len(w.pages)))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip())
    quelle = sys.argv[1]
    ziel = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(quelle)[0] + '.pdf'
    main(quelle, ziel)
