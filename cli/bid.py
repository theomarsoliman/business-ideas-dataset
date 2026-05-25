#!/usr/bin/env python3
"""
bid: command-line interface to the Business Ideas Database dataset.

A single-file Python tool (no external deps) for querying the BID dataset
from your terminal or for piping into any AI agent's context.

USAGE
    bid list [--category SaaS] [--min-feas 7] [--limit 10] [--format json|md|table]
    bid get SLUG
    bid search "invoice"
    bid top-opportunity [--limit 10]
    bid top-growth [--limit 10]
    bid categories
    bid stats

The dataset is fetched from GitHub on first use and cached locally for 1 day.

Live data:
    https://github.com/theomarsoliman/business-ideas-dataset
    https://businessideasdb.com
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

DATASET_URL = (
    "https://raw.githubusercontent.com/theomarsoliman/business-ideas-dataset/"
    "main/data/ideas.json"
)
CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "bid"
CACHE_FILE = CACHE_DIR / "ideas.json"
CACHE_TTL_SECONDS = 24 * 60 * 60

UTM = "?utm_source=github&utm_medium=cli&utm_campaign=bid-cli"


def fetch_dataset(refresh: bool = False) -> dict[str, Any]:
    """Pull the dataset, using a 1 day local cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    fresh = False
    if not refresh and CACHE_FILE.exists():
        age = time.time() - CACHE_FILE.stat().st_mtime
        fresh = age < CACHE_TTL_SECONDS
    if not fresh:
        with urllib.request.urlopen(DATASET_URL, timeout=30) as r:
            data = r.read()
        CACHE_FILE.write_bytes(data)
    return json.loads(CACHE_FILE.read_text())


def tracked(url: str) -> str:
    """Stamp a CLI-specific UTM on a BID URL for attribution."""
    if "utm_source=" in url:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}{UTM[1:]}"


def fmt_vol(n: int | None) -> str:
    if n is None:
        return "-"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M".replace(".0M", "M")
    if n >= 1_000:
        return f"{n/1_000:.1f}K".replace(".0K", "K")
    return str(n)


def fmt_growth(n: int | None) -> str:
    if n is None or n == 0:
        return "-"
    return f"{'+' if n > 0 else ''}{n}%"


def output(ideas: list[dict[str, Any]], fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(ideas, indent=2))
        return
    if fmt == "md":
        for i in ideas:
            print(f"## {i['title']}")
            print(f"- Category: {i['category']}")
            print(f"- Keyword: `{i['keyword']}` ({fmt_vol(i['search_volume'])} monthly, {fmt_growth(i['growth_percent'])} YoY)")
            print(f"- Scores: opp {i['opportunity_score']}, problem {i['problem_score']}, feasibility {i['feasibility_score']}, timing {i['timing_score']}")
            if i.get("pitch"):
                print(f"- Pitch: {i['pitch']}")
            print(f"- Full analysis: {tracked(i['url'])}")
            print()
        return
    # table
    if not ideas:
        print("(no results)")
        return
    cols = ["title", "category", "opp", "feas", "vol", "yoy"]
    widths = [60, 14, 4, 4, 7, 6]
    print("  ".join(c.upper().ljust(w) for c, w in zip(cols, widths)))
    print("  ".join("-" * w for w in widths))
    for i in ideas:
        row = [
            (i["title"] or "")[: widths[0]],
            (i["category"] or "")[: widths[1]],
            str(i["opportunity_score"] or "-"),
            str(i["feasibility_score"] or "-"),
            fmt_vol(i["search_volume"]),
            fmt_growth(i["growth_percent"]),
        ]
        print("  ".join(v.ljust(w) for v, w in zip(row, widths)))
    print()
    print(f"{len(ideas)} idea{'s' if len(ideas) != 1 else ''}. Full analysis at https://businessideasdb.com/ideas?utm_source=github&utm_medium=cli")


def cmd_list(args: argparse.Namespace) -> None:
    data = fetch_dataset(args.refresh)
    ideas = data["ideas"]
    if args.category:
        ideas = [i for i in ideas if i["category"].lower() == args.category.lower()]
    if args.min_feas is not None:
        ideas = [i for i in ideas if (i["feasibility_score"] or 0) >= args.min_feas]
    if args.min_opp is not None:
        ideas = [i for i in ideas if (i["opportunity_score"] or 0) >= args.min_opp]
    ideas = sorted(
        ideas,
        key=lambda i: (
            -(i["opportunity_score"] or 0)
            - (i["problem_score"] or 0)
            - (i["feasibility_score"] or 0)
            - (i["timing_score"] or 0)
        ),
    )
    if args.limit:
        ideas = ideas[: args.limit]
    output(ideas, args.format)


def cmd_get(args: argparse.Namespace) -> None:
    data = fetch_dataset(args.refresh)
    match = next((i for i in data["ideas"] if i["slug"] == args.slug), None)
    if not match:
        print(f"No idea with slug '{args.slug}'", file=sys.stderr)
        sys.exit(1)
    if args.format == "json":
        print(json.dumps(match, indent=2))
        return
    print(f"# {match['title']}\n")
    print(f"**Category:** {match['category']}  ")
    print(f"**Keyword:** `{match['keyword']}` ({fmt_vol(match['search_volume'])} monthly, {fmt_growth(match['growth_percent'])} YoY)  ")
    print(f"**Competition:** {match['competition']}  ·  **Difficulty:** {match['difficulty']}  ·  **Revenue range:** {match['revenue_range']}\n")
    print(f"## Pitch\n{match['pitch']}\n")
    print(f"## Scores")
    print(f"- Opportunity: **{match['opportunity_score']}**/10")
    print(f"- Problem severity: **{match['problem_score']}**/10")
    print(f"- Feasibility: **{match['feasibility_score']}**/10")
    print(f"- Timing: **{match['timing_score']}**/10\n")
    if match.get("tags"):
        print(f"## Tags\n{', '.join(match['tags'])}\n")
    if match.get("competitor_names"):
        print(f"## Existing competitors\n{', '.join(match['competitor_names'])}\n")
    print(f"## Full editorial analysis\n{tracked(match['url'])}\n")
    print("(Customer profile, MVP feature list, source Reddit threads, and competitor URLs live at the link above.)")


def cmd_search(args: argparse.Namespace) -> None:
    data = fetch_dataset(args.refresh)
    q = args.query.lower()
    hits = [
        i for i in data["ideas"]
        if q in (i["title"] or "").lower()
        or q in (i["pitch"] or "").lower()
        or q in (i["keyword"] or "").lower()
        or any(q in (t or "").lower() for t in (i.get("tags") or []))
    ]
    output(hits, args.format)


def cmd_top_opportunity(args: argparse.Namespace) -> None:
    data = fetch_dataset(args.refresh)
    ideas = sorted(
        [i for i in data["ideas"] if i["opportunity_score"] is not None],
        key=lambda i: (-(i["opportunity_score"] or 0), -(i["search_volume"] or 0)),
    )[: args.limit]
    output(ideas, args.format)


def cmd_top_growth(args: argparse.Namespace) -> None:
    data = fetch_dataset(args.refresh)
    ideas = sorted(
        [i for i in data["ideas"] if i.get("growth_percent")],
        key=lambda i: -(i["growth_percent"] or 0),
    )[: args.limit]
    output(ideas, args.format)


def cmd_categories(args: argparse.Namespace) -> None:
    data = fetch_dataset(args.refresh)
    from collections import Counter
    c = Counter(i["category"] for i in data["ideas"])
    for cat, n in c.most_common():
        print(f"{n:>4}  {cat}")


def cmd_stats(args: argparse.Namespace) -> None:
    data = fetch_dataset(args.refresh)
    ideas = data["ideas"]
    print(f"Total ideas:        {len(ideas)}")
    print(f"Categories:         {len({i['category'] for i in ideas})}")
    print(f"Updated:            {data['meta'].get('generated_at','')}")
    print(f"Source:             {data['meta'].get('source','')}")
    print(f"License:            {data['meta'].get('license','MIT')}")
    print(f"Dataset (GitHub):   https://github.com/theomarsoliman/business-ideas-dataset")
    print(f"Annual report:      https://businessideasdb.com/state-of-indie-business-ideas-2026{UTM}")


def main() -> None:
    p = argparse.ArgumentParser(
        prog="bid",
        description="Query the Business Ideas Database dataset from the CLI.",
    )
    p.add_argument("--refresh", action="store_true", help="Bypass cache and refetch the dataset")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List ideas, sorted by composite score")
    p_list.add_argument("--category", help="Filter by category (SaaS, App, Tool, etc.)")
    p_list.add_argument("--min-feas", type=int, help="Minimum feasibility score")
    p_list.add_argument("--min-opp", type=int, help="Minimum opportunity score")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.add_argument("--format", choices=["table", "md", "json"], default="table")
    p_list.set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Get a single idea by slug")
    p_get.add_argument("slug")
    p_get.add_argument("--format", choices=["md", "json"], default="md")
    p_get.set_defaults(func=cmd_get)

    p_search = sub.add_parser("search", help="Text search across title, pitch, keyword, tags")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--format", choices=["table", "md", "json"], default="table")
    p_search.set_defaults(func=cmd_search)

    p_opp = sub.add_parser("top-opportunity", help="Ideas with highest opportunity score")
    p_opp.add_argument("--limit", type=int, default=10)
    p_opp.add_argument("--format", choices=["table", "md", "json"], default="table")
    p_opp.set_defaults(func=cmd_top_opportunity)

    p_growth = sub.add_parser("top-growth", help="Ideas with highest YoY keyword growth")
    p_growth.add_argument("--limit", type=int, default=10)
    p_growth.add_argument("--format", choices=["table", "md", "json"], default="table")
    p_growth.set_defaults(func=cmd_top_growth)

    sub.add_parser("categories", help="Count of ideas per category").set_defaults(func=cmd_categories)
    sub.add_parser("stats", help="Dataset metadata").set_defaults(func=cmd_stats)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
