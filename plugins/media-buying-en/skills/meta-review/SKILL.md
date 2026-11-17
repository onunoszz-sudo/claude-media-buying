---
name: meta-review
description: Reviews live Meta Ads ads and labels each one KILL, WATCH or SCALE, shows the funnel stage where each ad leaks (hook, hold, click, conversion), flags creative fatigue, unfair delivery and ads blocked from scaling by the account's claim rules. Use when the user says "Meta review", "Facebook ads review", "what should I pause", "which ads to scale", "creative fatigue", "analyze my creatives", or shares an Ads Manager export.
---

# Meta Ads review

"ROAS good, keep; ROAS bad, kill" tells you what happened, not why. This review reads every ad
stage by stage against the account's own average and returns a numbered list of actions for the
user to approve.

## Before you start
1. Find the account folder (`**/accounts/<slug>/`). Read `numbers.md`, `rules.md`, `brand.md`
   and `learnings.md`. No `numbers.md`: stop and run `account-numbers` first.
2. Get the data, in this order:
   - **Official Meta Ads connector** (if its tools are in this session): use the reporting tools at
     ad level for the last 7 and 14 days, with the fields below, plus breakdowns by placement, age
     and day. **The connector can also write** (create paused campaigns, change budgets, pause,
     activate): never call a write tool without a "yes" for that specific action, and read back
     afterwards to confirm the change matches what was approved.
   - **Ads Manager export:** ad level, last 7 and last 14 days. Needed: ad name, ad set, campaign,
     delivery, start date, amount spent, impressions, frequency, CPM, link clicks, CTR (link),
     3-second video plays, ThruPlays, results/purchases, conversion value. Say which columns are missing.
3. **Real revenue:** if the source of truth is not the pixel, ask for the real number. Pixel vs.
   source of truth more than 20% apart: flag it before labeling and suggest running `tracking-check`. In low-ticket and hotel accounts
   the pixel often records only part of the value (front-end only; booked, not stayed).
   **Real sales per ad:** if the payment platform stores where each sale came from (Hotmart:
   `sck` / checkout source; store: `utm_content`; CRM: source field) and the ad links pass the ad
   name in that parameter, count approved sales per ad and use the **real CPA** (ad spend ÷ its
   real sales) instead of the pixel CPA. Say how many sales in the period had no source. If the
   links don't carry that parameter, recommend adding it: it is what lets you kill an ad on real sales.
4. **Custom columns** (e.g. "HOOK RATE", "HOLD RATE"): use them as given, but ask for the formula if
   it changes the read (ThruPlays ÷ impressions is not ThruPlays ÷ 3-second plays).
5. **Breakdowns:** check totals match across placement, age and day files before using them. The
   export day itself is partial and stays out of the trend read.
6. **Plan vs. reality:** if a campaign plan is documented, compare planned daily budget, age,
   countries and placements with what the export shows delivering.

## Per-ad metrics
| Stage | Formula | If low, the problem is |
|---|---|---|
| Hook | 3-second plays ÷ impressions | first 3 seconds don't stop the scroll |
| Hold | ThruPlays ÷ 3-second plays | they stop but don't stay: slow story, product too late |
| Click | link clicks ÷ impressions | they watch but don't want it enough: offer, proof, CTA |
| Conversion | conversions ÷ link clicks | they click but don't buy: page, price, checkout, speed |

Compare each ad with the account average for the same format. No outside benchmarks. Statics have
no hook/hold: read CTR and conversion. In low-ticket, lead-crm and hotel accounts, conversion opens
into post-click steps (quiz, booking engine search, checkout, lead to MQL): use `ad-diagnosis` for
an ad that leaks there.

## Labels
Use thresholds from `rules.md`; otherwise:
- **KILL:** spent 2x target CPA with no conversion, or CPA 50%+ above target for 3 days with volume.
- **WATCH:** under 72 h live; ad set in learning; fewer conversions than the minimum (default 3);
  or CPA between target and max.
- **SCALE:** under target CPA (or above target ROAS) for 3+ days with the minimum conversions, CPA
  and frequency stable.

Two extra labels:
- **NO SPEND:** spent less than 1x target CPA in the period. Untested, not a loser. Several of them
  in one ad set with campaign budget (Advantage+ campaign budget) means Meta concentrated delivery
  on one ad: the fix is a separate ad set with an equal budget (ABO) for the creatives that need a
  test, not pausing the unspent ones.
- **BLOCKED FROM SCALING (claims):** the ad uses a claim, credential, testimonial, number or anchor
  price that `brand.md` forbids. It gets no budget step whatever its numbers; the action is to swap
  in a compliant version. If you cannot see the ad's content, say the claim check was not done.
  If `brand.md` records that the account owner accepted a given claim, it does not block.

Small samples never become winners or losers: they stay in WATCH, with how much more spend is
needed to decide.

**Wasted spend** (sorts the action list): spend − conversions × target CPA. It is how much the ad
cost above what it should have for what it delivered. High and positive = the most money lost,
even when campaign ROAS looks fine. The bottom 3 by wasted spend open the actions.

## Fatigue radar
For every ad with meaningful spend in the last 14 days (default: over 2x target CPA), compare its
first 7 days live with its last 7: frequency, CTR, CPM, CPA, hook rate. Flag **FATIGUING** when two
or more move the wrong way together. Rank by spend; the top ones need fresh variations first
(suggest running `winner-multiplier`).

**Account-wide drop is not fatigue:** if almost every ad got worse in the same week (new ones
too), the cause is shared: tracking, page, checkout, offer, price or the auction (seasonality). Do
not flag FATIGUING; say so and suggest `tracking-check` or `ad-diagnosis` before swapping creative.

## Output
Plain words, no em dashes.
1. **Three lines:** what's working, what's leaking, what to do today.
2. **Table**, one ad per row, sorted by wasted spend (highest first): ad, spend, conversions (real,
   if available), CPA, wasted spend, ROAS, hook, hold, CTR, frequency, leaking stage, label.
3. **Breakdowns that change a decision:** an age band or placement taking spend without converting,
   low-quality click sources (Audience Network with CTR far above average, ads inside Reels).
   Always with the sample size caveat.
4. **Fatigue:** the FATIGUING list with the metrics that moved (or "not applicable" if no ad has 14 days).
5. **Numbered actions to approve:** pauses (never deletes); the **budget ladder**, at most one
   step per ad set or campaign, 48 h after the last one:
   - **up** to 20%: SCALE with stable CPA;
   - **hold:** a new ad entered the ad set in the last 48 h, the ad set is in learning, or the page
     or offer changed (the read is not clean yet);
   - **down one step** (−20%) instead of killing: CPA between target and max (break-even) in an ad
     set that was a winner;

   and which ads need a new hook, a new story, a new offer/proof or a page fix.
6. **Candidate learning** for `learnings-log`, if a pattern is clear.

Save the review as `meta-review-YYYY-MM-DD.md` in the client or offer folder when asked to save.

An ad **rejected by Meta**: add a line to the account's `brand.md` the same day (what was rejected
and the likely phrase or image), so the rule holds in the next creative round.

## Guardrails
- No change in the account without a "yes" for each numbered action.
- Pause, never delete.
- Never more than +20% per budget step; never two steps on the same ad set within 48 h.
- One bad day is not a trend: judge on the window in `numbers.md`.
- Never invent a number; a missing metric shows as MISSING.
