# Publisher Editing Workflow 3 - Complete Guide

## Overview

Workflow 3 is the publisher editing process for **"Out of the Swamp: How I Found Truth"** - Publisher's Review Edition. This workflow guides the revision process while maintaining the book's primary purpose: **featuring the author's songs**.

## Quick Start

### Trigger the Workflow
```
/workflow3
```

Or run the script directly:
```bash
python3 workflows/publisher_edit_workflow.py
```

## Core Principles

### 1. PRIMARY PURPOSE: Feature the Author's Songs
**This is the most important principle.**

- Songs are the core of this book, not a supplementary feature
- Editorial feedback should improve song presentation, not remove songs
- **Never remove a song without explicit author approval**
- When faced with "song vs. narrative" conflicts, revise the narrative to serve the song

### 2. Preserve Author's Authentic Voice
- Maintain vulnerable, "wayfarer" tone
- Keep direct address to reader
- Preserve honest personal storytelling
- Don't over-polish into corporate Christianity speak

### 3. Eliminate Redundancy, Not Content
- Remove repetitive statements
- Combine similar concepts
- Don't cut for word count alone

### 4. Maintain Theological Integrity
- Preserve core doctrines
- Keep scripture references
- Maintain balance of theology and personal story

### 5. Improve Reader Experience
- Better pacing
- Clearer progression
- Reduce "academic lecture" feel

## Workflow Steps

### Step 1: Initialize Workflow

Run the workflow script to see current status:
```bash
python3 workflows/publisher_edit_workflow.py
```

This shows:
- Current movement being worked on
- Completed movements
- Songs removed/kept
- Recent revisions

### Step 2: Review Editorial Feedback

Read the relevant section in `publish-editor.md` for the movement you're working on:

**Movement 1 (IN THE SWAMP)** - Lines 55-77
- Diagnosis: TOO LONG and REPETITIVE
- Recommendation: Condense to 2 chapters
- Cut percentage: 40%

**Movement 2 (AT THE WATER'S EDGE)** - Lines 79-112
- Diagnosis: BLOATED with good ideas
- Recommendation: Selective cutting by chapter
- Cut percentage: 25-40% per chapter

**Movement 3 (UNFORCED RHYTHMS)** - Lines 114-158
- Diagnosis: RUSHED and loses cohesion
- Recommendation: Add personal narrative
- Cut percentage: Selective

### Step 3: Create Revision Plan

Before making changes, document your plan:

1. Which chapters will be merged/split/removed?
2. What content will be cut?
3. Which songs will be kept? (Answer: ALL unless author approves removal)
4. What will be integrated from multiple chapters?

### Step 4: Make Revisions in Wiki

All revised chapters go in: `skylerthomas3.wiki/`

**File Naming Convention:**
- `REVISED-##_chapter-##-title.md` - Revised chapters
- `DELETED-##_chapter-##-title.md` - Deletion note with rationale
- `MOVEMENT-#-REVISION-SUMMARY.md` - Summary document

**Example from Movement 1:**
- `REVISED-02_chapter-01-my-swamp.md` - Merged Ch 1+2
- `DELETED-04_chapter-03-stop-decide.md` - Deletion note
- `REVISED-05_chapter-04-dying-changes.md` - Lightly edited Ch 4
- `MOVEMENT-1-REVISION-SUMMARY.md` - Complete summary

### Step 5: Track Song Decisions

For every song, document the decision:

**If keeping a song:**
```markdown
### KEPT: [Song Title]
- **Reason:** [Why this song serves the book's purpose]
- **Quality:** [Professional/strong/adequate]
- **Integration:** [How it fits the narrative]
```

**If removing a song (REQUIRES AUTHOR APPROVAL):**
```markdown
### REMOVED: [Song Title] - AUTHOR APPROVED [DATE]
- **Author approval:** [Quote author's approval]
- **Reason:** [Why removal was necessary]
- **Content preserved:** [What content was integrated elsewhere]
- **Alternative use:** [Suggestions for song's use outside book]
```

### Step 6: Generate Revision Summary

After completing a movement's revisions, create the summary:

1. Copy the template from the workflow script
2. Fill in all sections:
   - Executive Summary
   - Before/After structure
   - Songs kept/removed
   - Detailed changes by chapter
   - Metrics
3. Save to: `skylerthomas3.wiki/MOVEMENT-#-REVISION-SUMMARY.md`

### Step 7: Update Workflow State

The workflow script tracks state in `workflows/workflow_state.json`. Update this file as you progress:

```json
{
  "current_movement": 2,
  "completed_movements": [1],
  "revision_history": [...],
  "songs_removed": [...],
  "songs_kept": [...],
  "last_updated": "2025-10-16T08:00:00"
}
```

## Movement-Specific Guidelines

### Movement 1: In the Swamp (Chapters 1-4)
**Status:** ✓ COMPLETED

**Editorial Recommendation:**
- Merge Ch 1 + 2 into single opening
- Delete Ch 3 or integrate decision moment
- Keep Ch 4 as theological anchor

**Song Policy for Movement 1:**
- "My Swamp" - KEEP (establishes crisis)
- "But Then I Prayed" - Author approved removal (content integrated)
- "STOP!! And Make a Decision" - Author approved removal (tonal clash)
- "Dying Changes Everything" - KEEP (theological climax)

### Movement 2: At the Water's Edge (Chapters 5-8)
**Status:** ○ PENDING

**Editorial Recommendation:**
- Ch 5: Cut 40% (focus on grace + Lake Hefner moment)
- Ch 6: Cut 25% (streamline Psalm 91)
- Ch 7: Cut 30% (pick ONE primary story)
- Ch 8: Keep mostly intact (best chapter)

**Song Policy for Movement 2:**
- Editorial review says: "All songs in Movement 2 are strong"
- **DEFAULT: KEEP ALL SONGS**
- Review each song for quality and integration
- Revise surrounding content to serve songs better

### Movement 3: Unforced Rhythms (Chapters 9-14)
**Status:** ○ PENDING

**Editorial Recommendation:**
- Add more personal narrative (currently too academic)
- Ch 13 "Devil's On The Run" may not fit tone
- Add concrete "where I am now" examples

**Song Policy for Movement 3:**
- Ch 13 song flagged as "aggressive tone clash"
- **DO NOT REMOVE without author discussion**
- Consider: Can surrounding content be rewritten to fit the song better?
- Alternative: Move to appendix rather than delete

## Quality Checklist

Before marking a movement complete, verify:

### Content Quality
- [ ] Redundancy eliminated (same point not made 5+ times)
- [ ] Author's voice preserved
- [ ] Personal narrative balanced with theology
- [ ] Clear progression through movement
- [ ] Strong opening and closing for each chapter

### Song Integration
- [ ] Every song has clear purpose
- [ ] Song lyrics are integrated into chapter flow
- [ ] QR codes and URLs present
- [ ] Song quality meets professional standard
- [ ] Any removed songs have author approval documented

### Documentation
- [ ] Revision summary completed
- [ ] All changed files tracked
- [ ] Before/after metrics recorded
- [ ] Song decisions documented
- [ ] Rationale provided for major cuts

### Technical
- [ ] Files properly named (REVISED-##_ prefix)
- [ ] Markdown formatting correct
- [ ] Links and references updated
- [ ] QR codes and URLs functional

## Common Scenarios

### Scenario 1: Editorial says remove a song
**Response:**
1. Do NOT remove immediately
2. Consult author first
3. Explore alternatives:
   - Revise surrounding content
   - Move to different chapter
   - Adjust song presentation
   - Keep song, cut other content
4. Only remove with explicit author approval
5. Document approval in revision summary

### Scenario 2: Two chapters seem repetitive
**Response:**
1. Identify unique content in each
2. Merge if both serve same purpose
3. Extract and preserve all songs from both
4. Combine complementary content
5. Create stronger unified chapter

### Scenario 3: Chapter is too long
**Response:**
1. Remove redundant statements
2. Condense over-explained concepts
3. Reduce theologian quotes (keep best 2-3)
4. Trust reader to understand
5. **DO NOT cut songs to reduce length**

### Scenario 4: Song doesn't fit narrative
**Response:**
1. **Revise narrative to fit song** (not vice versa)
2. Remember: book exists to feature songs
3. Adjust surrounding context
4. Strengthen song introduction
5. Add personal story connecting song to chapter theme

## Troubleshooting

### Problem: Workflow script won't run
```bash
# Make script executable
chmod +x workflows/publisher_edit_workflow.py

# Run with Python 3
python3 workflows/publisher_edit_workflow.py
```

### Problem: Can't find editorial feedback
Editorial feedback is in: `publish-editor.md`
- Movement 1: Lines 55-77
- Movement 2: Lines 79-112
- Movement 3: Lines 114-158

### Problem: Not sure if song should be removed
**Default answer: KEEP THE SONG**

Only remove if:
1. Author explicitly approves
2. Strong justification exists
3. Content is preserved elsewhere
4. Alternative use is suggested

### Problem: Revision summary is incomplete
Use the template in `publisher_edit_workflow.py`:
```python
workflow.generate_revision_summary(movement_num=2)
```

## Files and Directories

### Project Structure
```
skylerthomas3/
├── .claude/
│   └── commands/
│       └── workflow3.md          # Slash command
├── workflows/
│   ├── publisher_edit_workflow.py   # Main script
│   ├── WORKFLOW3-GUIDE.md          # This guide
│   ├── workflow_config.json        # Configuration
│   └── workflow_state.json         # Current state
├── publish-editor.md               # Editorial feedback
└── [other project files]

skylerthomas3.wiki/
├── REVISED-##_chapter-##-*.md      # Revised chapters
├── DELETED-##_chapter-##-*.md      # Deletion notes
└── MOVEMENT-#-REVISION-SUMMARY.md  # Summaries
```

## Support and Questions

### When in doubt:
1. **Preserve the song** - Songs are the book's core purpose
2. **Ask the author** - Don't make major decisions alone
3. **Document everything** - Future you will thank you
4. **Check Movement 1** - It's the completed example

### Key Reference Files:
- **Editorial Review:** `publish-editor.md`
- **Movement 1 Example:** `skylerthomas3.wiki/MOVEMENT-1-REVISION-SUMMARY.md`
- **Workflow Script:** `workflows/publisher_edit_workflow.py`
- **This Guide:** `workflows/WORKFLOW3-GUIDE.md`

## Version History

- **v1.0** (2025-10-16): Initial workflow creation
  - Slash command established
  - Python workflow script created
  - Documentation completed
  - Song preservation policy emphasized

---

**Remember: The songs are the star. The book exists to feature them. Revise accordingly.**
