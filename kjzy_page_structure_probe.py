"""Read-only page-structure diagnostic for Symphony and Green Music Center."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

PAGES = {
    "Symphony calendar": "https://www.srsymphony.org/event-calendar/",
    "Symphony classical series": "https://www.srsymphony.org/event-calendar/season-tickets/classical-series/",
    "Green Music Center October": "https://gmc.sonoma.edu/category/events/october/",
    "Green Music Center November": "https://gmc.sonoma.edu/category/events/november/",
}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.active_link = None
        self.link_text = []
        self.times = []
        self.date_attributes = []
        self.scripts = []
        self.meta = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a":
            self.active_link = a.get("href")
            self.link_text = []
        if tag == "time":
            self.times.append({"datetime": a.get("datetime", ""), "class": a.get("class", "")})
        for k, v in a.items():
            if k in ("data-date", "data-start", "data-event-date", "startdate", "datetime"):
                self.date_attributes.append({"tag": tag, "attribute": k, "value": str(v)[:120]})
        if tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        if tag == "meta" and (a.get("property", "").startswith("og:") or a.get("name", "").startswith("twitter:")):
            self.meta.append({"name": a.get("property") or a.get("name"), "content": a.get("content", "")[:160]})
    def handle_data(self, data):
        if self.active_link is not None:
            self.link_text.append(data)
    def handle_endtag(self, tag):
        if tag == "a" and self.active_link is not None:
            title = " ".join(" ".join(self.link_text).split())
            if title:
                self.links.append({"title": title[:130], "url": self.active_link})
            self.active_link = None
            self.link_text = []

def inspect(name, url):
    result = {"source": name, "url": url, "read_only": True}
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
        with urlopen(request, timeout=25) as response:
            result["http_status"] = response.status
            final_url = response.url
            body = response.read(2000001)
        if len(body) > 2000000:
            raise ValueError("Page exceeded diagnostic size limit")
        html = body.decode("utf-8", errors="replace")
        page = Page()
        page.feed(html)
        links = []
        seen = set()
        for item in page.links:
            absolute = urljoin(final_url, item["url"])
            host = urlsplit(absolute).netloc.lower()
            if not host.endswith(("srsymphony.org", "sonoma.edu")):
                continue
            if absolute in seen:
                continue
            seen.add(absolute)
            links.append({"title": item["title"], "url": absolute})
        # The existing probe filtered event URLs too aggressively. Sample all local links.
        result["links"] = links[:120]
        result["link_count"] = len(links)
        result["time_tags"] = page.times[:35]
        result["date_attributes"] = page.date_attributes[:35]
        result["script_paths"] = [urljoin(final_url, s) for s in page.scripts if re.search(r"calendar|event|tribe|ajax|schedule", s, re.I)][:20]
        result["metadata"] = page.meta[:12]
        result["date_like_snippets"] = list(dict.fromkeys(re.findall(
            r".{0,55}(?:2026[-/]\\d{2}[-/]\\d{2}|2027[-/]\\d{2}[-/]\\d{2}|(?:Oct|Nov|Dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep)[a-z]*\\s+\\d{1,2}).{0,55}",
            re.sub(r"\\s+", " ", html), flags=re.I)))[:12]
        result["status"] = "inspected"
    except Exception as exc:
        result["status"] = "failed"
        result["error"] = str(exc)[:250]
    return result

def main():
    results = [inspect(name, url) for name, url in PAGES.items()]
    Path("kjzy_page_structure_report.json").write_text(json.dumps({"read_only": True, "sources": results}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for r in results:
        print(r["source"], "|", r["status"], "| links:", r.get("link_count", 0), "| time tags:", len(r.get("time_tags", [])), "| date attributes:", len(r.get("date_attributes", [])))
        if r.get("error"):
            print("  ERROR:", r["error"])
        for x in r.get("time_tags", [])[:4]:
            print("  TIME:", x)
        for x in r.get("date_attributes", [])[:4]:
            print("  DATE ATTRIBUTE:", x)
        for x in r.get("links", [])[:10]:
            print("  LINK:", x["title"], "|", x["url"])
        for x in r.get("script_paths", [])[:3]:
            print("  SCRIPT:", x)
    print("Read-only diagnostic. No calendar files modified.")

if __name__ == "__main__":
    main()
