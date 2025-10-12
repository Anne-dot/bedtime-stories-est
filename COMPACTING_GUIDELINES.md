# Compacting Guidelines - Kuidas meiega töötada

## Töökäik uue koodi kirjutamisel

### 1. BIG PICTURE ENNE DETAILE
- Alustame ALATI big picture'ist
- Iga klassi jaoks: **Eesmärk, Sisend, Väljund**
- Maksimaalselt 29 rida korraga (mahub ekraanile)
- Üks klass korraga, ei rutta edasi

### 2. ARUTELU ENNE KOODI
- **MITTE KUNAGI** kirjuta koodi enne arutelu
- Näita ENNE alternatiive (plussid/miinused)
- Kasutaja otsustab, mida kasutada
- Kasutaja on BOSS - tema kinnitab otsused

### 3. MEETOD MEETODI HAAVAL
- Üks meetod korraga
- Arutame läbi: mis see teeb, miks, kuidas
- Näitan koodi → kasutaja kinnitab → kirjutan
- EI KUNAGI kirjuta mitut meetodit korraga ilma kinnituseta

### 4. SELGITA INIMKEELES
- Kui kasutaja küsib "mis see teeb", siis samm-sammult inimkeeles
- Ei tehnilisi termineid kui pole vaja
- ADHD-friendly: lühidalt, konkreetselt

### 5. KONTROLLI TEGELIKKUST
- Kui kasutan eeldusi, küsin kasutajalt kinnitust
- Vaatan tegelikke faile, ei aja oletusi
- Kui midagi on ebaselge, KÜSIN enne

## Kasutaja põhimõtted (OLULINE!)

### MVP (Minimum Viable Product)
- Kõige lihtsam töötav lahendus
- Ei lisa mittevajalikke funktsioone
- Komplekssus tuleb ainult kui vaja

### DRY (Don't Repeat Yourself)
- Ei korda koodi
- Helper funktsioonid korduvale loogikale
- Single source of truth

### Single Responsibility
- Iga funktsioon teeb AINULT ühte asja
- Palju väikeseid funktsioone > üks suur
- Helper funktsioonid konkreetseteks ülesanneteks

### ADHD-sõbralik
- Väikesed, hõlpsalt mõistetavad tükid
- Selged, kirjeldavad nimed (self-explanatory)
- Ei pea tervet faili pähe õppima
- Iga funktsioon on iseseisev moodul

### KISS (Keep It Simple, Stupid)
- Lihtne on parem kui keeruline
- Globaalsed konstantid faili alguses (nähtav kohe)
- Ei üle-inseneeri

### Reusable
- Funktsioonid korduvkasutatavad
- Sama helper saab kasutada programmi eri osades

## Kommunikatsioon

### MIDA TEHA:
✓ Küsi alternatiive (plussid/miinused)
✓ **Kui kasutaja tahab alternatiive võrrelda: näita KÕRVUTI TULPADES**
✓ Selgita samm-sammult kui küsitakse
✓ Näita koodi ENNE kirjutamist
✓ Oota kinnitust "jah" või "kirjuta"
✓ Maksimaalselt 29 rida korraga
✓ Üks klass/meetod korraga
✓ Kontrolli tegelikke faile
✓ **Kasutaja töötab manual approval reziimis** - saab ise sudo käske käivitada
  - Näide: `sudo apt install python3-mutagen` - kasutaja käivitab ise
  - Ära rutta alternatiivi juurde, anna kasutajale võimalus ise käivitada
✓ **KASUTAJA KÄIVITAB ALATI TESTE JA SKRIPTE ISE**
  - EI OLE: "Käivitan testi", "Testime nüüd", "Panen käima"
  - ON: "Palun käivita test", "Kopeeri mulle tulemus", "Anna teada kui valmis"
  - Kasutaja kopeerib tulemused sulle - sina EI käivita kunagi ise
✓ **ALATI tuleta meelde dokumentatsiooni uuendamist pärast koodi muudatusi**
  - Kui lisad funktsionaalsust → täienda README.md
  - Kui muudad käitumist → täienda dokumentatsiooni
  - Küsi kasutajalt: "Kas täiendan dokumentatsiooni?"

### MIDA MITTE TEHA:
✗ EI kirjuta koodi enne kinnitust
✗ EI rutta edasi järgmise klassiga
✗ EI tee oletusi - küsi!
✗ EI näita rohkem kui 29 rida korraga
✗ EI lisa "kasulikke" funktsioone ilma küsimata
✗ EI üle-inseneeri lahendust

## Näide töövoog (CSVManager klassi loomine)

1. **Big picture:**
   - "CSVManager eesmärk: haldab CSV andmeid"
   - "Sisend: CSV path"
   - "Väljund: Story dict või None"
   - Kasutaja kinnitab: "jah"

2. **Esimene meetod `__init__`:**
   - Näitan 2 varianti (load kohe vs load eraldi)
   - Plussid/miinused
   - Kasutaja otsustab: "paneme loadi siia"
   - Kirjutan täpselt nii

3. **Teine meetod `load()`:**
   - Arutame: kas helper vaja?
   - Kasutaja: "teeme helperi"
   - Näitan koodi
   - Kasutaja: "jah"
   - Kirjutan

4. **Helper `_read_csv_file()`:**
   - Küsimus: "kas url on unikaalne?"
   - Kasutaja kinnitab
   - Küsimus: "encoding?"
   - Kasutaja: "UTF-8"
   - Kirjutan

5. **Kontrolli tegelikkust:**
   - "Kas CSV-s on tühje ridu?" → Vaatan faili
   - Leian 7 rida ilma kestuseta
   - Panen TODO.md kirja
   - Jätkame

## Failid, mida lugeda enne töö jätkamist

1. **README.md** - projekt ülevaade, koodipõhimõtted, arhitektuur
2. **TODO.md** - mis on tehtud, mis tuleb teha
3. **record_stories.py** - praegune kood (CSVManager valmis)

## Olemasolev kood (seisuga compact)

- ✅ **CSVManager klass** - täielikult valmis
  - `__init__()` - init ja load
  - `load()` - laeb CSV mällu
  - `_read_csv_file()` - helper
  - `find_next_original_unsaved()` - leiab järgmise loo
  - `_is_ready_to_record()` - kontrollib tingimusi
  - `mark_as_saved()` - märgib salvestatuks (kontrollib faili)
  - `save()` - salvestab CSV backupiga
  - `_create_backup()` - helper
  - `_write_csv_file()` - helper

- ⏳ **BrowserController klass** - järgmine (pole alustatud)
- ⏳ **AudioRecorder klass** - veel tegemata
- ⏳ **main() funktsioon** - veel tegemata

## Kompaktimise järel

Kui compacting on tehtud:
1. Loe README.md
2. Loe TODO.md
3. Loe see fail (COMPACTING_GUIDELINES.md)
4. Vaata record_stories.py (mis on juba valmis)
5. Küsi kasutajalt: "Kas jätkame BrowserController klassiga?"
6. Järgi täpselt neid guideline'e!
