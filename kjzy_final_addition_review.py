"""Read-only final date-aware duplicate and source-page checks for KJZY additions."""
import html
import json
import re
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from kjzy_candidate_review import canonical_url, normalize, similarity
from kjzy_expiration_preview import final_day, MONTHS

class Existing(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.year = None
        self.month = None
        self.heading = None
        self.head_parts = []
        self.depth = 0
        self.event_depth = None
        self.date_depth = None
        self.title_anchor = False
        self.events = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = a.get("class", "").split()
        if tag in ("h2", "h3") and ("year" in classes or "month" in classes):
            self.heading = "year" if "year" in classes else "month"
            self.head_parts = []
        if tag == "div":
            self.depth += 1
            if "event" in classes and self.event_depth is None:
                self.event_depth = self.depth
                self.current = {"year": self.year, "month": self.month, "date_label": "", "title": "", "url": ""}
            elif self.event_depth is not None and "date" in classes:
                self.date_depth = self.depth
        if tag == "a" and self.event_depth is not None and self.current.get("url", "") == "":
            self.current["url"] = a.get("href", "")
            self.title_anchor = True
    def handle_data(self, data):
        if self.heading:
            self.head_parts.append(data)
        if self.date_depth is not None:
            self.current["date_label"] += data
        if self.title_anchor:
            self.current["title"] += data
    def handle_endtag(self, tag):
        if tag in ("h2", "h3") and self.heading:
            value = "".join(self.head_parts).strip()
            if self.heading == "year" and value.isdigit():
                self.year = int(value)
            if self.heading == "month":
                self.month = MONTHS.get(value)
            self.heading = None
        if tag == "a":
            self.title_anchor = False
        if tag == "div":
            if self.depth == self.date_depth:
                self.date_depth = None
            if self.depth == self.event_depth:
                self.events.append(self.current)
                self.event_depth = None
            self.depth -= 1

def same_date(existing, candidate_date):
    year, month = existing["year"], existing["month"]
    if not year or not month:
        return True  # Uncertain: avoid approving duplicate
    try:
        target = date.fromisoformat(candidate_date)
    except ValueError:
        return True
    label = existing["date_label"].strip().replace("-", "–")
    end = final_day(label, year, month)
    if end is None:
        return True
    start_match = re.match(r"^(\\d{1,2})", label)
    start = date(year, month, int(start_match.group(1))) if start_match else date(year, month, 1)
    return start <= target <= end

def main():
    calendar = Existing()
    calendar.feed(Path("SC_Events.html").read_text(encoding="utf-8"))
    addition = json.loads(Path("kjzy_addition_preview.json").read_text(encoding="utf-8"))
    verified = json.loads(Path("kjzy_event_page_verification.json").read_text(encoding="utf-8"))
    approved_pages = {(row["url"], row["date"]): row for row in verified["events"] if row["status"] == "page_metadata_matches"}
    rows = []
    for candidate in addition["events"]:
        if candidate["status"] != "needs_event_page_verification":
            continue
        key = (candidate["url"], candidate["date"])
        if key not in approved_pages:
            rows.append({**candidate, "final_status": "hold_page_not_verified"})
            continue
        matches = []
        for existing in calendar.events:
            if canonical_url(existing["url"]) == canonical_url(candidate["url"]):
                matches.append({"title": existing["title"], "reason": "same_link"})
            elif same_date(existing, candidate["date"]) and similarity(existing["title"], candidate["title"]) >= 0.78:
                matches.append({"title": existing["title"], "reason": "similar_title_on_overlapping_date"})
        status = "hold_possible_duplicate" if matches else "ready_for_manual_publication_review"
        rows.append({**candidate, "final_status": status, "matching_existing_events": matches[:5]})
    counts = dict(Counter(r["final_status"] for r in rows))
    result = {"read_only": True, "calendar_events_checked": len(calendar.events), "status_counts": counts, "events": rows,
              "note": "No geographic exclusion for Novato or San Francisco. Ready for manual review is NOT authorization for automatic publishing."}
    Path("kjzy_final_addition_review.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")
    print("KJZY DATE-AWARE ADDITION SAFETY REVIEW")
    print("Calendar listings compared:", len(calendar.events))
    print("Results:", json.dumps(counts, sort_keys=True))
    for row in rows:
        print("REVIEW:", row["final_status"], "|", row["date"], "|", row["title"])
    print("READ ONLY. NO CALENDAR CHANGES.")

if __name__ == "__main__":
    main()
