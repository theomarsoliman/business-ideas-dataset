# Data directory

Three files, same dataset, three shapes.

## Files

* **`ideas.json`** is the primary data file. It contains a `meta` object with summary info plus an `ideas` array with one entry per validated business idea. See the [schema in the main README](../README.md#schema).
* **`ideas.csv`** is the same data flattened to CSV. Array fields (`tags`, `competitor_names`) are joined with `|`.
* **`summary.json`** is a small metadata file with totals and categories. Useful as a lightweight ping target (the shields.io badge in the main README pulls from it).

## Example queries

### Get the top 10 ideas by composite score

```bash
jq '.ideas | map({title, score: (.opportunity_score + .problem_score + .feasibility_score + .timing_score), url, category}) | sort_by(-.score) | .[0:10]' ideas.json
```

### Filter for solo founder friendly SaaS

```bash
jq '.ideas | map(select(.category == "SaaS" and .feasibility_score >= 7)) | sort_by(-.opportunity_score) | .[] | {title, opportunity_score, feasibility_score, url}' ideas.json
```

### Find ideas with rising search demand

```bash
jq '.ideas | map(select(.growth_percent != null and .growth_percent > 20)) | sort_by(-.growth_percent) | .[] | {title, growth_percent, keyword, url}' ideas.json
```

### Python: cluster by category, average opportunity

```python
import json
from collections import defaultdict
from statistics import mean

ideas = json.load(open("ideas.json"))["ideas"]
by_cat = defaultdict(list)
for i in ideas:
    if i["opportunity_score"] is not None:
        by_cat[i["category"]].append(i["opportunity_score"])

for cat, scores in sorted(by_cat.items(), key=lambda x: -mean(x[1])):
    print(f"{cat:25s} mean opp {mean(scores):.1f}  n={len(scores)}")
```

### Python: pull full editorial analysis for each idea

```python
import json, urllib.request

ideas = json.load(open("ideas.json"))["ideas"]
for i in ideas[:5]:
    print(i["title"])
    print(f"  Full analysis: {i['url']}")
```

## Field semantics, common gotchas

* `growth_percent` is year over year change in US monthly search volume. Negative values mean the keyword is in decline.
* `feasibility_score` of 7 or higher correlates roughly with "shippable as an MVP by a solo founder in 2 to 4 weeks using the modern AI assisted stack". This is the most useful filter for indie builders.
* `competition: "Low"` means the SERP and the App Store both have weak incumbents. `Medium` means established players exist but with visible gaps. `High` means a clear leader owns the space.
* `signal_count` is the number of Reddit threads supporting the idea. Higher is better (more independent confirmations of the pain). The thread URLs and content live only on the live site.
* `revenue_range` is an estimated range based on incumbent revenue and addressable demand. Treat as directional.
* `competitor_names` is just names. Pricing, URLs, and notes live on the live site.

## How to refresh

The dataset is regenerated from the live database on demand. The regeneration script lives in the parent project. Each refresh updates the three files above and bumps `summary.json.generated_at`.
