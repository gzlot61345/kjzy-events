"""Collect machine-readable event candidates from priority KJZY sources.

Read-only. Never treat discovery as publication approval.
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

LIMIT = 1100000
FEEDS_PER_SOURCE = 5
DETAIL_PAGES_PER_SOURCE = 12
EVENT_LINK = re.compile(r"(event|concert|show|performance|festival|ticket|calendar)", re.I)
WORKERS = 6
FEED_HINT = re.compile(r"(?:\.ics(?:$|\?)|/feed/?(?:$|\?)|ical|webcal)", re.I)

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.scripts = []
        self._script = False
        self._parts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("href"):
            self.links.append(a["href"])
        if tag == "script" and "ld+json" in a.get("type", "").lower():
            self._script = True
            self._parts = []
    def handle_data(self, data):
        if self._script:
            self._parts.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self._script:
            self.scripts.append("".join(self._parts))
            self._script = False

def json_events(node):
    if isinstance(node, list):
        for v in node:
            yield from json_events(v)
    elif isinstance(node, dict):
        typ = node.get("@type", [])
        if isinstance(typ, str):
            typ = [typ]
        if any(str(t).lower().split("/")[-1].endswith("event") for t in typ):
            loc = node.get("location")
            if isinstance(loc, list):
                loc = loc[0] if loc else None
            yield {"title": node.get("name"), "start_date": node.get("startDate"),
                   "end_date": node.get("endDate"), "event_url": node.get("url"),
                   "venue": loc.get("name") if isinstance(loc, dict) else None,
                   "format": "jsonld"}
        for key in ("@graph", "mainEntity", "itemListElement", "event", "events", "subEvent", "subjectOf"):
            if key in node:
                yield from json_events(node[key])

def fetch(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; KJZYCalendarCollector/1.0)",
                                "Accept": "text/html,text/calendar,application/json"})
    with urlopen(req, timeout=12) as response:
        data = response.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError("response exceeds safety limit")
        return response.url, response.headers.get("Content-Type", ""), data.decode("utf-8", errors="replace")

def ics_events(body, source_url):
    # Unfold RFC5545 continuation lines; leave recurrence expansion to a future verifier.
    lines = re.sub(r"\r?\n[ \t]", "", body).splitlines()
    result, event = [], None
    for line in lines:
        if line == "BEGIN:VEVENT":
            event = {}
        elif line == "END:VEVENT" and event is not None:
            if event.get("title") and event.get("start_date"):
                event.update({"format": "ics", "event_url": event.get("event_url") or source_url})
                result.append(event)
            event = None
        elif event is not None and ":" in line:
            key, val = line.split(":", 1)
            key = key.split(";", 1)[0].upper()
            field = {"SUMMARY": "title", "DTSTART": "start_date", "DTEND": "end_date",
                     "LOCATION": "venue", "URL": "event_url", "RRULE": "recurrence_rule"}.get(key)
            if field:
                event[field] = val[:500]
    return result

def inspect(item):
    row = {"source": item["source"], "url": item["url"], "events": [],
           "feed_urls_checked": [], "errors": [], "read_only": True}
    try:
        base, kind, body = fetch(item["url"])
        if "text/calendar" in kind or "BEGIN:VCALENDAR" in body[:200]:
            row["events"].extend(ics_events(body, base))
            row["method"] = "ics"
        else:
            page = Page()
            page.feed(body)
            for script in page.scripts:
                try:
                    row["events"].extend(json_events(json.loads(script)))
                except (ValueError, TypeError):
                    continue
            row["method"] = "jsonld"
            host = urlsplit(base).hostname
            feeds = []
            for href in page.links:
                link = urljoin(base, href)
                if urlsplit(link).hostname == host and FEED_HINT.search(link) and link not in feeds:
                    feeds.append(link)
            # Discover structured event records on linked detail pages, not only index pages.
            detail_links = []
            for href in page.links:
                link = urljoin(base, href)
                if (urlsplit(link).hostname == host and EVENT_LINK.search(urlsplit(link).path)
                        and link != base and link not in feeds and link not in detail_links):
                    detail_links.append(link)
            row["detail_urls_checked"] = []
            for link in detail_links[:DETAIL_PAGES_PER_SOURCE]:
                row["detail_urls_checked"].append(link)
                try:
                    final, ctype, detail = fetch(link)
                    subpage = Page()
                    subpage.feed(detail)
                    for script in subpage.scripts:
                        try:
                            row["events"].extend(json_events(json.loads(script)))
                        except (ValueError, TypeError):
                            continue
                except Exception as exc:
                    row["errors"].append("detail: " + str(exc)[:120])
            for link in feeds[:FEEDS_PER_SOURCE]:
                row["feed_urls_checked"].append(link)
                try:
                    final, ctype, content = fetch(link)
                    if "BEGIN:VCALENDAR" in content[:300]:
                        row["events"].extend(ics_events(content, final))
                except Exception as exc:
                    row["errors"].append(str(exc)[:140])
        # The Events Calendar (Luther Burbank Center) offers an iCalendar export.
        # Probe it explicitly because its "Export Events" link may be JS-generated.
        if "lutherburbankcenter.org" in urlsplit(base).hostname.lower():
            for calendar_url in (urljoin(base, "/events/?ical=1"),):
                if calendar_url not in row["feed_urls_checked"]:
                    row["feed_urls_checked"].append(calendar_url)
                    try:
                        final, ctype, content = fetch(calendar_url)
                        if "BEGIN:VCALENDAR" in content[:300]:
                            row["events"].extend(ics_events(content, final))
                            row["method"] = "official_ics_export"
                        else:
                            row["errors"].append("Official calendar export did not return ICS data")
                    except Exception as exc:
                        row["errors"].append("Official calendar export: " + str(exc)[:140])
        seen = set()
        clean = []
        for event in row["events"]:
            title, start = event.get("title"), event.get("start_date")
            if not isinstance(title, str) or not title.strip() or not isinstance(start, str) or not start.strip():
                continue
            key = (title.strip().casefold(), start.strip())
            if key not in seen:
                seen.add(key)
                clean.append(event)
        row["events"] = clean[:250]
        row["candidate_count"] = len(clean)
        row["status"] = "candidates_found" if clean else "adapter_needed"
        row["coverage_note"] = ("Machine-readable candidates found; not proof of full source coverage" if clean else "No machine-readable candidates found; source-specific adapter required")
        row["adapter_hint"] = ("Inspect structured calendar APIs, embedded widgets, or official feeds; never infer zero upcoming events from zero parsed records" if not clean else "Cross-check candidates against organizer details and calendar before publication")
    except Exception as exc:
        row["status"] = "access_or_parse_failure"
        row["coverage_note"] = "Source could not be accessed or parsed; do not count as verified"
        row["adapter_hint"] = "Investigate access failure or use an official alternative feed"
        row["errors"].append(str(exc)[:200])
        row["candidate_count"] = 0
    return row

def main():
    registry = json.loads(Path("refresh_summary.json").read_text(encoding="utf-8"))["source_coverage"]
    priority_path = Path("kjzy_priority_sources.txt")
    if priority_path.exists():
        priority_urls = [line.strip() for line in priority_path.read_text(encoding="utf-8").splitlines()
                         if line.strip() and not line.lstrip().startswith("#")]
        from urllib.parse import urldefrag
        selected = {urldefrag(url)[0].rstrip("/") for url in priority_urls}
        registry = [item for item in registry if urldefrag(item["url"])[0].rstrip("/") in selected]
        if len(registry) != len(priority_urls):
            raise RuntimeError("Priority source URLs do not all match the source registry")
    rows = [None] * len(registry)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(inspect, item): i for i, item in enumerate(registry)}
        for future in as_completed(futures):
            rows[futures[future]] = future.result()
    out = {"checked_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
           "read_only": True, "sources_checked": len(rows),
           "sources_with_candidates": sum(bool(r["candidate_count"]) for r in rows),
           "total_candidates": sum(r["candidate_count"] for r in rows),
           "warning": "Candidates are unverified; dates, links, recurrences and duplicates require verification.",
           "sources": rows}
    Path("kjzy_shared_collector_report.json").write_text(json.dumps(out, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print("KJZY SHARED COLLECTOR: %d/%d sources with candidates; %d unverified records" %
          (out["sources_with_candidates"], out["sources_checked"], out["total_candidates"]))
    for r in rows:
        print("%-58s | %-23s | %3d records | %d feeds | %d details" %
              (r["source"][:58], r["status"], r["candidate_count"], len(r["feed_urls_checked"]), len(r.get("detail_urls_checked", []))))
    print("READ ONLY. NO CALENDAR CHANGES.")

if __name__ == "__main__":
    main()
