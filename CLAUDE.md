# Working rules for Claude on Afritech projects

## Output format (Andrew's standing rule, 10 Nov 2026)
- Anything meant to go out (email, WhatsApp, post, briefing, client text) is given as a **copy-ready block**: final wording, links and dates filled in, nothing to edit except clearly marked [brackets]. One block per channel.
- Notes for Andrew (what changed, decisions, checks, instructions) go in a **separate section**, after the copy-ready blocks, and never inside them.
- Deliver the complete package in one reply: anticipate what goes with it (links, attachments, cover note, checklist) instead of sending it piece by piece.
- Be proactive: build what the task obviously needs without being asked. Keep replies short; no lectures or jargon.
- Gatekeeper questions go at the very end of the reply, after the notes, so Andrew never has to search for them (Andrew, 19 Nov 2026).

## Blocked items in one section (Andrew, 23 Nov 2026, applies to every chat, project and task)
- Anything that did not open or work (a file, PDF, page, tool, login, connector, permission) and everything left undone because of it goes in **one section** of the reply, headed **"Blocked: for you to deal with"**. One line each: what it is, why it failed, what it holds up, and the fix or next step. Never scatter these through the rest of the reply.
- Place it after the notes and before the Gatekeeper questions, which stay last. If nothing was blocked, leave the section out.

## Four Sentences first (Andrew's rule, 15 Nov 2026)
- Before writing or changing any page, card, invite, briefing or tracker text, read the Afritech Four Sentences (the afritech-four-sentences skill and memory file): who it's for, what they get, why they'd believe us, the one action.
- Every public page's first screen passes the stranger test: someone outside football can say who it's for and what to do next.
- When desk work shows a sharper way to say one of the four sentences for this desk's readers (participants, scouts, clubs), put it to Andrew as a lettered Gatekeeper question. Don't change the master yourself.
- Scheduled runs on reduced cadence still skip this; it applies whenever real work runs.

## The desk's other working rules are private
Run cadence, tracker stamps, approval alerts, automatic catch-up, the tag standard and the nightly tag check are kept in Afritech Sports' private files: `internal/tournament-desk/CLAUDE.md` in the private repository `Afritech-Advisory/afritech-matchiq-clients` (moved 16 Nov 2026). The scheduled runs carry them in their own instructions. In a session Andrew starts himself, attach that private repository and read the file before any desk work.

## Nation pages: every match goes under its country (Andrew, 20 Nov 2026)
- Each of Africa's ten has its own page at `qatar-u17-2026/<nation>/`, built from `src/data/qatar-u17-2026-nations.json` by `src/nations.py`.
- When a match result is approved for the desk, add it to that nation's entry in the same pull request: `id` (the tracker match id), `score`, `video` (FIFA's official highlights URL), `goals` (minute, team, scorer, `type`, `how`, and the clip window `s`/`e` = seconds into the official highlights from the build-up to just after the finish or its replay, only for goals checked on video), `story`, `keyNumbers` (3 to 4 numbers that tell the match), `analysis` (3 to 4 short points: how the goals came, game state, what it means for the group and the next match) and `scout` (one sales-first "For clubs" line naming who to follow next). Every claim comes from the video or published match reports; no guesses. Then the nation card's link label and the Match centre result link to `<nation>/#<id>`.
- Clips stay on the desk (Andrew, 20 Nov 2026): every clip plays inside its own box through the shared player `window.afClip` (src/scouting.py), from its start to its end, then stops on a Replay / Next goal card. A layer over the video takes every tap, so no YouTube logo, title or suggested video can be pressed. No "Open on YouTube" links on desk pages.
- Final scores only. Never publish scout scores or anything provisional. Never download, clip or re-upload match video: link to FIFA's official video only.
- How goal clips get their timings (Andrew, 23 Nov 2026, Gatekeeper 1A+D): Claude does not download match video. Each day Claude puts a download list (FIFA's official 2-minute highlights on FIFA's YouTube channel, one link per finished African match) in Andrew's `Afritech_Video` folder on his computer (`C:\Users\andre\Afritech_Video`, connected to the chat) as `DOWNLOAD_LIST_<date>.txt`, and Andrew downloads them into that folder. Claude reads the files there only to time the clips: the score change on the broadcast scoreboard is found frame by frame, then `t` (the finish), `s` (start of the move) and `e` (end of the celebration or replay, never into the next goal) are set and checked on contact sheets. Nothing from those files is uploaded or published: the site still plays FIFA's official video through `window.afClip`. Andrew spot-checks the timings at review time from the QA pack (Desk_QA_pack_<date>.md in Afritech_Video). ChatGPT is no longer part of the desk (Andrew, 24 Nov 2026): no task, prompt or QA step goes to it.
- A goalless match gets `moments` instead of goals (Andrew, 23 Nov 2026, Gatekeeper 2D): 2 to 4 key chances and saves, each with `min`, `team`, `who`, `how`, `s` and `e`, shown under "Key moments" with the same clip player. Only describe what the video shows.
- Key frames (Andrew, 23 Nov 2026, decision 1; updated Gatekeeper 1D the same day): every goal and key moment gets three still frames from FIFA's official highlights (build-up, the finish, the celebration), taken from the copy Andrew downloaded into Afritech_Video, saved web-sized (JPEG, 640 px wide) as `qatar-u17-2026/stills/<match id>-<goal no>-<1..3>.jpg` and listed in the goal's `stills` field. They show when FIFA refuses the clip, with the credit "Key frames: FIFA official broadcast, used for match analysis". No other use of match images.
- FIFA blocks its videos from playing inside other websites (checked 23 Nov 2026: "FIFA has blocked it from display on this website"). So when a clip is refused, the player shows the key frames and a "Watch the goal on FIFA's video" button (Andrew, Gatekeeper 1D): it opens FIFA's video at the goal's start in a new tab, counts down the clip length, closes that tab by itself at the clip's end and brings the reader back to the same goal on the desk (Replay / Next goal). This button is the one allowed route to YouTube; no plain links to YouTube on desk pages. No request to FIFA for embed permission (Andrew's call).
- Any News item about a match links to its nation page and match, e.g. `qatar-u17-2026/mozambique/#moz-den`.

## Results first on the main page (Andrew, 20 Nov 2026)
- The main page opens with **Results**: every finished African match (score, scorers, three key numbers, link to the full report on the nation page), then the other results at the tournament. It is built automatically from the nations and results data files by `scouting.results_html`, so a new match report appears there in the same build. The section menu stays visible on phones.

## Scouting merged into the desk: scout cards (Andrew, 20 Nov 2026)
The desk is a scouting system, so every nation page and the main board run on the Afritech-TSA scouting method (afritech-scouting skill, Stage 1 public-domain evidence, minors rules).
- **Who gets a card (whole-tournament exception scan of all 48 teams, after every matchday, automatically):** every African player with a goal or assist, every captain with real impact, standout goalkeepers, unusually young starters, decisive performers, plus the pre-tournament board; and from the other 38 teams every multi-goal scorer, every Player of the Match and every decisive performer. Each one goes into `src/data/qatar-u17-2026-scouting.json` (African players with `nation`, others with `country`, `code`, `flag`) and appears as a full scout card on the main board (filter: All / Africa / Rest of the world) and, for African players, on the nation page too. Final results of matches without an African side go in `src/data/qatar-u17-2026-results.json` with `pid`/`apid`, so every player's numbers compute themselves.
- **Card record:** `id` (same as the tracker prospect id), `nation`, `name`, `role` (from the squad list or line-up; leave blank if not sourced), `club`, `shirt`, `captain`, `age` only if published, `facts` (public-domain, sourced, sales-first), `fed` (WATCHLIST until grades are approved), `next` (positive next-step line), `up` and `down` (verdict ladder). Goals and assists link to players with `pid`/`apid` in the match report; tournament numbers, clips and the peer comparison are computed from the match reports, never typed.
- **Minors caps on every card:** Club MONITOR, Agent DEVELOP FIRST, no valuation, no transfer language.
- **Grades:** four-area and position pizzas and numeric grades are drafted only in the private tracker (rule 8D) and published on a card only after Andrew approves them. Until then the card says the full profile follows after the group matches.
- Every new card is also added to the tracker's `prospects` collection with status "Watch" and a dated note.
- **Every matchday run updates all of it in one pull request:** match reports for every finished African match, results file for the other matches, new and updated scout cards (Ziyad Baha-style updates to facts, next and up/down lines), nation cards, Match centre results and the board. Final scores only: a match still live or not reported as finished by two sources waits for the next run.

## Four languages on every page (Andrew, 20 Nov 2026, Gatekeeper 1D)
- The desk is published in English, French, Kiswahili and Brazilian Portuguese: English at the root, copies at `fr/`, `sw/` and `pt/`, each with the language bar and hreflang links.
- Every new or changed piece of English text (data files, match reports, scout cards, page text, JS messages) gets its French, Kiswahili and Brazilian Portuguese wording in `src/i18n/dict_a.py` (site and main page) or `src/i18n/dict_b.py` (nations, reports, cards, JS) in the same pull request. `build.py` turns them into `src/i18n/*.json`.
- The build stops if any text is missing a translation and lists it in `src/i18n/missing-<lang>.txt`. Never publish with missing translations and never ship English inside a translated page.
- Names of players, clubs, coaches and places stay as written. Write natural sales-first wording for each reader (French with " : " spacing, Brazilian Portuguese not European), not word-for-word.

## Gatekeeper decisions, 23 Nov 2026 (Andrew)
- **A3, readers stay on the desk:** no link on a desk page sends people elsewhere except the contact routes: WhatsApp, Afritech's and Andrew's LinkedIn pages, and Afritech Sports' own sites (home site, Player CVs, this desk) stay live (Andrew, 23 Nov 2026). `build.py` turns every other outside link into plain text (the source stays named) and the desk header keeps the full Afritech Sports bar (Home, Menu, sections, Our desks; restored 23 Nov 2026 after it was dropped by mistake), with "Talk to us" going to WhatsApp. Don't add outside links by hand.
- **B2, Kiswahili reads label first:** number tiles on Kiswahili pages show the label, then the value ("Pointi: 3"). `src/i18n.py` does it in every build; write the English tile as usual.
- **C, FIFA's minute is the record:** when FIFA's match report or round-up gives a different goal minute from a feed or another site, use FIFA's minute straight away. Don't wait for the video.


## Commonwealth English (24 Nov 2026)

Afritech Sports writes Commonwealth English, the formal register taught in Kenya
and across the Commonwealth. It is human writing. Read every page, CV and form in
context and judge it on what it says.

- Formal vocabulary, linking words (moreover, consequently), lists of three, long
  measured sentences and the contrasting parallel ("it's not X, it's Y") are
  allowed when every part is specific and true. Cut them only when they are empty.
- Never roughen text to look human: no slang, no deliberate errors, no chopping a
  long sentence that carries one line of thought.
- Never flag, reject or run anyone's writing (players, parents, coaches, scouts,
  analysts) through an AI detector. Their own English is kept as written.
- Hype words stay out (tapestry, game-changer, unlock, leverage, seamless). Em
  dashes stay out unless Andrew lifts that rule.
- Full rules: the afritech-anti-ai-writing-os and afritech-editor skills.
