# WORKFLOW3 - QUICK START GUIDE

**Trigger Command:** "Execute workflow3"
**Purpose:** Build publisher-ready revised version of "Out of the Swamp"

---

## TO RUN WORKFLOW3 RIGHT NOW:

### Option 1: Say to Claude
```
Execute workflow3
```

### Option 2: Command Line
```bash
cd /Users/paulmarshall/Documents/GitHub/skylerthomas3/workflow3_production_scripts
python3 run_workflow3.py
```

---

## WHAT IT DOES:

1. ✅ Combines all REVISED chapters from `skylerthomas3.wiki/`
2. ✅ Generates KDP-ready PDF: `OUT-OF-THE-SWAMP-PUBLISHER.pdf`
3. ✅ Generates EPUB: `OUT-OF-THE-SWAMP-PUBLISHER.epub`

**All output goes to:** `skylerthomas3/KDP/`

---

## CURRENT STATUS:

### ✅ Ready to Build:
- Movement 1 intro
- Chapter 1: My Swamp (merged from Ch 1+2)
- Chapter 2: Dying Changes Everything

### ⏳ Still To Do:
- Movements 2-3 (will be added as revised)
- Front/back matter

**You can build NOW with what exists!**

---

## FILE LOCATIONS:

```
skylerthomas3/
├── workflow3_production_scripts/
│   └── run_workflow3.py          ← Master script
└── KDP/                          ← Output here

skylerthomas3.wiki/
└── REVISED-*.md                  ← Source chapters
```

---

## DIFFERENCES FROM WORKFLOW2:

| | WORKFLOW2 | WORKFLOW3 |
|---|---|---|
| **Version** | Original 14-chapter | Revised 12-chapter |
| **Location** | skylerthomas2/ | skylerthomas3/ |
| **Trigger** | "Run workflow2" | "Execute workflow3" |
| **PDF Name** | OUT-OF-THE-SWAMP-KDP-READY.pdf | OUT-OF-THE-SWAMP-PUBLISHER.pdf |

---

## FOR MORE INFO:

- Full docs: `WORKFLOW3-README.md`
- Setup details: `WORKFLOW3-SETUP-COMPLETE.md`
- Editorial review: `publish-editor.md`

---

**Just say: "Execute workflow3"** 🚀
