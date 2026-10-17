"""Read-only LBC event discovery and comparison. No calendar changes."""
import json, re
from datetime import datetime, date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

URL = "https://lutherburbankcenter.org/events/"

class JsonLd(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts = []
        self.docs = []
    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type", "").lower() == "application/ld+json":
            self.active, self.parts = True, []
    def handle_data(self, data):
        if self.active: self.parts.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.active:
            try: self.docs.append(json.loads("".join(self.parts)))
            except ValueError: pass
            self.active = False

def events(node):
    if isinstance(node, list):
        for item in node: yield from events(item)
    if isinstance(node, dict):
        typ = node.get("@type", [])
        if isinstance(typ, str): typ = [typ]
        if "Event" in typ: yield node
        for value in node.values():
            if isinstance(value, (dict, list)): yield from events(value)

def norm_url(s):
    if not isinstance(s, str): return ""
    p = urlsplit(s)
    return urlunsplit((p.scheme.lower(), p.netloc.lower().removeprefix("www."), p.path.rstrip("/").lower(), "", ""))

def norm_title(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.title_depth = 0
        self.items = []
        self.current = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and self.depth == 0 and "event" in a.get("class", "").split():
            self.depth, self.current = 1, {"title": "", "url": ""}
            return
        if self.depth:
            if tag == "div":
                self.depth += 1
                if self.title_depth: self.title_depth += 1
                if "event-name" in a.get("class", "").split(): self.title_depth = 1
            if tag == "a" and self.title_depth and a.get("href"):
                self.current["url"] = a["href"]
    def handle_data(self, data):
        if self.title_depth: self.current["title"] += data
    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            if self.title_depth: self.title_depth -= 1
            self.depth -= 1
            if not self.depth:
                self.current["title"] = " ".join(self.current["title"].split())
                self.items.append(self.current)
                self.current = None

def main():
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    calendar = Calendar()
    calendar.feed(Path("SC_Events.html").read_text(encoding="utf-8"))
    if len(calendar.items) < 1: raise RuntimeError("Could not parse calendar")
    known_urls = {norm_url(e["url"]) for e in calendar.items if e["url"]}
    known_titles = {norm_title(e["title"]) for e in calendar.items if e["title"]}
    req = Request(URL, headers={"User-Agent": "KJZY-Calendar-ReadOnly-Checker/0.2", "Accept": "text/html"})
    with urlopen(req, timeout=30) as response:
        if "html" not in response.headers.get("Content-Type", "").lower(): raise RuntimeError("Non-HTML response")
        body = response.read(3_000_001)
        if len(body) > 3_000_000: raise RuntimeError("HTML too large")
        html = body.decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    parser = JsonLd()
    parser.feed(html)
    results, seen = [], set()
    for doc in parser.docs:
        for obj in events(doc):
            name = " ".join(str(obj.get("name") or "").split())
            url = obj.get("url") or ""
            if isinstance(url, dict): url = url.get("@id", "")
            if not isinstance(url, str): url = ""
            start = obj.get("startDate") or ""
            if not isinstance(start, str): start = ""
            try: day = date.fromisoformat(start[:10])
            except ValueError: day = None
            key = (norm_title(name), start, norm_url(url))
            if key in seen: continue
            seen.add(key)
            if not name or not day or not url.startswith(("https://", "http://")):
                status = "needs_review_missing_fields"
            elif day < today: status = "past_event"
            elif norm_url(url) in known_urls: status = "already_listed_url"
            elif norm_title(name) in known_titles: status = "possible_match_title_review"
            else: status = "candidate_review"
            location = obj.get("location")
            if isinstance(location, list): location = location[0] if location else None
            location_name = location.get("name", "") if isinstance(location, dict) else str(location or "")
            results.append({"title": name, "start_date": start, "url": url, "location": location_name, "status": status})
    counts = {}
    for e in results: counts[e["status"]] = counts.get(e["status"], 0) + 1
    report = {"source": URL, "as_of_pacific": today.isoformat(), "read_only": True,
              "calendar_entries": len(calendar.items), "extracted_events": len(results),
              "counts": counts, "events": results,
              "note": "Candidates are not verified for publishing; no files were modified."}
    Path("kjzy_lbc_discovery_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Calendar entries:", len(calendar.items), "LBC structured events:", len(results))
    for status, count in sorted(counts.items()): print(status + ":", count)
    for e in results:
        if e["status"] in ("candidate_review", "possible_match_title_review", "needs_review_missing_fields"):
            print("REVIEW CANDIDATE:", json.dumps(e, ensure_ascii=False))
    print("Read-only report saved. No calendar files modified.")

if __name__ == "__main__": main()
