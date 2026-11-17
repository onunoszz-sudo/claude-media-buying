---
name: launch-qa
description: Checks a Meta Ads campaign against its written plan, before launch and 72 hours after - countries and location type, age, Advantage+ audience, placements, ABO or CBO, budget, event and pixel, URL and UTMs, names - and runs the technical read of early delivery (spend outside the planned countries, budget concentrated in one ad, rejections, landing page). Read-only; no performance verdicts. Use when the user says "launch QA", "check the campaign before it goes live", "does it match the plan", "I just launched, check it", "72-hour read", "QA the setup".
---

# Launch QA

The most expensive mistake in a new campaign is rarely the creative: it is the campaign being set
up differently from the plan (country, age, placements, budget type) and nobody noticing for days.
This skill compares the account with the plan field by field and says what blocks launch and what
is only a warning. It **only reads**: fixing is for the user or a separately approved action.

## Before you start
1. Find the account folder (`**/accounts/<slug>/`) and read `launch-plan.md`. No plan: stop and
   offer to build one with the user from `templates/launch-plan.md`. Without a plan there is no QA,
   only opinion.
2. Read `rules.md` (what is off-limits in the account) and `brand.md` (what ads must not say), if
   they exist.
3. State the mode: **pre-launch** (draft, or created and still paused) or **72-hour** (live for 1 to
   4 days). If unsure, run both.
4. Data comes from the **official Meta Ads connector**, read tools only (entities, drafts, activity
   log, breakdowns, creatives, errors, datasets). **Never** call a tool that creates, edits, pauses
   or activates, even if the connector suggests it.

## Pre-launch mode: plan vs. account
Read the campaign, ad sets and ads (drafts with `object_state=draft` if not yet published) with
their settings and compare:

| Plan field | Where it lives in the account | Severity if different |
|---|---|---|
| Objective | campaign `objective` | BLOCK |
| ABO or CBO | budget on the campaign (`daily_budget`/`lifetime_budget`) = CBO; on the ad set = ABO | BLOCK |
| Daily budget | `daily_budget` (minor units in the API) | BLOCK if above plan; WARN if below |
| Countries | `targeting.geo_locations` (`countries`, `country_groups`; "worldwide" is everywhere) | BLOCK |
| Location type | `geo_locations.location_types`: `home` = living in; `recent` = recently in; `travel_in` = traveling | WARN (Meta sometimes saves `frequently_in` alongside `home`; record it, do not block) |
| Age | `age_min`, `age_max`, `age_range` | BLOCK if outside the range when age is a hard limit |
| Age as a hard limit | `targeting_automation.advantage_audience`: 1 = Advantage+ on, age and gender become suggestions | BLOCK if the plan needs a limit and it is 1 |
| Gender | `genders` (1 men, 2 women) | BLOCK |
| Placements | `publisher_platforms`, `facebook_positions`, `instagram_positions`, `audience_network_positions` (prefer the `effective_*` fields; `page_types` does not decide) | BLOCK if anything on the "excluded on purpose" list is in, or if the plan lists exact placements and the account has others; a plan of "automatic" does not check the list |
| Event and pixel | ad set `optimization_goal` and `promoted_object` | BLOCK |
| Names | exact campaign, ad set and ad names | WARN (breaks the `utm_content` read) |
| Final URL and UTMs | each ad's creative link (creative tools, `link_url`; video creatives may not return it, then try the ad preview) | BLOCK if it is another URL; WARN if UTMs are missing; no data: "not checked", the user checks in Ads Manager |
| Status | `effective_status` of ads and ad sets; rejections | BLOCK if rejected |
| Dates | ad set start and end | WARN |

A blank plan field: write "MISSING in plan" and do not check it. A field set to "any": do not
check it.

Also check, when possible:
- **Landing page:** the final URL loads (no 404, no redirect to another page) and mobile PageSpeed
  (median of a few runs; a single run misleads).
- **Ad copy** against what `brand.md` forbids (without reopening anything the account owner has
  already accepted and recorded there).
- **Automatic creative enhancements** switched on when the plan wants the creative as is.

## 72-hour mode: technical read
No performance verdicts (that is `meta-review`). Read from launch to today and flag:
1. **Is it delivering?** Active ad set or ad with zero spend for more than 24 h: the reason
   (learning limited, rejection, budget too low, audience too small).
2. **Spend outside the planned countries.** Ask for the country breakdown **ad set by ad set**
   (`object_ids` of the ad set): at campaign level the country list can come back cut. Sum the
   spend outside the plan in money and %.
3. **Concentrated budget.** One ad with more than 80% of the ad set's spend: the others are not
   being tested. If the plan was an even creative test, the fix is a separate ad set (ABO), not
   pausing the ads with no spend.
4. **Delivered age and placements** vs. the plan (age and placement breakdowns) when Advantage+ is on.
5. **Tracking:** did the optimization event record anything? Do link clicks become landing page
   views (under 50% points to a slow page or a broken link)? If there is a revenue source of truth,
   do purchases match?
6. **Changes since launch** (activity log): who changed what, so the user knows the performance read
   has to be split before and after.

## Output
No em dashes, plain words.

1. **One-line verdict:** "OK to launch", "do not launch: N blockers" or, in 72-hour mode,
   "running as planned" / "running differently from the plan in N places".
2. **Table per campaign and ad set:** field, plan, account, status (OK, BLOCK, WARN, MISSING in plan).
3. **72-hour mode:** spend outside the plan (amount and %), concentration by ad, tracking.
4. **Step-by-step fixes** in Ads Manager, one per blocker, ordered by what spends money wrong first.
   Remember that editing a live ad set pauses delivery until it is reactivated.
5. **What was not checked** and why (blank field, tool without the data).

When saving, use `launch-qa-YYYY-MM-DD.md` in the offer or client folder.

## Guardrails
- No write tools, ever. A fix is a separate action with a "yes".
- Never assume the plan: what is not written is MISSING.
- Never invent a number; data the tool did not return shows as MISSING.
- QA is not a performance review: no KILL or SCALE here.
