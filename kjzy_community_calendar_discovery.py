"""Read-only extraction of event titles, displayed date ranges, and organizer links.
Displayed date ranges are NOT individual recurring performance dates.
"""
import json
import re
from datetime import datetime, date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

URL = "https://kjzy.com/events/community-calendar"
DATE = re.compile(r"^(?:(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s+)?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?$", re.I)
TIME = re.compile(r"^\d{1,2}:\d{2}\s*(?:AM|PM)(?:\s*-\s*\d{1,2}:\d{2}\s*(?:AM|PM))?$", re.I)

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens = []
        self.heading_depth = 0
        self.link = None
        self.in_script = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.in_script = True
        if tag == "h3":
            self.heading_depth += 1
        if tag == "a":
            self.link = attrs.get("href")
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.in_script = False
        if tag == "h3":
            self.heading_depth = max(0, self.heading_depth-1)
        if tag == "a":
            self.link = None
    def handle_data(self, data):
        if self.in_script:
            return
        value = " ".join(data.split())
        if value:
            self.tokens.append({"text": value, "heading": bool(self.heading_depth), "href": self.link})

def extract(tokens):
    headings = [i for i, token in enumerate(tokens) if token["heading"]]
    rows = []
    for pos, i in enumerate(headings):
        item = tokens[i]
        if not item["text"] or len(item["text"]) > 180:
            continue
        # Date/time display is immediately BEFORE the title, not after it.
        before = [t["text"] for t in tokens[max(0, i-12):i]]
        dates = [t for t in before if DATE.fullmatch(t)]
        times = [t for t in before if TIME.fullmatch(t)]
        end = headings[pos+1] if pos+1 < len(headings) else len(tokens)
        section = tokens[i+1:end]
        # Only the organizer's explicit Website link is eligible, not images or navigation.
        website = None
        for j, token in enumerate(section):
            if token["text"].lower().rstrip(":") == "website":
                for candidate in section[j:j+5]:
                    if candidate["href"] and candidate["href"].startswith(("https://", "http://")):
                        website = urljoin(URL, candidate["href"])
                        break
                if website:
                    break
        rows.append({
            "title": item["text"], "displayed_dates": dates[-2:],
            "displayed_time": times[-1] if times else None,
            "organizer_website": website,
            "status": "requires_individual_date_link_and_duplicate_verification",
        })
    return rows


def classify(rows):
    """Conservative review only: date ranges never imply every date is an event."""
    from kjzy_candidate_review import CalendarLinks, normalize
    calendar = CalendarLinks()
    calendar.feed(Path("SC_Events.html").read_text(encoding="utf-8"))
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    for row in rows:
        dates = row["displayed_dates"]
        parsed = []
        for label in dates:
            m = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})", label, re.I)
            if not m:
                continue
            month = datetime.strptime(m.group(1).title(), "%B").month
            day = int(m.group(2))
            year = today.year
            # Calendar listing spans may cross New Year.
            if parsed and (month, day) < (parsed[-1].month, parsed[-1].day):
                year = parsed[-1].year + 1
            try:
                parsed.append(date(year, month, day))
            except ValueError:
                pass
        row["interpreted_bounds"] = [d.isoformat() for d in parsed]
        row["review_flags"] = []
        if len(parsed) == 2 and parsed[1] < parsed[0]:
            row["review_flags"].append("reversed_range")
        if len(dates) == 2 and len(parsed) != 2:
            row["review_flags"].append("date_range_parse_failed")
        if len(dates) == 2 and parsed:
            # A displayed span is not evidence that every day is an occurrence.
            row["review_flags"].append("range_or_recurring_dates_not_verified")
        if parsed and parsed[-1] < today:
            row["review_flags"].append("displayed_range_expired")
        if not row["organizer_website"]:
            row["review_flags"].append("missing_organizer_link")
        if row["organizer_website"] and re.search(r"/202[0-5](?:/|\b)", urlsplit(row["organizer_website"]).path):
            row["review_flags"].append("organizer_link_may_be_stale")
        title = normalize(row["title"])
        row["existing_title_match"] = title in calendar.titles
        if row["existing_title_match"]:
            row["review_flags"].append("title_already_on_calendar_check_date")
        elif title and len(title) >= 12:
            from difflib import SequenceMatcher
            if any(SequenceMatcher(None, title, existing).ratio() >= .88 for existing in calendar.titles):
                row["review_flags"].append("similar_title_on_calendar_check_date")
        row["status"] = "manual_verification_required"
    return rows

def main():
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0 (compatible; KJZYCalendarAudit/1.1)"})
    with urlopen(req, timeout=25) as response:
        raw = response.read(2000000)
    parser = CalendarParser()
    parser.feed(raw.decode("utf-8", errors="replace"))
    rows = classify(extract(parser.tokens))
    result = {
        "source": URL, "read_only": True,
        "checked_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
        "candidate_count": len(rows),
        "with_displayed_date": sum(bool(r["displayed_dates"]) for r in rows),
        "with_organizer_website": sum(bool(r["organizer_website"]) for r in rows),
        "matching_calendar_titles": sum(r["existing_title_match"] for r in rows),
        "unmatched_titles": sum(not r["existing_title_match"] for r in rows),
        "date_parse_failures": sum("date_range_parse_failed" in r["review_flags"] for r in rows),
        "range_or_recurring": sum("range_or_recurring_dates_not_verified" in r["review_flags"] for r in rows),
        "warning": "All rows require verification of each actual occurrence, year, weekday, venue and direct event page.",
        "candidates": rows,

    }
    Path("kjzy_community_calendar_candidates.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("KJZY COMMUNITY CALENDAR:", len(rows), "unverified candidates")
    print("With displayed dates:", result["with_displayed_date"])
    print("With organizer websites:", result["with_organizer_website"])
    print("Exact calendar title matches:", result["matching_calendar_titles"])
    print("Ranges requiring occurrence checks:", result["range_or_recurring"])
    print("Date parse failures:", result["date_parse_failures"])
    print("Unmatched titles needing individual verification:", result["unmatched_titles"])
    for row in rows:
        print(row["title"], "|", " to ".join(row["displayed_dates"]), "|", row["organizer_website"] or "no organizer link")
    print("READ ONLY. NOTHING PUBLISHED.")

if __name__ == "__main__":
    main()
