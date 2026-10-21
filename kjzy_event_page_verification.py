"""Read-only verification of direct event pages for KJZY addition candidates."""
import html
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from kjzy_all_sources_probe import Markup, events_in
from kjzy_candidate_review import normalize, similarity

MAX_BYTES = 1000000
PACIFIC = ZoneInfo("America/Los_Angeles")

def check(row):
    result = {k: row.get(k) for k in ("title", "url", "date", "location", "source")}
    try:
        req = Request(row["url"], headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
        with urlopen(req, timeout=12) as response:
            result["http_status"] = response.status
            result["final_url"] = response.url
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                result["status"] = "manual_review_page_too_large"
                return result
            if "html" not in response.headers.get("Content-Type", "").lower():
                result["status"] = "manual_review_non_html"
                return result
        parser = Markup()
        parser.feed(raw.decode("utf-8", errors="replace"))
        matches = []
        for doc in parser.documents:
            for event in events_in(doc):
                name = html.unescape(str(event.get("name", "")))
                start = str(event.get("startDate", ""))
                location = event.get("location", {})
                venue = str(location.get("name", "")) if isinstance(location, dict) else str(location)
                try:
                    dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                    event_date = dt.astimezone(PACIFIC).date().isoformat() if dt.tzinfo else start[:10]
                except ValueError:
                    event_date = ""
                if similarity(name, row["title"]) >= 0.88 and event_date == row["date"]:
                    matches.append({"title": name, "date": event_date, "venue": venue})
        if len(matches) == 1:
            venue = normalize(matches[0]["venue"])
            expected = normalize(row["location"])
            if venue and expected and (venue in expected or expected in venue or similarity(venue, expected) >= 0.75):
                result["status"] = "page_metadata_matches"
            else:
                result["status"] = "manual_review_venue_mismatch"
            result["page_event"] = matches[0]
        elif len(matches) > 1:
            result["status"] = "manual_review_multiple_matches"
        else:
            result["status"] = "manual_review_no_matching_event_metadata"
    except HTTPError as error:
        result["http_status"] = error.code
        result["status"] = "manual_review_http_error"
    except (URLError, TimeoutError, OSError, ValueError) as error:
        result["status"] = "manual_review_request_failed"
        result["error"] = str(error)[:150]
    return result

def main():
    source = json.loads(Path("kjzy_addition_preview.json").read_text(encoding="utf-8"))
    candidates = [row for row in source["events"] if row["status"] == "needs_event_page_verification"]
    results = [None] * len(candidates)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(check, row): i for i, row in enumerate(candidates)}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    counts = dict(Counter(row["status"] for row in results))
    report = {
        "read_only": True,
        "checked_at_pacific": datetime.now(PACIFIC).isoformat(),
        "candidates_checked": len(results),
        "status_counts": counts,
        "events": results,
        "warning": "Matching metadata is not permission to publish: date-specific duplicates, Sonoma County geography, and organizer legitimacy require further checks.",
    }
    Path("kjzy_event_page_verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("KJZY DIRECT EVENT PAGE VERIFICATION (READ ONLY)")
    print("Candidates checked:", len(results))
    print("Results:", json.dumps(counts, sort_keys=True))
    for row in results:
        print("CHECK:", json.dumps(row, ensure_ascii=False))
    print("NO EVENTS ADDED OR PUBLISHED.")

if __name__ == "__main__":
    main()
