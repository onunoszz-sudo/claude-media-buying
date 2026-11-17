---
name: learnings-log
description: Turns the week's results (reviews, tests, negatives, diagnoses) into short rules for an ad account, with evidence, data volume and confidence, writes them to learnings.md and flags when a new rule contradicts an old one. Can also roll up patterns across a portfolio of similar accounts. Use when the user says "log the learning", "update learnings", "what did we learn this week", "learnings log", "cross-account patterns", or at the end of a review or weekly report.
---

# Learnings log

After a month of logs the agent knows the account better than a new hire. Without one, every week
starts from zero and the same mistake gets paid for twice.

## Input
The week's results: output of `meta-review`, `ad-diagnosis`, `search-terms`, `google-ads-health`,
`weekly-report`, or what the user tells you. Read the account's current `learnings.md`
(`**/accounts/<slug>/`).

## How to write a rule
One sentence that guides a future decision, specific to the account:
- "Social proof ads run at 2.4 ROAS and discount ads at 0.6 in this account."
- "Searches containing 'cheap' never converted in 90 days."
- "Package ads (room + breakfast) beat room-only ads on cost per booking for weekend stays."

For each rule record:
| Field | Content |
|---|---|
| Date | YYYY-MM-DD |
| Rule | the sentence |
| Platform | Meta, Google, funnel, follow-up |
| Evidence | the numbers behind it, with the period |
| Data volume | spend and conversions behind it |
| Confidence | **low** (one week, few conversions), **medium** (2 to 4 weeks or one clean test), **high** (repeated across tests or more than a month) |
| Status | active, testing, SUPERSEDED on YYYY-MM-DD by <new rule> |

Not a rule: one day, one ad with a handful of conversions, an opinion with no number. Those can go
in as "testing" hypotheses.

## Contradictions
Before writing, compare each new rule with the active ones. If it contradicts one:
1. show both side by side, with evidence and volume;
2. **ask the user** which one stays;
3. the loser is not deleted: its status becomes SUPERSEDED with the date.

## Portfolio patterns (optional)
With several accounts of the same kind (e.g. ten hotels), read every `learnings.md` and list rules
that hold in three or more accounts, rules that hold for one segment only (resort vs. boutique,
city vs. leisure), and rules that contradict each other between accounts. Portfolio patterns are
suggestions to test in each account, never rules copied in without a test.

## Output
1. Proposed rules as a table, ready to write.
2. Contradictions found, with the question.
3. After the user's ok: write to `learnings.md` and say how many active rules the account has per platform.

## Guardrails
- Write only after showing the rules and getting a confirmation.
- Never invent evidence; a rule with no number stays as "testing".
- High confidence requires repetition. When in doubt, medium.
