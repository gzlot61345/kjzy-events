"""Read-only comparison of Symphony event API queries and available metadata."""
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = "https://www.srsymphony.org/wp-json/tribe/events/v1/"
QUERIES = {
    "API metadata": ROOT,
    "Unfiltered events": ROOT + "events?per_page=5",
    "October 2026 events": ROOT + "events?" + urlencode({"start_date": "2026-10-01", "end_date": "2026-10-31", "per_page": 5}),
    "November 2026 events": ROOT + "events?" + urlencode({"start_date": "2026-11-01", "end_date": "2026-11-30", "per_page": 5}),
    "December 2026 events": ROOT + "events?" + urlencode({"start_date": "2026-12-01", "end_date": "2026-12-31", "per_page": 5}),
}

def inspect(name, url):
    result = {"name": name, "url": url}
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
        with urlopen(req, timeout=20) as resp:
            result["http_status"] = resp.status
            raw = resp.read(1000001)
        if len(raw) > 1000000:
            raise ValueError("Response too large")
        obj = json.loads(raw)
        if isinstance(obj, dict):
            result["top_level_keys"] = list(obj)[:25]
            result["total"] = obj.get("total")
            result["total_pages"] = obj.get("total_pages")
            events = obj.get("events", [])
            if isinstance(events, list):
                result["events_count"] = len(events)
                result["sample_events"] = [{"title": e.get("title"), "start_date": e.get("start_date"), "url": e.get("url")} for e in events[:5] if isinstance(e, dict)]
            if name == "API metadata":
                result["namespace"] = obj.get("namespace")
                result["routes"] = list(obj.get("routes", {}))[:12] if isinstance(obj.get("routes"), dict) else []
            if obj.get("message"):
                result["message"] = str(obj["message"])[:200]
        else:
            result["format"] = type(obj).__name__
    except Exception as exc:
        result["error"] = str(exc)[:250]
    return result

def main():
    results = [inspect(name, url) for name, url in QUERIES.items()]
    Path("kjzy_symphony_api_variants_report.json").write_text(json.dumps({"read_only": True, "results": results}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for r in results:
        print(r["name"], "| HTTP:", r.get("http_status", "failed"), "| total:", r.get("total", "unknown"), "| returned:", r.get("events_count", "n/a"))
        if r.get("error"):
            print(" ERROR:", r["error"])
        if r.get("message"):
            print(" MESSAGE:", r["message"])
        if r.get("routes"):
            print(" ROUTES:", r["routes"][:8])
        for e in r.get("sample_events", []):
            print(" EVENT:", json.dumps(e, ensure_ascii=False))
    print("Read-only; no calendar modifications.")
if __name__ == "__main__":
    main()
