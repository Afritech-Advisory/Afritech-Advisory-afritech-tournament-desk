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
