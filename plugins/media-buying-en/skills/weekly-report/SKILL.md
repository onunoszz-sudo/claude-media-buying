---
name: weekly-report
description: Writes the weekly (Monday) report for an ad account, combining Meta, Google and the source of truth for revenue, in two versions - internal (break-even, losses, decisions) and client-facing (progress, what we changed, next steps). Hotel accounts separate booking date from stay date and report revenue net of cancellations. Use when the user says "weekly report", "Monday report", "client report", "weekly recap", "how did the week go".
---

# Weekly report

Once a week, the account's story in plain words: what happened, why, what was done and what needs
a decision. The report a good media buyer would send, no call needed.

## Before you start
1. Read the six account files (`**/accounts/<slug>/`). `brand.md` says what may and may not appear
   in client-facing material.
2. Dates: the closed week (Monday to Sunday) vs. the week before. State the dates at the top.
3. Data: Meta, Google and the source of truth for this week and last; what was paused or scaled;
   new learnings; month-to-date pacing.
4. **Golden rule:** recompute every derived metric (CPA, ROAS, MER, cost of sale, AOV, CPM) from the
   week's totals. Never copy a derived number from a spreadsheet or a totals row, which can be stale.

**Hotels:** keep two views and label them:
- **Booked this week** (by booking date): bookings, room nights, booked revenue, cost of sale. This
  is what the ads drove and what optimization uses.
- **Stayed this week** (by stay date), net of cancellations: what the hotel actually earned.
  Mention upcoming-month pickup if the client tracks it.

## Internal version (for the media buyer / account lead)
Under 400 words, no em dashes.
1. **Headline** in one sentence.
2. **Numbers:** total spend, revenue (source of truth), MER or cost of sale vs. target and
   break-even; for lead-crm, leads, MQLs, quotes, sales and cost per each.
3. **Meta:** spend, conversions, CPA, ROAS; top 3 ads and why they won, and the **bottom 3 by
   wasted spend** (spend − conversions × target CPA) with the action for each. If the source of
   truth records the sale's source per ad, use real sales.
4. **Google:** spend, conversions, ROAS; best and worst campaign; negatives added; brand vs. non-brand.
5. **Post-click:** the funnel step that changed most (page, quiz, booking engine, checkout, follow-up).
6. **Paused/scaled** this week and roughly what it saved or added (estimate, with the math).
7. **Pacing:** month-to-date vs. contracted budget, projection.
   Also list what changed in the funnel this week (deploy, price, VSL, bump, upsell) from the
   account's change log, if there is one: an unlogged change muddles the weekly read.
8. **Creative needed next week.**
9. **Three decisions for the account lead**, numbered.

## Client version
Same facts, client framing:
- **No** break-even, loss, negative ROI or comparisons that read as failure. Show what improved, what
  was adjusted and what's next.
- Numbers the client recognizes (bookings, room nights, revenue, cost per booking, leads), with the
  change vs. last week.
- A "what we did this week" paragraph and a "next steps" paragraph. Anything that depends on the
  client (photos, approvals, rates, lead follow-up) is written as a clear request.
- Respect everything `brand.md` says must not appear.
- Never hide a problem the client has to solve (e.g. leads not called back, direct rate above the
  OTAs): write it as a next step, not as blame.
- US business English, short paragraphs, no jargon the client wouldn't use.

## After the report
Propose new lines for `learnings.md` (run `learnings-log`) and, if a winner spent two weeks in SCALE,
suggest adding it to `winners.md`.

## Guardrails
- Never invent a number; missing data shows as MISSING in the internal version and is left out
  (never replaced by a guess) in the client version.
- Any estimate of savings or gains shows its math.
- The client version is never sent by the agent: the account lead reviews and sends it.
