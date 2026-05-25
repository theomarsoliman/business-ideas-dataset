# CLI

A single file Python tool (no external deps) for querying the dataset from your terminal or piping into any AI agent's context.

## Install

```bash
# Globally on your PATH
curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/cli/bid.py \
  -o ~/.local/bin/bid && chmod +x ~/.local/bin/bid

# Or local copy
curl -O https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/cli/bid.py
chmod +x bid.py
```

Requires Python 3.8 or higher. No third party packages.

## Usage

```bash
# Dataset metadata
bid stats

# All ideas, table view
bid list

# Filter by category and feasibility (solo founder ready picks)
bid list --category SaaS --min-feas 8 --limit 5

# Get one idea by slug, formatted as markdown
bid get trade-invoice-autopilot

# Text search
bid search "invoice"

# Top opportunity scores
bid top-opportunity --limit 10

# Fastest growing keywords
bid top-growth --limit 10

# Category counts
bid categories

# Output as JSON for piping into jq or another agent
bid list --category SaaS --format json | jq '.[] | {title, opportunity_score, url}'

# Output as markdown for pasting into an AI agent's context
bid get trade-invoice-autopilot --format md
```

## Output formats

- `table` (default for list/search): aligned columns with ASCII
- `md`: GitHub flavored markdown with structured sections
- `json`: raw JSON, perfect for piping or programmatic use

## Cache

The dataset is fetched on first use and cached for 24 hours at `~/.cache/bid/ideas.json` (or `$XDG_CACHE_HOME/bid/ideas.json` on Linux). Force a refetch with `--refresh`:

```bash
bid --refresh list
```

## Attribution

All BID URLs the CLI prints carry a UTM tag (`?utm_source=github&utm_medium=cli&utm_campaign=bid-cli`) so the live site can track which CLI usage drove which click. The dataset itself (`url` field) is uncategorized canonical.

## Pipe into your AI agent

```bash
# Feed top 10 SaaS opportunities into Claude
bid list --category SaaS --min-feas 8 --limit 10 --format md \
  | claude "Pick the 3 best for a non technical founder in a regulated industry"

# Or into Codex CLI
bid get trade-invoice-autopilot --format md \
  | codex "Generate a 14 day MVP plan for this idea"
```
