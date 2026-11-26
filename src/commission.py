"""The "Commission a tournament desk" offer page (/commission/).

Four Sentences: who (organisers, federations, leagues, academies and confederations running youth tournaments),
what they get (a live desk like this one), why believe (this desk is the live proof: its real numbers are computed
here at build time from the same data files), one action (WhatsApp: Book a briefing). No prices, no email address
or phone number in plain text, no data files linked, and the method described as outcomes, not as a recipe.
The product is shown with the desk's own components rendered from live data, not stock images."""
import json, html as H
import scouting, nations, radar

DESK = "https://afritech-advisory.github.io/Afritech-Advisory-afritech-tournament-desk/"
URL = DESK + "commission/"
WA = "https://wa.me/qr/JU7PO5B5ADCOI1"
TITLE = "Commission a tournament desk for your youth tournament | Afritech Sports"
DESC = ("A live tournament desk for organisers, federations, leagues and academies: every result, goal clips, match reports "
        "with decision lines, scout cards, animated radars, in four languages, updated every matchday.")

CSS = """
.proof{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.proof div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;display:grid;gap:2px}
.proof b{font-family:var(--display);font-size:2.4rem;line-height:1;color:var(--teal)}
.proof span{color:var(--muted);font-size:.92rem}
.gets{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.gets div{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--teal);border-radius:12px;padding:14px 16px;display:grid;gap:4px;align-content:start}
.gets h3{font-size:1.2rem;margin:0}.gets p{margin:0;color:var(--muted)}
.who{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.who div{border-left:4px solid var(--orange);background:var(--card);border-radius:0 10px 10px 0;padding:12px 14px}
.who b{display:block;font-family:var(--display);font-size:1.15rem}.who p{margin:2px 0 0;color:var(--muted);font-size:.95rem}
.shots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;align-items:start}
.shot{display:grid;gap:8px;min-width:0;margin:0}
.shot .frame{border:1px solid var(--line);border-radius:14px;padding:10px;background:var(--soft);box-shadow:0 10px 30px rgba(15,36,66,.12);pointer-events:none;user-select:none}
.shot .frame>*{margin:0}
.shot figcaption{font-size:.95rem;color:var(--muted)}
.shot figcaption b{color:var(--fg)}
.wide{grid-column:1/-1}
.rdemo{--ring:var(--soft);background:var(--card);border:1px solid var(--line);border-top:5px solid var(--teal);border-radius:12px;padding:16px;display:grid;gap:10px}
.rdemo header{display:flex;gap:12px;align-items:center}.rdemo h3{font-size:1.45rem;line-height:1.1;margin:0}.rdemo .meta{color:var(--muted);font-size:.92rem;margin:0}
.rdemo svg{width:100%;height:auto;display:block;overflow:visible}.rdemo .read{font-weight:600;margin:0}.rdemo .tips{display:none}
.rdemo .fl{display:inline-block;width:36px;height:27px;border-radius:3px;background-size:cover;background-position:center;flex:none}
.offer{background:var(--navy);color:var(--on-navy);border-radius:14px;padding:22px;display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;margin-top:26px}
.offer p{margin:0;max-width:60ch;color:#DCE5F0}.offer b{display:block;font-family:var(--display);font-size:1.5rem;color:#fff}
.steps{counter-reset:s;display:grid;gap:10px;padding:0;list-style:none}
.steps li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px 12px 52px;position:relative}
.steps li::before{content:counter(s);position:absolute;left:14px;top:12px;width:26px;height:26px;border-radius:50%;background:var(--teal);color:#fff;font:700 .9rem var(--body);display:grid;place-items:center}
@media (max-width:760px){.shots{grid-template-columns:minmax(0,1fr)}}
@media (max-width:520px){.proof b{font-size:2rem}}
"""


def numbers(root, nd, sd):
    matches = {m["id"] for m in scouting._uniq(nd)}
    african = {m["id"] for n in nd["nations"] for m in n["matches"] if m.get("score")}
    clips = sum(1 for n in nd["nations"] for m in n["matches"] if m.get("score") for g in m.get("goals", []) + m.get("moments", []) if g.get("s") is not None)
    involved = sum(1 for p in sd["players"] if any(scouting.numbers(p["id"], nd)))
    return [(len(matches), "matches reported with final scores"), (len(african), "African match reports with decision lines"),
            (len(sd["players"]), "scout cards on the board"), (involved, "player radars drawn from match reports"),
            (clips, "goals and key moments checked on video"), (4, "languages on every page")]


def jsonld():
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "Afritech Sports Technology and Innovation Group Limited",
           "alternateName": "Afritech Sports", "url": "https://afritechsports.github.io/",
           "sameAs": ["https://www.linkedin.com/company/afritech-sports-technology-and-innovation-group-limited/"]}
    svc = {"@context": "https://schema.org", "@type": "Service", "name": "Afritech Tournament Desk", "serviceType": "Youth football tournament coverage and scouting desk",
           "provider": {"@type": "Organization", "name": "Afritech Sports Technology and Innovation Group Limited"},
           "areaServed": "Worldwide", "audience": {"@type": "Audience", "audienceType": "Tournament organisers, federations, leagues, academies and confederations"},
           "description": DESC, "url": URL, "availableLanguage": ["en", "fr", "sw", "pt-BR"]}
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (org, svc))


def build(root, fonts, emblem, flags):
    nd, sd = scouting.load(root)
    src = (root / "src/qatar-u17-2026.html").read_text()
    head = src[:src.index("</head>") + len("</head>")].replace("{{FONTS}}", fonts).replace("{{FLAGS}}", flags)
    import re
    head = re.sub(r"<title>.*?</title>", f"<title>{H.escape(TITLE)}</title>", head, 1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{H.escape(DESC)}">', head, 1)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{H.escape("Commission a tournament desk | Afritech Sports")}">', head, 1)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{H.escape(DESC)}">', head, 1)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{URL}">', head, 1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{URL}">', head, 1)
    head = re.sub(r'<meta name="twitter:title" content="[^"]*">', "", head)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*">', "", head)
    head = head.replace("</style>", nations.EXTRA_CSS + scouting.CSS + CSS + "</style>", 1).replace("</head>", jsonld() + "</head>", 1)

    nums = "".join(f'<div><b>{n}</b><span>{H.escape(l)}</span></div>' for n, l in numbers(root, nd, sd))
    # the desk's own components, rendered from the live data
    nations.FULL = nd
    ps = [p for p in scouting.ranked(sd["players"], nd) if p.get("nation")]
    star = ps[0]
    card = scouting.card(star, nd, here_slug="__demo__")
    rows = radar.player_rows(nd, sd)
    bavg = radar.avg(rows)
    r0 = next(r for r in rows if r["p"]["id"] == star["id"])
    rd = (f'<div class="rdemo"><header>{radar.flag(r0["t"])}<div><h3>{H.escape(star["name"])}</h3><p class="meta">{H.escape(r0["t"]["name"])}</p></div></header>'
          + radar.radar_svg(radar.P_AXES, r0["v"], bavg, "Tournament radar of six areas against the comparison average")
          + f'<p class="read">{H.escape(radar.read_player(r0["v"], bavg))}</p></div>')
    show = None
    for n in nd["nations"]:
        for m in n["matches"]:
            if m.get("id") == "mli-bel" and m.get("decisions"):
                show = (m, n["name"])
    if show is None:
        show = next((m, n["name"]) for n in nd["nations"] for m in n["matches"] if m.get("decisions"))
    rep = nations.match_report(*show)
    rep = re.sub(r'<div class="player".*?</div></div>', "", rep, 1, flags=re.S)  # no live player inside the picture
    rep = re.sub(r'<p class="now"[^>]*></p>', "", rep)
    rep = re.sub(r'<button[^>]*>.*?</button>', "", rep, flags=re.S)
    rep = rep.replace(f'id="{show[0]["id"]}"', "")
    card = re.sub(r'\sid="[^"]*"', "", card, 1)
    card = re.sub(r'<button[^>]*>(.*?)</button>', r'<span class="clipbtn">\1</span>', card, flags=re.S)
    card = re.sub(r'<a [^>]*>(.*?)</a>', r'<span>\1</span>', card, flags=re.S)
    rep = re.sub(r'<a [^>]*>(.*?)</a>', r'<span>\1</span>', rep, flags=re.S)

    body = f"""
<body>
<header class="bar"><div class="wrap">
  <a class="brand" href="../"><img src="{emblem}" alt="Afritech Sports emblem" width="36" height="39">Tournament Desk</a>
  <nav aria-label="Sections"><a href="#get">What you get</a><a href="#see">See it</a><a href="#who">Who it is for</a><a href="../qatar-u17-2026/">Live desk</a><a class="cta" href="{WA}" target="_blank" rel="noopener">Book a briefing</a></nav>
</div></header>

<section class="hero" id="top"><div class="wrap">
  <div>
    <p class="eyebrow">For tournament organisers, federations, leagues, academies and confederations</p>
    <h1>Commission a tournament desk. <em>Every player seen, every match read.</em></h1>
    <p class="lead">Running a youth tournament? We cover it live: every result, goal clips, match reports with decision lines, scout cards on every standout and animated radars, in four languages, updated every matchday. Your players get seen by the clubs, scouts and federations who decide their next step.</p>
    <p style="display:flex;flex-wrap:wrap;gap:10px;margin-top:18px"><a class="btn primary" href="{WA}" target="_blank" rel="noopener">Book a briefing on WhatsApp</a><a class="btn ghost" href="../qatar-u17-2026/">See the live desk</a></p>
  </div>
  <div class="proof" aria-label="This desk today">{nums}</div>
</div></section>

<main class="wrap">
<section class="s" id="proof"><div class="s-head"><p class="eyebrow">The live proof</p><h2>This desk, at the FIFA U-17 World Cup Qatar 2026</h2>
<p>The numbers above are counted from this desk when the page is built, the same way your desk would be. Youth tournaments rarely give their players coverage like this. Your tournament can.</p></div></section>

<section class="s" id="get"><div class="s-head"><p class="eyebrow">What you get</p><h2>A live desk for your tournament</h2></div>
<div class="gets">
  <div><h3>Every result, every matchday</h3><p>Final scores, scorers and the numbers that tell each match, for every team in the tournament.</p></div>
  <div><h3>Goal clips that stay on your desk</h3><p>Each goal plays as its own clip from the official video, then stops. Readers stay with your tournament.</p></div>
  <div><h3>Match reports that lead to a decision</h3><p>Every report ends with three lines: for scouts, for coaches and for technical directors.</p></div>
  <div><h3>A scout card on every standout</h3><p>Every scorer, creator and decisive performer gets a card with his numbers, his clips and what would move him up or down.</p></div>
  <div><h3>Animated radars</h3><p>Player and team radars computed from the match reports, so a club sees in one picture where a player stands.</p></div>
  <div><h3>Four languages, rules for minors built in</h3><p>English, French, Kiswahili and Brazilian Portuguese on every page. Under-18 rules on every card: no valuations, no transfer talk.</p></div>
</div></section>

<section class="s" id="see"><div class="s-head"><p class="eyebrow">See it</p><h2>What your readers will see</h2><p>Three parts of this desk, exactly as they appear on it today.</p></div>
<div class="shots">
  <figure class="shot"><div class="frame" inert aria-hidden="true">{card}</div><figcaption><b>Scout card.</b> Every standout, with his numbers, his clips, a Tournament read and what moves him up or down.</figcaption></figure>
  <figure class="shot"><div class="frame" inert aria-hidden="true">{rd}</div><figcaption><b>Player radar.</b> Six areas from the match reports, against the rest of the tournament. On the desk it draws itself as you scroll.</figcaption></figure>
  <figure class="shot wide"><div class="frame" inert aria-hidden="true">{rep}</div><figcaption><b>Match report.</b> The goals, the numbers, our analysis and three decision lines for scouts, coaches and technical directors.</figcaption></figure>
</div></section>

<section class="s" id="how"><div class="s-head"><p class="eyebrow">How it runs</p><h2>What happens on a matchday</h2></div>
<ol class="steps">
  <li>After the final whistle: the result and the scorers, final scores only.</li>
  <li>After every matchday: match reports with decision lines, new and updated scout cards, redrawn radars.</li>
  <li>Every goal checked on the official video before its clip goes live.</li>
  <li>All of it in four languages, and nothing provisional published.</li>
</ol></section>

<section class="s" id="who"><div class="s-head"><p class="eyebrow">Who it is for</p><h2>Built for the people who run youth football</h2></div>
<div class="who">
  <div><b>Tournament organisers</b><p>A tournament that clubs and scouts follow, and a record that brings teams back next year.</p></div>
  <div><b>Federations</b><p>Your players seen by clubs abroad, with the evidence on one page.</p></div>
  <div><b>Leagues</b><p>Every standout in your youth competition on a card a club can act on.</p></div>
  <div><b>Academies</b><p>A public record of every player you developed, match by match.</p></div>
  <div><b>Confederations</b><p>One desk for every nation in your competition, in the languages your members read.</p></div>
</div>
<div class="offer"><div><b>Message us for a quote</b><p>Tell us the tournament, the dates and the number of teams. We reply with what your desk would cover and when it can go live.</p></div><a class="wa" href="{WA}" target="_blank" rel="noopener">Book a briefing on WhatsApp</a></div>
</section>
</main>

<footer><div class="wrap">© Afritech Sports Technology and Innovation Group Limited. The Afritech tournament desk method.<br>Independent coverage by Afritech. Not affiliated with or endorsed by FIFA.<br><a href="../qatar-u17-2026/">See the live desk</a></div></footer>
</body>
</html>"""
    return {"commission/index.html": head + body}
