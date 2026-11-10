# Afritech Tournament Desk: plan

_Created 2026-11-10. Sister site to the Player CV Desk (`afritech-sports-cv-desk`)._

## 1. What it is
A live public website for each tournament Afritech covers. One folder per tournament (`qatar-u17-2026/`), listed on the root page. Built for clubs, agents and federations, read mostly on a phone.

## 2. Two products, kept apart
| Product | Where | Who sees it |
|---|---|---|
| Public tournament desk | This repo, GitHub Pages | Anyone with the link |
| Working scouting tracker (nations notes, watchlist ratings, match coverage, expected-threat log) | Private claude.ai artifact "U-17 Qatar Scouting Desk" | Afritech scouts only |

Afritech's assessment models, scoring methods, internal ratings, internal outcome lines and price information never go in this repo. The public site carries conclusions (verdict labels with a next step), public facts and the call to action only.

## 3. Rules for every page
- Sales-first customer voice: open with what the reader gains, end with the call-to-action ladder (book a call, request the private pack, engage Afritech).
- Client-safe language scan before every commit (afritech-client-safe-language banned terms, stage wording, internal decision language, medical detail).
- All U-17 players are minors: public-domain facts only, club signal no higher than MONITOR, every conversation through family and federation, no valuation or commercial terms.
- Contact block: Afritech only, Kenya +254 715 551 506 only, no `tel:` links, WhatsApp and both LinkedIn links.
- Works with scripts off; light and dark; no horizontal scroll at 390px.
- Every page shows "Updated <date>"; re-check squads, groups and fixtures on each update.

## 4. Update cadence during Qatar 2026
| When | Update |
|---|---|
| Squad announcements (to 18 Nov) | Squad status pills, coaches, Mozambique and Uganda groups |
| FIFA publishes the schedule | Kick-off times in the match centre |
| Daily, 19 to 27 Nov | Board additions (top scorers, standout goalkeepers, captains, decisive performers) |
| After each round | Scout cards linked from the board |
| After 13 Dec | Tournament review and talent report teaser |

## 5. Open items
1. ~~Repo and Pages.~~ Live 2026-11-10 at https://afritech-advisory.github.io/Afritech-Advisory-afritech-tournament-desk/ (repo kept under its created name).
2. Confirm Mozambique's and Uganda's groups (B or C) on FIFA's group page.
3. Add kick-off times when FIFA publishes them.
4. Confirm whether Seb Fisher is in Uganda's final 21.
5. Player photos: none used. Add only verified photos Afritech may publish.

## 6. Player radars (added 2026-11-10)
- Public page: `qatar-u17-2026/radars/`, built from `src/data/qatar-u17-2026-radars.json` by `build.py` (static SVG, works with scripts off; role filter is an optional script).
- Each player is shown against the **role average only**. The public data file holds only approved players and pre-computed role averages with a count. No individual peer score is ever published.
- Source of scores: the private tracker's "Tournament role radar" (eight areas per role, matches and minutes watched, "Approved by Afritech" tick). After each matchday Claude reads the approved entries, computes role averages from all rated players in each role, updates the JSON, rebuilds and publishes.
- A role average appears once 3 players in that role are rated. Under-18 safeguards: club signal stays MONITOR; footer states FIFA minors rules.

## 7. Photos
- Use a player photo only with a recorded permission basis in the tracker: supplied by the player or family with consent, a federation or club media release whose terms allow our use, a licensed agency photo, or our own photo taken with consent. A photo appearing in public media is not permission.
