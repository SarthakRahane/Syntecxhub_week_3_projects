"""
headline_scraper.py — Terminal Web Scraper for Headlines
Syntecxhub Internship | Python Programming | Project 2

Usage:
  python headline_scraper.py
  python headline_scraper.py --keyword india
  python headline_scraper.py --source hindustan --format json
  python headline_scraper.py --keyword tech --format csv --output my_news.csv
"""

import argparse
import csv
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import feedparser
import requests

# ── Logging setup ────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── RSS sources (no scraping / robots.txt issues) ─────────────
SOURCES = {
    "hindu":        ("The Hindu",          "https://www.thehindu.com/feeder/default.rss"),
    "hindustan":    ("Hindustan Times",    "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml"),
    "ndtv":         ("NDTV",               "https://feeds.feedburner.com/ndtvnews-india-news"),
    "timesofindia": ("Times of India",     "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"),
    "reuters":      ("Reuters",            "https://feeds.reuters.com/reuters/topNews"),
    "bbc":          ("BBC News",           "https://feeds.bbci.co.uk/news/rss.xml"),
}

COLORS = {
    "header":  "\033[1;34m",   # bold blue
    "title":   "\033[0;37m",   # white
    "source":  "\033[1;36m",   # bold cyan
    "time":    "\033[0;33m",   # yellow
    "url":     "\033[0;35m",   # magenta
    "ok":      "\033[0;32m",   # green
    "err":     "\033[0;31m",   # red
    "reset":   "\033[0m",
    "dim":     "\033[2m",
    "bold":    "\033[1m",
}

def c(color, text):
    """Wrap text in ANSI color."""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


# ── Core scraper ──────────────────────────────────────────────
def fetch_feed(name: str, label: str, url: str, delay: float = 1.0) -> list[dict]:
    """Fetch and parse one RSS feed. Returns list of article dicts."""
    log.info("Fetching %-15s → %s", label, url)
    time.sleep(delay)                        # polite delay

    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "headline-scraper/1.0"})
        resp.raise_for_status()
    except requests.RequestException as e:
        log.error("%-15s  FAILED: %s", label, e)
        return []

    feed = feedparser.parse(resp.content)
    articles = []
    for entry in feed.entries:
        articles.append({
            "source":    label,
            "title":     entry.get("title", "").strip(),
            "url":       entry.get("link", "").strip(),
            "published": entry.get("published", ""),
            "summary":   entry.get("summary", "")[:200].strip(),
        })

    log.info("%-15s  %s%d headlines%s fetched",
             label, COLORS["ok"], len(articles), COLORS["reset"])
    return articles


def scrape(sources: list[str], keyword: str | None) -> list[dict]:
    """Scrape selected sources, optionally filter by keyword."""
    all_articles = []
    for key in sources:
        label, url = SOURCES[key]
        articles = fetch_feed(key, label, url)
        all_articles.extend(articles)

    if keyword:
        kw = keyword.lower()
        before = len(all_articles)
        all_articles = [
            a for a in all_articles
            if kw in a["title"].lower() or kw in a["summary"].lower()
        ]
        log.info("Keyword filter '%s': %d → %d articles", keyword, before, len(all_articles))

    return all_articles


# ── Display ───────────────────────────────────────────────────
def display(articles: list[dict]):
    width = 80
    print()
    print(c("header", "═" * width))
    print(c("header", f"  📰  HEADLINE SCRAPER  —  {datetime.now().strftime('%d %b %Y, %H:%M')}"))
    print(c("header", "═" * width))
    print()

    if not articles:
        print(c("err", "  No headlines found."))
        return

    for i, a in enumerate(articles, 1):
        print(c("bold",   f"  [{i:>2}]  ") + c("title", a["title"]))
        print(c("dim",    "       ") + c("source", a["source"]) +
              c("dim",    "  ·  ") + c("time", a["published"] or "—"))
        print(c("dim",    "       ") + c("url", a["url"][:75] + ("…" if len(a["url"]) > 75 else "")))
        print()

    print(c("dim", f"  {len(articles)} total headlines"))
    print(c("header", "═" * width))
    print()


# ── Save ──────────────────────────────────────────────────────
def save_json(articles: list[dict], path: str):
    Path(path).write_text(json.dumps(articles, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("%s%s%s saved (%d articles)", COLORS["ok"], path, COLORS["reset"], len(articles))


def save_csv(articles: list[dict], path: str):
    if not articles:
        log.warning("Nothing to save.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=articles[0].keys())
        writer.writeheader()
        writer.writerows(articles)
    log.info("%s%s%s saved (%d articles)", COLORS["ok"], path, COLORS["reset"], len(articles))


# ── CLI ───────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Terminal headline scraper — Syntecxhub Project 2",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument(
        "--source", "-s",
        nargs="+",
        choices=list(SOURCES.keys()) + ["all"],
        default=["ndtv"],
        metavar="SOURCE",
        help="Sources: ndtv bbc hindu hindustan timesofindia reuters all  (default: ndtv)",
    )
    p.add_argument(
        "--keyword", "-k",
        default=None,
        metavar="WORD",
        help="Filter headlines containing this keyword",
    )
    p.add_argument(
        "--format", "-f",
        choices=["json", "csv", "none"],
        default="none",
        help="Save output format (default: none — display only)",
    )
    p.add_argument(
        "--output", "-o",
        default=None,
        metavar="FILE",
        help="Output filename (auto-generated if omitted)",
    )
    p.add_argument(
        "--limit", "-l",
        type=int,
        default=20,
        metavar="N",
        help="Max headlines to show (default: 20)",
    )
    return p


def resolve_sources(raw: list[str]) -> list[str]:
    if "all" in raw:
        return list(SOURCES.keys())
    return raw


def auto_filename(fmt: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"headlines_{ts}.{fmt}"


# ── Entry point ───────────────────────────────────────────────
def main():
    parser = build_parser()
    args = parser.parse_args()

    sources = resolve_sources(args.source)
    log.info("Sources: %s", ", ".join(sources))

    articles = scrape(sources, args.keyword)

    if args.limit:  # always truthy now (default=20)
        articles = articles[: args.limit]

    display(articles)

    if args.format != "none":
        path = args.output or auto_filename(args.format)
        if args.format == "json":
            save_json(articles, path)
        elif args.format == "csv":
            save_csv(articles, path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(c("err", "\n  Interrupted."))
        sys.exit(0)
