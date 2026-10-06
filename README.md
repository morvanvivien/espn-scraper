# How to Scrape ESPN Scores, Schedules & Odds (NFL, NBA, MLB, NHL & More)

> **Run it now, no code: [espn-scores-scraper on the Apify Store](https://apify.com/bibian/espn-scores-scraper)** &nbsp;|&nbsp; $0.60 per 1,000 games &nbsp;|&nbsp; no browser, no proxy

ESPN publishes a public JSON scoreboard API behind its own site, covering NFL, NBA, WNBA, MLB, NHL, NCAA football, NCAA basketball and Premier League soccer. This guide shows how to read it directly and get clean structured scores, schedules and pre-match odds, for one league or several.

Searches this page answers: espn scraper, nfl scores api, nba scores scraper, sports odds scraper, espn api scores.

## What you get from the ESPN scraper

- Every game for the league and days you choose, with final or live score, venue and broadcast.
- Scheduled games with pre-match odds (spread, moneyline, total) when a sportsbook has posted a line.
- One normalized schema across eight leagues: NFL, NBA, WNBA, MLB, NHL, NCAA football, NCAA basketball and Premier League.
- Team names, abbreviations and the canonical espn.com game URL.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `league`, `id`, `url` | League code, ESPN game id and canonical game page |
| `date`, `name`, `shortName` | Kickoff/start time (ISO), full and short matchup names |
| `state`, `statusDetail`, `completed` | `pre`/`in`/`post`, human status text, whether the game is over |
| `venue`, `venueCity` | Where the game is played |
| `homeTeam`, `homeTeamAbbreviation`, `homeScore` | Home side |
| `awayTeam`, `awayTeamAbbreviation`, `awayScore` | Away side |
| `winner` | `home`, `away` or `null` before the game ends |
| `broadcast` | TV/streaming network |
| `odds` | `null`, or `{ provider, details, spread, overUnder, moneylineHome, moneylineAway, favorite }` |

## Use cases

- **Track live and final scores.** Pull recent and in-progress games with the full score, venue and broadcast.
- **Watch upcoming games and odds.** Get scheduled games with pre-match spread, moneyline and total before they start.
- **Feed a scores widget or alert.** Run daily and get every game of the day for a league in one call.
- **Build a multi-league dataset.** Run the same Actor once per league to compare schedules, scores and odds side by side.

## Input

| Field | What it does |
|---|---|
| `league` | `nfl`, `nba`, `wnba`, `mlb`, `nhl`, `ncaaf`, `ncaab` or `eng.1` (Premier League). |
| `mode` | `results` reads games going backward from today, with final or live scores. `upcoming` reads games going forward from today, with pre-match odds when published. |
| `days` | How many calendar days to read (default 14). |
| `maxItems` | The run stops once this many games are saved. |

## Three ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/espn-scores-scraper) and click **Try for free** (a free Apify account is enough).
2. Pick a league and mode, then click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily feed, open **Schedules**, create a daily schedule for the Actor and, optionally, add an integration that sends new games to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/espn-scores-scraper').call({
    "league": "nfl",
    "mode": "results",
    "days": 14,
    "maxItems": 50
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.shortName} | ${item.awayScore}-${item.homeScore} | ${item.statusDetail}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/espn-scores-scraper").call(run_input={
    "league": "nfl",
    "mode": "results",
    "days": 14,
    "maxItems": 50,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{item['shortName']} | {item.get('awayScore')}-{item.get('homeScore')} | {item.get('statusDetail')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

## Pricing

Pay per result: **$0.60 per 1,000 games** (that is $0.0006 per game), plus a tiny start fee of $0.00005 per run. You pay only for the results saved to the dataset. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/espn-scores-scraper) when this guide was written; the Store page is the reference.

## Limits and honest notes

- `odds` is `null` until a sportsbook has posted a line for the game, and is never backfilled for games already finished.
- `winner` is `null` until the game is `completed`; `homeScore`/`awayScore` are `0` before the game starts.
- Only league, team and game data is collected: no player or fan personal data of any kind.
- This is an unofficial tool, not affiliated with ESPN. Check the site terms that apply to your use.

## FAQ

**Does it need a browser or a proxy?**  
No. It reads ESPN's own public JSON scoreboard API directly, so runs are fast and cheap.

**How do I get several leagues at once?**  
Each league is a separate ESPN endpoint, so `league` only takes one value per run. Run the Actor once per league and merge the datasets, or schedule one run per league.

**How do I only get today's games?**  
Set `days` to `1`.

**Can I get the data in Excel or Google Sheets?**  
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open espn-scores-scraper on the Apify Store](https://apify.com/bibian/espn-scores-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
