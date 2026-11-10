"""Static SVG radars for the public Player radars page.

Each player is drawn against the average of all players Afritech graded in the same
tournament role. Individual peer scores are never published: the data file only
carries approved players and pre-computed role averages.
"""
import html, json, math

ROLES = {
    "gk": ("Goalkeeper", ["Shot stopping", "Handling", "Positioning", "Aerial command", "1v1 ability", "Distribution", "Communication", "Decision-making"]),
    "cb": ("Centre back", ["Defensive positioning", "Aerial ability", "Duels", "Recovery speed", "Reading the game", "Ball progression", "Passing", "Composure"]),
    "fb": ("Full back", ["Defensive 1v1", "Recovery pace", "Positioning", "Crossing", "Ball carrying", "Combination play", "Overlapping runs", "Pressing"]),
    "cm": ("Central midfielder", ["Ball retention", "Press resistance", "Progressive passing", "Ball carrying", "Tactical awareness", "Work rate", "Duels", "Creativity"]),
    "am": ("Attacking midfielder", ["Creativity", "Vision", "Final pass", "Receiving between lines", "Dribbling", "Combination play", "Shooting threat", "Off-ball movement"]),
    "w": ("Winger", ["Acceleration", "1v1 dribbling", "Ball carrying", "Crossing", "Chance creation", "Off-ball movement", "Finishing", "Defensive work rate"]),
    "st": ("Striker", ["Finishing", "Shot quality", "Movement in the box", "Link play", "Hold-up play", "Aerial threat", "1v1 ability", "Pressing from the front"]),
}
MIN_PEERS = 3  # a role average is shown only once this many players are graded in the role
E = html.escape


def _wrap(label):
    words = label.split()
    if len(label) <= 9 or len(words) == 1:
        return [label]
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


def radar_svg(role, scores=None, avg=None, title=""):
    axes = ROLES[role][1]
    W, H, cx, cy, R = 460, 400, 230, 200, 108
    n = len(axes)
    ang = lambda i: -math.pi / 2 + i * 2 * math.pi / n
    pt = lambda i, v: (cx + math.cos(ang(i)) * R * v / 10, cy + math.sin(ang(i)) * R * v / 10)
    poly = lambda vals: " ".join("%.1f,%.1f" % pt(i, v) for i, v in enumerate(vals))
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{E(title)}"><title>{E(title)}</title>']
    for lvl in (2, 4, 6, 8, 10):
        o.append(f'<polygon points="{poly([lvl] * n)}" fill="{"var(--ring)" if lvl == 10 else "none"}" stroke="var(--line)" stroke-width="1"/>')
    o.append(f'<polygon points="{poly([7] * n)}" fill="none" stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 4" opacity=".7"/>')
    for i in range(n):
        x, y = pt(i, 10)
        o.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="var(--line)" stroke-width="1"/>')
    if avg:
        o.append(f'<polygon points="{poly([avg[a] for a in axes])}" fill="none" stroke="var(--orange)" stroke-width="2.5" stroke-dasharray="7 5" stroke-linejoin="round"/>')
    if scores:
        o.append(f'<polygon points="{poly([scores[a] for a in axes])}" fill="var(--teal)" fill-opacity=".28" stroke="var(--teal)" stroke-width="3" stroke-linejoin="round"/>')
        for i, a in enumerate(axes):
            x, y = pt(i, scores[a])
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="var(--teal)" stroke="var(--card)" stroke-width="2"/>')
    for i, a in enumerate(axes):
        x, y = pt(i, 12.3)
        c = math.cos(ang(i))
        anchor = "middle" if abs(c) < 0.3 else ("start" if c > 0 else "end")
        lines = _wrap(a)
        val = f' {scores[a]:.1f}' if scores else ""
        y0 = y - (len(lines) - 1) * 8.5 + 5
        for j, ln in enumerate(lines):
            tail = f'<tspan font-weight="700" fill="var(--teal)">{val}</tspan>' if (scores and j == len(lines) - 1) else ""
            o.append(f'<text x="{x:.1f}" y="{y0 + j * 17:.1f}" text-anchor="{anchor}" font-size="15.5" font-family="Source Sans 3,Segoe UI,sans-serif" fill="var(--fg)">{E(ln)}{tail}</text>')
    if not scores:
        o.append(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="16" font-weight="600" font-family="Source Sans 3,sans-serif" fill="var(--muted)">First scores after matchday 1</text>')
    o.append("</svg>")
    return "".join(o)


def _flag(code, name):
    return f'<i class="fl fl-{E(code)}" role="img" aria-label="{E(name)} flag"></i>' if code else ""


def player_card(p, averages):
    role = p["role"]
    label, axes = ROLES[role]
    avg_entry = averages.get(role) or {}
    count = avg_entry.get("count", 0)
    avg = avg_entry.get("scores") if count >= MIN_PEERS else None
    s = p["scores"]
    title = f'{p["name"]}, {label}: radar of eight areas' + (" against the role average" if avg else "")
    if avg:
        diffs = sorted(((s[a] - avg[a], a) for a in axes), reverse=True)
        ups = [(d, a) for d, a in diffs if d >= 0.3][:2]
        if ups:
            read = "Above the role average in " + " and ".join(f'{E(a.lower())} (+{d:.1f})' for d, a in ups) + "."
        else:
            d, a = diffs[0]
            read = f"Closest to the role average in {E(a.lower())}."
        basis_avg = f"Role average: {count} {label.lower()}s rated by Afritech at this tournament."
    else:
        read = f"Strongest area so far: {E(max(axes, key=lambda a: s[a]).lower())} ({max(s.values()):.1f})."
        basis_avg = f"The role average appears once {MIN_PEERS} {label.lower()}s are rated."
    watched = []
    if p.get("matches"):
        watched.append(f'{p["matches"]} full match{"es" if p["matches"] != 1 else ""} watched')
    if p.get("minutes"):
        watched.append(f'{p["minutes"]} minutes')
    return f'''<article class="rc" data-role="{role}">
  <header>{_flag(p.get("flag"), p["nation"])}<div><h3>{E(p["name"])}</h3><p class="meta">{E(p["nation"])} · {E(label)}</p></div></header>
  {radar_svg(role, s, avg, title)}
  <p class="read">{read}</p>
  <p class="cap">Scout scores, 1 to 10, from full-match viewing{": " + " · ".join(watched) if watched else ""}. {basis_avg} Dashed ring marks 7.0.</p>
  <p class="rec"><span class="verdict">MONITOR</span> <span>Full scout card after the group stage. <a href="../#contact">Request the private pack</a>.</span></p>
</article>'''


def empty_card(b):
    role = b.get("role")
    if role:
        label = ROLES[role][0]
        body = radar_svg(role, None, None, f'{b["name"]}: {label} radar, awaiting first scores')
    else:
        label = "Role confirmed at first match"
        body = '<div class="norole">Radar appears once his role at the tournament is confirmed.</div>'
    return f'''<article class="rc pending" data-role="{role or "tbc"}">
  <header>{_flag(b.get("flag"), b["nation"])}<div><h3>{E(b["name"])}</h3><p class="meta">{E(b["nation"])} · {E(label)}</p></div></header>
  {body}
  <p class="cap">Scores appear after his first match is watched in full.</p>
</article>'''


def build_content(path):
    d = json.load(open(path, encoding="utf-8"))
    players = [p for p in d.get("players", []) if p.get("role") in ROLES and len(p.get("scores", {})) == len(ROLES[p["role"]][1])]
    shown = {p["name"] for p in players}
    cards = [player_card(p, d.get("averages", {})) for p in players]
    cards += [empty_card(b) for b in d.get("board", []) if b["name"] not in shown]
    roles_present = []
    for c in players + [b for b in d.get("board", []) if b["name"] not in shown]:
        r = c.get("role") or "tbc"
        if r not in roles_present:
            roles_present.append(r)
    chips = "".join(f'<button type="button" data-f="{r}">{E(ROLES[r][0] if r in ROLES else "Role to be confirmed")}</button>' for r in roles_present)
    status = (f"{len(players)} player{'s' if len(players) != 1 else ''} rated" if players else "Scoring starts with matchday 1 on 19 November")
    return {"{{CARDS}}": "\n".join(cards), "{{CHIPS}}": chips, "{{UPDATED}}": E(d.get("updated", "")), "{{STATUS}}": E(status)}
