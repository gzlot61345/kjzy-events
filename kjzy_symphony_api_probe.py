"""Read-only Santa Rosa Symphony Events Calendar REST API test."""
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

BASE = "https://www.srsymphony.org/wp-json/tribe/events/v1/events"
PARAMS = {"start_date": datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat(), "per_page": 30, "page": 1}

def main():
    url = BASE + "?" + urlencode(PARAMS)
    report = {"source": "Santa Rosa Symphony", "endpoint": BASE, "read_only": True, "requested": PARAMS}
    try:
        req = Request(url, headers={"User-Agent": "KJZYCalendarReadOnlyAudit/1.0", "Accept": "application/json"})
        with urlopen(req, timeout=30) as response:
            report["http_status"] = response.status
            raw = response.read(1500001)
        if len(raw) > 1500000:
            raise ValueError("API response exceeded 1.5 MB safety limit")
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("Unexpected API response format")
        report["total"] = data.get("total")
        report["total_pages"] = data.get("total_pages")
        events = data.get("events", [])
        if not isinstance(events, list):
            raise ValueError("API did not return an events list")
        report["events"] = [
            {"title": e.get("title", ""), "start_date": e.get("start_date", ""), "url": e.get("url", ""), "id": e.get("id")}
            for e in events if isinstance(e, dict)
        ]
        report["status"] = "events_returned" if report["events"] else "empty_events"
    except Exception as exc:
        report["status"] = "failed"
        report["error"] = str(exc)[:350]
    Path("kjzy_symphony_api_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Santa Rosa Symphony API |", report["status"], "| HTTP:", report.get("http_status", "unavailable"), "| total:", report.get("total", "unknown"), "| events this page:", len(report.get("events", [])))
    if "error" in report:
        print("ERROR:", report["error"])
    for event in report.get("events", [])[:12]:
        print("EVENT:", json.dumps(event, ensure_ascii=False))
    print("Read-only. No calendar files modified.")

if __name__ == "__main__":
    main()
