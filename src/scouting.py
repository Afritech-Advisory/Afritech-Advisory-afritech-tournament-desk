"""Afritech-TSA scout cards for the Tournament Desk (Stage 1, public-domain evidence).

Whole-tournament scan: every African player with a goal or assist, and from the other 38 teams every
multi-goal scorer, Player of the Match or decisive performer. One record per player
(src/data/qatar-u17-2026-scouting.json). Tournament numbers are computed from the final match reports
(African matches: src/data/qatar-u17-2026-nations.json; other matches: src/data/qatar-u17-2026-results.json),
never typed by hand, so the main board, nation pages and peer comparison always agree.
Every player is under 18: club signal MONITOR, agent DEVELOP FIRST, no valuation, and no published
grades until Andrew approves them in the private tracker."""
import json, re, html as H

CSS = """
html[lang=sw] .nums div{display:flex;flex-direction:column-reverse;justify-content:flex-end;gap:2px}
.scard .clipbtn,.gl .clipbtn{white-space:normal;max-width:100%;min-height:44px;text-align:left;overflow-wrap:anywhere}
.scard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;display:grid;gap:10px;scroll-margin-top:70px;align-content:start}
.scard header{display:flex;gap:12px;align-items:center}
.scard .sil{width:52px;height:52px;flex:none;border-radius:50%;background:var(--soft);display:grid;place-items:center}
.scard h3{font-size:1.35rem}
.scard .meta{color:var(--muted);font-size:.92rem}
.cap{font:600 .68rem var(--mono);letter-spacing:.06em;background:var(--navy);color:#fff;border-radius:4px;padding:2px 6px;margin-left:6px;vertical-align:2px}
.ccode{font:600 .72rem var(--mono);background:var(--soft);border-radius:4px;padding:1px 5px;margin-right:4px}
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
.scard .clipbtn{font:700 .88rem var(--body);border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:99px;padding:6px 12px;cursor:pointer;white-space:nowrap;text-decoration:none;display:inline-block}
.gl{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:6px}
.gl .tm{font:600 .78rem var(--mono);color:var(--muted);align-self:center}
.cplayer{position:relative;aspect-ratio:16/9;background:#000;border-radius:10px;overflow:hidden}
.cplayer iframe,.cplayer>div{position:absolute;inset:0;width:100%;height:100%;border:0}
.cplayer[hidden],.scard[hidden],.bfilter[hidden]{display:none}
.peer{width:100%;height:auto;display:block;max-width:640px}
.scards{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}
.bfilter{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.bfilter button{font:700 .9rem var(--body);border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:99px;padding:7px 14px;cursor:pointer}
.bfilter button[aria-pressed="true"]{background:var(--navy);color:#fff;border-color:var(--navy)}
@media (max-width:420px){.nums b{font-size:1.35rem}.ladder2{grid-template-columns:1fr}.scards{grid-template-columns:1fr}}
"""

SIL = '<svg viewBox="0 0 40 40" width="40" height="40" aria-hidden="true"><circle cx="20" cy="14" r="8" fill="var(--line)"/><path d="M4 38c2-9 9-13 16-13s14 4 16 13z" fill="var(--line)"/></svg>'

# Shared YouTube loader: every clip player on a page (match reports and scout cards) uses it.
YT_LOADER = """<script>
window.afYT=function(cb,fail){if(window.YT&&YT.Player)return cb();(window.__ytq=window.__ytq||[]).push(cb);if(window.__ytl)return;window.__ytl=1;
var prev=window.onYouTubeIframeAPIReady;window.onYouTubeIframeAPIReady=function(){if(prev)prev();var q=window.__ytq||[];window.__ytq=[];q.forEach(function(f){f()})};
var s=document.createElement('script');s.src='https://www.youtube.com/iframe_api';s.onerror=function(){window.__ytfail=1;if(fail)fail()};document.head.appendChild(s)};
</script>
<style>
.afp{position:absolute;inset:0;background:#000;overflow:hidden}
.afp-frame,.afp-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.afp-shield{position:absolute;inset:0;z-index:2;background:transparent;border:0;margin:0;padding:0;cursor:pointer;-webkit-tap-highlight-color:transparent}
.afp-cover{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:14px;text-align:center;color:#fff;background:linear-gradient(135deg,#0F2442,#1A365D);font:600 .98rem var(--body,system-ui)}
.afp-cover[hidden],.afp-hint[hidden],.afp-snd[hidden]{display:none}
.afp-hint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:3;pointer-events:none;background:rgba(232,112,26,.95);color:#1B1206;font:700 1rem var(--body,system-ui);padding:10px 18px;border-radius:22px}
.afp-snd{position:absolute;right:8px;top:8px;z-index:4;min-height:36px;padding:6px 12px;border-radius:18px;border:0;background:rgba(11,28,51,.85);color:#fff;font:700 .85rem var(--body,system-ui);cursor:pointer}
.afp-cover .row{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.afp-cover button{font:700 .95rem var(--body,system-ui);min-height:44px;padding:8px 16px;border-radius:22px;border:0;cursor:pointer;background:#E8701A;color:#1B1206}
.afp-cover button.g{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.6)}
.afp-bar{position:absolute;left:0;right:0;bottom:0;height:4px;z-index:4;background:rgba(255,255,255,.18)}
.afp-bar i{display:block;height:100%;width:0;background:#E8701A}
</style>
<script>
/* One clip player for the whole site. A clip plays from its start to its end inside its own box, then stops
   and shows Replay / Next. A transparent layer over the video takes every tap (pause, play), so nothing on the
   YouTube player itself can be pressed: no logo, no title, no suggested videos, no way off this page. */
(function(){
var T={sound:'Sound on',mute:'Sound off',tap:'Tap to play',paused:'Paused',cont:'Continue',replay:'Replay',next:'Next goal',done:'Clip finished.',err:'This clip cannot be shown here right now.',retry:'Try again',pp:'Pause or play the clip'};
function el(h){var d=document.createElement('div');d.innerHTML=h;return d.firstChild}
function cover(st,msg,btns){var c=st.cover;c.innerHTML='<p style="margin:0">'+msg+'</p>';var r=el('<div class="row"></div>');
 btns.forEach(function(b){var x=document.createElement('button');x.type='button';x.textContent=b[0];if(b[2])x.className='g';x.addEventListener('click',function(ev){ev.stopPropagation();b[1]()});r.appendChild(x)});
 c.appendChild(r);c.hidden=false;st.shield.hidden=true;if(st.snd)st.snd.hidden=true;if(st.hint)st.hint.hidden=true}
function uncover(st){st.cover.hidden=true;st.shield.hidden=false}
function stopPoll(st){if(st.t){clearInterval(st.t);st.t=null}}
function finish(st){stopPoll(st);st.done=true;try{st.p.pauseVideo()}catch(x){}
 var o=st.o,b=[[T.replay,function(){window.afClip(st.box,o)}]];if(o.next)b.push([T.next+' ›',o.next]);
 cover(st,T.done,b);st.bar.style.width='100%';if(o.onEnd)o.onEnd()}
function poll(st){stopPoll(st);st.t=setInterval(function(){try{var t=st.p.getCurrentTime(),o=st.o,end=o.e||st.p.getDuration()-0.4;
 if(end>o.s)st.bar.style.width=Math.min(100,Math.max(0,(t-o.s)/(end-o.s)*100))+'%';if(end&&t>=end-0.15)finish(st)}catch(x){}},200)}
function fail(st){stopPoll(st);clearTimeout(st.w);cover(st,T.err,[[T.retry,function(){window.afClip(st.box,st.o)}]])}
function start(st){var o=st.o;st.done=false;st.bar.style.width='0';uncover(st);
 try{if(!st.sound)st.p.mute()}catch(x){}
 st.p.loadVideoById({videoId:o.v,startSeconds:o.s||0});
 try{st.p.playVideo()}catch(x){}
 clearTimeout(st.w);st.w=setTimeout(function(){try{var s=st.p.getPlayerState();if(s!==1&&s!==3&&!st.done)tapThrough(st)}catch(x){tapThrough(st)}},2500)}
function tapThrough(st){ /* the phone wants a tap on the video itself: let one tap through, then the shield comes back */
 st.cover.hidden=true;st.shield.hidden=true;st.hint.hidden=false}
window.afClip=function(box,o){
 var st=box.__af;
 if(!st){box.innerHTML='';var w=el('<div class="afp"><div class="afp-frame"><div></div></div><button type="button" class="afp-shield"></button><div class="afp-cover" hidden></div><div class="afp-hint" hidden></div><button type="button" class="afp-snd" hidden></button><div class="afp-bar"><i></i></div></div>');
  box.appendChild(w);st=box.__af={box:box,frame:w.querySelector('.afp-frame>div'),shield:w.querySelector('.afp-shield'),cover:w.querySelector('.afp-cover'),hint:w.querySelector('.afp-hint'),snd:w.querySelector('.afp-snd'),bar:w.querySelector('.afp-bar i')};
  st.hint.textContent='\u25B6 '+T.tap;st.snd.textContent='\u266A '+T.sound;
  st.snd.addEventListener('click',function(ev){ev.stopPropagation();st.sound=!st.sound;try{st.sound?st.p.unMute():st.p.mute()}catch(x){};st.snd.textContent=(st.sound?'\u266A ':'\u266A ')+(st.sound?T.mute:T.sound)});
  st.shield.setAttribute('aria-label',T.pp);
  st.shield.addEventListener('click',function(){if(!st.p)return;var s=st.p.getPlayerState();if(s===1){st.p.pauseVideo()}else{uncover(st);st.p.playVideo()}})}
 st.o=o;
 if(st.p&&st.ready)return start(st);
 if(st.loading)return;st.loading=1;
 window.afYT(function(){st.p=new YT.Player(st.frame,{videoId:o.v,
  playerVars:{playsinline:1,controls:0,disablekb:1,fs:0,rel:0,modestbranding:1,iv_load_policy:3,cc_load_policy:0,start:Math.floor(o.s||0)},
  events:{onReady:function(){st.ready=1;start(st)},
   onError:function(){fail(st)},
   onStateChange:function(e){if(e.data===1){clearTimeout(st.w);st.hint.hidden=true;st.snd.hidden=false;uncover(st);poll(st)}
    else if(e.data===2&&!st.done){stopPoll(st);cover(st,T.paused,[['▶ '+T.cont,function(){uncover(st);st.p.playVideo()}],['↺ '+T.replay,function(){window.afClip(st.box,st.o)},1]])}
    else if(e.data===0&&!st.done){finish(st)}}}})},
  function(){cover(st,T.err,[[T.retry,function(){location.reload()}]])});
};
})();
</script>"""

# Scout-card clips: each card has its own small player; a clip plays from its start to its end and stops.
CARD_JS = """<script>
(function(){
document.querySelectorAll('button.cclip').forEach(function(b){b.addEventListener('click',function(){
 var card=b.closest('.scard'),box=card.querySelector('.cplayer');box.hidden=false;
 card.querySelectorAll('button.cclip').forEach(function(x){x.classList.toggle('on',x===b)});
 window.afClip(box,{v:b.getAttribute('data-v'),s:+b.getAttribute('data-s'),e:+b.getAttribute('data-e')});
})});
var f=document.querySelector('.bfilter');if(f){f.hidden=false;f.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){
 var r=b.getAttribute('data-r');f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
 document.querySelectorAll('#board-cards .scard').forEach(function(c){c.hidden=!(r==='all'||c.getAttribute('data-region')===r)})})})}
})();
</script>"""


def load(root):
    nations = json.loads((root / "src/data/qatar-u17-2026-nations.json").read_text())
    scout = json.loads((root / "src/data/qatar-u17-2026-scouting.json").read_text())
    results = json.loads((root / "src/data/qatar-u17-2026-results.json").read_text())
    nations["_results"] = results["matches"]
    return nations, scout


def team(p, nations):
    """Name, FIFA code, flag and desk slug (None outside Africa) for a player's team."""
    if p.get("nation"):
        for n in nations["nations"]:
            if n["slug"] == p["nation"]:
                return {"name": n["name"], "code": n["code"], "flag": n["flag"], "slug": n["slug"]}
    return {"name": p["country"], "code": p["code"], "flag": p.get("flag", ""), "slug": None}


def all_matches(nations):
    for n in nations["nations"]:
        for m in n["matches"]:
            if m.get("score"):
                yield m
    for m in nations.get("_results", []):
        yield m


def numbers(pid, nations):
    goals, assists = [], []
    for m in all_matches(nations):
        clips = [g for g in m.get("goals", []) if g.get("s") is not None]
        for g in m.get("goals", []):
            rec = {"m": m, "g": g, "clip": clips.index(g) if g in clips else None}
            if g.get("pid") == pid:
                goals.append(rec)
            if g.get("apid") == pid:
                assists.append(rec)
    return goals, assists


def team_matches(t, nations):
    return sum(1 for m in all_matches(nations) if t["name"] in (m["home"], m["away"]))


def flag_html(t):
    if t["flag"]:
        return f'<i class="fl fl-{t["flag"]}" role="img" aria-label="{H.escape(t["name"])} flag"></i> '
    return f'<span class="ccode">{t["code"]}</span>'


def vid(url):
    return url.split("v=")[1].split("&")[0]


def card(p, nations, here_slug=None):
    """Full scout card. here_slug: the nation page it sits on (None = main board)."""
    t = team(p, nations)
    goals, assists = numbers(p["id"], nations)
    bits = [x for x in (p.get("role"), p.get("club"), ("No. " + p["shirt"]) if p.get("shirt") else "", ("Age %d" % p["age"]) if p.get("age") else "") if x]
    meta = flag_html(t) + H.escape(t["name"]) + ("" if not bits else " · " + " · ".join(H.escape(b) for b in bits))
    cap = '<span class="cap">CAPTAIN</span>' if p.get("captain") else ""
    moments, clips = [], 0
    for r, kind in [(x, "Goal") for x in goals] + [(x, "Assist") for x in assists]:
        m, g = r["m"], r["g"]
        opp = m["away"] if m["home"] == t["name"] else m["home"]
        label = f'{kind} v {opp}, {g["min"]}'
        if g.get("s") is not None and m.get("video"):
            clips += 1
            moments.append(f'<li><button class="clipbtn cclip" type="button" data-v="{vid(m["video"])}" data-s="{g["s"]}" data-e="{g["e"]}">&#9654; {H.escape(label)}</button></li>')
        elif t["slug"]:
            href = f'#{m["id"]}' if here_slug == t["slug"] else (f'../{t["slug"]}/#{m["id"]}' if here_slug else f'{t["slug"]}/#{m["id"]}')
            moments.append(f'<li><a class="clipbtn" href="{href}">{H.escape(label)} &rsaquo;</a></li>')
        else:
            moments.append(f'<li class="tm">{H.escape(label)}</li>')
    pl = lambda n, one, many: f'<div><b>{n}</b><span>{one if n == 1 else many}</span></div>'
    tm = team_matches(t, nations)
    nums = ('<div class="nums">' + pl(len(goals), "Goal", "Goals") + pl(len(assists), "Assist", "Assists")
            + pl(tm, "Team match", "Team matches") + pl(clips, "Clip", "Clips") + '</div>')
    seen = "".join(f"<li>{H.escape(f)}</li>" for f in p["facts"])
    page_link = ""
    if t["slug"] and here_slug is None:
        page_link = f'<p class="fine" style="margin:0"><a href="{t["slug"]}/">{H.escape(t["name"])}: match reports and all scout cards &rsaquo;</a></p>'
    region = "africa" if t["slug"] else "world"
    return (f'<article class="scard" id="{p["id"]}" data-region="{region}"><header><div class="sil">{SIL}</div><div><h3>{H.escape(p["name"])}{cap}</h3>'
            f'<p class="meta">{meta}</p></div></header>'
            f'<div class="sig"><span>Club: <b>MONITOR</b></span><span>Agent: <b>DEVELOP FIRST</b></span><span>Federation: <b>{p["fed"]}</b></span></div>'
            f'<p><b>Next:</b> {H.escape(p["next"])}</p>{nums}'
            f'{f"<ul class=gl>{chr(10).join(moments)}</ul>" if moments else ""}'
            f'<div class="cplayer" hidden></div>'
            f'<h4 style="margin:2px 0 0;font-family:var(--display);font-size:1.1rem">What we have seen</h4><ul class="seen">{seen}</ul>'
            f'<div class="ladder2"><div class="u"><b>Moves him up</b>{H.escape(p["up"])}</div><div class="d"><b>Moves him down</b>{H.escape(p["down"])}</div></div>'
            f'<p class="fine" style="margin:0">Built from final match reports, FIFA\'s official highlights and published sources. His full four-area and position profile follows after his group matches.</p>{page_link}</article>')


def ranked(players, nations):
    def key(p):
        g, a = numbers(p["id"], nations)
        return (-(len(g) + len(a)), -len(g), 0 if p.get("nation") else 1, p["name"])
    return sorted(players, key=key)


def peer_svg(nations, scout, highlight_nation=None):
    """Tournament peer comparison: goal involvements of every carded player (one dot per goal or assist)."""
    rows = []
    for p in ranked(scout["players"], nations):
        g, a = numbers(p["id"], nations)
        if g or a:
            rows.append((len(g), len(a), p))
    if not rows:
        return ""
    W, rh, x0 = 360, 28, 190
    h = 20 + rh * len(rows) + 34
    o = [f'<svg class="peer" viewBox="0 0 {W} {h}" role="img" aria-label="Goal involvements of the players on our board">']
    for k, (g, a, p) in enumerate(rows):
        y = 20 + k * rh
        t = team(p, nations)
        mine = highlight_nation in (None, p.get("nation"))
        bold = 700 if (highlight_nation and p.get("nation") == highlight_nation) or (highlight_nation is None and p.get("nation")) else 400
        o.append(f'<text x="0" y="{y + 4}" font-size="12.5" fill="{"var(--fg)" if mine else "var(--muted)"}" font-family="Source Sans 3,Segoe UI,sans-serif" font-weight="{bold}">{H.escape(p["name"])} ({t["code"]})</text>')
        for i in range(g + a):
            c = "var(--teal)" if i < g else "var(--purple)"
            o.append(f'<circle cx="{x0 + 10 + i * 22}" cy="{y}" r="8" fill="{c}" opacity="{1 if mine else .45}"/>')
    ly = h - 8
    o.append(f'<circle cx="6" cy="{ly - 4}" r="6" fill="var(--teal)"/><text x="16" y="{ly}" font-size="12" fill="var(--muted)">Goal</text>'
             f'<circle cx="66" cy="{ly - 4}" r="6" fill="var(--purple)"/><text x="76" y="{ly}" font-size="12" fill="var(--muted)">Assist</text>'
             f'<text x="{W}" y="{ly}" text-anchor="end" font-size="12" fill="var(--muted)">One dot = one goal or assist</text>')
    o.append("</svg>")
    return ("".join(o) + '<p class="fine">How to read: every player on our board with a goal or assist, from all 48 teams; African players in bold. '
            'Teal dots are goals, purple dots assists. Counts from final match reports, updated after every matchday.</p>')


def board_html(nations, scout):
    """Main desk board: the full scout card of every player, ranked by goal involvements, with an Africa / rest-of-world filter."""
    ps = ranked(scout["players"], nations)
    na = sum(1 for p in ps if p.get("nation"))
    filt = (f'<div class="bfilter" role="group" aria-label="Filter the board" hidden>'
            f'<button type="button" data-r="all" aria-pressed="true">All ({len(ps)})</button>'
            f'<button type="button" data-r="africa" aria-pressed="false">Africa ({na})</button>'
            f'<button type="button" data-r="world" aria-pressed="false">Rest of the world ({len(ps) - na})</button></div>')
    return filt + '<div class="scards" id="board-cards">' + "".join(card(p, nations) for p in ps) + "</div>"


def results_html(nations, flag):
    """Results first on the main page: every finished African match with scorers and key numbers,
    linking to the full match report on the nation page, then the other results at the tournament."""
    seen, cards = set(), []
    order = lambda m: int(re.search(r"(\d+)", m["date"]).group(1))
    rows = []
    for n in nations["nations"]:
        for m in n["matches"]:
            if m.get("score") and m["id"] not in seen:
                seen.add(m["id"]); rows.append((n, m))
    rows.sort(key=lambda r: (-order(r[1]), r[0]["group"]))
    for n, m in rows:
        side = lambda x: (flag(n["flag"], x) if x == n["name"] else "") + H.escape(x)
        goals = "".join(f'<li><span class="m">{g["min"]}</span><span>{H.escape(g["who"])} ({H.escape(g["team"])})</span></li>' for g in m.get("goals", []))
        kn = "".join(f'<div><b>{H.escape(a)}</b><span>{H.escape(b)}</span></div>' for a, b in m.get("keyNumbers", [])[:3])
        cards.append(f'<article class="rc"><p class="when">{H.escape(m["date"])} · Group {n["group"]}</p>'
                     f'<p class="sc2"><span>{side(m["home"])}</span><b>{m["score"]}</b><span class="r">{side(m["away"])}</span></p>'
                     f'{f"<ul class=rg>{goals}</ul>" if goals else ""}{f"<div class=kn>{kn}</div>" if kn else ""}'
                     f'<a class="btn primary" href="{n["slug"]}/#{m["id"]}">Match report, goal clips and analysis &rsaquo;</a></article>')
    other = "".join(f'<li><span>{H.escape(m["home"])}</span> <b>{m["score"]}</b> <span>{H.escape(m["away"])}</span> <i>Group {m["group"]}</i></li>'
                    for m in nations.get("_results", []))
    return (f'<section class="s" id="results"><div class="s-head"><p class="eyebrow">Results</p><h2>Every African match so far</h2>'
            f'<p class="sub">Final scores, the goals and the numbers that tell each match. Tap a match for every goal as a clip and our full analysis.</p></div>'
            f'<div class="rgrid">{"".join(cards)}</div>'
            + (f'<h3 style="margin-top:22px">Other results at the tournament</h3><ul class="ores">{other}</ul>' if other else "")
            + '</section>')

RESULTS_CSS = """
.rgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.rc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;display:grid;gap:10px;align-content:start}
.rc .when{font-family:var(--mono);font-size:.8rem;color:var(--muted);margin:0}
.sc2{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:10px;margin:0;font-family:var(--display);font-weight:700;font-size:1.3rem;line-height:1.15}
.sc2 .r{text-align:right}.sc2 b{background:var(--navy);color:#fff;border-radius:8px;padding:4px 12px;white-space:nowrap;font-variant-numeric:tabular-nums}
.sc2 .fl{width:26px;height:19px;vertical-align:-2px;margin-right:6px}
.rg{list-style:none;margin:0;padding:0;display:grid;gap:4px;font-size:.95rem}
.rg li{display:grid;grid-template-columns:3.4em minmax(0,1fr);gap:6px;border-top:1px solid var(--line);padding-top:4px}
.rg .m{font-family:var(--mono);font-weight:600;color:var(--orange-text)}
.rc .kn{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.rc .kn div{background:var(--soft);border-radius:8px;padding:8px}
.rc .kn b{display:block;font-family:var(--display);font-size:1.4rem;line-height:1;color:var(--navy)}
@media (prefers-color-scheme:dark){.rc .kn b{color:var(--orange-text)}}
.rc .kn span{font-size:.78rem;color:var(--muted);overflow-wrap:anywhere}
.rc .btn{justify-self:stretch;text-align:center;white-space:normal}
.ores{list-style:none;padding:0;margin:8px 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:6px}
.ores li{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px;font-size:.95rem}
.ores b{font-variant-numeric:tabular-nums;margin:0 4px}.ores i{font-style:normal;color:var(--muted);font-size:.82rem;margin-left:6px}
"""
