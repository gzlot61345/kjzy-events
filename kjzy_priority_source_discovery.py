"""Read-only event discovery for five priority KJZY calendars.

Follows a bounded number of links on each official event index and looks for
Event JSON-LD on event-detail pages. Findings are NOT eligible for automatic
publication until independently reviewed and the source is approved.
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

from kjzy_all_sources_probe import Markup, events_in

PRIORITY = {
    "Green Music Center — Official Events",
    "Luther Burbank Center for the Arts — Official Events",
    "Sonoma County Tourism Events",
    "Visit Santa Rosa Events",
    "Santa Rosa Symphony",
}
MAX_LINKS = 15
MAX_BYTES = 1000000
PATTERN = re.compile(r"event|concert|performance|show|ticket|symphony|season|music|festival", re.I)

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.href = None
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href")
            self.parts = []
    def handle_data(self, data):
        if self.href is not None:
            self.parts.append(data)
    def handle_endtag(self, tag):
        if tag == "a":
            if self.href:
                self.items.append((self.href, " ".join(self.parts).strip()))
            self.href = None
            self.parts = []

def fetch(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; KJZYEventDiscovery/1.0)", "Accept": "text/html"})
    with urlopen(req, timeout=15) as response:
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Page exceeds inspection limit")
        if "html" not in response.headers.get("Content-Type", "").lower():
            raise ValueError("Not an HTML page")
        return response.url, raw.decode("utf-8", errors="replace")

def discover(source):
    row = {"source": source["source"], "index": source["url"], "pages_checked": 0, "events": [], "errors": [], "read_only": True}
    try:
        base, html = fetch(source["url"])
        links = Links()
        links.feed(html)
        root_host = (urlsplit(base).hostname or "").removeprefix("www.")
        seen = {base.rstrip("/")}
        targets = []
        for href, title in links.items:
            url = urljoin(base, href)
            parts = urlsplit(url)
            host = (parts.hostname or "").removeprefix("www.")
            if parts.scheme not in ("http", "https") or host != root_host:
                continue
            if not PATTERN.search(title + " " + parts.path):
                continue
            url = parts._replace(fragment="", query="").geturl()
            if url.rstrip("/") in seen:
                continue
            seen.add(url.rstrip("/"))
            targets.append(url)
            if len(targets) >= MAX_LINKS:
                break
        row["links_selected"] = len(targets)
        def inspect(url):
            _, markup = fetch(url)
            parser = Markup()
            parser.feed(markup)
            events = []
            for doc in parser.documents:
                for event in events_in(doc):
                    if isinstance(event, dict):
                        location = event.get("location", "")
                        if isinstance(location, dict):
                            location = location.get("name", "")
                        events.append({"title": str(event.get("name", ""))[:180],
                                       "start_date": str(event.get("startDate", ""))[:100],
                                       "url": str(event.get("url") or url)[:350],
                                       "location": str(location)[:180],
                                       "discovered_at": url})
            return events
        with ThreadPoolExecutor(max_workers=4) as pool:
            jobs = {pool.submit(inspect, url): url for url in targets}
            for job in as_completed(jobs):
                row["pages_checked"] += 1
                try:
                    row["events"].extend(job.result())
                except Exception as exc:
                    row["errors"].append({"url": jobs[job], "reason": str(exc)[:120]})
        unique = {}
        for event in row["events"]:
            key = (event["title"], event["start_date"], event["url"])
            unique[key] = event
        row["events"] = list(unique.values())[:80]
    except Exception as exc:
        row["errors"].append({"url": source["url"], "reason": str(exc)[:160]})
    row["status"] = "candidate_metadata_found" if row["events"] else "no_verified_event_inventory"
    return row

def main():
    registry = json.loads(Path("refresh_summary.json").read_text(encoding="utf-8"))["source_coverage"]
    sources = [item for item in registry if item["source"] in PRIORITY]
    if len(sources) != 5:
        raise RuntimeError("Priority source registry changed; review configuration")
    rows = [discover(item) for item in sources]
    output = {"checked_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
              "read_only": True, "sources": rows,
              "warning": "Discovery is limited to 15 same-domain links per source. No discovered event is approved for automatic publication."}
    Path("kjzy_priority_source_discovery.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for row in rows:
        print(row["source"], "| pages", row["pages_checked"], "| event metadata", len(row["events"]), "| errors", len(row["errors"]))
    print("READ ONLY. NO CALENDAR CHANGES.")

if __name__ == "__main__":
    main()
