"""Audit KJZY insertion preview before allowing any publication."""
import json
import re
from collections import Counter
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

from kjzy_expiration_preview import CalendarParser, final_day
from kjzy_insertion_preview import event_block, EVENT_RE

def main():
    original = Path("SC_Events.html").read_text(encoding="utf-8")
    preview = Path("kjzy_insertion_preview.html").read_text(encoding="utf-8")
    proposal = json.loads(Path("kjzy_insertion_preview.json").read_text(encoding="utf-8"))
    original_parser, preview_parser = CalendarParser(original), CalendarParser(preview)
    original_parser.feed(original)
    preview_parser.feed(preview)
    before = [original[start:end] for start, end, _, _ in original_parser.events]
    after = [preview[start:end] for start, end, _, _ in preview_parser.events]
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    problems = []
    if len(before) != proposal["original_count"]:
        problems.append("Original count mismatch")
    if len(after) != proposal["preview_count"]:
        problems.append("Preview count mismatch")
    if len(after) - len(before) != proposal["proposed_additions"]:
        problems.append("Addition count mismatch")
    before_counter, after_counter = Counter(before), Counter(after)
    if any(after_counter[block] < count for block, count in before_counter.items()):
        problems.append("Original event changed or removed")
    if any(date.fromisoformat(row["date"]) < today for row in proposal["proposed_events"]):
        problems.append("Proposal contains past event")
    for row in proposal["proposed_events"]:
        block = event_block(row, date.fromisoformat(row["date"]).day).rstrip("\n")
        if block not in preview:
            problems.append("Missing exact proposed event block: " + row["title"])
    for start, end, year, month in preview_parser.events:
        block = preview[start:end]
        dm = re.search(r'<div class="date">([^<]+)</div>', block)
        if not dm or not year or not month or final_day(dm.group(1), year, month) is None:
            problems.append("Unparseable event date")
            break
    # Verify all non-event HTML is byte-for-byte unchanged. The only permitted
    # modifications are the new event blocks, not styling or existing content.
    cleaned = preview
    for row in reversed(proposal["proposed_events"]):
        block = event_block(row, date.fromisoformat(row["date"]).day)
        if cleaned.count(block) != 1:
            problems.append("Proposed event not uniquely identifiable: " + row["title"])
        else:
            cleaned = cleaned.replace(block, "", 1)
    if cleaned != original:
        problems.append("Non-event markup or original listing order changed")
    result = {
        "read_only": True,
        "passed": not problems,
        "original_listings": len(before),
        "preview_listings": len(after),
        "proposed_additions": proposal["proposed_additions"],
        "problems": problems,
        "note": "This audits structure and preservation; it does not authorize publishing.",
    }
    Path("kjzy_insertion_audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("KJZY INSERTION PREVIEW AUDIT:", json.dumps(result))
    if problems:
        raise RuntimeError("Preview audit failed; publication remains disabled")
    print("PREVIEW AUDIT PASSED. LIVE CALENDAR UNCHANGED.")

if __name__ == "__main__":
    main()
