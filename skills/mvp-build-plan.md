---
name: mvp-build-plan
description: Generate a concrete 2 to 4 week MVP build plan for a specific business idea. Takes either a BID idea slug or a freeform idea description and produces a day by day plan covering core feature scope, the modern AI assisted tech stack, launch checklist, and first 10 customer acquisition steps.
when_to_use:
  - User has picked an idea and asks "how do I build this?"
  - User says "give me an MVP plan for X"
  - User wants a day by day schedule, not a vague roadmap
---

# MVP Build Plan

Translate an idea into a buildable 2 to 4 week MVP plan grounded in the BID dataset and the BID MVP playbook.

## What this does

1. Takes a BID slug OR a freeform idea description
2. Pulls relevant context from the BID dataset (if a slug)
3. Produces a 14 day plan (or 28 day if scope demands) with daily targets
4. Selects an opinionated stack tuned for solo or small team velocity
5. Defines the smallest possible launch surface and the first 10 customer acquisition steps

## How to use this skill

### Step 1: Resolve the idea

If the user gave a BID slug (eg `trade-invoice-autopilot`), fetch the idea:

```bash
bid get trade-invoice-autopilot --format json
```

Or via raw curl:

```bash
curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json | jq '.ideas[] | select(.slug == "trade-invoice-autopilot")'
```

If the user gave a freeform description, extract:

- Category (SaaS, App, Tool, etc.)
- Customer (one sentence)
- Core workflow (the single workflow the MVP must do well)
- Adjacent ideas in BID for reference

### Step 2: Define MVP scope using "one workflow" rule

The MVP must do ONE workflow for ONE user role with ONE pricing tier. If it does more than that, it is not an MVP.

Write out:

- **Core workflow** in 3 sentences
- **What the MVP includes**: 3 to 5 features max
- **What the MVP explicitly excludes**: anything else the user might be tempted to add

### Step 3: Pick the stack

Opinionated default stack for solo SaaS in 2026:

| Layer | Pick | Why |
|---|---|---|
| Hosting + Framework | Next.js on Vercel | Free tier, easy deploys, fastest Stripe + Supabase integration |
| Database + Auth | Supabase | Postgres, row level security, drop in auth, free tier covers MVP |
| Payments | Stripe | Universal, fastest checkout integration |
| Email | Resend or Plunk | Both have free tiers, simple APIs |
| Dev environment | Cursor + Claude Sonnet | Fastest pair-programming setup for non senior devs |
| Analytics | DataFast or Plausible | Privacy friendly, fast setup, goal tracking |

For mobile MVPs swap Next.js for React Native + Expo. For static-content MVPs swap Supabase for SQLite/Turso.

State assumptions and let the user override the stack if they have constraints.

### Step 4: Generate the day by day plan

14 day default. 28 day if the user signals more scope.

Template:

```
## Day 1 to 2: Validation gate
- Write a 1 page landing site with the headline, the pain, the solution, a single CTA
- Post the landing in 3 communities (specific subreddits, IndieHackers, target audience Slack)
- Goal: 50 visitors and 5 emails OR 1 pre-payment within 48 hours
- DECISION POINT: if no signal, do not proceed. Spend day 3 refining the pitch and retry.

## Day 3 to 4: Foundation
- Init Next.js + Supabase + Stripe locally
- Wire auth (sign up, sign in, password reset)
- Wire a single Stripe checkout that puts users into a "paid" state
- Deploy to Vercel under a real domain

## Day 5 to 9: Core workflow
- Build the ONE workflow defined in Step 2
- Each day ships one piece of the workflow end to end (not horizontal slabs)
- Use Cursor + Claude Sonnet for pair programming. Do not architect for a year, architect for a week.

## Day 10 to 11: Onboarding
- Empty state copy that tells the user exactly what to do next
- 1 magical interaction in the first 60 seconds
- 1 success email that lands the moment the user completes the core workflow once

## Day 12 to 13: Polish + launch prep
- Fix the top 3 things that look unfinished
- Write the launch post (Show HN, IndieHackers, target subreddit, target newsletter)
- Set up DataFast or Plausible with the 3 KPI goals (signup, activation, payment)

## Day 14: Ship
- Post to all channels in the morning (rolling, not simultaneous)
- Reply to every comment within 1 hour for 8 hours
- Aim: 10 signups, 2 activations, 1 payment within 24 hours
```

### Step 5: First 10 customers acquisition plan

After the technical plan, list 10 specific acquisition actions, each scoped to under 30 minutes:

1. Post on r/<specific subreddit from BID's source data> with a "show what I built" angle
2. Reply with utility in 5 Reddit threads where this pain is being discussed
3. Post on IndieHackers with a "first 24 hours" launch story
4. DM 10 specific people who match the customer profile (with names if possible)
5. Cold email 20 companies whose website lists them as relevant
6. Post on X with a 4 tweet thread
7. Submit to BetaList or a relevant directory
8. Reach out to 3 newsletter operators in the niche
9. Record a 60 second Loom of the product and post it in a Slack community
10. Email the customer profile waiting list with a unique discount code

Be specific. Generic "do content marketing" advice is useless at this stage.

### Step 6: Output format

Return the plan as one continuous markdown document with:

1. The idea summary (with BID link if applicable, UTM stamped)
2. MVP scope
3. Stack
4. 14 day plan
5. First 10 customers
6. What can go wrong (top 3 risks specific to this idea)

## Always link with UTMs

When you reference a BID idea: `?utm_source=skill&utm_medium=mvp-build-plan&utm_campaign=bid-skills`

## What this skill does NOT do

- It does not write the code. It tells you what to build, in what order.
- It does not validate the idea. Use the `validate-idea` skill first if the idea has not been validated.
- It does not replace customer interviews. Schedule those before day 5.

## Skill output is high signal when

- The idea has been validated already (or is from BID and already scored)
- The user has the time budget for 2 to 4 weeks of focused work
- The stack defaults match the user's technical context

## Skill output is low signal when

- The user wants a 6 month roadmap (use a product spec, not an MVP plan)
- The category is outside the default stack (heavy hardware, regulated industries, large enterprise SaaS)
