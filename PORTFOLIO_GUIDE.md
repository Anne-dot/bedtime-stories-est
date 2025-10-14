# Portfolio Guide: Bedtime Stories Automation Project

## Projekt Tööintervjuuks

### 🎯 Projekti Kokkuvõte

**Probleem:**
- ERR.ee Vikerraadio on avaldanud ~2000 õhtujuttu lastele
- Failid on halvasti organiseeritud, puuduvad sarjad, palju duplikaate
- Käsitsi organiseerimine võtaks kuid aega

**Lahendus:**
- Automatiseeritud allalaadimise ja organiseerimise süsteem
- Intelligentne duplikaatide tuvastamine
- Sarjade automaatne grupeerimine
- Kvaliteedikontroll ja metaandmete puhastamine

**Tulemus:**
- ~1822 lugu kvaliteetselt organiseeritud
- 81 sarja kausta grupeeritud
- ~78 duplikaati tuvastatud ja eemaldatud
- 2-3 aastat sisu perekonna tarbeks

---

## 💼 Mida Tööintervjuul Näidata

### Tehnilised Oskused

1. **Automatiseerimine & Scripting**
   - Python skriptid failihalduseks
   - Fuzzy string matching (difflib.SequenceMatcher)
   - Batch processing suurte andmehulkade jaoks

2. **Probleemi Lahendamine**
   - Keerulise probleemi lihtsateks sammudeks jagamine
   - Iteratiivne lähenemine (käsitsi → automatiseeritud)
   - Edge case'ide käsitlemine (eri versioonid vs duplikaadid)

3. **Andmete Puhastamine**
   - Duplikaatide tuvastamine 90%+ täpsusega
   - Metaandmete normaliseerimine
   - Kvaliteedikontroll (kestuse võrdlus)

4. **Git & Versioonikontroll**
   - Struktureeritud commitid
   - Progress tracking
   - Dokumentatsioon

5. **Projekti Juhtimine**
   - TODO tracking
   - Progress updates
   - Järgmiste sammude planeerimine

---

## 🗣️ Kuidas Esitada

### Raamistik

**"Mul oli isiklik vajadus..."**
- Lapse õhtuseks unejutustamiseks
- ERR.ee arhiiv on halvasti organiseeritud
- Otsustasin probleemi tehniliselt lahendada

**"Lõin automatiseeritud lahenduse..."**
- Näita koodi näiteid (duplicate detection, folder organization)
- Rõhuta tehnilist lähenemist
- Maini väljakutseid ja lahendusi

**"Tulemus on..."**
- Konkret numbrid (1822 lugu, 81 kausta, 78 duplikaati)
- Ajakulu (käsitsi: kuud vs automatiseeritud: päevad)
- Kvaliteet (parem kui originaal ERR.ee arhiivist)

---

## 📊 Võtmenumbrid

- **2330** faili alguses allalaaditud
- **81** sarja kausta loodud
- **543** lugu kaustades
- **1279** üksiklugu
- **~78** duplikaati eemaldatud
- **90%+** duplikaatide tuvastamise täpsus
- **12 päeva** projektile kulunud aega
- **2-3 aastat** sisu (korduste ja lemmikutega)

---

## 🔧 Tehnilised Lahendused

### 1. Duplikaatide Tuvastamine

```python
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# 90%+ similarity = likely duplicate
# 80-90% = needs review
# <80% = different files
```

**Väljakutsed:**
- Eristamine: tõelised duplikaadid vs erinevad versioonid
- Näide: "Kuldnokk" vs "Kuldnokad" (eri lood, mitte duplikaadid)

**Lahendus:**
- Manuaalne ülevaatus 90%+ sarnasuste puhul
- "Eri versioonide" nimekiri false positive'te vältimiseks
- Iteratiivne töövoog: automaatne filtreerimine → inimese otsus

### 2. Sarjade Organiseerimine

**Väljakutsed:**
- Episoodinumbrite tuvastamine (erinev formaat)
- Sarja nime ekstraheerimine
- Õige failiarvu valideerimine

**Lahendus:**
- JSON-põhine progress tracking
- Käsitsi valideeritud sarjade nimekiri
- Automaatne failide grupeerimine

### 3. Kvaliteedikontroll

- Failikestuste võrdlus duplikaatide puhul
- Metaandmete normaliseerimine
- Sarjade täielikkuse kontrollimine

---

## ✅ Mida Rõhutada

1. **Praktiline probleem → Tehniline lahendus**
   - Reaalse vajaduse lahendamine
   - End-to-end projekt

2. **Automatiseerimine**
   - Käsitsi töö optimeerimine
   - Ajakulu vähendamine kuudelt päevadele

3. **Kvaliteet**
   - Parem kui originaal (duplikaatideta, organiseeritud)
   - Inimese + masina kombinatsioon

4. **Dokumentatsioon**
   - Progress updates
   - Compacting guidelines
   - Selge projektistruktuur

5. **Iteratiivne Töövoog**
   - Start simple → optimize
   - Learn from errors
   - Continuous improvement

---

## ⚠️ Mida MITTE Mainida

- ❌ Autoriõigused
- ❌ "Mul ei tohiks neid olla"
- ❌ Levitamine või müük
- ❌ GitHub'i public repo

---

## ✨ Võtmesõnum

> "Mul oli probleem: 2000 halvasasti organiseeritud audiolugu. Lõin automatiseeritud lahenduse, mis tuvastab duplikaate 90%+ täpsusega ja organiseerib failid sarjadesse. Tulemus: parem kvaliteet kui originaalal, kuud käsitööd optimeeritud päevadeks."

---

## 📁 Projektifailid Näitamiseks

**Kood:**
- Duplicate detection skript
- Folder organization logic
- Progress tracking system

**Dokumentatsioon:**
- `COMPACTING_GUIDELINES.md` - töövoo selgitus
- `progress_updates/` - päevikud
- `TODO.md` - projekti planeerimine

**Tulemused:**
- `different_versions_not_duplicates.txt` - kvaliteedikontroll
- `ohtujutt_catalog.csv` - sarjade nimekiri
- Struktureeritud kaustade hierarhia

---

**Loodud:** 2025-10-15
**Eesmärk:** Tööintervjuude ettevalmistus
**Kontekst:** Privaatne demo, mitte avalik jagamine
