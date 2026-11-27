"""Editor zum Positionieren der Beschriftungen auf den vier Bio-Bildern.

Bedienung:
  - Kästchen und rote Punkte mit der Maus ziehen
  - Pfeiltasten: markiertes Element fein bewegen (Shift = 10 px)
  - Oben zwischen den Bildern wechseln, mit "Speichern" sichern

Kästchen lassen sich frei platzieren (für das Layout außerhalb des
Bildes vorsehen), die roten Punkte bleiben immer innerhalb des Bildes.
Ergebnis: Bilder/beschriftungen.json (inkl. Zuschnitt-Rechteck "crop").
"""

import json
import os
import tkinter as tk
from tkinter import font as tkfont, messagebox, simpledialog

from PIL import Image, ImageTk

BASE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE, "Bilder")
DATA_FILE = os.path.join(IMG_DIR, "beschriftungen.json")

MARGIN_X = 300      # Platz für Kästchen links/rechts vom Bild
MARGIN_Y = 240      # Platz ober-/unterhalb
MAX_IMG_W = 1000    # Bild wird auf diese Anzeigegröße skaliert
MAX_IMG_H = 540
CROP_PAD = 30       # Zuschlag um Bild+Kästchen beim Zuschnitt
GAP = 40            # Abstand Kästchen <-> Bildkante bei Startposition

ZONES = {"full": (0.05, 0.95), "top": (0.05, 0.5), "bottom": (0.5, 0.95)}

IMAGES = [
    {
        "file": "Tropischer Regenwald weltweit.png",
        "name": "1 · Verbreitung",
        "labels": [
            ("noerdlicher_wendekreis", "nördlicher Wendekreis", "left", "top"),
            ("aequator", "Äquator", "left", "top"),
            ("suedlicher_wendekreis", "südlicher Wendekreis", "left", "bottom"),
            ("amazonas", "Amazonasbecken", "right", "top"),
            ("kongo", "Kongobecken", "right", "top"),
            ("suedostasien", "Südostasien", "right", "bottom"),
        ],
    },
    {
        "file": "Hadley-Zirkulation über Tropenlandschaft.png",
        "name": "2 · Passatkreislauf",
        "labels": [
            ("aufsteigend", "aufsteigende Luftmassen", "left", "top"),
            ("regenwolken", "Regenwolken (ITC)", "left", "top"),
            ("hoehenwinde_l", "Höhenwinde", "left", "full"),
            ("passatwinde", "Passatwinde", "left", "bottom"),
            ("wueste", "Wendekreiswüsten", "left", "bottom"),
            ("hoehenwinde_r", "Höhenwinde", "right", "top"),
            ("hoch_oben", "Hochdruckgebiet (H)", "right", "top"),
            ("tief_oben_l", "Tiefdruckgebiet (T)", "right", "top"),
            ("tief_oben_r", "Tiefdruckgebiet (T)", "right", "top"),
            ("hoch_l", "Hochdruckgebiet (H)", "right", "full"),
            ("tief_boden", "Tiefdruckgebiet (T)", "right", "full"),
            ("hoch_r", "Hochdruckgebiet (H)", "right", "full"),
            ("absinkend_l", "absinkende Luftmassen", "right", "bottom"),
            ("absinkend_r", "absinkende Luftmassen", "right", "bottom"),
            ("wende_n", "nördlicher Wendekreis", "right", "bottom"),
            ("aequator", "Äquator", "right", "bottom"),
            ("wende_s", "südlicher Wendekreis", "right", "bottom"),
        ],
    },
    {
        "file": "Tropenwald im Wandel der Wetterstimmungen.png",
        "name": "3 · Wetterablauf",
        "labels": [
            ("morgen", "Morgens: heiter und klar", "left", "top"),
            ("mittag", "Mittags: Quellwolken", "left", "bottom"),
            ("nachmittag", "Nachmittags: Hitzegewitter", "right", "top"),
            ("abend", "Abends: Aufklaren", "right", "bottom"),
        ],
    },
    {
        "file": "Gewitter mit Ladungstrennung und Blitzen.png",
        "name": "4 · Gewitter",
        "labels": [
            ("pos_wolke", "positive Ladung", "left", "top"),
            ("aufwinde", "Aufwinde", "left", "top"),
            ("eis", "Eiskristalle & Tropfen", "left", "bottom"),
            ("regen", "Regen", "left", "bottom"),
            ("abwinde", "Abwinde", "right", "top"),
            ("neg_wolke", "negative Ladung", "right", "top"),
            ("blitz", "Blitz", "right", "bottom"),
            ("pos_boden", "positiv geladener Erdboden", "right", "bottom"),
        ],
    },
    {
        "file": "Regenwald-Nährstoffkreislauf im Querschnitt.png",
        "name": "5 · Nährstoffkreislauf",
        "labels": [
            ("niederschlag", "Niederschlag", "left", "top"),
            ("fallstreu", "Fallstreu", "left", "top"),
            ("humus", "dünne Humus-/Streuschicht", "left", "bottom"),
            ("zersetzung", "Zersetzung (Kleinstlebewesen)", "left", "bottom"),
            ("biomasse", "lebende Biomasse", "right", "top"),
            ("kreislauf", "schneller Kreislauf", "right", "full"),
            ("naehrstoffe", "Nährstoffe im Boden", "right", "bottom"),
            ("wurzeln", "flache Wurzeln", "right", "bottom"),
        ],
    },
    {
        "file": "Regenwaldschichten mit Tieren und Pflanzen.png",
        "name": "6 · Stockwerkbau",
        "labels": [
            ("emergent", "Emergent (Überholer)", "left", "top"),
            ("lianen", "Lianen", "left", "top"),
            ("brettwurzeln", "Brettwurzeln", "left", "bottom"),
            ("epiphyten", "Epiphyten (Aufsitzer)", "left", "bottom"),
            ("dachschicht", "Dachschicht (Kronendach)", "right", "top"),
            ("oberschoss2", "2. Oberschoss", "right", "top"),
            ("oberschoss1", "1. Oberschoss (Strauchschicht)", "right", "bottom"),
            ("erdschicht", "Erdschicht (Krautschicht)", "right", "bottom"),
        ],
    },
    {
        "file": "Kreislauf des Wanderfeldbaus.png",
        "name": "7 · Wanderfeldbau",
        "labels": [
            ("wald", "1 · intaktes Waldstück", "left", "top"),
            ("jungwald", "5 · Fläche verlassen – Wald wächst nach", "left", "bottom"),
            ("faellen", "2 · Bäume fällen & trocknen", "right", "top"),
            ("brennen", "3 · Abbrennen (Asche düngt)", "right", "full"),
            ("felder", "4 · Felder bestellen", "right", "bottom"),
        ],
    },
    {
        "file": "Yanomami-Dorf im Regenwald.png",
        "name": "8 · Yanomami",
        "labels": [
            ("wald", "Regenwald", "left", "top"),
            ("shabono", "Shabono (Gemeinschaftshaus)", "left", "top"),
            ("feuer", "Feuerstelle", "left", "bottom"),
            ("haengematten", "Hängematten", "right", "top"),
            ("platz", "zentraler Dorfplatz", "right", "full"),
            ("feld", "Feld (Wanderfeldbau)", "right", "bottom"),
        ],
    },
    {
        "file": "Palmöl-Lieferkette im Überblick.png",
        "name": "9 · Palmöl-Kette",
        "labels": [
            ("plantage", "Ölpalmenplantage", "left", "top"),
            ("ernte", "Ernte der Fruchtstände", "left", "bottom"),
            ("transport", "Transport", "right", "top"),
            ("muehle", "Ölmühle / Fabrik", "right", "full"),
            ("produkte", "Endprodukte & Biosprit", "right", "bottom"),
        ],
    },
    {
        "file": "Palmölplantage am Regenwaldrand.png",
        "name": "10 · Monokultur",
        "labels": [
            ("rodung", "frisch gerodete Fläche", "left", "top"),
            ("monokultur", "Monokultur (Ölpalmen)", "left", "bottom"),
            ("regenwald", "verbliebener Regenwald", "right", "top"),
        ],
    },
    {
        "file": "Ökologische Folgen der Abholzung.png",
        "name": "11 · Folgen Abholzung",
        "labels": [
            ("verdunstung_hoch", "hohe Verdunstung", "left", "top"),
            ("sickerwasser", "Versickerung / Sickerwasser", "left", "top"),
            ("naehrstoffe", "Nährstoffe im Boden", "left", "bottom"),
            ("abfluss", "Oberflächenabfluss", "left", "bottom"),
            ("verdunstung_gering", "geringe Verdunstung", "right", "top"),
            ("temperatur", "große Temperaturschwankung", "right", "top"),
            ("erosion", "Erosion", "right", "full"),
            ("wenig_sicker", "kaum Versickerung", "right", "bottom"),
        ],
    },
    {
        "file": "Tornado und Hurrikan im Vergleich.png",
        "name": "12 · Wirbelstürme",
        "labels": [
            ("mutterwolke", "Mutterwolke (Gewitterzelle)", "left", "top"),
            ("tornado", "Tornado-Schlauch", "left", "full"),
            ("truemmer", "Trümmer am Erdboden", "left", "bottom"),
            ("regenbaender", "Regenbänder", "right", "top"),
            ("auge", "Auge (windstill)", "right", "full"),
            ("wirbelsturm", "tropischer Wirbelsturm", "right", "bottom"),
        ],
    },
    {
        "file": "Palmöl im Alltag_ Produktvielfalt rundherum.png",
        "name": "13 · Palmöl-Produkte",
        "labels": [
            ("biosprit", "Biosprit", "left", "top"),
            ("suesswaren", "Süßwaren", "left", "top"),
            ("tierfutter", "Tierfutter", "left", "bottom"),
            ("palmfrucht", "Palmfrucht (Ausgangsstoff)", "left", "bottom"),
            ("fertig", "Fertigprodukte", "right", "top"),
            ("fett", "Nahrungsmittel & Fette", "right", "full"),
            ("kosmetik", "Kosmetik & Pflege", "right", "bottom"),
        ],
    },
    {
        "file": "Zwei Wälder, zwei Wurzelsysteme.png",
        "name": "14 · Waldvergleich",
        "labels": [
            ("mischwald", "Laubmischwald", "left", "top"),
            ("laubfall", "Laubfall im Herbst", "left", "full"),
            ("humus_dick", "dicke Humusschicht", "left", "bottom"),
            ("wurzeln_tief", "tiefe Wurzeln", "left", "bottom"),
            ("regenwald", "tropischer Regenwald", "right", "top"),
            ("brettwurzeln", "Brettwurzeln", "right", "full"),
            ("wurzeln_flach", "flache Wurzeln", "right", "bottom"),
            ("humus_duenn", "dünne Humusschicht", "right", "bottom"),
        ],
    },
    {
        "file": "Nachhaltige Ideen im Icon-Raster.png",
        "name": "15 · Schutz-Tipps",
        "labels": [
            ("recycling", "Recyclingpapier benutzen", "left", "top"),
            ("fleisch", "wenig/kein Fleisch essen", "left", "top"),
            ("drucken", "nur Nötiges drucken", "left", "full"),
            ("fertig", "wenig Fertigprodukte", "left", "bottom"),
            ("biosprit", "keinen Biosprit tanken", "left", "bottom"),
            ("flasche", "Mehrwegflasche nutzen", "left", "bottom"),
            ("wasser", "Leitungswasser trinken", "right", "top"),
            ("beutel", "Stoffbeutel nutzen", "right", "top"),
            ("moebel", "keine Tropenholz-Möbel", "right", "full"),
            ("papier", "Papier mehrmals verwenden", "right", "bottom"),
            ("briefe", "Briefe an Konzerne schreiben", "right", "bottom"),
            ("vorbild", "anderen ein Vorbild sein", "right", "bottom"),
        ],
    },
]
class Editor:
    def __init__(self, root):
        self.root = root
        root.title("Beschriftungs-Editor – Geo Klasse 7")
        root.state("zoomed")
        self.font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.data = self._load_json()
        self.img_index = None
        self.labels = []
        self.items = {}
        self.dirty = False
        self.sel = None
        self.drag = None
        self._build_ui()
        self.load_image(0)

    def _load_json(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _build_ui(self):
        bar = tk.Frame(self.root, bg="#eef3ef", pady=6, padx=10)
        bar.pack(fill="x")
        self.img_buttons = []
        for i, spec in enumerate(IMAGES):
            b = tk.Button(bar, text=spec["name"], command=lambda i=i: self.switch_image(i))
            b.pack(side="left", padx=(0, 6))
            self.img_buttons.append(b)
        tk.Button(bar, text="Speichern", bg="#17634d", fg="white",
                  command=self.save).pack(side="right")
        tk.Button(bar, text="Zurücksetzen", command=self.reset).pack(side="right", padx=(0, 6))
        tk.Button(bar, text="+ Kästchen", command=self.add_box).pack(side="right", padx=(0, 6))
        tk.Label(bar, text="Ziehen = grob · Pfeiltasten = fein (Shift ×10) · Doppelklick = Text · Entf = löschen",
                 bg="#eef3ef", fg="#5d7080").pack(side="right", padx=14)

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        self.cv = tk.Canvas(frame, bg="#dfe7e1", highlightthickness=0)
        vsb = tk.Scrollbar(frame, orient="vertical", command=self.cv.yview)
        hsb = tk.Scrollbar(self.root, orient="horizontal", command=self.cv.xview)
        self.cv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(fill="x")
        self.cv.pack(fill="both", expand=True)

        self.cv.bind("<ButtonPress-1>", self.on_press)
        self.cv.bind("<B1-Motion>", self.on_drag)
        self.cv.bind("<ButtonRelease-1>", self.on_release)
        self.cv.bind("<Double-Button-1>", self.on_double)
        self.root.bind("<Delete>", lambda e: self.delete_selected())
        self.root.bind("<Left>", lambda e: self.nudge(-1, 0, e))
        self.root.bind("<Right>", lambda e: self.nudge(1, 0, e))
        self.root.bind("<Up>", lambda e: self.nudge(0, -1, e))
        self.root.bind("<Down>", lambda e: self.nudge(0, 1, e))
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- Bild laden / wechseln ----------

    def switch_image(self, i):
        if i == self.img_index:
            return
        if not self.confirm_discard():
            return
        self.load_image(i)

    def confirm_discard(self):
        if not self.dirty:
            return True
        r = messagebox.askyesnocancel("Ungespeicherte Änderungen",
                                      "Änderungen an diesem Bild speichern?")
        if r is None:
            return False
        if r:
            self.save()
        return True

    def load_image(self, i):
        self.img_index = i
        spec = IMAGES[i]
        path = os.path.join(IMG_DIR, spec["file"])
        with Image.open(path) as im:
            self.orig_size = im.size
            scale = min(MAX_IMG_W / im.width, MAX_IMG_H / im.height, 1.6)
            self.scale = scale
            disp = im.resize((round(im.width * scale), round(im.height * scale)),
                             Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(disp.convert("RGB"))

        ix, iy = MARGIN_X, MARGIN_Y
        iw, ih = disp.width, disp.height
        self.img_rect = (ix, iy, iw, ih)
        self.canvas_w = ix * 2 + iw
        self.canvas_h = iy * 2 + ih

        saved = self.data.get(spec["file"])
        if saved and saved.get("labels"):
            self.labels = saved["labels"]
        else:
            self.labels = self.default_labels(spec)

        self.normalize_boxes()
        self.dirty = False
        self.sel = None
        self.draw()
        for j, b in enumerate(self.img_buttons):
            b.configure(relief="sunken" if j == i else "raised")
        self.root.title(f"Beschriftungs-Editor – {spec['name']}"
                        + (" (gespeichert)" if saved else ""))

    def default_labels(self, spec):
        ix, iy, iw, ih = self.img_rect
        groups = {}
        for lid, text, side, zone in spec["labels"]:
            groups.setdefault((side, zone), []).append((lid, text))
        labels = []
        for (side, zone), entries in groups.items():
            z0, z1 = ZONES[zone]
            for k, (lid, text) in enumerate(entries):
                w = self.font.measure(text) + 30
                h = 34
                cy = iy + ih * (z0 + (z1 - z0) * (k + 1) / (len(entries) + 1))
                x = ix - GAP - w if side == "left" else ix + iw + GAP
                y = cy - h / 2
                px = min(max(x + w / 2, ix + 50), ix + iw - 50)
                py = min(max(cy, iy + 50), iy + ih - 50)
                labels.append({
                    "id": lid, "text": text,
                    "box": {"x": round(x), "y": round(y), "w": w, "h": h},
                    "point": {"x": round(px), "y": round(py)},
                })
        return labels

    def normalize_boxes(self):
        """Zieht alle Kästchen auf einheitliche Größe (zentriert) – so wie
        es der Build fürs HTML macht, damit die Ansicht hier dem späteren
        Ergebnis entspricht."""
        if not self.labels:
            return
        w = max(lb["box"]["w"] for lb in self.labels)
        h = max(lb["box"]["h"] for lb in self.labels)
        for lb in self.labels:
            b = lb["box"]
            b["x"] += (b["w"] - w) / 2
            b["y"] += (b["h"] - h) / 2
            b["w"], b["h"] = w, h

    # ---------- Zeichnen ----------

    def draw(self):
        self.cv.delete("all")
        self.items = {}
        ix, iy, iw, ih = self.img_rect
        self.cv.create_image(ix, iy, anchor="nw", image=self.photo, tags="img")
        self.cv.create_rectangle(ix - 1, iy - 1, ix + iw + 1, iy + ih + 1,
                                 outline="#17634d", width=1)
        for i, lb in enumerate(self.labels):
            b, p = lb["box"], lb["point"]
            ax, ay = self.attach_point(b, p)
            line = self.cv.create_line(ax, ay, p["x"], p["y"], fill="#c0392b",
                                       width=2, arrow=tk.LAST,
                                       arrowshape=(11, 13, 5))
            rect = self.cv.create_rectangle(
                b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"],
                fill="white", outline="#17634d", width=2,
                tags=(f"bx{i}", "bx"))
            text = self.cv.create_text(
                b["x"] + b["w"] / 2, b["y"] + b["h"] / 2, text=lb["text"],
                font=self.font, fill="#1b3040", tags=(f"bx{i}", "bx"))
            r = 6
            dot = self.cv.create_oval(
                p["x"] - r, p["y"] - r, p["x"] + r, p["y"] + r,
                fill="#c0392b", outline="white", width=2,
                tags=(f"pt{i}", "pt"))
            self.items[i] = {"line": line, "rect": rect, "text": text, "dot": dot}
        self.cv.configure(scrollregion=(0, 0, self.canvas_w, self.canvas_h))

    def attach_point(self, box, point):
        cx, cy = box["x"] + box["w"] / 2, box["y"] + box["h"] / 2
        dx, dy = point["x"] - cx, point["y"] - cy
        if dx == 0 and dy == 0:
            return cx, cy
        tx = (box["w"] / 2) / abs(dx) if dx else float("inf")
        ty = (box["h"] / 2) / abs(dy) if dy else float("inf")
        t = min(tx, ty)
        return cx + dx * t, cy + dy * t

    def refresh_label(self, i):
        lb = self.labels[i]
        b, p = lb["box"], lb["point"]
        it = self.items[i]
        ax, ay = self.attach_point(b, p)
        self.cv.coords(it["line"], ax, ay, p["x"], p["y"])
        self.cv.coords(it["rect"], b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"])
        self.cv.coords(it["text"], b["x"] + b["w"] / 2, b["y"] + b["h"] / 2)
        r = 6
        self.cv.coords(it["dot"], p["x"] - r, p["y"] - r, p["x"] + r, p["y"] + r)

    # ---------- Kästchen hinzufügen / umbenennen / löschen ----------

    def add_box(self):
        text = simpledialog.askstring("Neues Kästchen", "Beschriftung:",
                                      parent=self.root)
        if not text:
            return
        ix, iy, iw, ih = self.img_rect
        w = self.font.measure(text) + 30
        n = sum(1 for lb in self.labels if lb["id"].startswith("custom"))
        self.labels.append({
            "id": f"custom_{n}", "text": text,
            "box": {"x": ix - GAP - w, "y": iy + 40 * (n % 5), "w": w, "h": 34},
            "point": {"x": ix + iw // 2, "y": iy + ih // 2},
        })
        self.dirty = True
        self.normalize_boxes()
        self.draw()
        self.select(("bx", len(self.labels) - 1))

    def on_double(self, e):
        x, y = self.cv.canvasx(e.x), self.cv.canvasy(e.y)
        for item in reversed(self.cv.find_overlapping(x - 3, y - 3, x + 3, y + 3)):
            for tag in self.cv.gettags(item):
                if tag.startswith("bx") and len(tag) > 2:
                    self.rename_box(int(tag[2:]))
                    return

    def rename_box(self, i):
        lb = self.labels[i]
        t = simpledialog.askstring("Kästchen umbenennen", "Beschriftung:",
                                   initialvalue=lb["text"], parent=self.root)
        if not t or t == lb["text"]:
            return
        b = lb["box"]
        nw = self.font.measure(t) + 30
        b["x"] += (b["w"] - nw) / 2
        b["w"] = nw
        lb["text"] = t
        self.dirty = True
        self.normalize_boxes()
        self.draw()

    def delete_selected(self):
        if not self.sel or self.sel[0] != "bx":
            return
        del self.labels[self.sel[1]]
        self.dirty = True
        self.select(None)
        self.normalize_boxes()
        self.draw()

    # ---------- Ziehen ----------

    def on_press(self, e):
        x, y = self.cv.canvasx(e.x), self.cv.canvasy(e.y)
        hit = None
        for item in reversed(self.cv.find_overlapping(x - 4, y - 4, x + 4, y + 4)):
            for tag in self.cv.gettags(item):
                if tag.startswith("pt") and len(tag) > 2:
                    hit = ("pt", int(tag[2:]))
                elif tag.startswith("bx") and len(tag) > 2 and not hit:
                    hit = ("bx", int(tag[2:]))
            if hit and hit[0] == "pt":
                break
        if not hit:
            self.drag = None
            self.select(None)
            return
        kind, idx = hit
        self.drag = (kind, idx, x, y)
        self.select(hit)

    def select(self, hit):
        if self.sel:
            kind, idx = self.sel
            if kind == "bx":
                self.cv.itemconfigure(self.items[idx]["rect"],
                                      outline="#17634d", width=2)
            else:
                self.cv.itemconfigure(self.items[idx]["dot"], fill="#c0392b")
        self.sel = hit
        if hit:
            kind, idx = hit
            if kind == "bx":
                self.cv.itemconfigure(self.items[idx]["rect"],
                                      outline="#e67e22", width=3)
            else:
                self.cv.itemconfigure(self.items[idx]["dot"], fill="#e67e22")

    def on_drag(self, e):
        if not self.drag:
            return
        kind, idx, sx, sy = self.drag
        x, y = self.cv.canvasx(e.x), self.cv.canvasy(e.y)
        dx, dy = x - sx, y - sy
        lb = self.labels[idx]
        if kind == "bx":
            b = lb["box"]
            b["x"] += dx
            b["y"] += dy
        else:
            p = lb["point"]
            p["x"], p["y"] = self.clamp_point(p["x"] + dx, p["y"] + dy)
        self.drag = (kind, idx, x, y)
        self.refresh_label(idx)
        self.dirty = True

    def on_release(self, e):
        self.drag = None

    def nudge(self, dx, dy, e):
        if not self.sel:
            return
        step = 10 if e.state & 0x0001 else 1
        kind, idx = self.sel
        lb = self.labels[idx]
        if kind == "bx":
            b = lb["box"]
            b["x"] += dx * step
            b["y"] += dy * step
        else:
            p = lb["point"]
            p["x"], p["y"] = self.clamp_point(p["x"] + dx * step,
                                              p["y"] + dy * step)
        self.refresh_label(idx)
        self.dirty = True

    # ---------- Grenzen ----------

    def clamp_point(self, x, y):
        ix, iy, iw, ih = self.img_rect
        return (min(max(x, ix + 6), ix + iw - 6),
                min(max(y, iy + 6), iy + ih - 6))

    # ---------- Speichern ----------

    def crop_rect(self):
        ix, iy, iw, ih = self.img_rect
        x0, y0, x1, y1 = ix, iy, ix + iw, iy + ih
        for lb in self.labels:
            b = lb["box"]
            x0 = min(x0, b["x"]); y0 = min(y0, b["y"])
            x1 = max(x1, b["x"] + b["w"]); y1 = max(y1, b["y"] + b["h"])
        x0 = max(0, x0 - CROP_PAD); y0 = max(0, y0 - CROP_PAD)
        x1 = min(self.canvas_w, x1 + CROP_PAD)
        y1 = min(self.canvas_h, y1 + CROP_PAD)
        return {"x": round(x0), "y": round(y0),
                "w": round(x1 - x0), "h": round(y1 - y0)}

    def save(self):
        spec = IMAGES[self.img_index]
        ix, iy, iw, ih = self.img_rect
        self.data[spec["file"]] = {
            "image": {"file": f"Bilder/{spec['file']}",
                      "width": self.orig_size[0], "height": self.orig_size[1]},
            "canvas": {"width": self.canvas_w, "height": self.canvas_h,
                       "scale": round(self.scale, 5)},
            "imageRect": {"x": ix, "y": iy, "w": iw, "h": ih},
            "crop": self.crop_rect(),
            "labels": self.labels,
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        self.dirty = False
        self.root.title(f"Beschriftungs-Editor – {spec['name']} (gespeichert)")

    def reset(self):
        if not messagebox.askyesno("Zurücksetzen",
                                   "Positionen dieses Bildes auf Startwerte?"):
            return
        self.labels = self.default_labels(IMAGES[self.img_index])
        self.dirty = True
        self.select(None)
        self.draw()

    def on_close(self):
        if self.confirm_discard():
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Editor(root)
    root.mainloop()
