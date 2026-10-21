"""Publish only a fully audited KJZY addition preview when explicitly enabled.

This script does not fetch events; the calling workflow must regenerate every
source report and audit from the same checkout immediately beforehand.
"""
import argparse
import json
import re
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

from kjzy_expiration_preview import preview as expiration_preview

PACIFIC = ZoneInfo("America/Los_Angeles")

def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--publish", action="store_true")
    args = cli.parse_args()
    original_path = Path("SC_Events.html")
    original = original_path.read_text(encoding="utf-8")
    proposed = Path("kjzy_insertion_preview.html").read_text(encoding="utf-8")
    audit = json.loads(Path("kjzy_insertion_audit.json").read_text(encoding="utf-8"))
    review = json.loads(Path("kjzy_insertion_preview.json").read_text(encoding="utf-8"))
    today = datetime.now(PACIFIC).date()

    if not audit.get("passed") or audit.get("problems"):
        raise RuntimeError("Insertion audit did not pass")
    if not review.get("read_only") or not audit.get("read_only"):
        raise RuntimeError("Missing read-only preview provenance")
    n = review["proposed_additions"]
    if n < 0 or n > 25:
        raise RuntimeError("Unexpected addition volume; manual investigation required")
    if audit["proposed_additions"] != n or audit["original_listings"] != review["original_count"]:
        raise RuntimeError("Inconsistent preview reports")
    if len(re.findall(r'<div class="event"(?:\s|>)', original)) != review["original_count"]:
        raise RuntimeError("Master changed after review")
    if any(date.fromisoformat(row["date"]) < today for row in review["proposed_events"]):
        raise RuntimeError("Past event in proposed additions")
    if n == 0:
        print("NO ADDITIONS. CALENDAR UNCHANGED.")
        return

    cleaned, expiration = expiration_preview(proposed, today)
    if expiration["unresolved_date_labels"]:
        raise RuntimeError("Unrecognized calendar date; refusing publication")
    if expiration["expired_count"]:
        raise RuntimeError("Preview includes expired events; run expiration cleanup first")

    header = re.compile(r'(<div class="calendar-count">)\d+[^<]*(</div>)')
    updated, count = header.subn(
        lambda m: m.group(1) + str(review["preview_count"]) + " event listings • Updated "
        + today.strftime("%B %d, %Y").replace(" 0", " ") + m.group(2),
        proposed, count=1
    )
    if count != 1:
        raise RuntimeError("Cannot locate calendar listing count")
    if len(re.findall(r'<div class="event"(?:\s|>)', updated)) != review["preview_count"]:
        raise RuntimeError("Final calendar count mismatch")
    print(f"SAFE PUBLICATION PREVIEW: {review['original_count']} + {n} = {review['preview_count']}")
    if args.publish:
        original_path.write_text(updated, encoding="utf-8")
        print("MASTER UPDATED LOCALLY. Workflow must commit and push to publish.")
    else:
        print("DRY RUN ONLY. MASTER UNCHANGED.")

if __name__ == "__main__":
    main()
