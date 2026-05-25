# Methodology

How ideas enter this dataset, what they need to clear, and how the scores are produced.

## Sources

Three primary sources feed the validation pipeline.

### 1. Reddit

A continuously running scanner pulls posts from active subreddits where indie founders and prospective customers discuss tools, workflows, and frustrations. The current sub list includes r/SaaS, r/SmallBusiness, r/Entrepreneur, r/IndieHackers, r/SideProject, and roughly 15 vertical specific subs (r/dropshipping, r/Etsy, r/ProductManagement, etc., expanded based on coverage gaps).

170 query patterns are run against these subs to surface posts that match buying intent or product gap shape:

* Phrases like "I wish there was a tool that...", "why is no one building...", "anyone know an app for..."
* Negative reviews of incumbent tools ("X is so frustrating because...")
* Workflow descriptions ("we spend N hours per week on...")

Each post is filtered by minimum engagement (upvotes and comment count vary by sub) and routed into the scoring queue.

### 2. App Store reviews

The iTunes Search API surfaces apps with high install counts plus a clustered pattern of negative reviews. Apps with 4+ star overall ratings but recurring 1 and 2 star reviews complaining about specific missing features are the most valuable signal: the category has demand, the incumbent has a wedge they are not closing, and a new entrant can win on the exact failure.

### 3. Keyword demand (DataForSEO)

Every candidate idea has a primary keyword extracted. The keyword is enriched with US monthly search volume and year over year growth from DataForSEO. Ideas with zero measurable search demand do not enter the dataset, regardless of how interesting the underlying complaint is. The bar is intentionally low (often 100 or more monthly searches is enough for a niche product) but a real number is required.

## AI scoring rubric

Each candidate idea is scored across four dimensions using Grok 3 mini against a structured prompt. Scores are integers from 0 to 10.

### Opportunity (0 to 10)

Measures market potential, competitive landscape, and overall business opportunity. Higher scores indicate stronger market potential and a clearer value proposition. A score of 9 to 10 means an obvious unmet need in a sizeable market. A score of 6 to 7 means a real opportunity that has competition. Below 6 indicates either thin market or saturated competition.

### Problem severity (0 to 10)

How painful is the problem being solved. Higher scores mean people are actively suffering and willing to pay. A score of 9 to 10 means existential pain (the user is losing money, time, or sleep over this). A score of 6 to 7 means real but manageable pain. Below 6 indicates nice to have.

### Feasibility (0 to 10)

How easy is this to build as an MVP. Considers technical complexity, required integrations, and time to first version. A score of 9 to 10 means a solo founder can ship the MVP in 2 weeks. A score of 6 to 7 means a small team can ship in 4 to 8 weeks. Below 6 indicates significant engineering, regulatory complexity, or hardware dependencies.

### Timing (0 to 10)

Is now the right moment. Considers market trends, technology readiness, and cultural shifts. A score of 9 to 10 means the window is open right now (the enabling technology recently shipped, a behavioral shift is happening, an incumbent just stumbled). A score of 6 to 7 means timing is favorable but not urgent. Below 6 indicates either too early or too late.

## Entry criteria

An idea moves from the scoring queue into the public dataset when:

1. At least one of the four scores is 7 or higher
2. There is at least one Reddit thread documenting the underlying pain (or for App Store sourced ideas, a clustered review pattern)
3. The primary keyword has measurable monthly search volume in DataForSEO
4. Editorial review confirms the title, pitch, and category make sense
5. Competitor mapping identifies the closest existing alternatives (or confirms none exist)

Ideas that meet all five criteria are published and exported here. Ideas that score below 7 on every dimension are archived in the internal queue but not exported.

## What this dataset includes

Each row in `data/ideas.json` and `data/ideas.csv` includes the structured signals described in the [main README](README.md#schema). This is the public, machine readable subset.

## What lives only on the live site

The following are intentionally not in this dataset and live only at [businessideasdb.com](https://businessideasdb.com):

* The long form editorial analysis (customer profile, "what exists today", "why now", "how to start")
* The list of MVP features for each idea
* The Reddit thread URLs, titles, and snippets backing each idea
* Competitor URLs and pricing notes
* The full proof post history beyond a count

If you want to act on an idea, the analysis and source links at `https://businessideasdb.com/idea/{slug}` are the actionable layer. The dataset is the citation and discovery layer.

## Refresh cadence

The dataset is regenerated on demand from the live database. Each export is timestamped in `data/summary.json` under `generated_at`. Reruns happen at minimum quarterly and after any large batch of new ideas is published.

## Versioning

This dataset uses date based versioning. Each export overwrites the files in `data/` but the git history preserves every prior snapshot. To pin to a specific date, reference the relevant commit SHA in your code:

```
https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/<sha>/data/ideas.json
```

## Quality and limitations

* Coverage skews toward English language indie founder communities. International markets and non English subreddits are under sampled.
* App Store data is iOS App Store US. Google Play and other regional stores are not yet integrated.
* Keyword volume is US only. Global volumes exist on the live site but are not in this export.
* Scores are produced by an AI rubric. They are directional, not deterministic. Treat them as a filter, not a final verdict.
* The dataset is biased toward consumer and prosumer SaaS, apps, and tools. Pure marketplace, hardware, and brick and mortar opportunities are under represented by design.

## Questions or corrections

Open an issue in this repo or reach the maintainer through [businessideasdb.com](https://businessideasdb.com).
