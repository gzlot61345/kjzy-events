"""Read-only verification of direct event pages for KJZY addition candidates."""
import html
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
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
                    matches.append({"title": name, "date": event_date, "venue": venue, "city": normalize(location.get("address", {}).get("addressLocality", "")) if isinstance(location, dict) and isinstance(location.get("address"), dict) else "", "time_pacific": dt.astimezone(PACIFIC).strftime("%I:%M %p").lstrip("0") if dt.tzinfo else ""})
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

def corroborate(row, result, sources):
    """Find independent structured records and verify their direct event pages."""
    original_host = (urlsplit(row["url"]).hostname or "").removeprefix("www.")
    try:
        expected = datetime.fromisoformat(row["start_date"].replace("Z", "+00:00"))
    except (ValueError, KeyError):
        return result
    # Do not expand the geographic scope through fallback verification.
    local_cities = {"santa rosa", "sebastopol", "petaluma", "rohnert park",
                    "cotati", "windsor", "healdsburg", "cloverdale", "sonoma",
                    "guerneville", "forestville", "occidental", "graton",
                    "kenwood", "glen ellen", "bodega bay", "bodega",
                    "penngrove", "monte rio", "rio nido", "cazadero",
                    "jenner", "geyserville", "freestone",
                    "valley ford", "vineburg", "boyes hot springs", "el verano",
                    "fulton", "roseland", "larkfield", "mark west"}
    checked = set()
    for source in sources:
        for event in source.get("sample_events", []):
            url = str(event.get("url") or "")
            host = (urlsplit(url).hostname or "").removeprefix("www.")
            if not url.startswith("https://") or not host or host == original_host or url in checked:
                continue
            if similarity(event.get("title", ""), row["title"]) < 0.92:
                continue
            venue = normalize(event.get("location", ""))
            target = normalize(row["location"])
            if not venue or not target or similarity(venue, target) < 0.85:
                continue
            try:
                start = datetime.fromisoformat(str(event.get("start_date", "")).replace("Z", "+00:00"))
                if start.tzinfo is None or expected.tzinfo is None or start != expected:
                    continue
            except ValueError:
                continue
            checked.add(url)
            if len(checked) > 5:
                return result
            alternate = check({**row, "url": url})
            if alternate["status"] != "page_metadata_matches":
                continue
            page = alternate.get("page_event", {})
            if page.get("city") not in local_cities or page.get("time_pacific") != row["time_pacific"]:
                continue
            result.update({"status": "cross_source_verified_pending_link_review",
                           "verification_method": "independent_source",
                           "alternate_url": alternate["final_url"],
                           "alternate_source": source["source"],
                           "page_event": page})
            return result
    return result

def main():
    source = json.loads(Path("kjzy_addition_preview.json").read_text(encoding="utf-8"))
    candidates = [row for row in source["events"] if row["status"] == "needs_event_page_verification"]
    results = [None] * len(candidates)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(check, row): i for i, row in enumerate(candidates)}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    sources = json.loads(Path("kjzy_all_sources_report.json").read_text(encoding="utf-8"))["sources"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(corroborate, candidates[i], row, sources): i
                   for i, row in enumerate(results) if row["status"] != "page_metadata_matches"}
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
