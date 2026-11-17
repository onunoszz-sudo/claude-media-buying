---
name: winner-multiplier
description: Takes a winning ad (or a near winner) and multiplies it - explains why it won stage by stage, separates what must not change, plans one-variable variations with the original as control, rewrites the script in blocks (hook, story, close) with a mix-and-match grid, rescues the hook when only the hook is weak, and writes RSA headlines and descriptions for Google. Use when the user says "multiply this winner", "variations of the ad that sells", "new hooks", "the hook is weak", "rescue this ad", "script in blocks", "ad is fatiguing, what now", "RSA headlines from the winner".
---

# Winner multiplier

A winner is the cheapest asset in the account: it already proved the angle works. Instead of
looking for the next one from scratch, this skill finds what works in it, protects that and changes
one thing at a time. It also rescues an ad when only the opening is weak.

## Before you start
1. Find the account folder (`**/accounts/<slug>/`). Read `numbers.md`, `brand.md`, `winners.md`,
   `learnings.md` and `tests.md`.
2. Ad data, from the official Meta Ads connector or an export: spend, impressions, 3-second (or
   2-second continuous) plays, 25/50/75/100% video views, ThruPlays, link clicks, landing page views,
   checkouts, purchases, frequency; and the same numbers as the **account average** for the same
   format. The ad's primary text and headline.
3. **The creative's content:** script, transcript or the video file. Without knowing what the ad says
   and shows there is no way to explain why it won: ask before going on.
4. Confirm it is a winner by the criteria in `numbers.md`. If not yet (few sales), call it a "near
   winner" and treat the variations as a test, not as scaling.

## 1. Why it won
Read the ad stage by stage against the account average (same format):
| Stage | Math | Read |
|---|---|---|
| Hook | 3-second plays ÷ impressions | do the first seconds stop the scroll? |
| Hold | 25%, 50%, ThruPlays ÷ 3-second plays | does the story hold? where does the curve drop? |
| Click | link CTR | does the close make people want more? |
| Post-click | LPV ÷ click, checkout ÷ LPV, purchase ÷ checkout | are the clickers the right people? |

Then list, with evidence, **the 3 things the ad does** (e.g. opens on today's pain, shows the product
before 5 s, ends with an invitation to the quiz). Those do not change.

## 2. One-variable variations
Each variation changes **one** thing; the original stays live as the control. Order, cheapest first:
1. **Hook** (first 3 to 5 s: line, on-screen text, first image). With an AI avatar or existing
   footage, it is just a new generation or a new cut of the opening.
2. **Primary text and headline** (the video stays).
3. **Close** (final call to action, what happens after the click).
4. **Format** (the same script as a static, carousel or shorter video).
5. **Who speaks or where** (another setting, another person): only after 1 to 4 are tested.

Each variation gets a `trigger / angle / H#` name and an agreed decision, in the `test-round` format
(which sizes how many fit the budget).

## 3. Script in blocks
Rewrite the winner in blocks that fit together:
- **Hooks (H1, H2, H3):** 3 to 5 s each, different openings (question, surprising statement, scene of
  the problem, true number, line from someone who feels it), each with on-screen text, because many
  people watch muted.
- **Story (S1):** the winner's body, unchanged.
- **Closes (C1, C2):** the current call to action and an alternative.

Grid: H1+S1+C1, H2+S1+C1, H3+S1+C1 first (only the hook changes); closes after. With AI avatar video,
each hook is a short generation joined to the existing body; with filming, the blocks are shot
separately for the editor to combine.

## 4. Hook rescue
When **only** the hook is weak (3-second plays ÷ impressions below the account average while hold,
click and post-click are at or above average), do not remake the ad: write 3 new hooks for the same
body and test them as in section 2. If more than one stage is weak, it is not the hook: use
`ad-diagnosis`.

## 5. For Google (RSA)
From the winner, write up to 15 headlines (up to 30 characters) and 4 descriptions (up to 90): the
pain, the claim allowed in `brand.md`, the proof, the invitation. Count the characters. One idea per
headline, without repeating the keyword in all of them.

## Output
No em dashes; copy that goes live stays in the ad's language.

1. **Why it won:** stage table against the average, and the 3 things that do not change.
2. **Variations:** table with name, what changes, what stays, hypothesis, agreed decision.
3. **Script in blocks:** H1 to H3 (line + on-screen text + image), S1, C1 and C2, and the grid.
4. **RSA headlines and descriptions**, if the account runs Google.
5. **What to ask the producer for:** files, avatar generations or cuts needed.

Record the variations in `tests.md` and the reason for the win in `winners.md`.

## Guardrails
- Nothing launches without a "yes"; creating and activating ads is a separate action.
- One variable per variation; the original stays as the control.
- No claim, number, credential or testimonial that `brand.md` forbids; what the account owner
  accepted and recorded there can be used.
- A number in a hook only if it is true and sourced.
- Never invent a metric; anything missing shows as MISSING.
