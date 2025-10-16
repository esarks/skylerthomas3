#!/usr/bin/env python3
"""
Publisher Editing Workflow (Workflow 3)
For "Out of the Swamp: How I Found Truth" - Publisher's Review Edition

This script orchestrates the editorial revision process while preserving
the PRIMARY PURPOSE: Featuring the author's songs.
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
WIKI_DIR = PROJECT_ROOT.parent / "skylerthomas3.wiki"
WORKFLOWS_DIR = PROJECT_ROOT / "workflows"
EDITORIAL_REVIEW = PROJECT_ROOT / "publish-editor.md"

# Workflow state file
STATE_FILE = WORKFLOWS_DIR / "workflow_state.json"

# Movement structure
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
        "revised_chapters": [],
        "status": "pending"
    },
    3: {
        "name": "Unforced Rhythms (Living in Grace)",
        "original_chapters": [9, 10, 11, 12, 13, 14],
        "revised_chapters": [],
        "status": "pending"
    }
}

class PublisherWorkflow:
    def __init__(self):
        self.state = self.load_state()

    def load_state(self):
        """Load workflow state from file"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        return {
            "current_movement": 1,
            "completed_movements": [],
            "revision_history": [],
            "songs_removed": [],
            "songs_kept": [],
            "last_updated": None
        }

    def save_state(self):
        """Save workflow state to file"""
        self.state["last_updated"] = datetime.now().isoformat()
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)

    def get_movement_info(self, movement_num):
        """Get information about a specific movement"""
        return MOVEMENTS.get(movement_num)

    def get_editorial_feedback(self, movement_num):
        """Extract editorial feedback for a specific movement"""
        feedback = {
            1: {
                "diagnosis": "TOO LONG and REPETITIVE",
                "recommendation": "Condense to 2 chapters max",
                "cut_percentage": "40%",
                "songs_note": "Chapter 3 rap format jarring - BUT check with author on song removal policy"
            },
            2: {
                "diagnosis": "BLOATED with good ideas that need pruning",
                "recommendation": "Chapter 5: cut 40%, Chapter 6: cut 25%, Chapter 7: cut 30%, Chapter 8: keep mostly intact",
                "cut_percentage": "30-40%",
                "songs_note": "All songs in Movement 2 are strong - preserve them"
            },
            3: {
                "diagnosis": "RUSHED and loses narrative cohesion",
                "recommendation": "Add more personal narrative, possibly cut Chapter 13 entirely",
                "cut_percentage": "Selective - add some, cut some",
                "songs_note": "Chapter 13 spiritual warfare may not fit - CONSULT AUTHOR before removing"
            }
        }
        return feedback.get(movement_num, {})

    def record_revision(self, movement, chapter, action, details):
        """Record a revision action"""
        revision = {
            "timestamp": datetime.now().isoformat(),
            "movement": movement,
            "chapter": chapter,
            "action": action,
            "details": details
        }
        self.state["revision_history"].append(revision)
        self.save_state()

    def record_song_action(self, song_title, action, reason):
        """Record when a song is removed or kept"""
        song_record = {
            "song": song_title,
            "action": action,  # "removed" or "kept"
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }

        if action == "removed":
            self.state["songs_removed"].append(song_record)
        else:
            self.state["songs_kept"].append(song_record)

        self.save_state()

    def generate_revision_summary(self, movement_num, output_file=None):
        """Generate a revision summary document"""
        movement = MOVEMENTS[movement_num]
        feedback = self.get_editorial_feedback(movement_num)

        if output_file is None:
            output_file = WIKI_DIR / f"MOVEMENT-{movement_num}-REVISION-SUMMARY.md"

        summary = f"""---
title: "Movement {movement_num} Revision Summary"
date: {datetime.now().strftime('%Y-%m-%d')}
revision_phase: "Phase 1: Structure"
---

# Movement {movement_num} Revision Summary
## {movement['name']}

**Date Completed:** {datetime.now().strftime('%B %d, %Y')}
**Editorial Phase:** Phase 1 (Structure)
**Revision Scope:** Movement {movement_num}

---

## Executive Summary

[TO BE FILLED IN AFTER REVISIONS]

---

## Editorial Feedback

**Diagnosis:** {feedback.get('diagnosis', 'N/A')}
**Recommendation:** {feedback.get('recommendation', 'N/A')}
**Target Reduction:** {feedback.get('cut_percentage', 'N/A')}
**Songs Note:** {feedback.get('songs_note', 'N/A')}

---

## What Changed: Before & After Structure

### BEFORE (Original Structure)
**Movement {movement_num}:** {len(movement['original_chapters'])} Chapters
{self._format_chapter_list(movement['original_chapters'])}

### AFTER (Revised Structure)
**Movement {movement_num}:** [TO BE DETERMINED]

---

## Songs: What Was Kept vs. Cut

### IMPORTANT: PRIMARY PURPOSE
**The primary purpose of this book is to feature the author's songs.**
Songs should only be removed with explicit author approval and strong justification.

### KEPT
[TO BE FILLED]

### CUT (if any)
[TO BE FILLED - requires author approval]

---

## Revision Details by Chapter

[TO BE FILLED AS REVISIONS ARE MADE]

---

## Key Editorial Principles Applied

1. **Song Preservation First** - Songs are the book's core purpose
2. **Redundancy Elimination** - Remove repetitive content
3. **Voice Preservation** - Maintain author's authentic voice
4. **Theological Integrity** - Preserve doctrinal content
5. **Reader Experience** - Improve pacing and clarity

---

## Files Created/Modified

[TO BE FILLED]

---

## Metrics Summary

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Chapters | {len(movement['original_chapters'])} | TBD | TBD |
| Songs | TBD | TBD | TBD |
| Estimated Words | TBD | TBD | TBD |

---

**Revision completed by:** [EDITOR NAME]
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Editorial Review Reference:** `/Users/paulmarshall/Documents/GitHub/skylerthomas3/publish-editor.md`
"""

        return summary

    def _format_chapter_list(self, chapters):
        """Format a list of chapters"""
        return "\n".join([f"- Chapter {ch}: [Title TBD]" for ch in chapters])

    def print_status(self):
        """Print current workflow status"""
        print("\n" + "="*70)
        print("PUBLISHER EDITING WORKFLOW - STATUS")
        print("="*70)
        print(f"\nProject: Out of the Swamp - Publisher's Review Edition")
        print(f"Last Updated: {self.state.get('last_updated', 'Never')}")
        print(f"\nCurrent Movement: {self.state['current_movement']}")
        print(f"Completed Movements: {len(self.state['completed_movements'])}")

        print("\n" + "-"*70)
        print("MOVEMENT STATUS:")
        print("-"*70)
        for num, info in MOVEMENTS.items():
            status_icon = "✓" if num in self.state['completed_movements'] else "○"
            print(f"{status_icon} Movement {num}: {info['name']}")
            print(f"   Original: {len(info['original_chapters'])} chapters | " +
                  f"Revised: {len(info['revised_chapters']) if info['revised_chapters'] else 'TBD'} chapters")

        print("\n" + "-"*70)
        print("SONG TRACKING:")
        print("-"*70)
        print(f"Songs Removed: {len(self.state['songs_removed'])}")
        if self.state['songs_removed']:
            for song in self.state['songs_removed']:
                print(f"  ✗ {song['song']}: {song['reason']}")

        print(f"\nSongs Kept: {len(self.state['songs_kept'])}")
        if self.state['songs_kept']:
            for song in self.state['songs_kept'][:5]:  # Show first 5
                print(f"  ✓ {song['song']}")
            if len(self.state['songs_kept']) > 5:
                print(f"  ... and {len(self.state['songs_kept']) - 5} more")

        print("\n" + "-"*70)
        print("RECENT REVISIONS:")
        print("-"*70)
        recent = self.state['revision_history'][-5:] if self.state['revision_history'] else []
        if recent:
            for rev in recent:
                print(f"  • Movement {rev['movement']}, Ch {rev['chapter']}: {rev['action']}")
        else:
            print("  No revisions recorded yet")

        print("\n" + "="*70 + "\n")


def main():
    """Main workflow execution"""
    workflow = PublisherWorkflow()

    print("\n" + "="*70)
    print("PUBLISHER EDITING WORKFLOW 3")
    print("Out of the Swamp: How I Found Truth - Publisher's Review Edition")
    print("="*70)

    workflow.print_status()

    print("\nWorkflow initialized successfully!")
    print("\nNext steps:")
    print("1. Review editorial feedback in publish-editor.md")
    print("2. Select movement/chapter to revise")
    print("3. Make revisions in skylerthomas3.wiki")
    print("4. Record changes using this workflow")
    print("5. Generate revision summary")

    print("\n" + "-"*70)
    print("IMPORTANT REMINDER:")
    print("-"*70)
    print("The PRIMARY PURPOSE of this book is to feature the author's songs.")
    print("Do NOT remove songs without explicit author approval.")
    print("When in doubt, keep the song and revise the surrounding content.")
    print("-"*70 + "\n")


if __name__ == "__main__":
    main()
