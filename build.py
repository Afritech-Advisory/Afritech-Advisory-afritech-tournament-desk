"""Build the public pages: inline fonts, the Afritech emblem and flags so each page is self-contained,
and render the player radars from src/data/qatar-u17-2026-radars.json."""
import base64, pathlib, sys
root = pathlib.Path(__file__).parent
sys.path.insert(0, str(root / "src"))
import radar, sitebar, nations, scouting, i18n

fonts = (root / "src/fonts.css").read_text()
emblem = "data:image/png;base64," + base64.b64encode((root / "src/emblem.png").read_bytes()).decode()
flags = "\n".join(".fl-%s{background-image:url(data:image/png;base64,%s)}" % (f.stem, base64.b64encode(f.read_bytes()).decode())
                  for f in sorted((root / "src/flags").glob("*.png")))
pages = {
    "src/qatar-u17-2026.html": ("qatar-u17-2026/index.html", {}),
    "src/index.html": ("index.html", {}),
    "src/radars.html": ("qatar-u17-2026/radars/index.html", radar.build_content(root / "src/data/qatar-u17-2026-radars.json")),
}
built = {}
for src, (out, extra) in pages.items():
    html = (root / src).read_text().replace("{{FONTS}}", fonts).replace("{{EMBLEM}}", emblem).replace("{{FLAGS}}", flags)
    for k, v in extra.items():
        html = html.replace(k, v)
    if src == "src/qatar-u17-2026.html":
        nd, sd = scouting.load(root)
        a = html.index('<div class="board">') + len('<div class="board">')
        b = html.index('</div>\n  <p class="fine" style="margin-top:12px"><a class="btn primary" href="radars/"', a)
        html = html[:a] + scouting.board_html(nd, sd) + html[b:]
        html = html.replace('<p class="note">All players on this board are under 18.',
                            '<h3 style="margin-top:22px">Goal involvements so far</h3>' + scouting.peer_svg(nd, sd) + '<p class="note">All players on this board are under 18.', 1)
        html = html.replace("{{RESULTS}}", scouting.results_html(nd, nations.flag))
        html = html.replace("</style>", scouting.CSS + scouting.RESULTS_CSS + "</style>", 1)
        html = html.replace("</body>", scouting.YT_LOADER + scouting.CARD_JS + "</body>", 1)
    built[out] = sitebar.inject(html, "desk", "desk")
pages_n, _ = nations.build(root, fonts, emblem, flags)
for out, html in pages_n.items():
    built[out] = sitebar.inject(html, "desk", "desk")
# Desk pages keep readers on the desk (Andrew, 23 Nov 2026, Gatekeeper A3): every outside link becomes plain text;
# the source stays named, the address is not clickable. Contact routes stay live (Andrew, 23 Nov 2026): WhatsApp,
# Afritech's and Andrew's LinkedIn pages, and Afritech Sports' own sites (home site, Player CVs, this desk).
import re as _re
DESK = "https://afritech-advisory.github.io/Afritech-Advisory-afritech-tournament-desk/"
def _local(html):
    def sub(m):
        u = m.group(1)
        if u.startswith(("https://wa.me/", DESK, "https://www.linkedin.com/company/afritech-sports-technology-and-innovation-group-limited", "https://www.linkedin.com/in/andrew-r-b1b514", "https://afritech-advisory.github.io/", "https://afritechsports.github.io/")):
            return m.group(0)
        return f'<span class="src-ref">{m.group(2)}</span>'
    return _re.sub(r'<a\b[^>]*?href="(https?://[^"]+)"[^>]*>(.*?)</a>', sub, html, flags=_re.S)
built = {k: _local(v) for k, v in built.items()}
# English pages plus French, Kiswahili and Brazilian Portuguese copies under /fr/, /sw/ and /pt/
import runpy; runpy.run_path(str(root / 'src/i18n/make_json.py'))
english, report = i18n.build(root, built)
for out, html in english.items():
    (root / out).parent.mkdir(parents=True, exist_ok=True)
    (root / out).write_text(html)
    print(out, len(html))
missing = {k: v for k, v in report.items() if v}
if missing:
    sys.exit("Missing translations (see src/i18n/missing-<lang>.txt): " + ", ".join(f"{k} {v}" for k, v in missing.items()))
print("translations complete:", ", ".join(report))
