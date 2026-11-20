"""Translate the built English desk pages into French, Kiswahili and Brazilian Portuguese.

Every visible text, the page title, descriptions and accessibility labels are looked up by their exact
English text in src/i18n/<lang>.json. A missing translation stops the build and is listed in
src/i18n/missing-<lang>.txt, so no English slips onto a translated page. Article titles in the sources
list stay in their original language. Pages are written under /fr/, /sw/ and /pt/ with the same paths."""
import json, re, pathlib
from bs4 import BeautifulSoup, NavigableString, Comment
from bs4.element import PreformattedString
import i18n_rules

NAMES = set()  # player, scorer, coach and club names, kept as written


def lookup(k, lang, d):
    if not needs(k):
        return k
    if k in d:
        return d[k]
    sub = lambda x: lookup(x, lang, d)
    return i18n_rules.rule(lang, k, NAMES, sub)

BASE = "https://afritech-advisory.github.io/Afritech-Advisory-afritech-tournament-desk/"
HOME = "https://afritechsports.github.io/"
LABEL = {"en": "Language", "fr": "Langue", "sw": "Lugha", "pt": "Idioma"}
LANGS = [("en", "English", "en"), ("fr", "Français", "fr"), ("sw", "Kiswahili", "sw"), ("pt", "Português", "pt-BR")]
ATTRS = ("alt", "title", "aria-label", "placeholder")
META = {("name", "description"), ("property", "og:title"), ("property", "og:description"), ("name", "twitter:title"), ("name", "twitter:description")}
LETTER = re.compile(r"[A-Za-zÀ-ÿ]{2,}")
SWITCH_CSS = """<style id="afs-lang-css">.afs-lang{background:#0B1C33;font:600 13px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;text-align:center;padding:6px 8px}
.afs-lang a{color:#C9D6E6;text-decoration:none;padding:6px 8px;border-radius:6px;display:inline-block}.afs-lang a.on{background:#14B8A6;color:#06221F}</style>"""


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def needs(s):
    return bool(LETTER.search(s))


def skip_node(node):
    for p in node.parents:
        if p.name in ("script", "style"):
            return True
        if p.get("translate") == "no":
            return True
        if p.name == "details" and "src" in (p.get("class") or []) and node.parent.name != "summary":
            return True
    return False


def keys(html):
    """All English strings on a page that need a translation."""
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for s in soup.find_all(string=True):
        if isinstance(s, PreformattedString) or skip_node(s):
            continue
        t = norm(s)
        if t and needs(t):
            out.append(t)
    for el in soup.find_all(True):
        if any(p.get("translate") == "no" for p in [el] + list(el.parents)):
            continue
        for a in ATTRS:
            if el.has_attr(a) and needs(el[a]):
                out.append(norm(el[a]))
        if el.name == "meta":
            for k, v in META:
                if el.get(k) == v and el.get("content") and needs(el["content"]):
                    out.append(norm(el["content"]))
    return out


def switcher(rel, lang):
    links = []
    for code, name, _ in LANGS:
        href = BASE + ("" if code == "en" else code + "/") + rel
        links.append(f'<a href="{href}" hreflang="{code}"{" class=on" if code == lang else ""}>{name}</a>')
    return f'<!-- afs-lang:start -->{SWITCH_CSS}<nav class="afs-lang" aria-label="' + LABEL[lang] + '">' + "".join(links) + "</nav><!-- afs-lang:end -->"


def alternates(rel):
    return "".join(f'<link rel="alternate" hreflang="{hl}" href="{BASE + ("" if c == "en" else c + "/") + rel}">' for c, _, hl in LANGS)


def add_switch(html, rel, lang):
    """Language bar right after the Afritech Sports site bar, and hreflang links in the head."""
    html = re.sub(r"<!-- afs-lang:start -->.*?<!-- afs-lang:end -->", "", html, flags=re.S)
    html = re.sub(r'<link rel="alternate" hreflang=[^>]*>', "", html)
    html = html.replace("</head>", alternates(rel) + "</head>", 1)
    i = html.find("<!-- afs-bar:end -->")
    if i < 0:
        i = html.index(">", html.index("<body")) + 1
    else:
        i += len("<!-- afs-bar:end -->")
    return html[:i] + switcher(rel, lang) + html[i:]


def translate(html, rel, lang, d, missing):
    soup = BeautifulSoup(html, "html.parser")
    def tr(t):
        k = norm(t)
        r = lookup(k, lang, d)
        if r is not None:
            return r
        missing.add(k)
        return t
    for s in soup.find_all(string=True):
        if isinstance(s, PreformattedString) or skip_node(s):
            continue
        t = norm(s)
        if t and needs(t):
            lead = s[: len(s) - len(s.lstrip())]
            trail = s[len(s.rstrip()):]
            s.replace_with(NavigableString(lead + tr(t) + trail))
    for el in soup.find_all(True):
        if any(p.get("translate") == "no" for p in [el] + list(el.parents)):
            continue
        for a in ATTRS:
            if el.has_attr(a) and needs(el[a]):
                el[a] = tr(el[a])
        if el.name == "meta":
            for k, v in META:
                if el.get(k) == v and el.get("content") and needs(el["content"]):
                    el["content"] = tr(el["content"])
        if el.name == "a" and el.get("href", "").startswith(HOME):
            h = el["href"]
            el["href"] = h + ("&" if "?" in h else "?") + "lang=" + lang if "lang=" not in h else h
    for sc in soup.find_all("script"):
        txt = sc.string
        if txt:
            for en_s, t in d.get("__js__", {}).items():
                txt = txt.replace(en_s, t)
            sc.string = txt
    out = str(soup)
    hl = dict((c, h) for c, _, h in LANGS)[lang]
    out = re.sub(r'<html lang="[^"]*"', f'<html lang="{hl}"', out, 1)
    # canonical, og:url and the desk's own links point at this language's copy
    out = out.replace(BASE + rel + '"', BASE + lang + "/" + rel + '"')
    out = out.replace('href="' + BASE + '"', 'href="' + BASE + lang + '/"')
    return out


def build(root, pages):
    """pages: {relative output path: English html}. Writes translated copies and returns English pages with the switcher."""
    report = {}
    for f in ("scouting", "nations", "results"):
        data = json.loads((root / f"src/data/qatar-u17-2026-{f}.json").read_text())
        for p in data.get("players", []):
            NAMES.update(x for x in (p["name"], p.get("club")) if x)
        for n in data.get("nations", []):
            NAMES.add(n["coach"])
            for m in n["matches"]:
                NAMES.update(g["who"] for g in m.get("goals", []))
        for m in data.get("matches", []):
            NAMES.update(g["who"] for g in m.get("goals", []))
    NAMES.update({"Afritech Sports", "Afritech Tournament Desk", "Afritech Sports Technology and Innovation Group Limited", "WhatsApp", "html", "Olympique de Marseille", "Zamalek", "Black Bulls", "Costa do Sol", "Sydney FC"})
    for code, _, _ in LANGS[1:]:
        f = root / "src/i18n" / f"{code}.json"
        d = json.loads(f.read_text()) if f.exists() else {}
        missing = set()
        for out, html in pages.items():
            rel = out[:-len("index.html")] if out.endswith("index.html") else out
            t = translate(html, rel, code, d, missing)
            t = add_switch(t, rel, code)
            p = root / code / out
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(t)
        mf = root / "src/i18n" / f"missing-{code}.txt"
        if missing:
            mf.write_text("\n".join(sorted(missing)) + "\n")
        elif mf.exists():
            mf.unlink()
        report[code] = len(missing)
    english = {}
    for out, html in pages.items():
        rel = out[:-len("index.html")] if out.endswith("index.html") else out
        english[out] = add_switch(html, rel, "en")
    return english, report
