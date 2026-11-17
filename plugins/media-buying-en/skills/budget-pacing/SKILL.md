---
name: budget-pacing
description: Tracks spend pace for one or many ad accounts against the monthly (or flight) budget - pace, end-of-period projection, recommended daily budget and status ON PACE, UNDER, OVER or OVERSPEND, with corrections split into steps of up to 20%. Use when the user says "pacing", "budget pacing", "MTD spend", "are we going to overspend", "underspending", "client budget", "land the month on budget", or runs the Friday review.
---

# Budget pacing

At an agency, spending the contracted budget (no more, no less) is a daily obligation.
Underspending leaves results on the table and makes the client ask what the fee is for;
overspending becomes a refund conversation. This skill reads the whole portfolio and returns the
corrections, largest dollar variance first.

## Data
One row per account and platform, in a CSV (header in English or Portuguese):

| Column | Meaning |
|---|---|
| `account` | account or client name |
| `platform` | Google Ads, Meta... |
| `budget` | budget for the period |
| `spend_to_date` | spend **through yesterday** (complete days) |
| `start`, `end` | flight dates, YYYY-MM-DD, inclusive |
| `current_daily` | optional: daily budget set today (otherwise the average run rate) |
| `planned_to_date` | optional: planned spend through yesterday, for a seasonal curve (otherwise linear) |

Where to get it:
- **Google Ads MCP connected:** per account, `SELECT campaign.name, campaign_budget.amount_micros,
  metrics.cost_micros FROM campaign WHERE segments.date DURING THIS_MONTH AND campaign.status = 'ENABLED'`
  (micros ÷ 1,000,000; current daily = sum of `amount_micros` of live campaigns). Today is excluded:
  sum through yesterday only.
- **Official Meta connector:** month-to-date spend through yesterday at account level and the daily
  budgets of live campaigns/ad sets.
- **No connector:** platform exports or the agency's budget tracker.
- **Contracted budget:** from each account's `rules.md` (`**/accounts/<slug>/`). If it is not there,
  it is MISSING: ask, never assume.

## Run
```bash
python scripts/calc_pacing.py portfolio.csv --as-of YYYY-MM-DD --lang en --currency $
```
The script is in `scripts/` next to this file, with `example-portfolio.csv` (10 fictional hotels).

## Reading the statuses
- **ON PACE:** end-of-period projection within ±10% of budget. Hold; the script shows the exact
  daily to land on budget as an optional fine-tune.
- **UNDER:** projection more than 10% below budget. Raise the daily in steps of up to 20%, 48 h
  apart. A correction above 50% is a **client or account lead decision** (the account may lack
  demand or creative to absorb the budget; flag it instead of forcing it). If 20% steps can't get
  there before the flight ends, raise what you can and flag the underspend early.
- **OVER:** projection more than 10% above budget; the script shows the date the money runs out.
  Lower the daily. Cuts don't need the 20% step rule, but a big cut on an ad set that is selling
  well deserves a conversation with the client about raising the budget.
- **OVERSPEND:** the flight budget is already spent. Pause or ask the client for more budget, today.

Before recommending more spend, check `numbers.md`: raising budget on an account below break-even
(or above max cost of sale) just to "spend the contract" burns the client's money. Then the
recommendation is a client conversation, not a budget increase.

**Hotels:** pacing follows demand. Front-load or hold back around high-demand dates, events and
low-occupancy periods with the client's revenue manager, and put that curve in `planned_to_date`
instead of pacing linearly.

## Output
1. The script's table (all accounts, largest dollar variance first).
2. The numbered actions to approve.
3. The platform reminders (daily budget is not an exact cap: Google can spend up to 2x daily on a
   day and bills at most 30.4x average daily per month; Meta can spend up to 75% over daily on a day,
   at most 7x daily per week).
4. For accounts UNDER because of delivery, one line of likely cause (bids, narrow audience,
   disapproved creative, account spending limit) to check with `google-ads-health` or `meta-review`.

## Guardrails
- No change without a "yes" per action.
- Increases in steps of up to 20%, one every 48 h per campaign or ad set.
- Today's spend is excluded: the day is incomplete.
- Never invent a contracted budget; without it the account is left out and shown as MISSING.
