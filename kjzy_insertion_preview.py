"""Read-only KJZY HTML insertion preview. Never changes SC_Events.html."""
import html
import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlsplit

from kjzy_expiration_preview import MONTHS
from kjzy_candidate_review import canonical_url

MONTH_NAMES = {v: k for k, v in MONTHS.items()}
EVENT_RE = re.compile(r'<div class="event"(?:\s|>)')
HEADING_RE = re.compile(r'<h3 class="month">([^<]+)</h3>')
DATE_RE = re.compile(r'<div class="date">([^<]+)</div>')

def start_day(label):
    m = re.match(r"\s*(\d{1,2})", label)
    return int(m.group(1)) if m else 1

def event_block(row, day):
    title = html.escape(row["title"])
    url = html.escape(row["url"], quote=True)
    venue = html.escape(row["location"])
    time = html.escape(row["time_pacific"])
    return (
        '<div class="event">\n'
        f'<div class="date">{day}</div>\n'
        '<div>\n'
        f'<div class="event-name"><a href="{url}" rel="noopener noreferrer" target="_blank">{title}</a></div>\n'
        f'<div class="location">{venue} • {time}</div>\n'
        '</div>\n</div>\n'
    )

def insert_preview(master, candidates):
    updated = master
    inserted = []
    for row in sorted(candidates, key=lambda x: (x["date"], datetime.strptime(x["time_pacific"], "%I:%M %p").time(), x["title"])):
        event_date = date.fromisoformat(row["date"])
        month_label = MONTH_NAMES[event_date.month]
        year_heading = '<h2 class="year">' + str(event_date.year) + '</h2>'
        year_pos = updated.find(year_heading)
        if year_pos < 0:
            raise ValueError("Year section missing: " + str(event_date.year))
        year_end = updated.find('<h2 class="year">', year_pos + len(year_heading))
        if year_end < 0:
            year_end = len(updated)
        heading = '<h3 class="month">' + month_label + '</h3>'
        month_pos = updated.find(heading, year_pos, year_end)
        if month_pos < 0:
            raise ValueError("Month section missing: " + month_label)
        section_start = month_pos + len(heading)
        next_month = updated.find('<h3 class="month">', section_start, year_end)
        section_end = next_month if next_month >= 0 else year_end
        section = updated[section_start:section_end]
        entries = list(EVENT_RE.finditer(section))
        if not entries:
            raise ValueError("No existing events in month: " + month_label)
        at = section_end
        for entry in entries:
            dm = DATE_RE.search(section, entry.start(), entries[entries.index(entry)+1].start() if entries.index(entry)+1 < len(entries) else len(section))
            if dm and start_day(dm.group(1)) > event_date.day:
                at = section_start + entry.start()
                break
        block = event_block(row, event_date.day)
        updated = updated[:at] + block + updated[at:]
        inserted.append({"date": row["date"], "title": row["title"], "url": row["url"], "location": row["location"], "time_pacific": row["time_pacific"]})
    return updated, inserted

def main():
    original = Path("SC_Events.html").read_text(encoding="utf-8")
    report = json.loads(Path("kjzy_final_addition_review.json").read_text(encoding="utf-8"))
    candidates = [row for row in report["events"] if row["final_status"] == "ready_for_manual_publication_review"]
    existing_urls = {canonical_url(u) for u in re.findall(r'<div class="event">[\s\S]*?<a href="([^"]+)"', original)}
    candidates = [r for r in candidates if canonical_url(r["url"]) not in existing_urls]
    updated, inserted = insert_preview(original, candidates)
    old_count = len(EVENT_RE.findall(original))
    new_count = len(EVENT_RE.findall(updated))
    if new_count != old_count + len(inserted):
        raise RuntimeError("Insertion count mismatch")
    if not all(row["url"] in updated for row in inserted):
        raise RuntimeError("Missing inserted links")
    if updated.replace("\n", "") == original.replace("\n", "") and inserted:
        raise RuntimeError("Preview unexpectedly unchanged")
    output = {
        "read_only": True,
        "original_count": old_count,
        "proposed_additions": len(inserted),
        "preview_count": new_count,
        "excluded_for_review": len(report["events"]) - len(inserted),
        "proposed_events": inserted,
        "warning": "PREVIEW ONLY: No calendar changes or publication. Candidate events still require publication approval.",
    }
    Path("kjzy_insertion_preview.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    Path("kjzy_insertion_preview.html").write_text(updated, encoding="utf-8")
    print("KJZY HTML INSERTION PREVIEW (READ ONLY)")
    print("Current listings:", old_count)
    print("Proposed additions:", len(inserted))
    print("Preview listings:", new_count)
    print("Held for review:", output["excluded_for_review"])
    for row in inserted:
        print("PREVIEW:", row["date"], "|", row["title"])
    print("MASTER FILE UNCHANGED. NO PUBLICATION.")

if __name__ == "__main__":
    main()
