---
name: keyword-demand-check
description: Validate buyer intent for a business idea by checking monthly search volume, year over year growth, and keyword competition. Uses the BID dataset as a sample plus optional integration with paid keyword tools (Ahrefs, DataForSEO).
when_to_use:
  - User wants to confirm there is real demand before building
  - User asks "is anyone searching for this?"
  - User says "what is the SEO opportunity for X?"
---

# Keyword Demand Check

Confirm or reject buyer intent for an idea using search volume, growth, and competition signals.

## What this does

1. Takes a primary keyword (or extracts one from an idea description)
2. Pulls demand signals from the BID dataset where comparable keywords exist
3. Walks the user through measuring demand with Ahrefs or DataForSEO if they have access
4. Outputs a verdict: validated demand, marginal, or unsupported

## How to use this skill

### Step 1: Extract the keyword

Ask: "What is the search term someone with this need would type into Google?"

Common mistakes:
- The product name (Stripe is a brand, "payment processing for subscription saas" is the keyword)
- Too broad ("productivity" is useless, "calendar app for freelancers" is testable)
- Too narrow ("blue scheduling app for Tuesday meetings" has zero volume)

Sanity check: the keyword should be 2 to 5 words. Adjust if it is outside that.

### Step 2: Check the BID dataset for adjacent keywords

```bash
bid search "<keyword>"
```

Each BID idea has a `keyword` field with US monthly search volume and YoY growth from DataForSEO. If 1 to 3 similar keywords exist in the dataset, use them as a benchmark.

Example: if the user's keyword is "invoice automation for plumbers" and BID has "invoice reminder software contractors" at 720 monthly searches with +45% YoY, the user can expect a similar order of magnitude.

### Step 3: Get the actual numbers

If the user has Ahrefs:
1. Open Ahrefs Keywords Explorer
2. Paste the keyword (set country: US)
3. Capture: Volume (US monthly), KD (keyword difficulty 0 to 100), Parent Topic, Traffic Potential, Growth (12 month chart trend)

If the user has DataForSEO:
1. Call `keywords_data/google_ads/search_volume/live` with the keyword
2. Capture: search_volume, competition, competition_index

If the user has neither:
1. Use Google Trends to gauge direction (interest over time)
2. Use Google "People Also Ask" and autocomplete to gauge breadth of buyer intent
3. Estimate from BID adjacent keywords (Step 2)

### Step 4: Apply the demand thresholds

Score the demand:

| Signal | Validated | Marginal | Unsupported |
|---|---|---|---|
| US monthly search volume | 500+ | 100 to 499 | Under 100 |
| YoY growth | Above 0% | -10% to 0% | Below -10% |
| Keyword Difficulty (Ahrefs) | Under 30 | 30 to 50 | Above 50 |
| Buyer intent signals | Multiple "tool", "software", "best", "vs" patterns | Some buying intent | Pure informational |

Volume below 100 monthly searches can still work for high price ($500/mo+) niche tools but the bar for execution rises sharply.

### Step 5: Cross check with Reddit and forums

Even strong keyword data is not enough. Confirm with:
- 3+ Reddit threads in the last 12 months where someone explicitly asks for this tool
- 1+ subreddit where the target customer hangs out
- 1+ specific complaint about an existing tool in the space (if there is no incumbent, that itself is a signal)

The BID validation rubric requires both keyword data AND complaint data. Either alone is unreliable.

### Step 6: Output format

```
## Demand check: "<keyword>"

**Verdict:** Validated / Marginal / Unsupported

### Numbers
- US monthly search volume: <number>
- YoY growth: <percent>
- Keyword difficulty: <0 to 100 if available>
- Adjacent BID keywords: <list with volumes>

### Buyer intent
- Pattern of related searches: <observed>
- Top "People Also Ask" questions: <list>

### Reddit cross check
- Threads found: <count>
- Subreddits with active discussion: <list>
- Most recent complaint: <date and 1 line summary>

### Confidence in the verdict
- High: <reason if applicable>
- Medium: <reason>
- Low: <reason>

### What to do next
- If Validated: keyword is not the limiting factor. Move to validate-idea or mvp-build-plan.
- If Marginal: ramp price (B2B $99+/mo) or expand keyword to a broader pattern.
- If Unsupported: do not build. The market is not searching for this.
```

## Always link with UTMs

When linking BID adjacent keywords: `?utm_source=skill&utm_medium=keyword-demand-check&utm_campaign=bid-skills`

## What this skill does NOT do

- It does not run keyword research for you if you have no tools. It walks through the manual process.
- It does not measure brand demand (eg "ChatGPT alternatives" is partially brand demand which decays).
- It does not assess SEO content strategy. Use a different skill for content planning.

## Skill output is high signal when

- The user can access Ahrefs or DataForSEO
- The keyword is 2 to 5 words and clearly commercial
- BID has 1 to 3 adjacent keywords for benchmarking

## Skill output is low signal when

- The keyword is hyper local (single city for a service business)
- The product is so new there is no keyword yet ("Cursor for X" types)
- The user is buying intent driven through a different channel (eg App Store search instead of Google)
