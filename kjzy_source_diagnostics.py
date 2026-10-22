"""Read-only diagnostics for KJZY sources without structured event extraction.

Consumes the existing all-source report. Identifies calendar technology, source
access failures, and candidate same-domain event links for adapter development.
Never alters the published calendar or promotes links to verified events.
"""
import json
import re
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

KEYWORDS = re.compile(r"event|concert|show|performance|calendar|festival|ticket|what.s.on|schedule", re.I)
MAX_BYTES = 1400000

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
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
        if tag == "a" and self.href:
            self.links.append((self.href, " ".join(self.parts).strip()))
            self.href = None
            self.parts = []

def inspect(source):
    row = {k: source.get(k) for k in ("source", "url", "status", "http_status", "calendar_clues")}
    if source.get("structured_event_count", 0):
        row["next_step"] = "Structured events available; continue date/link verification"
        row["candidate_links"] = []
        return row
    if source.get("status") in ("http_error", "request_failed"):
        row["next_step"] = "Investigate blocked or failed access; no events inferred"
        row["candidate_links"] = []
        return row
    try:
        request = Request(source["url"], headers={"User-Agent": "Mozilla/5.0 (compatible; KJZYSourceDiagnostics/1.0)", "Accept": "text/html"})
        with urlopen(request, timeout=18) as response:
            raw = response.read(MAX_BYTES + 1)
            base = response.url
        if len(raw) > MAX_BYTES:
            row["next_step"] = "Large page; requires bounded or site-specific extraction"
            row["candidate_links"] = []
            return row
        parser = Links()
        parser.feed(raw.decode("utf-8", errors="replace"))
        host = urlsplit(base).hostname or ""
        matches = []
        seen = set()
        for href, title in parser.links:
            absolute = urljoin(base, href)
            parsed = urlsplit(absolute)
            if parsed.scheme not in ("http", "https") or (parsed.hostname or "") != host:
                continue
            if not KEYWORDS.search(title + " " + parsed.path):
                continue
            clean = parsed._replace(fragment="", query="").geturl()
            if clean in seen or clean.rstrip("/") == base.rstrip("/"):
                continue
            seen.add(clean)
            matches.append({"title": title[:120], "url": clean})
        row["candidate_links"] = matches[:12]
        row["next_step"] = ("Inspect event detail pages or site-specific feed" if matches else "Inspect JavaScript calendar/API or alternate source page")
        row["candidate_link_count"] = len(matches)
    except Exception as exc:
        row["candidate_links"] = []
        row["next_step"] = "Diagnostic fetch failed; investigate source access"
        row["diagnostic_error"] = str(exc)[:200]
    return row

def main():
    report = json.loads(Path("kjzy_all_sources_report.json").read_text(encoding="utf-8"))
    rows = [inspect(source) for source in report["sources"]]
    output = {"checked_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
              "sources": rows, "read_only": True,
              "warning": "Links are discovery clues, not verified event listings. Do not publish them directly."}
    Path("kjzy_source_diagnostics.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("KJZY SOURCE ADAPTER DIAGNOSTICS")
    for i, row in enumerate(rows, 1):
        print(f'{i:02d} | {row["source"]} | {row["status"]} | links={len(row["candidate_links"])} | {row["next_step"]}')
    print("READ ONLY. NO EVENTS ADDED OR PUBLISHED.")

if __name__ == "__main__":
    main()
