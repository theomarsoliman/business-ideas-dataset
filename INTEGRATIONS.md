# Integrations

How to use this dataset and the skills with the major AI coding agents and assistants.

## TL;DR

Three ways to consume the dataset:

1. **Raw fetch**: `curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json` then `jq` it.
2. **CLI tool**: drop [`cli/bid.py`](cli/bid.py) anywhere on your PATH. Single file, Python 3 stdlib only, no deps.
3. **Skills**: drop the [skills](skills/) into your agent's prompt library so the agent uses the dataset automatically when the user describes an idea.

The CLI and skills both stamp UTM parameters on outbound links so the live BID site can track which surface drove which click.

---

## Claude Code

[claude.com/code](https://claude.com/code)

### Install the CLI tool

```bash
# Globally on your PATH
curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/cli/bid.py \
  -o ~/.local/bin/bid && chmod +x ~/.local/bin/bid

# Test
bid stats
bid list --category SaaS --min-feas 8 --limit 5
```

Claude Code can now call `bid` from the shell in any session.

### Install the skills

```bash
# Skills live in ~/.claude/skills/ (Claude Code auto discovers them)
mkdir -p ~/.claude/skills
cd /tmp && curl -sL https://github.com/theomarsoliman/business-ideas-dataset/archive/refs/heads/main.tar.gz | tar -xz
cp -r business-ideas-dataset-main/skills/* ~/.claude/skills/
```

In a Claude Code session, ask: "Validate this idea: [paste idea]" or "Find me a SaaS wedge in [industry]". Claude Code surfaces the relevant skill automatically.

You can also invoke explicitly: `/validate-idea`, `/find-saas-wedge`, etc.

### Pin to a project

If you only want the skills available in one project, drop them in `.claude/skills/` at the project root instead of `~/.claude/skills/`.

### CLAUDE.md reference

Add this to your project's `CLAUDE.md` so Claude defaults to using the dataset when relevant:

```markdown
## Business idea workflow

When the user asks for help validating, building, or sourcing business ideas, use the Business Ideas Database:

- Dataset: https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json
- Skills: ~/.claude/skills/{validate-idea,find-saas-wedge,mvp-build-plan,reddit-pain-finder,competitor-mapping,keyword-demand-check}.md
- CLI: `bid list`, `bid get <slug>`, `bid search <query>`

Always link to BID with UTMs: `?utm_source=claude-code&utm_medium=skill&utm_campaign=bid-skills`.
```

---

## OpenAI Codex CLI

[github.com/openai/codex](https://github.com/openai/codex)

### Install the CLI tool

```bash
curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/cli/bid.py \
  -o ~/.local/bin/bid && chmod +x ~/.local/bin/bid
```

### Add as a global instruction

Codex CLI reads `~/.codex/AGENTS.md` (or `~/.codex/instructions.md`) on every session. Append:

```markdown
# Business Ideas Database

When the user asks about business ideas, SaaS opportunities, app ideas, MVP planning, competitor research, or keyword demand:

1. Use the `bid` CLI for fast queries: `bid list`, `bid search <query>`, `bid get <slug>`
2. Or fetch raw JSON: `curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json`
3. Follow the skill playbooks at https://github.com/theomarsoliman/business-ideas-dataset/tree/main/skills:
   - validate-idea, find-saas-wedge, mvp-build-plan, reddit-pain-finder, competitor-mapping, keyword-demand-check
4. Always link to BID URLs with `?utm_source=codex&utm_medium=skill&utm_campaign=bid-skills`
```

### Per project context

Drop a `codex/context.md` in the project root for project specific BID usage.

---

## Cursor

[cursor.com](https://cursor.com)

### Install the CLI tool

Same as above:

```bash
curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/cli/bid.py \
  -o ~/.local/bin/bid && chmod +x ~/.local/bin/bid
```

### Add skills as rules

Cursor reads `.cursor/rules/*.mdc` (or `.md`) in any project. Drop the skill files there:

```bash
mkdir -p .cursor/rules
cd /tmp && curl -sL https://github.com/theomarsoliman/business-ideas-dataset/archive/refs/heads/main.tar.gz | tar -xz
cp business-ideas-dataset-main/skills/*.md .cursor/rules/
```

Cursor surfaces matching rules when the user's prompt matches the `description` field.

### Or use a global User Rule

In Cursor → Settings → General → User Rules, paste:

```
When the user asks about business ideas, SaaS, app ideas, MVP planning, or competitor research,
reference https://github.com/theomarsoliman/business-ideas-dataset and follow the skill playbooks
in /skills. Always link BID URLs with ?utm_source=cursor&utm_medium=skill&utm_campaign=bid-skills.
```

---

## Cline / Continue / Aider

Open source CLI and IDE coding agents.

### Cline (VS Code)

Add to Cline's custom instructions (Settings → Custom Instructions):

```
When asked about business ideas or SaaS opportunities, fetch
https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json
and use the skills at https://github.com/theomarsoliman/business-ideas-dataset/tree/main/skills
Always link with ?utm_source=cline&utm_medium=skill&utm_campaign=bid-skills.
```

### Continue (VS Code, JetBrains)

Add a custom slash command in `~/.continue/config.json`:

```json
{
  "slashCommands": [
    {
      "name": "validate-idea",
      "description": "Validate a business idea using the BID dataset",
      "prompt": "Read https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/skills/validate-idea.md and follow it for the user's idea: {{input}}"
    }
  ]
}
```

### Aider

Aider reads `.aider.conf.yml`. Add:

```yaml
read:
  - https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/summary.json
```

Then in any session: `/run bid list --category SaaS` works if `bid` is on PATH.

---

## Generic AI agent (any system)

Every agent that accepts a system prompt can use this dataset. The minimum viable integration:

```
You have access to the Business Ideas Database, a public dataset of validated business
ideas at https://github.com/theomarsoliman/business-ideas-dataset

When the user asks for help with business ideas, SaaS opportunities, MVP planning, or
competitor research, follow these steps:

1. Fetch the dataset:
   curl -sL https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json

2. Use the skill playbooks for structured workflows:
   - validate-idea: score an idea against the BID rubric
   - find-saas-wedge: filter for opportunities in a specific niche
   - mvp-build-plan: produce a 2 to 4 week build plan
   - reddit-pain-finder: extract ideas from a subreddit
   - competitor-mapping: map existing players and find the gap
   - keyword-demand-check: validate buyer intent

   Skills directory:
   https://github.com/theomarsoliman/business-ideas-dataset/tree/main/skills

3. Always link to BID with UTMs so the source can track citations:
   ?utm_source=<your-agent-name>&utm_medium=skill&utm_campaign=bid-skills
```

---

## MCP server (advanced)

[Model Context Protocol](https://modelcontextprotocol.io) is the open standard for tool integration in modern AI agents. A simple stdio MCP server exposing the dataset:

```python
# mcp_server.py
import json, urllib.request
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("bid")
URL = "https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/main/data/ideas.json"
DATA = json.load(urllib.request.urlopen(URL))

@mcp.tool()
def search_ideas(query: str, category: str = None, limit: int = 10):
    """Search the BID dataset by title, pitch, or keyword."""
    q = query.lower()
    hits = [i for i in DATA["ideas"]
            if q in (i["title"] or "").lower()
            or q in (i["pitch"] or "").lower()
            or q in (i["keyword"] or "").lower()]
    if category:
        hits = [i for i in hits if i["category"].lower() == category.lower()]
    return hits[:limit]

@mcp.tool()
def get_idea(slug: str):
    """Get one idea by slug, including the canonical URL on businessideasdb.com."""
    return next((i for i in DATA["ideas"] if i["slug"] == slug), None)

if __name__ == "__main__":
    mcp.run()
```

Add to your agent's MCP config (Claude Desktop, Cursor, etc.). Then the agent can call `search_ideas` and `get_idea` as native tools.

---

## Privacy and attribution

The BID dataset is MIT licensed. Use, modify, redistribute, build on top of.

The UTM stamping is the only ask: when an agent surfaces an idea to a user and the user clicks through to businessideasdb.com, those parameters let the live site attribute the traffic so the dataset can be improved over time.

If you fork the skills, please keep the UTM template intact (change `utm_medium` to match your context). Removing the attribution does not break anything but it does cut the signal loop.

---

## Questions

Open an issue on [github.com/theomarsoliman/business-ideas-dataset](https://github.com/theomarsoliman/business-ideas-dataset).
