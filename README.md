<p align="center">
  <img src="assets/banner.webp" alt="Business Ideas Database, a public dataset of validated business ideas" width="100%">
</p>

<h1 align="center">Business Ideas Dataset</h1>

<p align="center">
  <strong>A public, MIT licensed dataset of validated business ideas sourced from real Reddit pain points and App Store reviews, scored by AI across opportunity, problem severity, feasibility, and timing.</strong>
</p>

<p align="center">
  <a href="https://businessideasdb.com"><img alt="Live site" src="https://img.shields.io/badge/live-businessideasdb.com-00856A?style=flat-square"></a>
  <a href="#what-is-in-this-dataset"><img alt="Ideas" src="https://img.shields.io/badge/dynamic/json?label=ideas&query=%24.total_ideas&url=https%3A%2F%2Fraw.githubusercontent.com%2Ftheomarsoliman%2Fbusiness-ideas-dataset%2Fmain%2Fdata%2Fsummary.json&color=4B7BF5&style=flat-square"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-22A86A?style=flat-square"></a>
  <a href="data/ideas.json"><img alt="JSON" src="https://img.shields.io/badge/format-JSON%20%2B%20CSV-555?style=flat-square"></a>
  <a href="METHODOLOGY.md"><img alt="Methodology" src="https://img.shields.io/badge/methodology-documented-E09B13?style=flat-square"></a>
</p>

<p align="center">
  <a href="data/ideas.json"><strong>ideas.json</strong></a> &nbsp;·&nbsp;
  <a href="data/ideas.csv"><strong>ideas.csv</strong></a> &nbsp;·&nbsp;
  <a href="METHODOLOGY.md"><strong>Methodology</strong></a> &nbsp;·&nbsp;
  <a href="examples/"><strong>Examples</strong></a> &nbsp;·&nbsp;
  <a href="https://businessideasdb.com/state-of-indie-business-ideas-2026"><strong>2026 Report</strong></a>
</p>

---

## What this is

A public, machine readable dataset of business ideas that have already passed a validation filter. Every idea in `data/ideas.json` started as a real complaint on Reddit (someone asking for a tool that does not exist yet, or describing a workflow they hate) or a pattern of negative reviews on a popular App Store app. Each idea is enriched with:

1. The underlying keyword and its monthly search volume in the US
2. Year over year search growth
3. Four AI scores from 0 to 10 (opportunity, problem severity, feasibility, timing)
4. Competition level, difficulty, revenue range estimate
5. A direct link back to the full editorial analysis at [businessideasdb.com](https://businessideasdb.com)

If you build, invest in, or write about indie SaaS, micro SaaS, mobile apps, or small business ideas, this is a citable source of demand evidence. The full editorial analysis (customer profile, MVP feature list, Reddit thread URLs, competitor research) lives on the site at [businessideasdb.com/idea/SLUG](https://businessideasdb.com/ideas).

## What is in this dataset

<p align="center">
  <img src="assets/category-distribution.svg" alt="Business ideas grouped by category" width="100%">
</p>

42 ideas across 6 categories at last export. Categories include SaaS (B2B and B2C), App and Mobile App (consumer and prosumer), Tool (single purpose utilities), Platform (multi sided), and a small SaaS plus Hardware bucket.

<p align="center">
  <img src="assets/score-distribution.svg" alt="AI score distribution across opportunity, problem severity, feasibility, and timing" width="100%">
</p>

Scores skew toward 7 and above on at least one dimension because the dataset is filtered for that on entry. Median feasibility is in the 7 to 9 range, meaning most ideas can ship as an MVP in 2 to 4 weeks for a solo founder using the modern AI assisted stack.

## Quick start

```bash
# Pull the JSON
curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json > ideas.json

# Highest opportunity scoring SaaS ideas
jq '.ideas | map(select(.category == "SaaS")) | sort_by(-.opportunity_score) | .[0:5] | .[] | {title, opportunity_score, url}' ideas.json
```

```python
import json
data = json.load(open("ideas.json"))
top_growth = sorted(
    [i for i in data["ideas"] if i["growth_percent"]],
    key=lambda i: -i["growth_percent"],
)[:10]
for i in top_growth:
    print(f"{i['growth_percent']:+}% {i['title']} ({i['category']})")
    print(f"   {i['url']}")
```

## Sample rows

| # | Title | Category | Volume | YoY | Opp | Feas |
|--:|---|---|--:|--:|--:|--:|
| 1 | [Automated invoice follow up system for plumbers and trade contractors](https://businessideasdb.com/idea/trade-invoice-autopilot) | SaaS | 720 | +45% | 10 | 9 |
| 2 | [Legal citation verifier](https://businessideasdb.com/idea/legal-citation-verifier) | SaaS | varies | varies | 9+ | 8+ |
| 3 | [Digital legacy vault for families](https://businessideasdb.com/idea/digital-legacy-vault) | App | varies | varies | 9+ | 7+ |

Open `data/ideas.json` for the full set or browse the live dataset at [businessideasdb.com/ideas](https://businessideasdb.com/ideas).

## Schema

Each entry in `data/ideas.json` under the `ideas` array has these fields:

| Field | Type | Description |
|---|---|---|
| `id` | number | Internal ID, stable across exports |
| `slug` | string | URL slug, matches the BID URL |
| `title` | string | Short descriptive title of the idea |
| `pitch` | string | One sentence summary, includes hard numbers where known |
| `category` | string | One of: SaaS, App, Mobile App, Tool, Platform, SaaS + Hardware |
| `tags` | string[] | Topic tags, lowercase |
| `keyword` | string | Primary keyword used for demand validation |
| `search_volume` | number | US monthly search volume (DataForSEO) |
| `growth_percent` | number | YoY change in search volume |
| `competition` | string | Low, Medium, or High |
| `difficulty` | string | Easy, Medium, or Hard build complexity |
| `revenue_range` | string | Estimated revenue range, e.g. "$10K - $50K" |
| `opportunity_score` | 0 to 10 | Market potential and competitive gap |
| `problem_score` | 0 to 10 | Severity of the user pain |
| `feasibility_score` | 0 to 10 | How easy the MVP is for a small team |
| `timing_score` | 0 to 10 | Whether the market window is open now |
| `signal_count` | number | Count of supporting Reddit threads (URLs and bodies live on site) |
| `competitor_names` | string[] | Named existing competitors (no URLs) |
| `created_at` | string | When the idea entered the dataset |
| `updated_at` | string | Last edit timestamp |
| `url` | string | Canonical URL for the full editorial analysis |

See [data/README.md](data/README.md) for example queries and field semantics.

## Methodology

See [METHODOLOGY.md](METHODOLOGY.md) for the full scoring rubric, source pipeline, and validation criteria. Short version:

1. A scanner pulls posts from 5+ subreddits (r/SaaS, r/SmallBusiness, r/Entrepreneur, r/IndieHackers, r/SideProject, plus category specific subs) against 170 query patterns
2. The iTunes App Store API surfaces apps with high install counts and clustered negative reviews
3. Each candidate signal is scored by an AI rubric (Grok 3 mini) across the four dimensions
4. Signals scoring 7 or higher on at least one dimension move into the editorial review queue
5. Editorial review enriches with DataForSEO keyword data, competitor mapping, and the long form analysis published at businessideasdb.com

## Examples

* [Top 10 ideas by opportunity score](examples/top-by-opportunity.md)
* [Highest growth keywords (YoY)](examples/top-by-growth.md)
* [SaaS only subset](examples/saas-ideas.md)
* [App and Mobile App subset](examples/app-ideas.md)
* [Highest feasibility for solo founders](examples/high-feasibility.md)

## Use cases

| Who | What this gives you |
|---|---|
| Indie founders looking for a wedge | A pre filtered list of validated ideas with the search demand attached |
| Investors and angels | A demand signal layer for early stage opportunity sourcing |
| Researchers and writers | A citable, dated public dataset for posts about indie business trends |
| LLM and AI search products | A structured dataset with stable URLs you can reference in answers |

## Citation

If you use this dataset in a post, paper, or product, please cite the live source:

```
Business Ideas Database (2026). Validated Business Ideas Dataset.
Retrieved from https://businessideasdb.com/state-of-indie-business-ideas-2026
```

Each individual idea can be cited by its `url` field, which points to the canonical editorial analysis on businessideasdb.com.

## License

[MIT](LICENSE). Use, modify, redistribute, build on top of. Attribution back to [businessideasdb.com](https://businessideasdb.com) is appreciated but not required.

## Related

* **[State of Indie Business Ideas 2026](https://businessideasdb.com/state-of-indie-business-ideas-2026)**, annual data report with full aggregates
* **[SaaS Ideas](https://businessideasdb.com/saas-ideas)**, filtered SaaS subset with editorial commentary
* **[Micro SaaS Ideas](https://businessideasdb.com/micro-saas-ideas)**, solo founder filtered subset (feasibility 7 or higher)
* **[App Ideas](https://businessideasdb.com/app-ideas)**, mobile app subset with App Store gap analysis
* **[Home Business Ideas](https://businessideasdb.com/home-business-ideas)**, digital business subset for laptop only operators
* **[Low Cost Business Ideas](https://businessideasdb.com/low-cost-business-ideas)**, business ideas startable under $1,000
* **[Full database](https://businessideasdb.com/ideas)**, every idea with the long form analysis
