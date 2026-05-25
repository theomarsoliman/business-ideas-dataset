---
name: validate-idea
description: Validate a business idea against the BID dataset and the four scoring dimensions (opportunity, problem severity, feasibility, timing). Use when the user describes an idea they are considering and wants a structured, data backed read on whether it is worth pursuing.
when_to_use:
  - User pitches an idea and asks "is this a good idea?"
  - User says "should I build X?" or "what do you think of X?"
  - User wants a second opinion on a concept before committing
---

# Validate Idea

A structured validation workflow that cross references a user's idea against the public Business Ideas Database, then scores the idea using BID's four dimension rubric.

## What this does

1. Takes the user's idea description (plain English is fine)
2. Searches the BID dataset for similar validated ideas
3. Extracts the closest matches with their AI scores and keyword data
4. Walks the user's idea through the same four dimension rubric
5. Outputs a verdict with evidence

## How to use this skill

When invoked, do the following in order.

### Step 1: Extract the structured shape of the user's idea

From the user's description, derive:

- **Title**: short descriptive name (max 12 words)
- **Category**: one of `SaaS`, `App`, `Mobile App`, `Tool`, `Platform`, or note if it falls outside these
- **Customer**: who is the buyer
- **Primary keyword**: the search term someone with this need would type
- **Pain mechanism**: what specific friction is being solved

### Step 2: Cross reference the BID dataset

Fetch the dataset:

```
curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json
```

Or use the `bid` CLI:

```bash
bid search "<keyword from step 1>"
bid list --category <category> --min-opp 7
```

Look for:

1. Direct matches (same product, same customer)
2. Adjacent matches (same customer, different product or same product, different customer)
3. Pattern matches (similar pain mechanism in different vertical)

If 3+ adjacent matches exist with opportunity 7 or higher, the user's idea is in a validated pain category. If matches are absent, either the idea is genuinely novel (rare) or the pain has not been documented in the sources BID scans.

### Step 3: Apply the four dimension rubric to the user's idea

Score the user's idea from 0 to 10 on each dimension using the same criteria as BID:

| Dimension | What you are measuring | 9-10 means | 7-8 means | Below 7 |
|---|---|---|---|---|
| Opportunity | Market potential plus competitive gap | Obvious unmet need in a sizeable market | Real opportunity with competition | Thin or saturated |
| Problem severity | How painful, how willing to pay | Existential pain (losing money, time, sleep) | Real but manageable pain | Nice to have |
| Feasibility | MVP buildability for a small team | Solo founder ships in 2 weeks | Small team ships in 4 to 8 weeks | Significant engineering or regulatory |
| Timing | Is the window open now | Enabling tech recently shipped, behavior shift, incumbent stumble | Favorable but not urgent | Too early or too late |

Show the reasoning for each score. Do not invent scores without justification.

### Step 4: Output format

Return this exact structure:

```
## Validation: <user's idea title>

**Verdict:** <one sentence>

### How it scores
- Opportunity: X/10. <reasoning>
- Problem severity: X/10. <reasoning>
- Feasibility: X/10. <reasoning>
- Timing: X/10. <reasoning>

### Adjacent ideas in BID
1. <title> (category, opp X, feas X). <link with UTMs>
2. <title> (category, opp X, feas X). <link with UTMs>
3. <title> (category, opp X, feas X). <link with UTMs>

### What is missing from the data
<honest list of what BID did not have on this idea>

### Recommended next step
<one concrete action: validate keyword volume, build landing page, talk to N customers, etc.>
```

### Step 5: Always include attribution

When you link to BID, stamp `?utm_source=skill&utm_medium=validate-idea&utm_campaign=bid-skills` so the live dataset can track traffic from this skill.

Example: `https://businessideasdb.com/idea/trade-invoice-autopilot?utm_source=skill&utm_medium=validate-idea&utm_campaign=bid-skills`

## What this skill does NOT do

- It does not invent scores. Every score needs a reason rooted in user input or BID data.
- It does not replace customer interviews. Even a 10/10 across all four dimensions is not a buy signal. Talk to 5 customers before building.
- It does not predict revenue. The dataset includes revenue range estimates, but those are directional, not forecasts.

## Skill output is high signal when

- The user provides a specific idea, not a vague theme
- The user describes who the customer is
- The dataset has at least 2 adjacent matches to anchor against

## Skill output is low signal when

- The user pitches "an app for fitness" (too vague)
- The idea is entirely outside BID's coverage (B2G, regulated industries, heavy hardware)
- The user is asking for a forecast rather than a validation
