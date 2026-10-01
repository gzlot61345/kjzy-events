# KJZY Sonoma County Events Calendar — draft correction report

Prepared October 1, 2026 (America/Los_Angeles). **Draft only: no commit, GitHub modification, Netlify change, or publication.**

## Baseline and counts

Based on the read-only snapshot of `gzlot61345/kjzy-events`, branch `main`, `SC_Events.html`, blob `593602b35f474ba7aa23e9b5a4217184667398f4`. The repository changed externally during research; this draft preserves the valid links in the latest snapshot. Counts and old URLs below refer to that snapshot.

| Measure | Count |
|---|---:|
| Original displayed event rows | 273 |
| Removed rows | 4 |
| Additional Balletto Thursday rows | 4 |
| Additional Finley occurrence rows | 7 |
| Corrected displayed event rows | **280** |
| Existing rows with content or URL edits | 61 |
| Event links replaced | 59 (unchanged in the Finley revision) |

The displayed count measures listings/occurrences, not distinct event series. Calculation: 273 − 4 + 4 + 7 = 280. No new event series was added. All dates are sorted by year, month, and starting day; same-day events are alphabetized because the calendar does not consistently provide times. Multi-day events are ordered by their first date.

## Final Finley-only correction — October 1, 2026

Rechecked the [official City of Santa Rosa Classes and Events page](https://www.srcity.org/3673/Classes-and-Events), “Friday Afternoon Dances.” The existing October 2, 2026–January 6, 2027 range was removed and replaced with eight individual occurrences through January. The official source URL, event name and Finley Complex location remain unchanged.

| Added occurrence | Official support |
|---|---|
| October 9, 2026 | Explicit makeup for the excluded October 2 date |
| October 16, 2026 | Explicit Halloween dance date |
| November 6, 2026 | First Friday under the published first/third-Friday rule |
| November 20, 2026 | Third Friday under that rule |
| December 11, 2026 | Explicit makeup for the excluded December 4 date |
| December 18, 2026 | Explicit holiday dance date |
| January 8, 2027 | Explicit makeup for the excluded January 1 date |
| January 15, 2027 | Third Friday under the published rule |

The city supplies the recurrence and exceptions; the three regular dates above are calendar calculations from that rule, not individually enumerated dates on the page. Its surrounding seasonal information identifies the 2026–27 season. All eight fall on Fridays. October 2, December 4 and January 1 are excluded. January 6 is not a Friday and has no support as a dance date or series closing date. January 15 is simply the final included January occurrence, not a claimed end to the series. The source gives 1–4 PM for these dances. No better official standalone dance detail page was present in its dance section.

**Count: 273 − 1 unsupported range row + 8 occurrence rows = 280.** No unrelated event, event link, event name or venue was changed. The header count was updated. The unchanged event blocks were checked byte-for-byte, and chronological order and normalized duplicates were checked across all 280 rows. Existing unresolved items unrelated to Finley remain below; this correction does not claim they are resolved. No GitHub or Netlify operations were performed.

## Previous verified draft corrections — October 1, 2026

The preceding revision changed four existing listings only. No events were added or removed. GitHub, Netlify, and the live calendar were not modified. That preceding revision retained 273 rows; the subsequent Finley correction above brings the current total to 280. The existing 55 URL changes remain, with four additional URL replacements (59 cumulative).

| Event | Exact correction / outcome | Current evidence |
|---|---|---|
| Harvest and Stomp — Battaglini Estate Winery | October 11 → **October 10, 2026**; moved into the October 10 group. Generic Sonoma.com calendar → dedicated Taste Route 116 event page. | [Winery](https://battagliniwines.com/) confirms October 10, 2026, 2–5 PM; [direct detail](https://tasteroute116.com/event/annual-grape-stomp-at-battaglini-estate-winery/) agrees. |
| Downtown Trick-or-Treat — Cloverdale | Date retained: **October 30, 2026**. Generic Chamber calendar → dedicated Chamber detail page. | [Chamber detail](https://members.cloverdalechamber.com/chambereventcalendar/Details/downtown-trick-or-treat-1903205?sourceTypeId=Website) explicitly lists Friday, October 30, 2026, 4–6 PM PDT, Downtown Cloverdale. |
| A Chanticleer Christmas — Petaluma | Date retained: **December 14, 2026**. Holiday roundup → official Petaluma event page. Location clarified from “Petaluma” to “St. Vincent de Paul — Petaluma.” | [Official 5 PM performance](https://www.chanticleer.org/202627-concerts/2026/9/13/san-francisco-ksb3m-sstnd-yb6xe-b5nnr). [Official 7:30 PM performance](https://www.chanticleer.org/202627-concerts/2026/9/13/san-francisco-ksb3m-sstnd-yb6xe-b5nnr-zgl6d) also confirmed. Existing one-date row retained; main link opens the 5 PM performance and report records both choices. |
| Reuse & Repair Fair — Windsor | Date retained: **April 18, 2027**. Generic Windsor calendar → Reuse Alliance’s dedicated Windsor Repair Fair page. | [Reuse Alliance](https://www.reusealliance.org/events/windsor-repairfair-2): April 18, 2027, 10 AM–1 PM, Huerta Gymnasium. |
| Earth Day Celebration — Windsor | **Verified and unchanged**, including its current official Town link. | [Town’s 2027 table](https://www.townofwindsor.ca.gov/338/Special-Events) confirms April 18, 2027, 10 AM–1 PM on Market Street. Reuse Alliance independently identifies Earth Day as the concurrent celebration. No separate Earth Day-specific 2027 page was verified; the repair fair page should not replace Earth Day’s own source. |
| Senior Dance at Finley Center | Previously left unresolved; **now resolved using eight occurrences**, as documented above. | [Current city schedule](https://www.srcity.org/3673/Classes-and-Events) supplies first/third-Friday recurrence and named exceptions. |

Earth Day and the Repair Fair are separately named, concurrent activities at different adjacent locations, not duplicate listings. No changes were made to unrelated entries in this revision.

### Four additional link replacements

| Event | Previous URL | Revised URL |
|---|---|---|
| Harvest and Stomp | [https://www.sonoma.com/events/](https://www.sonoma.com/events/) | [https://tasteroute116.com/event/annual-grape-stomp-at-battaglini-estate-winery/](https://tasteroute116.com/event/annual-grape-stomp-at-battaglini-estate-winery/) |
| Downtown Trick-or-Treat | [https://members.cloverdalechamber.com/chambereventcalendar](https://members.cloverdalechamber.com/chambereventcalendar) | [https://members.cloverdalechamber.com/chambereventcalendar/Details/downtown-trick-or-treat-1903205?sourceTypeId=Website](https://members.cloverdalechamber.com/chambereventcalendar/Details/downtown-trick-or-treat-1903205?sourceTypeId=Website) |
| A Chanticleer Christmas | [https://www.visitpetaluma.com/blog/holiday-event-calendar/](https://www.visitpetaluma.com/blog/holiday-event-calendar/) | [https://www.chanticleer.org/202627-concerts/2026/9/13/san-francisco-ksb3m-sstnd-yb6xe-b5nnr](https://www.chanticleer.org/202627-concerts/2026/9/13/san-francisco-ksb3m-sstnd-yb6xe-b5nnr) |
| Reuse & Repair Fair | [https://www.townofwindsor.ca.gov/338/Special-Events](https://www.townofwindsor.ca.gov/338/Special-Events) | [https://www.reusealliance.org/events/windsor-repairfair-2](https://www.reusealliance.org/events/windsor-repairfair-2) |

## Every event removed

| Original row | Event and date | Reason |
|---|---|---|
| 15 | Art Trails Opening – Itinerary Check! — October 2, 2026 | Duplicate of Art Trails Opening — Itinerary Check! on October 2 at Corrick’s; retain the Downtown Santa Rosa event page. Original: [https://happeningsonomacounty.com/event/art-trails-opening-itinerary-check/](https://happeningsonomacounty.com/event/art-trails-opening-itinerary-check/) |
| 118 | Song of Sonoma Autumn Tea — October 18, 2026 | Duplicate of the October 18 Song of Sonoma Autumn Tea at Luther Burbank Art & Garden Center; retain one listing with the organizer’s tea page. Original: [http://www.songofsonoma.org](http://www.songofsonoma.org) |
| 10 | Karaoke at the Speakeasy — October 1, 2026 | October 1, 2026 occurrence not independently verified. Venue calendar shows September only; attempted date-specific Sonoma Valley Events URL redirects to the general calendar. This is not a claim that the event was canceled. Original: [https://sonomaspeakeasy.com/calendar/](https://sonomaspeakeasy.com/calendar/) |
| 66 | Women Veterans of Sonoma County Meetup — October 6–Dec 8, 2026 | Specific October–December 2026 occurrences could not be established. Existing destination is January 7, 2025. EANGUS repeats a first-Tuesday recurrence without confirming these 2026 dates; KJZY points back to the old page. Remove pending current confirmation, not as a confirmed cancellation. Original: [https://veteran.events/event/women-veterans-of-sonoma-county-meetup-a-meetup-for-empowerment-camaraderie/2025-01-07/](https://veteran.events/event/women-veterans-of-sonoma-county-meetup-a-meetup-for-empowerment-camaraderie/2025-01-07/) |

The two Song of Sonoma listings describe the same October 18 Autumn Tea at Luther Burbank Art & Garden Center. One listing remains, titled “Song of Sonoma Autumn Tea,” with the organizer’s tea page.

## Every event modified beyond its link or position

| Event | Previous content | Corrected content | Evidence / reason |
|---|---|---|---|
| 6th Street Playhouse presents Misalliance | date: 2–18 | date: 2–25 | Replace generic or mismatched destination with a verified event-specific page. Official production page gives October 2–25, 2026, rather than October 2–18. [https://6thstreetplayhouse.com/shows/misalliance/](https://6thstreetplayhouse.com/shows/misalliance/) |
| 6th Street Playhouse presents Who's Afraid of Virginia Woolf | month: March; date: 5–21; name: 6th Street Playhouse presents Who's Afraid of Virginia Woolf | month: February; date: 26; name: 6th Street Playhouse presents Who’s Afraid of Virginia Woolf? — Opening performance | Replace generic or mismatched destination with a verified event-specific page. Official production page confirms opening February 26, 2027. Closing date not verified; show opening explicitly rather than retain unsupported March 5–21 range. [https://6thstreetplayhouse.com/shows/whos-afraid-of-virginia-woolf/](https://6thstreetplayhouse.com/shows/whos-afraid-of-virginia-woolf/) |
| Autumn Tea with Song of Sonoma at Luther Burbank | name: Autumn Tea with Song of Sonoma at Luther Burbank; location: Luther Burbank Art & Garden Center — Santa Rosa | name: Song of Sonoma Autumn Tea; location: Luther Burbank Art & Garden Center — Santa Rosa | Replace generic or mismatched destination with a verified event-specific page. Consolidate the duplicate tea listings; organizer confirms the Art & Garden Center venue. [https://www.songofsonoma.org/tea/](https://www.songofsonoma.org/tea/) |
| Bob Edmonson | location: Passaggio Wines — Sonoma | location: Passaggio Wines — Glen Ellen | Replace generic or mismatched destination with a verified event-specific page. Event-detail page gives Passaggio Wines, 14301 Arnold Drive, Glen Ellen. [https://www.sonomavalleyevents.com/10/03/2026/bob-edmonson/](https://www.sonomavalleyevents.com/10/03/2026/bob-edmonson/) |
| Murder Mystery at The Gables Inn | date: 23 | date: 24 | Replace generic or mismatched destination with a verified event-specific page. Organizer and Sonoma County Tourism both give October 24, not October 23. [https://www.sonomacounty.com/events/murder-mystery/](https://www.sonomacounty.com/events/murder-mystery/) |
| Harvest Happy Hour at Balletto | date: 1–29 | Five separate rows: October 1, 8, 15, 22, and 29, 2026. | Replace continuous October 1–29 range with five separate Thursday occurrences: October 1, 8, 15, 22, 29. [https://www.sonomacounty.com/events/harvest-happy-hour-at-balletto/](https://www.sonomacounty.com/events/harvest-happy-hour-at-balletto/) |

## Every link replaced

Each row below identifies the exact old and new destination. Date-specific pages were matched to the listed occurrence; event-series pages were used where their published schedule covers that occurrence. Some replacements are verified local event listings where a usable organizer detail page was unavailable.

| Event / listed date | Old URL | New URL |
|---|---|---|
| Autumn Tea with Song of Sonoma at Luther Burbank — October 18, 2026 | [https://www.sonoma.com/event/autumn-tea-with-song-of-sonoma-at-luther-burbank/](https://www.sonoma.com/event/autumn-tea-with-song-of-sonoma-at-luther-burbank/) | [https://www.songofsonoma.org/tea/](https://www.songofsonoma.org/tea/) |
| Art Nite Healdsburg — October 1, 2026 | [https://www.artnitehealdsburg.com/](https://www.artnitehealdsburg.com/) | [https://stayhealdsburg.com/event/artnite-healdsburg-every-first-thursday/](https://stayhealdsburg.com/event/artnite-healdsburg-every-first-thursday/) |
| Dick Conte Trio — October 1, 2026 | [https://www.sonomavalleyevents.com/](https://www.sonomavalleyevents.com/) | [https://www.sonomavalleyevents.com/10/01/2026/dick-conte-trio/](https://www.sonomavalleyevents.com/10/01/2026/dick-conte-trio/) |
| Don’t Tell Santa Rosa at Vintage Space — October 1, 2026 | [https://happeningsonomacounty.com/comedy-in-sonoma-county/](https://happeningsonomacounty.com/comedy-in-sonoma-county/) | [https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-01/](https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-01/) |
| 2026 BIG BOOK SALE by Friends of the Santa Rosa Libraries — October 2–5, 2026 | [https://sonomalibrary.org/friends](https://sonomalibrary.org/friends) | [https://www.froggy929.com/event/2026-big-book-sale-by-friends-of-the-santa-rosa-libraries/](https://www.froggy929.com/event/2026-big-book-sale-by-friends-of-the-santa-rosa-libraries/) |
| 6th Street Playhouse presents Misalliance — October 2–18, 2026 | [https://6thstreetplayhouse.com/2026-27-season-shows/](https://6thstreetplayhouse.com/2026-27-season-shows/) | [https://6thstreetplayhouse.com/shows/misalliance/](https://6thstreetplayhouse.com/shows/misalliance/) |
| Friday Market Music — October 2, 2026 | [https://www.sonomavalleyevents.com/](https://www.sonomavalleyevents.com/) | [https://www.sonomavalleyevents.com/10/02/2026/friday-market-music/](https://www.sonomavalleyevents.com/10/02/2026/friday-market-music/) |
| Scarlett Letters — October 2, 2026 | [https://www.sonomavalleyevents.com/](https://www.sonomavalleyevents.com/) | [https://www.sonomavalleyevents.com/10/02/2026/scarlett-letters/](https://www.sonomavalleyevents.com/10/02/2026/scarlett-letters/) |
| 2026 Ripp’n River Bash — October 3, 2026 | [https://stayhealdsburg.com/healdsburg-events/](https://stayhealdsburg.com/healdsburg-events/) | [https://stayhealdsburg.com/event/2026-rippn-river-bash/](https://stayhealdsburg.com/event/2026-rippn-river-bash/) |
| Blue Rooster — October 3, 2026 | [https://www.sonomavalleyevents.com/](https://www.sonomavalleyevents.com/) | [https://www.sonomavalleyevents.com/10/03/2026/blue-rooster/](https://www.sonomavalleyevents.com/10/03/2026/blue-rooster/) |
| Bob Edmonson — October 3, 2026 | [https://www.sonomavalleyevents.com/](https://www.sonomavalleyevents.com/) | [https://www.sonomavalleyevents.com/10/03/2026/bob-edmonson/](https://www.sonomavalleyevents.com/10/03/2026/bob-edmonson/) |
| Downtown Sound: Pazifico — October 3, 2026 | [https://www.downtownsantarosa.org/events/calendar](https://www.downtownsantarosa.org/events/calendar) | [https://www.downtownsantarosa.org/do/downtown-sound-pazifico](https://www.downtownsantarosa.org/do/downtown-sound-pazifico) |
| Grape Stomp in the Vineyard — October 3, 2026 | [http://www.thegablesinn.com](http://www.thegablesinn.com) | [https://www.sonomacounty.com/events/4th-annual-grape-stomp-at-the-gables-wine-country-inn/](https://www.sonomacounty.com/events/4th-annual-grape-stomp-at-the-gables-wine-country-inn/) |
| Live Music by Sophia Rayne at Usher Gallery — October 3, 2026 | [https://happeningsonomacounty.com/art-events-in-sonoma-county/](https://happeningsonomacounty.com/art-events-in-sonoma-county/) | [https://happeningsonomacounty.com/event/live-music-by-sophia-rayne-at-usher-gallery/](https://happeningsonomacounty.com/event/live-music-by-sophia-rayne-at-usher-gallery/) |
| OAEC Garden Tour — October 3, 2026 | [https://sebastopolcalendar.com/event/oaec-garden-tour/2026-10-17/](https://sebastopolcalendar.com/event/oaec-garden-tour/2026-10-17/) | [https://sebastopolcalendar.com/event/oaec-garden-tour/2026-10-03/](https://sebastopolcalendar.com/event/oaec-garden-tour/2026-10-03/) |
| Saturday Harvest Market — October 3, 2026 | [https://sonomaecologycenter.org/event/saturday-harvest-markets-at-sonoma-garden-park-7/2026-10-03/](https://sonomaecologycenter.org/event/saturday-harvest-markets-at-sonoma-garden-park-7/2026-10-03/) | [https://www.sonomavalleyevents.com/10/03/2026/saturday-harvest-market/](https://www.sonomavalleyevents.com/10/03/2026/saturday-harvest-market/) |
| Water Bark at Spring Lake Park — October 3–4, 2026 | [https://happeningsonomacounty.com/](https://happeningsonomacounty.com/) | [https://www.sonomacountyparksfoundation.org/water-bark.html](https://www.sonomacountyparksfoundation.org/water-bark.html) |
| Salsa Sundays — October 4, 2026 | [https://www.downtownsantarosa.org/events/calendar](https://www.downtownsantarosa.org/events/calendar) | [https://www.downtownsantarosa.org/do/salsa-sundays-2](https://www.downtownsantarosa.org/do/salsa-sundays-2) |
| Spring Hill Halloween and Fall Market — October 4, 2026 | [https://happeningsonomacounty.com/art-events-in-sonoma-county/](https://happeningsonomacounty.com/art-events-in-sonoma-county/) | [https://happeningsonomacounty.com/event/spring-hill-halloween-and-fall-market/](https://happeningsonomacounty.com/event/spring-hill-halloween-and-fall-market/) |
| Ukrainian BBQ and Beer Fest — October 4, 2026 | [https://www.sebastopolwf.org](https://www.sebastopolwf.org) | [https://business.sebastopol.org/events/details/ukrainian-bbq-and-beer-fest-5052236](https://business.sebastopol.org/events/details/ukrainian-bbq-and-beer-fest-5052236) |
| Hiss Golden Messenger — October 6, 2026 | [https://www.sonoma.com/events/](https://www.sonoma.com/events/) | [https://www.sonomacounty.com/events/live-at-little-saint-hiss-golden-messenger/](https://www.sonomacounty.com/events/live-at-little-saint-hiss-golden-messenger/) |
| Work In Progress — Robert Reich New Movie — October 7, 2026 | [https://www.wakeupsonoma.org/events](https://www.wakeupsonoma.org/events) | [https://www.sonomavalleyevents.com/10/07/2026/wake-up-sonoma-presents-work-in-progress/](https://www.sonomavalleyevents.com/10/07/2026/wake-up-sonoma-presents-work-in-progress/) |
| Don’t Tell Santa Rosa at Vintage Space — October 8, 2026 | [https://happeningsonomacounty.com/comedy-in-sonoma-county/](https://happeningsonomacounty.com/comedy-in-sonoma-county/) | [https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-08/](https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-08/) |
| Celestial Sips: Stargazing in the Vineyard — October 9, 2026 | [https://www.wineroad.com/events/winery-events/](https://www.wineroad.com/events/winery-events/) | [https://stayhealdsburg.com/event/celestial-sips-stargazing-in-the-vineyard/](https://stayhealdsburg.com/event/celestial-sips-stargazing-in-the-vineyard/) |
| Ross Street Sessions: Funky Milagro — October 9, 2026 | [https://www.downtownsantarosa.org/events/calendar](https://www.downtownsantarosa.org/events/calendar) | [https://www.downtownsantarosa.org/do/ross-street-sessions-funky-milagro](https://www.downtownsantarosa.org/do/ross-street-sessions-funky-milagro) |
| Petaluma Pride Festival — October 10, 2026 | [https://petalumapride.org/](https://petalumapride.org/) | [https://www.visitpetaluma.com/event/2026-petaluma-pride-festival/](https://www.visitpetaluma.com/event/2026-petaluma-pride-festival/) |
| Sonoma County Harvest Fair Awards Gala — October 10, 2026 | [https://harvestfair.org/](https://harvestfair.org/) | [https://www.sonomacounty.com/events/sonoma-county-harvest-fair-awards-gala-2/](https://www.sonomacounty.com/events/sonoma-county-harvest-fair-awards-gala-2/) |
| SRJC Shone Farm Fall Festival — October 10, 2026 | [https://shonefarm.santarosa.edu/](https://shonefarm.santarosa.edu/) | [https://shonefarm.santarosa.edu/shone-farm-fall-festival](https://shonefarm.santarosa.edu/shone-farm-fall-festival) |
| Cyrus Chestnut Trio — October 11, 2026 | [https://healdsburgjazz.org/](https://healdsburgjazz.org/) | [https://www.ksro.com/event/cyrus-chestnut-trio/](https://www.ksro.com/event/cyrus-chestnut-trio/) |
| Don’t Tell Santa Rosa at Vintage Space — October 15, 2026 | [https://happeningsonomacounty.com/comedy-in-sonoma-county/](https://happeningsonomacounty.com/comedy-in-sonoma-county/) | [https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-15/](https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-15/) |
| Forbidden Kiss LIVE – Chaos — October 16, 2026 | [https://happeningsonomacounty.com/comedy-in-sonoma-county/](https://happeningsonomacounty.com/comedy-in-sonoma-county/) | [https://happeningsonomacounty.com/event/forbidden-kiss-live-chaos/](https://happeningsonomacounty.com/event/forbidden-kiss-live-chaos/) |
| Ross Street Sessions: School of Rock House Band — October 16, 2026 | [https://www.downtownsantarosa.org/events/calendar](https://www.downtownsantarosa.org/events/calendar) | [https://www.downtownsantarosa.org/do/ross-street-sessions-school-of-rock-house-band-2](https://www.downtownsantarosa.org/do/ross-street-sessions-school-of-rock-house-band-2) |
| Downtown Sound: The Psychedelic Fuzz — October 17, 2026 | [https://www.downtownsantarosa.org/events/calendar](https://www.downtownsantarosa.org/events/calendar) | [https://www.downtownsantarosa.org/do/downtown-sound-the-psychedelic-fuzz](https://www.downtownsantarosa.org/do/downtown-sound-the-psychedelic-fuzz) |
| Fort Ross Harvest Festival — October 17, 2026 | [https://happeningsonomacounty.com/fall-festivals-in-sonoma-county/](https://happeningsonomacounty.com/fall-festivals-in-sonoma-county/) | [https://www.fortross.org/events/2026/harvest](https://www.fortross.org/events/2026/harvest) |
| LumaFest & Día de los Muertos Celebration — October 17, 2026 | [https://www.visitpetaluma.com/fairs-and-festivals/](https://www.visitpetaluma.com/fairs-and-festivals/) | [https://www.visitpetaluma.com/event/lumafest-petalumas-educational-fair-and-el-dia-de-los-muertos-celebration/](https://www.visitpetaluma.com/event/lumafest-petalumas-educational-fair-and-el-dia-de-los-muertos-celebration/) |
| OAEC Garden Tour — October 17, 2026 | [https://sebastopolcalendar.com/](https://sebastopolcalendar.com/) | [https://sebastopolcalendar.com/event/oaec-garden-tour/2026-10-17/](https://sebastopolcalendar.com/event/oaec-garden-tour/2026-10-17/) |
| Don’t Tell Santa Rosa at Vintage Space — October 22, 2026 | [https://happeningsonomacounty.com/comedy-in-sonoma-county/](https://happeningsonomacounty.com/comedy-in-sonoma-county/) | [https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-22/](https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-22/) |
| Murder Mystery at The Gables Inn — October 23, 2026 | [https://www.thegablesinn.com](https://www.thegablesinn.com) | [https://www.sonomacounty.com/events/murder-mystery/](https://www.sonomacounty.com/events/murder-mystery/) |
| Ross Street Sessions: MCHS Mariachi — October 23, 2026 | [https://www.downtownsantarosa.org/events/calendar](https://www.downtownsantarosa.org/events/calendar) | [https://www.downtownsantarosa.org/do/ross-street-sessions-mchs-mariachi](https://www.downtownsantarosa.org/do/ross-street-sessions-mchs-mariachi) |
| Don’t Tell Santa Rosa at Vintage Space — October 29, 2026 | [https://happeningsonomacounty.com/comedy-in-sonoma-county/](https://happeningsonomacounty.com/comedy-in-sonoma-county/) | [https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-29/](https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-10-29/) |
| Slay O'Ween — October 29, 2026 | [https://www.wakeupsonoma.org/events](https://www.wakeupsonoma.org/events) | [https://www.sonomavalleyevents.com/10/29/2026/wake-up-sonoma-presents-slay-o-ween/](https://www.sonomavalleyevents.com/10/29/2026/wake-up-sonoma-presents-slay-o-ween/) |
| Ross Street Sessions: 945 — October 30, 2026 | [https://www.downtownsantarosa.org/events/calendar](https://www.downtownsantarosa.org/events/calendar) | [https://www.downtownsantarosa.org/do/ross-street-sessions-945](https://www.downtownsantarosa.org/do/ross-street-sessions-945) |
| Halloween Trick or Treat Trail — October 31, 2026 | [https://www.visitpetaluma.com/find-events/](https://www.visitpetaluma.com/find-events/) | [https://www.visitpetaluma.com/event/trick-or-treat-trail/](https://www.visitpetaluma.com/event/trick-or-treat-trail/) |
| Art Nite Healdsburg — November 5, 2026 | [https://www.artnitehealdsburg.com/](https://www.artnitehealdsburg.com/) | [https://stayhealdsburg.com/event/artnite-healdsburg-every-first-thursday/](https://stayhealdsburg.com/event/artnite-healdsburg-every-first-thursday/) |
| Don’t Tell Santa Rosa at Vintage Space — November 5, 2026 | [https://happeningsonomacounty.com/comedy-in-sonoma-county/](https://happeningsonomacounty.com/comedy-in-sonoma-county/) | [https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-11-05/](https://happeningsonomacounty.com/event/dont-tell-santa-rosa-at-vintage-space-7/2026-11-05/) |
| 6th Street Playhouse presents Meet Me In St. Louis — November 20–Dec 20, 2026 | [https://6thstreetplayhouse.com/2026-27-season-shows/](https://6thstreetplayhouse.com/2026-27-season-shows/) | [https://6thstreetplayhouse.com/shows/meet-me-in-st-louis/](https://6thstreetplayhouse.com/shows/meet-me-in-st-louis/) |
| Santa's Riverboat Arrival — November 28, 2026 | [https://www.visitpetaluma.com/fairs-and-festivals/](https://www.visitpetaluma.com/fairs-and-festivals/) | [https://www.visitpetaluma.com/event/santas-riverboat-arrival/](https://www.visitpetaluma.com/event/santas-riverboat-arrival/) |
| Downtown Holiday Shopping Stroll — December 5, 2026 | [https://www.visitpetaluma.com/blog/holiday-event-calendar/](https://www.visitpetaluma.com/blog/holiday-event-calendar/) | [https://www.visitpetaluma.com/event/downtown-holiday-open-house-marketplace/](https://www.visitpetaluma.com/event/downtown-holiday-open-house-marketplace/) |
| 6th Street Playhouse presents A Night With Janis Joplin — January 15–31, 2027 | [https://6thstreetplayhouse.com/2026-27-season-shows/](https://6thstreetplayhouse.com/2026-27-season-shows/) | [https://6thstreetplayhouse.com/shows/a-night-with-janis-joplin/](https://6thstreetplayhouse.com/shows/a-night-with-janis-joplin/) |
| HYPROV with Colin Mochrie — February 10, 2027 | [https://www.sonomacounty.com/events/hyprov-with-colin-mochrie/](https://www.sonomacounty.com/events/hyprov-with-colin-mochrie/) | [https://lutherburbankcenter.org/event/hyprov-colin-mochrie/](https://lutherburbankcenter.org/event/hyprov-colin-mochrie/) |
| Smokey Robinson — February 13, 2027 | [https://www.sonomacounty.com/events/smokey-robinson-legacy-of-love-tour/](https://www.sonomacounty.com/events/smokey-robinson-legacy-of-love-tour/) | [https://lutherburbankcenter.org/event/smokey-robinson27/](https://lutherburbankcenter.org/event/smokey-robinson27/) |
| 6th Street Playhouse presents Who's Afraid of Virginia Woolf — March 5–21, 2027 | [https://6thstreetplayhouse.com/2026-27-season-shows/](https://6thstreetplayhouse.com/2026-27-season-shows/) | [https://6thstreetplayhouse.com/shows/whos-afraid-of-virginia-woolf/](https://6thstreetplayhouse.com/shows/whos-afraid-of-virginia-woolf/) |
| Symphony Pops: The Music of Billy Joel Starring Michael Cavanaugh — April 4, 2027 | [https://lutherburbankcenter.org/tickets/symphony-pops-26/](https://lutherburbankcenter.org/tickets/symphony-pops-26/) | [https://www.srsymphony.org/event/the-music-of-billy-joel-starring-michael-cavanaugh/](https://www.srsymphony.org/event/the-music-of-billy-joel-starring-michael-cavanaugh/) |
| 6th Street Playhouse presents Seagull — May 7–23, 2027 | [https://6thstreetplayhouse.com/2026-27-season-shows/](https://6thstreetplayhouse.com/2026-27-season-shows/) | [https://6thstreetplayhouse.com/shows/seagull/](https://6thstreetplayhouse.com/shows/seagull/) |
| 6th Street Playhouse presents The Pajama Game — May 28–Jun 26, 2027 | [https://6thstreetplayhouse.com/2026-27-season-shows/](https://6thstreetplayhouse.com/2026-27-season-shows/) | [https://6thstreetplayhouse.com/shows/the-pajama-game/](https://6thstreetplayhouse.com/shows/the-pajama-game/) |

The October 3 OAEC tour previously pointed to October 17 in the latest snapshot; both tours now have their matching occurrence pages. Saturday Harvest Market’s newly supplied organizer URL returned 404, so the draft uses its verified October 3 event listing. HYPROV and Smokey Robinson now point directly to Luther Burbank Center event pages.

## Unresolved verification and intentionally retained items

Karaoke and Women Veterans were removed pending verification as requested; inability to verify is not evidence of cancellation. Other unresolved items remain unchanged and are listed here for review. This is not a certification of every date in the calendar.

| Event / listed date | What remains unresolved |
|---|---|
| Harvest Open House — October 3, 2026 | No verified standalone detail page found to replace the generic calendar. Existing source: [https://www.sonoma.com/events/](https://www.sonoma.com/events/) |
| Pumpkin Day at Oak Hill Farm — October 3, 2026 | No verified stable standalone detail page found; retain the existing roundup. Existing source: [https://happeningsonomacounty.com/fall-festivals-in-sonoma-county/](https://happeningsonomacounty.com/fall-festivals-in-sonoma-county/) |
| Live Band Karaoke — October 15–Nov 19, 2026 | Exact recurrence dates within October 15–November 19 not independently confirmed; homepage retained. Existing source: [https://barrelprooflounge.com/](https://barrelprooflounge.com/) |
| Green Halloween Party — October 16, 2026 | No verified event-detail page for this occurrence found; general Windsor page retained. Existing source: [https://www.townofwindsor.ca.gov/338/Special-Events](https://www.townofwindsor.ca.gov/338/Special-Events) |
| Día de los Muertos — October 31, 2026 | No verified event-detail page for this occurrence found; general Windsor page retained. Existing source: [https://www.townofwindsor.ca.gov/338/Special-Events](https://www.townofwindsor.ca.gov/338/Special-Events) |
| Healdsburg Farmers’ Market Pumpkin Festival and Costume Competition — October 31, 2026 | Organizer visitor information supports October 31, 2026, but no standalone event page found. Existing source: [https://healdsburgfarmersmarket.org/](https://healdsburgfarmersmarket.org/) |
| Veterans Day Ceremony — November 11, 2026 | No verified direct detail page found; general Windsor page retained. Existing source: [https://www.townofwindsor.ca.gov/338/Special-Events](https://www.townofwindsor.ca.gov/338/Special-Events) |
| Wine Country Women's Festival — November 14, 2026 | No verified direct detail page found; general Windsor page retained. Existing source: [https://www.townofwindsor.ca.gov/338/Special-Events](https://www.townofwindsor.ca.gov/338/Special-Events) |
| Winter Wine Walk — November 19, 2026 | No verified direct detail page found; general Windsor page retained. Existing source: [https://www.townofwindsor.ca.gov/338/Special-Events](https://www.townofwindsor.ca.gov/338/Special-Events) |
| Petaluma City of Lights Driving Tour — December 1–31, 2026 | The available standalone driving-tour page is for December 2025–January 2026, so it was rejected as a replacement for December 2026. Current occurrence still needs confirmation. Existing source: [https://www.visitpetaluma.com/blog/holiday-event-calendar/](https://www.visitpetaluma.com/blog/holiday-event-calendar/) |
| Windsor Holiday Celebration — December 3, 2026 | Date is confirmed in the official 2026 Town table. The separate holiday-detail page remains a 2025 edition, so the current official calendar link is retained. [Town source](https://www.townofwindsor.ca.gov/338/Special-Events) |
| Christmas Craft Fair — December 5, 2026 | The Sonoma.com detail result describes December 6, 2025. A matching 2026 organizer page was not verified. Existing source: [https://www.sonoma.com/events/](https://www.sonoma.com/events/) |
| Light Up the Square — December 12, 2026 | The holiday roundup calls December 12, 2026 a Friday, although it is Saturday. The intended date needs organizer confirmation. Existing source: [https://www.visitpetaluma.com/blog/holiday-event-calendar/](https://www.visitpetaluma.com/blog/holiday-event-calendar/) |
| Healdsburg Jazz Winterfest — January 28–31, 2027 | Organizer homepage confirms January 28–31, 2027; a separate detail page was not found. Existing source: [https://healdsburgjazz.org/](https://healdsburgjazz.org/) |
| 30th Sonoma International Film Festival — March 16–21, 2027 | A more specific event-detail replacement was not verified; the existing festival trip page remains. Existing source: [https://sonomafilmfest.org/festival/plan-your-trip](https://sonomafilmfest.org/festival/plan-your-trip) |
| Healdsburg Jazz Summerfest — June 11–20, 2027 | Organizer homepage confirms June 11–20, 2027; a separate detail page was not found. Existing source: [https://healdsburgjazz.org/](https://healdsburgjazz.org/) |

For Who’s Afraid of Virginia Woolf?, February 26, 2027 is the confirmed opening; a closing date was not verified, so the draft explicitly lists the opening performance only. The official Janis Joplin page’s cast schedule supports January 15–31, 2027. Closing dates for Meet Me in St. Louis, Seagull, and The Pajama Game remain unverified; existing ranges remain.

Access-denied or temporary server responses were not treated as proof that an event was invalid. Links were not replaced with stale prior-year pages merely because those pages loaded. Unedited listings in the inventory below are preserved, not newly certified.

## Preservation and checks

The document prefix is unchanged except for the required count update to 280; KJZY styling, favicon, search controls, and the entire source-section/footer/script tail remain unchanged. The search JavaScript is unchanged. Structural checks confirm 280 rows, ascending dates, the five Balletto dates, one Art Trails listing, one Song of Sonoma listing, and no exact date/name duplicates. JavaScript syntax was checked. Search behavior passed DOM-based checks for the Search button, Enter key, venue matching, no-results message, empty month/year hiding, Clear, and clearing the input. The test emulated innerText with textContent; visual browser rendering was not tested. The Finley revision preserves all 272 non-Finley event blocks byte-for-byte; only the Finley range was expanded and the header count updated. No listed event starts before October 1, 2026 (America/Los_Angeles); this checks displayed dates, not independently certified dates for every untouched listing. No exact normalized duplicates were found. The two concurrent Windsor events are distinct. Publication review is appropriate, but the other flagged dates should be settled before going live; Finley has been resolved as described above.

## Complete corrected order and modification inventory

Original row numbers are one-based positions in the baseline. “Retained” means no content or URL edit; position may have changed. The four additional Balletto occurrences share original row 9.

| Corrected row | Original row | Date | Event | Changes |
|---|---:|---|---|---|
| 1 | 3 | October 1, 2026 | Art Nite Healdsburg | url |
| 2 | 4 | October 1, 2026 | Chris Jorgensen Gallery Evening & Birthday Celebration with Sons of Norway | Retained |
| 3 | 5 | October 1, 2026 | Dick Conte Trio | url |
| 4 | 6 | October 1, 2026 | Don’t Tell Santa Rosa at Vintage Space | url |
| 5 | 7 | October 1, 2026 | First Thursdays Art Walk Sonoma | Retained |
| 6 | 8 | October 1–29, 2026 | Happy Hour Russian River Vineyards Style | Retained |
| 7 | 9 | October 1, 2026 | Harvest Happy Hour at Balletto | Separate Thursday occurrence |
| 8 | 11 | October 1, 2026 | Maple Magic & Winter Wonder | Retained |
| 9 | 12 | October 1, 2026 | Wanderlust Food Truck Festival | Retained |
| 10 | 13 | October 2–5, 2026 | 2026 BIG BOOK SALE by Friends of the Santa Rosa Libraries | url |
| 11 | 14 | October 2–25, 2026 | 6th Street Playhouse presents Misalliance | url, date |
| 12 | 1 | October 2, 2026 | Art Trails Opening - Itinerary Check! | Retained |
| 13 | 16 | October 2, 2026 | Best of San Francisco Stand-Up Comedy 2026 | Retained |
| 14 | 17 | October 2, 2026 | Fiber, Paintings and Prints Gallery Opening Reception | Retained |
| 15 | 18 | October 2, 2026 | First Friday Art Walk at SOFA Art Galleries | Retained |
| 16 | 19 | October 2, 2026 | First Fridays at Chimera Arts | Retained |
| 17 | 20 | October 2, 2026 | Friday Market Music | url |
| 18 | 21 | October 2–4, 2026 | Grand Bazaar of Petaluma | Retained |
| 19 | 22 | October 2, 2026 | Hal Sparks! Friday Night Comedy | Retained |
| 20 | 23 | October 2, 2026 | Holly Near and Friends | Retained |
| 21 | 24 | October 2, 2026 | Irish Sessions — Participate or Listen | Retained |
| 22 | 25 | October 2, 2026 | Lucía | Retained |
| 23 | 26 | October 2, 2026 | Ross Street Sessions: Michael Capella Band | Retained |
| 24 | 27 | October 2, 2026 | Scarlett Letters | url |
| 25 | 29 | October 2, 2026 | The Beatles Reimagined featuring Jazz Mafia & Otis McDonald | Retained |
| 26 | 30 | October 2, 2026 | Ultimate Heirloom Apple Tasting & Orchard Experience | Retained |
| 27 | 31 | October 2, 2026 | Wine Blending Workshop | Retained |
| 28 | 32 | October 3–4, 2026 | 1TRIBE: Reggae • Dancehall • Afrobeats • Amapiano with Konnex & Kobie | Retained |
| 29 | 33 | October 3, 2026 | 2026 Ripp’n River Bash | url |
| 30 | 34 | October 3, 2026 | Blue Rooster | url |
| 31 | 35 | October 3, 2026 | Bob Edmonson | url, location |
| 32 | 36 | October 3–11, 2026 | Brewsters Annual Oktoberfest | Retained |
| 33 | 37 | October 3, 2026 | Color Lab with Lena Wolff | Retained |
| 34 | 38 | October 3, 2026 | Comedy Night at the Cloverdale Citrus Fair | Retained |
| 35 | 39 | October 3, 2026 | Downtown Sound: Pazifico | url |
| 36 | 40 | October 3, 2026 | Dry Creek Station | Retained |
| 37 | 41 | October 3, 2026 | Grape Stomp in the Vineyard | url |
| 38 | 42 | October 3, 2026 | Harvest Open House | Retained |
| 39 | 43 | October 3, 2026 | Live Music by Sophia Rayne at Usher Gallery | url |
| 40 | 44 | October 3, 2026 | Many Moons Festival | Retained |
| 41 | 45 | October 3, 2026 | OAEC Garden Tour | url |
| 42 | 46 | October 3, 2026 | Pumpkin Day at Oak Hill Farm | Retained |
| 43 | 47 | October 3, 2026 | Saturday Harvest Market | url |
| 44 | 48 | October 3–Dec 19, 2026 | Saturday Live Music at Spicy Vines | Retained |
| 45 | 49 | October 3, 2026 | SCRIBE at Shady Oak Barrel House | Retained |
| 46 | 50 | October 3–4, 2026 | Sonoma Con 2026 | Retained |
| 47 | 51 | October 3–4, 2026 | Water Bark at Spring Lake Park | url |
| 48 | 52 | October 4, 2026 | Anaba Harvest Party | Retained |
| 49 | 53 | October 4, 2026 | Blessing of the Animals | Retained |
| 50 | 54 | October 4, 2026 | Cindy's Race | Retained |
| 51 | 55 | October 4, 2026 | Festival Calentano | Retained |
| 52 | 56 | October 4–31, 2026 | Pumpkin Patch & Fall Festival | Retained |
| 53 | 57 | October 4, 2026 | Salsa Sundays | url |
| 54 | 58 | October 4, 2026 | Sip & Paint @ Paradise Ridge | Retained |
| 55 | 59 | October 4, 2026 | Spring Hill Halloween and Fall Market | url |
| 56 | 60 | October 4, 2026 | The SoCo Market Presents Ross Street Markets | Retained |
| 57 | 61 | October 4, 2026 | Ukrainian BBQ and Beer Fest | url |
| 58 | 62 | October 4, 2026 | We Are One — Artist Talk with Bryan Keith Thomas | Retained |
| 59 | 63 | October 5, 2026 | In Conversation with Van Jones | Retained |
| 60 | 64 | October 6, 2026 | Hiss Golden Messenger | url |
| 61 | 65 | October 6–Dec 31, 2026 | Open Door Mobile Services Program | Retained |
| 62 | 67 | October 7, 2026 | Summer Film Series at The Madrona | Retained |
| 63 | 68 | October 7, 2026 | Work In Progress — Robert Reich New Movie | url |
| 64 | 69 | October 8, 2026 | Brazilian Cooking Class Benefiting Sonoma Family Meal | Retained |
| 65 | 70 | October 8, 2026 | Don’t Tell Santa Rosa at Vintage Space | url |
| 66 | 9 | October 8, 2026 | Harvest Happy Hour at Balletto | Separate Thursday occurrence |
| 67 | 71 | October 8, 2026 | The Lily Tomlin Tour 2026 | Retained |
| 68 | 72 | October 8, 2026 | Wanderlust Food Truck Festival | Retained |
| 69 | 73 | October 9, 2026 | 2026 Santa Rosa Municipal Community Information Meeting | Retained |
| 70 | 74 | October 9, 2026 | Celestial Sips: Stargazing in the Vineyard | url |
| 71 | 75 | October 9, 2026 | P.U.R.R. Presents: A Punk Clown Takeover | Retained |
| 72 | 76 | October 9, 2026 | Ross Street Sessions: Funky Milagro | url |
| 73 | 28 | October 9, 2026 | Senior Dance at Finley Center | Separate verified Friday occurrence (Finley revision) |
| 74 | 77 | October 9, 2026 | Sunset Trivia Night | Retained |
| 75 | 78 | October 10–11, 2026 | 5th Annual Sonoma County Americana Music Festival | Retained |
| 76 | 79 | October 10–18, 2026 | ART TRAILS 2026 at the Art & Music Gallery in Petaluma | Retained |
| 77 | 80 | October 10, 2026 | Funky Florals — Cut Paper Collage Workshop with Sally-Ann Langley | Retained |
| 78 | 81 | October 10, 2026 | Golden Harvest Senior Resource & Wellness Faire 2026 | Retained |
| 79 | 94 | October 10, 2026 | Harvest and Stomp | date, url (this revision) |
| 80 | 82 | October 10, 2026 | Headline Comedy — Joey Bragg | Retained |
| 81 | 83 | October 10, 2026 | John Prine Birthday Celebration | Retained |
| 82 | 84 | October 10, 2026 | Museum of Sonoma County’s Block Party | Retained |
| 83 | 85 | October 10, 2026 | Petaluma Pride Festival | url |
| 84 | 86 | October 10, 2026 | See Art in Action at T Barny’s Sculpture Studio | Retained |
| 85 | 87 | October 10, 2026 | Sonoma County Harvest Fair Awards Gala | url |
| 86 | 88 | October 10, 2026 | SRJC Shone Farm Fall Festival | url |
| 87 | 89 | October 10, 2026 | Turn of the Century — High Energy Party Rock | Retained |
| 88 | 90 | October 10–12, 2026 | Twist of Fate — Santa Rosa Symphony | Retained |
| 89 | 91 | October 11, 2026 | 8th Annual Harvest Party | Retained |
| 90 | 92 | October 11, 2026 | Cyrus Chestnut Trio | url |
| 91 | 93 | October 11, 2026 | Fall Harvest Festival | Retained |
| 92 | 95 | October 11, 2026 | Lasseter Lounge | Retained |
| 93 | 96 | October 15, 2026 | An Evening with the Rush Tribute Project | Retained |
| 94 | 97 | October 15, 2026 | Don’t Tell Santa Rosa at Vintage Space | url |
| 95 | 9 | October 15, 2026 | Harvest Happy Hour at Balletto | Separate Thursday occurrence |
| 96 | 98 | October 15–Nov 19, 2026 | Live Band Karaoke | Retained |
| 97 | 99 | October 15, 2026 | Multi-Chamber Mixer — October | Retained |
| 98 | 100 | October 15–Nov 19, 2026 | Sonoma County Sketchbook Club | Retained |
| 99 | 101 | October 16, 2026 | Forbidden Kiss LIVE – Chaos | url |
| 100 | 102 | October 16, 2026 | Froggy’s 30th Birthday Featuring Corey Kent with Max Vogel | Retained |
| 101 | 103 | October 16, 2026 | Green Halloween Party | Retained |
| 102 | 104 | October 16, 2026 | Raiatea Helm — A Legacy of Hawaiian Song & String | Retained |
| 103 | 105 | October 16, 2026 | Ross Street Sessions: School of Rock House Band | url |
| 104 | 28 | October 16, 2026 | Senior Dance at Finley Center | Separate verified Friday occurrence (Finley revision) |
| 105 | 106 | October 17, 2026 | Downtown Sound: The Psychedelic Fuzz | url |
| 106 | 107 | October 17, 2026 | Dust to Dust — Artist Talk with Katie Murken | Retained |
| 107 | 108 | October 17, 2026 | Floating Pumpkin Patch | Retained |
| 108 | 109 | October 17, 2026 | Fort Ross Harvest Festival | url |
| 109 | 110 | October 17, 2026 | LumaFest & Día de los Muertos Celebration | url |
| 110 | 111 | October 17, 2026 | Mistah F.A.B. & Philthy Rich — Motion Detected Tour | Retained |
| 111 | 112 | October 17, 2026 | OAEC Garden Tour | url |
| 112 | 113 | October 17, 2026 | Petaluma Gap Wind to Wine Festival | Retained |
| 113 | 114 | October 17, 2026 | Tequila Teaser | Retained |
| 114 | 115 | October 18, 2026 | 2026 Norbay Theater Awards | Retained |
| 115 | 116 | October 18, 2026 | Ingrid Michaelson featuring Allie Moss & Hannah Winkler | Retained |
| 116 | 117 | October 18, 2026 | Reuse in Art, Reuse in Life — Ali Gass & Phoebe Schenker | Retained |
| 117 | 2 | October 18, 2026 | Song of Sonoma Autumn Tea | url, name, location |
| 118 | 119 | October 18, 2026 | Symphony Pops: A Tribute to John Williams, The Movie Maestro | Retained |
| 119 | 120 | October 22, 2026 | Don’t Tell Santa Rosa at Vintage Space | url |
| 120 | 9 | October 22, 2026 | Harvest Happy Hour at Balletto | Separate Thursday occurrence |
| 121 | 121 | October 23, 2026 | AREA 54 The Alien Disco: Mos Eisely Cantina Edition | Retained |
| 122 | 122 | October 23–Dec 4, 2026 | Garden Table Dinner Series | Retained |
| 123 | 124 | October 23, 2026 | Ross Street Sessions: MCHS Mariachi | url |
| 124 | 125 | October 24, 2026 | Cider Circus | Retained |
| 125 | 126 | October 24, 2026 | Downtown Sound: LaiddBackZach & the .Wav | Retained |
| 126 | 127 | October 24, 2026 | Halloween at Howarth | Retained |
| 127 | 128 | October 24, 2026 | KSRO Presents Jimmy Failla | Retained |
| 128 | 129 | October 24, 2026 | Lobster Bash | Retained |
| 129 | 123 | October 24, 2026 | Murder Mystery at The Gables Inn | url, date |
| 130 | 130 | October 24, 2026 | Sonoma Family Meal's Knife's Edge Chef Showdown and Tasting | Retained |
| 131 | 131 | October 24, 2026 | Sonoma Guitar Series: Gaëlle Solal | Retained |
| 132 | 132 | October 24, 2026 | Trick or Treat Trail | Retained |
| 133 | 133 | October 25, 2026 | Boo! Let’s Dance | Retained |
| 134 | 134 | October 25, 2026 | Clover Sonoma Family Fun Series: 360 Allstars | Retained |
| 135 | 135 | October 25, 2026 | Día de Muertos | Retained |
| 136 | 136 | October 25, 2026 | Geyserville Fall Colors Festival & Vintage Car Show | Retained |
| 137 | 137 | October 26, 2026 | Pro Jam — Special Guest Mark Hummel | Retained |
| 138 | 138 | October 29, 2026 | Don’t Tell Santa Rosa at Vintage Space | url |
| 139 | 9 | October 29, 2026 | Harvest Happy Hour at Balletto | Separate Thursday occurrence |
| 140 | 139 | October 29, 2026 | Lyle Lovett and his Small Large Band | Retained |
| 141 | 140 | October 29, 2026 | Slay O'Ween | url |
| 142 | 141 | October 30, 2026 | Downtown Trick-or-Treat | url (this revision) |
| 143 | 142 | October 30, 2026 | Ross Street Sessions: 945 | url |
| 144 | 143 | October 31, 2026 | Día de los Muertos | Retained |
| 145 | 144 | October 31, 2026 | Halloween Trick or Treat Trail | url |
| 146 | 145 | October 31, 2026 | Healdsburg Farmers’ Market Pumpkin Festival and Costume Competition | Retained |
| 147 | 146 | October 31, 2026 | The Halloween Bar Crawl — Santa Rosa | Retained |
| 148 | 147 | November 5, 2026 | Art Nite Healdsburg | url |
| 149 | 148 | November 5, 2026 | Don’t Tell Santa Rosa at Vintage Space | url |
| 150 | 149 | November 5, 2026 | La Santa Cecilia | Retained |
| 151 | 28 | November 6, 2026 | Senior Dance at Finley Center | Separate verified Friday occurrence (Finley revision) |
| 152 | 150 | November 7, 2026 | Leonid & Friends 2026 Tour | Retained |
| 153 | 151 | November 7–8, 2026 | Wine & Food Affair | Retained |
| 154 | 152 | November 8, 2026 | What You Won’t Do For Love — Why Not Theatre | Retained |
| 155 | 153 | November 9, 2026 | In Conversation with Scott Pelley | Retained |
| 156 | 154 | November 10, 2026 | Pearls Jubilee with Stephan Pastis | Retained |
| 157 | 155 | November 11, 2026 | Petaluma Veterans Day Parade | Retained |
| 158 | 156 | November 11, 2026 | Veterans Day Ceremony | Retained |
| 159 | 157 | November 13, 2026 | Healthcare Forum 2026 + Resource Fair | Retained |
| 160 | 158 | November 14–16, 2026 | Echoes of Innocence — Santa Rosa Symphony | Retained |
| 161 | 159 | November 14, 2026 | Jerry Seinfeld — 5 PM & 8 PM | Retained |
| 162 | 160 | November 14, 2026 | Santa Rosa Growlers vs. Oakland Skates | Retained |
| 163 | 161 | November 14–15, 2026 | Sonoma Bach: Harvest Time — A Seal Upon Our Hearts | Retained |
| 164 | 162 | November 14, 2026 | Wine Country Women's Festival | Retained |
| 165 | 163 | November 14, 2026 | Write & Collage: Words, Images & Memory | Retained |
| 166 | 164 | November 19, 2026 | Anthony Jeselnik: Wrath of Man | Retained |
| 167 | 165 | November 19, 2026 | Juilliard String Quartet with Simone Dinnerstein | Retained |
| 168 | 166 | November 19, 2026 | Winter Wine Walk | Retained |
| 169 | 167 | November 20–Dec 20, 2026 | 6th Street Playhouse presents Meet Me In St. Louis | url |
| 170 | 168 | November 20, 2026 | Santa Rosa Growlers vs. Chicago Misfits | Retained |
| 171 | 28 | November 20, 2026 | Senior Dance at Finley Center | Separate verified Friday occurrence (Finley revision) |
| 172 | 169 | November 21, 2026 | Bored Teachers | Retained |
| 173 | 170 | November 21, 2026 | Santa Rosa Growlers vs. Chicago Misfits | Retained |
| 174 | 171 | November 24, 2026 | Sesame Street Live — Elmo’s Got the Moves | Retained |
| 175 | 172 | November 27, 2026 | Winter Lights Tree Lighting Celebration | Retained |
| 176 | 173 | November 28, 2026 | Santa's Riverboat Arrival | url |
| 177 | 174 | November 28, 2026 | Tower of Power | Retained |
| 178 | 175 | November 29, 2026 | Emporium Presents Brad Williams: The Tall Tales Tour | Retained |
| 179 | 176 | December 1–31, 2026 | Petaluma City of Lights Driving Tour | Retained |
| 180 | 177 | December 3, 2026 | A Celtic Christmas by A Taste of Ireland | Retained |
| 181 | 178 | December 3–Jan 1, 2026 | Charlie Brown Christmas Tree Grove | Retained |
| 182 | 179 | December 3, 2026 | Windsor Holiday Celebration | Retained |
| 183 | 180 | December 4, 2026 | Cherish the Ladies — A Celtic Christmas | Retained |
| 184 | 181 | December 4, 2026 | Merry Healdsburg Tree Lighting Celebration | Retained |
| 185 | 182 | December 4, 2026 | Santa Rosa Growlers vs. Dallas Scorpions | Retained |
| 186 | 183 | December 5, 2026 | Christmas Craft Fair | Retained |
| 187 | 184 | December 5, 2026 | Downtown Holiday Shopping Stroll | url |
| 188 | 185 | December 5, 2026 | Santa Rosa Growlers vs. Dallas Scorpions | Retained |
| 189 | 186 | December 6, 2026 | Symphony Pops: Home for the Holidays | Retained |
| 190 | 187 | December 7, 2026 | In Conversation with Evan Thomas | Retained |
| 191 | 188 | December 8, 2026 | Pink Martini All-Stars present A Season of Stars | Retained |
| 192 | 189 | December 10, 2026 | Mark West Area Chamber of Commerce Monthly Social | Retained |
| 193 | 190 | December 11, 2026 | 20th Annual Posada Navideña | Retained |
| 194 | 28 | December 11, 2026 | Senior Dance at Finley Center | Separate verified Friday occurrence (Finley revision) |
| 195 | 191 | December 12–13, 2026 | Broadway Holiday | Retained |
| 196 | 192 | December 12, 2026 | Light Up the Square | Retained |
| 197 | 193 | December 12–13, 2026 | Winterlude…Handel’s Messiah — Santa Rosa Symphony | Retained |
| 198 | 194 | December 13, 2026 | A Drag Queen Christmas | Retained |
| 199 | 195 | December 14, 2026 | A Chanticleer Christmas | url, location (this revision) |
| 200 | 196 | December 16–20, 2026 | Broadway Holiday | Retained |
| 201 | 197 | December 17, 2026 | Nutcracker! Magical Christmas Ballet | Retained |
| 202 | 198 | December 17, 2026 | Voctave — It Feels Like Christmas | Retained |
| 203 | 199 | December 18, 2026 | A Magical Cirque Christmas | Retained |
| 204 | 28 | December 18, 2026 | Senior Dance at Finley Center | Separate verified Friday occurrence (Finley revision) |
| 205 | 200 | December 19–20, 2026 | Sonoma Bach: Early Music Christmas — On Yoolis Night | Retained |
| 206 | 201 | December 20, 2026 | San Francisco Gay Men’s Chorus — Holiday Spectacular | Retained |
| 207 | 202 | December 23, 2026 | Dave Koz and Friends Christmas Tour 2026 | Retained |
| 208 | 28 | January 8, 2027 | Senior Dance at Finley Center | Separate verified Friday occurrence (Finley revision) |
| 209 | 203 | January 9, 2027 | Psychic Medium John Edward | Retained |
| 210 | 204 | January 9–11, 2027 | Santa Rosa Symphony: Beethoven & Dvořák | Retained |
| 211 | 205 | January 15–31, 2027 | 6th Street Playhouse presents A Night With Janis Joplin | url |
| 212 | 206 | January 15, 2027 | Santa Rosa Growlers vs. Kenosha Knights | Retained |
| 213 | 28 | January 15, 2027 | Senior Dance at Finley Center | Separate verified Friday occurrence (Finley revision) |
| 214 | 207 | January 16, 2027 | Beth Hart with Special Guest Rome | Retained |
| 215 | 208 | January 16, 2027 | Santa Rosa Growlers vs. Kenosha Knights | Retained |
| 216 | 209 | January 16, 2027 | Sonoma Bach: Organ Recital — Reflections of Light | Retained |
| 217 | 210 | January 16–17, 2027 | Winter WINEland | Retained |
| 218 | 211 | January 24, 2027 | Clover Sonoma Family Fun Series: The Cat in the Hat — Live on Stage | Retained |
| 219 | 212 | January 24, 2027 | Santa Rosa Symphony: Back to Beethoven | Retained |
| 220 | 213 | January 28–31, 2027 | Healdsburg Jazz Winterfest | Retained |
| 221 | 214 | January 29, 2027 | New Century Chamber Orchestra | Retained |
| 222 | 215 | January 29, 2027 | Santa Rosa Growlers vs. Boston Wahoos | Retained |
| 223 | 216 | January 30, 2027 | Santa Rosa Growlers vs. Boston Wahoos | Retained |
| 224 | 217 | February 6–8, 2027 | Santa Rosa Symphony: Of Myths & Masters | Retained |
| 225 | 218 | February 9, 2027 | World Ballet Company: Swan Lake | Retained |
| 226 | 219 | February 10, 2027 | HYPROV with Colin Mochrie | url |
| 227 | 220 | February 11, 2027 | Kenny Barron — Songbook | Retained |
| 228 | 221 | February 13, 2027 | Smokey Robinson | url |
| 229 | 222 | February 18, 2027 | Ladysmith Black Mambazo | Retained |
| 230 | 223 | February 20, 2027 | Santa Rosa Growlers vs. Oakland Skates | Retained |
| 231 | 224 | February 21, 2027 | Symphony Pops: Storm Large, The Crazy Arc of Love | Retained |
| 232 | 225 | February 25, 2027 | Cirque Kalabanté — World of Words | Retained |
| 233 | 228 | February 26, 2027 | 6th Street Playhouse presents Who’s Afraid of Virginia Woolf? — Opening performance | url, month, date, name |
| 234 | 226 | February 26, 2027 | Let Love Lead — A Celebration of Black Music | Retained |
| 235 | 227 | February 27, 2027 | Michael Davidman, piano | Retained |
| 236 | 229 | March 5, 2027 | Mavis Staples | Retained |
| 237 | 230 | March 5, 2027 | Santa Rosa Growlers vs. San Diego Renegades | Retained |
| 238 | 231 | March 6, 2027 | Jake Shimabukuro | Retained |
| 239 | 232 | March 6, 2027 | Santa Rosa Growlers vs. San Diego Renegades | Retained |
| 240 | 233 | March 6–7, 2027 | Wine Road Barrel Tasting Weekend | Retained |
| 241 | 234 | March 8, 2027 | Treasure Island Reimagined: Jane Hawkins and the Pirate’s Gold | Retained |
| 242 | 235 | March 13–15, 2027 | Mozart & Brahms — Santa Rosa Symphony | Retained |
| 243 | 236 | March 16–21, 2027 | 30th Sonoma International Film Festival | Retained |
| 244 | 237 | March 19, 2027 | Santa Rosa Growlers vs. New York Fire Department | Retained |
| 245 | 238 | March 20, 2027 | Santa Rosa Growlers vs. New York Fire Department | Retained |
| 246 | 239 | March 20, 2027 | Sonoma Guitar Series: David Russell | Retained |
| 247 | 240 | March 21, 2027 | Burn the Floor: Maks and Peta | Retained |
| 248 | 241 | March 24, 2027 | Twilight in Concert | Retained |
| 249 | 242 | March 27, 2027 | Step Afrika! | Retained |
| 250 | 243 | April 2, 2027 | Clifford The Big Red Dog — The Musical | Retained |
| 251 | 244 | April 2, 2027 | Santa Rosa Growlers vs. St. Louis Spirit | Retained |
| 252 | 245 | April 3, 2027 | Free Family Day with 123 Andrés | Retained |
| 253 | 246 | April 3, 2027 | Santa Rosa Growlers vs. St. Louis Spirit | Retained |
| 254 | 247 | April 4, 2027 | Symphony Pops: The Music of Billy Joel Starring Michael Cavanaugh | url |
| 255 | 248 | April 9, 2027 | Santa Rosa Growlers vs. Vancouver BC Hockey Club | Retained |
| 256 | 249 | April 10–12, 2027 | Carmina Burana — Santa Rosa Symphony | Retained |
| 257 | 250 | April 10, 2027 | Santa Rosa Growlers vs. Vancouver BC Hockey Club | Retained |
| 258 | 251 | April 10–11, 2027 | Sonoma Bach: Spring Returns — Bella Madre de’ Fiori | Retained |
| 259 | 252 | April 17, 2027 | Butter & Egg Days Parade & Festival | Retained |
| 260 | 253 | April 18, 2027 | Aga Khan Master Musicians with Vincent Peirani & Vincent Ségal | Retained |
| 261 | 254 | April 18, 2027 | Earth Day Celebration | Retained |
| 262 | 255 | April 18, 2027 | Reuse & Repair Fair | url (this revision) |
| 263 | 256 | April 20, 2027 | Alice in Wonderland — International Ballet Stars | Retained |
| 264 | 257 | April 20, 2027 | Anthony Ray Hinton | Retained |
| 265 | 258 | April 24, 2027 | Dave Pietro Quintet | Retained |
| 266 | 259 | April 24, 2027 | Levi's GranFondo | Retained |
| 267 | 260 | April 25, 2027 | Click, Clack, Moo | Retained |
| 268 | 261 | April 25, 2027 | Music in the Wild — Santa Rosa Symphony | Retained |
| 269 | 262 | April 25, 2027 | Petaluma Spring Antique Faire | Retained |
| 270 | 263 | April 29, 2027 | Chamber Music Society of Lincoln Center — Mozart & Brahms | Retained |
| 271 | 264 | May 7–23, 2027 | 6th Street Playhouse presents Seagull | url |
| 272 | 265 | May 8–10, 2027 | Pictures at an Exhibition — Santa Rosa Symphony | Retained |
| 273 | 266 | May 13, 2027 | Ethan Lipton & His Orchestra | Retained |
| 274 | 267 | May 14, 2027 | Stella Swings Ella — Big Band | Retained |
| 275 | 268 | May 15, 2027 | Windsor Half Marathon / 10K / 5K | Retained |
| 276 | 269 | May 28–Jun 26, 2027 | 6th Street Playhouse presents The Pajama Game | url |
| 277 | 270 | June 4–5, 2027 | Sonoma Bach Season Finale — Where Two or More are Gathered | Retained |
| 278 | 271 | June 6, 2027 | Road to 100: The Complete Beethoven Symphonies, Year 4 | Retained |
| 279 | 272 | June 11–20, 2027 | Healdsburg Jazz Summerfest | Retained |
| 280 | 273 | August 7–8, 2027 | Gravenstein Apple Fair | Retained |
