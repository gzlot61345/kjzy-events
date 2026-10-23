"""Read-only discovery of KJZY Community Calendar events.
No automatic publication: recurring date ranges require human/date-aware verification.
"""
import json
import re
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

URL = "https://kjzy.com/events/community-calendar"
DATE = re.compile(r"\\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\\s+\\d{1,2}(?:st|nd|rd|th)?\\b", re.I)

class Sections(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.capture = []
        self.heading = False
        self.anchor = None
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("h3", "h2"):
            self.heading = True
        if tag == "a":
            self.anchor = attrs.get("href")
        if tag in ("p", "div", "h3", "h2", "li", "br"):
            self.flush()
    def handle_data(self, data):
        if data.strip():
            self.capture.append(data.strip())
    def flush(self):
        if self.capture:
            value = " ".join(self.capture).strip()
            self.lines.append({"text": value, "heading": self.heading, "href": self.anchor})
            self.capture = []
    def handle_endtag(self, tag):
        if tag in ("h3", "h2", "p", "li", "div", "a"):
            self.flush()
        if tag in ("h3", "h2"):
            self.heading = False
        if tag == "a":
            self.anchor = None

def main():
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0 (compatible; KJZYCalendarAudit/1.0)"})
    with urlopen(req, timeout=25) as response:
        raw = response.read(2000000)
    parser = Sections()
    parser.feed(raw.decode("utf-8", errors="replace"))
    parser.flush()
    rows = []
    for i, item in enumerate(parser.lines):
        if not item["heading"] or not item["text"] or len(item["text"]) > 180:
            continue
        preceding = " ".join(x["text"] for x in parser.lines[max(0, i-12):i])
        dates = DATE.findall(preceding)
        following = parser.lines[i+1:i+22]
        links = [x["href"] for x in following if x["href"] and x["href"].startswith("http")]
        rows.append({"title": item["text"], "date_clues": dates[-2:],
                     "candidate_link": links[0] if links else None,
                     "status": "requires_date_link_duplicate_verification"})
    result = {"source": URL, "read_only": True,
              "checked_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
              "candidate_count": len(rows), "candidates": rows,
              "warning": "Date ranges may be recurring schedules; no events automatically approved."}
    Path("kjzy_community_calendar_candidates.json").write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\\n", encoding="utf-8")
    print("KJZY COMMUNITY CALENDAR: %s unverified candidate headings" % len(rows))
    for row in rows[:40]:
        print(row["title"], "|", ", ".join(row["date_clues"]))
    print("READ ONLY. NOTHING PUBLISHED.")

if __name__ == "__main__":
    main()
