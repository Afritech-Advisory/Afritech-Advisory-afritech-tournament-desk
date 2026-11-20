"""One page per African nation: results with goal-by-goal match reports (goal times link to FIFA's
official highlights), next fixtures, players to watch and a briefing call to action.
Data: src/data/qatar-u17-2026-nations.json. Styles come from the main desk page so the look stays one system."""
import json, html as H

BASE = "https://afritech-advisory.github.io/Afritech-Advisory-afritech-tournament-desk/qatar-u17-2026/"
WA = "https://wa.me/qr/JU7PO5B5ADCOI1"

EXTRA_CSS = """
/* nation pages */
.crumb{font-size:.92rem;margin-bottom:6px}.crumb a{color:var(--on-navy-muted)}
.hero h1 .fl{width:54px;height:40px;vertical-align:4px;margin-right:12px}
.mr{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;display:grid;gap:12px;margin-bottom:14px;scroll-margin-top:70px}
.mr .when{font-family:var(--mono);font-size:.8rem;color:var(--muted);letter-spacing:.04em}
.sc{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:12px;font-family:var(--display);font-weight:700;font-size:clamp(1.3rem,4.6vw,1.9rem);line-height:1.1}
.sc .r{text-align:right}.sc b{background:var(--navy);color:#fff;border-radius:8px;padding:4px 14px;font-variant-numeric:tabular-nums;white-space:nowrap}
.sc .af{color:var(--teal)}
.res{display:inline-block;font:600 .74rem var(--mono);letter-spacing:.08em;text-transform:uppercase;border-radius:4px;padding:3px 8px;justify-self:start}
.res.W{background:color-mix(in srgb,var(--teal) 18%,transparent);color:var(--teal)}
.res.L{background:color-mix(in srgb,var(--rose) 16%,transparent);color:var(--rose)}
.res.D{background:var(--soft);color:var(--muted)}
.goals{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.goals li{display:grid;grid-template-columns:3.6em minmax(0,1fr);gap:8px;padding:8px 0;border-top:1px solid var(--line);font-size:.97rem}
.goals .m{font-family:var(--mono);font-weight:600;color:var(--orange-text)}
.goals .tm{color:var(--muted);font-size:.88rem}
.goals a{white-space:nowrap;font-weight:600}
.mr .scout{border-left:4px solid var(--orange);padding:6px 0 6px 12px;font-size:.98rem}
.mr .scout b{font-family:var(--display);text-transform:uppercase;letter-spacing:.04em;color:var(--orange-text);margin-right:6px}
.next{display:grid;gap:8px}
.next .fxd{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 10px;align-items:center}
.next .fxd b{margin:0}
.next .fxd .af{font:inherit;color:var(--teal)}
.next .fxd span{color:var(--muted);font-size:.9rem}
.ptw{list-style:none;padding:0;margin:0;display:grid;gap:8px}
.ptw li{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.others{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.others a{display:inline-flex;align-items:center;gap:6px;background:var(--card);border:1px solid var(--line);border-radius:99px;padding:6px 12px;text-decoration:none;color:var(--fg);font-weight:600}
.cta-box{background:var(--navy);color:var(--on-navy);border-radius:12px;padding:22px;display:grid;gap:10px;margin-top:8px}
.cta-box h2{color:#fff}.cta-box p{color:#DCE5F0}
"""


def flag(code, name):
    return f'<i class="fl fl-{code}" role="img" aria-label="{H.escape(name)} flag"></i>'


def team(t, nation):
    return f'<span class="af">{H.escape(t)}</span>' if t == nation else H.escape(t)


def outcome(m, nation):
    a, b = (int(x) for x in m["score"].split("-"))
    mine, theirs = (a, b) if m["home"] == nation else (b, a)
    return "W" if mine > theirs else "L" if mine < theirs else "D"


def match_report(m, nation):
    o = outcome(m, nation)
    word = {"W": "Win", "L": "Defeat", "D": "Draw"}[o]
    goals = []
    for g in m.get("goals", []):
        link = ""
        if g.get("t") is not None and m.get("video"):
            mm, ss = divmod(g["t"], 60)
            link = f' · <a href="{m["video"]}&amp;t={g["t"]}s" target="_blank" rel="noopener">Watch the goal ({mm}:{ss:02d})</a>'
        how = f', {H.escape(g["how"])}' if g.get("how") else ""
        goals.append(f'<li><span class="m">{g["min"]}</span><span><b>{H.escape(g["who"])}</b> <span class="tm">({H.escape(g["team"])})</span>{how}{link}</span></li>')
    video = (f'<p class="fine" style="margin:0"><a href="{m["video"]}" target="_blank" rel="noopener">FIFA\'s official highlights on YouTube</a></p>'
             if m.get("video") else "")
    return (f'<article class="mr" id="{m["id"]}"><p class="when">{m["date"]} · {m["time"]} Doha · {H.escape(m["venue"])}</p>'
            f'<span class="res {o}">{word}</span>'
            f'<div class="sc"><span class="r">{team(m["home"], nation)}</span><b>{m["score"]}</b><span>{team(m["away"], nation)}</span></div>'
            f'<p>{H.escape(m["story"])}</p>'
            f'<h3>Goals</h3><ul class="goals">{"".join(goals)}</ul>'
            f'<p class="scout"><b>Our read</b>{H.escape(m["scout"])}</p>{video}</article>')


def page(n, all_nations, head, emblem, updated):
    name = n["name"]
    played = [m for m in n["matches"] if m.get("score")]
    upcoming = [m for m in n["matches"] if not m.get("score")]
    if played:
        rec = [outcome(m, name) for m in played]
        summary = (f'{len(played)} played: {rec.count("W")} won, {rec.count("D")} drawn, {rec.count("L")} lost. '
                   f'Every goal with its minute, the official highlight and our read for clubs, agents and federations.')
    else:
        f = upcoming[0]
        summary = (f'First match: {f["home"]} v {f["away"]}, {f["date"]}, {f["time"]} Doha time. '
                   f'The match report, goals and our read go up here after the final whistle.')
    reports = "".join(match_report(m, name) for m in played) or \
        '<p class="fine">No match played yet. The report goes up here after the final whistle, with every goal and our read.</p>'
    nxt = "".join(f'<div class="fxd"><b>{team(m["home"], name)} v {team(m["away"], name)}</b>'
                  f'<span class="num">{m["time"]} Doha</span><span>{m["date"]} · {H.escape(m["venue"])}</span></div>' for m in upcoming)
    players = "".join(f"<li>{H.escape(p)}</li>" for p in n["players"]) or \
        f"<li>Our board for {H.escape(name)} is built from the group matches: the standouts are added here after each matchday.</li>"
    others = "".join(f'<a href="../{o["slug"]}/">{flag(o["flag"], o["name"])}{H.escape(o["name"])}</a>'
                     for o in all_nations if o["slug"] != n["slug"])
    subj = f'{name}%20U-17%20World%20Cup%20briefing'.replace(" ", "%20").replace("'", "%27")
    title = f"{name} at the U-17 World Cup 2026: results, goals and players | Afritech Tournament Desk"
    desc = f"{name} at the FIFA U-17 World Cup Qatar 2026: every result, every goal with the official highlight, next matches and the players to watch, from Afritech Sports."
    url = BASE + n["slug"] + "/"
    h = head.replace("<title>Africa's Ten in Qatar | Afritech Tournament Desk</title>", f"<title>{H.escape(title)}</title>")
    h = h.replace('content="Afritech covers all ten African nations at the FIFA U-17 World Cup Qatar 2026: groups, players to watch, match centre and briefings for clubs, agents and federations."',
                  f'content="{H.escape(desc)}"')
    h = h.replace('<meta property="og:title" content="Africa\'s ten at the FIFA U-17 World Cup Qatar 2026">',
                  f'<meta property="og:title" content="{H.escape(name)} at the FIFA U-17 World Cup Qatar 2026">')
    h = h.replace(BASE + '"', url + '"').replace("</style>", EXTRA_CSS + "</style>", 1)
    return f"""{h}
<body>
<header class="bar"><div class="wrap">
  <a class="brand" href="../"><img src="{emblem}" alt="Afritech Sports emblem" width="36" height="39">Tournament Desk</a>
  <nav aria-label="Sections"><a href="#results">Results</a><a href="#next">Next</a><a href="#players">Players</a><a href="../#nations">All nations</a><a class="cta" href="#contact">Book a briefing</a></nav>
</div></header>
<section class="hero" id="top"><div class="wrap" style="grid-template-columns:1fr">
  <div>
    <p class="crumb"><a href="../">Africa's ten in Qatar</a> › {H.escape(name)}</p>
    <p class="eyebrow">FIFA U-17 World Cup Qatar 2026 · Group {n["group"]} · Updated {updated}</p>
    <h1>{flag(n["flag"], name)}{H.escape(name)} <em>match by match.</em></h1>
    <p class="lead">{summary}</p>
    <div class="btns"><a class="btn primary" href="mailto:Advisory@afritechsports.com?subject={subj}">Book a briefing on {H.escape(name)}</a><a class="btn ghost" href="#results">See the results</a></div>
    <div class="chips"><span>Coach: {H.escape(n["coach"])}</span><span>{H.escape(n["route"])}</span></div>
  </div>
</div></section>
<main class="wrap">
<section class="s" id="results">
  <div class="s-head"><p class="eyebrow">Match reports</p><h2>Results and goals</h2>
  <p>Final scores only, after the whistle. Goal times link to FIFA's official highlights on YouTube.</p></div>
  {reports}
</section>
<section class="s" id="next">
  <div class="s-head"><p class="eyebrow">Next</p><h2>Coming up for {H.escape(name)}</h2></div>
  <div class="next">{nxt or '<p class="fine">Group stage complete. Knockout fixtures follow on the main desk page.</p>'}</div>
</section>
<section class="s" id="players">
  <div class="s-head"><p class="eyebrow">Players to watch</p><h2>Who clubs should follow</h2></div>
  <ul class="ptw">{players}</ul>
  <p class="note fine">All players at this tournament are under 18. We follow FIFA's rules on minors, and every conversation runs through the player's family and federation. This page carries only information already in the public domain.</p>
</section>
<section class="s" id="contact">
  <div class="cta-box"><h2>Want the full picture on {H.escape(name)}'s players?</h2>
  <p>We prepare private scout packs on any player in this squad: the moments, the context and a clear recommendation. Message us for a quote.</p>
  <div class="btns" style="margin-top:6px"><a class="btn primary" href="mailto:Advisory@afritechsports.com?subject={subj}">Email Advisory@afritechsports.com</a><a class="btn ghost" href="{WA}" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
  <p style="font-size:.95rem">Phone and WhatsApp: +254 715 551 506</p></div>
</section>
<section class="s" id="others">
  <div class="s-head"><p class="eyebrow">Africa's ten</p><h2>The other nations</h2></div>
  <div class="others">{others}</div>
</section>
</main>
<footer><div class="wrap">Independent coverage by Afritech. Not affiliated with or endorsed by FIFA.<br>Produced by Afritech Sports Technology and Innovation Group Limited · Updated {updated}</div></footer>
</body>
</html>
"""


def build(root, fonts, emblem, flags):
    data = json.loads((root / "src/data/qatar-u17-2026-nations.json").read_text())
    src = (root / "src/qatar-u17-2026.html").read_text()
    head = src[:src.index("</head>") + len("</head>")].replace("{{FONTS}}", fonts).replace("{{FLAGS}}", flags)
    out = {}
    for n in data["nations"]:
        out["qatar-u17-2026/%s/index.html" % n["slug"]] = page(n, data["nations"], head, emblem, data["updated"])
    return out, data
