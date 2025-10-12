# Vikerraadio Õhtujutt Automatiseerimine

Automaatsed skriptid Vikerraadio õhtujuttude katalogiseerimiseks ja lindistamiseks.

## Skriptide Ülevaade

### 1. `collect_story_info.py` - Lugude Katalogiseerimine ⚠️ KADUNUD

**Staatus:** ⚠️ **Originaal skript on kadunud/üle kirjutatud**. Praegune fail on mingi test skript m4s URL-ide jaoks.

**Originaalne eesmärk:** Kammis läbi KOGU Vikerraadio arhiivi ja kogu kõikide lugude info CSV faili.

**Originaalsed funktsioonid (CSV juba olemas, uuesti tegemine pole vajalik):**
- Navigeeris läbi kõik arhiivi leheküljed (dünaamiliselt Angular SPA-s)
- Kasutas tab-e, et säilitada arhiivi dünaamiline olek
- Luges iga loo kestuse audio playerist
- Kontrollis, kas fail on juba alla laaditud (saved=0/1)
- Salvestas info `ohtujutt_catalog.csv` faili
- Jätkas katkestuse korral (skip juba töödeldud lood)

**Märkus:** CSV (`ohtujutt_catalog.csv`) on juba olemas 3501 looga. Skripti taastamine pole vajalik, kuna kõik lood on juba kataloogis. Uute lugude lisamiseks tuleks skript taastada README kirjelduse põhjal.

**Väljund:** `ohtujutt_catalog.csv`
- Tulbad: `page, index, title, url, duration_seconds, duration_formatted, saved`
- Näide: `1,0,Õhtujutt lastele. Kiisula loss,https://vikerraadio.err.ee/1609812943/ohtujutt-lastele-kiisula-loss,838,13:58,0`

**Oluline:**
- Iseseisev skript - ei sõltu teistest
- Kasutab uusi tab-e, et säilitada arhiivi dünaamiline olek
- Võib katkestada ja hiljem jätkata (append mode)

---

### 2. `record_stories.py` - Lugude Lindistamine

**Eesmärk:** Lindistab lood, mis on CSV-s märgitud kui `saved=0`.

**Funktsioonid:**
- Loeb lugude info `ohtujutt_catalog.csv` failist
- Filtreerib välja `saved=0` lood
- Lindistab ffmpeg-iga (pulse audio)
- Jälgib playback progressi ja peatab õigel hetkel
- Uuendab CSV-s `saved=1` pärast edukat lindistust

**Kasutamine:**
```bash
python3 record_stories.py
```

**Eeldused:**
- `ohtujutt_catalog.csv` peab eksisteerima
- ffmpeg peab olema installitud
- pulse audio peab töötama

**Väljund:**
- MP3 failid: `Õhtujutt/` kaustas
- Logid: `failed_downloads.txt`, `downloaded_items.txt`

---

### 3. `download_stories.py` - Lugude Allalaadimine (SOOVITATAV)

**Eesmärk:** Laadib lood alla otse ERR.ee serverist kasutades manifest faile (DASH).

**Funktsioonid:**
- Loeb lugude info `ohtujutt_catalog.csv` failist
- Filtreerib välja `saved=0` lood
- Ekstraktib manifest URL iga loo jaoks (Selenium)
- Laadib audio alla yt-dlp abil (DASH manifest)
- **19x kiirem** kui monitor recording (20h vs 390h 2163 loo jaoks)
- 3x retry loogika ebaõnnestunud allalaadimistele
- Quality control: kontrollib faili kestust (mutagen)
- Progress tracking: ETA, kiirus, statistika
- **Võrguühenduse kaitse:** peatub automaatselt 5 järjestikuse ebaõnnestumise järel
- **Automaatne cleanup:** kustutab yt-dlp ajutised failid (.temp.mp3, .part, .ytdl) pärast edukat allalaadimist

**Kasutamine:**
```bash
python3 download_stories.py
# Küsib: How many stories to download? (Enter või number)
```

**Eeldused:**
- `ohtujutt_catalog.csv` peab eksisteerima
- yt-dlp peab olema installitud (`pip install yt-dlp`)
- python3-mutagen peab olema installitud (`sudo apt install python3-mutagen`)

**Väljund:**
- MP3 failid: `Õhtujutt/` kaustas
- Log: `duration_mismatch.txt` (quality control)

**Eelised vs record_stories.py:**
- ✅ **19x kiirem** (20h vs 16 päeva)
- ✅ Stabiilsem (ei sõltu brauseri playback'ist)
- ✅ Quality control built-in
- ✅ 3x retry loogika
- ✅ Reaalajas progress tracking
- ✅ Ei vaja audio monitoring
- ✅ Võrguühenduse kaitse (peatub automaatselt kui võrk kadunud)
- ✅ Automaatne temp failide cleanup (ei jäta prügi maha)
- ❌ Vajab internetiühendust (ERR.ee server)

**Märkused:**
- Öösel kiirem (vähem kasutajaid ERR.ee serveris)
- Postprocessing error "Stream #0:0 -> #0:0 (copy)" on harmless
- Vaata täpsemat dokumentatsiooni: `MANIFEST_DOWNLOAD_ANALYSIS.md`

---

### 4. `trim_silence.py` - Vaikuse Eemaldamine

**Eesmärk:** Eemaldab üleliigsed vaiksed osad lindistuste lõpust.

**Kasutamine:**
```bash
python3 trim_silence.py
```

**Funktsioon:**
- Leiab kõik MP3 failid `Õhtujutt/` kaustas
- Eemaldab vaikuse lõpust (alla -40dB)
- Teeb backup originaalist

---

## Töövoog

### Esimene Kord (SOOVITATAV):

1. **Kogu kataloog:**
   ```bash
   python3 collect_story_info.py
   ```
   - Kammib läbi kogu arhiivi
   - Loob `ohtujutt_catalog.csv`
   - Võib võtta mitu tundi (kõik leheküljed läbi)

2. **Lae lood alla (SOOVITATAV - 19x kiirem):**
   ```bash
   python3 download_stories.py
   ```
   - Loeb CSV-st `saved=0` lood
   - Laadib alla DASH manifest abil
   - Uuendab CSV-s `saved=1`
   - ~20h 2163 loo jaoks (vs 16 päeva monitor recording)

**VÕI alternatiiv (aeglasem):**

2. **Lindista lood (monitor recording):**
   ```bash
   python3 record_stories.py
   ```
   - Loeb CSV-st `saved=0` lood
   - Lindistab ffmpeg-iga
   - Uuendab CSV-s `saved=1`
   - ~390h 2163 loo jaoks

3. **Puhasta vaikused (ainult kui kasutasid record_stories.py):**
   ```bash
   python3 trim_silence.py
   ```

### Hilisemad Korrad (uued lood):

1. **Uuenda kataloogi:**
   ```bash
   python3 collect_story_info.py
   ```
   - Skip-ib juba olemasolevad lood
   - Lisab ainult uued

2. **Lae uued lood alla:**
   ```bash
   python3 download_stories.py
   # VÕI
   python3 record_stories.py
   ```

---

## Failide Struktuur

```
ohtujutt-vikerraadio/
├── .gitignore                      # Git ignore (MP3, backups, temp failid)
├── README.md                       # See fail
├── TODO.md                         # Tehtavad ülesanded
├── USAGE.md                        # Kasutamise juhend
├── COMPACTING_GUIDELINES.md        # Koodipõhimõtted
├── MANIFEST_DOWNLOAD_ANALYSIS.md   # Manifest meetodi dokumentatsioon
├── download_stories.py             # DASH manifest allalaadimine (SOOVITATAV)
├── record_stories.py               # Monitor recording (alternatiiv)
├── csv_manager.py                  # CSV moodul (reusable)
├── manifest_downloader.py          # Manifest download funktsioonid
├── cleanup_temp_files.py           # Temp failide kustutamine (manual)
├── trim_silence.py                 # Vaikuse eemaldamine
├── ohtujutt_catalog.csv            # Lugude kataloog (3501 lugu)
├── deprecated/                     # Vanad/kasutamata skriptid
│   ├── find_duplicates.py
│   ├── fix_duplicate_status.py
│   ├── mark_duplicates.py
│   └── sync_saved_status.py
├── vikerraadio-source-data/        # Test skriptid ja andmed
│   ├── test_manifest_download.py
│   ├── test_three_stories.py
│   └── ...
└── Õhtujutt/                       # Allalaaditud/lindistatud MP3-d (gitignore)
    ├── Õhtujutt lastele. Kiisula loss.mp3
    └── ...
```

---

## Tehnilised Detailid

### CSV Kataloog (`ohtujutt_catalog.csv`)

**Tulbad:**
- `page` - Arhiivi lehekülje number (1, 2, 3, ...)
- `index` - Loo järjekorranumber lehel (0-99)
- `title` - Loo pealkiri
- `url` - Loo URL
- `duration_seconds` - Kestus sekundites (nt 838)
- `duration_formatted` - Kestus formaadis MM:SS (nt 13:58)
- `saved` - Kas lindistatud (0=ei, 1=jah)

### Arhitektuuri Otsused

**Miks kaks skripti?**
- `collect_story_info.py` - Raske töö (kõik lehed läbi)
- `record_stories.py` - Lihtne töö (CSV-st lindistamine)
- Kui lindistamine katkestatakse, ei pea uuesti lehti skaneerima

**Miks tab-id?**
- Arhiivi leht on Angular SPA (dünaamiline)
- VANEMAD nupp laadib uued lood dünaamiliselt
- `driver.get(URL)` kaotaks dünaamilise oleku
- Tab-id säilitavad arhiivi lehe oleku

**Miks skip juba töödeldud?**
- Kui skript katkestatakse, saab jätkata
- Ei pea uuesti sama tööd tegema
- CSV append mode + URL kontrollimine

---

## Probleemid ja Lahendused

### Probleem: Angular SPA dünaamiline laadimine
**Põhjus:** ERR.ee kasutab vanemat Angular raamistikku, mis laadib sisu dünaamiliselt
- Elemendist saadud markerid (audio player, duration, jne) toimivad ainult avatud lehel
- Kui samas tab'is järgmine leht avada (`driver.get()`), ei uuenda Angular ennast korralikult
- Player init'imine ebaõnnestub, audio element puudub või ei mängi

**Lahendus:** Kasuta uusi tab-e
- Ava iga lugu uues tab'is (`window.open(url, '_blank')`)
- Säilitab Angular state'i ja player laeb korrektselt
- Kasutatud nii `collect_story_info.py` kui `record_stories.py` skriptides

### Probleem: "Extracted 0 story URLs" teisel lehel
**Põhjus:** `driver.get(URL)` kaotab dünaamiliselt laaditud lood
**Lahendus:** Kasuta tab-e, ära navigate tagasi

### Probleem: Üleliigne vaikus lindistuste lõpus
**Põhjus:** Lindistamine ei peatu õigel hetkel
**Lahendus:** `trim_silence.py` või paranda `monitor_playback_and_stop()`

### Probleem: Mitu lugu ühes failis (54-58MB)
**Põhjus:** Playback auto-restart (järgmine lugu mängib)
**Lahendus:** Restart detection `monitor_playback_and_stop()`-is

---

## Tuleviku Täiendused

- [ ] Parallelsete lindistuste tugi
- [ ] Retry loogika ebaõnnestunud lugudele
- [ ] Web UI kataloo gi vaatamiseks
- [ ] Automaatne uute lugude tuvastamine (cron job)
- [ ] Metaandmete lisamine MP3 failidele (ID3 tags)

---

## record_stories.py Arhitektuur

### Konfiguratsioon
Globaalsed konstantid faili alguses (ADHD-friendly, KISS):
```python
OUTPUT_FOLDER = "Õhtujutt"
AUDIO_FORMAT = "mp3"
CSV_PATH = "ohtujutt_catalog.csv"
AUDIO_SOURCE = "alsa_output.pci-0000_00_1b.0.analog-stereo.monitor"
```

### Klassid ja nende vastutus

#### CSVManager
**Eesmärk:** Haldab lugude andmeid CSV failist

**Töövoog:**
1. Laeb CSV → mälu (dict)
2. Otsib järgmine salvestamata originaal lugu → annab edasi
3. Saab tagasi kinnituse (salvestatud!)
4. **Kontrollib, et fail on tõesti olemas** enne märkimist
5. Uuendab mälus olevat dict'i
6. Teeb backup vanast CSV-st
7. Kirjutab uue CSV faili

**Sisend:**
- CSV path konstruktoris
- Story URL kui uuendab

**Väljund:**
- Story dict kui otsib
- None kui enam pole midagi salvestada
- Boolean kui märgib saved (kas fail eksisteerib)

**Oluline:**
- Kontrollib `title`, `url`, `duration_seconds` olemasolu
- Kontrollib `saved='0'` ja `duplicate_status='original'`
- Salvestab ainult kui fail on tõesti olemas (usaldusväärne andmeallikas)
- **Quality control:** Kontrollib faili kestust (mutagen library)
  - Kui erinevus > 10 sekundit, logib `duration_mismatch.txt`
  - Märgib ikkagi `saved='1'` (kasutaja saab hiljem parandada)

#### BrowserController
**Eesmärk:** Juhib Chrome brauserit - avab lehti tab'ides, käivitab audio mängimise

**Töövoog:**
1. Käivitab Chrome driveri (üks kord alguses)
2. **ESIMENE lugu:** Avab main tab'is (`driver.get()`)
   - 5s ooteaeg (cookie modal, Angular init)
3. **JÄRGMISED lood:** Avab uues tab'is (`open_story_in_new_tab()`)
   - 3× retry logic kui tab avamine ebaõnnestub
   - Defensive: kontrollib et tab tekkis, timeout 5s
   - Vahetab automaatselt uuele tab'ile
   - Page load: 5s ooteaeg
4. **Leiab ja klikib play nuppu** (`click_play()`)
   - Scrollib nupu viewport'i keskele
   - Simuleerib hiire hover'it (Angular detect)
   - Klikib nuppu
5. Kinnitab, et mängimine käivitus (TODO: `verify_playback()`)
6. **Sulgeb story tab** (`close_story_tab()`)
   - Ainult järgmiste lugude puhul (mitte esimene)
   - Defensive: kontrollib tab'ide arvu
   - Vahetab tagasi järelejäänud tab'ile
7. (kordub järgmiste lugude jaoks - alati 1-2 tab'i)
8. Sulgeb browseri (lõpus, kui kõik lood valmis)

**Sisend:**
- Story URL (iga loo jaoks)

**Väljund:**
- Boolean (kas operatsioon õnnestus)

**Oluline:**
- **Esimene lugu main tab'is** - browser värskelt käivitatud, Angular init'ib korrektselt
- **Järgmised lood uutes tab'ides** - Angular SPA dünaamilise laadimise probleem
- **Hiire simulatsioon** - scroll + hover trigger'dab Angular event detection
- Helper meetodid: `_open_new_tab()`, `_wait_for_page_load()`, `_try_click_play_with_hover()`

#### AudioRecorder
**Eesmärk:** Salvestab audio failiks - MVP lähenemisega (fixed duration)

**Töövoog:**
1. Võtab title ja duration_seconds
2. Ehitab faili tee: `{output_folder}/{title}.mp3`
3. **Kontrollib faili olemasolu** - kui eksisteerib, lisab suffix (_2, _3, ...)
4. Salvestab audio täpselt `duration_seconds + 2` sekundit (buffer)
5. Tagastab faili tee

**Sisend:**
- Story title (failinimeks)
- Duration seconds (kui kaua salvestada)

**Väljund:**
- File path (kuhu salvestati)

**Oluline:**
- **Ei kirjuta olemasolevat faili üle** - kaitseb duplikaatide eest
- Helper meetod: `_get_unique_filename()` - leiab vaba failinime

#### main() funktsioon
**Eesmärk:** Ühendab 3 klassi kokku ja jooksutab salvestamise tsüklit

**Töövoog:**

1. **Setup ja kasutaja sisend:**
   - Loo OUTPUT_FOLDER kui puudub
   - Küsi kasutajalt: "How many stories to record? (Enter number or press Enter for all):"
   - Kui tühi → `max_stories = None` (kõik lood)
   - Kui number → `max_stories = int(user_input)`

2. **Initsialiseerige komponendid:**
   - CSVManager laeb CSV
   - BrowserController käivitab driveri
   - AudioRecorder valmis salvestama
   - Statistics tracking: `recorded_count`, `skipped_count`, `failed_count`, `start_time`, `total_duration`

3. **Peamine tsükkel:**
   ```python
   while True:
       # Check limit
       if max_stories and recorded_count >= max_stories:
           break

       story = csv_manager.find_next_original_unsaved()
       if story is None:
           break

       print(f"Salvestan: {story['title']}")

       # Open in new tab (defensive, 3× retry)
       if not browser.open_story_in_new_tab(story['url']):
           skipped_count += 1
           continue

       if not browser.click_play():
           browser.close_story_tab()
           skipped_count += 1
           continue

       file_path = recorder.record(story['title'], story['duration_seconds'])
       if not file_path:
           browser.close_story_tab()
           skipped_count += 1
           continue

       csv_manager.mark_as_saved(story['url'])
       csv_manager.save()

       # Close tab before next iteration
       browser.close_story_tab()
       recorded_count += 1
   ```

4. **Lõpetamine (finally block):**
   - Sulge browser
   - Salvesta CSV viimane kord
   - Prindi statistika:
     - Successfully recorded (count)
     - Skipped stories (count)
     - Failed verification (count)
     - Total audio duration
     - Session time

---

## Koodipõhimõtted

Kõik skriptid järgivad järgmisi põhimõtteid:

### MVP (Minimum Viable Product)
- Kõige lihtsam töötav lahendus
- Ei lisa mittevajalikke funktsioone
- Iga funktsionaalsus enne testimist kinnitatud

### DRY (Don't Repeat Yourself)
- Korduvat koodi ei kirjutata uuesti
- Ühine loogika helper funktsioonides
- Single source of truth

### Single Responsibility
- Iga funktsioon/klass teeb AINULT ühte asja
- Palju väikeseid funktsioone > üks suur funktsioon
- Helper funktsioonid konkreetseteks ülesanneteks

### ADHD-sõbralik kood
- Väikesed, hõlpsalt mõistetavad tükid
- Selged, kirjeldavad nimed (self-explanatory)
- Ei pea tervet faili pähe õppima
- Iga funktsioon on iseseisev moodul

### Reusable
- Funktsioonid korduvkasutatavad
- Sama helper saab kasutada programmi eri osades
- Modulaarne struktuur

### Näide:
```python
# HALB - pikk, mitut asja korraga
def process_story():
    # Read CSV
    # Find story
    # Open browser
    # Record audio
    # Save file
    # Update CSV
    pass

# HEA - väikesed, konkreetsed
def read_csv():
    pass

def find_next_story():
    pass

def open_browser():
    pass

def record_audio():
    pass
```

---

## Autorid

Loodud 2025. aasta oktoobris koos Claude Code'iga.

**Eesmärk:** Automaatselt alla laadida ja katalogiseerida kõik Vikerraadio õhtujutud lastele.
