"""Read-only diagnostic discovery for Symphony and Green Music Center."""
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
from pathlib import Path

SOURCES = {
    "Santa Rosa Symphony": "https://www.srsymphony.org/event-calendar/",
    "Green Music Center": "https://gmc.sonoma.edu/events/",
    "Green Music Center October": "https://gmc.sonoma.edu/category/events/october/",
    "Green Music Center November": "https://gmc.sonoma.edu/category/events/november/",
    "Santa Rosa Symphony Season Tickets": "https://www.srsymphony.org/event-calendar/season-tickets/",
}
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.href = None
        self.text = []
        self.links = []
        self.structured_scripts = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a":
            self.href = a.get("href")
            self.text = []
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.structured_scripts += 1
    def handle_data(self, data):
        if self.href is not None:
            self.text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.href is not None:
            self.links.append((self.href, " ".join(" ".join(self.text).split())))
            self.href = None
            self.text = []

def check(label, url):
    record = {"source": label, "url": url, "status": "unknown", "sample_links": []}
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; KJZYReadOnlySourceAudit/1.0)", "Accept": "text/html"})
        with urlopen(req, timeout=25) as resp:
            record["http_status"] = resp.status
            record["final_url"] = resp.url
            record["content_type"] = resp.headers.get("Content-Type", "")
            raw = resp.read(2500001)
        if len(raw) > 2500000:
            raise ValueError("Response exceeded 2.5MB inspection limit")
        if "html" not in record["content_type"].lower():
            raise ValueError("Response was not HTML")
        html = raw.decode("utf-8", errors="replace")
        parser = Links()
        parser.feed(html)
        seen = set()
        for href, title in parser.links:
            absolute = urljoin(record["final_url"], href)
            path = urlsplit(absolute).path.lower()
            if not re.search(r"/(event|events|concert|performance|calendar|show)(/|-)", path):
                continue
            if not title or absolute in seen:
                continue
            seen.add(absolute)
            record["sample_links"].append({"title": title[:160], "url": absolute})
            if len(record["sample_links"]) >= 60:
                break
        record["structured_script_tags"] = parser.structured_scripts
        record["html_bytes"] = len(raw)
        record["status"] = "fetched_for_diagnostic_review"
    except Exception as exc:
        record["status"] = "fetch_or_parse_failed"
        record["error"] = str(exc)[:350]
    return record

def main():
    results = [check(label, url) for label, url in SOURCES.items()]
    report = {"read_only": True, "checked_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(), "sources": results, "note": "Link samples are not verified events. No calendar modifications."}
    Path("kjzy_additional_sources_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for result in results:
        print(result["source"], "|", result["status"], "|", "candidate links:", len(result["sample_links"]), "|", "structured script tags:", result.get("structured_script_tags", 0))
        if result.get("error"):
            print("  ERROR:", result["error"])
        for item in result["sample_links"][:12]:
            print("  SAMPLE:", item["title"], "|", item["url"])
    print("Diagnostic only. No calendar files modified.")

if __name__ == "__main__":
    main()
