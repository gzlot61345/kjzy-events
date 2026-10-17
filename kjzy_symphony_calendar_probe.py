"""Read-only investigation of the Santa Rosa Symphony events-calendar plugin."""
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin

URLS = {
    "Symphony events calendar": "https://www.srsymphony.org/event-calendar/",
    "Symphony season": "https://www.srsymphony.org/2026-2027-season/",
    "Symphony events tickets": "https://www.srsymphony.org/events-tickets/",
}
PATTERNS = {
    "event_plugin": r".{0,110}(?:the-events-calendar|tribe-events|eventCalendar|event-calendar|tribe\\/v1|wp-json).{0,180}",
    "date_clues": r".{0,90}(?:2026[-/]1[012][-/]\\d{1,2}|2027[-/]\\d{1,2}[-/]\\d{1,2}|November\\s+\\d{1,2}|December\\s+\\d{1,2}).{0,110}",
    "embedded_frames": r"<iframe\\b[^>]{0,500}>",
}
def inspect(name, url):
    record = {"source": name, "url": url}
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
        with urlopen(request, timeout=25) as response:
            raw = response.read(2000001)
            record["status"] = response.status
            record["final_url"] = response.url
        if len(raw) > 2000000:
            raise ValueError("Response exceeded 2MB limit")
        html = raw.decode("utf-8", errors="replace")
        record["html_length"] = len(html)
        for label, pattern in PATTERNS.items():
            matches = re.findall(pattern, html, flags=re.I | re.S)
            record[label] = list(dict.fromkeys(re.sub(r"\\s+", " ", match)[:300] for match in matches))[:8]
        record["wp_api_reference"] = bool(re.search(r"wp-json|api\\.w\\.org", html, flags=re.I))
    except Exception as exc:
        record["error"] = str(exc)[:220]
    return record
def main():
    results = [inspect(name, url) for name, url in URLS.items()]
    Path("kjzy_symphony_calendar_report.json").write_text(json.dumps({"read_only": True, "sources": results}, indent=2) + "\n", encoding="utf-8")
    for result in results:
        print(result["source"], "| HTTP:", result.get("status", "failed"), "| plugin clues:", len(result.get("event_plugin", [])), "| date clues:", len(result.get("date_clues", [])))
        if "error" in result:
            print(" ERROR:", result["error"])
        for key in ("event_plugin", "date_clues", "embedded_frames"):
            for sample in result.get(key, [])[:3]:
                print(" ", key.upper(), ":", sample)
    print("Read-only. No calendar files modified.")
if __name__ == "__main__":
    main()
