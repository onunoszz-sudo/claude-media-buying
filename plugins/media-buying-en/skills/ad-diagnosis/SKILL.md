---
name: ad-diagnosis
description: Diagnoses an ad or campaign that is underperforming (or doing suspiciously well) by reading it as its own funnel from the first second to the sale, including post-click steps (quiz, booking engine, checkout, lead in the CRM), and rebriefs only the weak stage. Also investigates a "bad day" when sales or bookings suddenly drop. Use when the user says "why isn't this ad working", "diagnose this creative", "where is it leaking", "bookings dropped yesterday", "bad day", "rebrief".
---

# Ad diagnosis

An ad is rarely bad everywhere. Usually one stage leaks and the rest is healthy, and rebuilding
the whole ad throws away what worked. This skill finds the stage and rewrites only that. If every
stage is weak, it confirms a real flop.

## Before you start
Read `numbers.md`, `rules.md`, `brand.md` and `learnings.md` (`**/accounts/<slug>/`). Ask for the
ad's data and the account average for the same format. If the ad has too little spend, say how
much more it needs before a verdict and stop there.

## The full funnel
Build the chain for the account's funnel type and fill in what exists. Missing steps are MISSING,
with where to get them.

| Stage | direct-sale | low-ticket | lead-crm | hotel |
|---|---|---|---|---|
| 1. Hook | 3s plays ÷ impressions | same | same | same |
| 2. Hold | ThruPlays ÷ 3s plays | same | same | same |
| 3. Click | CTR (link) | same | same | same |
| 4. Arrival | landing page views ÷ clicks | quiz visits ÷ clicks | LP visits ÷ clicks | site sessions ÷ clicks |
| 5. Middle | product view / add to cart | quiz completion, VSL reached | form submit | date search in the booking engine |
| 6. Decision | checkout started | VSL watch, checkout started | lead → MQL | rate/room selected, checkout started |
| 7. Close | purchase | purchase + bump + upsell | MQL → quote → sale | booking (and stay, after cancellations) |

- Compare each stage with the account average, or with the ad's own history if there is no average.
- **Low arrival** (stage 4) is almost always technical: slow page, redirects, video that won't play
  on mobile, in-app browser issues, duplicated pixel. Check before blaming the creative.
- High CTR with low sales points after the click, not at the ad.
- **Hotels:** a drop between date search and booking is often price, not marketing: compare the
  direct rate with Booking.com/Expedia for the same dates (rate parity). Also check that the
  booking engine domain is tracked (cross-domain GA4, purchase event with value) before concluding.

## Verdict
- **One stage below average:** FIX. Rebrief that stage only.
- **Two stages:** FIX the earliest one first (a new hook changes who reaches the rest).
- **All stages below:** before you KILL, find what failed, cheapest fix first:
  1. **packaging** (hook, first frame, on-screen text, headline): cheap to swap, keeps the idea;
  2. **external** (seasonality, holidays, pricier auction, a change in the page or the offer);
  3. **idea** (the angle itself);
  4. **audience** (do the people this ad attracts fit the offer?).

  Swap the packaging before you drop the idea. If nothing explains it, KILL for real and write the
  lesson: what hypothesis the ad tested and what the result suggests.

## Rebrief by stage
Three specific fixes that can be briefed today, using only claims allowed in `brand.md`:
- **Hook:** three new openings with different structures (audience callout, curiosity gap,
  contrarian take, problem moment, social proof), written as what is **seen**, **heard** and
  **read on screen** in the first 3 seconds. Never open on a logo.
- **Hold:** cut what comes before the problem, show the product or result earlier, faster pace,
  on-screen captions.
- **Click:** stronger proof, clearer offer, a single low-friction CTA, a curiosity loop that only
  closes after the click.
- **Post-click:** the fix is on the page, quiz, booking engine, checkout or lead follow-up. Name the
  step, the number and the test to run. This is not a creative brief.

Every fix comes with a hypothesis: "If we change X, we expect Y to go from A to B."

## Bad day mode
When sales or bookings drop suddenly, check in this order before touching anything:
1. Did tracking work? (conversions firing on the platforms and in the source of truth)
2. Did the site, booking engine or checkout break? (conversion rate, errors, payment gateway,
   booking engine outage, sold-out dates or closed-to-arrival restrictions)
3. Did spend or CPM jump on any platform?
4. Did a key ad or campaign stop delivering? (disapproved, spending limit, billing)
5. Outside causes: holiday, local event ending, competitor promo, OTA undercutting the direct rate,
   price change, offer offline.

Give the most likely cause with the numbers, how sure you are (low, medium, high) and the one thing
to check first. If it looks like a normal bad day within the account's variance, say so and
recommend waiting.

## Guardrails
- Diagnosis changes nothing in the account. Any action becomes a numbered item for approval.
- Never invent a metric or an ad claim.
- Small sample: say how much more is needed, no verdict.
