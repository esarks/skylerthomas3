# Workflow 3 - Quick Reference Card

## Execute Workflow

### Option 1: Slash Command (Recommended)
```
/workflow3
```

### Option 2: Direct Script Execution
```bash
python3 workflows/publisher_edit_workflow.py
```

## Update Progress (As You Add Chapters)

### After adding a revised chapter
```bash
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5
```

### Check your progress
```bash
python3 workflows/update_workflow_progress.py --status
```

**See:** `workflows/UPDATING-WORKFLOW.md` for complete guide

---

## Core Principle

**THE PRIMARY PURPOSE OF THIS BOOK IS TO FEATURE THE AUTHOR'S SONGS**

Songs should NOT be removed without explicit author approval.

---

## Workflow Steps

1. **Check Status** - Run workflow script to see current state
2. **Review Feedback** - Read relevant section in `publish-editor.md`
3. **Make Revisions** - Edit files in `skylerthomas3.wiki/`
4. **Track Changes** - Document all song and content decisions
5. **Generate Summary** - Create `MOVEMENT-#-REVISION-SUMMARY.md`

---

## File Naming

| File Type | Pattern | Example |
|-----------|---------|---------|
| Revised Chapter | `REVISED-##_chapter-##-title.md` | `REVISED-02_chapter-01-my-swamp.md` |
| Deleted Chapter | `DELETED-##_chapter-##-title.md` | `DELETED-04_chapter-03-stop-decide.md` |
| Summary | `MOVEMENT-#-REVISION-SUMMARY.md` | `MOVEMENT-1-REVISION-SUMMARY.md` |

All files go in: `skylerthomas3.wiki/`

---

## Song Decision Checklist

Before removing ANY song:

- [ ] Have I explored revising the narrative to fit the song?
- [ ] Have I consulted the author?
- [ ] Do I have EXPLICIT written approval?
- [ ] Have I documented the reason?
- [ ] Have I preserved the song content elsewhere?
- [ ] Have I suggested alternative uses for the song?

**If you answered NO to any question above: KEEP THE SONG**

---

## Movement Status

### ✓ Movement 1: Complete
- Chapters: 4 → 2
- Songs: 2 kept ("I Will Rise", "Dying Changes Everything")
- Reference: `skylerthomas3.wiki/MOVEMENT-1-REVISION-SUMMARY.md`

### ○ Movement 2: Pending
- Chapters: 4 (cut 25-40% each)
- Songs: Keep all (editorial says "strong")
- Focus: Ch 8 is best chapter, keep mostly intact

### ○ Movement 3: Pending
- Chapters: 6 → 5 (maybe)
- Songs: Ch 13 flagged, needs author discussion
- Focus: Add personal narrative, reduce academic tone

---

## Common Scenarios

| Situation | Action |
|-----------|--------|
| Editor says remove song | **Consult author first** |
| Two chapters repetitive | Merge, keep both songs |
| Chapter too long | Cut redundancy, NOT songs |
| Song doesn't fit | **Revise narrative to fit song** |

---

## Quality Checklist

Before marking movement complete:

- [ ] Redundancy eliminated (concepts not repeated 5+ times)
- [ ] Author's voice preserved
- [ ] All songs accounted for
- [ ] QR codes/URLs functional
- [ ] Revision summary complete
- [ ] Metrics recorded
- [ ] Files properly named

---

## Key Files

| File | Purpose |
|------|---------|
| `publish-editor.md` | Editorial feedback |
| `workflows/publisher_edit_workflow.py` | Main script |
| `workflows/WORKFLOW3-GUIDE.md` | Complete guide |
| `workflows/workflow_config.json` | Configuration |
| `workflows/workflow_state.json` | Current state |
| `skylerthomas3.wiki/MOVEMENT-1-REVISION-SUMMARY.md` | Completed example |

---

## Troubleshooting

**Script won't run?**
```bash
chmod +x workflows/publisher_edit_workflow.py
python3 workflows/publisher_edit_workflow.py
```

**Can't find editorial feedback?**
- Movement 1: `publish-editor.md` lines 55-77
- Movement 2: `publish-editor.md` lines 79-112
- Movement 3: `publish-editor.md` lines 114-158

**Not sure about song?**
- Default: KEEP THE SONG
- Consult author
- Document decision

---

## Remember

**"The songs are the star. The book exists to feature them. Revise accordingly."**

When in doubt:
1. Keep the song
2. Ask the author
3. Document everything
4. Check Movement 1 as example

---

**Quick Start:** Type `/workflow3` to begin!
