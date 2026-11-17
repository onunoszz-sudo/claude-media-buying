---
name: daily-brief
description: Morning brief across one or many ad accounts - reads Meta Ads, Google Ads, budget pacing and each account's source of truth for revenue, and returns at most 5 things per account that need the user today, most expensive first, plus the number of the day (spend, revenue, MER or cost of sale vs. target). Use when the user says "daily brief", "morning brief", "what needs me today", "how are my accounts", "portfolio check", "anything on fire".
---

# Daily brief

Instead of opening twenty dashboards, one short answer: what needs a decision today, ranked by
what it costs to ignore. About ten minutes of the user's time. Changes nothing.

## Which accounts
If the user doesn't say, glob for `**/accounts/*/numbers.md` and ask whether to run all of them.
With several accounts, open with a **portfolio line** (accounts on fire / accounts fine), then one
block per account, starting with the most expensive problem in the whole portfolio.

## Data (per account)
1. **Meta:** yesterday and last 7 days through the official connector if it is in this session;
   otherwise the latest export the user shares.
2. **Google Ads:** through the Google Ads MCP (`search` tool) if connected, otherwise the latest CSV
   or the browser. **State the date of the data.** Data older than 7 days is flagged as stale.
   Yesterday by campaign:
   ```sql
   SELECT campaign.name, campaign.status, metrics.cost_micros, metrics.conversions,
          metrics.conversions_value, metrics.search_budget_lost_impression_share
   FROM campaign WHERE segments.date DURING YESTERDAY AND campaign.status = 'ENABLED'
   ```
3. **Source of truth** (from `numbers.md`): booking engine/PMS, Shopify, payment platform, CRM. If
   unreachable, use the pixel and write "pixel revenue, unconfirmed".
4. **Pacing:** month-to-date spend vs. contracted budget (`budget-pacing` logic): only flag accounts
   whose projection is more than 10% off.

## What to look for
- **Meta:** ad 50%+ over target CPA for 3 days; ad spending with no conversion past 2x target CPA;
  ad ready to SCALE; fatigue (frequency up, CTR down).
- **Google:** search terms spending with no conversions; profitable campaign limited by budget;
  CPC or spend jump; disapproved ad or keyword; broken final URL.
- **Funnel:** sudden drop in page, quiz, booking engine or checkout conversion; for lead-crm,
  yesterday's leads with no first contact.
- **Hotels:** booking engine errors or no bookings on a normally busy day, rate parity issue,
  sold-out dates still being advertised, brand campaign losing impression share to OTAs.
- **Creative:** best ads aging with no variation briefed.
- **Tracking:** pixel vs. source of truth more than 20% apart (action: run `tracking-check`).
- **Pacing:** projected to over- or under-spend the contracted budget by more than 10%.

## Output
Under 200 words per account, no em dashes.

```
<ACCOUNT> · <date>
Number of the day: spend yesterday $X · revenue $Y (source) · MER Z (target A) · 7 days: MER W
Pacing: <on pace | under/over by $N projected>

Needs you today:
1. [Meta] <what's wrong in one line> · <numbers> · Action: <one action>
2. ...
(at most 5, most expensive first; if nothing needs the user, say so)

Protect: <one thing that's working and should not be touched>
```

End by asking which numbered actions the user approves. For approved items that need deeper work,
call the right skill (`meta-review`, `ad-diagnosis`, `search-terms`, `google-ads-health`,
`budget-pacing`).

## Guardrails
- Read-only. No change without a "yes" per action.
- Low volume: no winner or loser with fewer conversions than the minimum in `rules.md`; say
  "still in WATCH".
- Never invent a number. Missing data shows as MISSING.
- As a scheduled task the brief takes no action at all: it only writes the text (and saves it to a
  file if asked).
