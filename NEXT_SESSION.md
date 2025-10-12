# 🚀 Järgmiseks Sessiooniks - START HERE

**Projekti nimi:** Vikerraadio Õhtujuttude Automatiseerimine
**GitHub:** https://github.com/Anne-dot/bedtime-stories-est

---

## Kuidas alustada uut sessiooni kontekstiga

### 1. Anna Claude'ile see käsk:

```
Loe NEXT_SESSION.md fail ja jätka projekti ülesannetega.
```

### 2. Claude loeb automaatselt läbi:

**Loe nende linkide järjekorras:**
1. 📅 [progress_updates/2025-10-13_bedtime-stories.md](./progress_updates/2025-10-13_bedtime-stories.md) - Viimane päev tööd
2. ✅ [TODO.md](./TODO.md) - Järgmised sammud detailselt
3. 📖 [README.md](./README.md) - Projekti ülevaade ja kasutamisjuhend
4. 🎯 [COMPACTING_GUIDELINES.md](./COMPACTING_GUIDELINES.md) - Töövoo põhimõtted

**Järgmine ülesanne:** Failide reorganiseerimine + seeriate organiseerimine

---

## Mis on praegu VALMIS

✅ Projekt GitHub'is: https://github.com/Anne-dot/bedtime-stories-est
✅ 5 commiti tehtud
✅ Kõik peamised funktsioonid töötavad:
   - Manifest download (19x kiirem)
   - Quality control (kestuse kontroll)
   - 3x retry loogika
   - Progress tracking (ETA, statistics)
   - Võrguühenduse kaitse (5 consecutive failures → stop)
   - Automaatne temp cleanup (pärast iga lugu)
   - Graceful shutdown (Ctrl+C)

✅ **Allalaadimine POOLELI:**
   - Alustatud: 2025-10-13 õhtul
   - Tempo: ~100 lugu/tunnis (~33s/lugu)
   - Target: 1981 lugu
   - ETA: 2025-10-14 õhtul ~15:00-16:00
   - Quality control töötab: püüab kinni valed failid ja proovib uuesti

---

## Järgmised sammud (pärast allalaadimist)

Vaata täpsed sammud: `TODO.md` failis projekti kaustas.

**Põhisammud:**
1. **Failide reorganiseerimine:**
   - Loo `scripts/` ja `scripts/utils/` struktuur
   - Liiguta failid õigetesse kaustadesse
   - Paranda impordid
   - Testi
   - Loo `docs/` kaust dokumentatsioonile

2. **Seeriate organiseerimine (UUS):**
   - Loo `organize_series.py` skript
   - Leia lood, mis lõpevad `, number` (nt "Sirli, Siim ja saladused, 1")
   - Liiguta seerialood oma kaustadesse (nt `Õhtujutt/Sirli, Siim ja saladused/`)
   - Üksikud lood jäävad `Õhtujutt/` juurkausta

3. **Dokumentatsioon ja Git:**
   - Uuenda README.md
   - Commit ja push

---

## Olulised failid

- `progress_updates/2025-10-13_bedtime-stories.md` - Täna tehtud töö (ALUSTA SIIT!)
- `README.md` - Projekti ülevaade
- `TODO.md` - Järgmised ülesanded
- `COMPACTING_GUIDELINES.md` - Töövoo põhimõtted
- `USAGE.md` - Kasutamise juhend
- `download_stories.py` - Peamine skript

---

## Git seisund

```bash
git log --oneline  # Vaata commite
git status         # Vaata muudatusi
```

**Viimased commitid:**
1. Initial commit
2. Add automatic temp file cleanup
3. Update README
4. Add progress tracking
5. [pending after download completes]

---

## Kasulikud käsud

```bash
# Vaata projekti struktuuri
tree -L 2 -I '__pycache__|*.mp3'

# Kontrolli mitu lugu on allalaaditud
grep ",1,original" ohtujutt_catalog.csv | wc -l

# Kontrolli mitu on veel allalaadimata
grep ",0,original" ohtujutt_catalog.csv | wc -l

# Kontrolli allalaadimise progressi
ls -1 Õhtujutt/*.mp3 | wc -l
```

---

## Hetkeseisund

**Allalaadimine käib:**
- Skript töötab terminal aknas
- Ubuntu screen lock EI mõjuta (terminal process jätkab)
- Arvuti peab olema sees (mitte suspend/sleep)
- Tempo: ~100 lugu/tunnis
- ETA: homme õhtu ~15:00-16:00

**Pärast allalaadimist:**
1. Failide reorganiseerimine
2. Seeriate organiseerimine (numbriga lood kaustadesse)
3. Git commit ja push
4. Projekt VALMIS!

---

**Loodud:** 2025-10-13
**Viimati uuendatud:** 2025-10-13 23:00
**Projekti staatus:** Allalaadimine pooleli, reorganiseerimine järgmisena
