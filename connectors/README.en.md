# Connectors: Meta Ads and Google Ads (no cost)

*Versão em português: [README.md](README.md)*

With both connectors on, the skills read the accounts directly, with no exports, and scheduled
tasks (daily brief, Monday review, Friday pacing) can run on their own. Both routes below are
official and free. The ad options in Claude's connector directory (Supermetrics, Windsor.ai,
Adspirer, Funnel) are paid.

| | Meta Ads | Google Ads |
|---|---|---|
| Published by | Meta (official connector, beta since 2026-04-29) | Google (`googleads/google-ads-mcp`, open source) |
| Runs | on Meta's server, as a custom connector in Claude | locally on your machine, via `uvx` |
| Access | **read and write** (paused campaigns, budget changes, pause) | **read only** |
| You need | a Facebook login with access to the ad accounts | developer token, Google Cloud project, OAuth credential |
| Time | 2 minutes | 30 to 45 minutes, plus token approval if it isn't granted right away |

## The safety rule for both
Claude proposes, you approve. The skills never call a write tool without a "yes" for that action,
and Claude **does not read, copy or paste** tokens, keys or passwords: those go straight into local
files only you edit.

## 1. Meta Ads
1. claude.ai → **Customize → Connectors → Add → Add custom connector**.
2. Name: `Meta Ads` · URL: `https://mcp.facebook.com/ads` → **Continue → Add** (leave
   authentication as detected).
3. Click **Connect**. Log in with the Facebook profile that has access to the ad accounts, select
   **only** the businesses and pages Claude should see, and accept Meta's terms.
4. In a new chat, check the **Meta Ads** connector is on and ask: "list the ad accounts you can see
   and each one's spend for the last 7 days". Change nothing for the first few days.

If you see "account not enabled": Meta is rolling the connector out gradually. Until then, use the
Ads Manager CSV export (ad level) with the same skills.

The connector gets the same permissions your login has on the account. The account is protected by
the skills' guardrails and by your habit of never approving an action you haven't read.

## 2. Google Ads
### 2.1 API access level (in the Google Cloud project)
Since 2026 Google Ads API access is managed **in the Google Cloud project**, no longer through the
Google Ads API Center form. That form is now only for the "App Conversion Tracking and Remarketing
API": don't use it for this.
1. After creating the project and enabling the API (2.2), open **APIs & Services → Google Ads API →
   Access levels → Manage**.
2. Projects start at **Test** (test accounts only). Under **Upgrade access level → Explorer**, click
   **Apply for access**. The request is sent **on click**, with no form, and stays "under review"
   for a few minutes.
3. With Explorer approved, a developer token is **optional**: leave the `.env` line as is unless you
   already have a legacy token.

At an agency, the Cloud project and its access level should belong to the agency. Ask whoever owns
the MCC before creating your own.

### 2.2 Google Cloud project (you)
1. console.cloud.google.com → create a project (e.g. `ads-mcp`) and note the **project ID**.
2. **APIs & Services → Library →** enable the **Google Ads API**.
3. **Google Auth Platform (OAuth consent screen):** External, app name, your email. Under
   **Audience**, publishing **In production** requires a homepage and privacy policy URL in Branding.
   Without them, stay in **Testing**, add your email under **Test users** and re-run
   `gerar_credencial.py` every 7 days (testing-mode credentials expire).
4. **Clients → Create client → Desktop app →** download the JSON and save it as
   `%USERPROFILE%\.config\google-ads-mcp\client_secret.json` (or `~/.config/google-ads-mcp/` on macOS/Linux).

### 2.3 Credential and token on your machine
1. Generate the credential (opens the browser; authorize with the Google account that can access the MCC):
   ```bash
   python connectors/google-ads/gerar_credencial.py
   ```
   It is written to `~/.config/google-ads-mcp/adc.json`. Nothing is printed to the screen.
2. Open `~/.config/google-ads-mcp/.env` (template in `google-ads/env.exemplo`) and fill in
   `GOOGLE_PROJECT_ID` and, with an MCC, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (digits only).
   `GOOGLE_ADS_DEVELOPER_TOKEN` is optional (see 2.1).

### 2.4 Plug it into Claude Code
In the project you work in, a `.mcp.json` with:
```json
{
  "mcpServers": {
    "google-ads": {
      "command": "python",
      "args": ["<repo path>/connectors/google-ads/iniciar_servidor.py"]
    }
  }
}
```
Restart the app and approve the `google-ads` server when asked. The launcher checks the `.env` and
the credential before starting; if something is missing it stops and says what.
Test: "which Google Ads accounts can you access?" (`list_accessible_customers` tool).

## 3. Automation (once both respond)
With the connectors working, scheduled tasks run read-only and save their output to a file:

| When | Task |
|---|---|
| Weekdays, 8 am | `daily-brief` for the portfolio |
| Monday, 9 am | `meta-review` + `weekly-report` + `learnings-log` (proposals) |
| Tuesday, 9 am | `google-ads-health` + `search-terms` |
| Friday, 9 am | `budget-pacing` |

No scheduled task changes an account: they deliver the action list, and you approve in a conversation.

## Common issues
- **"only approved for use with test accounts":** the project is still at Test. Apply for Explorer
  under Google Ads API → Access levels (2.1).
- **`invalid_grant` after a week:** the consent screen was left in "Testing". Set it to
  "In production" and run `gerar_credencial.py` again.
- **No `refresh_token`:** remove the app's access at myaccount.google.com/permissions and run again.
- **Server not showing in Claude:** check the path in `.mcp.json`, that `uvx` is on PATH and that you
  approved the server when opening the project.
- **Agency data policy:** connecting client accounts to an AI tool may need the agency's approval.
  Check before connecting.
