# Updating Workflow 3 as You Add Chapters

## Quick Answer

**Yes, the workflow needs updates as you add chapters.**

Use the helper script to make updates easy:

```bash
# After adding a revised chapter
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5

# When you complete a movement
python3 workflows/update_workflow_progress.py --movement 2 --complete

# Check your progress anytime
python3 workflows/update_workflow_progress.py --status
```

---

## What Needs Updating

As you add revised chapters, two things need updates:

### 1. The Main Workflow Script
**File:** `workflows/publisher_edit_workflow.py`

**What:** The `MOVEMENTS` dictionary (lines 25-44)
- Tracks which chapters have been revised in each movement
- Tracks movement status (pending/in_progress/completed)

### 2. The Workflow State File
**File:** `workflows/workflow_state.json`

**What:** Current progress tracking
- Current movement being worked on
- Completed movements list
- Revision history
- Songs removed/kept

---

## Using the Helper Script

### Show Current Status
```bash
python3 workflows/update_workflow_progress.py --status
```

**Output:**
```
======================================================================
WORKFLOW PROGRESS STATUS
======================================================================

Last Updated: 2025-10-16T10:30:00
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
```

### Add a Revised Chapter
When you finish revising a chapter and add it to skylerthomas3.wiki:

```bash
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5
```

**What it does:**
- Adds chapter 5 to Movement 2's revised chapters list
- Updates `publisher_edit_workflow.py` automatically
- Records the action in `workflow_state.json`
- Timestamps the change

### Mark Movement Complete
When you finish all chapters in a movement:

```bash
python3 workflows/update_workflow_progress.py --movement 2 --complete
```

**What it does:**
- Marks Movement 2 as "completed"
- Adds Movement 2 to completed movements list
- Moves current movement to Movement 3
- Updates both script and state file

### Record Song Decisions

**Keep a song:**
```bash
python3 workflows/update_workflow_progress.py --song "Living Waters Edge" --status kept
```

**Remove a song (requires author approval):**
```bash
python3 workflows/update_workflow_progress.py \
  --song "Song Title" \
  --status removed \
  --reason "Author approved removal on 2025-10-16"
```

---

## Manual Update (If Needed)

If you prefer to update manually or the script doesn't work:

### Step 1: Edit the Python Script

**File:** `workflows/publisher_edit_workflow.py`

**Find this section (around line 25):**
```python
MOVEMENTS = {
    1: {
        "name": "In the Swamp (The Struggle)",
        "original_chapters": [1, 2, 3, 4],
        "revised_chapters": [1, 2],
        "status": "completed"
    },
    2: {
        "name": "At the Water's Edge (Encountering Grace)",
        "original_chapters": [5, 6, 7, 8],
        "revised_chapters": [],  # ← UPDATE THIS
        "status": "pending"
    },
```

**Update the `revised_chapters` list:**
```python
        "revised_chapters": [4, 5, 6, 7],  # ← Added chapters as you revise them
```

**Update status as needed:**
- `"pending"` - Not started
- `"in_progress"` - Working on it
- `"completed"` - All chapters revised

### Step 2: Update State File

**File:** `workflows/workflow_state.json`

Add to revision history:
```json
{
  "revision_history": [
    {
      "timestamp": "2025-10-16T10:30:00",
      "movement": 2,
      "chapter": 5,
      "action": "added",
      "details": "Chapter 5 revised and added"
    }
  ]
}
```

---

## Workflow for Adding Chapters

### Your Process:
1. **Revise chapter** (following Workflow 3 guidelines)
2. **Save file** in `skylerthomas3.wiki/REVISED-##_chapter-##-title.md`
3. **Update workflow** using helper script
4. **Check status** to verify
5. **Repeat** for next chapter

### Example: Adding Chapter 5 (Living Waters Edge)

```bash
# 1. You've finished revising chapter 5
# 2. Saved as: skylerthomas3.wiki/REVISED-07_chapter-04-living-waters-edge.md

# 3. Update the workflow
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5

# 4. Record the song
python3 workflows/update_workflow_progress.py \
  --song "Living Waters Edge" \
  --status kept \
  --reason "Strong song, serves chapter well"

# 5. Check status
python3 workflows/update_workflow_progress.py --status
```

---

## Current Progress Tracking

### Movement 1: ✓ COMPLETED
- Original chapters: 1, 2, 3, 4
- Revised chapters: 1, 2
- Songs kept: 2 ("I Will Rise", "Dying Changes Everything")
- Songs removed: 2 (with author approval)
- Status: Completed

### Movement 2: ○ IN PROGRESS
- Original chapters: 5, 6, 7, 8
- Revised chapters: 4, 5, 6, 7 (as you add them)
- Songs: TBD (record as you revise)
- Status: In progress

### Movement 3: ○ PENDING
- Original chapters: 9, 10, 11, 12, 13, 14
- Revised chapters: 8 (as you add them)
- Songs: TBD
- Status: Pending

**Note:** Chapter numbers in "revised" refer to the revised numbering after Movement 1 was condensed.

---

## Checking Your Progress

### Quick Status Check
```bash
python3 workflows/update_workflow_progress.py --status
```

### Run Full Workflow
```bash
/workflow3
# or
python3 workflows/publisher_edit_workflow.py
```

### Check State File Directly
```bash
cat workflows/workflow_state.json | python3 -m json.tool
```

---

## Important Reminders

### When Adding Chapters:
1. **Update workflow immediately** after saving chapter
2. **Record song decisions** for every chapter
3. **Generate revision summary** when movement complete
4. **Keep REVISED-## prefix** in filename

### Song Tracking:
- **Every chapter has a song** - track each one
- **Default is KEEP** - only remove with approval
- **Document decisions** - use the helper script
- **Reason required** - especially for removals

---

## Troubleshooting

### Script won't run
```bash
# Make it executable
chmod +x workflows/update_workflow_progress.py

# Run with Python 3
python3 workflows/update_workflow_progress.py --status
```

### Updates not showing
```bash
# Check if files exist
ls -la workflows/publisher_edit_workflow.py
ls -la workflows/workflow_state.json

# Run status to see current state
python3 workflows/update_workflow_progress.py --status
```

### Want to undo an update
The helper script automatically updates the files. To undo:
1. Check git status: `git status`
2. Revert if needed: `git checkout -- workflows/publisher_edit_workflow.py`
3. Or manually edit the files

---

## Summary

**Yes, workflow needs updates, but it's easy:**

```bash
# After each revised chapter:
python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5

# After each song decision:
python3 workflows/update_workflow_progress.py --song "Title" --status kept

# When movement done:
python3 workflows/update_workflow_progress.py --movement 2 --complete

# Check progress anytime:
python3 workflows/update_workflow_progress.py --status
```

The helper script automatically updates both the workflow script and state file, keeping everything in sync.

---

**Quick Reference:**
- **Helper script:** `workflows/update_workflow_progress.py`
- **Main workflow:** `workflows/publisher_edit_workflow.py`
- **State tracking:** `workflows/workflow_state.json`
- **Full guide:** `workflows/WORKFLOW3-GUIDE.md`
