# Kasutamise Juhend - download_stories.py

## Kiire Alustamine

### 1. Käivitamine

```bash
cd /home/d0021/Automation/ohtujutt-vikerraadio
python3 download_stories.py
```

**Küsimus:** "How many stories to download?"
- **Enter** → laadib KÕIK salvestamata lood (2163 tk)
- **Number** → laadib N lugu (testimiseks)

### 2. Mida Ekraanil Näed

```
Starting to download stories...
Total unsaved stories in catalog: 2163
Target: all unsaved stories

============================================================
[1/2163] Õhtujutt. Okasroosike
============================================================
Opening: https://vikerraadio.err.ee/...
  ✓ Manifest URL: https://vod.err.ee/dash/...
Downloading with yt-dlp...
[dashsegments] Total fragments: 62
[download] 100% of 9.51MiB in 00:00:16 at 582.81KiB/s
  ✓ Downloaded: Õhtujutt/Õhtujutt. Okasroosike.mp3
  ✓ Size: 9.40 MB
  ✓ Time: 22.1s
  ✓ Downloaded successfully
CSV saved: ohtujutt_catalog.csv

============================================================
[2/2163] Õhtujutt lastele. Mullitamaa suvi, 5
Progress: 1 downloaded, 0 skipped, 0 failed
ETA: 20.3h remaining (avg 34s/story)
============================================================
...
```

### 3. Mida Jälgida

**✅ Normaalne käitumine:**
- Progress: [X/2163] kasvab
- ETA: 19-20h (päeval) või 16-17h (öösel)
- Download kiirus: 580-624 KiB/s
- "✓ Downloaded successfully" iga loo järel
- Postprocessing error: **IGNOREERI** (harmless, fail on OK)

**⚠️ Hoiatused:**
```
⚠ Duration mismatch: expected 439s, got 4s
✗ File rejected due to duration mismatch
⚠ Retry attempt 1/2...
```
- Automaatne retry (kuni 3x)
- Kustutab katkise faili
- Proovib uuesti

**❌ Errorid:**
```
✗ Could not extract manifest URL
✗ Download failed
✗ Failed after 3 attempts, skipping
```
- Skip'ib loo
- Jätkab järgmisega
- Lõpus näitab statistikas

**🛑 Võrguühenduse kaitse:**
```
⚠ WARNING: 5 consecutive failures detected!
⚠ This usually indicates a network problem.
⚠ Please check your internet connection and restart the script.
```
- Peatub automaatselt 5 järjestikuse ebaõnnestumise järel
- Kaitseb tunde asjata töötamise eest kui võrk kadunud
- Kontrolli internetiühendust ja käivita uuesti

---

## Pauside Tegemine

### Graceful Shutdown (Ctrl+C)

**Vajuta:** `Ctrl+C`

**Mis juhtub:**
1. Skript kuulab järgmist võimalust
2. Lõpetab **käimasoleva loo** allalaadimise
3. Salvestab CSV (saved=1 märgitud)
4. Näitab statistikat
5. Sulgeb browseri
6. Väljub

**MITTE:**
- ❌ Ära vajuta Ctrl+C mitu korda (ootab rahulikult)
- ❌ Ära sulge terminali enne kui "Download session complete!" ilmub

### Jätkamine Pärast Pausi

```bash
python3 download_stories.py
# Sisesta: Enter
```

- Skript leiab CSV-st järgmise `saved=0` loo
- Jätkab sealt, kus pooleli jäi
- **EI ALUSTA ALGUSEST!**

---

## Pärast Lõppu

### 1. Kontrolli Statistikat

Skript prindib automaatselt:

```
============================================================
Download session complete!
Successfully downloaded: 2163 stories
Skipped: 15 stories
Failed verification: 2 stories
Total audio duration: 1234567s (342h)
Session time: 71280s (19h)
============================================================
```

### 2. Kontrolli Quality Control Logi

```bash
cat duration_mismatch.txt
```

**Kui fail on tühi:**
- ✅ Kõik failid olid õiges pikkuses

**Kui on kirjeid:**
```
Õhtujutt. Hunt ja seitse kitsetalle: expected 439s, got 4s (diff: 435s)
```
- Need lood ebaõnnestusid 3x
- Märgitud `saved=0` (saad uuesti proovida)

### 3. Kontrolli Salvestatud Faile

```bash
ls -lh Õhtujutt/ | tail -10  # Viimased 10 faili
du -sh Õhtujutt/              # Kokku suurus
```

**Eeldatav:**
- 2163 MP3 faili
- Kokku ~20-25 GB

### 4. Vaata CSV Backup'it

```bash
ls -lh ohtujutt_catalog.csv*
```

```
ohtujutt_catalog.csv         # Uusim
ohtujutt_catalog.csv.backup  # Eelmine (enne viimast salvestust)
```

---

## Probleemide Lahendamine

### "Could not extract manifest URL" (palju kordi)

**Põhjus:** ERR.ee leht ei laadinud korrektselt

**Lahendus:**
- Retry töötab automaatselt (3x)
- Kui ikkagi ebaõnnestub → skip
- Proovi neid lugusid hiljem käsitsi

### "Download failed" (palju kordi)

**Põhjus 1:** Internetiühendus katkes
**Lahendus:**
- Skript peatub automaatselt pärast 5 järjestikust ebaõnnestumist
- Kontrolli võrguühendust
- Käivita uuesti: `python3 download_stories.py` (jätkab sealt)

**Põhjus 2:** ERR.ee server aeglane/koormus
**Lahendus:** Öösel kiirem - proovi siis

### "Rate limiting" / 403 Forbidden (ei tohiks juhtuda)

**Põhjus:** ERR.ee blokeerib liiga palju päringuid

**Lahendus:**
- Pausi 10-15 min
- Jätka (skript jätkab sealt)
- Kui kordub → anna teada (vajab rate limiting'ut)

### Skript hangub / ei liigu

**Kontrolli:**
```bash
ps aux | grep python3  # Kas töötab?
```

**Lahendus:**
- Oodata (yt-dlp võib olla aeglane)
- Ctrl+C (graceful shutdown)
- Vaata viimast CSV salvestust

---

## Näpunäited

### ✅ TEES:
- **Käivita öösel** (kiirem võrk, 16h vs 20h)
- **Jälgi ETA-d** esimeste 10 loo järel (stabiliseerub)
- **Lase jooksma** - ei vaja järelevalvet
- **Kontrolli hommikul** - peaks läbi olema

### ❌ ÄRA TEES:
- Ära välju Ctrl+C mitu korda (ootab kenasti)
- Ära kustuta CSV-d pooleli olles
- Ära muuda faile `Õhtujutt/` kaustas pooleli olles
- Ära välju sudo-ga (pole vaja)

---

## Oodatavad Tulemused

### Päeval (14:00-22:00)
- **Aeg:** 19-20h
- **Kiirus:** 580-620 KiB/s
- **Per lugu:** 33-35s

### Öösel (22:00-06:00)
- **Aeg:** 16-17h
- **Kiirus:** 620-700 KiB/s (parem!)
- **Per lugu:** 27-30s

### Kokku
- **Failid:** 2163 MP3 (kui kõik õnnestuvad)
- **Suurus:** ~20-25 GB
- **Quality:** 128kbps AAC, täpne kestus
- **Kiirusevõit:** 18-22x kiirem kui monitor recording

---

## Abi Vajad?

1. **Vaata logi faile:**
   - `duration_mismatch.txt` - kestuse erinevused
   - Ekraani output (kopeeri error)

2. **Kontrolli CSV-d:**
   ```bash
   grep ",0,original" ohtujutt_catalog.csv | wc -l  # Mitu veel laadimata
   ```

3. **Käivita test:**
   ```bash
   python3 download_stories.py
   # Sisesta: 1
   # Kontrolli kas üks lugu õnnestub
   ```

---

**Loodud:** 2025-10-12
**Skript:** download_stories.py v1.0
**Dokumentatsioon:** README.md, MANIFEST_DOWNLOAD_ANALYSIS.md
