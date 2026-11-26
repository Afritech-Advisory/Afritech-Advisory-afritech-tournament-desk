"""Animated tournament radars for the public Radars page, computed from the evidence the desk has.

FIFA has not posted full matches from Qatar 2026, so scout grades from full-match viewing cannot be drawn yet
(and the four-area grades stay private until Andrew approves them). These radars use only counts from final
match reports and FIFA's official highlights:
- a player radar for every board player with a goal or assist: six axes, each a percentile 0-10 against all
  board players with a goal or assist, set against the board average or the African players' average;
- a team radar for each of Africa's ten: six axes, each a percentile 0-10 against the other nine.
Nothing on these radars is typed by hand: change a match report and every radar redraws in the next build."""
import html, json, math, re
import scouting

E = html.escape
SET_PIECE = ("Penalty", "Free kick", "Corner", "Set piece")

P_AXES = [  # (label, unit for the raw value, how the matches behind it are chosen)
    ("Output", "goals and assists per team match"),
    ("Finishing share", "of his team's goals"),
    ("Creation", "assists per team match"),
    ("Decisive goals", "goals that levelled or put his team ahead"),
    ("Opposition quality", "involvements v sides with a win"),
    ("Late impact", "involvements from the 75th minute"),
]
T_AXES = [
    ("Goals for", "goals scored per match"),
    ("Goals against", "goals conceded per match (fewer scores higher)"),
    ("Set pieces", "of goals from penalties and set pieces"),
    ("Late goals", "goals in the last 15 minutes"),
    ("Points from behind", "points won after falling behind"),
    ("Clean sheets", "matches without conceding"),
]


def minute(g):
    m = re.match(r"(\d+)(?:\+(\d+))?", g.get("min", "0"))
    return int(m[1]) if m else 0


def pct(values, v, high_good=True):
    """Percentile 0-10: the share of the group he matches or beats; 0 when there is nothing to count."""
    if high_good and v <= 0:
        return 0.0
    n = len(values)
    beat = sum(1 for x in values if (x <= v if high_good else x >= v))
    return round(10 * beat / n, 1)


def opp(m, name):
    return m["away"] if m["home"] == name else m["home"]


def fmt(x, unit):
    if unit.startswith("of "):
        return f"{round(100 * x)}%"
    if "per" in unit:
        return f"{x:.2f}"
    return str(int(x))


def inv_label(r, kind, name):
    return f'{kind} v {opp(r["m"], name)}, {r["g"]["min"]}'


# ---------- players ----------

def player_rows(nd, sd):
    wins = scouting.wins_by_team(nd)
    rows = []
    for p in scouting.ranked(sd["players"], nd):
        goals, assists = scouting.numbers(p["id"], nd)
        if not goals and not assists:
            continue
        t = scouting.team(p, nd)
        tm = len({m["id"] for m in scouting._uniq(nd) if t["name"] in (m["home"], m["away"])}) or 1
        tg = scouting.team_goals(t, nd) or 1
        inv = [(r, "Goal") for r in goals] + [(r, "Assist") for r in assists]
        dec = [(r, "Goal") for r in goals if scouting.complete(r["m"]) and scouting.decisive(r["m"], r["g"])]
        vw = [(r, k) for r, k in inv if wins.get(opp(r["m"], t["name"]), 0) > 0]
        late = [(r, k) for r, k in inv if minute(r["g"]) >= 75]
        raw = [len(inv) / tm, len(goals) / tg, len(assists) / tm, len(dec), len(vw), len(late)]
        behind = [inv, [(r, "Goal") for r in goals], [(r, "Assist") for r in assists], dec, vw, late]
        rows.append({"p": p, "t": t, "raw": raw, "behind": [[inv_label(r, k, t["name"]) for r, k in b] for b in behind], "tm": tm})
    for i in range(len(P_AXES)):
        col = [r["raw"][i] for r in rows]
        for r in rows:
            r.setdefault("v", []).append(pct(col, r["raw"][i]))
    return rows


def avg(rows):
    if not rows:
        return [0] * len(P_AXES)
    return [round(sum(r["v"][i] for r in rows) / len(rows), 1) for i in range(len(rows[0]["v"]))]


# ---------- teams ----------

def team_rows(nd):
    rows = []
    for n in nd["nations"]:
        ms = [m for m in n["matches"] if m.get("score")]
        if not ms:
            continue
        name = n["name"]
        gf = ga = late = sp = cs = pts_back = 0
        late_l, sp_l, cs_l, back_l, gf_l, ga_l = [], [], [], [], [], []
        for m in ms:
            a, b = scouting._sc(m)
            f, c = (a, b) if m["home"] == name else (b, a)
            gf += f; ga += c
            lab = f'v {opp(m, name)}'
            gf_l.append((lab, m["score"])); ga_l.append((lab, m["score"]))
            if c == 0:
                cs += 1; cs_l.append((lab, m["score"]))
            for g in m.get("goals", []):
                if g["team"] != name:
                    continue
                if minute(g) >= 76:
                    late += 1; late_l.append((lab, g["min"]))
                how = (g.get("how") or "").lower()
                if g.get("type") in SET_PIECE or "corner" in how or "free kick" in how or "penalty" in how:
                    sp += 1; sp_l.append((lab, g["min"]))
            if scouting.complete(m):
                tally, trailed = {name: 0, "o": 0}, False
                for g in m["goals"]:
                    tally[name if g["team"] == name else "o"] += 1
                    if tally["o"] > tally[name]:
                        trailed = True
                if trailed and f >= c:
                    pts = 3 if f > c else 1
                    pts_back += pts; back_l.append((lab, m["score"]))
        k = len(ms)
        raw = [gf / k, ga / k, (sp / gf) if gf else 0, late, pts_back, cs]
        rows.append({"n": n, "raw": raw, "k": k, "behind": [gf_l, ga_l, sp_l, late_l, back_l, cs_l]})
    for i in range(len(T_AXES)):
        col = [r["raw"][i] for r in rows]
        for r in rows:
            r.setdefault("v", []).append(pct(col, r["raw"][i], high_good=(i != 1)))
    return rows


# ---------- drawing ----------

W, HH, CX, CY, R = 760, 420, 380, 205, 125


def pt(i, v, n=6):
    a = -math.pi / 2 + i * 2 * math.pi / n
    return CX + math.cos(a) * R * v / 10, CY + math.sin(a) * R * v / 10


def poly(vals):
    return " ".join("%.1f,%.1f" % pt(i, v) for i, v in enumerate(vals))


def _wrap(label):
    w = label.split()
    if len(w) == 1:
        return [label]
    best = min(range(1, len(w)), key=lambda i: abs(len(" ".join(w[:i])) - len(" ".join(w[i:]))))
    return [" ".join(w[:best]), " ".join(w[best:])]


def radar_svg(axes, vals, cmp_vals, title, alt=None):
    o = [f'<svg class="rd" viewBox="0 0 {W} {HH}" role="img" aria-label="{E(title)}">']
    for lvl in (2, 4, 6, 8, 10):
        o.append(f'<polygon points="{poly([lvl] * 6)}" fill="{"var(--ring)" if lvl == 10 else "none"}" stroke="var(--line)" stroke-width="1"/>')
    for i in range(6):
        x, y = pt(i, 10)
        o.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="var(--line)" stroke-width="1"/>')
    data_alt = f' data-alt="{",".join(map(str, alt))}"' if alt else ""
    o.append(f'<polygon class="ra" data-v="{",".join(map(str, cmp_vals))}" data-b="{",".join(map(str, cmp_vals))}"{data_alt} points="{poly(cmp_vals)}" fill="none" stroke="var(--orange)" stroke-width="2.5" stroke-dasharray="7 5" stroke-linejoin="round"/>')
    o.append(f'<polygon class="rp" data-v="{",".join(map(str, vals))}" points="{poly(vals)}" fill="var(--teal)" fill-opacity=".28" stroke="var(--teal)" stroke-width="3" stroke-linejoin="round"/>')
    for i, v in enumerate(vals):
        x, y = pt(i, v)
        o.append(f'<circle class="rdot" data-i="{i}" cx="{x:.1f}" cy="{y:.1f}" r="5" fill="var(--teal)" stroke="var(--card)" stroke-width="2"/>')
    for i, (a, _) in enumerate(axes):
        x, y = pt(i, 12.4)
        c = math.cos(-math.pi / 2 + i * 2 * math.pi / 6)
        anchor = "middle" if abs(c) < 0.3 else ("start" if c > 0 else "end")
        yy = y + 6 + (-16 if i == 0 else (8 if i == 3 else 0))
        o.append(f'<g class="ax" data-i="{i}" tabindex="0" role="button" aria-label="{E(a)}">')
        hx, hy = pt(i, 11.2)
        o.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="30" fill="transparent"/>')
        o.append(f'<text x="{x:.1f}" y="{yy:.1f}" text-anchor="{anchor}" font-size="20" font-family="Source Sans 3,Segoe UI,sans-serif" fill="var(--fg)">{E(a)}</text>')
        o.append(f'<text x="{x:.1f}" y="{yy + 24:.1f}" text-anchor="{anchor}" font-size="23" font-weight="700" font-family="Barlow Condensed,sans-serif" fill="var(--teal)" class="rv" data-v="{vals[i]}">{vals[i]:.1f}</text>')
        o.append("</g>")
    o.append("</svg>")
    return "".join(o)


def tips(axes, vals, raws, behind, pair=False):
    """One panel per axis (shown on hover or tap): value, raw count and the matches behind it."""
    out = []
    for i, (a, unit) in enumerate(axes):
        items = ("".join(f'<li><span>{E(x)}</span> <span>{E(y)}</span></li>' for x, y in behind[i]) if pair
                 else "".join(f'<li>{E(x)}</li>' for x in behind[i]))
        out.append(f'<div class="tip" data-i="{i}" hidden><p><b>{E(a)}</b> <span class="tv">{vals[i]:.1f}</span></p>'
                   f'<p class="tr"><b>{fmt(raws[i], unit)}</b> <span>{E(unit)}</span></p>'
                   + (f'<ul>{items}</ul>' if items else '<p class="tn">No match yet.</p>') + '</div>')
    return '<div class="tips"><p class="thint">Tap or hover an axis to see the matches behind it.</p>' + "".join(out) + "</div>"


def flag(t):
    return f'<i class="fl fl-{E(t["flag"])}" role="img" aria-label="{E(t["name"])} flag"></i>' if t.get("flag") else f'<span class="ccode">{E(t["code"])}</span>'


def read_player(v, b):
    best = max(range(6), key=lambda i: (v[i] - b[i], v[i]))
    return P_READ[best] if v[best] > b[best] else "Below the board average on every axis so far: one more match changes this picture."


P_READ = [
    "Above the board in output: he is involved in his team's goals more often than most.",
    "Above the board in finishing share: his team depends on his goals.",
    "Above the board in creation: he makes goals for others, not only scores them.",
    "Above the board in decisive goals: he scores when the match is still open.",
    "Above the board against strong opposition: his numbers came against sides that win.",
    "Above the board late in matches: he is still decisive after the 75th minute.",
]


def player_card(r, bavg, aavg):
    p, t = r["p"], r["t"]
    title = "Tournament radar of six areas against the comparison average"
    region = "africa" if p.get("nation") else "world"
    link = f'<a href="../{t["slug"]}/">{E(t["name"])}: match reports and all scout cards &rsaquo;</a>' if t.get("slug") else ""
    return (f'<article class="rc" data-k="p" data-region="{region}">'
            f'<header>{flag(t)}<div><h3>{E(p["name"])}</h3><p class="meta">{E(t["name"])}{(" · " + E(p["role"])) if p.get("role") else ""}</p></div></header>'
            + radar_svg(P_AXES, r["v"], bavg, title, aavg)
            + tips(P_AXES, r["v"], r["raw"], r["behind"])
            + f'<p class="read">{E(read_player(r["v"], bavg))}</p>'
            + (f'<p class="fine">{link}</p>' if link else "") + '</article>')


T_READ = [
    "Scores more per match than most of Africa's ten.",
    "Concedes less per match than most of Africa's ten.",
    "Gets more of its goals from penalties and set pieces than most.",
    "Scores late: more goals in the last 15 minutes than most.",
    "Wins points back after falling behind.",
    "Keeps clean sheets more often than most.",
]


def team_card(r, tavg):
    n = r["n"]
    v = r["v"]
    best = max(range(6), key=lambda i: (v[i] - tavg[i], v[i]))
    read = T_READ[best]
    title = "Team radar of six areas against the average of Africa's ten"
    return (f'<article class="rc" data-k="t">'
            f'<header><i class="fl fl-{E(n["flag"])}" role="img" aria-label="{E(n["name"])} flag"></i><div><h3>{E(n["name"])}</h3><p class="meta">Group {n["group"]}</p></div></header>'
            + radar_svg(T_AXES, v, tavg, title)
            + tips(T_AXES, v, r["raw"], r["behind"], pair=True)
            + f'<p class="read">{E(read)}</p><p class="fine"><a href="../{n["slug"]}/">{E(n["name"])}: match reports and all scout cards &rsaquo;</a></p></article>')


def build_content(root):
    nd, sd = scouting.load(root)
    prow = player_rows(nd, sd)
    bavg = avg(prow)
    aavg = avg([r for r in prow if r["p"].get("nation")])
    trow = team_rows(nd)
    tavg = [round(sum(r["v"][i] for r in trow) / len(trow), 1) for i in range(6)] if trow else [0] * 6
    nmatch = len({m["id"] for m in scouting._uniq(nd)})
    return {
        "{{PCARDS}}": "\n".join(player_card(r, bavg, aavg) for r in prow),
        "{{TCARDS}}": "\n".join(team_card(r, tavg) for r in trow),
        "{{NP}}": str(len(prow)), "{{NA}}": str(sum(1 for r in prow if r["p"].get("nation"))),
        "{{NT}}": str(len(trow)), "{{NM}}": str(nmatch),
        "{{UPDATED}}": E(sd.get("updated", "")),
    }
