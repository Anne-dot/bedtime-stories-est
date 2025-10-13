# Download Behavior Use Cases

Allalaadimise käitumine erinevate stsenaariumite korral `download_stories.py` skriptis.

---

## Praegune probleem

**Hetkel (enne muudatusi):**
- 5 järjestikust ebaõnnestumist → skript peatub KOHE
- Ei erita ebaõnnestumise põhjuseid
- Ei proovi automaatselt taastuda
- Kasutaja peab käsitsi monitoorima ja restartima

---

## Eesmärk

**Intelligentne allalaadimise käitumine:**

1. **Happy path:** Kõik lood laetakse alla sujuvalt

2. **Eristab ebaõnnestumisi:** lugu vs server vs võrk vs rate limit

3. **Käsitleb sobivalt:** skip vs exponential backoff

4. **Automaatne taastumine:** <15min → ise, >15min → kasutaja

5. **Kasutajasõbralik:** selge feedback, Ctrl+C, progress säilib

---

## USE CASE 0: Happy Path

### Stsenaarium
Kõik töötab normaalselt, probleeme pole.

### Mis juhtub

1. Lugu #1 → manifest URL → download → verify → ✓ success
2. Lugu #2 → manifest URL → download → verify → ✓ success
3. Lugu #3 → manifest URL → download → verify → ✓ success
...
4. Lugu #1981 → ✓ success
5. "No more stories to download!"
6. Näita statistikat
7. Exit

### Käitumine
- Kõik lood laetakse alla
- consecutive_failures = 0 (reset iga õnnestumise järel)
- Temp failid kustutatakse pärast iga lugu
- CSV uuendatakse pidevalt
- Kasutaja näeb progressi ja ETA-d

### Tulemus
✅ 1981 lugu alla laaditud
✅ ~20h aega kulunud

---

## USE CASE 1: Konkreetse loo probleem

### Stsenaarium
Üks lugu ERR.ee serveris puudu/katkine.
Manifest URL ei eksisteeri või 404.

### Mis juhtub (samm-sammult)

1. **Lugu #47 allalaadimine:**
   - Proovib manifest URL-i ekstraktida
   - **Fail:** Element ei leitud lehel

2. **Retry #1:**
   - Proovib uuesti
   - **Fail:** Ikka ei leia

3. **Retry #2:**
   - Kolmas katse
   - **Fail:** Element tõesti puudub

4. **Tulemus:**
   - "✗ Failed after 3 attempts, skipping"
   - `consecutive_failures += 1` (nüüd = 1)

5. **Lugu #48:**
   - Jätkab KOHE (ei oota)
   - Download õnnestub
   - `consecutive_failures = 0` (reset)

### Käitumine
- ✅ Skip konkreetne lugu (3 retry järel)
- ✅ Jätka KOHE järgmisega
- ❌ EI aktiveeri exponential backoff
- ❌ EI oota

### Põhjendus
Probleemiks on üks konkreetne lugu, mitte süsteem.
Teised lood töötavad → pole mõtet oodata.

### Tulemus
✅ 1980 lugu alla laaditud (1 skipped)
⚠ Lugu #47 jääb vahele (kasutaja saab hiljem käsitsi proovida)
📝 Logitakse `failed_downloads.log`:
   "Lugu #47: Õhtujutt title - manifest_not_found - 3 attempts"

---

## USE CASE 2a: ERR.ee server maas (taastub)

### Stsenaarium
ERR.ee server crashis või maintenance.
KÕIK lood failivad, aga server taastub 1-5min jooksul.

### Mis juhtub (samm-sammult)

1. **5 lugu järjest failib:**
   - Lugu #50-54: timeout (manifest ekstraktimine >30s)
   - `consecutive_failures = 5`

2. **Hoiatus:** "⚠ WARNING: 5 consecutive failures detected!"

3. **Esimene retry (30s):**
   - "⏳ Network issue detected. Waiting 30s before retry 1/5..."
   - Countdown: "⏳ 30s... 20s... 10s..."
   - Proovib test lugu #55
   - **Fail:** ERR server ikka maas
   - "✗ Test download failed, retry 1/5"

4. **Teine retry (60s):**
   - Ootab 60s
   - Proovib test lugu
   - **Fail**

5. **Kolmas retry (120s = 2min):**
   - Ootab 120s
   - **Selle 120s ajal ERR server taastub!**
   - Proovib test lugu
   - **✓ Success!**
   - "✓ Network restored! Resuming downloads..."
   - Test fail kustutatakse

6. **Jätkamine:**
   - `consecutive_failures = 0` (reset)
   - Main loop proovib lugu #55 uuesti (korralikult)
   - Kõik töötab normaalselt edasi

### Käitumine
- ✅ Exponential backoff (30s → 60s → 120s)
- ✅ Automaatne taastumine
- ✅ Jätkab kus pooleli jäi
- ❌ Ei kaota lugusid (test ei salvesta CSV-sse)

### Ajakulu
~5-7min (failures + retries 210s)

### Tulemus
✅ Kõik 1981 lugu alla laaditud
✅ Automaatne taastumine, kasutaja ei pea sekkuma
⏳ ~5-7min lisakulu

---

## USE CASE 2b: ERR.ee server maas (ei taastu kiiresti)

### Stsenaarium
ERR.ee server crashis pikaks ajaks (>15min).

### Mis juhtub - osa 1 (esimesed 5 retry'd)

1. **5 lugu järjest failib:** #50-54 → `consecutive_failures = 5`

2. **Hoiatus:** "⚠ WARNING: 5 consecutive failures detected!"

3. **Exponential backoff (5 proovi):**
   - Retry 1 (30s): ootab → test → fail
   - Retry 2 (60s): ootab → test → fail
   - Retry 3 (120s): ootab → test → fail
   - Retry 4 (240s): ootab → test → fail
   - Retry 5 (480s): ootab → test → fail
   - Kokku: ~15.5min

4. **Diagnoos (pärast 5 faili):**
   - "🔍 Diagnosing issue..."
   - Ping test: `ping -c 1 8.8.8.8`
   - ERR test: HTTP GET `https://err.ee`

5. **Diagnoos tulemus: ERR.ee maas (internet OK)**
   - "⚠ Internet OK, but ERR.ee is down"
   - "🔄 Switching to long-term monitoring (every 10min)"
   - "Press 'q' to quit, 's' to skip and continue"

6. **Pikaajaline kontroll:**
   - Ootab 10min → proovib ERR.ee → fail
   - Ootab 10min → proovib → fail
   - Ootab 10min → proovib → ✓ SUCCESS!
   - "✓ ERR.ee restored! Resuming downloads..."

### Käitumine
- ✅ Exponential backoff (15min)
- ✅ Intelligent diagnoos (ping + ERR test)
- ✅ Pikaajaline monitooring (iga 10min lõputult)
- ✅ Kasutaja saab katkestada: 'q' või 's'
- ✅ Automaatne taastumine

### Ajakulu
~15min (exponential) + 30min (3× 10min) = ~45min

### Tulemus
✅ Kõik 1981 lugu alla laaditud
✅ Ei pea käsitsi restartima
⏳ ~45min lisakulu (sõltub kui kaua ERR maas)
