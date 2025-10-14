# Compacting Guidelines - Kuidas meiega töötada

## 🚀 UUE SESSIOONI ALUSTAMISEKS

**ALUSTA ALATI SIIT:**
👉 **Loe [NEXT_SESSION.md](./NEXT_SESSION.md) faili**

NEXT_SESSION.md sisaldab:
- Hetkeseisund (mis on valmis)
- Linke kõigile olulistele failidele (progress updates, TODO, README)
- Järgmised sammud
- Kiire konteksti taastamine

**Pärast NEXT_SESSION.md lugemist jätka nende juhistega allpool.**

---

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

### Best Practices
- Järgi üldtunnustatud koodi kirjutamise häid tavasid
- Kasuta ametlikku dokumentatsiooni kui kahtled
- Vaata teekide/raamistike ametlikku dokumentatsiooni
- Järgi keele/platvormi standardeid ja konventsioone

## 📏 Response Format - ADHD-sõbralik (KOHUSTUSLIK!)

**SEE ON KRIITILISE TÄHTSUSEGA! Kasutajal on ADHD ja need reeglid on MITTE-LÄBIRÄÄGITAVAD!**

### Maksimaalne teksti pikkus vastuse kohta

**REEGEL: Näita maksimaalselt 29 rida teksti/koodi korraga**

**Miks see on oluline:**
- Kasutaja VIHKAB scrollimist
- Kaotab mõttelõnga kui sisu ei mahu ekraanile
- ADHD teeb VÄGA raskeks fookuse hoidmise üle scrollimise
- See EI OLE valikuline - see on vajalik efektiivseks suhtluseks

### Kuidas käsitleda pikka sisu

❌ **MITTE KUNAGI ära tee nii:**
- Kokku võtta või lühendada sisu
- Vahele jätta sektsioone
- Tihendata infot et mahuks

✅ **ALATI tee nii:**
- Näita sisu osade kaupa (max 29 rida iga)
- Esita täielik sisu, lihtsalt jaga hallatavateks tükkideks
- Nummerda osad kui kasulik (nt "OSA 1/3")
- Küsi "Kas jätkan järgmise osaga?" osade vahel
- Anna kasutajale aega kommenteerida iga osa järel

### Erand: Võrdlustabelid

Kui kasutaja palub võrrelda variante (plussid/miinused):
- ✅ Võid kasutada 2-tulpa tabeleid
- ❌ Aga ÄRA tee teksti liiga tihedaks/lühendatuks
- ✅ Kasuta täislauseid ja näiteid (nagu näitaksid teksti järjest)
- Eesmärk on loetavus, mitte lühidus

### Näited

**❌ VALE vastus (liiga pikk):**
```
Siin on terve 50-realine konfiguratsioonifail...
[tohutu tekstimüür mis nõuab scrollimist]
```

**✅ ÕIGE vastus:**
```
Siin on konfiguratsioonifail (OSA 1/2 - esimesed 25 rida):

[25 rida sisu]

Kas jätkan ülejäänuga?
```

---

**SEE ON SELGE JA KINDEL OOTUS!** Nende reeglite järgimine on vajalik produktiivseks koostööks.

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
✓ **Pikemad selgitused ja mitmeosalised vastused:**
  - Näita **ÜKS OSA korraga** (max ~29 rida, mis mahub ekraanile)
  - Anna kasutajale aega kommenteerida
  - Oota kinnitust: "jah", "jätka", "edasi" VÕI küsimust
  - **EI liigu edasi enne kui kasutaja ütleb**
  - EI tee vähendatud infoga tabeleid kui info on pikk
  - EI paku kõike korraga ekraanile

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

## 📚 Failid, mida lugeda enne töö jätkamist

**ALATI alusta [NEXT_SESSION.md](./NEXT_SESSION.md) failist!**

NEXT_SESSION.md juhendab sind lugema järgmised failid:
1. 📅 [progress_updates/](./progress_updates/) - Viimane progress update (vt kuupäeva)
2. ✅ [TODO.md](./TODO.md) - Järgmised sammud detailselt
3. 📖 [README.md](./README.md) - Projekti ülevaade ja dokumentatsioon
4. 🎯 [COMPACTING_GUIDELINES.md](./COMPACTING_GUIDELINES.md) (see fail) - Töövoo põhimõtted

## Uue sessiooni alustamine

1. ✅ Loe [NEXT_SESSION.md](./NEXT_SESSION.md)
2. ✅ Järgi linkide järjekorda NEXT_SESSION.md failis
3. ✅ Tule tagasi siia ja järgi allpool olevaid töövoo põhimõtteid
4. ✅ Küsi kasutajalt kinnitust enne alustamist
