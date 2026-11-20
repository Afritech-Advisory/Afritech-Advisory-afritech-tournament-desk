"""Afritech-TSA scout cards for the Tournament Desk (Stage 1, public-domain evidence).

One data record per player (src/data/qatar-u17-2026-scouting.json). Tournament numbers are
computed from the match reports (src/data/qatar-u17-2026-nations.json), never typed by hand,
so a player's card, the nation page and the main board always agree.
Every player is under 18: club signal MONITOR, agent DEVELOP FIRST, no valuation, no
published grades until Andrew approves them in the private tracker."""
import json, html as H

CSS = """
.scard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;display:grid;gap:10px;scroll-margin-top:70px}
.scard header{display:flex;gap:12px;align-items:center}
.scard .sil{width:52px;height:52px;flex:none;border-radius:50%;background:var(--soft);display:grid;place-items:center}
.scard h3{font-size:1.35rem}
.scard .meta{color:var(--muted);font-size:.92rem}
.cap{font:600 .68rem var(--mono);letter-spacing:.06em;background:var(--navy);color:#fff;border-radius:4px;padding:2px 6px;margin-left:6px;vertical-align:2px}
.sig{display:flex;flex-wrap:wrap;gap:6px}
.sig span{font:600 .74rem var(--mono);letter-spacing:.04em;text-transform:uppercase;border-radius:6px;padding:4px 8px;background:var(--soft)}
.sig span b{color:var(--orange-text)}
.nums{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}
.nums div{background:var(--soft);border-radius:8px;padding:8px;text-align:center}
.nums b{display:block;font-family:var(--display);font-size:1.6rem;line-height:1}
.nums span{font-size:.74rem;color:var(--muted)}
.seen{margin:0;padding-left:18px;display:grid;gap:4px;font-size:.96rem}
.ladder2{display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.9rem}
.ladder2 div{border-radius:8px;padding:8px 10px;border:1px solid var(--line)}
.ladder2 .u{border-left:4px solid var(--teal)} .ladder2 .d{border-left:4px solid var(--rose)}
.ladder2 b{display:block;font-family:var(--display);text-transform:uppercase;letter-spacing:.04em;font-size:.85rem}
.gl{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:6px}
.peer{width:100%;height:auto;display:block;max-width:640px}
.scards{display:grid;gap:12px}
@media (max-width:420px){.nums b{font-size:1.35rem}.ladder2{grid-template-columns:1fr}}
"""

SIL = '<svg viewBox="0 0 40 40" width="40" height="40" aria-hidden="true"><circle cx="20" cy="14" r="8" fill="var(--line)"/><path d="M4 38c2-9 9-13 16-13s14 4 16 13z" fill="var(--line)"/></svg>'


def load(root):
    nations = json.loads((root / "src/data/qatar-u17-2026-nations.json").read_text())
    scout = json.loads((root / "src/data/qatar-u17-2026-scouting.json").read_text())
    return nations, scout


def numbers(pid, nations):
    """Goals and assists with match, minute and clip index, computed from the match reports."""
    goals, assists = [], []
    for n in nations["nations"]:
        for m in n["matches"]:
            clips = [g for g in m.get("goals", []) if g.get("s") is not None]
            for g in m.get("goals", []):
                rec = {"m": m, "g": g, "nation": n, "clip": clips.index(g) if g in clips else None}
                if g.get("pid") == pid:
                    goals.append(rec)
                if g.get("apid") == pid:
                    assists.append(rec)
    return goals, assists


def flag_of(slug, nations):
    for n in nations["nations"]:
        if n["slug"] == slug:
            return n
    return None


def card(p, nations, here_slug=None):
    n = flag_of(p["nation"], nations)
    goals, assists = numbers(p["id"], nations)
    clips = sum(1 for r in goals + assists if r["clip"] is not None)
    bits = [x for x in (p.get("role"), p.get("club"), ("No. " + p["shirt"]) if p.get("shirt") else "", ("Age %d" % p["age"]) if p.get("age") else "") if x]
    meta = f'<i class="fl fl-{n["flag"]}" role="img" aria-label="{H.escape(n["name"])} flag"></i> {H.escape(n["name"])} · ' + " · ".join(H.escape(b) for b in bits)
    cap = '<span class="cap">CAPTAIN</span>' if p.get("captain") else ""
    moments = []
    for r, kind in [(x, "Goal") for x in goals] + [(x, "Assist") for x in assists]:
        m, g = r["m"], r["g"]
        opp = m["away"] if m["home"] == n["name"] else m["home"]
        label = f'{kind} v {opp}, {g["min"]}'
        if r["clip"] is not None and here_slug == p["nation"]:
            moments.append(f'<li><button class="clipbtn" type="button" data-m="{m["id"]}" data-i="{r["clip"]}">&#9654; {H.escape(label)}</button></li>')
        else:
            href = f'../{p["nation"]}/#{m["id"]}' if here_slug else f'{p["nation"]}/#{m["id"]}'
            moments.append(f'<li><a class="clipbtn" href="{href}">&#9654; {H.escape(label)}</a></li>')
    played = sum(1 for m in n["matches"] if m.get("score"))
    nums = (f'<div class="nums"><div><b>{len(goals)}</b><span>Goals</span></div><div><b>{len(assists)}</b><span>Assists</span></div>'
            f'<div><b>{played}</b><span>Team matches</span></div><div><b>{clips}</b><span>Clips</span></div></div>')
    seen = "".join(f"<li>{H.escape(f)}</li>" for f in p["facts"])
    return (f'<article class="scard" id="{p["id"]}"><header><div class="sil">{SIL}</div><div><h3>{H.escape(p["name"])}{cap}</h3>'
            f'<p class="meta">{meta}</p></div></header>'
            f'<div class="sig"><span>Club: <b>MONITOR</b></span><span>Agent: <b>DEVELOP FIRST</b></span><span>Federation: <b>{p["fed"]}</b></span></div>'
            f'<p><b>Next:</b> {H.escape(p["next"])}</p>{nums}'
            f'{f"<ul class=gl>{chr(10).join(moments)}</ul>" if moments else ""}'
            f'<h4 style="margin:2px 0 0;font-family:var(--display);font-size:1.1rem">What we have seen</h4><ul class="seen">{seen}</ul>'
            f'<div class="ladder2"><div class="u"><b>Moves him up</b>{H.escape(p["up"])}</div><div class="d"><b>Moves him down</b>{H.escape(p["down"])}</div></div>'
            f'<p class="fine" style="margin:0">Built from match reports, FIFA\'s official highlights and published sources. His full four-area and position profile follows after his group matches.</p></article>')


def peer_svg(nations, scout, highlight_nation=None):
    """Tournament peer comparison: goal involvements of every African player on the board (dot plot, one dot per goal or assist)."""
    rows = []
    for p in scout["players"]:
        g, a = numbers(p["id"], nations)
        if g or a:
            rows.append((len(g) + len(a), len(g), len(a), p))
    rows.sort(key=lambda r: (-r[0], r[3]["name"]))
    if not rows:
        return ""
    W, rh, x0 = 360, 30, 168
    h = 26 + rh * len(rows) + 30
    o = [f'<svg class="peer" viewBox="0 0 {W} {h}" role="img" aria-label="Goal involvements of Africa\'s players at the tournament so far">']
    for k, (tot, g, a, p) in enumerate(rows):
        y = 26 + k * rh
        n = flag_of(p["nation"], nations)
        mine = highlight_nation in (None, p["nation"])
        col = "var(--fg)" if mine else "var(--muted)"
        o.append(f'<text x="0" y="{y + 5}" font-size="12.5" fill="{col}" font-family="Source Sans 3,Segoe UI,sans-serif" font-weight="{700 if highlight_nation == p["nation"] else 400}">{H.escape(p["name"])} ({n["code"]})</text>')
        for i in range(tot):
            c = "var(--teal)" if i < g else "var(--purple)"
            o.append(f'<circle cx="{x0 + 10 + i * 24}" cy="{y}" r="8" fill="{c}" opacity="{1 if mine else .45}"/>')
    ly = h - 8
    o.append(f'<circle cx="6" cy="{ly - 4}" r="6" fill="var(--teal)"/><text x="16" y="{ly}" font-size="12" fill="var(--muted)">Goal</text>'
             f'<circle cx="66" cy="{ly - 4}" r="6" fill="var(--purple)"/><text x="76" y="{ly}" font-size="12" fill="var(--muted)">Assist</text>'
             f'<text x="{W}" y="{ly}" text-anchor="end" font-size="12" fill="var(--muted)">One dot = one goal or assist</text>')
    o.append("</svg>")
    return ("".join(o) + '<p class="fine">How to read: each row is one African player on our board with a goal or assist so far; teal dots are goals, purple dots assists. '
            'Counts from final match reports, all ten African squads, updated after every matchday.</p>')


def board_html(nations, scout):
    """Main desk board: compact cards generated from the same records, newest goal involvement first."""
    out = []
    for p in scout["players"]:
        g, a = numbers(p["id"], nations)
        if not (p.get("board") or g or a):
            continue
        n = flag_of(p["nation"], nations)
        bits = " · ".join(H.escape(b) for b in (p.get("role"), "Captain" if p.get("captain") else "", p.get("club"), ("Age %d" % p["age"]) if p.get("age") else "") if b)
        tally = f"{len(g)} goal{'s' if len(g) != 1 else ''}, {len(a)} assist{'s' if len(a) != 1 else ''} so far" if (g or a) else "First match to come" if not any(m.get("score") for m in n["matches"]) else "No goal involvement yet"
        out.append((-(len(g) + len(a)), p["name"],
            f'<article class="pl"><div class="sil" aria-hidden="true">{SIL}</div><div>'
            f'<h3>{H.escape(p["name"])}</h3><p class="meta"><i class="fl fl-{n["flag"]}" role="img" aria-label="{H.escape(n["name"])} flag"></i>{H.escape(n["name"])}{" · " + bits if bits else ""}</p>'
            f'<p class="why"><b>{tally}.</b> {H.escape(p["facts"][0])}</p>'
            f'<p class="rec"><span class="verdict">MONITOR</span><span class="next">{H.escape(p["next"])} <a href="{p["nation"]}/#{p["id"]}">Scout card &rsaquo;</a></span></p></div></article>'))
    out.sort()
    return "".join(x[2] for x in out)
