#!/usr/bin/env python3
"""KJZY read-only calendar audit and event-source connectivity probe."""
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from zoneinfo import ZoneInfo

SOURCES = {
    "Santa Rosa Symphony homepage": "https://www.srsymphony.org/",
    "Santa Rosa Symphony calendar": "https://www.srsymphony.org/event-calendar/",
    "Santa Rosa Symphony season": "https://www.srsymphony.org/2026-2027-season/",
    "Green Music Center events": "https://gmc.sonoma.edu/all-events/",
    "Luther Burbank Center events": "https://lutherburbankcenter.org/events/",
}

class Signals(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = 0
        self.event_jsonld = 0
        self.in_script = False
        self.script_type = ""
        self.script_parts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links += 1
        if tag == "script":
            self.in_script = True
            self.script_type = a.get("type", "").lower()
            self.script_parts = []
    def handle_data(self, data):
        if self.in_script and self.script_type == "application/ld+json":
            self.script_parts.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.in_script:
            if self.script_type == "application/ld+json":
                try:
                    obj = json.loads("".join(self.script_parts))
                    def count(node):
                        if isinstance(node, list):
                            return sum(count(x) for x in node)
                        if isinstance(node, dict):
                            typ = node.get("@type", [])
                            if isinstance(typ, str):
                                typ = [typ]
                            return int("Event" in typ) + sum(count(v) for k, v in node.items() if k not in ("@type",))
                        return 0
                    self.event_jsonld += count(obj)
                except (ValueError, TypeError):
                    pass
            self.in_script = False

def probe(url):
    req = Request(url, headers={"User-Agent": "KJZY-Calendar-ReadOnly-Checker/0.1", "Accept": "text/html"})
    try:
        with urlopen(req, timeout=18) as response:
            status = response.status
            ctype = response.headers.get("Content-Type", "")
            if "html" not in ctype.lower():
                return {"status": "unsupported_content_type", "http_status": status, "content_type": ctype}
            data = response.read(2_000_001)
            if len(data) > 2_000_000:
                return {"status": "too_large", "http_status": status}
            html = data.decode(response.headers.get_content_charset() or "utf-8", errors="replace")
            parser = Signals()
            parser.feed(html)
            return {"status": "fetched", "http_status": status, "final_url": response.geturl(),
                    "bytes": len(data), "links": parser.links,
                    "structured_event_signals": parser.event_jsonld,
                    "note": "Zero structured events does not mean the page has no events."}
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
        return {"status": "fetch_failed", "error": str(error)[:250]}

def audit(html):
    events = re.findall(r'<div class="event"(?:\s[^>]*)?>', html)
    banner = re.search(r'(\d+) upcoming unique event listings', html)
    headings = re.findall(r'<h[23] class="(?:year|month)">([^<]+)</h[23]>', html)
    return {"actual_events": len(events),
            "displayed_events": int(banner.group(1)) if banner else None,
            "count_matches": bool(banner) and len(events) == int(banner.group(1)),
            "heading_count": len(headings),
            "warning": "This audit checks structure and count only; it does not verify event dates or links."}

def main():
    html = Path("SC_Events.html").read_text(encoding="utf-8")
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
    report = {"date_pacific": today, "read_only": True, "publishing_enabled": False,
              "calendar_audit": audit(html),
              "sources": {name: {"url": url, **probe(url)} for name, url in SOURCES.items()}}
    Path("kjzy_read_only_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Calendar entries:", report["calendar_audit"]["actual_events"])
    print("Count matches:", report["calendar_audit"]["count_matches"])
    for name, result in report["sources"].items():
        print(name + ":", result["status"], "structured events:", result.get("structured_event_signals", "n/a"))
    print("Read-only test finished; no calendar files modified.")
    if not report["calendar_audit"]["count_matches"]:
        raise SystemExit("Calendar count mismatch")

if __name__ == "__main__":
    main()
