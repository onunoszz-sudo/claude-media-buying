---
name: angle-map
description: Builds an account's angle map - the angle x person x format grid from customers' own words (comments, quiz answers, messages, reviews), marks what was already tested and how it did, points to the empty cells with the most evidence and writes hooks for them, each one run through a policy check (personal attributes, health claims, promises) before production. Use when the user says "angle map", "new angles", "trigger research", "what creative to test", "ad ideas", "new hooks for the account", "check these hooks for policy".
---

# Angle map

New creative that comes from the ad maker's head tends to repeat what is already running. This skill
starts from what customers say in their own words, arranges it in a grid and shows where there is
no ad yet. The result feeds `test-round`.

## Before you start
1. Find the account folder (`**/accounts/<slug>/`). Read `brand.md` (what can't be said),
   `winners.md`, `learnings.md` and `tests.md`.
2. Collect **real words** (the more sources the better), noting where each line came from:
   - comments on the ads and the profile;
   - open answers from the quiz or lead form;
   - support, WhatsApp and email messages;
   - reviews and testimonials already approved for use;
   - Google search terms (what people actually type).
3. List the ads that already ran with the angle, person and format of each, and the result (real
   sales when available, otherwise the stage metric).

With no real words at all, say so and stop: a map made only of guesses isn't worth a round.

## 1. The three columns
- **Angle:** the reason the person acts. Types: pain (what hurts today), fear (what might happen),
  desire (what they want to feel or have), objection (why they wouldn't buy) and identity (who they
  are or want to be).
- **Person:** who speaks or who is targeted, by situation rather than demographics (e.g. "first
  baby, third trimester" instead of "women 25-34").
- **Format:** UGC/testimonial, expert talking, demo, animation/mini-series, proof-led static, carousel.

Two ads share an angle when the reason to buy is the same, even in different words. Changing only
the face or the colors doesn't make a new angle.

## 2. The grid
1. Group the real lines by angle and count them (that's the strength of evidence).
2. Cross angle x person. In each cell: the ads that already ran there, their format and result
   (WINNER, LOSER, NO SPEND, UNTESTED).
3. Mark the **empty cells with the most evidence**: many customers talk about it and no ad does.
   These are the first candidates.
4. A tested losing cell comes back only in a different format, with a written reason.

## 3. Hooks for the top 3 cells
For each chosen cell:
- 3 real lines that support the angle (anonymized, no names or personal data);
- 5 hooks of up to 3 spoken seconds or 8 written words, each with a suggested format;
- the hypothesis in one line: "if we show X to people who feel Y, they click because Z".

## 4. Policy check (every hook, before production)
Mark each hook OK, REWRITE or BLOCKED:
| Risk | What goes wrong | How to rewrite |
|---|---|---|
| Personal attribute | stating or asking about the viewer's condition ("are you overweight?", "your anxiety...") | talk about the situation, or a character in the third person |
| Health claim or guaranteed result | "cure", "pain-free", "lose X lb in Y days" | describe what the product teaches or does, without promising an outcome |
| Before/after, body focus | body comparisons, close-ups of body parts | show the routine or the whole person |
| Forbidden by the account | anything in `brand.md` | follow `brand.md` |
| Rejection history | a line or image close to an ad Meta already rejected | use the rejection line recorded in `brand.md` |

BLOCKED hooks don't appear in the final list. Show the rewritten version next to each REWRITE.

## Output
Plain words, no em dashes.
1. **One line:** how many real lines, from how many sources, how many empty cells with evidence.
2. **The grid** (angle x person) with each cell's status.
3. **The 3 cells to test now**, with evidence, hypothesis and the 5 checked hooks.
4. **Queue:** the next cells, by strength of evidence.

Save the map as `angles.md` in the account folder (update it every round) and hand the 3 cells to
`test-round`.

## Guardrails
- Never invent a customer line or a testimonial. A line without a source stays out.
- Never copy a competitor's ad: competitors show which angles exist, not the words to use.
- No customer personal data goes into the map.
- The policy check lowers the risk of rejection but doesn't guarantee approval: the final call is
  Meta's and the account owner's.
