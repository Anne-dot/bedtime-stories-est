# Projekti Struktureerimise Plaan

## 🎯 Praegune Olukord

**Probleem:** Projektikaust on segane, GitHubis ei paista ilusasti välja.

**Failide arv juurkaustas:**
- 6 Python skripti
- 9 Markdown dokumenti
- 6 TXT faili (duplikaatide tracking)
- 1 JSON fail (kaustade puhastamine)
- 1 CSV fail + backup
- Kaustad: `deprecated/`, `vikerraadio-source-data/`, `progress_updates/`, `Õhtujutt/`

---

## ✅ Soovitatud Uus Struktuur

```
ohtujutt-vikerraadio/
├── README.md                          # Põhidokument (portfolio showcase)
├── LICENSE                            # (lisa kui plaanid GitHubis näidata)
├── .gitignore                         # Jäta
│
├── docs/                              # 📚 KÕIK DOKUMENTATSIOON
│   ├── PORTFOLIO_GUIDE.md             # Kuidas tööintervjuul näidata
│   ├── USAGE.md                       # Kasutamise juhend
│   ├── COMPACTING_GUIDELINES.md       # Koodipõhimõtted
│   ├── MANIFEST_DOWNLOAD_ANALYSIS.md  # Tehniline analüüs
│   ├── DOWNLOAD_BEHAVIOR_USE_CASES.md # Use case'id
│   ├── TODO.md                        # Järgmised sammud
│   ├── NEXT_SESSION.md                # Sessiooni plaan (working doc)
│   └── PROGRESS.md                    # Üldine progress
│
├── progress_updates/                  # 📅 PÄEVIKUD (jäta)
│   └── 2025-10-15_bedtime-stories.md
│
├── scripts/                           # 🛠️ KÕIK PYTHON SKRIPTID
│   ├── download_stories.py            # Põhiskript
│   ├── record_stories.py              # Alternatiiv
│   ├── manifest_downloader.py         # Helper
│   ├── csv_manager.py                 # Helper
│   ├── trim_silence.py                # Utility
│   ├── cleanup_temp_files.py          # Utility
│   └── deprecated/                    # Vanad/kasutamata
│       ├── find_duplicates.py
│       ├── fix_duplicate_status.py
│       ├── mark_duplicates.py
│       └── sync_saved_status.py
│
├── data/                              # 📊 TÖÖTAVAD ANDMED
│   ├── ohtujutt_catalog.csv           # Põhikataloog
│   ├── kaustade_puhastamine.json      # Progress tracking
│   │
│   └── duplicates/                    # Duplikaatide tracking
│       ├── all_suspects.txt           # Kõik kahtlused (TÜHI - kustuta?)
│       ├── high_similarity_remaining.txt  # 90%+ sarnased
│       ├── different_versions_not_duplicates.txt  # Eri versioonid
│       ├── duplicates.txt             # (vana - kustuta?)
│       ├── duration_mismatch.txt      # Quality control log
│       └── stories_without_duration.txt  # (vana - kustuta?)
│
├── tests/                             # 🧪 TESTID (optional)
│   └── vikerraadio-source-data/       # Test skriptid
│       ├── test_manifest_download.py
│       ├── test_three_stories.py
│       └── ...
│
└── Õhtujutt/                          # 🎵 AUDIO FAILID (gitignore)
    ├── (81 kausta)
    └── (1279 üksikut MP3)
```

---

## 🗂️ Detailsed Muudatused

### 1. Loo Uued Kaustad

```bash
mkdir -p docs
mkdir -p scripts/deprecated
mkdir -p data/duplicates
mkdir -p tests
```

### 2. Teisalda Dokumentatsioon → `docs/`

**Teisalda:**
- `PORTFOLIO_GUIDE.md` → `docs/`
- `USAGE.md` → `docs/`
- `COMPACTING_GUIDELINES.md` → `docs/`
- `MANIFEST_DOWNLOAD_ANALYSIS.md` → `docs/`
- `DOWNLOAD_BEHAVIOR_USE_CASES.md` → `docs/`
- `TODO.md` → `docs/`
- `NEXT_SESSION.md` → `docs/`
- `PROGRESS.md` → `docs/`

**Jäta juurde:**
- `README.md` (peamine showcase dokument)

### 3. Teisalda Skriptid → `scripts/`

**Teisalda:**
- `download_stories.py` → `scripts/`
- `record_stories.py` → `scripts/`
- `manifest_downloader.py` → `scripts/`
- `csv_manager.py` → `scripts/`
- `trim_silence.py` → `scripts/`
- `cleanup_temp_files.py` → `scripts/`
- `deprecated/*` → `scripts/deprecated/`

**Pärast teisaldamist:**
- Uuenda import path'id (kui vajalik)
- Uuenda README.md kasutamise näited

### 4. Teisalda Andmed → `data/`

**Teisalda:**
- `ohtujutt_catalog.csv` → `data/`
- `kaustade_puhastamine.json` → `data/`
- `all_suspects.txt` → `data/duplicates/`
- `high_similarity_remaining.txt` → `data/duplicates/`
- `different_versions_not_duplicates.txt` → `data/duplicates/`
- `duplicates.txt` → `data/duplicates/`
- `duration_mismatch.txt` → `data/duplicates/`
- `stories_without_duration.txt` → `data/duplicates/`

**Pärast teisaldamist:**
- Uuenda skriptide CSV_PATH (`data/ohtujutt_catalog.csv`)

### 5. Teisalda Testid → `tests/`

**Teisalda:**
- `vikerraadio-source-data/*` → `tests/`

### 6. Kustuta Mittevajalikud Failid

**Kustuta kindlasti:**
- `ohtujutt_catalog.csv.backup` (backup, ei ole vajalik GitHubis)
- `all_suspects.txt` (TÜHI - 0 kahtlust)
- `duplicates.txt` (vana, asendatud `different_versions_not_duplicates.txt`)
- `stories_without_duration.txt` (vana/deprecated)

**Hoia alles (töötavad failid):**
- `high_similarity_remaining.txt` (35 paari - töö pooleli)
- `different_versions_not_duplicates.txt` (5 eri versiooni)
- `duration_mismatch.txt` (quality control log)

---

## 📝 README.md Uuendused

**Praegune probleem:**
- README on liiga pikk (520+ rida)
- Tehnilised detailid võtavad liiga palju ruumi
- Portfolio aspekt puudub

**Soovitus:**

### Uus README.md struktuur (150-200 rida):

```markdown
# Vikerraadio Õhtujutt Automatiseerimine

> Automatiseeritud süsteem Estonian Public Broadcasting (ERR) Vikerraadio õhtujuttude
> allalaadimiseks, organiseerimiseks ja kvaliteedikontrolliks.

## 🎯 Projekti Ülevaade

**Probleem:** 2000+ audiolugu halvasti organiseeritud, palju duplikaate, kaustad puuduvad

**Lahendus:** Automaatne allalaadimine + intelligentne duplikaatide tuvastamine (90%+ täpsus)

**Tulemus:**
- ✅ 1822 lugu kvaliteetselt organiseeritud
- ✅ 81 sarja kausta grupeeritud
- ✅ 78 duplikaati tuvastatud ja eemaldatud
- ✅ 19x kiirem kui käsitsi (20h vs 16 päeva)

## 🚀 Kiirstart

[lühike setup ja kasutamise juhend - 20-30 rida]

## 📊 Tehnilised Lahendused

[3-4 highlight'i koodi näidetega - 30-40 rida]

## 📁 Projekti Struktuur

[kaust-tree 15-20 rida]

## 📚 Dokumentatsioon

- [Usage Guide](docs/USAGE.md) - Detailne kasutamise juhend
- [Portfolio Guide](docs/PORTFOLIO_GUIDE.md) - Kuidas tööintervjuul esitada
- [Compacting Guidelines](docs/COMPACTING_GUIDELINES.md) - Koodipõhimõtted
- [Technical Analysis](docs/MANIFEST_DOWNLOAD_ANALYSIS.md) - DASH manifest dokumentatsioon

## 🤝 Contributing

[kui avalik projekt]

## 📜 License

[MIT või "For personal use only"]

## ✨ Acknowledgments

Loodud 2025 oktoobris Claude Code'iga.
```

**Kõik tehniline detail → eraldi dokumendid:**
- Detailne setup → `docs/USAGE.md`
- Arhitektuur → `docs/COMPACTING_GUIDELINES.md`
- Manifest analüüs → `docs/MANIFEST_DOWNLOAD_ANALYSIS.md`

---

## 🔧 .gitignore Uuendused

**Lisa:**
```gitignore
# CSV backups
*.csv.backup

# Duplicate tracking (generated files)
data/duplicates/all_suspects.txt
data/duplicates/duplicates.txt

# Working docs (sessions)
docs/NEXT_SESSION.md
docs/TODO.md

# Progress tracking (optional - might want to keep)
# progress_updates/
```

---

## ✅ Eelis

**Enne:**
- 22 faili juurkaustas
- Segane, pole selge mis on mis
- Raske navigeerida

**Pärast:**
- 2-3 faili juurkaustas (README, LICENSE, .gitignore)
- Selge struktuur: `docs/`, `scripts/`, `data/`, `tests/`
- Portfolio showcase valmis
- Professionaalne välimus GitHubis

---

## 📋 Implementeerimise Sammud

### Samm 1: Backup (ohutu algus)

```bash
# Loo backup kogu projektist
cd /home/d0021/Automation/
tar -czf ohtujutt-vikerraadio-backup-$(date +%Y%m%d).tar.gz ohtujutt-vikerraadio/
```

### Samm 2: Loo Kaustastruktuur

```bash
cd /home/d0021/Automation/ohtujutt-vikerraadio
mkdir -p docs scripts/deprecated data/duplicates tests
```

### Samm 3: Git Teisaldamised (säilitab ajalugu)

```bash
# Dokumentatsioon
git mv PORTFOLIO_GUIDE.md docs/
git mv USAGE.md docs/
git mv COMPACTING_GUIDELINES.md docs/
git mv MANIFEST_DOWNLOAD_ANALYSIS.md docs/
git mv DOWNLOAD_BEHAVIOR_USE_CASES.md docs/
git mv TODO.md docs/
git mv NEXT_SESSION.md docs/
git mv PROGRESS.md docs/

# Skriptid
git mv download_stories.py scripts/
git mv record_stories.py scripts/
git mv manifest_downloader.py scripts/
git mv csv_manager.py scripts/
git mv trim_silence.py scripts/
git mv cleanup_temp_files.py scripts/
git mv deprecated scripts/

# Andmed
git mv ohtujutt_catalog.csv data/
git mv kaustade_puhastamine.json data/
git mv all_suspects.txt data/duplicates/
git mv high_similarity_remaining.txt data/duplicates/
git mv different_versions_not_duplicates.txt data/duplicates/
git mv duplicates.txt data/duplicates/
git mv duration_mismatch.txt data/duplicates/
git mv stories_without_duration.txt data/duplicates/

# Testid
git mv vikerraadio-source-data tests/

# Kustuta tarbetud
git rm ohtujutt_catalog.csv.backup
```

### Samm 4: Uuenda Skriptide Path'id

**Muuda kõikides skriptides:**
```python
# Vana:
CSV_PATH = "ohtujutt_catalog.csv"

# Uus:
CSV_PATH = "../data/ohtujutt_catalog.csv"
```

**Või parem - kasuta absoluutset path'i:**
```python
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "ohtujutt_catalog.csv")
```

### Samm 5: Uuenda README.md

- Lühenda 520 reast → 150-200 rida
- Lisa portfolio aspekt
- Uuenda path'id (`python3 download_stories.py` → `python3 scripts/download_stories.py`)

### Samm 6: Commit ja Push

```bash
git add -A
git commit -m "Restructure project: organize into docs/, scripts/, data/, tests/ folders

- Move all documentation to docs/ (8 files)
- Move all Python scripts to scripts/ (6 files)
- Move data files to data/ and data/duplicates/ (8 files)
- Move test files to tests/
- Update script paths to use new data/ location
- Shorten README.md for better GitHub showcase
- Remove unnecessary backup files

Result: Clean, professional project structure suitable for portfolio"

git push
```

---

## 🎯 Prioriteet

**MUST (teha kindlasti):**
1. ✅ Loo `docs/`, `scripts/`, `data/` kaustad
2. ✅ Teisalda failid (git mv)
3. ✅ Uuenda skriptide CSV path'id
4. ✅ Kustuta backup failid

**SHOULD (väga soovitav):**
5. ✅ Lühenda README.md
6. ✅ Uuenda .gitignore

**COULD (tulevikus):**
7. ⏳ Lisa LICENSE fail
8. ⏳ Paranda import path'id (kui mooduleid importitakse)

---

**Loodud:** 2025-10-15
**Eesmärk:** Professionaalne GitHub portfolio
**Ajakulu:** ~30 min implementeerimiseks
