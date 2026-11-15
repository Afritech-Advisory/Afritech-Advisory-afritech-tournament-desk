# Working rules for Claude on Afritech projects

## Run cadence before the tournament (Andrew's rule, 14 Nov 2026) — check this first
- To save usage, scheduled runs are reduced until the eve of the tournament. Dates are Qatar time (UTC+3).
- **Runs that do the full work:** the morning run on 16 November 2026, then every scheduled run from 18 November 2026 onward (morning and evening).
- **Every other scheduled run on 14, 15, 16 and 17 November 2026** (both evening runs included, and the morning runs of 15 and 17 November): reply with the single line `Tournament Desk: reduced cadence before the tournament, nothing to do` and stop. Do not load skills, search, read the tracker, open a pull request or send a notification.
- A message typed by Andrew himself is never skipped; this rule covers scheduled runs only.
- From 19 November 2026 this section no longer applies and can be removed.

## Output format (Andrew's standing rule, 10 Nov 2026)
- Anything meant to go out (email, WhatsApp, post, briefing, client text) is given as a **copy-ready block**: final wording, links and dates filled in, nothing to edit except clearly marked [brackets]. One block per channel.
- Notes for Andrew (what changed, decisions, checks, instructions) go in a **separate section**, after the copy-ready blocks, and never inside them.
- Deliver the complete package in one reply: anticipate what goes with it (links, attachments, cover note, checklist) instead of sending it piece by piece.
- Be proactive: build what the task obviously needs without being asked. Keep replies short; no lectures or jargon.

## "Last verified" stamps in the private tracker (rule of 12 Nov 2026)
- The tracker shows a "last verified" time on every nation, player and match card. It reads two fields on each document: `verified` (ISO time, UTC) and `verifiedBy` (short label).
- Every run that checks a nation, prospect or match against a source sets `verified` to the time of the check and `verifiedBy` to "Morning run" or "Evening run", in the same update, **whether or not the facts changed**. Stamp only documents actually checked in that run; never stamp one you could not confirm.
- Always write with `update` (merge), never `set`, so stamps and other fields are not lost.
- Cards turn amber after 48 hours without a check. In the final message, list any Full-priority match or board player whose stamp is older than 48 hours.

## Approval alerts (rule of 12 Nov 2026)
- Whenever anything is waiting for Andrew's approval (an open pull request, a board addition, a photo, a verdict change), the run's final message **starts** with the line `APPROVAL NEEDED: <what> · reply "approved"` followed by the QA pack and pull request links. If nothing is waiting, start with `No approval needed today`.
- The morning run repeats the alert for anything still unapproved from earlier days, oldest first.

## Automatic catch-up when assistants have not updated (rule of 12 Nov 2026)
The tracker must be current every day, whether or not a human covered a match. In every run, for each African match that has finished and has neither `live` nor `replay` ticked and no video tags:
1. **Do the desk work from official and reliable public data** (FIFA match report via search, CAF, federations, ESPN, FotMob, national media; two sources): set `result` on the match (e.g. "MAR 2-1 ESP"), write scorers, assists, cards and line-up notes in `notes`, and set `autoCovered: true`. Stamp `verified` and `verifiedBy`.
2. **Tag the goals and assists** of watchlist players in the `videos` collection with the match minute, `scout: "System"`, and a link to the official highlights (FIFA+ or FIFA's YouTube channel) when one exists.
3. **Update each watchlist player's notes** with a dated stat line (started or sub, minutes, goals, assists, cards) and add any standout (see the standout triggers) to `prospects` with status "Watch".
4. **Provisional scores only, never final ones** (Andrew's rule 8D, 14 Nov 2026; replaces "never invent scout scores"). The system may draft `roleRadar` scores for a watchlist player when both are true: (a) FIFA's post-match report for that match gives his per-player data, copied to his `fifaData` field as one line per match; (b) he has video tags for the areas being scored. Any area at 8 or above needs at least two tags with `seen: "Clearly seen"`; otherwise leave that area "Not graded". Set `roleRadar.provisional: true`, never tick `approved`, and list each provisional player on the run's `APPROVAL NEEDED` line for Andrew's 22:30 review. Andrew's approval confirms the scores and clears `provisional`. Never tick `live` or `replay` for a match nobody watched, and never change scores a person entered.
5. **Report it**: the final message lists "Auto-covered matches still needing a viewing" and, from the second missed day, names the assistant shown in `scout` for each.

## Tag standard and nightly tag check (rule of 14 Nov 2026, taken from the FOOTPASS method)
Every tag in the `videos` collection answers who, what, when and where. When the system or a person writes a tag:
- **Who:** `player` (watchlist id). For a player not yet on the watchlist, leave `player` empty and set `nation` and `shirt`; the tracker links the tag automatically once a prospect with that nation and shirt number exists. Add a prospect's `shirt` whenever the squad list gives it.
- **When, the exact moment:** goal, shot: the frame the ball is struck · pass, key pass, assist, cross: the frame the ball leaves his foot · carry: his first touch after receiving · dribble: the moment he goes past the opponent · press: the moment his pressure forces the error · tackle, interception, block: his first touch on the ball · aerial duel: head-ball contact · save, claim or punch: the moment his hands touch the ball · distribution: the frame the ball leaves hands or foot · turnover: the moment possession is lost. Take the time from live play, never from a replay of the same moment.
- **Where:** `zone` on the xT grid (letter A to L across the pitch, number 1 to 16 towards the goal he attacks), for where the action starts.
- **Angle and clarity:** `angle` "Live" or "Replay"; `seen` "Clearly seen", "Partly seen" or "From context". System tags from match reports are "From context" unless the moment was viewed.
- **Action list** includes Block.

**Nightly tag check, every evening run before the 22:30 review.** Read the day's tags and check they make football sense in order: an assist needs a team-mate's goal within about 15 seconds of video in the same match; a key pass needs a team-mate's shot; the same player, action and match within 2 seconds is a double tag (keep the live-angle one); a tag that doesn't fit his role and side (a centre back's cross from the far flank, a goalkeeper's tackle in the opponent's half) gets a second look. Fix clear errors yourself and stamp them in the note; anything you cannot settle goes on the `APPROVAL NEEDED` line as "Tag check: [player, match, minute, what doesn't fit]".

**FIFA counts behind the moments.** After each match, copy each watchlist player's per-player data from FIFA's post-match report into his `fifaData` field (one line: match · minutes · the counts FIFA gives). Scout cards and private packs show rates from these counts beside the tagged moments, and action maps from tag zones.

**Agreement test (once, before 19 Nov, then each new assistant).** Two viewers tag the same 2025 U-17 World Cup match on FIFA+. A tag agrees when it names the same player and action within 2 seconds. Report the share that agree and the actions where they differ; tighten the exact-moment line for any action below 70%.

Also keep everything else current without waiting for anyone: kick-off times, venues, squads, standings lines on nation cards, knockout fixtures, the timeline phase, and public fact updates prepared for approval.

## Four Sentences first (Andrew's rule, 15 Nov 2026)
- Before writing or changing any page, card, invite, briefing or tracker text, read the Afritech Four Sentences (the afritech-four-sentences skill and memory file): who it's for, what they get, why they'd believe us, the one action.
- Every public page's first screen passes the stranger test: someone outside football can say who it's for and what to do next.
- When desk work shows a sharper way to say one of the four sentences for this desk's readers (participants, scouts, clubs), put it to Andrew as a lettered Gatekeeper question. Don't change the master yourself.
- Scheduled runs on reduced cadence (see the first section) still skip this; it applies whenever real work runs.
