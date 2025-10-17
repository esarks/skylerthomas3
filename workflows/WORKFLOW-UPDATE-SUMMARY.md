# Workflow Update Capability - Summary

**Date:** October 16, 2025
**Question:** "As I add chapters does workflow3 require modification?"
**Answer:** Yes, but it's automated with a helper script

---

## Quick Answer

**YES, the workflow needs updates as you add chapters, BUT it's easy:**

```bash
# After adding each revised chapter:
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5

# Check your progress:
python3 workflows/update_workflow_progress.py --status
```

---

## What Was Created

### New Helper Script ✓
**File:** `workflows/update_workflow_progress.py`

**Purpose:** Automatically update workflow as you add chapters

**Features:**
- Add revised chapters to movement tracking
- Mark movements as complete
- Record song decisions (kept/removed)
- Update workflow script automatically
- Update state tracking file
- Show current progress status

### New Documentation ✓
**File:** `workflows/UPDATING-WORKFLOW.md`

**Purpose:** Complete guide for updating workflow

**Contents:**
- How to use the helper script
- Manual update instructions (if needed)
- Workflow for adding chapters
- Progress tracking
- Troubleshooting

### Updated Files ✓
- `workflows/QUICK-REFERENCE.md` - Added update commands
- `CLAUDE.md` - Added update capability section

---

## How It Works

### The Problem
The workflow tracks:
1. Which chapters have been revised in each movement
2. Which movements are complete
3. Which songs were kept or removed
4. Revision history

As you add chapters, this tracking needs updates.

### The Solution
A helper script that automatically updates everything:

**Two files get updated:**
1. `publisher_edit_workflow.py` - Main workflow script (MOVEMENTS dictionary)
2. `workflow_state.json` - Progress tracking file

**One command does it all:**
```bash
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5
```

---

## Usage Examples

### Example 1: You just revised Chapter 5 (Living Waters Edge)

```bash
# 1. Save your work
# File: skylerthomas3.wiki/REVISED-07_chapter-04-living-waters-edge.md

# 2. Update workflow
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5

# 3. Record the song
python3 workflows/update_workflow_progress.py \
  --song "Living Waters Edge" \
  --status kept \
  --reason "Strong song, fits chapter theme perfectly"

# 4. Check status
python3 workflows/update_workflow_progress.py --status
```

**Output:**
```
✓ Added chapter 5 to Movement 2
✓ Updated workflows/publisher_edit_workflow.py
✓ State saved to workflows/workflow_state.json
✓ Recorded song kept: Living Waters Edge
```

### Example 2: You completed all of Movement 2

```bash
# Mark movement complete
python3 workflows/update_workflow_progress.py --movement 2 --complete

# Check status
python3 workflows/update_workflow_progress.py --status
```

**Output:**
```
✓ Marked Movement 2 as completed
✓ Updated workflows/publisher_edit_workflow.py
✓ State saved to workflows/workflow_state.json

WORKFLOW PROGRESS STATUS
Current Movement: 3
Completed Movements: [1, 2]
```

### Example 3: Check your current progress

```bash
python3 workflows/update_workflow_progress.py --status
```

**Output:**
```
======================================================================
WORKFLOW PROGRESS STATUS
======================================================================

Last Updated: 2025-10-16T11:43:00
Current Movement: 2
Completed Movements: [1]

----------------------------------------------------------------------
MOVEMENTS:
----------------------------------------------------------------------
✓ Movement 1: In the Swamp (The Struggle)
   Original: 4 chapters | Revised: 2 chapters
   Status: completed
   Revised chapters: [1, 2]

○ Movement 2: At the Water's Edge (Encountering Grace)
   Original: 4 chapters | Revised: 4 chapters
   Status: in_progress
   Revised chapters: [4, 5, 6, 7]

○ Movement 3: Unforced Rhythms (Living in Grace)
   Original: 6 chapters | Revised: 1 chapters
   Status: in_progress
   Revised chapters: [8]

----------------------------------------------------------------------
SONGS:
----------------------------------------------------------------------
Kept: 2
Removed: 0
======================================================================
```

---

## Your Workflow Now

### Before (Manual)
1. Revise chapter
2. Save file
3. Manually edit `publisher_edit_workflow.py`
4. Manually edit `workflow_state.json`
5. Make sure you didn't break the syntax
6. Test it

### After (Automated)
1. Revise chapter
2. Save file
3. Run: `python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5`
4. Done!

---

## All Update Commands

### Check Status
```bash
python3 workflows/update_workflow_progress.py --status
```

### Add Revised Chapter
```bash
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5
```

### Mark Movement Complete
```bash
python3 workflows/update_workflow_progress.py --movement 2 --complete
```

### Record Song Kept
```bash
python3 workflows/update_workflow_progress.py --song "Song Title" --status kept
```

### Record Song Removed (requires reason)
```bash
python3 workflows/update_workflow_progress.py \
  --song "Song Title" \
  --status removed \
  --reason "Author approved on 2025-10-16"
```

---

## What Gets Updated Automatically

### 1. publisher_edit_workflow.py
**The MOVEMENTS dictionary:**
```python
MOVEMENTS = {
    2: {
        "name": "At the Water's Edge (Encountering Grace)",
        "original_chapters": [5, 6, 7, 8],
        "revised_chapters": [4, 5, 6, 7],  # ← Updated automatically
        "status": "in_progress"             # ← Updated automatically
    }
}
```

### 2. workflow_state.json
**Progress tracking:**
```json
{
  "current_movement": 2,
  "completed_movements": [1],
  "revision_history": [
    {
      "timestamp": "2025-10-16T11:43:00",
      "movement": 2,
      "chapter": 5,
      "action": "added",
      "details": "Chapter 5 revised and added to Movement 2"
    }
  ],
  "songs_kept": [
    {
      "song": "Living Waters Edge",
      "action": "kept",
      "reason": "Strong song, fits chapter perfectly",
      "timestamp": "2025-10-16T11:43:00"
    }
  ]
}
```

---

## Important Notes

### When to Update
**Update immediately after:**
- Adding a revised chapter file
- Making a song decision
- Completing a movement

**Don't wait** - update as you go to keep tracking accurate.

### Song Tracking
**Every chapter has a song** - record each decision:
- Use `--status kept` for songs you keep
- Use `--status removed` for songs you remove (requires `--reason`)
- Include reason for kept songs too (good documentation)

### Movement Numbers
Use the **original movement numbers** when updating:
- Movement 1: Chapters 1-4 (original) → 1-2 (revised)
- Movement 2: Chapters 5-8 (original) → 4-7 (revised)
- Movement 3: Chapters 9-14 (original) → 8+ (revised)

---

## Troubleshooting

### Script won't run
```bash
# Make it executable
chmod +x workflows/update_workflow_progress.py

# Run with Python 3
python3 workflows/update_workflow_progress.py --status
```

### "Chapter already in Movement"
The chapter was already added. Check status:
```bash
python3 workflows/update_workflow_progress.py --status
```

### Want to see what changed
```bash
# Check git diff
git diff workflows/publisher_edit_workflow.py
git diff workflows/workflow_state.json
```

### Need to undo
```bash
# Git checkout to restore
git checkout -- workflows/publisher_edit_workflow.py
git checkout -- workflows/workflow_state.json

# Or edit manually
```

---

## Documentation Reference

| File | Purpose |
|------|---------|
| `workflows/update_workflow_progress.py` | Helper script (use this!) |
| `workflows/UPDATING-WORKFLOW.md` | Complete update guide |
| `workflows/WORKFLOW3-GUIDE.md` | Full workflow guide |
| `workflows/QUICK-REFERENCE.md` | Quick commands |
| `CLAUDE.md` | Project documentation |

---

## Summary

**Question:** "As I add chapters does workflow3 require modification?"

**Answer:** Yes, but it's automated.

**How:**
```bash
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5
```

**Why:** Keeps tracking accurate for progress monitoring and reporting.

**When:** After adding each revised chapter file.

**Details:** See `workflows/UPDATING-WORKFLOW.md`

---

**Status:** ✓ Update capability created and tested
**Date:** October 16, 2025
**Files Created:** 2 (helper script + guide)
**Files Updated:** 2 (quick reference + CLAUDE.md)

---

**Ready to use!** Add your next chapter and update the workflow automatically.
