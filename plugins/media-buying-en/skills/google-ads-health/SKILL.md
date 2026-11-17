---
name: google-ads-health
description: Weekly health check of Google Ads campaigns (Search, Performance Max, Demand Gen, YouTube, hotel campaigns) against the account's numbers - profitable campaigns limited by budget, campaigns below break-even, CPC jumps, wrong final URLs, conversion goals counting the wrong thing, Performance Max taking credit for brand searches - and returns 5 actions as exact steps, separating what the agent can do from what only the account owner can. Use when the user says "Google Ads health check", "campaign audit", "Google review", "why is Google spending more", or shares a campaign report.
---

# Google Ads health check

Google leaks money in quiet places: a good campaign capped by budget, a bad one nobody opens, ads
sending traffic to the wrong page, a conversion goal counting page views. This skill runs the
check-up and returns the actions as exact steps.

## Before you start
1. Read `numbers.md`, `rules.md` and `learnings.md`. `rules.md` holds what the agent may do in Google
   Ads and what only the account owner does (with the official MCP: everything is read-only for the
   agent; some accounts also require identity verification for ad edits).
2. Data, in order: Google Ads MCP (`search` tool), the interface in the browser, or a campaign CSV
   for the period **and** the previous period. State the date of the data.

### Ready-made queries (Google Ads MCP, `search` tool)
> Official server `search` tool: pass the parts separately, not the whole query. `resource` = what follows FROM, `fields` = the SELECT list, `conditions` = each WHERE clause (e.g. `"segments.date DURING LAST_30_DAYS"`), plus `orderings` and `limit`. When unsure about a field, use `metadata_get_resource_metadata`.

Run for the period and the previous period (`LAST_14_DAYS`, then `BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'`).
Cost and budget in micros (÷ 1,000,000).
```sql
-- campaigns: results, budget and impression share lost to budget/rank
SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign.status,
       campaign.bidding_strategy_type, campaign_budget.amount_micros,
       metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.average_cpc,
       metrics.conversions, metrics.conversions_value,
       metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date DURING LAST_14_DAYS AND campaign.status = 'ENABLED'

-- what is being counted as a conversion
SELECT conversion_action.name, conversion_action.category, conversion_action.primary_for_goal,
       conversion_action.status
FROM conversion_action

-- final URLs of live ads
SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls
FROM ad_group_ad
WHERE ad_group_ad.status = 'ENABLED' AND campaign.status = 'ENABLED'

-- disapproved or limited ads
SELECT campaign.name, ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status
FROM ad_group_ad
WHERE ad_group_ad.policy_summary.approval_status != 'APPROVED' AND ad_group_ad.status = 'ENABLED'
```
Final URL expansion in Performance Max and search partners are checked in the interface.

## What to check, per campaign
| Check | Signal | Why it matters |
|---|---|---|
| ROAS/CPA or cost of sale vs. `numbers.md` | below break-even, between, above target | cut, hold or grow |
| Limited by budget | profitable and "Limited by budget" (budget lost IS > 10%) | money left on the table |
| CPC | up 30%+ vs. previous period | competition, quality or bid change |
| Conversion goal | optimizing for the right action (booking with value, purchase, qualified lead; not page views) | the wrong goal trains the algorithm wrong |
| Final URL | every ad lands on the right page; PMax final URL expansion on? | traffic to pages that don't convert |
| Search terms | spend with no conversions | run `search-terms` |
| Search partners / Display inside Search | on with no results | budget outside Search |
| Performance Max | share of revenue from brand searches; asset strength | may be taking credit for sales that come anyway |
| Status | disapproved ads/keywords, paused by limit or billing | delivery stopped without anyone noticing |

**Hotels:**
- Brand vs. non-brand split: brand campaigns are judged against the OTA commission they save, not
  against non-brand CPA. Watch brand impression share lost to OTAs.
- Performance Max for travel goals and hotel ads depend on the Hotel Center feed and live rates:
  check feed and price accuracy warnings in the interface (feed work is out of this skill's scope).
- Report bookings by **booking date** for optimization and by **stay date** for the client's revenue,
  and say which one each number is.
- Conversion value should be the booking value with cancellations reconciled, not a fixed value.

For lead-crm, the real result of a campaign is what became MQL/quote/sale in the CRM or sales sheet.
Cross by campaign when UTM/gclid is captured; if not, that is action number one.

## Output
No em dashes.
1. **Three lines:** what's good, what's leaking, what to do this week.
2. **Table:** campaign, type, spend, conversions, value, CPA/ROAS (or cost of sale), change vs.
   previous period, status vs. target, alert.
3. **5 actions, most valuable first**, each with:
   - what to do and the expected gain (with the number behind it);
   - **who does it:** "agent can do it after your yes" or "account owner only", per `rules.md`;
   - exact steps in the Google Ads interface.
4. **Candidate learning** for `learnings-log`.

## Guardrails
- No change without a "yes" per action.
- Budgets: at most +20% per step, 48 h apart; respect known budget floors in `rules.md`.
- Pause, never remove a campaign.
- Before re-enabling a paused campaign, check every ad's final URL.
- Never invent a number; stale or missing data is flagged.
