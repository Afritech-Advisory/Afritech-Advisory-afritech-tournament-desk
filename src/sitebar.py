"""Afritech Sports site bar: one shared header (Home button + menu) for pages outside the home site.
Self-contained (no fonts, images or scripts loaded), so offline match dashboards stay offline-safe."""
H = "https://afritechsports.github.io/"
LINKS = [("home", "Home", H), ("tech", "Sports Technology", H + "technology/"),
         ("adv", "Advisory Services", H + "advisory/"), ("inn", "Innovation", H + "innovation/")]
DESKS = [("miq", "MatchIQ library", "https://afritech-advisory.github.io/afritech-matchiq/"),
         ("desk", "U-17 Tournament Desk", "https://afritech-advisory.github.io/Afritech-Advisory-afritech-tournament-desk/"),
         ("cv", "CV Desk", "https://afritech-advisory.github.io/afritech-sports-cv-desk/")]
CSS = """<style id="afs-bar-css">
.afs-bar{background:#0F2442;color:#fff;font:600 15px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;position:relative;z-index:60}
.afs-bar *{box-sizing:border-box}
.afs-in{max-width:1240px;margin:0 auto;padding:0 14px;display:flex;align-items:center;gap:6px;min-height:52px}
.afs-bar a.afs-brand{flex-direction:column;align-items:flex-start;justify-content:center}
.afs-brand{color:#fff;text-decoration:none;font-weight:800;font-size:17px;letter-spacing:.3px;margin-right:10px;white-space:nowrap}
.afs-brand small{display:block;font-size:10px;font-weight:700;letter-spacing:1.4px;opacity:.7;text-transform:uppercase}
.afs-bar a,.afs-bar summary{color:#E6EEF7;text-decoration:none;padding:10px 9px;border-radius:8px;cursor:pointer;white-space:nowrap;display:inline-flex;align-items:center;min-height:44px}
.afs-bar a:hover,.afs-bar summary:hover{background:#1A365D;color:#fff}
.afs-bar a.on{box-shadow:inset 0 -3px 0 #14B8A6;color:#fff;border-radius:0}
.afs-bar summary{list-style:none}.afs-bar summary::-webkit-details-marker{display:none}
.afs-links{display:none;align-items:center;gap:2px;flex:1}
.afs-links summary:after{content:" \\25BE";white-space:pre}
.afs-bar a.afs-talk{background:#1F8F4E;color:#fff;font-weight:700;padding:10px 14px;margin-left:auto}
.afs-bar a.afs-talk:hover{background:#25a35a}
.afs-dd{position:relative}
.afs-list{position:absolute;top:100%;left:0;min-width:240px;background:#0F2442;border-radius:0 0 12px 12px;padding:6px;box-shadow:0 14px 30px rgba(0,0,0,.35);display:flex;flex-direction:column}
.afs-list a{border-radius:8px}
.afs-list .afs-talk{margin:8px 4px 4px;justify-content:center}
.afs-lab{color:#14B8A6;font-size:11px;font-weight:800;letter-spacing:1.3px;text-transform:uppercase;padding:12px 10px 4px;border-top:1px solid rgba(255,255,255,.12);margin-top:6px}
.afs-mob{display:flex;align-items:center;margin-left:auto;gap:4px}
.afs-mob .afs-list{left:auto;right:0}
@media (min-width:960px){.afs-links{display:flex}.afs-mob{display:none}}
@media (max-width:959px){.afs-brand small{display:none}.afs-brand{margin-right:0;font-size:16px}.afs-in{padding:0 8px}}
@media print{.afs-bar{display:none}}
</style>"""

def bar(active="", src="site"):
    talk = H + "?src=" + src + "#talk"
    prim = "".join(f'<a href="{u}"{" class=on aria-current=page" if k == active else ""}>{t}</a>' for k, t, u in LINKS)
    desks = "".join(f'<a href="{u}"{" class=on aria-current=page" if k == active else ""}>{t}</a>' for k, t, u in DESKS)
    js = ("<script>(function(){document.addEventListener('click',function(e){document.querySelectorAll('.afs-bar details[open]')"
          ".forEach(function(d){if(!d.contains(e.target))d.open=false})})})();</script>")
    return (f'<!-- afs-bar:start -->{CSS}<nav class="afs-bar" aria-label="Afritech Sports"><div class="afs-in">'
            f'<a class="afs-brand" href="{H}">Afritech Sports<small>Technology and Innovation Group</small></a>'
            f'<div class="afs-links">{prim}<details class="afs-dd"><summary>Our desks</summary><div class="afs-list">{desks}</div></details>'
            f'<a class="afs-talk" href="{talk}">Talk to us</a></div>'
            f'<div class="afs-mob"><a href="{H}">&#8962; Home</a><details class="afs-dd"><summary>&#9776; Menu</summary><div class="afs-list">'
            f'{prim}<span class="afs-lab">Our desks</span>{desks}<a class="afs-talk" href="{talk}">Talk to us on WhatsApp</a></div></details></div>'
            f'</div></nav>{js}<!-- afs-bar:end -->')

def inject(html, active, src):
    import re
    html = re.sub(r"<!-- afs-bar:start -->.*?<!-- afs-bar:end -->", "", html, flags=re.S)
    i = html.index("<body"); j = html.index(">", i) + 1
    return html[:j] + bar(active, src) + html[j:]
