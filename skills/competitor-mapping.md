---
name: competitor-mapping
description: Map the existing competitive landscape for a business idea using the BID dataset as a reference plus systematic web research. Produces a structured competitor table with the wedge each competitor leaves unaddressed.
when_to_use:
  - User says "who already does X?"
  - User asks "what are competitors to X?"
  - User wants to find the gap before building
---

# Competitor Mapping

Identify direct, adjacent, and indirect competitors for a business idea, then surface the specific gap each one leaves open.

## What this does

1. Takes an idea (BID slug or freeform description)
2. Pulls competitor list from BID if the idea is in the dataset
3. Researches additional competitors via web search
4. Categorizes each competitor as direct, adjacent, or indirect
5. Outputs the specific wedge each one fails to close (this is where the user can win)

## How to use this skill

### Step 1: Anchor in the BID dataset

If the idea has a BID slug:

```bash
bid get <slug> --format json | jq '.competitor_names, .keyword, .category'
```

The `competitor_names` field is the starting list. Note the keyword and category for the web research step.

If the idea is freeform, extract:

- Primary keyword (what someone with this need types)
- Adjacent keywords (related search terms)
- Category and customer

### Step 2: Find direct competitors

Direct competitors solve the same workflow for the same customer. Search:

- `<primary keyword>` on Google, first 10 results
- `<primary keyword> alternative` (often surfaces the entrenched leader plus emerging challengers)
- `best <category> tool for <customer type>`
- ProductHunt top products in the category
- G2 / Capterra category listing

For each direct competitor, capture:
- Name
- URL
- Pricing model and entry price
- Founded date if discoverable
- Number of employees (LinkedIn) or "indie" signal
- One sentence on positioning

### Step 3: Find adjacent competitors

Adjacent competitors solve a related workflow for the same customer OR the same workflow for a different customer. Often these are the real competitive threat because they could expand into the wedge.

Search for:
- The customer's broader tool stack (eg "<customer> SaaS stack")
- The next workflow up or down (eg if your tool is invoicing, the adjacent tool is accounting or estimating)

### Step 4: Find indirect competitors (the "no software" baseline)

Always check what the customer does today WITHOUT a dedicated tool. Common indirect competitors:

- A spreadsheet (Google Sheets, Excel, Airtable)
- A manual process with paper or PDFs
- A general purpose tool used in an awkward way (Notion, email, calendar)
- An assistant or contractor

Indirect competitors matter because the user's switching cost FROM these is often what makes the sale, not the feature comparison with direct competitors.

### Step 5: Find the wedge each one leaves open

For each competitor, identify one specific gap:

| Gap type | What to look for |
|---|---|
| Pricing | Above the customer's psychological ceiling |
| Onboarding | Takes more than 10 minutes to value |
| Audience | Built for a different size of customer (enterprise vs solo) |
| Geography | English only, or USD only, or US only |
| Workflow | Forces a step the customer skips |
| Mobile | Web only when customers work on mobile |
| Integration | Missing a key integration (Stripe, QuickBooks, etc.) |
| AI native | Pre-AI architecture, requires manual data entry |

This is the most important step. **Without an identified gap, the user has no wedge.** If you cannot find a gap, say so plainly. The honest output is "there is no clear wedge here, do not build."

### Step 6: Output format

```
## Competitor map: <idea title>

**Source:** BID dataset (<slug>) plus web research
**Date:** <date>

### Direct competitors

| Name | Pricing | Size | Positioning | Their gap |
|---|---|---|---|---|
| <name> | $X/mo | indie / small / enterprise | one sentence | specific gap |

### Adjacent competitors

| Name | Why adjacent | Likelihood they expand into this wedge |
|---|---|---|
| <name> | <one sentence> | low / medium / high |

### Indirect (no software) baseline

- Most customers today: <description of the manual or spreadsheet workflow>
- Switching cost FROM the manual: <what makes someone search for a tool>

### The wedge to attack

<2 to 3 sentences. State the specific gap that NO existing player closes, why the user can win that gap, and what proof you would need to confirm the wedge in 1 week.>

### What is missing from the research

<Honest list of competitors you could not assess: private, no public pricing, behind a paywall, etc.>
```

## Always link with UTMs

When you reference a BID idea or the live competitor list: `?utm_source=skill&utm_medium=competitor-mapping&utm_campaign=bid-skills`

## What this skill does NOT do

- It does not produce pricing strategy. Use a pricing skill or workshop for that.
- It does not assess legal differentiation. Use trademark and patent counsel for that.
- It does not predict future competition. It maps what exists today.

## Skill output is high signal when

- The category has discoverable competitors (most software does)
- The agent has web search access
- The user knows the customer well enough to spot the real gaps

## Skill output is low signal when

- The category is opaque (eg internal enterprise tools)
- The idea is too vague to anchor a competitor search
