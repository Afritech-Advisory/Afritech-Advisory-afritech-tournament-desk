# Working rules for Claude on Afritech projects

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
4. **Never invent scout scores.** `ratings` and `roleRadar` scores come only from a person who watched the full match; leave them untouched. Never tick `live` or `replay` for a match nobody watched.
5. **Report it**: the final message lists "Auto-covered matches still needing a viewing" and, from the second missed day, names the assistant shown in `scout` for each.
Also keep everything else current without waiting for anyone: kick-off times, venues, squads, standings lines on nation cards, knockout fixtures, the timeline phase, and public fact updates prepared for approval.
