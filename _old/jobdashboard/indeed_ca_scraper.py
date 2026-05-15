"""
Indeed Canada Job Scraper
=========================
Scrapes job listings from ca.indeed.com and saves results to CSV/JSON.

Usage:
    python indeed_ca_scraper.py --query "software engineer" --location "Toronto, ON" --pages 3
    python indeed_ca_scraper.py --query "data analyst" --location "Vancouver, BC" --output jobs.csv

Requirements:
    pip install requests beautifulsoup4
"""

import argparse
import csv
import json
import random
import re
import time
from dataclasses import dataclass, asdict, fields
from datetime import datetime
from typing import Optional
from urllib.parse import urlencode, urljoin

import requests
from bs4 import BeautifulSoup


# ── Constants ────────────────────────────────────────────────────────────────

BASE_URL = "https://ca.indeed.com"
SEARCH_URL = f"{BASE_URL}/jobs"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
]

RESULTS_PER_PAGE = 10  # Indeed shows 10–15 results per page


# ── Data model ───────────────────────────────────────────────────────────────

@dataclass
class Job:
    title: str
    company: str
    location: str
    salary: Optional[str]
    job_type: Optional[str]
    summary: Optional[str]
    posted: Optional[str]
    url: str
    scraped_at: str = ""

    def __post_init__(self):
        if not self.scraped_at:
            self.scraped_at = datetime.now().isoformat(timespec="seconds")


# ── HTTP helpers ─────────────────────────────────────────────────────────────

def make_session() -> requests.Session:
    """Create a session with browser-like headers."""
    session = requests.Session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-CA,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": BASE_URL,
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    })
    return session


def get_page(session: requests.Session, url: str, params: dict = None,
             retries: int = 3, delay: float = 2.0) -> Optional[BeautifulSoup]:
    """Fetch a page and return a BeautifulSoup object, with retries."""
    for attempt in range(1, retries + 1):
        session.headers["User-Agent"] = random.choice(USER_AGENTS)
        try:
            response = session.get(url, params=params, timeout=15)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            elif response.status_code == 403:
                print(f"  ⚠  Blocked (403) on attempt {attempt}. Waiting longer…")
                time.sleep(delay * 3)
            else:
                print(f"  ⚠  HTTP {response.status_code} on attempt {attempt}.")
                time.sleep(delay)
        except requests.RequestException as e:
            print(f"  ⚠  Request error on attempt {attempt}: {e}")
            time.sleep(delay * attempt)

    print(f"  ✗  Failed to fetch after {retries} attempts: {url}")
    return None


# ── Parsing ──────────────────────────────────────────────────────────────────

def _text(tag, default: str = "") -> str:
    return tag.get_text(strip=True) if tag else default


def parse_job_card(card) -> Optional[Job]:
    """Extract job data from a single Indeed result card."""
    try:
        # Title
        title_tag = (
            card.find("h2", class_=re.compile(r"jobTitle"))
            or card.find("a", {"data-testid": "job-title"})
        )
        title = _text(title_tag.find("span") or title_tag) if title_tag else None
        if not title:
            return None

        # Company
        company_tag = (
            card.find("span", {"data-testid": "company-name"})
            or card.find("span", class_=re.compile(r"companyName"))
        )
        company = _text(company_tag)

        # Location
        location_tag = (
            card.find("div", {"data-testid": "text-location"})
            or card.find("div", class_=re.compile(r"companyLocation"))
        )
        location = _text(location_tag)

        # Salary (optional)
        salary_tag = (
            card.find("div", {"data-testid": "attribute_snippet_testid"})
            or card.find("div", class_=re.compile(r"salary-snippet|estimated-salary"))
        )
        salary = _text(salary_tag) or None

        # Job type (Full-time, Part-time, etc.)
        job_type = None
        for meta in card.find_all("div", class_=re.compile(r"metadata|attribute")):
            text = _text(meta)
            if any(t in text for t in ["Full-time", "Part-time", "Contract",
                                        "Permanent", "Temporary", "Casual"]):
                job_type = text
                break

        # Summary
        summary_tag = card.find("div", class_=re.compile(r"job-snippet|summary"))
        summary = _text(summary_tag) or None

        # Posted date
        date_tag = (
            card.find("span", class_=re.compile(r"date"))
            or card.find("span", {"data-testid": "myJobsStateDate"})
        )
        posted = _text(date_tag) or None

        # URL
        link = card.find("a", id=re.compile(r"^job_")) or card.find("a", href=re.compile(r"/rc/clk|/pagead"))
        if not link:
            link = title_tag.find("a") if title_tag else None
        href = link["href"] if link and link.get("href") else ""
        url = urljoin(BASE_URL, href) if href else BASE_URL

        return Job(
            title=title,
            company=company or "Unknown",
            location=location or "Unknown",
            salary=salary,
            job_type=job_type,
            summary=summary,
            posted=posted,
            url=url,
        )

    except Exception as e:
        print(f"  ⚠  Error parsing card: {e}")
        return None


def parse_results_page(soup: BeautifulSoup) -> list[Job]:
    """Parse all job cards from a search results page."""
    # Indeed wraps jobs in <div> with class containing 'job_seen_beacon' or 'result'
    cards = (
        soup.find_all("div", class_=re.compile(r"job_seen_beacon"))
        or soup.find_all("div", class_=re.compile(r"resultContent"))
        or soup.find_all("li", class_=re.compile(r"result"))
    )

    jobs = []
    for card in cards:
        job = parse_job_card(card)
        if job:
            jobs.append(job)
    return jobs


# ── Main scraper ─────────────────────────────────────────────────────────────

def scrape_indeed(
    query: str,
    location: str = "Canada",
    pages: int = 1,
    min_delay: float = 2.0,
    max_delay: float = 5.0,
    date_posted: str = "",  # e.g. "1" (last 24h), "3", "7", "14"
    job_type: str = "",     # "fulltime", "parttime", "contract", "temporary"
    remote: bool = False,
) -> list[Job]:
    """
    Scrape Indeed Canada for jobs matching `query` in `location`.

    Args:
        query:       Job title or keywords (e.g. "data scientist")
        location:    City, province, or "Canada" (e.g. "Toronto, ON")
        pages:       Number of result pages to scrape
        min_delay:   Min seconds to wait between page requests
        max_delay:   Max seconds to wait between page requests
        date_posted: Filter by recency in days ("1", "3", "7", "14")
        job_type:    Filter by employment type
        remote:      If True, filter for remote jobs

    Returns:
        List of Job objects
    """
    session = make_session()
    all_jobs: list[Job] = []
    seen_urls: set[str] = set()

    params: dict = {
        "q": query,
        "l": location,
        "lang": "en",
    }
    if date_posted:
        params["fromage"] = date_posted  # "fromage" = days old
    if job_type:
        params["jt"] = job_type
    if remote:
        params["remotejob"] = "1"

    print(f"\n🔍  Searching Indeed CA: '{query}' in '{location}'")
    print(f"    Pages: {pages}  |  Filters: date={date_posted or 'any'}, "
          f"type={job_type or 'any'}, remote={remote}\n")

    for page in range(pages):
        start = page * RESULTS_PER_PAGE
        if start > 0:
            params["start"] = start

        print(f"  → Page {page + 1}/{pages} (start={start})…", end=" ")

        soup = get_page(session, SEARCH_URL, params=params)
        if soup is None:
            print("skipped.")
            continue

        page_jobs = parse_results_page(soup)

        # Deduplicate by URL
        new_jobs = [j for j in page_jobs if j.url not in seen_urls]
        seen_urls.update(j.url for j in new_jobs)
        all_jobs.extend(new_jobs)

        print(f"found {len(page_jobs)} cards, {len(new_jobs)} new. "
              f"Total: {len(all_jobs)}")

        if page < pages - 1:
            wait = random.uniform(min_delay, max_delay)
            print(f"     Waiting {wait:.1f}s…")
            time.sleep(wait)

    print(f"\n✅  Done. Scraped {len(all_jobs)} unique jobs.")
    return all_jobs


# ── Output helpers ───────────────────────────────────────────────────────────

def save_csv(jobs: list[Job], path: str) -> None:
    if not jobs:
        print("No jobs to save.")
        return
    fieldnames = [f.name for f in fields(Job)]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(j) for j in jobs)
    print(f"💾  Saved {len(jobs)} jobs to {path}")


def save_json(jobs: list[Job], path: str) -> None:
    if not jobs:
        print("No jobs to save.")
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(j) for j in jobs], f, ensure_ascii=False, indent=2)
    print(f"💾  Saved {len(jobs)} jobs to {path}")


def print_summary(jobs: list[Job], limit: int = 10) -> None:
    if not jobs:
        print("No jobs found.")
        return
    print(f"\n{'─'*70}")
    print(f"{'TITLE':<35} {'COMPANY':<20} {'LOCATION'}")
    print(f"{'─'*70}")
    for job in jobs[:limit]:
        print(f"{job.title[:34]:<35} {job.company[:19]:<20} {job.location}")
    if len(jobs) > limit:
        print(f"… and {len(jobs) - limit} more.")
    print(f"{'─'*70}\n")


# ── CLI entry point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Scrape job listings from Indeed Canada",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python indeed_ca_scraper.py --query "software engineer" --location "Toronto, ON"
  python indeed_ca_scraper.py --query "nurse" --location "Calgary, AB" --pages 5 --output nurses.csv
  python indeed_ca_scraper.py --query "remote developer" --remote --pages 3 --format json
  python indeed_ca_scraper.py --query "accountant" --location "Montreal, QC" --date-posted 7
        """,
    )
    parser.add_argument("--query", "-q", required=True, help="Job title or keywords")
    parser.add_argument("--location", "-l", default="Canada",
                        help="City/province (default: Canada)")
    parser.add_argument("--pages", "-p", type=int, default=1,
                        help="Number of result pages to scrape (default: 1)")
    parser.add_argument("--output", "-o", default="",
                        help="Output file path (auto-named if omitted)")
    parser.add_argument("--format", "-f", choices=["csv", "json"], default="csv",
                        help="Output format (default: csv)")
    parser.add_argument("--date-posted", type=str, default="",
                        help="Max days since posting: 1, 3, 7, or 14")
    parser.add_argument("--job-type", type=str, default="",
                        choices=["", "fulltime", "parttime", "contract", "temporary"],
                        help="Filter by employment type")
    parser.add_argument("--remote", action="store_true",
                        help="Filter for remote jobs only")
    parser.add_argument("--min-delay", type=float, default=2.0,
                        help="Min seconds between page requests (default: 2)")
    parser.add_argument("--max-delay", type=float, default=5.0,
                        help="Max seconds between page requests (default: 5)")

    args = parser.parse_args()

    jobs = scrape_indeed(
        query=args.query,
        location=args.location,
        pages=args.pages,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        date_posted=args.date_posted,
        job_type=args.job_type,
        remote=args.remote,
    )

    print_summary(jobs)

    if jobs:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = re.sub(r"\W+", "_", args.query.lower())
        filename = args.output or f"indeed_{slug}_{timestamp}.{args.format}"

        if args.format == "json":
            save_json(jobs, filename)
        else:
            save_csv(jobs, filename)


if __name__ == "__main__":
    main()