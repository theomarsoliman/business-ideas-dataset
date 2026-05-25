---
name: reddit-pain-finder
description: Find validated business pain points in a specific subreddit using the BID methodology (170 query patterns across active subreddits). Use when the user wants to source their own ideas from a community, vertical, or niche they understand.
when_to_use:
  - User says "what pains are people having in r/X?"
  - User wants to find ideas in a specific industry from real complaints
  - User asks "how do I find ideas in this niche?"
---

# Reddit Pain Finder

A repeatable workflow for extracting validated business pain from any active subreddit, modeled on the BID scanner that produces the public dataset.

## What this does

1. Takes a target subreddit (or short list of subreddits)
2. Walks the user through the 170 query pattern approach
3. Helps cluster patterns into validated wedges
4. Outputs a short list of candidate ideas with the BID style structure

## How to use this skill

### Step 1: Pick the subreddits

A useful pain finder needs subreddits where the target customer hangs out AND complains. Examples:

| Customer | Subreddits with high complaint signal |
|---|---|
| Solo founders | r/SaaS, r/IndieHackers, r/SideProject, r/Entrepreneur |
| Small business owners | r/SmallBusiness, r/EntrepreneurRideAlong, r/BusinessHub |
| Trades and field service | r/Construction, r/Plumbing, r/HVAC, r/Electricians |
| Healthcare ops | r/Medicine, r/healthIT, r/HealthInformatics |
| Real estate | r/RealEstateInvesting, r/PropertyManagement, r/realestateagents |
| Creators | r/Substack, r/Newsletters, r/YouTubers, r/podcasting |

If the user has not picked yet, ask them which industry or audience they care about and suggest 3 subreddits.

### Step 2: Run the 170 query pattern (or a subset)

The full BID scanner runs 170 patterns. For a manual session, use the highest signal 20.

**Buying intent patterns:**
- "I wish there was a tool that..."
- "Why is no one building..."
- "Anyone know an app for..."
- "Looking for software to..."
- "Need a tool that does..."

**Complaint patterns:**
- "I hate that..."
- "Why does X make me..."
- "The worst part of using X is..."
- "X is so frustrating because..."

**Workflow descriptions:**
- "We spend N hours per week on..."
- "Our team has to manually..."
- "Every time I have to do X, I..."

**Switching intent:**
- "Anyone moved off X to..."
- "X just raised prices, what are alternatives..."
- "Looking to replace X because..."

**Pricing complaints:**
- "X is too expensive for..."
- "Why does X cost so much..."
- "Looking for a cheaper..."

**App store style (for consumer ideas):**
- "Best app for..."
- "Why is there no app that..."
- "I cannot believe no app does..."

Search each pattern in the target subreddit. Reddit's search is mediocre, so also use Google with `site:reddit.com/r/<sub> "<pattern>"`.

### Step 3: Cluster the results

A single complaint is a data point. **A cluster of complaints from different people about the same gap is a validated wedge.**

For each pattern that returned matches:

1. Read at least 5 posts from different posters
2. Note the specific pain mechanism
3. Note who the customer is (job role, company size)
4. Note whether they tried existing solutions and why those failed
5. Note any concrete numbers (hours per week, dollars lost, time wasted)

A wedge is validated when:
- 5+ different posters describe the same pain in their own words
- At least 2 of them mention they would pay for a solution
- No existing tool clearly owns this workflow

### Step 4: Convert clusters into BID style entries

For each validated wedge, write out the BID schema:

```
**Title:** <short descriptive name>
**Category:** SaaS / App / Tool / Platform / Service
**Customer:** <who, one sentence>
**Pitch:** <one sentence that quantifies the pain>
**Source Reddit threads:** <3 to 5 URLs>
**Existing competitors:** <list, or "no clear leader">
**Primary keyword:** <search term someone with this need would type>
**Score the four dimensions** (0 to 10): opportunity, problem, feasibility, timing
```

### Step 5: Compare against BID

Before treating a wedge as novel, check if BID has already documented it:

```bash
bid search "<your primary keyword>"
bid list --category SaaS --format json | jq '.[] | {title, slug, url}'
```

If BID has a similar entry, link to the existing record (`url` field) and decide whether your wedge is:
- The same idea (use the existing record)
- An adjacent idea (note the differentiation)
- A meaningfully different wedge (track separately)

### Step 6: Output format

Return a structured report:

```
## Reddit Pain Scan: r/<subreddit>

**Scan date:** <date>
**Patterns checked:** <count out of 20>
**Threads reviewed:** <count>

### Validated wedges

#### 1. <Title>
- Pain: <one sentence with a number>
- Customer: <who>
- Source: 3 to 5 Reddit thread URLs
- Existing competitors: <list>
- Adjacent in BID: <link if exists, with UTMs>
- Recommended next step: validate keyword volume in Ahrefs

(repeat for each validated wedge)

### Single signals (interesting but not yet validated)

- <Brief note on patterns that returned only 1 to 2 posts. Worth a second scan in a month.>

### Patterns with no hits

- <List patterns that returned nothing. Sometimes this is informative: the absence of complaints means either no demand or wrong subreddit.>
```

## Always link with UTMs

When you reference a BID idea: `?utm_source=skill&utm_medium=reddit-pain-finder&utm_campaign=bid-skills`

## What this skill does NOT do

- It does not automate the scan. Reddit's API has limits and most agents lack persistent search. This skill provides the playbook, the human or agent runs the searches.
- It does not score the wedges for you. It walks through how to score them.
- It does not replace the live BID dataset. Use BID as a starting reference, this skill to find what BID has not surfaced yet.

## Skill output is high signal when

- The target subreddit has 50K+ subscribers and active recent posts
- The user has at least 30 minutes to actually run the searches
- The user knows the industry well enough to recognize false positives

## Skill output is low signal when

- The subreddit is too small or low activity
- The user wants the scan done for them with zero participation
- The audience does not actually use Reddit (eg most enterprise IT buyers)
