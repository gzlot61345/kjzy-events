"""Read-only comparison of priority-source discoveries with KJZY master.

Conservative matching: a title match alone is ambiguous, never proof of a
duplicate. No source is approved for publication by this report.
"""
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from kjzy_candidate_review import CalendarLinks, review_match, normalize
from kjzy_event_page_verification import check as verify_page

PACIFIC = ZoneInfo("America/Los_Angeles")
FOCUS = {"Sonoma County Tourism Events", "Visit Santa Rosa Events"}


def exact_day_calendar_matches(html_text, title, day, url):
    """Only a single-day listing with the same title or URL counts as confirmed."""
    import re
    from html import unescape
    from kjzy_candidate_review import canonical_url
    month = None
    year = None
    target = str(day)
    for token in re.finditer(r'<h2 class="year">([^<]+)</h2>|<h3 class="month">([^<]+)</h3>|<div class="event"\\b[^>]*>.*?</div>\\s*</div>\\s*</div>', html_text, re.S):
        raw = token.group(0)
        if token.group(1):
            year = token.group(1).strip()
        elif token.group(2):
            try:
                month = datetime.strptime(token.group(2).strip(), "%B").month
            except ValueError:
                month = None
        elif month and year:
            date_match = re.search(r'<div class="date">\\s*(\\d{1,2})\\s*</div>', raw)
            link_match = re.search(r'<a\\s+href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S)
            if not date_match or not link_match:
                continue
            try:
                listed_day = datetime(int(year), month, int(date_match.group(1))).date().isoformat()
            except ValueError:
                continue
            if listed_day == target and (normalize(unescape(re.sub(r'<[^>]*>', '', link_match.group(2)))) == normalize(title) or canonical_url(unescape(link_match.group(1))) == canonical_url(url)):
                return True
    return False

def main():
    discovery = json.loads(Path("kjzy_priority_source_discovery.json").read_text(encoding="utf-8"))
    parser = CalendarLinks()
    html_text = Path("SC_Events.html").read_text(encoding="utf-8")
    parser.feed(html_text)
    today = datetime.now(PACIFIC).date()
    results = []
    seen = set()
    for source in discovery["sources"]:
        if source["source"] not in FOCUS:
            continue
        for event in source["events"]:
            title = event.get("title", "").strip()
            date_raw = event.get("start_date", "")
            url = event.get("url", "").strip()
            location = event.get("location", "").strip()
            try:
                dt = datetime.fromisoformat(date_raw.replace("Z", "+00:00"))
                date = dt.astimezone(PACIFIC).date() if dt.tzinfo else dt.date()
            except (ValueError, TypeError):
                date = None
            key = (source["source"], normalize(title), str(date), url)
            if key in seen:
                continue
            seen.add(key)
            row = {"source": source["source"], "title": title, "date": str(date) if date else "",
                   "url": url, "location": location}
            if not date or not title or not url or not location or urlsplit(url).scheme != "https":
                row["status"] = "incomplete_metadata"
            elif date < today:
                row["status"] = "past_event"
            else:
                match, reason = review_match(title, url, parser)
                row["calendar_comparison"] = match
                row["comparison_reason"] = reason
                same_day = exact_day_calendar_matches(html_text, title, date, url)
                row["same_day_existing"] = same_day
                if same_day:
                    row["status"] = "confirmed_same_date_existing"
                elif match != "potential_addition_requires_verification":
                    row["status"] = "possible_existing_needs_date_review"
                else:
                    verification = verify_page({"source": source["source"], "title": title,
                                                "date": str(date), "url": url, "location": location})
                    row["page_verification"] = verification["status"]
                    row["status"] = ("potential_new_requires_manual_date_duplicate_review"
                                     if verification["status"] == "page_metadata_matches"
                                     else "page_verification_incomplete")
            results.append(row)
    counts = dict(Counter(row["status"] for row in results))
    output = {"read_only": True, "date_checked_pacific": today.isoformat(),
              "calendar_listings": parser.event_count, "candidates_compared": len(results),
              "status_counts": counts, "events": results,
              "warning": "This is a preliminary comparison. Only explicit single-day calendar matches are date-confirmed; ranges and title-only matches still require review. No publication is authorized."}
    Path("kjzy_priority_candidate_review.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("KJZY PRIORITY SOURCE CANDIDATE REVIEW (READ ONLY)")
    print("Calendar listings:", parser.event_count)
    print("Records compared:", len(results))
    print("Status totals:", json.dumps(counts, sort_keys=True))
    for row in results:
        print("CANDIDATE:", json.dumps(row, ensure_ascii=False))
    print("NO EVENTS PUBLISHED.")

if __name__ == "__main__":
    main()
