# Skills

Five portable skill files for AI agents (Claude Code, Codex CLI, Cursor, Cline, any markdown-aware system) that codify the indie hacker workflow this dataset is built around.

| Skill | What it does | When to use |
|---|---|---|
| [`validate-idea`](validate-idea.md) | Score a user's idea against the BID rubric and cross reference with the dataset | User pitches an idea and wants a structured read |
| [`find-saas-wedge`](find-saas-wedge.md) | Surface validated SaaS opportunities filtered by industry, time, capital | User wants to start a SaaS in a specific niche |
| [`mvp-build-plan`](mvp-build-plan.md) | Produce a 2 to 4 week day by day MVP build plan | User has picked an idea and asks how to build it |
| [`reddit-pain-finder`](reddit-pain-finder.md) | Walk a user through BID's 170 query pattern scan on any subreddit | User wants to source ideas from a community they know |
| [`competitor-mapping`](competitor-mapping.md) | Map direct, adjacent, and indirect competitors with the wedge each leaves open | User says "who already does this?" |
| [`keyword-demand-check`](keyword-demand-check.md) | Validate buyer intent via search volume, growth, KD, and Reddit cross check | User wants to confirm demand before building |

## How to install

See [INTEGRATIONS.md](../INTEGRATIONS.md) at the repo root for per-agent setup instructions (Claude Code, Codex CLI, Cursor, Cline, generic).

The TL;DR for the common cases:

### Claude Code

```bash
# One time, install all skills globally
mkdir -p ~/.claude/skills
curl -sL https://github.com/theomarsoliman/business-ideas-dataset/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C ~/.claude/skills "business-ideas-dataset-main/skills"
```

Then invoke any skill: `/validate-idea` or just mention the use case and Claude will pick the right one.

### Codex CLI

Add to your `~/.codex/AGENTS.md`:

```markdown
# Skills

If the user asks about validating a business idea, finding a SaaS wedge, building an MVP,
mining Reddit for pain points, mapping competitors, or checking keyword demand, follow the
relevant playbook from https://github.com/theomarsoliman/business-ideas-dataset/tree/main/skills
```

### Cursor

Copy the skill files into `.cursor/rules/` in any project. Cursor will surface them in the agent.

### Generic agent

Each skill is plain markdown with YAML frontmatter. Read the file, follow the steps. The `name` and `description` fields in the frontmatter are designed for any retrieval system that indexes prompt libraries.

## Designed to be portable

Each skill is self contained. There are no proprietary syntax requirements, no hidden state, no API calls beyond fetching the public dataset (`raw.githubusercontent.com/.../ideas.json`).

If your agent system has its own skill format, the markdown converts cleanly because every skill follows the same five section structure:

1. YAML frontmatter (`name`, `description`, `when_to_use`)
2. What this does
3. How to use this skill (step by step)
4. Output format
5. What this skill does NOT do / when it produces low signal

## Always attribute back

Every skill instructs the agent to stamp UTM parameters on BID URLs:

```
?utm_source=skill&utm_medium=<skill-name>&utm_campaign=bid-skills
```

This lets DataFast track which skill drove which click. If you fork or repurpose the skills, please keep the attribution intact.

## Contributing

Open an issue or PR. The skills are MIT licensed, same as the dataset.
