"""Erzeugt Startpositionen für Bilder/beschriftungen.json.

Die Punktpositionen (point) sind grob voreingestellt und können im
beschriftung_editor.py feinjustiert werden. Kästchen werden wie im
Editor an die Bildränder gesetzt; Einträge mit "onspot" legen das
Kästchen direkt auf einen im Bild vorhandenen Platzhalter.
"""

import json
import os

from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "Bilder")
DATA_FILE = os.path.join(IMG_DIR, "beschriftungen.json")

MARGIN_X = 300
MARGIN_Y = 240
MAX_IMG_W = 1000
MAX_IMG_H = 540
GAP = 40
ZONES = {"full": (0.05, 0.95), "top": (0.05, 0.5), "bottom": (0.5, 0.95)}

# label: (id, text, mode, side, zone, fx, fy)
# mode "margin": Kästchen am Rand (side/zone), Punkt bei (fx, fy) im Bild
# mode "onspot": Kästchen UND Punkt bei (fx, fy) – auf Platzhaltern im Bild
SPEC = {
    "Tropischer Regenwald weltweit.png": [
        ("noerdlicher_wendekreis", "nördlicher Wendekreis", "margin", "left", "top", 0.50, 0.454),
        ("aequator", "Äquator", "margin", "left", "top", 0.42, 0.583),
        ("suedlicher_wendekreis", "südlicher Wendekreis", "margin", "left", "bottom", 0.45, 0.737),
        ("amazonas", "Amazonasbecken", "margin", "right", "top", 0.29, 0.60),
        ("kongo", "Kongobecken", "margin", "right", "top", 0.515, 0.575),
        ("suedostasien", "Südostasien", "margin", "right", "bottom", 0.80, 0.59),
    ],
    "Hadley-Zirkulation über Tropenlandschaft.png": [
        ("aufsteigend", "aufsteigende Luftmassen", "margin", "left", "top", 0.46, 0.42),
        ("regenwolken", "Regenwolken (ITC)", "margin", "left", "top", 0.56, 0.27),
        ("hoehenwinde_l", "Höhenwinde", "margin", "left", "full", 0.28, 0.13),
        ("passatwinde", "Passatwinde", "margin", "left", "bottom", 0.33, 0.69),
        ("wueste", "Wendekreiswüsten", "margin", "left", "bottom", 0.075, 0.72),
        ("hoehenwinde_r", "Höhenwinde", "margin", "right", "full", 0.72, 0.13),
        ("hoch_oben", "Hochdruckgebiet (H)", "onspot", None, None, 0.50, 0.105),
        ("tief_oben_l", "Tiefdruckgebiet (T)", "onspot", None, None, 0.157, 0.185),
        ("tief_oben_r", "Tiefdruckgebiet (T)", "onspot", None, None, 0.84, 0.185),
        ("hoch_l", "Hochdruckgebiet (H)", "onspot", None, None, 0.204, 0.71),
        ("tief_boden", "Tiefdruckgebiet (T)", "onspot", None, None, 0.498, 0.715),
        ("hoch_r", "Hochdruckgebiet (H)", "onspot", None, None, 0.795, 0.715),
        ("absinkend_l", "absinkende Luftmassen", "onspot", None, None, 0.055, 0.435),
        ("absinkend_r", "absinkende Luftmassen", "onspot", None, None, 0.935, 0.435),
        ("wende_n", "nördlicher Wendekreis", "onspot", None, None, 0.136, 0.895),
        ("aequator", "Äquator", "onspot", None, None, 0.498, 0.895),
        ("wende_s", "südlicher Wendekreis", "onspot", None, None, 0.86, 0.895),
    ],
    "Tropenwald im Wandel der Wetterstimmungen.png": [
        ("morgen", "Morgens: heiter und klar", "margin", "left", "top", 0.125, 0.42),
        ("mittag", "Mittags: Quellwolken", "margin", "left", "bottom", 0.375, 0.38),
        ("nachmittag", "Nachmittags: Hitzegewitter", "margin", "right", "top", 0.625, 0.38),
        ("abend", "Abends: Aufklaren", "margin", "right", "bottom", 0.875, 0.42),
    ],
    "Gewitter mit Ladungstrennung und Blitzen.png": [
        ("pos_wolke", "positive Ladung", "margin", "left", "top", 0.41, 0.10),
        ("aufwinde", "Aufwinde", "margin", "left", "top", 0.295, 0.30),
        ("eis", "Eiskristalle & Tropfen", "margin", "left", "bottom", 0.42, 0.28),
        ("regen", "Regen", "margin", "left", "bottom", 0.30, 0.72),
        ("abwinde", "Abwinde", "margin", "right", "top", 0.50, 0.35),
        ("neg_wolke", "negative Ladung", "margin", "right", "top", 0.42, 0.47),
        ("blitz", "Blitz", "margin", "right", "bottom", 0.485, 0.63),
        ("pos_boden", "positiv geladener Erdboden", "margin", "right", "bottom", 0.44, 0.95),
    ],
    "Regenwald-Nährstoffkreislauf im Querschnitt.png": [
        ("niederschlag", "Niederschlag", "onspot", None, None, 0.144, 0.095),
        ("biomasse", "lebende Biomasse", "onspot", None, None, 0.70, 0.065),
        ("fallstreu", "Fallstreu", "onspot", None, None, 0.38, 0.395),
        ("humus", "dünne Humus-/Streuschicht", "onspot", None, None, 0.395, 0.66),
        ("naehrstoffe", "Nährstoffe im Boden", "onspot", None, None, 0.476, 0.92),
        ("kreislauf", "schneller Kreislauf", "onspot", None, None, 0.837, 0.41),
        ("wurzeln", "flache Wurzeln", "onspot", None, None, 0.862, 0.81),
        ("zersetzung", "Zersetzung (Kleinstlebewesen)", "margin", "left", "bottom", 0.10, 0.62),
    ],
    "Regenwaldschichten mit Tieren und Pflanzen.png": [
        ("dachschicht", "Dachschicht (Kronendach)", "onspot", None, None, 0.766, 0.145),
        ("oberschoss2", "2. Oberschoss", "onspot", None, None, 0.766, 0.40),
        ("oberschoss1", "1. Oberschoss (Strauchschicht)", "onspot", None, None, 0.766, 0.67),
        ("erdschicht", "Erdschicht (Krautschicht)", "onspot", None, None, 0.766, 0.89),
        ("emergent", "Emergent (Überholer)", "margin", "left", "top", 0.10, 0.10),
        ("lianen", "Lianen", "margin", "left", "top", 0.095, 0.55),
        ("epiphyten", "Epiphyten (Aufsitzer)", "margin", "left", "bottom", 0.315, 0.79),
        ("brettwurzeln", "Brettwurzeln", "margin", "left", "bottom", 0.09, 0.88),
    ],
    "Kreislauf des Wanderfeldbaus.png": [
        ("wald", "1 · intaktes Waldstück", "margin", "left", "top", 0.50, 0.17),
        ("jungwald", "5 · Fläche verlassen – Wald wächst nach", "margin", "left", "bottom", 0.21, 0.42),
        ("faellen", "2 · Bäume fällen & trocknen", "margin", "right", "top", 0.79, 0.44),
        ("brennen", "3 · Abbrennen (Asche düngt)", "margin", "right", "full", 0.73, 0.84),
        ("felder", "4 · Felder bestellen", "margin", "right", "bottom", 0.23, 0.83),
    ],
    "Yanomami-Dorf im Regenwald.png": [
        ("wald", "Regenwald", "margin", "left", "top", 0.15, 0.08),
        ("shabono", "Shabono (Gemeinschaftshaus)", "margin", "left", "top", 0.42, 0.36),
        ("feuer", "Feuerstelle", "margin", "left", "bottom", 0.34, 0.35),
        ("haengematten", "Hängematten", "margin", "right", "top", 0.56, 0.28),
        ("platz", "zentraler Dorfplatz", "margin", "right", "full", 0.45, 0.47),
        ("feld", "Feld (Wanderfeldbau)", "margin", "right", "bottom", 0.80, 0.82),
    ],
    "Palmöl-Lieferkette im Überblick.png": [
        ("plantage", "Ölpalmenplantage", "margin", "left", "top", 0.095, 0.50),
        ("ernte", "Ernte der Fruchtstände", "margin", "left", "bottom", 0.30, 0.50),
        ("transport", "Transport", "margin", "right", "top", 0.495, 0.55),
        ("muehle", "Ölmühle / Fabrik", "margin", "right", "full", 0.695, 0.50),
        ("produkte", "Endprodukte & Biosprit", "margin", "right", "bottom", 0.885, 0.50),
    ],
    "Palmölplantage am Regenwaldrand.png": [
        ("rodung", "frisch gerodete Fläche", "margin", "left", "top", 0.28, 0.22),
        ("monokultur", "Monokultur (Ölpalmen)", "margin", "left", "bottom", 0.45, 0.55),
        ("regenwald", "verbliebener Regenwald", "margin", "right", "top", 0.82, 0.22),
    ],
    "Ökologische Folgen der Abholzung.png": [
        ("verdunstung_hoch", "hohe Verdunstung", "margin", "left", "top", 0.155, 0.30),
        ("sickerwasser", "Versickerung / Sickerwasser", "margin", "left", "top", 0.10, 0.82),
        ("naehrstoffe", "Nährstoffe im Boden", "margin", "left", "bottom", 0.16, 0.88),
        ("abfluss", "Oberflächenabfluss", "margin", "left", "bottom", 0.59, 0.70),
        ("verdunstung_gering", "geringe Verdunstung", "margin", "right", "top", 0.855, 0.42),
        ("temperatur", "große Temperaturschwankung", "margin", "right", "top", 0.955, 0.29),
        ("erosion", "Erosion", "margin", "right", "full", 0.83, 0.53),
        ("wenig_sicker", "kaum Versickerung", "margin", "right", "bottom", 0.77, 0.88),
    ],
    "Tornado und Hurrikan im Vergleich.png": [
        ("mutterwolke", "Mutterwolke (Gewitterzelle)", "margin", "left", "top", 0.22, 0.18),
        ("tornado", "Tornado-Schlauch", "margin", "left", "full", 0.215, 0.45),
        ("truemmer", "Trümmer am Erdboden", "margin", "left", "bottom", 0.21, 0.77),
        ("regenbaender", "Regenbänder", "margin", "right", "top", 0.63, 0.30),
        ("auge", "Auge (windstill)", "margin", "right", "full", 0.775, 0.50),
        ("wirbelsturm", "tropischer Wirbelsturm", "margin", "right", "bottom", 0.70, 0.70),
    ],
    "Palmöl im Alltag_ Produktvielfalt rundherum.png": [
        ("biosprit", "Biosprit", "margin", "left", "top", 0.10, 0.42),
        ("suesswaren", "Süßwaren", "margin", "left", "top", 0.54, 0.15),
        ("tierfutter", "Tierfutter", "margin", "left", "bottom", 0.15, 0.84),
        ("palmfrucht", "Palmfrucht (Ausgangsstoff)", "margin", "left", "bottom", 0.50, 0.50),
        ("fertig", "Fertigprodukte", "margin", "right", "top", 0.77, 0.17),
        ("fett", "Nahrungsmittel & Fette", "margin", "right", "full", 0.87, 0.37),
        ("kosmetik", "Kosmetik & Pflege", "margin", "right", "bottom", 0.60, 0.88),
    ],
    "Zwei Wälder, zwei Wurzelsysteme.png": [
        ("mischwald", "Laubmischwald", "margin", "left", "top", 0.25, 0.18),
        ("laubfall", "Laubfall im Herbst", "margin", "left", "full", 0.22, 0.58),
        ("humus_dick", "dicke Humusschicht", "margin", "left", "bottom", 0.20, 0.63),
        ("wurzeln_tief", "tiefe Wurzeln", "margin", "left", "bottom", 0.17, 0.80),
        ("regenwald", "tropischer Regenwald", "margin", "right", "top", 0.75, 0.18),
        ("brettwurzeln", "Brettwurzeln", "margin", "right", "full", 0.78, 0.52),
        ("wurzeln_flach", "flache Wurzeln", "margin", "right", "bottom", 0.70, 0.63),
        ("humus_duenn", "dünne Humusschicht", "margin", "right", "bottom", 0.60, 0.62),
    ],
    "Nachhaltige Ideen im Icon-Raster.png": [
        ("recycling", "Recyclingpapier benutzen", "onspot", None, None, 0.125, 0.17),
        ("fleisch", "wenig/kein Fleisch essen", "onspot", None, None, 0.375, 0.17),
        ("wasser", "Leitungswasser trinken", "onspot", None, None, 0.625, 0.17),
        ("beutel", "Stoffbeutel nutzen", "onspot", None, None, 0.875, 0.17),
        ("drucken", "nur Nötiges drucken", "onspot", None, None, 0.125, 0.50),
        ("fertig", "wenig Fertigprodukte", "onspot", None, None, 0.375, 0.50),
        ("moebel", "keine Tropenholz-Möbel", "onspot", None, None, 0.625, 0.50),
        ("papier", "Papier mehrmals verwenden", "onspot", None, None, 0.875, 0.50),
        ("biosprit", "keinen Biosprit tanken", "onspot", None, None, 0.125, 0.83),
        ("flasche", "Mehrwegflasche nutzen", "onspot", None, None, 0.375, 0.83),
        ("briefe", "Briefe an Konzerne schreiben", "onspot", None, None, 0.625, 0.83),
        ("vorbild", "anderen ein Vorbild sein", "onspot", None, None, 0.875, 0.83),
    ],
}


def text_width(text):
    return len(text) * 9 + 36


def margin_box(entries_done, total, side, zone, iw, ih, text):
    """Kästchen-Position am Rand wie default_labels im Editor."""
    x_img, y_img = MARGIN_X, MARGIN_Y
    z0, z1 = ZONES[zone]
    w, h = text_width(text), 34
    cy = y_img + ih * (z0 + (z1 - z0) * (entries_done + 1) / (total + 1))
    x = x_img - GAP - w if side == "left" else x_img + iw + GAP
    return {"x": round(x), "y": round(cy - h / 2), "w": w, "h": h}


def crop_rect(labels, rect, canvas):
    ix, iy, iw, ih = rect["x"], rect["y"], rect["w"], rect["h"]
    x0, y0, x1, y1 = ix, iy, ix + iw, iy + ih
    for lb in labels:
        b = lb["box"]
        x0 = min(x0, b["x"])
        y0 = min(y0, b["y"])
        x1 = max(x1, b["x"] + b["w"])
        y1 = max(y1, b["y"] + b["h"])
    x0 = max(0, x0 - 30)
    y0 = max(0, y0 - 30)
    x1 = min(canvas["width"], x1 + 30)
    y1 = min(canvas["height"], y1 + 30)
    return {"x": round(x0), "y": round(y0), "w": round(x1 - x0), "h": round(y1 - y0)}


def normalize_boxes(labels):
    w = max(lb["box"]["w"] for lb in labels)
    h = max(lb["box"]["h"] for lb in labels)
    for lb in labels:
        b = lb["box"]
        b["x"] = round(b["x"] + b["w"] / 2 - w / 2)
        b["y"] = round(b["y"] + b["h"] / 2 - h / 2)
        b["w"], b["h"] = w, h


def main():
    data = {}
    for fname, specs in SPEC.items():
        path = os.path.join(IMG_DIR, fname)
        with Image.open(path) as im:
            ow, oh = im.size
        scale = min(MAX_IMG_W / ow, MAX_IMG_H / oh, 1.6)
        iw, ih = round(ow * scale), round(oh * scale)
        rect = {"x": MARGIN_X, "y": MARGIN_Y, "w": iw, "h": ih}
        canvas = {"width": 2 * MARGIN_X + iw, "height": 2 * MARGIN_Y + ih,
                  "scale": round(scale, 5)}

        groups = {}
        for spec in specs:
            if spec[2] == "margin":
                groups.setdefault((spec[3], spec[4]), []).append(spec)

        labels = []
        for (side, zone), entries in groups.items():
            for k, spec in enumerate(entries):
                lid, text, _, _, _, fx, fy = spec
                labels.append({
                    "id": lid, "text": text,
                    "box": margin_box(k, len(entries), side, zone, iw, ih, text),
                    "point": {"x": round(MARGIN_X + fx * iw),
                              "y": round(MARGIN_Y + fy * ih)},
                })
        for spec in specs:
            if spec[2] != "onspot":
                continue
            lid, text, _, _, _, fx, fy = spec
            w, h = text_width(text), 34
            cx, cy = MARGIN_X + fx * iw, MARGIN_Y + fy * ih
            labels.append({
                "id": lid, "text": text,
                "box": {"x": round(cx - w / 2), "y": round(cy - h / 2),
                        "w": w, "h": h},
                "point": {"x": round(cx), "y": round(cy)},
            })

        data[fname] = {
            "image": {"file": f"Bilder/{fname}", "width": ow, "height": oh},
            "canvas": canvas,
            "imageRect": rect,
            "crop": crop_rect(labels, rect, canvas),
            "labels": labels,
        }

    with open(DATA_FILE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = sum(len(v["labels"]) for v in data.values())
    print(f"{len(data)} Bilder, {total} Beschriftungen -> beschriftungen.json")


if __name__ == "__main__":
    main()
