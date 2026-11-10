"""Build the public pages: inline fonts, the Afritech emblem and flags so each page is self-contained,
and render the player radars from src/data/qatar-u17-2026-radars.json."""
import base64, pathlib, sys
root = pathlib.Path(__file__).parent
sys.path.insert(0, str(root / "src"))
import radar

fonts = (root / "src/fonts.css").read_text()
emblem = "data:image/png;base64," + base64.b64encode((root / "src/emblem.png").read_bytes()).decode()
flags = "\n".join(".fl-%s{background-image:url(data:image/png;base64,%s)}" % (f.stem, base64.b64encode(f.read_bytes()).decode())
                  for f in sorted((root / "src/flags").glob("*.png")))
pages = {
    "src/qatar-u17-2026.html": ("qatar-u17-2026/index.html", {}),
    "src/index.html": ("index.html", {}),
    "src/radars.html": ("qatar-u17-2026/radars/index.html", radar.build_content(root / "src/data/qatar-u17-2026-radars.json")),
}
for src, (out, extra) in pages.items():
    html = (root / src).read_text().replace("{{FONTS}}", fonts).replace("{{EMBLEM}}", emblem).replace("{{FLAGS}}", flags)
    for k, v in extra.items():
        html = html.replace(k, v)
    (root / out).parent.mkdir(parents=True, exist_ok=True)
    (root / out).write_text(html)
    print(out, len(html))
