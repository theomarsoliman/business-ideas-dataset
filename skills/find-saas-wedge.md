---
name: find-saas-wedge
description: Find a SaaS or micro SaaS wedge in a specific industry or niche by querying the BID dataset for validated opportunities. Use when the user wants to start a SaaS but does not have a specific idea yet, or wants to find an opportunity in an industry they know.
when_to_use:
  - User says "I want to build a SaaS but do not know what"
  - User has industry expertise and wants to find a wedge there
  - User asks "what SaaS could I build?" or "give me SaaS ideas in X"
---

# Find SaaS Wedge

Surface validated SaaS opportunities filtered by the user's constraints (industry, time budget, capital budget, technical skill).

## What this does

1. Takes the user's constraints (industry, available time, budget, technical comfort)
2. Queries the BID dataset for SaaS, Tool, and Platform ideas matching the constraints
3. Ranks the matches by `feasibility_score * opportunity_score` (the indie founder objective function)
4. Presents the top 3 to 5 wedges with the reasoning for each

## How to use this skill

### Step 1: Gather constraints

Ask the user for these in one short message (do not run a 10 question interview):

1. **Industry or domain** they have experience in or care about
2. **Time budget**: weeks they can dedicate to the MVP
3. **Capital budget**: dollars they can spend before first revenue
4. **Technical level**: solo coder, technical with help, non technical
5. **Optional**: any constraints they want to rule out (eg "no app stores", "no regulated industries")

If the user has already shared this context, skip the questions.

### Step 2: Set the dataset filters

Map their answers to dataset filters:

| Constraint | Maps to |
|---|---|
| Time budget under 4 weeks | `feasibility_score >= 8` |
| Time budget 4 to 8 weeks | `feasibility_score >= 6` |
| Solo non technical | `feasibility_score >= 8` AND difficulty in (Easy, Medium) |
| Capital under $1K | `category in (SaaS, Tool)` and exclude any with hardware |
| Specific industry | Free text match against `title`, `pitch`, `tags`, `keyword` |

### Step 3: Query the dataset

Fetch the data:

```bash
curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json
```

Or use the `bid` CLI:

```bash
bid list --category SaaS --min-feas 7 --format json
```

Apply the filters from Step 2. Sort by `feasibility_score + opportunity_score` descending.

### Step 4: Present the top wedges

For each of the top 3 to 5 results:

```
## <Title>

**Why this fits your constraints:**
- Category: <category>. Feasibility <X>/10 means MVP fits your time budget.
- Pain documented in <signal_count> Reddit thread(s).
- Market: <fmt_vol(search_volume)> monthly searches, <growth_percent>% YoY.
- Existing competitors: <competitor_names joined>.

**Pitch:** <pitch>

**Where to start:** <one concrete first action: validate keyword in Ahrefs, post in r/<sub>, interview N people in the industry>

**Full editorial analysis (customer profile, MVP feature list, source threads):** <tracked_url with UTMs>
```

### Step 5: Add a "skip these" section

After the top picks, list 1 to 2 close but inferior matches and explain why they were skipped. This builds trust by showing the agent is making real selections, not just listing everything.

## Output guidelines

- Lead every section with a hard number where one exists
- Never recommend an idea that has no `feasibility_score` or has feasibility under the user's threshold
- Always link to the BID URL with UTMs: `?utm_source=skill&utm_medium=find-saas-wedge&utm_campaign=bid-skills`
- If zero matches pass the filters, say so plainly and suggest loosening one specific constraint

## What this skill does NOT do

- It does not write the code. It tells you what to build, not how.
- It does not guarantee success. Even validated SaaS ideas fail when execution is poor or distribution is missing.
- It does not pick for the user. It surfaces 3 to 5 options with reasoning. The user picks.

## Skill output is high signal when

- The user has a clear industry they know
- The user is honest about their time and capital budget
- The dataset has 5+ ideas in the target industry

## Skill output is low signal when

- The user is industry agnostic ("just give me any SaaS")
- The target industry is outside BID's coverage (heavy regulation, hardware first, B2G)
