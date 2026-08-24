#!/usr/bin/env python3
"""
Builds resume.pdf from the structured content in resume_content.py.

Pure standard-library PDF writer (no third-party packages required).
Text metrics for the PDF base-14 fonts are read from the Adobe font
metrics shipped with groff (/usr/share/groff/*/font/devps/{TR,TB,TI,HB}),
so line breaking, centring and justification are measured exactly.

Usage:  python3 build_resume.py [output.pdf]
"""

import os
import sys
import zlib

from resume_content import CONTENT, NAME, CONTACT

# ---------------------------------------------------------------- page setup

PAGE_W, PAGE_H = 595.276, 841.890          # A4
MARGIN_L = MARGIN_R = 42.0
MARGIN_TOP, MARGIN_BOTTOM = 44.0, 40.0
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

ACCENT = (0x2E / 255, 0x74 / 255, 0xB5 / 255)   # heading blue
BLACK = (0, 0, 0)
RULE_GRAY = (0.62, 0.68, 0.75)

BODY = 10.2
LEADING = 12.3
HEAD_SIZE = 13.0
NAME_SIZE = 20.0
CONTACT_SIZE = 10.5

REGULAR, BOLD, ITALIC, SANS_BOLD = "Times-Roman", "Times-Bold", "Times-Italic", "Helvetica-Bold"

# ------------------------------------------------------------------ metrics

_GROFF_DIRS = ["/usr/share/groff"]
_FONT_FILE = {REGULAR: "TR", BOLD: "TB", ITALIC: "TI", SANS_BOLD: "HB"}

# WinAnsiEncoding: code -> Adobe glyph name (only the range we actually use)
_ASCII_NAMES = {
    32: "space", 33: "exclam", 34: "quotedbl", 35: "numbersign", 36: "dollar",
    37: "percent", 38: "ampersand", 39: "quotesingle", 40: "parenleft",
    41: "parenright", 42: "asterisk", 43: "plus", 44: "comma", 45: "hyphen",
    46: "period", 47: "slash", 58: "colon", 59: "semicolon", 60: "less",
    61: "equal", 62: "greater", 63: "question", 64: "at", 91: "bracketleft",
    92: "backslash", 93: "bracketright", 94: "asciicircum", 95: "underscore",
    96: "grave", 123: "braceleft", 124: "bar", 125: "braceright",
    126: "asciitilde",
}
_DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
for _i, _n in enumerate(_DIGITS):
    _ASCII_NAMES[48 + _i] = _n
for _c in range(65, 91):
    _ASCII_NAMES[_c] = chr(_c)
for _c in range(97, 123):
    _ASCII_NAMES[_c] = chr(_c)

_HIGH_NAMES = {0x92: "quoteright", 0x93: "quotedblleft", 0x94: "quotedblright",
               0x95: "bullet", 0x96: "endash", 0x97: "emdash", 0xD7: "multiply",
               0xA0: "space"}
CODE_NAMES = dict(_ASCII_NAMES)
CODE_NAMES.update(_HIGH_NAMES)

# unicode -> WinAnsi byte for the non-ASCII characters used in the resume
UNI_TO_WINANSI = {
    "\u2018": 0x91, "\u2019": 0x92, "\u201c": 0x93, "\u201d": 0x94,
    "\u2022": 0x95, "\u2013": 0x96, "\u2014": 0x97, "\u00d7": 0xD7,
    "\u00a0": 0xA0,
}


def _devps_dir():
    for root in _GROFF_DIRS:
        for dirpath, dirnames, filenames in os.walk(root):
            if os.path.basename(dirpath) == "devps" and "TR" in filenames:
                return dirpath
    raise RuntimeError("groff devps font metrics not found")


def _load_widths(devps, ps_name):
    """glyph name -> width (1/1000 em) parsed from a groff devps font file."""
    widths = {}
    with open(os.path.join(devps, _FONT_FILE[ps_name]), encoding="latin-1") as fh:
        in_charset = False
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("charset"):
                in_charset = True
                continue
            if not in_charset or not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 5 or parts[1].strip() == '"':
                continue
            widths[parts[-1].strip()] = float(parts[1].split(",")[0])
    return widths


_DEVPS = _devps_dir()
WIDTHS = {}          # font -> {byte code: width/1000}
for _f in _FONT_FILE:
    _gw = _load_widths(_DEVPS, _f)
    WIDTHS[_f] = {code: _gw[name] / 1000.0 for code, name in CODE_NAMES.items() if name in _gw}


def encode(text):
    """Unicode -> WinAnsi byte string."""
    out = bytearray()
    for ch in text:
        if ch in UNI_TO_WINANSI:
            out.append(UNI_TO_WINANSI[ch])
        elif ord(ch) < 127:
            out.append(ord(ch))
        else:
            out.append(63)      # '?' fallback
    return bytes(out)


def width_of(text, font, size):
    table = WIDTHS[font]
    default = table[32]
    return sum(table.get(b, default) for b in encode(text)) * size


# -------------------------------------------------------------- pdf plumbing

def pdf_escape(data):
    return data.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


class Document:
    def __init__(self):
        self.pages = []
        self._ops = None
        self.new_page()

    def new_page(self):
        self._ops = []
        self.pages.append(self._ops)
        self.y = PAGE_H - MARGIN_TOP

    def op(self, text):
        self._ops.append(text)

    # --- drawing primitives -------------------------------------------------
    def text_at(self, s, x, y, font, size, color=BLACK, word_space=0.0):
        if not s:
            return
        self.op("BT")
        self.op(f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg")
        self.op(f"/{font.replace('-', '')} {size:.2f} Tf")
        if word_space:
            self.op(f"{word_space:.3f} Tw")
        self.op(f"1 0 0 1 {x:.2f} {y:.2f} Tm")
        self.op(f"({pdf_escape(encode(s)).decode('latin-1')}) Tj")
        if word_space:
            self.op("0 Tw")
        self.op("ET")

    def rule(self, y, x0=MARGIN_L, x1=PAGE_W - MARGIN_R, thickness=0.7, color=RULE_GRAY):
        self.op(f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} RG")
        self.op(f"{thickness:.2f} w")
        self.op(f"{x0:.2f} {y:.2f} m {x1:.2f} {y:.2f} l S")

    def ensure(self, needed):
        if self.y - needed < MARGIN_BOTTOM:
            self.new_page()

    # --- rich text ----------------------------------------------------------
    @staticmethod
    def tokenize(runs):
        """[(text, font)] -> [(word, font)] preserving run fonts."""
        tokens = []
        for text, font in runs:
            for word in text.split(" "):
                if word:
                    tokens.append((word, font))
        return tokens

    def wrap(self, runs, size, avail_first, avail_rest=None):
        avail_rest = avail_first if avail_rest is None else avail_rest
        lines, current, cur_w = [], [], 0.0
        avail = avail_first
        for word, font in self.tokenize(runs):
            w = width_of(word, font, size)
            space = width_of(" ", font, size) if current else 0.0
            if current and cur_w + space + w > avail + 0.01:
                lines.append(current)
                current, cur_w, avail = [(word, font, w)], w, avail_rest
            else:
                current.append((word, font, w))
                cur_w += space + w
        if current:
            lines.append(current)
        return lines

    def draw_line(self, line, x, y, size, avail, justify):
        natural = sum(w for _, _, w in line)
        spaces = len(line) - 1
        space_w = width_of(" ", line[0][1], size) if line else 0.0
        extra = 0.0
        if justify and spaces:
            extra = (avail - natural - spaces * space_w) / spaces
            if extra < 0:
                extra = 0.0
        cursor = x
        for i, (word, font, w) in enumerate(line):
            self.text_at(word, cursor, y, font, size)
            cursor += w
            if i < spaces:
                cursor += space_w + extra

    def paragraph(self, runs, size=BODY, leading=LEADING, x=MARGIN_L,
                  indent=0.0, avail=None, justify=True, space_after=0.0):
        avail = CONTENT_W if avail is None else avail
        lines = self.wrap(runs, size, avail - indent, avail)
        for i, line in enumerate(lines):
            self.ensure(leading)
            lx = x + (indent if i == 0 else 0.0)
            la = avail - (indent if i == 0 else 0.0)
            last = i == len(lines) - 1
            self.draw_line(line, lx, self.y - size * 0.86, size, la, justify and not last)
            self.y -= leading
        self.y -= space_after

    def bullet(self, runs, size=BODY, leading=LEADING, x=MARGIN_L, hang=13.0,
               avail=None, justify=True, space_after=2.0, marker="\u2022"):
        avail = CONTENT_W if avail is None else avail
        lines = self.wrap(runs, size, avail - hang, avail - hang)
        for i, line in enumerate(lines):
            self.ensure(leading)
            baseline = self.y - size * 0.86
            if i == 0:
                self.text_at(marker, x + 3, baseline, REGULAR, size)
            last = i == len(lines) - 1
            self.draw_line(line, x + hang, baseline, size, avail - hang, justify and not last)
            self.y -= leading
        self.y -= space_after

    def heading(self, title):
        self.ensure(HEAD_SIZE + 14)
        self.y -= 4
        self.rule(self.y)
        self.y -= 3
        self.text_at(title, MARGIN_L, self.y - HEAD_SIZE * 0.86, BOLD, HEAD_SIZE, ACCENT)
        self.y -= HEAD_SIZE * 1.18
        self.y -= 2

    def centered(self, s, font, size, color=BLACK):
        self.ensure(size * 1.3)
        x = MARGIN_L + (CONTENT_W - width_of(s, font, size)) / 2
        self.text_at(s, x, self.y - size * 0.86, font, size, color)
        self.y -= size * 1.25

    def left_right(self, left_runs, right, size=BODY, leading=LEADING):
        self.ensure(leading)
        baseline = self.y - size * 0.86
        cursor = MARGIN_L
        for text, font in left_runs:
            self.text_at(text, cursor, baseline, font, size)
            cursor += width_of(text, font, size)
        if right:
            rx = PAGE_W - MARGIN_R - width_of(right, REGULAR, size)
            self.text_at(right, rx, baseline, REGULAR, size)
        self.y -= leading

    # --- serialise ----------------------------------------------------------
    def build(self):
        objects = []                      # 1-indexed list of byte strings

        def add(body):
            objects.append(body)
            return len(objects)

        font_ids = {}
        for font in [REGULAR, BOLD, ITALIC, SANS_BOLD]:
            font_ids[font] = add(
                b"<< /Type /Font /Subtype /Type1 /BaseFont /" + font.encode()
                + b" /Encoding /WinAnsiEncoding >>")
        res = (b"<< /Font << "
               + b" ".join(f"/{f.replace('-', '')} {i} 0 R".encode()
                           for f, i in font_ids.items())
               + b" >> >>")

        pages_id = len(objects) + 1 + 2 * len(self.pages)
        page_ids = []
        for ops in self.pages:
            stream = zlib.compress("\n".join(ops).encode("latin-1"))
            content_id = add(b"<< /Length " + str(len(stream)).encode()
                             + b" /Filter /FlateDecode >>\nstream\n" + stream + b"\nendstream")
            page_ids.append(add(
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox "
                f"[0 0 {PAGE_W:.3f} {PAGE_H:.3f}] /Contents {content_id} 0 R "
                "/Resources ".encode() + res + b" >>"))
        add(b"<< /Type /Pages /Count " + str(len(page_ids)).encode() + b" /Kids ["
            + b" ".join(f"{i} 0 R".encode() for i in page_ids) + b"] >>")
        catalog_id = add(b"<< /Type /Catalog /Pages " + str(pages_id).encode() + b" 0 R >>")
        info_id = add(b"<< /Title (" + encode(NAME + " - Resume")
                      + b") /Author (" + encode(NAME) + b") /Producer (build_resume.py) >>")

        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = []
        for num, body in enumerate(objects, start=1):
            offsets.append(len(out))
            out += f"{num} 0 obj\n".encode() + body + b"\nendobj\n"
        xref = len(out)
        out += f"xref\n0 {len(objects) + 1}\n".encode()
        out += b"0000000000 65535 f \n"
        for off in offsets:
            out += f"{off:010d} 00000 n \n".encode()
        out += (f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R "
                f"/Info {info_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n").encode()
        return bytes(out)


# ------------------------------------------------------------------- render

def render():
    doc = Document()
    doc.centered(NAME, BOLD, NAME_SIZE, ACCENT)
    doc.centered(CONTACT, BOLD, CONTACT_SIZE, ACCENT)
    doc.y -= 1

    for block in CONTENT:
        kind = block["type"]

        if kind == "section":
            doc.heading(block["title"])

        elif kind == "paragraph":
            doc.paragraph(block["runs"], space_after=block.get("space_after", 2.0),
                          justify=block.get("justify", True))

        elif kind == "bullet":
            doc.bullet(block["runs"], space_after=block.get("space_after", 3.0),
                       justify=block.get("justify", True),
                       x=MARGIN_L + block.get("x_offset", 8.0),
                       avail=CONTENT_W - block.get("x_offset", 8.0))

        elif kind == "entry":                      # heading line + right-aligned date
            doc.left_right(block["runs"], block.get("right", ""))

        elif kind == "columns":                    # skills grid
            cols = block["columns"]
            col_w = CONTENT_W / len(cols)
            rows = max(len(c) for c in cols)
            for r in range(rows):
                doc.ensure(LEADING)
                baseline = doc.y - BODY * 0.86
                for ci, col in enumerate(cols):
                    if r < len(col):
                        x = MARGIN_L + ci * col_w + block.get("indent", 10.0)
                        doc.text_at("\u2022", x, baseline, REGULAR, BODY)
                        doc.text_at(col[r], x + 9, baseline, REGULAR, BODY)
                doc.y -= LEADING
            doc.y -= 2

        elif kind == "labeled":                    # "Hobbies   : Book Reading"
            doc.ensure(LEADING)
            baseline = doc.y - BODY * 0.86
            doc.text_at(block["label"], MARGIN_L + 4, baseline, BOLD, BODY)
            doc.text_at(": " + block["value"], MARGIN_L + 4 + block.get("label_w", 62.0),
                        baseline, REGULAR, BODY)
            doc.y -= LEADING

        elif kind == "space":
            doc.y -= block.get("amount", 4.0)

        else:
            raise ValueError(f"unknown block type: {kind}")

    doc.y -= 4
    doc.rule(doc.y)
    return doc


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "resume.pdf"
    document = render()
    data = document.build()
    with open(target, "wb") as fh:
        fh.write(data)
    print(f"wrote {target}: {len(data)} bytes, {len(document.pages)} page(s)")
