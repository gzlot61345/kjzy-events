"""Create a conservative, read-only proposal for adding KJZY events.

Source inventory is incomplete; this NEVER publishes and never treats missing
records as proof an event is absent or cancelled.
"""
import html
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from kjzy_candidate_review import CalendarLinks, review_match, normalize

PACIFIC = ZoneInfo("America/Los_Angeles")
APPROVED_SOURCES = {"KJZY Community Calendar 2 / Sonoma Media Group", "Sebastopol Community Calendar"}

def valid_event(event, now):
    title = html.unescape(str(event.get("title", "")).strip())
    url = html.unescape(str(event.get("url", "")).strip())
    location = html.unescape(str(event.get("location", "")).strip())
    start = str(event.get("start_date", "")).strip()
    if not title or len(title) < 5 or not location or len(location) < 4:
        return None, "missing_title_or_venue"
    if not url.startswith("https://") or not urlsplit(url).netloc:
        return None, "invalid_event_link"
    try:
        dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return None, "time_zone_missing"
        dt = dt.astimezone(PACIFIC)
    except ValueError:
        return None, "invalid_start_date"
    if dt <= now:
        return None, "already_started_or_expired"
    if dt.year > now.year + 1:
        return None, "date_too_distant"
    return {"title": title, "url": url, "location": location, "date": dt.date().isoformat(), "time_pacific": dt.strftime("%I:%M %p").lstrip("0"), "start_date": start}, None

def main():
    now = datetime.now(PACIFIC)
    sources = json.loads(Path("kjzy_all_sources_report.json").read_text(encoding="utf-8"))["sources"]
    calendar = Path("SC_Events.html").read_text(encoding="utf-8")
    parser = CalendarLinks()
    parser.feed(calendar)
    rows, seen = [], set()
    for source in sources:
        if source["source"] not in APPROVED_SOURCES:
            continue
        for event in source.get("sample_events", []):
            candidate, error = valid_event(event, now)
            if error:
                rows.append({"source": source["source"], "title": html.unescape(str(event.get("title", ""))), "status": "skipped", "reason": error})
                continue
            key = (normalize(candidate["title"]), candidate["date"], candidate["url"])
            if key in seen:
                continue
            seen.add(key)
            status, reason = review_match(candidate["title"], candidate["url"], parser)
            if status == "potential_addition_requires_verification":
                status = "needs_event_page_verification"
                reason = "Venue and time found in source metadata, but event page and calendar-date duplicates require independent confirmation"
            rows.append({"source": source["source"], **candidate, "status": status, "reason": reason})
    counts = {status: sum(row["status"] == status for row in rows) for status in sorted({r["status"] for r in rows})}
    report = {"read_only": True, "checked_at_pacific": now.isoformat(), "existing_listings": parser.event_count, "status_counts": counts, "events": rows, "note": "No events are approved for automatic publication; verify direct event pages, organizer, location, date, and date-specific duplicates."}
    Path("kjzy_addition_preview.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("KJZY AUTOMATIC ADDITION SAFETY PREVIEW")
    print("Current listings:", parser.event_count)
    print("Review totals:", json.dumps(counts, sort_keys=True))
    for row in rows:
        if row["status"] == "needs_event_page_verification":
            print("VERIFY:", json.dumps(row, ensure_ascii=False))
    print("READ ONLY. NO EVENTS ADDED OR PUBLISHED.")

if __name__ == "__main__":
    main()
