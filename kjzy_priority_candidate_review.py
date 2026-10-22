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

def main():
    discovery = json.loads(Path("kjzy_priority_source_discovery.json").read_text(encoding="utf-8"))
    parser = CalendarLinks()
    parser.feed(Path("SC_Events.html").read_text(encoding="utf-8"))
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
                if match != "potential_addition_requires_verification":
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
              "warning": "This is a preliminary comparison. Title matches are not date-specific; neither a match nor matching event-page metadata authorizes publication."}
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
