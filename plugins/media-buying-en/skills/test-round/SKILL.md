---
name: test-round
description: Plans an account's next creative test round - how many ads the budget can judge (from the KILL line), which angles and hooks go in, ABO or CBO structure, and for every ad the hypothesis, deciding metric, read window and the decision agreed in advance - and records it in tests.md. Use when the user says "next test round", "plan the new creatives", "how many ads should I test", "angle test", "launch new creatives", "test plan".
---

# Test round

A test without a decision written beforehand turns into an argument afterwards, and a round bigger
than the budget leaves ads without enough spend to be judged. This skill sizes the round to the
budget and writes down, before launch, what each ad has to show and what happens in each case.

## Before you start
1. Find the account folder (`**/accounts/<slug>/`). Read `numbers.md` (KILL line, target CPA),
   `rules.md`, `brand.md`, `winners.md`, `learnings.md` and `tests.md` if it exists. No
   `numbers.md`: stop and run `account-numbers`.
2. Ask or read: daily budget for the test, start date, read window (default 7 days) and the
   creatives or ideas (angles and hooks) the user has.
3. Check what is being tested now (`tests.md` and the account): do not stack two tests that touch
   the same thing (new creative + new landing page + new price at once muddies the read). If they
   conflict, say so and propose the order.

## 1. Size from the budget
Run `scripts/calc_rodada.py --daily-budget B --days D --kill-line K [--ad-sets N] [--currency X] --lang en`.
The math: daily budget x window days ÷ KILL line, rounded down. Show the math.
- If a full angle does not fit (default 3 hooks), test **1 hook per angle** and keep hook variations
  for the winner (`winner-multiplier`).
- If no ad fits, say what has to change (window or budget) and stop.
- More ideas than ads: pick using `learnings.md` and what has never been tested; the rest goes to
  the queue in `tests.md`.

## 2. Structure
- **ABO (ad set budget)** when every angle needs the same chance: one ad set per angle, equal budget.
  Inside one ad set with several ads, Meta concentrates delivery on one.
- **CBO (campaign budget)** when the goal is to let Meta find the winner among already approved ads;
  accept that some will not spend.
- Same audience and placements across the test's ad sets: the creative is the only difference.
- Write the plan into the account's `launch-plan.md` and run `launch-qa` before launch.

## 3. Each ad
| Field | How to write it |
|---|---|
| Name | `trigger / angle / H#` (becomes `utm_content`); e.g. `fear-pain / prepared-body / H1` |
| Hypothesis | "If we show X to people who feel Y, they click/buy because Z", tied to evidence (a learning, a comment, a review, an ad that already ran) |
| Deciding metric | one only, from the stage the test touches: a new hook is judged on hook rate; a new angle on cost per checkout or CPA |
| Window | read date and minimum spend (the KILL line) |
| Agreed decision | "if by DATE it spends the line with no sale: pause; if CPA at target with the minimum sales: winner, goes to `winner-multiplier`; in between: one more window" |

Use the thresholds in `numbers.md` and `rules.md`. A number that is not there does not go into the
decision: write MISSING and ask.

## Output
No em dashes.

1. **One line:** how many ads, in how many ad sets, from when to when, what it costs.
2. **The sizing math** (script output).
3. **Round table:** name, angle, hook, creative (file), hypothesis, metric, window, decision.
4. **Ads Manager structure:** campaign, ad sets, budget, audience, placements.
5. **Queue:** ideas that did not fit, in the order they go in.
6. **Conflicts** with running tests, if any.

Record the round in `tests.md` in the account folder (one section per round, dated), so
`meta-review` reads the agreed decision and `learnings-log` records the result.

## Guardrails
- The round does not launch without the user's "yes"; launching and activating is a separate action.
- Never more ads than the budget can judge.
- A decision written beforehand does not change after seeing the result, unless the reason is recorded.
- A creative that conflicts with `brand.md` stays out, unless the account owner accepted that claim
  and it is recorded there.
- Never invent a number.
