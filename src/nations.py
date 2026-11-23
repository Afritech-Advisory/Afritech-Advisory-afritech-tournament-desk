"""One page per African nation: results with goal-by-goal match reports (goal times link to FIFA's
official highlights), next fixtures, players to watch and a briefing call to action.
Data: src/data/qatar-u17-2026-nations.json. Styles come from the main desk page so the look stays one system."""
import json, html as H
import scouting
FULL = {}

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
.goals a{font-weight:600;overflow-wrap:anywhere}
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
.kn{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}
.kn div{background:var(--soft);border-radius:8px;padding:10px 12px}
.kn b{display:block;font-family:var(--display);font-size:1.7rem;line-height:1;color:var(--navy)}
@media (prefers-color-scheme:dark){.kn b{color:var(--orange-text)}}
.kn span{font-size:.86rem;color:var(--muted)}
.tl{width:100%;max-width:560px;height:auto;display:block}
.an{display:grid;gap:10px}
.an div{border-top:1px solid var(--line);padding-top:10px}
.an h4{font-family:var(--display);font-size:1.15rem;margin:0 0 4px}
.player{position:relative;aspect-ratio:16/9;background:#000;border-radius:10px;overflow:hidden}
.player iframe,.player>div{position:absolute;inset:0;width:100%;height:100%;border:0}
.player .ph{display:grid;place-items:center;color:#fff;text-align:center;padding:16px;font-size:.95rem;background:linear-gradient(135deg,#0F2442,#1A365D)}
.now{font-family:var(--mono);font-size:.82rem;color:var(--muted);min-height:1.2em}
.clipbtn{font:700 .9rem var(--body);border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:22px;padding:8px 14px;cursor:pointer;white-space:normal;max-width:100%;min-height:44px;text-align:left;overflow-wrap:anywhere}
.goals li>span:last-child,.goals li>div{min-width:0;overflow-wrap:anywhere}
.clipbtn.on{background:var(--orange);color:#1B1206;border-color:var(--orange)}
.playall{font:700 1rem var(--body);background:var(--orange);color:#1B1206;border:0;border-radius:8px;padding:10px 16px;cursor:pointer;justify-self:start}
.gtype{display:inline-block;font:600 .7rem var(--mono);letter-spacing:.06em;text-transform:uppercase;background:var(--soft);border-radius:4px;padding:2px 6px;margin-left:6px;vertical-align:1px}
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


def vid_id(url):
    return url.split("v=")[1].split("&")[0]


def minute_num(m):
    m = m.strip("'")
    if "+" in m:
        a, b = m.split("+"); return int(a) + int(b) * 0.5
    return int(m)


def timeline(m, nation):
    """Goal timeline 0-90: the nation's goals above the line, the opponent's below."""
    W, X0, X1 = 360, 16, 344
    x = lambda mn: X0 + (X1 - X0) * min(mn, 94) / 94
    parts = [f'<line x1="{X0}" y1="50" x2="{X1}" y2="50" stroke="var(--line)" stroke-width="3"/>',
             f'<line x1="{x(45)}" y1="38" x2="{x(45)}" y2="62" stroke="var(--muted)" stroke-dasharray="3 3"/>',
             f'<text x="{x(45)}" y="96" text-anchor="middle" font-size="11" fill="var(--muted)" font-family="IBM Plex Mono,monospace">HT</text>']
    for t in (0, 90):
        parts.append(f'<text x="{x(t)}" y="96" text-anchor="middle" font-size="12" fill="var(--muted)" font-family="IBM Plex Mono,monospace">{t}\'</text>')
    last = {True: -99, False: -99}
    lift = {True: 0, False: 0}
    for g in m.get("goals", []):
        mine = g["team"] == nation
        cx, cy = x(minute_num(g["min"])), (30 if mine else 70)
        lift[mine] = (lift[mine] + 1) % 2 if cx - last[mine] < 22 else 0
        last[mine] = cx
        col = "var(--teal)" if mine else "var(--rose)"
        parts.append(f'<line x1="{cx}" y1="50" x2="{cx}" y2="{cy}" stroke="{col}" stroke-width="2"/>'
                     f'<circle cx="{cx}" cy="{cy}" r="7" fill="{col}"/>'
                     f'<text x="{cx}" y="{(cy - 14 - 12 * lift[mine]) if mine else (cy + 24 + 12 * lift[mine])}" text-anchor="middle" font-size="11" font-weight="700" fill="{col}" font-family="IBM Plex Mono,monospace">{g["min"]}</text>')
    label = H.escape(f'Goal timeline: {nation} goals above the line, opponent goals below')
    return f'<svg class="tl" viewBox="0 -12 {W} 128" role="img" aria-label="{label}">{"".join(parts)}</svg>'


def match_report(m, nation):
    o = outcome(m, nation)
    word = {"W": "Win", "L": "Defeat", "D": "Draw"}[o]
    mid = m["id"]
    clips = [g for g in m.get("goals", []) if g.get("s") is not None]
    goals = []
    for i, g in enumerate(m.get("goals", [])):
        btn = ""
        if g.get("s") is not None:
            btn = (f' <button class="clipbtn" type="button" data-m="{mid}" data-i="{clips.index(g)}">&#9654; Watch the goal</button>')
        how = f'<br>{H.escape(g["how"])}.' if g.get("how") else ""
        typ = f'<span class="gtype">{H.escape(g["type"])}</span>' if g.get("type") else ""
        goals.append(f'<li><span class="m">{g["min"]}</span><span><b>{H.escape(g["who"])}</b> <span class="tm">({H.escape(g["team"])})</span>{typ}{how}{btn}</span></li>')
    kn = "".join(f'<div><b>{H.escape(a)}</b><span>{H.escape(b)}</span></div>' for a, b in m.get("keyNumbers", []))
    an = "".join(f'<div><h4>{H.escape(x["h"])}</h4><p>{H.escape(x["p"])}</p></div>' for x in m.get("analysis", []))
    vid = vid_id(m["video"]) if m.get("video") else ""
    cl = json.dumps([{"s": g["s"], "e": g["e"], "l": f'{g["min"]} {g["who"]}', "st": scouting.stills(g)} for g in clips])
    lab = f"Play all {len(clips)} goals" if len(clips) > 1 else "Play the goal"
    if clips:
        player = (f'<div class="player" id="pl-{mid}" data-v="{vid}" data-mt="{H.escape(scouting.match_title(m))}" data-clips=\'{H.escape(cl)}\'><div class="ph"><p>{lab}: each goal plays as its own clip, stops, and moves to the next.</p></div></div>'
                  f'<button class="playall" type="button" data-m="{mid}">&#9654; {lab}</button><p class="now" id="now-{mid}" aria-live="polite"></p>')
    elif vid:
        player = (f'<div class="player" id="pl-{mid}" data-v="{vid}" data-clips="[]"><div class="ph"><p>Official FIFA highlights. Goal-by-goal clips follow once each goal is checked on video.</p></div></div>'
                  f'<button class="playall" type="button" data-m="{mid}">&#9654; Play the official highlights</button><p class="now" id="now-{mid}" aria-live="polite"></p>')
    else:
        player = ""
    return (f'<article class="mr" id="{mid}"><p class="when">{m["date"]} · {m["time"]} Doha · {H.escape(m["venue"])}</p>'
            f'<span class="res {o}">{word}</span>'
            f'<div class="sc"><span class="r">{team(m["home"], nation)}</span><b>{m["score"]}</b><span>{team(m["away"], nation)}</span></div>'
            f'<p>{H.escape(m["story"])}</p>'
            f'{f"<div class=kn>{kn}</div>" if kn else ""}'
            f'<h3>The goals</h3>{player}{timeline(m, nation)}<ul class="goals">{"".join(goals)}</ul>'
            f'{f"<h3>Our analysis</h3><div class=an>{an}</div>" if an else ""}'
            f'<p class="scout"><b>For clubs</b>{H.escape(m["scout"])}</p>'
            + (f'<p class="fine" style="margin:0">Clips play from FIFA\'s official highlights on YouTube.</p>' if m.get("video") else '<p class="fine" style="margin:0">Goal clips are added once FIFA\'s official highlights are checked on video.</p>') + '</article>')


def page(n, all_nations, head, emblem, updated, scout=None):
    name = n["name"]
    played = [m for m in n["matches"] if m.get("score")]
    upcoming = [m for m in n["matches"] if not m.get("score")]
    if played:
        rec = [outcome(m, name) for m in played]
        summary = (f'{len(played)} played: {rec.count("W")} won, {rec.count("D")} drawn, {rec.count("L")} lost. '
                   f'Watch every goal as its own clip, then read our analysis of what each match tells clubs, agents and federations.')
    else:
        f = upcoming[0]
        summary = (f'First match: {f["home"]} v {f["away"]}, {f["date"]}, {f["time"]} Doha time. '
                   f'The match report, goals and our read go up here after the final whistle.')
    reports = "".join(match_report(m, name) for m in played) or \
        '<p class="fine">No match played yet. The report goes up here after the final whistle, with every goal and our read.</p>'
    nxt = "".join(f'<div class="fxd"><b>{team(m["home"], name)} v {team(m["away"], name)}</b>'
                  f'<span class="num">{m["time"]} Doha</span><span>{m["date"]} · {H.escape(m["venue"])}</span></div>' for m in upcoming)
    sc = scout or {"players": []}
    ND = FULL
    mine = [p for p in sc["players"] if p.get("nation") == n["slug"]]
    mine.sort(key=lambda p: -sum(len(x) for x in scouting.numbers(p["id"], ND)))
    cards = "".join(scouting.card(p, ND, n["slug"]) for p in mine) or \
        f'<p class="fine">Our scout cards for {H.escape(name)} are built from the group matches: every goal scorer and standout is added here after each matchday.</p>'
    peer = scouting.peer_svg(ND, sc, n["slug"]) or '<p class="fine">The comparison fills in after the first matchday.</p>'
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
    h = h.replace(BASE + '"', url + '"').replace("</style>", EXTRA_CSS + scouting.CSS + "</style>", 1)
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
    <h1>{flag(n["flag"], name)}{H.escape(name)}: match by match.</h1>
    <p class="lead">{summary}</p>
    <div class="btns"><a class="btn primary" href="mailto:Advisory@afritechsports.com?subject={subj}">Book a briefing on {H.escape(name)}</a><a class="btn ghost" href="#results">See the results</a></div>
    <div class="chips"><span>Coach: {H.escape(n["coach"])}</span><span>{H.escape(n["route"])}</span></div>
  </div>
</div></section>
<main class="wrap">
<section class="s" id="results">
  <div class="s-head"><p class="eyebrow">Match reports</p><h2>Results and goals</h2>
  <p>Final scores, every goal as its own clip from FIFA's official highlights, and our analysis of what the match tells clubs, agents and federations.</p></div>
  {reports}
</section>
<section class="s" id="next">
  <div class="s-head"><p class="eyebrow">Next</p><h2>Coming up for {H.escape(name)}</h2></div>
  <div class="next">{nxt or '<p class="fine">Group stage complete. Knockout fixtures follow on the main desk page.</p>'}</div>
</section>
<section class="s" id="players">
  <div class="s-head"><p class="eyebrow">Scout cards</p><h2>Who clubs should follow</h2>
  <p>Every {H.escape(name)} player with a goal or assist, plus the players we tracked before the tournament. Each card carries our recommendation, his numbers so far, his goals as clips and what would move him up or down.</p></div>
  <div class="scards">{cards}</div>
  <h3 style="margin-top:22px">How they compare across Africa's ten</h3>
  {peer}
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
{scouting.YT_LOADER}
<script>
(function(){{
var state={{}};
function mark(m,i){{document.querySelectorAll('.clipbtn[data-m="'+m+'"]').forEach(function(b){{b.classList.toggle('on',+b.getAttribute('data-i')===i)}})}}
function play(m,i){{var el=document.getElementById('pl-'+m),clips=JSON.parse(el.getAttribute('data-clips')),v=el.getAttribute('data-v'),st=state[m];
 var now=document.getElementById('now-'+m),c=clips[i];st.i=i;
 if(!c){{now.textContent='Official highlights';mark(m,-1);window.afClip(el,{{v:v,s:0,e:0}});return}}
 now.textContent='Now playing: '+c.l+(st.all?' ('+(i+1)+' of '+clips.length+')':'');mark(m,i);
 var last=i+1>=clips.length;
 window.afClip(el,{{v:v,s:c.s,e:c.e,fb:{{m:el.getAttribute('data-mt'),g:c.l,st:c.st||[]}},
  next:last?null:function(){{st.all=false;play(m,i+1)}},
  onEnd:function(){{if(st.all&&!last){{setTimeout(function(){{if(st.all&&st.i===i)play(m,i+1)}},1200)}}
   else{{st.all=false;mark(m,-1);now.textContent=clips.length>1?'Clip finished. Press Play all or pick another goal.':'Clip finished.'}}}}}})}}
document.querySelectorAll('.playall').forEach(function(b){{b.addEventListener('click',function(){{var m=b.getAttribute('data-m');state[m]=state[m]||{{}};state[m].all=true;play(m,0)}})}});
document.querySelectorAll('button.clipbtn[data-m]').forEach(function(b){{b.addEventListener('click',function(){{var m=b.getAttribute('data-m');state[m]=state[m]||{{}};state[m].all=false;
 document.getElementById('pl-'+m).scrollIntoView({{behavior:'smooth',block:'center'}});play(m,+b.getAttribute('data-i'))}})}});
}})();
</script>
{scouting.CARD_JS}
</body>
</html>
"""


def build(root, fonts, emblem, flags):
    global FULL
    data, scout = scouting.load(root)
    FULL = data
    src = (root / "src/qatar-u17-2026.html").read_text()
    head = src[:src.index("</head>") + len("</head>")].replace("{{FONTS}}", fonts).replace("{{FLAGS}}", flags)
    out = {}
    for n in data["nations"]:
        out["qatar-u17-2026/%s/index.html" % n["slug"]] = page(n, data["nations"], head, emblem, data["updated"], scout)
    return out, data
