---
name: search-terms
description: Reads the Google Ads search terms report and turns wasted spend into a negative keyword list grouped by theme, with spend and match type, conflict-checked against keywords, converting terms and the brand, ready to paste; also lists converting terms that are not keywords yet. Covers hotel-specific waste (OTA names, jobs, wedding venue, wrong city). Use when the user says "search terms", "negatives", "negative keywords", "where is Google wasting money", "SQR", or shares a search terms CSV.
---

# Search terms → negatives

In almost every account part of the budget goes to searches that will never buy. Cutting them is
the easiest money to save on Google. Run weekly, on the last 14 to 30 days.

## Before you start
1. Read `numbers.md`, `offers.md`, `brand.md`, `rules.md` and `learnings.md`.
2. Get the data:
   - **Google Ads MCP connected** (`search` tool, read only). Pass the account's `customer_id`
     (digits only) and the MCC as `login_customer_id` when access is through a manager account.
     Cost is in micros (÷ 1,000,000).
> Official server `search` tool: pass the parts separately, not the whole query. `resource` = what follows FROM, `fields` = the SELECT list, `conditions` = each WHERE clause (e.g. `"segments.date DURING LAST_30_DAYS"`), plus `orderings` and `limit`. When unsure about a field, use `metadata_get_resource_metadata`.

     ```sql
     -- search terms by spend
     SELECT search_term_view.search_term, search_term_view.status, campaign.name, ad_group.name,
            metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.conversions_value
     FROM search_term_view
     WHERE segments.date DURING LAST_30_DAYS
     ORDER BY metrics.cost_micros DESC
     LIMIT 500

     -- active keywords
     SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
     FROM keyword_view WHERE ad_group_criterion.status = 'ENABLED'

     -- campaign negatives
     SELECT campaign.name, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
     FROM campaign_criterion
     WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'

     -- shared negative lists (the campaign negatives table does not show these)
     SELECT shared_set.name, shared_criterion.keyword.text, shared_criterion.keyword.match_type
     FROM shared_criterion WHERE shared_set.type = 'NEGATIVE_KEYWORDS'
     ```
   - **No MCP:** the search terms CSV plus the keyword and negative lists. Without the lists, say the
     conflict check could not be done and mark each suggestion "check conflict".

## How to analyze
- **Look at spend, not clicks.** A $80 term with zero conversions matters more than a 3-click one.
- Group into themes: jobs/careers, free/cheap, how-to/informational, wrong product or service,
  wrong city or region, competitor (support, login, phone), other language.
- **Hotels, typical themes:** OTA names ("booking.com", "expedia", "hotels.com", "airbnb"), "jobs",
  "wedding venue" or "events" (unless the hotel sells them), "cheap motel", "hostel", "camping",
  wrong city or neighborhood, "reviews"/"tripadvisor" research, competitor hotel names (decide with
  the client whether conquesting is intended), "phone number"/"address" of existing guests.
- For each theme: total spend, the terms, the suggested negative and match type:
  - **exact** `[term]` blocks only that search. Use it when unsure.
  - **phrase** `"term"` blocks every search containing the phrase. Stronger, riskier.

## Conflict check (mandatory)
Before suggesting a **phrase** negative, check that it would not block:
1. the account's brand or a product, room type or package in `offers.md`;
2. an active keyword;
3. a term that **converted** in the period.

Example of the mistake this prevents: a phrase negative "rental" blocking "LED panel rental", the
very service sold. In hotels, a phrase negative "booking" would block "book [hotel name] direct".
If there is a conflict, downgrade to exact or drop it, and explain.

**Brand defense (hotels):** if OTAs show up in the auction for the hotel's name, the brand campaign
is defending direct bookings. Do not cut brand spend just because brand CPA looks expensive vs.
non-brand; compare it with the OTA commission on those bookings.

## Output
1. **Three-line summary:** total spend in the period, spend on non-converting terms, how much the
   suggested negatives would have saved (estimate on the period analyzed).
2. **Table by theme:** theme, spend, terms, suggested negative, match type, conflict checked (yes/no).
3. **Paste-ready list** for the Google Ads negatives screen, one per line with syntax (`[exact]` or
   `"phrase"`), and the level to apply it (shared list, campaign or ad group).
4. **Converting terms that are not keywords**, with a suggested ad group.
5. **Candidate learning** for `learnings-log`.

## Guardrails
- Never suggest a negative that blocks the brand, an active product or a converting term.
- The official Google Ads MCP is read-only: approved negatives are added in the interface (or in the
  browser if the user asks), then checked in the negatives table.
- Low-sample terms with plausible intent stay out: note them for next round.
