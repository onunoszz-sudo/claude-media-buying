---
name: tracking-check
description: Checks whether the Meta pixel counts the right sales - compares, day by day, the purchase events received (browser and server), the purchases attributed in Ads Manager and the real sales in the source of truth (Hotmart, store, booking engine, CRM), finds double counts, purchases with no value and missing sales, and says whether ads can be judged. Read-only. Use when the user says "tracking check", "is the pixel counting right?", "extra purchases in the pixel", "pixel vs store orders", "check tracking", or when the Meta review flags a gap above 20%.
---

# Tracking check

Every verdict in this pack (KILL, SCALE, CPA, ROAS) comes from the pixel. If it counts sales that
don't exist, a bad ad looks good and gets budget; if it misses sales, a good ad gets paused. Meta
also learns who buys from the events it receives, so a wrong count teaches it the wrong audience.
This skill measures the count before any verdict. It is **read-only**: fixing it is the account
owner's job.

**When to run it:** the first time an account joins the pack; once a month; the same day as any
change to checkout, upsell funnel, tag manager, pixel or consent banner; and whenever `meta-review`
or `daily-brief` flag the pixel and the source of truth more than 20% apart.

## Before you start
1. Find the account folder (`**/accounts/<slug>/`) and read `numbers.md`: what the source of truth
   for sales is and what each sale sends to the pixel (gross or net; main product, bump, upsell).
2. Period: the last **14 full days** (not today). Under 7 days is not enough.
3. Ad account ID and dataset (pixel) ID. Without the pixel ID, list the account's datasets through
   the connector.

## Collect (read tools only)
1. **Real sales by day** from the source of truth: count and value, split into main product, bump
   and upsell, approved or completed sales only. **Never** read, copy or show customer names,
   emails, phone numbers or IDs: counts and values only.
2. **Attributed purchases by day** in Ads Manager, account level, `time_increment` "1": pixel
   purchases and purchase value. Also read the `attribution_setting` of the active ad sets.
3. **Events received by the pixel** (dataset stats, 28 days max, Unix timestamps): Purchase by day
   from browser only and server only; and Purchase grouped by URL (which page each event comes from).
4. **Pixel health:** quality per event (match score and keys sent) and dataset details (active, last
   browser and server fire, automatic matching).
5. **Time zones:** dataset stats come in Pacific time; Ads Manager in the account's time zone; the
   source of truth in its own. A gap that disappears in the weekly total is a time zone, not an error.

## Calculate
Build a CSV with one row per day (`date, real, attributed, attributed_value, real_value, raw_web,
raw_server`) and run:
`python scripts/calc_rastreamento.py days.csv --lowest-value <lowest value a sale sends to the pixel> --currency $ --lang en`
Show the output. The script gives the match rate (attributed ÷ real), extra purchases with no
value, events received per sale and the verdict.

## What to check
| Check | How to read it | Problem when |
|---|---|---|
| Match rate | attributed ÷ real sales, over the whole period | above 105%: counts what doesn't exist or counts twice; below 80%: missing sales; a 20-point drop week over week |
| Extra purchases with no value | a day with more attributed purchases than sales while the value matches the real value | any: something fires Purchase without a sale (funnel page, reload, payment status) |
| Received per sale | browser + server events ÷ real sales | about 2 is normal (both send, Meta deduplicates); above 3, the server sends more than one event per sale or other pages fire Purchase |
| Where it comes from | Purchase by URL | Purchase from a page that isn't the order confirmation (quiz, upsell, own thank-you page) |
| Server coverage | server events ÷ browser events | under 75%: sales blocked in the browser go unrecorded |
| Value and currency | attributed value ÷ real value | gap above 10%, wrong currency, or gross one day and net the next |
| Attribution setting | `attribution_setting` of the ad sets | ad sets on different windows can't be compared on CPA |
| Match score | Purchase quality | no score or under 6: note it; fix only after double counts and missing sales |
| Custom events | the pixel's event list | tag manager sending every site event to the pixel: just noise, but confirm none is named Purchase |
| Health restriction | the dataset Overview in Events Manager | health, pregnancy or wellness products may land in a category with data limits; the connector doesn't show it: ask the user for a screenshot |
| Test order | one real refunded order (or test mode) per main payment method | not exactly one Purchase with the right value |

**Patterns seen in low-ticket with Hotmart:**
- Bumps and upsells reach the pixel as separate Purchases. Compare against transactions, not orders.
- Hotmart sends the net value (e.g. about US$ 8.80 for a US$ 9.90 product).
- After an upsell funnel went live, extra attributed purchases with no value have shown up (about
  1 in 10). Suspect: the funnel widget on the offer pages. Confirm with a test
  order before changing anything.

## Output
Plain words.
1. **One-line verdict:** "Safe to judge ads: yes / with a caveat / no", with the match rate.
2. **Daily table** (script output) and totals.
3. **Findings** from the table above, most expensive first. For each one: the number that shows it
   and the effect on CPA (e.g. a 116% match makes the pixel CPA look 14% lower than the real one).
4. **First fix**, step by step, and who does it (account owner, platform, developer). Then run this
   skill again.
5. **What wasn't checked** and why (data the connector doesn't return, a missing screenshot).

Save it as `tracking-YYYY-MM-DD.md` in the account folder and update the baseline in `numbers.md`:
match rate, purchases with no value and date. While the verdict is "no", the other skills use the
source of truth, not the pixel, and say so at the top.

## Guardrails
- Read-only. No write tool, on the pixel or the account.
- No customer personal data: counts and values only.
- Never invent a number: what the connector or the source of truth didn't return is MISSING.
- One fix at a time: change two things in tracking and you can't tell which one worked.
