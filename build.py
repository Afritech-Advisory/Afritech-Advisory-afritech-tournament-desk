"""Build the public pages: inline fonts and the Afritech emblem so each page is self-contained."""
import base64, pathlib
root = pathlib.Path(__file__).parent
fonts = (root / "src/fonts.css").read_text()
emblem = "data:image/png;base64," + base64.b64encode((root / "src/emblem.png").read_bytes()).decode()
flags = "\n".join(".fl-%s{background-image:url(data:image/png;base64,%s)}" % (f.stem, base64.b64encode(f.read_bytes()).decode()) for f in sorted((root / "src/flags").glob("*.png")))
pages = {"src/qatar-u17-2026.html": "qatar-u17-2026/index.html", "src/index.html": "index.html"}
for src, out in pages.items():
    html = (root / src).read_text().replace("{{FONTS}}", fonts).replace("{{EMBLEM}}", emblem).replace("{{FLAGS}}", flags)
    (root / out).parent.mkdir(parents=True, exist_ok=True)
    (root / out).write_text(html)
    print(out, len(html))
