# Working rules for Claude on Afritech projects

## Output format (Andrew's standing rule, 10 Nov 2026)
- Anything meant to go out (email, WhatsApp, post, briefing, client text) is given as a **copy-ready block**: final wording, links and dates filled in, nothing to edit except clearly marked [brackets]. One block per channel.
- Notes for Andrew (what changed, decisions, checks, instructions) go in a **separate section**, after the copy-ready blocks, and never inside them.
- Deliver the complete package in one reply: anticipate what goes with it (links, attachments, cover note, checklist) instead of sending it piece by piece.
- Be proactive: build what the task obviously needs without being asked. Keep replies short; no lectures or jargon.
- Gatekeeper questions go at the very end of the reply, after the notes, so Andrew never has to search for them (Andrew, 19 Nov 2026).

## Four Sentences first (Andrew's rule, 15 Nov 2026)
- Before writing or changing any page, card, invite, briefing or tracker text, read the Afritech Four Sentences (the afritech-four-sentences skill and memory file): who it's for, what they get, why they'd believe us, the one action.
- Every public page's first screen passes the stranger test: someone outside football can say who it's for and what to do next.
- When desk work shows a sharper way to say one of the four sentences for this desk's readers (participants, scouts, clubs), put it to Andrew as a lettered Gatekeeper question. Don't change the master yourself.
- Scheduled runs on reduced cadence still skip this; it applies whenever real work runs.

## The desk's other working rules are private
Run cadence, tracker stamps, approval alerts, automatic catch-up, the tag standard and the nightly tag check are kept in Afritech Sports' private files: `internal/tournament-desk/CLAUDE.md` in the private repository `Afritech-Advisory/afritech-matchiq-clients` (moved 16 Nov 2026). The scheduled runs carry them in their own instructions. In a session Andrew starts himself, attach that private repository and read the file before any desk work.

## Nation pages: every match goes under its country (Andrew, 20 Nov 2026)
- Each of Africa's ten has its own page at `qatar-u17-2026/<nation>/`, built from `src/data/qatar-u17-2026-nations.json` by `src/nations.py`.
- When a match result is approved for the desk, add it to that nation's entry in the same pull request: `id` (the tracker match id), `score`, `video` (FIFA's official highlights URL), `goals` (minute, team, scorer, how, and `t` = seconds into the official highlights where the goal is clearly seen), `story` and `scout` (one sales-first line: what a club should take from the match). Then the nation card's link label and the Match centre result link to `<nation>/#<id>`.
- Final scores only. Never publish scout scores or anything provisional. Never download, clip or re-upload match video: link to FIFA's official video only.
- Any News item about a match links to its nation page and match, e.g. `qatar-u17-2026/mozambique/#moz-den`.
