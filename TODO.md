# TODO - Õhtujutt Automation

## Parandamist vajavad andmed

### CSV kirjed ilma kestuseta
- [ ] **Leia ja täienda lood, kus duration_seconds on tühi**
  - Probleem: 7 lugu CSV-s ei ole kestust
  - Näide: "Õhtujutt. Kõhu mäss, 2. Silmad vajavad puhkust" (index 145)
  - Põhjus: collect_story_info.py ei suutnud kestust lugeda
  - Lahendus: Käsitsi käi läbi või paranda collect_story_info.py retry loogikaga
  - Prioriteet: KESKMINE (need 7 lugu jäävad praegu vahele)

### Excluded lood ilma pealkirjadeta
- [ ] **Uurista excluded lugude olukorda**
  - Probleem: ~160 lugu CSV-s on märgitud `duplicate_status='excluded'`
  - Nende lugude pealkirjad puuduvad (tühi või placeholder)
  - Küsimus: Kas pealkiri on lehel mujal kuskil leitav?
  - Lahendus: Kontrolli ERR.ee lehte, kas metadata on saadaval
  - Prioriteet: MADAL (2167 lugu on piisavalt, see on üle aasta materjali)

## Optimeerimised

### record_stories.py
- [ ] **Salvestamise progressi näitamine**
  - Praegu: FFmpeg salvestab vaikselt, kasutaja ei tea mis toimub
  - Deprecated näitas progressi iga 10 sekundi kaupa
  - Lahendus: Lisa progressi jälgimine salvestamise ajal (nt iga 10s või progress bar)
  - Prioriteet: KESKMINE (kasutajakogemus)

- [x] **Faili ülekirjutamise probleem (duplikaadid)**
  - ✅ Lisatud `_get_unique_filename()` helper AudioRecorder klassi
  - ✅ Kontrollib faili olemasolu enne salvestamist
  - ✅ Lisab automaatselt suffix (_2, _3, ...) kui fail eksisteerib
  - ✅ README.md uuendatud

- [ ] **Graceful shutdown (Ctrl+C)**
  - Probleem: Kui kasutaja katkestab, jääb browser lahti ja CSV ei salvesta
  - Soov: Vajuta klahvi → lõpeta käimasolev lugu → sulge browser kenasti
  - Lahendus: Signal handler (SIGINT), lõpeta tsükkel pärast käimasolevat lugu
  - Prioriteet: KESKMINE (kasutajakogemus)

- [ ] **Duplikaatide kontrolli skript**
  - Probleem: CSV-s võib olla sama pealkiri, aga erinev kestus
  - Soov: Käsitsi märgi käsk faili nimele (nt "pikem", "lühem")
  - Eesmärk: Mõlemad failid salvestatakse (ei kirjuta üle), saab hiljem manuaalselt võrrelda
  - Lahendus: Skript, mis leiab duplikaadid ja küsib kasutajalt märget
  - Prioriteet: MADAL (harv juhtum)

### collect_story_info.py
- [ ] **CSV salvestamine ainult kui muudatusi on**
  - Praegu: salvestab CSV pärast iga lehekülge, isegi kui kõik lood on SKIPPED
  - Probleem: 11 lehekülge × tarbetu salvestus = ~30-40s raiskamine
  - Lahendus: Track `page_updated` flag, salvesta ainult kui `True`
  - Prioriteet: MADAL (toimib, lihtsalt ebatõhus)

## Manifest Download - VALMIS ✓

### download_stories.py implementeerimine
- [x] **Manifest download meetodi uurimine ja testimine**
  - ✅ DASH manifest meetod töötab
  - ✅ 19x kiirem kui monitor recording (20h vs 390h)
  - ✅ Test 1 lugu: 100% success
  - ✅ Test 3 lugu: 100% success
  - ✅ Dokumentatsioon: MANIFEST_DOWNLOAD_ANALYSIS.md

- [x] **CSV moodul (csv_manager.py)**
  - ✅ Eraldi moodul (DRY - kasutab nii record kui download)
  - ✅ Quality control: duration check (mutagen)
  - ✅ Return False kui duration mismatch > 10s
  - ✅ Automaatne CSV backup

- [x] **Manifest download moodul (manifest_downloader.py)**
  - ✅ extract_manifest_url() - Selenium + mediaId
  - ✅ download_with_ytdlp() - DASH download
  - ✅ verify_audio() - FFmpeg duration check
  - ✅ Progress tracking support

- [x] **download_stories.py põhiskript**
  - ✅ CSV integratsioon
  - ✅ 3x retry loogika
  - ✅ Graceful shutdown (Ctrl+C)
  - ✅ Per-lugu progress (yt-dlp fragments)
  - ✅ Session progress (ETA, avg speed, statistics)
  - ✅ Broken file cleanup
  - ✅ Võrguühenduse kaitse (5 consecutive failures → stop)

- [x] **Dokumentatsioon**
  - ✅ README.md uuendatud
  - ✅ TODO.md uuendatud
  - ✅ MANIFEST_DOWNLOAD_ANALYSIS.md täiendatud

## Tuleviku Täiendused

- [ ] **Rate limiting download_stories.py-s**
  - Kui ERR.ee blokeerib (403 Forbidden)
  - Lisa 1-2s delay requestide vahel
  - Prioriteet: MADAL (praegu ei bloki)

- [ ] Parallelsete lindistuste tugi
- [ ] Web UI kataloogi vaatamiseks
- [ ] Automaatne uute lugude tuvastamine (cron job)
- [ ] Metaandmete lisamine MP3 failidele (ID3 tags)

## Järgmised sammud (PÄRAST ALLALAADIMIST)

### 1. Failide reorganiseerimine
- [ ] **Loo professionaalne kaustade struktuur**
  - `scripts/` - peamised skriptid
  - `scripts/utils/` - utility moodulid
  - `docs/` - dokumentatsioon
  - Prioriteet: KÕRGE

- [ ] **Liiguta failid õigetesse kohtadesse**
  - `scripts/download_stories.py`
  - `scripts/record_stories.py`
  - `scripts/cleanup_temp_files.py`
  - `scripts/trim_silence.py`
  - `scripts/utils/csv_manager.py`
  - `scripts/utils/manifest_downloader.py`
  - Lisa `__init__.py` failid

- [ ] **Paranda impordid**
  - `from utils.csv_manager import CSVManager`
  - `from utils.manifest_downloader import ...`
  - Testi, et kõik töötab

- [ ] **Liiguta dokumentatsioon**
  - `docs/TODO.md`
  - `docs/USAGE.md`
  - `docs/COMPACTING_GUIDELINES.md`
  - `docs/MANIFEST_DOWNLOAD_ANALYSIS.md`

### 2. Seeriate organiseerimine (UUS!)
- [ ] **Loo organize_series.py skript**
  - Leia CSV-st lood, mis lõpevad `, \d+` (nt "Sirli, Siim ja saladused, 1")
  - Erasta sarja nimi (osa enne viimast koma)
  - Loo kaust `Õhtujutt/[sarja_nimi]/`
  - Liiguta kõik sarja osad õigesse kausta
  - Üksikud lood jäävad `Õhtujutt/` juurkausta
  - Prioriteet: KÕRGE

- [ ] **Testi mõnel lugudel**
  - Kontrolli, et failid liiguvad õigesti
  - Kontrolli, et üksikud lood jäävad paika

- [ ] **Jookse läbi kõikidel lugudel**
  - `python3 organize_series.py`

### 3. Dokumentatsioon ja Git
- [ ] **Uuenda README.md**
  - Uus failide struktuur
  - Seeriate organiseerimise kirjeldus
  - Kasutamisjuhendid

- [ ] **Git commit ja push**
  - Commit: "Reorganize project structure and add series organization"
  - Push to GitHub

### record_stories.py refaktoreerimine
- [x] Kasuta CSV-st täpseid kestusi (`duration_seconds`)
- [x] Salvesta täpselt nii kaua kui kestus näitab (+2s buffer)
- [x] MVP + DRY + small functions
- [x] **CSV võrdle faili tegelikku pikkust tabelis oleva infoga**
  - ✅ CSVManager.mark_as_saved() kontrollib faili kestust (mutagen)
  - ✅ Kui erinevus > 10s, logi `duration_mismatch.txt`
  - ✅ Märgib saved='1' ainult kui duration OK (uuendatud download jaoks)

## Valmis ✓

- ✅ Angular scope probleem lahendatud (page 2+ töötab)
- ✅ Indekseerimine jätkub viimasest numbrist
- ✅ CSV salvestamine iga 100 loo järel (crash protection)
- ✅ Pealkiri võrdlus "VANEMAD" nupu jaoks
- ✅ Page number eemaldatud CSV-st (mõttetu info)
