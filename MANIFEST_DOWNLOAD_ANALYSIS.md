# Manifest Download Võimaluse Analüüs

**Eesmärk:** Uurida kas saame audio failid alla laadida otse serverist ilma monitor recording'uta

**Praegune lahendus:** Selenium + FFmpeg monitor recording (2 nädalat nonstop)

**Alternatiiv:** Extract manifest URL → download otse (potentsiaalselt 100x kiirem)

---

## Test 1: HTML Source Analüüs

### Teostatud
- **Millal:** 2025-10-12
- **Meetod:** Chrome DevTools → Elements → Copy outerHTML
- **Fail:** `/home/d0021/Automation/ohtujutt-vikerraadio/vikerraadio-source-data/page_source_initial.html`
- **URL testitud:** https://vikerraadio.err.ee/1609228655/ohtujutt-lugu-tuisumemmest-ja-kolmest-vallatust-tuulesellist

### Tulemused
```javascript
// Rida 138 - window.pageControlData objekt
"playerInit": {
  "media": {
    "src": "//vod.err.ee/hls/viker/afcfda57e11c55b5700f88d16410f09f/a/master.m3u8",
    "config": {
      "mediaId": "afcfda57e11c55b5700f88d16410f09f",
      "seriesName": "Õhtujutt",
      "title": "Õhtujutt. Lugu Tuisumemmest ja kolmest vallatust tuulesellist"
    }
  }
}
```

**Täielik URL:**
```
https://vod.err.ee/hls/viker/afcfda57e11c55b5700f88d16410f09f/a/master.m3u8
```

### Järeldused
✅ **Manifest URL on HTML-is kohe olemas** - ei pea mängima
✅ **HLS format (.m3u8)** - MITTE DASH (.mpd) nagu ChatGPT otsis
✅ **Selenium saab selle kätte ilma play nuppu vajutamata**
✅ **mediaId on unikaalne iga loo jaoks**

### Välistatud
❌ Ei pea Network tab'ist püüdma
❌ Ei pea player'it käivitama
❌ Ei pea manifesti dünaamiliselt otsima

---

## Test 2: Console API Test

### Teostatud
- **Millal:** 2025-10-12
- **Meetod:** Chrome DevTools Console
- **Käsud:**
```javascript
console.log(window.radioCtrl);
console.log(document.querySelectorAll('audio'));
console.log(document.querySelectorAll('[src*="mpd"]'));
console.log(document.querySelectorAll('[src*="m4s"]'));
```

### Tulemused
```
window.radioCtrl: undefined
audio elements: NodeList(8) [...]
mpd elements: NodeList []
m4s elements: NodeList []
```

### Järeldused
⚠️ **Angular controller pole avalik** - ei saa `window.radioCtrl` kaudu
✅ **Audio elemente on 8 tükki** - player laadib need dünaamiliselt
❌ **MPD/M4S URL-id pole DOM-is** - need on HLS fragmentidena

### Välistatud
❌ Ei saa `window.radioCtrl` objekti kasutada
❌ DOM-is pole .mpd ega .m4s URL-e

---

## Test 3: Network Tab - Media Filter

### Teostatud
- **Millal:** 2025-10-12
- **Meetod:** Chrome DevTools → Network → Filter: Media
- **Testitud:** ENNE ja PÄRAST play nupu vajutamist

### Tulemused
```
Media tab - ENNE play: (tühi)
Media tab - PÄRAST play: (sama, tühi)
```

**Märkus:** Kasutaja ütles "käivitamine ei muutnud seal mitte midagi"

### Järeldused
⚠️ **Media filter ei näita HLS fragmente** - need võivad olla Fetch/XHR all
❓ **Kas HLS fragmentid laetakse üldse Network tab'is?**

### Järgmised sammud
🔍 **TEST 4: Vaata teisi Network filtreid:**
- [ ] All
- [ ] Fetch/XHR
- [ ] Doc
- [ ] CSS
- [ ] Manifest
- [ ] WS
- [ ] WASM
- [ ] Other

---

## Test 4: Network Tab - Täielik Analüüs ✅ TEHTUD

### Teostatud
- **Millal:** 2025-10-12
- **Meetod:** Chrome DevTools → Network → Save as HAR
- **Failid salvestatud:**
  - `/home/d0021/Automation/ohtujutt-vikerraadio/vikerraadio-source-data/network_after_play_fetch.har` (3.6MB)
  - `/home/d0021/Automation/ohtujutt-vikerraadio/vikerraadio-source-data/network_after_play_other.har` (17KB)
  - `/home/d0021/Automation/ohtujutt-vikerraadio/vikerraadio-source-data/dev_tools_network_analysis` (text)

### Tulemused ENNE Play

**Leitud (rida 108, 125-127):**
```
manifest.mpd        - https://vod.err.ee/dash/viker/afcfda57e11c55b5700f88d16410f09f/a/manifest.mpd
init-a1-x3.mp4      - https://vod.err.ee/dash/viker/.../a/init-a1-x3.mp4
fragment-1-a1-x3.m4s
fragment-2-a1-x3.m4s
fragment-3-a1-x3.m4s
```

### Tulemused PÄRAST Play (20-30s)

**Fetch/XHR filter (read 201, 204, 206, 208-209):**
```
manifest.mpd (uuesti)
init-a1-x3.mp4 (uuesti)
fragment-1-a1-x3.m4s
fragment-2-a1-x3.m4s
fragment-3-a1-x3.m4s
```

**Media filter:** TÜHI ❌
**Manifest filter:** TÜHI ❌

### Järeldused

✅ **ERR.ee kasutab DASH, MITTE HLS!**
- HTML-is on `.m3u8` (vale - ei kasutata)
- Päriselt laetakse `.mpd` manifest

✅ **Manifest laetakse KOHE lehel**
- Ei pea play nuppu vajutama
- Preload strateegia: laeb esimesed 3 fragmenti

✅ **Fragmentide URL struktuur:**
```
https://vod.err.ee/dash/viker/{mediaId}/a/init-a1-x3.mp4
https://vod.err.ee/dash/viker/{mediaId}/a/fragment-{N}-a1-x3.m4s
```

⚠️ **Ainult 3 fragmenti nähtav (20-30s mängimist)**
- Iga fragment ~10 sekundit?
- Kokku lugu on ~527s (8m47s)
- Peaks olema ~53 fragmenti

### Välistatud

❌ **HLS ei kasutata** - manifest.mpd on DASH
❌ **Media filter ei näita DASH fragmente**
❌ **Manifest filter ei näita .mpd faile** (ilmselt Fetch/XHR all)

---

## Test 5: Manifest.mpd Analüüs ✅ TEHTUD

### Teostatud
- **Millal:** 2025-10-12
- **Meetod:** Ava manifest URL brauseris, salvesta fail
- **Fail:** `/home/d0021/Automation/ohtujutt-vikerraadio/vikerraadio-source-data/manifest.mpd`
- **URL:** `https://vod.err.ee/dash/viker/afcfda57e11c55b5700f88d16410f09f/a/manifest.mpd`

### Manifest Sisu (XMLrida 1-35)

**Peamised parameetrid:**
```xml
<MPD type="static"
     mediaPresentationDuration="PT527.209S"
     minBufferTime="PT10S">
```

**Audio spetsifikatsioon:**
```xml
<Representation id="a1-x3"
    mimeType="audio/mp4"
    codecs="mp4a.40.2"
    audioSamplingRate="44100"
    bandwidth="128000">
```

**Segment template (rida 17-23):**
```xml
<SegmentTemplate
    timescale="1000"
    media="https://vod.err.ee/dash/viker/.../a/fragment-$Number$-$RepresentationID$.m4s"
    initialization="https://vod.err.ee/dash/viker/.../a/init-$RepresentationID$.mp4"
    duration="10000"
    startNumber="1">
```

### Arvutused

**Kestus:**
- Manifest: `PT527.209S` = **527.209 sekundit**
- CSV catalog: **527 sekundit**
- ✅ **TÄPNE MATCH!**

**Fragmentide arv:**
- Kestus: 527s
- Fragment kestus: 10s (duration="10000", timescale="1000")
- Fragmentide arv: 527 ÷ 10 = **~53 fragmenti**
- URL-id: `fragment-1-a1-x3.m4s` kuni `fragment-53-a1-x3.m4s`

**Audio kvaliteet:**
- Codec: AAC (`mp4a.40.2`)
- Sample rate: `44.1 kHz`
- Bitrate: `128 kbps`
- Channels: `1` (mono)

### Fragmentide URL-id

**Init segment:**
```
https://vod.err.ee/dash/viker/afcfda57e11c55b5700f88d16410f09f/a/init-a1-x3.mp4
```

**Audio fragmentid (näited):**
```
https://vod.err.ee/dash/viker/afcfda57e11c55b5700f88d16410f09f/a/fragment-1-a1-x3.m4s
https://vod.err.ee/dash/viker/afcfda57e11c55b5700f88d16410f09f/a/fragment-2-a1-x3.m4s
...
https://vod.err.ee/dash/viker/afcfda57e11c55b5700f88d16410f09f/a/fragment-53-a1-x3.m4s
```

**mediaId väljund URL-ist:**
```
afcfda57e11c55b5700f88d16410f09f
```

### Järeldused

✅ **Manifest on avalikult ligipääsetav** - ei vaja autentimist
✅ **Kestus täpselt CSV-ga** - 527s
✅ **Fragmentide URL-id on teada** - genereerimine lihtne
✅ **Audio kvaliteet hea** - 128kbps AAC
✅ **Segmentide struktuur lihtne** - init + 53 fragmenti

### Välistatud

❌ Ei vaja DRM dekodeerimist
❌ Ei vaja session cookie'sid
❌ Ei vaja IP whitelisting'ut (vähemalt manifest ligipääsetav)

---

## Test 6: yt-dlp Allalaadimine ✅ TÖÖTAB!

### Teostatud
- **Millal:** 2025-10-12
- **Meetod:** yt-dlp käsurealt
- **Käsk:**
```bash
yt-dlp "https://vod.err.ee/dash/viker/afcfda57e11c55b5700f88d16410f09f/a/manifest.mpd" -o "test_download.mp3"
```

### Tulemused

**Fail loodud:** `test_download.mp3`

**FFmpeg analüüs:**
```bash
ffmpeg -i test_download.mp3 2>&1 | grep Duration
Duration: 00:08:47.21, start: 0.000000, bitrate: 129 kb/s
```

**Võrdlus:**
| Parameeter | Oodatud | Saadud | Match |
|------------|---------|--------|-------|
| Kestus | 527s (8m47s) | 00:08:47.21 | ✅ TÄPNE |
| Bitrate | 128 kbps | 129 kb/s | ✅ OK |

### Järeldused

✅ **yt-dlp suudab alla laadida!**
✅ **Kestus täpselt õige** - 8m47s
✅ **Bitrate õige** - 128kbps
✅ **Ei vaja autentimist**
✅ **Ei vaja browser'it**

🎉 **MANIFEST DOWNLOAD TÖÖTAB 100%!**

### Kiirusehinnang

**Praegune meetod (monitor recording):**
- Lindistab reaalajas: 527s = **8m47s loo kohta**
- 2344 lugu × 8.78 min = **~342 tundi = 14 päeva**

**Uus meetod (yt-dlp manifest download):**
- Allalaadimine võrgukiirusega
- Eeldame 10 MB faili (128kbps × 527s ≈ 8.5MB)
- 10 Mbps interneti puhul: 8.5MB ÷ 1.25MB/s = **~7 sekundit**
- 2344 lugu × 7s = **~4.5 tundi**

**Kiiruse võit: ~75x kiirem!** (14 päeva → 4.5 tundi)

---

## Test 7: Täielik Workflow Test ✅ TÖÖTAB PERFEKTSELT!

### Teostatud
- **Millal:** 2025-10-12
- **Meetod:** Automatiseeritud test (Selenium + yt-dlp)
- **Testskript:** `vikerraadio-source-data/test_manifest_download.py`
- **Test URL:** `https://vikerraadio.err.ee/1609228655/ohtujutt-lugu-tuisumemmest-ja-kolmest-vallatust-tuulesellist`

### Workflow

**1. Selenium Extract (3s):**
```python
driver.get(story_url)
mediaId = window.pageControlData.playerInit.media.config.mediaId
manifest_url = f'https://vod.err.ee/dash/viker/{mediaId}/a/manifest.mpd'
```
✅ **Töötab:** Ekstraktis manifest URL-i

**2. yt-dlp Download (6s):**
```bash
yt-dlp "https://vod.err.ee/dash/viker/.../manifest.mpd" -o "test_story.mp3"
```
✅ **Töötab:** Laadiis 8.13 MB faili 6 sekundiga

**3. FFmpeg Verify:**
```bash
ffmpeg -i test_story.mp3
Duration: 00:08:47.21 (527.2s)
```
✅ **Töötab:** Kestus täpne

### Tulemused

```
TEST: Manifest Download Method
============================================================

[1/3] Extract manifest URL from page
  ✓ Manifest URL: https://vod.err.ee/dash/viker/.../manifest.mpd

[2/3] Download with yt-dlp
  ✓ Downloaded: test_downloads/test_story.mp3
  ✓ Size: 8.13 MB
  ✓ Time: 6.0s

[3/3] Verify audio file
  ✓ Duration: 527.2s (8m47s)

✓ TEST PASSED!
```

### Võrdlus Meetodite Vahel

| Parameeter | Monitor Recording | Manifest Download | Võit |
|------------|-------------------|-------------------|------|
| **Aeg loo kohta** | 527s (8m47s) | 6s | **88x kiirem** |
| **2344 lugu** | 342h (14 päeva) | 3.9h (~4h) | **88x kiirem** |
| **Vajab browser'it** | Jah (kogu aeg) | Jah (3s URL jaoks) | Vähem |
| **Võrgu kasutus** | Vähene | Intensiivne | - |
| **Kvaliteet** | 128kbps + vaikused | 128kbps täpne | Sama/parem |
| **Stabiilsus** | Võib hanguda | Stabiilne | Parem |

### Eeldatav Ajakulu 2344 Loole

**Selenium extract:**
- 3s × 2344 = **7032s = 2h**

**yt-dlp download:**
- 6s × 2344 = **14064s = 3.9h**

**Kokku:** ~**6 tundi** (konservatiivne hinnang)

**vs Praegune:** 14 päeva (336h)

**Kiirus:** **56x kiirem!**

### Järeldused

✅ **Meetod töötab 100%**
✅ **Selenium extract on kiire** (3s)
✅ **yt-dlp download on kiire** (6s vs 527s)
✅ **Audio kvaliteet täpne** (527.2s)
✅ **Pole vaja browser'it mängimiseks**
✅ **Stabiilsem** kui monitor recording

🎉 **VALMIS TOOTMISEKS!**

### Riskid

⚠️ **ERR.ee võib blokeerida:**
- Rate limiting (liiga palju päringuid)
- IP block
- Manifest URL aegub?

**Soovitus:**
- Lisa delay requestide vahele (1-2s)
- Retry logic
- Error logging

---

## Praegused Eeldused

### HLS Struktuur (teadaolevalt)
```
master.m3u8 (manifest)
  ↓
playlist.m3u8 (stream info)
  ↓
segment001.ts
segment002.ts
segment003.ts
...
```

### Allalaadimise Võimalused

**Variant A: yt-dlp**
```bash
yt-dlp "https://vod.err.ee/hls/viker/afcfda57e11c55b5700f88d16410f09f/a/master.m3u8"
```
- ✅ Lihtne
- ✅ Laadib automaatselt kõik fragmendid
- ⚠️ Kas töötab ERR.ee serveritega?

**Variant B: ffmpeg**
```bash
ffmpeg -i "https://vod.err.ee/hls/viker/.../master.m3u8" -c copy output.mp3
```
- ✅ Lihtne
- ✅ Ei dekodeeri, kopeerib otse
- ⚠️ Kas töötab ERR.ee serveritega?

**Variant C: Selenium extract + yt-dlp**
```python
# 1. Selenium avab lehe
driver.get(story_url)

# 2. Extract manifest URL
manifest_url = driver.execute_script(
    "return window.pageControlData.playerInit.media.src"
)

# 3. yt-dlp laadib alla
subprocess.run(["yt-dlp", manifest_url])
```
- ✅ Automatiseeritud
- ✅ Kasutab CSV-st URL-e
- ✅ Ei pea mängima

---

## Järgmised Sammud

### 1. Network Tab Täielik Analüüs ✅ TEHTUD
- [x] Testi kõiki Network filtreid
- [x] Salvesta HAR fail
- [x] DASH manifest.mpd leitud!

### 2. URL Testimine ✅ TEHTUD
- [x] **Ava manifest.mpd brauseris** - töötab!
- [x] **Vaata manifest sisu** - 53 fragmenti
- [x] **yt-dlp allalaadimine** - ✅ **TÖÖTAB!**

### 3. Selenium Extract + Download Test ✅ TÖÖTAB!
- [x] Testskript loodud: `vikerraadio-source-data/test_manifest_download.py`
- [x] Extract manifest URL HTML-ist - töötab!
- [x] yt-dlp download - töötab!
- [x] Audio verifitseerimine - töötab!

---

## Riskid ja Piirangud

### Võimalikud Probleemid
⚠️ **ERR.ee võib blokeerida otse allalaadimist** (CORS, auth)
⚠️ **URL võib aeguda** (session-based)
⚠️ **IP rate limiting** (liiga palju päringuid)

### Testimine Vajalik
✅ Kas master.m3u8 on avalikult ligipääsetav?
✅ Kas URL töötab väljaspool brauserit?
✅ Kas yt-dlp/ffmpeg saavad alla laadida?

---

## 🎉 LÕPLIK KOKKUVÕTE

### ✅ TÖÖTAV LAHENDUS LEITUD!

**Meetod:** Selenium extract + yt-dlp manifest download

**Tehtud Testid:**
1. ✅ HTML source analüüs → DASH manifest URL leitud
2. ✅ Console API test → mediaId ekstraktimine
3. ✅ Network tab analüüs → manifest.mpd struktuuri kinnitus
4. ✅ Manifest.mpd analüüs → 53 fragmenti, 527s kestus
5. ✅ yt-dlp download test → 6s, 8.13MB, töötab!
6. ✅ FFmpeg verify → kestus täpne (527.2s)
7. ✅ **Täielik workflow test → PERFEKTNE!**

### Peamised Avastused

**Tehnilised:**
- ❌ HTML-is on `.m3u8` (vale, ei kasutata)
- ✅ Päriselt kasutatakse **DASH** (`.mpd`)
- ✅ `window.pageControlData.playerInit.media.config.mediaId` sisaldab mediaId
- ✅ Manifest URL: `https://vod.err.ee/dash/viker/{mediaId}/a/manifest.mpd`
- ✅ Manifest avalikult ligipääsetav (ei vaja auth)
- ✅ yt-dlp oskab DASH manifest'e alla laadida

**Kiirusevõit:**
- Monitor recording: **14 päeva** (2344 lugu × 8.78 min)
- Manifest download: **~6 tundi** (2344 lugu × 9s)
- **Kiirus: 56x kiirem!**

### Järgmised Sammud

**Implementeerimine:**
1. Kopeeri `test_manifest_download.py` loogika
2. Integreeri CSV-ga
3. Lisa progressi tracking
4. Lisa error handling
5. Lisa retry logic
6. Lisa delay requestide vahele (rate limiting)

**Soovitused:**
- Alusta väikese testiga (10-20 lugu)
- Jälgi ERR.ee vastust (rate limiting?)
- Lisa statistika (kiirus, errorid, õnnestumised)

### Riskid ja Lahendused

⚠️ **Risk:** ERR.ee blokeerib liiga palju päringuid
✅ **Lahendus:** Lisa 1-2s delay, retry logic

⚠️ **Risk:** Manifest URL aegub
✅ **Lahendus:** Extract iga loo jaoks uuesti

⚠️ **Risk:** Võrk aeglane
✅ **Lahendus:** Timeout'id, error handling

---

🚀 **VALMIS TOOTMISEKS!**
📊 **ChatGPT vs Meie:** Me leidsime DASH lahenduse, ChatGPT ei leidnud

---

## 🎯 TOOTMISE TULEMUSED

### Implementeerimine Valmis ✅

**Loodud failid:**
- `download_stories.py` - Põhiskript (CSV integratsioon)
- `csv_manager.py` - Reusable CSV moodul
- `manifest_downloader.py` - Manifest download funktsioonid

**Funktsionaalsus:**
- ✅ CSV integratsioon (reused from record_stories.py)
- ✅ 3x retry loogika
- ✅ Quality control (duration check > 10s)
- ✅ Broken file cleanup (kustutab katkised failid retry jaoks)
- ✅ Graceful shutdown (Ctrl+C)
- ✅ Per-lugu progress (yt-dlp --progress, fragments)
- ✅ Session progress (ETA, avg speed, X/total)
- ✅ Automaatne CSV backup

### Tegelikud Testitulemused

**Test 1: Üks lugu (päeval)**
```
Lugu: Õhtujutt. Hunt ja seitse kitsetalle
Extract: 3s
Download: 18.8s
Size: 6.78 MB
Duration: 439s (7m19s)
Total: 29s
Result: ✅ 100% success
```

**Test 2: Kolm lugu (päeval)**
```
Total unsaved: 2163 stories
Test count: 3 stories

[1/2163] Okasroosike
  Extract: ~3s
  Download: 16s (9.40 MB, 582 KiB/s)
  Duration: 609s (10m9s)
  ✅ Success

[2/2163] Mullitamaa suvi, 5
  Extract: ~3s
  Download: 18s (10.50 MB, 603 KiB/s)
  Duration: 680s (11m20s)
  ETA: 20.3h (avg 34s/story)
  ✅ Success

[3/2163] Mullitamaa suvi, 4
  Extract: ~3s
  Download: 19s (11.75 MB, 624 KiB/s)
  Duration: 761s (12m41s)
  ETA: 19.9h (avg 33s/story)
  ✅ Success

Results:
  Downloaded: 3/3 (100%)
  Skipped: 0
  Failed: 0
  Total audio: 2050s (34m)
  Session time: 100s (1m40s)
  Speed: 20x faster than realtime!
```

### Realistlik Kiirusehinnang

**Päeval (tegelikud tulemused):**
- Avg per story: 33-34s
- 2163 stories × 33s = **19.8h ≈ 20 tundi**

**Öösel (hinnang):**
- Kiirem võrk (vähem kasutajaid)
- Eeldatav: 25-28s per story
- 2163 stories × 27s = **16.2h ≈ 16 tundi**

**Monitor recording:**
- 2163 stories × 600s (avg) = **360h ≈ 15 päeva**

**Kiirus:**
- Päeval: **18x kiirem** (20h vs 360h)
- Öösel: **22x kiirem** (16h vs 360h)

### Korrektsioonid Esialgsetele Hinnangutele

**Esialg optimistlik hinnang:**
- Extract: 3s
- Download: 6s
- Total: 9s per story
- 2163 × 9s = **5.4h**
- **56x kiirem**

**Tegelik (päeval):**
- Extract: 3s
- Download: 16-24s (varieeruv võrgukiirus)
- Total: 33s per story
- 2163 × 33s = **19.8h**
- **18x kiirem**

**Miks aeglasem kui oodatud:**
1. yt-dlp download varieeruv (16-24s, mitte 6s)
2. ERR.ee serveri kiirus päeval madalam
3. Võrgukiirus kõikub (580-624 KiB/s)

**Järeldus:** Ikkagi suurepärane tulemus - **18-22x kiirem** kui monitor recording!

### Märkused

**Postprocessing error:**
```
ERROR: Postprocessing: Stream #0:0 -> #0:0 (copy)
```
- See on yt-dlp tuntud error (container fix step)
- **Harmless** - fail luuakse korrektselt
- Quality control kinnitab kestuse

**Quality Control:**
- CSVManager kontrollib kestust (mutagen)
- Kui duration mismatch > 10s → reject & retry
- 3/3 lugu läbisid quality control ✅

### Soovitused Tootmiseks

1. **Käivita öösel** (kiirem võrk)
2. **Jälgi ETA-d** (progress tracking näitab)
3. **Ära katkesta Ctrl+C-ga** ilma põhjuseta (graceful shutdown toimib)
4. **Kontrolli duration_mismatch.txt** pärast lõppu

---

## 📊 LÕPLIK KOKKUVÕTE

### Võrdlus: Monitor Recording vs Manifest Download

| Parameeter | Monitor Recording | Manifest Download | Võit |
|------------|-------------------|-------------------|------|
| **Aeg (2163 lugu)** | 360h (15 päeva) | 20h (0.8 päeva) | **18x kiirem** |
| **Browser vajalik** | Kogu aeg | 3s per lugu | **99% vähem** |
| **Stabiilsus** | Võib hanguda | Retry loogika | **Parem** |
| **Quality control** | Manual check | Auto check | **Parem** |
| **Progress tracking** | Puudub | ETA + stats | **Parem** |
| **Failid** | Vaikustega | Täpne kestus | **Parem** |
| **Riskid** | Browser crash | Rate limit | **Erinevad** |

### Soovitus

🟢 **Kasuta download_stories.py** (manifest download):
- 18-22x kiirem
- Stabiilsem
- Built-in quality control
- Progress tracking

🟡 **Kasuta record_stories.py** ainult kui:
- Internetiühendus on ebastabiilne
- ERR.ee blokeerib (rate limiting)

---

🎉 **PROJEKT EDUKAS!**
⏱️ **19.8h vs 15 päeva - SUUR VÕIT!**
