"""Read-only comparison of structured event candidates with published KJZY links.

No candidate is automatically accepted as a verified missing event.
"""
import html
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from zoneinfo import ZoneInfo

class CalendarLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()
        self.titles = set()
        self.url_paths = set()
        self.in_event = 0
        self.depth = 0
        self.active_anchor = False
        self.text_parts = []
        self.event_count = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div":
            self.depth += 1
            if "event" in a.get("class", "").split() and not self.in_event:
                self.in_event = self.depth
                self.event_count += 1
        if tag == "a" and self.in_event:
            href = a.get("href")
            if href:
                self.urls.add(canonical_url(href))
                self.url_paths.add(urlsplit(html.unescape(href)).path.rstrip('/').lower())
                self.active_anchor = True
                self.text_parts = []
    def handle_data(self, data):
        if self.active_anchor:
            self.text_parts.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.active_anchor:
            title = normalize(" ".join(self.text_parts))
            if title:
                self.titles.add(title)
            self.active_anchor = False
        if tag == "div":
            if self.in_event == self.depth:
                self.in_event = 0
            self.depth -= 1

def normalize(s):
    return re.sub(r"[^a-z0-9]+", " ", html.unescape(str(s)).lower()).strip()

def canonical_url(url):
    p = urlsplit(html.unescape(str(url)))
    return (p.netloc.lower().removeprefix("www.") + unquote(p.path).rstrip("/").lower())

def similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()

def review_match(title, url, parser):
    path = urlsplit(html.unescape(url)).path.rstrip('/').lower()
    if canonical_url(url) in parser.urls:
        return "existing_url", "Exact event URL already listed"
    if path and len(path) > 8 and path in parser.url_paths:
        return "possible_existing_link_review", "Same URL path listed on another domain"
    cleaned = normalize(title)
    if cleaned in parser.titles:
        return "possible_existing_title_review", "Exact normalized title already listed"
    if cleaned and len(cleaned) >= 12:
        best = max(((similarity(cleaned, t), t) for t in parser.titles), default=(0, ""))
        if best[0] >= 0.88:
            return "possible_existing_title_review", "Similar title already listed: " + best[1][:110]
    return "potential_addition_requires_verification", "No strong matching title or link found; still unverified"

def date_status(value, today):
    try:
        raw = str(value)
        if not re.match(r"^\d{4}-\d{2}-\d{2}", raw):
            return "date_unverified"
        day = datetime.fromisoformat(raw[:10]).date()
        return "past" if day < today else "future"
    except (ValueError, TypeError):
        return "date_unverified"

def main():
    report = json.loads(Path("kjzy_all_sources_report.json").read_text(encoding="utf-8"))
    parser = CalendarLinks()
    parser.feed(Path("SC_Events.html").read_text(encoding="utf-8"))
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    seen = set()
    rows = []
    for source in report["sources"]:
        for event in source.get("sample_events", []):
            title = str(event.get("title", "")).strip()
            url = str(event.get("url", "")).strip()
            date = str(event.get("start_date", "")).strip()
            key = (normalize(title), date[:10], canonical_url(url))
            if key in seen:
                continue
            seen.add(key)
            ds = date_status(date, today)
            if ds == "past":
                status = "past_not_candidate"
            elif not title or not url or ds == "date_unverified":
                status = "incomplete_review"
            else:
                status, reason = review_match(title, url, parser)
            if ds == "past":
                reason = "Event date is before today"
            elif not title or not url or ds == "date_unverified":
                reason = "Title, direct URL, or parseable date missing"
            rows.append({"source": source["source"], "title": html.unescape(title), "start_date": date, "url": url, "status": status, "review_reason": reason})
    counts = Counter(row["status"] for row in rows)
    result = {
        "read_only": True,
        "date_checked_pacific": today.isoformat(),
        "calendar_event_blocks": parser.event_count,
        "sources_checked": report["sources_checked"],
        "structured_records_compared": len(rows),
        "status_counts": dict(counts),
        "warning": "Potential additions are unverified. Confirm organizer, date, venue, ticket link, and duplicate performances before any publication.",
        "candidates": rows,
    }
    Path("kjzy_candidate_review_report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# KJZY Candidate Review (Read Only)", "", "Checked: " + today.isoformat(),
             "", "No events have been verified or published.", "",
             "## Review candidates", ""]
    for row in rows:
        if row["status"] in ("potential_addition_requires_verification", "possible_existing_title_review", "possible_existing_link_review", "incomplete_review"):
            lines.extend(["### " + row["title"].replace("\n", " ")[:150],
                          "- Source: " + row["source"],
                          "- Date: " + row["start_date"],
                          "- Status: " + row["status"],
                          "- Reason: " + row["review_reason"],
                          "- Event link: " + row["url"], ""])
    Path("kjzy_candidate_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("KJZY READ-ONLY EVENT CANDIDATE COMPARISON")
    print("Calendar event blocks:", parser.event_count)
    print("Structured records compared:", len(rows))
    print("Status totals:", json.dumps(dict(counts), sort_keys=True))
    for row in rows:
        if row["status"] in ("potential_addition_requires_verification", "possible_existing_title_review", "possible_existing_link_review", "incomplete_review"):
            print("REVIEW:", json.dumps(row, ensure_ascii=False))
    print("NO EVENTS ADDED. NO CALENDAR MODIFICATIONS.")

if __name__ == "__main__":
    main()
