---
name: account-numbers
description: Onboards an ad account (or reviews one) by building its context files and computing the numbers every other decision depends on - break-even ROAS, target ROAS and CPA, target MER, CPL and cost per MQL, and for hotels the max cost of sale against the OTA commission, net of cancellations. Use when the user says "account numbers", "break-even", "what's my target ROAS", "onboard a new account", "new client", "hotel economics", "cost of sale", or when another media buying skill can't find the account's numbers.md.
---

# Account numbers

No other skill in this pack labels an ad without these numbers. A 3x ROAS is a great week for
one account and a slow loss for another: it depends on margin, and for a hotel on what the OTA
would have charged for the same booking. This skill interviews the user, does the math in the
open and writes the account's context files.

## Where account context lives
Each account has a folder `accounts/<account-slug>/` inside the user's project (for example
`clients/harbor-view-inn/accounts/harbor-view-inn/` or simply `accounts/harbor-view-inn/`). Glob
for `**/accounts/*/numbers.md`. If there is none, ask where to create it. Templates for the six
files are in `templates/` next to this file:

| File | What goes in it |
|---|---|
| `numbers.md` | funnel type, source of truth, decision numbers, label thresholds, contracted budget |
| `brand.md` | what it sells, to whom, voice, allowed and forbidden claims, rate parity rules |
| `offers.md` | offers, room types or products, price, margin, seasonality |
| `winners.md` | best ads with numbers and a hypothesis |
| `rules.md` | approvals, budget steps, what the agent may do on each platform |
| `learnings.md` | starts empty; `learnings-log` fills it |

## Step 1: funnel type
- **direct-sale:** the ad leads to a purchase in the same session (ecommerce, delivery). Judge on
  ROAS/MER against real revenue.
- **low-ticket:** a cheap info product with bumps and upsells. Judge on front-end CPA and ROAS on
  the effective order value.
- **lead-crm:** the ad produces a lead and a human closes the sale later. Judge on CPL and cost
  per MQL/quote short term, revenue per ad dollar over a long window.
- **hotel:** the booking happens on the hotel's own booking engine. Judge on **cost of sale**
  (ad spend ÷ realized revenue) against the OTA commission, net of cancellations, keeping booking
  date and stay date apart.

## Step 2: interview, one question at a time
Wait for each answer. Record **where each number came from** (PMS export, P&L, client email,
estimate). An estimate stays labeled as one.

All types:
1. Source of truth for revenue (booking engine/PMS, Shopify, payment platform, CRM). Never the pixel.
2. Contribution margin: revenue minus cost of goods, payment fees, taxes, shipping, commissions.
   If the user gives a **net** margin (after fixed costs), say it is a different number and ask
   for contribution margin.
3. Target profit after ads, as % of revenue.
4. Contracted monthly budget and platform split.

Low-ticket only: front-end, bump and upsell prices with 30-day take rates; **net-to-gross** from a
real payout statement (net received ÷ gross price, never a fee rate from memory); refund rate.

Lead-crm only: average closed deal value; 90-day lead → MQL → quote → sale rates (use the real
sales sheet if the CRM is not reliable, and say so in the file).

Hotel only:
- ADR and average length of stay (nights per booking), last 90 days, from the booking engine or PMS.
- Cancellation rate of direct bookings.
- **OTA commission from the hotel's actual contract** (15% to 25% is common, but use the contract).
  It is the ceiling on cost of sale: above it, a direct booking costs more than the same booking
  through Booking.com or Expedia.
- Target cost of sale agreed with the hotel (below the commission).
- Optional: contribution margin per room night and target profit, for the margin lens.
- Split **brand vs. non-brand**: a search for the hotel's own name is often a guest who would book
  direct anyway. The OTA lens applies to non-brand and to the share of brand traffic the OTAs bid on.

## Step 3: compute without arithmetic mistakes
Run this skill's script and paste the output into `numbers.md`:

```bash
python scripts/calc_numeros.py direct-sale --lang en --ticket 150 --margin 0.40 --profit 0.10
python scripts/calc_numeros.py low-ticket --lang en --front 14.90 --item 7.90:0.10 --item 19.90:0.03 --net-to-gross 0.90 --refund 0.05 --profit 0.20
python scripts/calc_numeros.py lead-crm --lang en --ticket 9000 --margin 0.45 --profit 0.15 --lead-to-sale 0.0125 --lead-to-mql 0.25 --lead-to-quote 0.075
python scripts/calc_numeros.py hotel --lang en --adr 220 --nights 2.6 --cancellation 0.18 --ota-commission 0.18 --target-cos 0.12 --margin 0.70 --profit 0.25
```

Formulas, for checking:
- Break-even ROAS = 1 ÷ margin; target ROAS = target MER = 1 ÷ (margin − target profit)
- Max CPA = order value × margin; target CPA = order value × (margin − target profit)
- Low-ticket: effective order value = front + Σ(price × take rate) over the funnel;
  margin = net-to-gross × (1 − refunds) − other costs
- Lead-crm: target CPL = target CPA × lead-to-sale; target cost per MQL = target CPA ×
  (lead-to-sale ÷ lead-to-MQL)
- Hotel: booking value = ADR × nights; realized revenue = booking value × (1 − cancellations);
  max CPA per booking = realized revenue × OTA commission; target CPA = realized × target COS.
  **In-platform ROAS** (what Google and Meta report, on booked revenue before cancellations)
  = 1 ÷ (COS × (1 − cancellations)). Compare platform ROAS with that number, not with 1 ÷ COS.

If target profit ≥ margin, or target COS ≥ OTA commission, the script stops and says why.

New offer with no take rates yet: compute **two scenarios** (front only; funnel at stated
hypothetical rates), write which one the labels use for now and what will settle it. A take rate
of zero across 3+ sales: open the checkout (read only) and confirm the bumps and upsell flow are
actually configured before treating it as buyer behavior.

## Step 4: an honest read
Compare with the account's real last 30 to 90 days, if available:
- Below break-even (or above max cost of sale): **do not recommend more budget.** The problem is
  offer, price, page, booking engine or post-click before it is the ad. Say where to look first.
- Between target and max: hold and optimize.
- Better than target: ready for budget steps of up to 20%.
- Low volume (hotels, high-ticket): most ads will sit in WATCH; the judging window must be longer.

## Step 5: write the files
Create or update the six files from the templates with only what the user confirmed. Everything
else is `MISSING: <what and where to get it>`. Finish with the list of what is still missing.

Also create an empty `changelog.md` (template in `templates/changelog.md`): from now on every change
to the funnel or the campaigns gets a line there the same day, and the other skills read it.

## Rules
- Never invent a number. Missing data is MISSING; odd data is flagged before use.
- Show the math for every decision number.
- Currency: if revenue and spend are in different currencies, state the rate used and its date.
