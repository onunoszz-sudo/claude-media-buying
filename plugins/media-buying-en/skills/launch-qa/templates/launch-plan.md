# Launch plan: <account>

> One block per campaign. Filled in before launch; the `launch-qa` skill compares the account with
> this file. A blank field becomes "MISSING in plan" and is not checked.
> Fields set to "any" are not checked on purpose.

## Campaign: <exact campaign name>
- **Platform:** Meta
- **Campaign ID:** <fill in after creating, helps find it>
- **Objective:** Sales | Leads | Traffic
- **Budget:** ABO (ad set) | CBO (campaign)
- **Daily budget:** <amount and currency> (per ad set if ABO; total if CBO)
- **Start:** YYYY-MM-DD · **Read:** YYYY-MM-DD · **End or spend cap:** <date or amount>

### Ad set: <exact ad set name>
- **Countries:** <codes, e.g. US, CA>
- **Location type:** living in | living in or recently in | any
- **Age:** <min> to <max>
- **Age as a hard limit:** yes (original audience options, Advantage+ off) | no (Advantage+ on, age is a suggestion)
- **Gender:** women | men | all
- **Interests or custom audiences:** none | <list>
- **Placements:** automatic | <exact list, e.g. Facebook Reels, Instagram Reels>
- **Excluded on purpose:** <e.g. Audience Network, ads within Reels>
- **Optimization event:** <e.g. Purchase>
- **Pixel or dataset:** <ID>
- **Ad set budget:** <if ABO>

### Ads
| Exact name | Creative file | Final URL | URL parameters |
|---|---|---|---|
| <name> | <file> | <https://...> | <utm_source=...&utm_content={{ad.name}}> |

### Agreed read rules
- **Pause:** <e.g. ad with $140 spent and no booking>
- **Scale:** <e.g. cost of sale under 12% with 5 bookings>
- **Hands off until:** <date>
