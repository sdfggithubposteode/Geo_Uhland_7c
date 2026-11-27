"""Erzeugt index.html (GeoLern) aus der Bio-Vorlage.

Liest GitHub_Bio_Uhland_7c/index.html, ersetzt Inhalte durch die
Geo-Version (Innere Tropen, KA Kl. 7c) und erzeugt zwei statische
SVG-Diagramme (Klimadiagramm Manaus, Ertrags-Säulendiagramm).
Danach: python build_beschriftung.py  (füllt den IMGS-Block)
"""

import json
import os
import re

BIO_INDEX = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "GitHub_Bio_Uhland_7c", "index.html")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

# ---------------------------------------------------------------- Fragen
# [Thema, Frage, richtige Antwort, [3 falsche], Erklärung, Kontrast]
Q = [
    # ---- Lage ----
    ["Lage", "Zwischen welchen beiden Linien liegen die inneren Tropen?",
     "Zwischen nördlichem und südlichem Wendekreis",
     ["Zwischen Äquator und Polarkreis", "Zwischen den beiden Polarkreisen",
      "Zwischen nördlichem Wendekreis und Nordpol"],
     "Die inneren Tropen umfassen den Gürtel um den Äquator, begrenzt durch die Wendekreise bei ca. 23,5° Nord und Süd.",
     "Polarkreise liegen bei 66,5° – sie begrenzen die Polarzonen, nicht die Tropen."],
    ["Lage", "Welche drei Regionen gehören zu den großen Regenwaldgebieten der Erde?",
     "Amazonasbecken, Kongobecken und Südostasien",
     ["Sahara, Kalahari und Arabische Halbinsel", "Mittelmeerraum, Anden und Alpen",
      "Kanada, Skandinavien und Sibirien"],
     "Tropischer Regenwald wächst im Amazonasbecken (Südamerika), im Kongobecken (Afrika) und in Südostasien (u. a. Indonesien).",
     "Sahara und Kalahari sind Wüsten; Mittelmeerraum und die nördlichen Nadelwälder gehören zu anderen Klimazonen."],
    ["Lage", "Wo liegt das größte zusammenhängende Gebiet tropischen Regenwalds?",
     "Im Amazonasbecken in Südamerika",
     ["In Zentralafrika entlang des Äquators", "Auf den Inseln Südostasiens",
      "In Mittelamerika"],
     "Der Amazonas-Regenwald ist mit Abstand das größte geschlossene Tropenwaldgebiet der Erde.",
     "Kongobecken und Südostasien sind die zweit- und drittgrößten Gebiete."],
    ["Lage", "Was ist das Besondere am Sonnenstand in den inneren Tropen?",
     "Die Sonne steht im Laufe des Jahres zweimal im Zenit über einem Ort.",
     ["Die Sonne steht das ganze Jahr genau im Zenit.", "Die Sonne geht nie unter.",
      "Die Sonne steht immer nur flach am Horizont."],
     "Zwischen den Wendekreisen steht die Sonne zweimal im Jahr senkrecht über einem Ort – das sorgt für die ganzjährig hohe Energiezufuhr.",
     "Nur an den Wendekreisen selbst steht sie einmal im Zenit; flacher Sonnenstand ist typisch für hohe Breiten."],

    # ---- Klima ----
    ["Klima", "Was ist das Kennzeichen des Tageszeitenklimas in den Tropen?",
     "Die Temperaturunterschiede zwischen Tag und Nacht sind größer als zwischen den Monaten.",
     ["Die Temperaturunterschiede zwischen den Monaten sind größer als zwischen Tag und Nacht.",
      "Es gibt große Temperaturunterschiede zwischen Sommer und Winter.",
      "Tag und Nacht sind immer genau gleich warm."],
     "Im Tageszeitenklima schwankt die Temperatur zwischen Tag und Nacht stärker als zwischen den Monaten – es gibt keine echten Jahreszeiten.",
     "Starke Monatsunterschiede sind das Kennzeichen des Jahreszeitenklimas in den gemäßigten Breiten."],
    ["Klima", "Wie verläuft die Temperaturkurve im Klimadiagramm von Manaus?",
     "Nahezu waagrecht bei etwa 26 bis 28 °C",
     ["Deutlich schwankend zwischen 0 und 30 °C", "Nur im Winter über 20 °C",
      "Mit einem tiefen Einbruch im Januar"],
     "Manaus zeigt die typische Tropen-Temperaturkurve: ganzjährig konstant warm, Jahresmittel ca. 27 °C.",
     "Starke Schwankungen und Wintereinbrüche gehören zu den gemäßigten Breiten."],
    ["Klima", "Wie sind die Niederschläge in Manaus verteilt?",
     "Ganzjährig hoch, mit einer regenärmeren Zeit etwa von Juni bis September.",
     ["Nur im Sommer, im Winter fällt kein Regen.", "Das ganze Jahr über fast kein Regen.",
      "Genau gleichmäßig über alle Monate verteilt."],
     "In Manaus fällt ganzjährig Regen; von Juni bis September sinken die Werte deutlich (auf ca. 40–100 mm), es bleibt aber humid.",
     "Eine echte Trockenzeit mit fast keinem Regen gibt es in den inneren Tropen nicht – das wäre typisch für die äußeren Tropen."],
    ["Klima", "Wann gilt ein Monat im Klimadiagramm als humid (feucht)?",
     "Wenn die Niederschlagssäule über der Temperaturkurve liegt.",
     ["Wenn die Temperaturkurve über der Niederschlagssäule liegt.",
      "Wenn beide Linien genau aufeinander liegen.", "Wenn es kälter als 10 °C ist."],
     "Liegt die Niederschlagskurve über der Temperaturkurve, fällt mehr Regen als verdunstet – der Monat gilt als humid.",
     "Temperatur über Niederschlag bedeutet arid (trocken), nicht feucht."],

    # ---- Wetter ----
    ["Wetter", "Wie sieht ein typischer Tagesablauf des Wetters in den Tropen aus?",
     "Morgens klar → mittags Quellwolken → nachmittags Hitzegewitter → abends Aufklaren",
     ["Morgens Gewitter → mittags klar → nachmittags Nebel",
      "Den ganzen Tag gleichmäßiger Regen",
      "Morgens Nebel → mittags Schnee → abends Sturm"],
     "Die feuchte Luft erwärmt sich über Tag, quellt zu Wolken auf und entlädt sich am Nachmittag als Hitzegewitter.",
     "Dauerregen und Schnee sind keine typischen Tropen-Wetter."],
    ["Wetter", "Warum gibt es in den Tropen fast täglich am Nachmittag Gewitter?",
     "Die stark erwärmte, feuchte Luft steigt auf und kühlt ab – der Wasserdampf kondensiert zu Gewitterwolken.",
     ["Weil jeden Tag eine Kaltfront durchzieht.", "Weil die Berge die Luft nach oben drücken.",
      "Weil der Wind am Abend aus dem Meer Regen bringt."],
     "Hohe Bodentemperatur lässt feuchte Luft aufsteigen; in der Höhe kondensiert der Wasserdampf zu Wolken – Hitzegewitter (Luftmassengewitter).",
     "Frontgewitter gibt es vor allem in den gemäßigten Breiten; orographische Gewitter brauchen Berge."],
    ["Wetter", "Was ist die ITC (innertropische Konvergenzzone)?",
     "Der Bereich am Äquator, wo die Passatwinde aufeinandertreffen und die Luft aufsteigt.",
     ["Eine Wüstenzone in den Wendekreisen.", "Die Grenze zwischen Tag und Nacht.",
      "Ein Hochdruckgebiet über dem Polarkreis."],
     "In der ITC treffen die Passate aus Norden und Süden zusammen; die aufsteigende feuchte Luft bringt Wolken und Regen.",
     "Die Wendekreise sind eher trockene Hochdruckzonen; die ITC liegt am Äquator."],
    ["Wetter", "Wohin strömen die Passatwinde bodennah?",
     "Von den Wendekreisen zum Äquator.",
     ["Vom Äquator zu den Wendekreisen.", "Von den Polen zum Äquator.",
      "Immer von West nach Ost um die Erde."],
     "Die aufsteigende Luft am Äquator erzeugt einen Sog: Bodennah strömen die Luftmassen als Passatwinde aus den subtropischen Hochdruckgürteln zum Äquator.",
     "In der Höhe fließt die Luft umgekehrt vom Äquator zu den Wendekreisen (Höhenwinde)."],
    ["Wetter", "Zwischen Blitz und Donner vergehen 9 Sekunden. Wie weit ist das Gewitter ungefähr weg?",
     "Etwa 3 km",
     ["Etwa 9 km", "Etwa 1 km", "Etwa 30 km"],
     "Der Schall braucht etwa 3 Sekunden pro Kilometer: Sekunden geteilt durch 3 ergibt die Entfernung – 9 Sekunden ≈ 3 km.",
     "Der Blitz ist fast sofort sichtbar (Licht ist viel schneller); nur die Sekundenzahl zählt, nicht mal 3."],

    # ---- Wald / Nährstoffe ----
    ["Wald", "Wie kann der tropische Regenwald auf nährstoffarmem Boden gedeihen?",
     "Die Nährstoffe stecken fast vollständig in der Biomasse und kreisen sehr schnell.",
     ["Der Boden dort ist besonders fruchtbar.", "Die Bäume brauchen keine Nährstoffe.",
      "Der Regen bringt jeden Tag neue Nährstoffe mit."],
     "Der schnelle Nährstoffkreislauf entschädigt für den armen Boden: Nährstoffe wandern rasch von abgestorbener Substanz über Zersetzung zurück in die Pflanzen.",
     "Der Boden ist gerade arm – die dicke Humusschicht gehört zum Laubwald, nicht zum Regenwald."],
    ["Wald", "Wie dick ist die Humusschicht im tropischen Regenwald im Vergleich zum Laubmischwald?",
     "Viel dünner – beim Laubwald ist sie bis ca. 15 cm dick, im Regenwald fast nicht vorhanden.",
     ["Genau gleich dick.", "Im Regenwald doppelt so dick.",
      "Es gibt in beiden Wäldern keinen Humus."],
     "Aus eurem Vergleich: Laubmischwald ca. 15 cm dicke Humusschicht – Regenwald nur eine sehr dünne Streuschicht.",
     "Im Regenwald wird abgefallenes Material so schnell zersetzt und aufgenommen, dass sich kaum Humus bildet."],
    ["Wald", "Wie wachsen die Wurzeln der Regenwaldbäume?",
     "Flach – viele bilden Brettwurzeln als Stütze aus.",
     ["Sehr tief bis ins Grundwasser.", "Gar nicht, die Bäume stehen ohne Wurzeln.",
      "Nur gerade nach unten wie eine Pfahlwurzel."],
     "Die Nährstoffe liegen direkt an der Oberfläche – die Bäume wurzeln flach und stabilisieren sich mit Brettwurzeln.",
     "Tief wurzeln lohnt nicht: Weiter unten gibt es kaum Nährstoffe; das ist eher typisch für Trockengebiete."],
    ["Wald", "Welche Baumschicht ragt über das geschlossene Kronendach hinaus?",
     "Die Emergentschicht (Überholer)",
     ["Die Krautschicht", "Die Strauchschicht", "Das erste Oberschoss"],
     "Einzelne Riesenbäume (Emergents/Überholer) ragen bis zu 60 m hoch über das Kronendach.",
     "Kraut-, Strauch- und Baumschichten liegen alle unter dem Überholer."],
    ["Wald", "Was sind Epiphyten?",
     "Pflanzen, die auf anderen Pflanzen sitzen, ohne sie zu schädigen.",
     ["Schmarotzer, die Bäume abtöten.", "Kletterpflanzen mit Dornen.",
      "Wurzeln, die aus dem Boden ragen."],
     "Epiphyten (Aufsitzerpflanzen) wie Bromelien wachsen auf Ästen, um ans Licht zu kommen – sie sind keine Parasiten.",
     "Kletterpflanzen mit Stämmen sind Lianen; Parasiten entziehen dem Wirt Nährstoffe."],

    # ---- Menschen ----
    ["Menschen", "Wie funktioniert der Brandrodungsfeldbau?",
     "Wald roden → trocknen → abbrennen → einige Jahre anbauen → Fläche verlassen",
     ["Wald roden → sofort düngen → dauerhaft anbauen",
      "Wald stehen lassen → zwischen den Bäumen säen",
      "Regenwald abholzen → Plantage anlegen → Maschinen einsetzen"],
     "Beim Brandrodungsfeldbau wird ein Waldstück gefällt und verbrannt; die Asche düngt den Boden für ein paar Jahre, dann zieht man weiter.",
     "Dauerhafter Anbau ohne Brache oder Maschineneinsatz beschreibt moderne Landwirtschaft, nicht den Wanderfeldbau."],
    ["Menschen", "Warum sinken die Erträge beim Brandrodungsfeldbau schon nach wenigen Jahren?",
     "Die Nährstoffe aus der Asche sind verbraucht oder ausgewaschen und bilden sich nicht nach.",
     ["Die Pflanzen werden jedes Jahr kleiner.", "Das Feld bekommt zu viel Schatten.",
      "Das Klima ändert sich nach drei Jahren."],
     "Die Asche liefert nur einmalig Nährstoffe; ohne Humusneubildung sind sie nach 3–4 Jahren weg – das Feld muss brach liegen.",
     "Der Ertragsrückgang hat Bodenursachen, nicht Klimawandel oder Pflanzengröße."],
    ["Menschen", "Wie heißt das große Gemeinschaftshaus der Yanomami?",
     "Shabono (auch Maloca genannt)",
     ["Tipi", "Iglo", "Pfahlbau"],
     "Das Shabono ist ein großes Rundhaus aus Palmblättern, in dem die ganze Gemeinschaft um einen zentralen Platz wohnt.",
     "Tipi, Iglu und Pfahlbau gehören zu anderen Kulturen und Klimazonen."],
    ["Menschen", "Warum gefährden Straßenbau und Bodenschätze die Yanomami?",
     "Sie bringen Krankheiten ein und locken Raubbau an ihrem Lebensraum an.",
     ["Sie machen den Wald grüner.", "Sie verbessern die Ernährung der Yanomami.",
      "Sie haben gar keine Auswirkungen."],
     "Seit den 1950er-Jahren bedrohen Straßenbau, eingeschleppte Krankheiten und der Bergbau (Gold, Uran) das Überleben der Yanomami.",
     "Der Kontakt mit der Außenwelt war für das Volk bisher vor allem verheerend."],

    # ---- Nutzung ----
    ["Nutzung", "Was ist eine Plantage?",
     "Eine riesige Pflanzung in den Tropen mit Monokultur für den Export.",
     ["Ein kleiner Familiengarten.", "Ein Mischwald aus heimischen Bäumen.",
      "Ein Naturschutzgebiet."],
     "Auf Plantagen werden einzelne Kulturen (z. B. Ölpalmen, Zucker, Kaffee, Kakao) in Monokultur in großem Stil für den Export angebaut.",
     "Plantagen sind genau das Gegenteil von kleinbäuerlicher oder naturnaher Nutzung."],
    ["Nutzung", "Was ist der Nachteil einer Monokultur?",
     "Hohe Anfälligkeit für Schädlinge und Krankheiten trotz hoher Erträge.",
     ["Sie erzeugt keinerlei Erträge.", "Sie kann nur einmal im Jahr bepflanzt werden.",
      "Sie verbraucht mehr Wasser als Wüsten."],
     "Nur eine Pflanzenart = einfache Bearbeitung und hohe Erträge, aber Schädlinge und Krankheiten können sich schnell ausbreiten.",
     "Monokulturen sind gerade wegen der hohen Erträge beliebt – der Nachteil ist die Anfälligkeit."],
    ["Nutzung", "Warum ist Palmöl auf dem Weltmarkt so erfolgreich?",
     "Es ist das billigste Pflanzenöl – ertragreich, neutral im Geschmack und lange haltbar.",
     ["Es wächst nur in Deutschland.", "Es ist das teuerste Pflanzenöl.",
      "Es kann nur für Kosmetik benutzt werden."],
     "Die Ölpalme ist ertragreicher als andere Ölpflanzen und braucht weniger Fläche; das Öl ist geschmacksneutral, gut erhitzbar und macht Cremes streichfest.",
     "Palmöl wird fast ausschließlich in den Tropen produziert und ist vor allem billig."],
    ["Nutzung", "Was passiert nach der Abholzung mit dem Regenwasser?",
     "Es fließt als Oberflächenabfluss ab und spült Nährstoffe und Boden fort.",
     ["Es versickert besser als vorher.", "Es bleibt in den Baumstümpfen stehen.",
      "Es verdunstet sofort vollständig."],
     "Ohne Blätterdach und Wurzeln versickert der Regen kaum; er läuft oberflächlich ab, verursacht Erosion und trägt die Nährstoffe davon.",
     "Der intakte Wald hingegen bremst den Regen, speichert ihn und lässt ihn versickern."],
    ["Nutzung", "Wie wirkt sich die Abholzung auf das lokale Klima aus?",
     "Weniger Verdunstung → weniger Regen und stärkere Temperaturschwankungen.",
     ["Es wird dort feuchter und kühler.", "Das Klima bleibt völlig gleich.",
      "Es regnet danach nur noch nachts."],
     "Der Wald gibt über Verdunstung Wasserdampf an die Atmosphäre zurück; ohne ihn sinken die Niederschläge und die Temperatur schwankt (tagsüber bis 50 °C, nachts unter 20 °C).",
     "Das Kahlschlagen macht das Klima extremer, nicht milder."],

    # ---- Schutz ----
    ["Schutz", "Wofür steht das RSPO-Siegel auf Produkten?",
     "Für zertifiziert nachhaltiges Palmöl.",
     ["Für besonders billiges Palmöl.", "Für palmölfreie Produkte.",
      "Für Produkte aus Deutschland."],
     "RSPO zertifiziert nachhaltig produziertes Palmöl – Plantagen müssen dafür Umwelt- und Sozialstandards einhalten.",
     "Das Siegel kennzeichnet die Art der Produktion, nicht den Preis oder das Fehlen von Palmöl."],
    ["Schutz", "Was bedeutet Nachhaltigkeit in der Landwirtschaft?",
     "So wirtschaften, dass die Böden langfristig nutzbar bleiben und die Natur nicht geschädigt wird.",
     ["So schnell wie möglich den Boden ausnutzen.", "Nur auf die Erträge achten.",
      "Alles auf eine Kultur setzen."],
     "Nachhaltig heißt: künftige Generationen sollen den Boden genauso nutzen können – ohne die Natur zu zerstören.",
     "Kurzfristige Maximierung ist das Gegenteil von Nachhaltigkeit."],
    ["Schutz", "Warum hilft es dem Regenwald, weniger Fleisch zu essen?",
     "Für Rinderweiden und Futtermittel-Anbau wird in Südamerika viel Regenwald gerodet.",
     ["Fleisch macht den Regenwald feuchter.", "Weil Rinder Regenwald fressen.",
      "Es hilft gar nicht."],
     "Weideland und Futtermittel-Plantagen gehören zu den Haupttreibern der Abholzung – Bio-Fleisch aus deutscher Haltung ist die bessere Wahl.",
     "Der Zusammenhang läuft über die Flächennutzung, nicht über das Verhalten der Tiere."],
]

assert len(Q) == len({id(q[1]) for q in Q}) == len(Q)

# ---------------------------------------------------------------- Diagramm-Helper
MONTHS = "J F M A M J J A S O N D".split()


def svg_climate():
    W, H = 560, 360
    L, R, T, B = 52, 60, 28, 34
    pw, ph = W - L - R, H - T - B
    tmax, nmax = 60, 300  # 1 °C = 5 mm
    temps = [26, 26, 26, 26, 26, 27, 27, 28, 28, 28, 28, 27]
    rain = [266, 247, 269, 267, 194, 100, 64, 38, 60, 124, 152, 216]
    bw = pw / 12
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Klimadiagramm Manaus" '
             f'style="width:100%;height:auto;display:block">',
             f'<text x="{W/2}" y="18" text-anchor="middle" font-weight="800" '
             f'font-size="15" fill="#1b3040">Klimadiagramm Manaus (Brasilien)</text>']
    # Gitter + Achsen
    for t in range(0, tmax + 1, 10):
        y = T + ph - t / tmax * ph
        parts.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+pw}" y2="{y:.1f}" stroke="#dce5de"/>')
        parts.append(f'<text x="{L-6}" y="{y+4:.1f}" text-anchor="end" font-size="10" fill="#5d7080">{t}</text>')
    for n in range(0, nmax + 1, 50):
        y = T + ph - n / nmax * ph
        parts.append(f'<text x="{L+pw+6}" y="{y+4:.1f}" font-size="10" fill="#5d7080">{n}</text>')
    parts.append(f'<text x="14" y="{T+ph/2}" text-anchor="middle" font-size="11" fill="#5d7080" transform="rotate(-90 14 {T+ph/2})">°C</text>')
    parts.append(f'<text x="{W-10}" y="{T+ph/2}" text-anchor="middle" font-size="11" fill="#5d7080" transform="rotate(-90 {W-10} {T+ph/2})">mm</text>')
    # Säulen + Linie
    pts = []
    for i, (t, n) in enumerate(zip(temps, rain)):
        x = L + i * bw
        y = T + ph - n / nmax * ph
        parts.append(f'<rect x="{x+2:.1f}" y="{y:.1f}" width="{bw-4:.1f}" '
                     f'height="{T+ph-y:.1f}" fill="#6fa8d8" stroke="#4a7fb5" rx="2"/>')
        ty = T + ph - t / tmax * ph
        pts.append((x + bw / 2, ty))
        parts.append(f'<text x="{x+bw/2:.1f}" y="{T+ph+14}" text-anchor="middle" '
                     f'font-size="11" fill="#5d7080">{MONTHS[i]}</text>')
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    parts.append(f'<polyline points="{line}" fill="none" stroke="#c0392b" stroke-width="2.5"/>')
    for x, y in pts:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#c0392b"/>')
    parts.append(f'<rect x="{L}" y="{T}" width="{pw}" height="{ph}" fill="none" stroke="#9db8ac"/>')
    parts.append('</svg>')
    return "".join(parts)


def svg_ertrag():
    W, H = 560, 330
    L, R, T, B = 52, 20, 40, 52
    pw, ph = W - L - R, H - T - B
    series = [("Maniok", "#3a9a74", [100, 75, 49, 18]),
              ("Mais", "#e8b13c", [100, 80, 60, 25]),
              ("Erdnuss", "#a45ec4", [100, 18, 3, 2])]
    years = ["1. Jahr", "2. Jahr", "3. Jahr", "4. Jahr"]
    gw = pw / 4
    bw = gw / 3
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Erträge Brandrodungsfeldbau" '
             f'style="width:100%;height:auto;display:block">',
             f'<text x="{W/2}" y="18" text-anchor="middle" font-weight="800" '
             f'font-size="15" fill="#1b3040">Ertrag beim Brandrodungsfeldbau (in %)</text>']
    for v in range(0, 101, 20):
        y = T + ph - v / 100 * ph
        parts.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+pw}" y2="{y:.1f}" stroke="#dce5de"/>')
        parts.append(f'<text x="{L-6}" y="{y+4:.1f}" text-anchor="end" font-size="10" fill="#5d7080">{v}</text>')
    parts.append(f'<text x="14" y="{T+ph/2}" text-anchor="middle" font-size="11" fill="#5d7080" transform="rotate(-90 14 {T+ph/2})">%</text>')
    for gi, yr in enumerate(years):
        gx = L + gi * gw
        for si, (name, color, vals) in enumerate(series):
            v = vals[gi]
            x = gx + si * bw + 2
            y = T + ph - v / 100 * ph
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw-4:.1f}" '
                         f'height="{T+ph-y:.1f}" fill="{color}" rx="2"/>')
        parts.append(f'<text x="{gx+gw/2:.1f}" y="{T+ph+16}" text-anchor="middle" '
                     f'font-size="11" fill="#5d7080">{yr}</text>')
    lx = L + 10
    for name, color, _ in series:
        parts.append(f'<rect x="{lx}" y="{H-18}" width="12" height="12" fill="{color}" rx="2"/>')
        parts.append(f'<text x="{lx+16}" y="{H-8}" font-size="11" fill="#1b3040">{name}</text>')
        lx += 16 + len(name) * 7 + 22
    parts.append(f'<rect x="{L}" y="{T}" width="{pw}" height="{ph}" fill="none" stroke="#9db8ac"/>')
    parts.append('</svg>')
    return "".join(parts)


def js_question(entry):
    topic, q, correct, wrong, explain, contrast = entry
    return "[" + ",".join([
        json.dumps(topic, ensure_ascii=False),
        json.dumps(q, ensure_ascii=False),
        json.dumps(correct, ensure_ascii=False),
        json.dumps(wrong, ensure_ascii=False),
        json.dumps(explain, ensure_ascii=False),
        json.dumps(contrast, ensure_ascii=False),
    ]) + "]"


def main():
    with open(BIO_INDEX, encoding="utf-8") as f:
        html = f.read()

    # --- Kopf / Branding ---
    html = html.replace("<title>BioLern – KA 1 · 25.11.2026</title>",
                        "<title>GeoLern – KA · Innere Tropen · Kl. 7c</title>")
    html = html.replace(
        '.hero{background:linear-gradient(125deg,#154d42,#226b50);',
        '.hero{background:linear-gradient(125deg,rgba(21,77,66,.90),rgba(34,107,80,.80)),'
        'url("Bilder/Tropischer%20Regenwald%20im%20Morgengl%C3%BChen.png") center/cover;')
    html = html.replace(
        '<div class="logo">🌱 Bio<span>Lern</span></div>'
        '<div class="tag">KA 1 · Mi 25.11.2026 · Kl. 7c</div>',
        '<div class="logo">🌴 Geo<span>Lern</span></div>'
        '<div class="tag">KA · Innere Tropen · Kl. 7c</div>')
    html = html.replace("<h1>Alles für KA 1.</h1>",
                        "<h1>Alles für die Geo-KA.</h1>")
    html = re.sub(
        r"<p>Genau auf die angekündigten Inhalte zugeschnitten:.*?</p>",
        "<p>Genau auf die angekündigten KA-Inhalte zugeschnitten: Lage der inneren Tropen, "
        "Klima &amp; Klimadiagramm, Wetterablauf &amp; Gewitter, Passatkreislauf, "
        "Nährstoffkreislauf &amp; Stockwerkbau, Brandrodungsfeldbau, Yanomami, "
        "Regenwaldzerstörung und Schutz des Regenwaldes.</p>",
        html, flags=re.S)

    # --- Diagramm-Sektion einfügen (vor Bildbeschriftung) ---
    diagram_html = (
        '<h2 class="section-title">2. Diagramme lesen</h2>'
        '<section class="card"><div class="imgtabs" style="margin-bottom:14px">'
        '<span class="pill">Klimadiagramm Manaus</span><span class="pill">Erträge Brandrodungsfeldbau</span></div>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px">'
        f"<div>{svg_climate()}</div>"
        f"<div>{svg_ertrag()}</div>"
        "</div>"
        '<p class="hint" style="margin:14px 0 0">Merke dir: Linie = Temperatur (rot, links °C), '
        "Säulen = Niederschlag (blau, rechts mm). Liegt die Linie über den Säulen, ist der Monat "
        "arid – darunter humid. Beim Ertragsdiagramm siehst du, warum Felder nach 3–4 Jahren "
        "verlassen werden.</p></section>")
    html = html.replace('<h2 class="section-title">2. Bilder gezielt beschriften</h2>',
                        diagram_html +
                        '<h2 class="section-title">3. Bilder gezielt beschriften</h2>')

    # --- Fußnote / Footer ---
    html = re.sub(
        r'Inhalte folgen der KA-Ankündigung[^<]*\.',
        'Inhalte folgen der KA-Ankündigung „Innere Tropen“, eurem Heftaufschrieb und den '
        'Arbeitsblättern (Passatkreislauf, Klimadiagramm Manaus, Stockwerkbau, '
        'Brandrodungsfeldbau, Yanomami, Palmöl).', html)
    html = html.replace("BioLern · Offline-HTML", "GeoLern · Offline-HTML")

    # --- localStorage-Keys ---
    html = html.replace("biolern_v1", "geolern_v1").replace(
        "biolern_bilder_v1", "geolern_bilder_v1")

    # --- Fragenpool ---
    q_block = "[" + ",\n".join(js_question(q) for q in Q) + "]"
    html, n = re.subn(r"const Q=\[.*?\]\.map\(\(a,i\)=>\(",
                      "const Q=" + q_block + ".map((a,i)=>(", html, flags=re.S)
    assert n == 1, "Q-Block nicht gefunden"

    # --- Themen ---
    topics = ["Alle Themen", "Lage", "Klima", "Wetter", "Wald",
              "Menschen", "Nutzung", "Schutz"]
    labels = {"Alle Themen": "Alle KA-Blöcke",
              "Lage": "Lage der Tropen",
              "Klima": "Klima &amp; Klimadiagramm",
              "Wetter": "Wetterablauf &amp; Stürme",
              "Wald": "Aufbau &amp; Nährstoffe",
              "Menschen": "Wanderfeldbau &amp; Ureinwohner",
              "Nutzung": "Nutzung &amp; Zerstörung",
              "Schutz": "Schutz des Regenwalds"}
    topics_js = "const topics=" + json.dumps(topics, ensure_ascii=False) + ";"
    labels_js = "const labels=" + json.dumps(labels, ensure_ascii=False) + ";"
    html, n = re.subn(r"const topics=\[.*?\];\s*const labels=\{.*?\};",
                      topics_js + labels_js, html, flags=re.S)
    assert n == 1, "topics/labels nicht gefunden"

    # --- IMGS-Block leeren (wird von build_beschriftung.py gefüllt) ---
    html, n = re.subn(
        r"const IMGS=/\*GENERATED-START\*/.*?/\*GENERATED-END\*/;",
        "const IMGS=/*GENERATED-START*/[]/*GENERATED-END*/;", html, flags=re.S)
    assert n == 1, "IMGS-Block nicht gefunden"

    # --- TOPIC_IMGS ---
    topic_imgs = ("const TOPIC_IMGS={Lage:['verbreitung'],Klima:[],"
                  "Wetter:['wetter','gewitter','passat','wirbelsturm'],"
                  "Wald:['naehrstoff','stockwerk','waldvergleich'],"
                  "Menschen:['wanderfeldbau','yanomami'],"
                  "Nutzung:['palmoelkette','plantage','folgen','produkte'],"
                  "Schutz:['tipps']};")
    html, n = re.subn(r"const TOPIC_IMGS=\{.*?\};", topic_imgs, html, flags=re.S)
    assert n == 1, "TOPIC_IMGS nicht gefunden"

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"index.html geschrieben: {len(Q)} Fragen, {len(topics)} Themen")


if __name__ == "__main__":
    main()
