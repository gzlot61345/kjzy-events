"""Read-only inventory of all sources in the canonical KJZY source registry.

A successful HTTP response is NOT proof that an event inventory was retrieved.
This script never changes SC_Events.html or refresh_summary.json.
"""
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

MAX_BYTES = 1250000
WORKERS = 5

def events_in(node):
    if isinstance(node, list):
        for item in node:
            yield from events_in(item)
    elif isinstance(node, dict):
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if any(str(t).lower().split("/")[-1] == "event" for t in types):
            yield node
        for value in node.values():
            if isinstance(value, (dict, list)):
                yield from events_in(value)

class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.jsonld_count = 0
        self.documents = []
        self._jsonld = False
        self._parts = []
        self.iframe_count = 0
        self.calendar_clues = set()
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "script" and data.get("type", "").lower().strip() == "application/ld+json":
            self.jsonld_count += 1
            self._jsonld = True
            self._parts = []
        if tag == "iframe":
            self.iframe_count += 1
        for key in ("src", "href", "class", "id"):
            value = str(data.get(key, "")).lower()
            for clue in ("tribe-events", "eventbrite", "evvnt", "citiespark", "calendar", "fullcalendar"):
                if clue in value:
                    self.calendar_clues.add(clue)
    def handle_data(self, data):
        if self._jsonld:
            self._parts.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self._jsonld:
            try:
                self.documents.append(json.loads("".join(self._parts)))
            except (ValueError, TypeError):
                pass
            self._jsonld = False
            self._parts = []

def check_once(item):
    result = {"source": item["source"], "url": item["url"], "prior_status": item.get("status", "unknown")}
    try:
        request = Request(item["url"], headers={
            "User-Agent": "Mozilla/5.0 (compatible; KJZYReadOnlySourceCheck/1.0)",
            "Accept": "text/html,application/xhtml+xml",
        })
        with urlopen(request, timeout=18) as response:
            result["http_status"] = response.status
            result["final_url"] = response.url
            result["content_type"] = response.headers.get("Content-Type", "")
            raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            result["status"] = "inspection_limit"
            result["note"] = "Page exceeds inspection limit; event inventory not verified"
            return result
        if "html" not in result["content_type"].lower():
            result["status"] = "non_html"
            result["note"] = "Content type is not HTML; event inventory not verified"
            return result
        parser = Markup()
        parser.feed(raw.decode("utf-8", errors="replace"))
        events = []
        for document in parser.documents:
            for event in events_in(document):
                if isinstance(event, dict):
                    events.append({
                        "title": str(event.get("name", ""))[:180],
                        "start_date": str(event.get("startDate", ""))[:100],
                        "url": str(event.get("url", ""))[:300],
                        "end_date": str(event.get("endDate", ""))[:100],
                        "location": (str(event.get("location", {}).get("name", ""))
                            if isinstance(event.get("location"), dict)
                            else str(event.get("location", "")))[:200],
                    })
        result["structured_event_count"] = len(events)
        result["sample_events"] = events[:100]
        result["jsonld_scripts"] = parser.jsonld_count
        result["iframes"] = parser.iframe_count
        result["calendar_clues"] = sorted(parser.calendar_clues)
        result["status"] = "structured_events_found" if events else "reachable_inventory_unverified"
        result["note"] = ("Structured event records found; dates and links still require verification"
                          if events else "Page reachable, but no structured events found; may be dynamic or use a different format")
    except HTTPError as error:
        result["http_status"] = error.code
        result["status"] = "http_error"
        result["note"] = "Automated request refused or unavailable; not proof of missing events"
    except (URLError, TimeoutError, OSError, ValueError) as error:
        result["status"] = "request_failed"
        result["note"] = str(error)[:200]
    except Exception as error:
        result["status"] = "inspection_failed"
        result["note"] = (type(error).__name__ + ": " + str(error))[:200]
    return result

# Read-only pilot: try the calendar-specific endpoints independently of
# the generic homepage probe. Do not feed these records into publication yet.
PILOT_ENDPOINTS = {
    "Happening in Sonoma County": (
        "https://happeningsonomacounty.com/wp-json/tribe/events/v1/events",
        "https://happeningsonomacounty.com/calendar/",
    ),
    "Luther Burbank Center for the Arts — Official Events": (
        "https://lutherburbankcenter.org/wp-json/tribe/events/v1/events",
        "https://lutherburbankcenter.org/events/",
        "https://tickets.lutherburbankcenter.org/events",
    ),
}

def pilot(item):
    from urllib.parse import urlencode
    results = []
    for endpoint in PILOT_ENDPOINTS.get(item["source"], ()):
        record = {"endpoint": endpoint, "events": [], "read_only": True}
        try:
            api = "/wp-json/" in endpoint
            url = endpoint
            if api:
                url += "?" + urlencode({"start_date": datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d 00:00:00"), "per_page": 50})
            req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json" if api else "text/html"})
            with urlopen(req, timeout=12) as response:
                record["http_status"] = response.status
                raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise ValueError("Response exceeds inspection limit")
            if api:
                payload = json.loads(raw)
                record["total_reported"] = payload.get("total")
                record["total_pages"] = payload.get("total_pages")
                for event in payload.get("events", []):
                    venue = event.get("venue") or {}
                    if not isinstance(venue, dict):
                        venue = {}
                    record["events"].append({"title": event.get("title"), "start_date": event.get("start_date"), "timezone": event.get("timezone"), "url": event.get("url"), "venue": venue.get("venue"), "city": venue.get("city")})
            else:
                parser = Markup()
                parser.feed(raw.decode("utf-8", errors="replace"))
                for doc in parser.documents:
                    for event in events_in(doc):
                        record["events"].append({"title": event.get("name"), "start_date": event.get("startDate"), "url": event.get("url"), "location": event.get("location")})
            record["count"] = len(record["events"])
            record["status"] = "pilot_candidates_found" if record["count"] else "pilot_no_structured_records"
        except Exception as exc:
            record["status"] = "pilot_failed"
            record["error"] = str(exc)[:200]
        results.append(record)
    return results

def check(item):
    attempts = []
    for attempt in range(2):
        result = check_once(item)
        attempts.append(result.get('status'))
        if result.get('structured_event_count', 0) or result.get('status') not in ('request_failed', 'http_error', 'reachable_inventory_unverified'):
            break
    result['attempts'] = attempts
    if item['source'] in PILOT_ENDPOINTS:
        result['pilot_endpoints'] = pilot(item)
        for record in result['pilot_endpoints']:
            print('SOURCE PILOT:', item['source'], record['endpoint'], record['status'], 'records:', record.get('count', 0), 'error:', record.get('error', ''))
    return result

def main():
    registry = json.loads(Path("kjzy_sources.json").read_text(encoding="utf-8"))["sources"]
    sources = [{"source": item["name"], "url": item["url"]} for item in registry]
    if len(sources) != 31:
        raise RuntimeError("Expected 31 recorded sources; got %s. Check source registry." % len(sources))
    results = [None] * len(sources)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(check, source): i for i, source in enumerate(sources)}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    counts = dict(Counter(item["status"] for item in results))
    report = {
        "read_only": True,
        "checked_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
        "sources_checked": len(results),
        "status_counts": counts,
        "limitations": [
            "A reachable page does not establish full event inventory coverage.",
            "Structured event records are candidates, not automatically verified events.",
            "Some calendars load events in JavaScript or block automated requests.",
            "No published calendar files were modified.",
        ],
        "sources": results,
    }
    Path("kjzy_all_sources_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("KJZY ALL-SOURCE READ-ONLY REPORT")
    print("Sources checked:", len(results))
    print("Status totals:", json.dumps(counts, sort_keys=True))
    for index, item in enumerate(results, 1):
        print("%02d | %-31s | HTTP %-4s | structured events %-3s | %s" % (
            index, item["status"], item.get("http_status", "-"),
            item.get("structured_event_count", "-"), item["source"]))
        if item.get("sample_events"):
            for event in item["sample_events"][:2]:
                print("     SAMPLE EVENT:", json.dumps(event, ensure_ascii=False))
        if item["status"] not in ("structured_events_found", "reachable_inventory_unverified"):
            print("     NOTE:", item.get("note", ""))
    print("NO CALENDAR MODIFICATIONS. NO NETLIFY PUBLICATION.")

if __name__ == "__main__":
    main()
