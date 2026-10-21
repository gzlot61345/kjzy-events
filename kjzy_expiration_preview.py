"""Safely preview removal of expired KJZY listings. Does not modify master by default."""
import argparse
import json
import re
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

MONTHS = {name: n for n, name in enumerate(("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"), 1)}
ABBR = {name[:3].lower(): n for name, n in MONTHS.items()}

class CalendarParser(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.content = content
        self.offsets = [0]
        for line in content.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.year = None
        self.month = None
        self.heading = None
        self.depth = 0
        self.event_depth = None
        self.event_start = None
        self.events = []
        self.head_text = []
    def pos(self):
        line, col = self.getpos()
        return self.offsets[line - 1] + col
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("h2", "h3"):
            classes = attrs.get("class", "").split()
            if "year" in classes or "month" in classes:
                self.heading = "year" if "year" in classes else "month"
                self.head_text = []
        if tag == "div":
            self.depth += 1
            if "event" in attrs.get("class", "").split() and self.event_depth is None:
                self.event_depth = self.depth
                self.event_start = self.pos()
    def handle_data(self, data):
        if self.heading:
            self.head_text.append(data)
    def handle_endtag(self, tag):
        if tag in ("h2", "h3") and self.heading:
            value = "".join(self.head_text).strip()
            if self.heading == "year" and value.isdigit():
                self.year = int(value)
            if self.heading == "month":
                self.month = MONTHS.get(value)
            self.heading = None
        if tag == "div":
            if self.event_depth == self.depth:
                start = self.event_start
                end = self.content.find(">", self.pos()) + 1
                self.events.append((start, end, self.year, self.month))
                self.event_depth = None
            self.depth -= 1

def final_day(label, year, month):
    label = re.sub(r"\s+", " ", label.strip()).replace("-", "–")
    month_range = re.fullmatch(r"([A-Za-z]{3,9})–([A-Za-z]{3,9})", label)
    if month_range:
        start_month = ABBR.get(month_range.group(1)[:3].lower())
        end_month = ABBR.get(month_range.group(2)[:3].lower())
        if start_month != month or end_month is None:
            return None
        import calendar
        end_year = year + (end_month < start_month)
        return date(end_year, end_month, calendar.monthrange(end_year, end_month)[1])
    m = re.fullmatch(r"(\d{1,2})(?:–(\d{1,2}))?", label)
    if m:
        day = int(m.group(2) or m.group(1))
        try:
            return date(year, month, day)
        except ValueError:
            return None
    m = re.fullmatch(r"(\d{1,2})–([A-Za-z]{3,9})\s+(\d{1,2})", label)
    if m:
        end_month = ABBR.get(m.group(2)[:3].lower())
        if not end_month:
            return None
        end_year = year + (end_month < month)
        try:
            return date(end_year, end_month, int(m.group(3)))
        except ValueError:
            return None
    return None

def preview(content, today):
    parser = CalendarParser(content)
    parser.feed(content)
    removed, unknown, edits = [], [], []
    for start, end, year, month in parser.events:
        block = content[start:end]
        label_match = re.search(r'<div class="date">([^<]+)</div>', block)
        title_match = re.search(r'<div class="event-name">\s*<a[^>]*>(.*?)</a>', block, re.S)
        label = label_match.group(1) if label_match else ""
        title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip() if title_match else "(unknown)"
        end_date = final_day(label, year, month) if year and month else None
        row = {"date_label": label, "title": title, "year": year, "month": month}
        if end_date is None:
            unknown.append(row)
        elif end_date < today:
            removed.append(row)
            edits.append((start, end))
    updated = content
    for start, end in reversed(edits):
        updated = updated[:start] + updated[end:]
    original_count = len(parser.events)
    remaining = original_count - len(removed)
    if len(re.findall(r'<div class="event"(?:\s|>)', updated)) != remaining:
        raise RuntimeError("Event count mismatch; refusing to publish")
    return updated, {"date_checked_pacific": today.isoformat(), "original_count": original_count, "expired_count": len(removed), "remaining_count": remaining, "unresolved_date_labels": unknown, "expired_events": removed}

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--apply", action="store_true", help="Write SC_Events.html; never used by read-only workflow")
    args.add_argument("--date", help="Test date YYYY-MM-DD")
    opts = args.parse_args()
    today = date.fromisoformat(opts.date) if opts.date else datetime.now(ZoneInfo("America/Los_Angeles")).date()
    path = Path("SC_Events.html")
    content = path.read_text(encoding="utf-8")
    updated, report = preview(content, today)
    Path("kjzy_expiration_preview.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("KJZY EXPIRATION PREVIEW:", json.dumps({k: v for k, v in report.items() if k not in ("expired_events", "unresolved_date_labels")}))
    print("Unresolved date labels:", len(report["unresolved_date_labels"]))
    if opts.apply:
        if report["unresolved_date_labels"]:
            raise RuntimeError("Unresolved date labels exist; refusing automatic publication")
        updated = re.sub(r'(<div class="calendar-count">)\d+[^<]*(</div>)', lambda m: m.group(1) + str(report["remaining_count"]) + " event listings • Updated " + today.strftime("%B %d, %Y").replace(" 0", " ") + m.group(2), updated, count=1)
        path.write_text(updated, encoding="utf-8")
        print("UPDATED MASTER FILE; publication requires separate approval.")
    else:
        print("READ ONLY. MASTER UNCHANGED.")

if __name__ == "__main__":
    main()
