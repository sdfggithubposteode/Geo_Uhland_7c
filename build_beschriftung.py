"""Überträgt die Positionen aus Bilder/beschriftungen.json in die HTML-Datei.

Ersetzt den Block zwischen GENERATED-START/END in index.html.
Nach Änderungen im beschriftung_editor.py einfach erneut ausführen:
    python build_beschriftung.py
"""

import json
import os
import re
from urllib.parse import quote

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "Bilder", "beschriftungen.json")
HTML_FILE = os.path.join(BASE, "index.html")

META = {
    "Tropischer Regenwald weltweit.png": {
        "key": "verbreitung",
        "name": "Verbreitung",
        "decoys": ["Polarkreis", "Sahara", "Mittelmeer"],
    },
    "Hadley-Zirkulation über Tropenlandschaft.png": {
        "key": "passat",
        "name": "Passatkreislauf",
        "decoys": ["Jetstream", "Westwinddrift", "Polarnacht"],
    },
    "Tropenwald im Wandel der Wetterstimmungen.png": {
        "key": "wetter",
        "name": "Wetterablauf",
        "decoys": ["Dauerregen den ganzen Tag", "Schneefall", "Nachts: Sonnenschein"],
    },
    "Gewitter mit Ladungstrennung und Blitzen.png": {
        "key": "gewitter",
        "name": "Gewitter",
        "decoys": ["Ozonschicht", "Magnetfeld", "Tropopause"],
    },
    "Regenwald-Nährstoffkreislauf im Querschnitt.png": {
        "key": "naehrstoff",
        "name": "Nährstoffkreislauf",
        "decoys": ["dicke Humusschicht", "tiefe Wurzeln", "Gletscher"],
    },
    "Regenwaldschichten mit Tieren und Pflanzen.png": {
        "key": "stockwerk",
        "name": "Stockwerkbau",
        "decoys": ["Wurzelstockwerk", "Laubschicht", "Moosebene"],
    },
    "Kreislauf des Wanderfeldbaus.png": {
        "key": "wanderfeldbau",
        "name": "Wanderfeldbau",
        "decoys": ["Bewässern", "Pflügen", "Ernten mit Mähdrescher"],
    },
    "Yanomami-Dorf im Regenwald.png": {
        "key": "yanomami",
        "name": "Yanomami",
        "decoys": ["Häuptlingshaus", "Schule", "Marktplatz"],
    },
    "Palmöl-Lieferkette im Überblick.png": {
        "key": "palmoelkette",
        "name": "Palmöl-Kette",
        "decoys": ["Kakao-Plantage", "Wasserkraftwerk", "Sägewerk"],
    },
    "Palmölplantage am Regenwaldrand.png": {
        "key": "plantage",
        "name": "Monokultur",
        "decoys": ["Mischkultur", "Savanne", "Urewald"],
    },
    "Ökologische Folgen der Abholzung.png": {
        "key": "folgen",
        "name": "Folgen Abholzung",
        "decoys": ["Grundwasseranreicherung", "mehr Artenvielfalt", "Abkühlung"],
    },
    "Tornado und Hurrikan im Vergleich.png": {
        "key": "wirbelsturm",
        "name": "Wirbelstürme",
        "decoys": ["Jetstream", "Landbrise", "Föhn"],
    },
    "Palmöl im Alltag_ Produktvielfalt rundherum.png": {
        "key": "produkte",
        "name": "Palmöl-Produkte",
        "decoys": ["Medikamente", "Baumaterial", "Kleidung"],
    },
    "Zwei Wälder, zwei Wurzelsysteme.png": {
        "key": "waldvergleich",
        "name": "Waldvergleich",
        "decoys": ["Nadelwald", "Mangroven", "Tropfsteine"],
    },
    "Nachhaltige Ideen im Icon-Raster.png": {
        "key": "tipps",
        "name": "Schutz-Tipps",
        "decoys": ["mehr Plastik kaufen", "häufiger fliegen", "Wald anzünden"],
    },
}


def img_src(fname):
    """Relativer Bildpfad – der Ordner Bilder/ muss neben der HTML liegen."""
    return "Bilder/" + quote(fname)


def normalize_boxes(labels):
    """Gibt allen Kästchen eines Bildes dieselbe Größe (zentriert auf der
    bisherigen Mitte), damit die Wortlänge nicht erraten werden kann."""
    w = max(lb["box"]["w"] for lb in labels)
    h = max(lb["box"]["h"] for lb in labels)
    for lb in labels:
        b = lb["box"]
        b["x"] = round(b["x"] + b["w"] / 2 - w / 2)
        b["y"] = round(b["y"] + b["h"] / 2 - h / 2)
        b["w"], b["h"] = w, h


def crop_rect(labels, rect, canvas):
    ix, iy, iw, ih = rect["x"], rect["y"], rect["w"], rect["h"]
    x0, y0, x1, y1 = ix, iy, ix + iw, iy + ih
    for lb in labels:
        b = lb["box"]
        x0 = min(x0, b["x"]); y0 = min(y0, b["y"])
        x1 = max(x1, b["x"] + b["w"]); y1 = max(y1, b["y"] + b["h"])
    x0 = max(0, x0 - 30); y0 = max(0, y0 - 30)
    x1 = min(canvas["width"], x1 + 30); y1 = min(canvas["height"], y1 + 30)
    return {"x": round(x0), "y": round(y0), "w": round(x1 - x0), "h": round(y1 - y0)}


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    imgs = []
    for fname, meta in META.items():
        if fname not in data:
            print(f"Überspringe (noch keine Positionen): {meta['name']}")
            continue
        e = data[fname]
        labels = [{"text": lb["text"], "box": dict(lb["box"]),
                   "point": dict(lb["point"])} for lb in e["labels"]]
        normalize_boxes(labels)
        imgs.append({
            "key": meta["key"],
            "name": meta["name"],
            "src": img_src(fname),
            "crop": crop_rect(labels, e["imageRect"], e["canvas"]),
            "imageRect": e["imageRect"],
            "labels": labels,
            "targets": [lb["text"] for lb in labels],
            "decoys": meta["decoys"],
        })

    block = json.dumps(imgs, ensure_ascii=False, separators=(",", ":"))

    with open(HTML_FILE, encoding="utf-8") as f:
        html = f.read()

    html, n = re.subn(
        r"(const IMGS=/\*GENERATED-START\*/).*?(/\*GENERATED-END\*/;)",
        lambda m: m.group(1) + block + m.group(2),
        html, flags=re.S,
    )
    if n != 1:
        raise SystemExit("GENERATED-Marker nicht gefunden oder mehrfach vorhanden.")

    with open(HTML_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    print(f"{len(imgs)} Bilder eingetragen -> {os.path.basename(HTML_FILE)}")


if __name__ == "__main__":
    main()
