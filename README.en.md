# claude-media-buying (English)

*Português: [README.md](README.md)*

A set of Claude skills for running Meta Ads and Google Ads accounts the way an agency media buyer
does, on one principle: **Claude proposes, you approve.** The `media-buying-en` plugin is the
English edition, built for US agencies and multi-account portfolios such as hotels.

It does not replace the media buyer. It replaces the parts of the job that don't need judgment:
opening twenty dashboards, recomputing the same metrics, formatting the same reports, and
remembering what each account taught us last month.

## What's inside (v0.5)
| Skill | What it does | When |
|---|---|---|
| `account-numbers` | Onboards an account: context files plus break-even ROAS, target CPA/ROAS, MER; **hotel mode** with cost of sale vs. OTA commission, net of cancellations | onboarding, quarterly |
| `daily-brief` | Portfolio morning brief: at most 5 items per account, most expensive first, plus pacing | every morning |
| `meta-review` | KILL / WATCH / SCALE per ad, leaking funnel stage, fatigue, unfair delivery, claim-blocked ads | daily read, deep on Mondays |
| `ad-diagnosis` | Reads one ad as its own funnel through post-click (booking engine, checkout, CRM) and rebriefs only the weak stage; "bad day" mode | when something surprises you |
| `search-terms` | Wasted spend → conflict-checked negatives, paste-ready; hotel themes (OTA names, jobs, wedding venue) | Tuesdays |
| `google-ads-health` | Campaigns vs. targets, budget-limited winners, CPC jumps, wrong final URLs, wrong conversion goals, PMax brand credit | Tuesdays |
| `budget-pacing` | Portfolio pacing vs. contracted budgets: projection, recommended daily, ON PACE / UNDER / OVER / OVERSPEND | daily, Fridays |
| `weekly-report` | Internal report plus a client-facing version; hotels split booking date vs. stay date | Mondays |
| `learnings-log` | Account rules with evidence and confidence; contradiction check; cross-portfolio patterns | Mondays |
| `launch-qa` | Checks the account against the written launch plan, before launch and 72 h after; read-only, BLOCK / WARN per field | every launch |
| `test-round` | Sizes the creative test to the budget (how many ads the KILL line can judge); hypothesis and agreed decision per ad | Thursdays, each round |
| `winner-multiplier` | Why a winner won, one-variable variations, script in blocks, hook rescue, RSA headlines | Thursdays, when there is a winner |
| `angle-map` | Angle x person x format grid from customers' own words, empty cells, hooks with a policy check | Tuesdays, before each round |
| `tracking-check` | Pixel vs. real sales by day: match rate, purchases with no value, double counts, missing sales; says whether ads can be judged (read-only) | monthly and after checkout/funnel changes |

Three scripts (Python 3, standard library only) do the arithmetic so the numbers are never
hand-calculated: `calc_numeros.py` (decision numbers, incl. hotel), `calc_pacing.py` (portfolio
pacing) and `calc_rodada.py` (test round size). All print the math.

## Example: taking over 10 hotel accounts
**Week 0, onboarding (about 45 minutes per hotel)**
1. **Tracking audit:** Meta pixel + Conversions API, GA4 with cross-domain tracking into the
   booking engine (SynXis, Cloudbeds, SiteMinder, Mews...), Google Ads conversion = booking with
   value, Hotel Center if used.
2. **`account-numbers` in hotel mode:** ADR, length of stay, cancellation rate, the OTA commission
   from the hotel's contract, target cost of sale. Example:
   ```bash
   python calc_numeros.py hotel --lang en --adr 220 --nights 2.6 --cancellation 0.18 \
       --ota-commission 0.18 --target-cos 0.12 --margin 0.70 --profit 0.25
   ```
   → realized revenue $469.04 per booking; max CPA $84.43 (OTA lens); target CPA $56.28;
   **target in-platform ROAS 10.16x** (platforms report booked revenue before cancellations,
   so this is the number to compare with Google and Meta).
3. **`brand.md` and `rules.md`:** brand rules, rate parity, allowed promos, who signs off on what,
   contracted budget per platform.
4. **Data feeds:** official Meta connector + Google Ads MCP, or scheduled exports into
   `clients/<hotel>/exports/YYYY-MM-DD/`.

**Weekly rhythm (10 hotels)**
| When | What | Rough time* |
|---|---|---|
| Every day | `daily-brief` for the portfolio + pacing; approve and apply actions | 20 to 30 min |
| Monday | `meta-review` ×10, `weekly-report` (client versions), `learnings-log` | half a day |
| Tuesday | `google-ads-health` + `search-terms` ×10 | 1 to 2 h |
| Wednesday | Fix what diagnosis found (pages, booking engine, ads) | varies |
| Thursday | `test-round` and `winner-multiplier`; `launch-qa` before launch and 72 h after | varies |
| Friday | `budget-pacing` and next week's budget steps | 1 h |
| Monthly | Review numbers, seasonality and events calendar, cross-hotel patterns | 2 h |

\*Estimates, not measurements. The biggest gain is not the analysis itself but never building a
report by hand and never missing an expensive problem.

**What the portfolio view adds:** one list of the costliest problems across all ten hotels; the
same labels and thresholds everywhere, so accounts are comparable; and, over time, patterns by
segment (what works for resorts vs. boutique vs. city hotels), always tested per account before
being adopted.

## Limits (read before relying on it)
- **Data access:** without connectors everything runs on exports. The Meta connector is in gradual
  rollout; the Google Ads MCP needs a developer token from the agency's MCC. Agency tools
  (Supermetrics, Looker Studio, Funnel) work as inputs too.
- **Execution:** Claude proposes; a person applies. The Google Ads MCP is read-only. Meta's
  connector can write, so the skills require a "yes" per action.
- **Attribution in hotels is fragile:** a booking engine on another domain or inside an iframe
  often breaks tracking. Every analysis is only as good as the real revenue it's given.
- **Not covered yet:** Hotel Center feed, metasearch (Google Hotel Ads, Tripadvisor, Trivago),
  Meta travel catalogs, revenue management, creative production.
- **Small samples:** hotels are high-value, low-volume. Many ads stay in WATCH longer; judging
  windows must be longer than in ecommerce.
- **Data policy:** check the agency's rules on connecting client accounts and sharing client data
  with AI tools.

## Connectors and automation
Setup guide: [connectors/README.en.md](connectors/README.en.md). Both routes are free and official:
Meta's connector (custom connector in Claude, read and write) and Google's open-source Google Ads
MCP server (local, read-only). Scheduled tasks are read-only and only deliver action lists.

## Guardrails (all skills)
1. No change to an account without a "yes" for that specific action.
2. First week: read-only.
3. Pause, never delete.
4. Budget: at most +20% per step, one step every 48 h per campaign or ad set.
5. Small samples stay in WATCH.
6. Never invent a number or a claim: missing data shows as MISSING.
7. The pixel is not the source of truth for revenue.
8. Claude never reads or copies tokens, keys or passwords.

## Install (5 minutes)
You need **Claude Code** (terminal, desktop app or VS Code extension) on a paid Claude plan.

1. Open Claude Code and type, one line at a time:
   ```
   /plugin marketplace add onunoszz-sudo/claude-media-buying
   /plugin install media-buying-en@claude-media-buying
   ```
2. Restart Claude Code. The skills show up in the `/` menu.
3. Make a folder for your ads work, open Claude Code there and ask for **"account numbers"** for
   your first account. It creates `accounts/<account-name>/` with the files every other skill reads.
4. Connect your data (optional, but it's what makes it hands-off): follow
   [connectors/README.en.md](connectors/README.en.md) for the official Meta connector and Google
   Ads. Without a connector, the skills work from an Ads Manager export pasted into the chat.

**Update to a new version:** `/plugin marketplace update claude-media-buying`.

Without `/plugin`, copy `plugins/media-buying-en/skills/*` into `~/.claude/skills/`.

## Credits
The method is adapted, in original wording, from four public playbooks: *The Claude Media Buying
Team* and *The Claude Code Paid Ads Team* (Paul Ryan Jones, ORIRI Marketing), *The Meta + Google
Ads Agent* and *12 Claude Agents for Meta Ads* (Dusan Radovanovic, Hook & Scale). No text, prompt or file from them is copied here.
