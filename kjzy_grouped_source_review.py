"""Read-only grouped event-detail diagnostics for priority KJZY sources."""
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

SOURCES = ("Green Music Center", "Santa Rosa Symphony", "Luther Burbank Center", "Sonoma County Tourism Events", "Visit Santa Rosa Events")
LIMIT_PER_SOURCE = 3

class StructuredData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_json = False
        self.parts = []
        self.blocks = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and "ld+json" in a.get("type", "").lower():
            self.in_json = True
            self.parts = []
    def handle_data(self, data):
        if self.in_json:
            self.parts.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.in_json:
            self.blocks.append("".join(self.parts))
            self.in_json = False

def events(value):
    if isinstance(value, list):
        for item in value:
            yield from events(item)
    elif isinstance(value, dict):
        types = value.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if any(str(t).lower().endswith("event") for t in types):
            yield {"title": value.get("name"), "start_date": value.get("startDate"),
                   "event_url": value.get("url"), "location": value.get("location")}
        for key in ("@graph", "mainEntity", "itemListElement"):
            if key in value:
                yield from events(value[key])

def check(link):
    row = {"discovery_url": link["url"], "link_label": link.get("title", ""), "verified": False}
    try:
        req = Request(link["url"], headers={"User-Agent": "Mozilla/5.0 (compatible; KJZYSourceReview/1.0)"})
        with urlopen(req, timeout=10) as response:
            content = response.read(900000).decode("utf-8", errors="replace")
            row["http_status"] = response.status
            row["final_url"] = response.url
        parser = StructuredData()
        parser.feed(content)
        found = []
        for block in parser.blocks:
            try:
                found.extend(events(json.loads(block)))
            except (ValueError, TypeError):
                continue
        row["structured_events"] = found[:12]
        row["structured_event_count"] = len(found)
        row["next_step"] = "Independently verify event dates and duplicates" if found else "Requires source-specific extraction or feed"
    except Exception as exc:
        row["error"] = str(exc)[:200]
        row["next_step"] = "Investigate inaccessible detail page"
    return row

def main():
    report = json.loads(Path("kjzy_priority_source_review.json").read_text(encoding="utf-8"))
    results = []
    for name in SOURCES:
        source = next((s for s in report["priority_sources"] if s["source"].startswith(name)), None)
        if source is None:
            results.append({"source": name, "error": "Source absent from priority report", "checks": []})
            continue
        links = source.get("candidate_links", [])
        checks = [check(link) for link in links[:LIMIT_PER_SOURCE]]
        results.append({"source": source["source"], "candidate_links_available": len(links),
                        "detail_pages_checked": len(checks), "checks": checks,
                        "needs_custom_adapter": not any(c.get("structured_event_count", 0) for c in checks)})
    out = {"read_only": True, "checked_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
           "sources": results, "warning": "Discovery links and metadata are unverified; nothing is approved for publication."}
    Path("kjzy_grouped_source_review.json").write_text(json.dumps(out, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print("KJZY GROUPED PRIORITY SOURCE REVIEW")
    for row in results:
        count = sum(c.get("structured_event_count", 0) for c in row["checks"])
        print(row["source"], "| detail pages:", row.get("detail_pages_checked", 0), "| structured records:", count,
              "| custom extraction needed:", row["needs_custom_adapter"] if "needs_custom_adapter" in row else "unknown")
    print("READ ONLY. NO EVENTS PUBLISHED.")

if __name__ == "__main__":
    main()
