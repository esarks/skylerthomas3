#!/usr/bin/env python3
"""
Workflow Progress Updater
Updates the workflow as you add revised chapters

Usage:
  python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5 --song "Living Waters Edge" --status kept
  python3 workflows/update_workflow_progress.py --movement 2 --complete
  python3 workflows/update_workflow_progress.py --status
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Paths
WORKFLOWS_DIR = Path(__file__).parent
SCRIPT_FILE = WORKFLOWS_DIR / "publisher_edit_workflow.py"
STATE_FILE = WORKFLOWS_DIR / "workflow_state.json"

# Movement definitions (edit this as needed)
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
        "revised_chapters": [4, 5, 6, 7],  # Updated as chapters are added
        "status": "in_progress"
    },
    3: {
        "name": "Unforced Rhythms (Living in Grace)",
        "original_chapters": [9, 10, 11, 12, 13, 14],
        "revised_chapters": [8],  # Start with what's done
        "status": "in_progress"
    }
}

def load_state():
    """Load current workflow state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "current_movement": 2,
        "completed_movements": [1],
        "revision_history": [],
        "songs_removed": [],
        "songs_kept": [],
        "last_updated": None
    }

def save_state(state):
    """Save workflow state"""
    state["last_updated"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✓ State saved to {STATE_FILE}")

def update_python_script():
    """Update the MOVEMENTS dictionary in the main Python script"""
    with open(SCRIPT_FILE, 'r') as f:
        content = f.read()

    # Find and replace the MOVEMENTS dictionary
    start_marker = "# Movement structure\nMOVEMENTS = {"
    end_marker = "\n}\n\nclass PublisherWorkflow:"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find MOVEMENTS dictionary in script")
        return False

    # Build new MOVEMENTS dictionary string
    movements_str = "# Movement structure\nMOVEMENTS = {\n"
    for num, data in MOVEMENTS.items():
        movements_str += f"    {num}: {{\n"
        movements_str += f"        \"name\": \"{data['name']}\",\n"
        movements_str += f"        \"original_chapters\": {data['original_chapters']},\n"
        movements_str += f"        \"revised_chapters\": {data['revised_chapters']},\n"
        movements_str += f"        \"status\": \"{data['status']}\"\n"
        movements_str += f"    }},\n"
    movements_str = movements_str.rstrip(",\n") + "\n}"

    # Replace in content
    new_content = content[:start_idx] + movements_str + content[end_idx:]

    # Write back
    with open(SCRIPT_FILE, 'w') as f:
        f.write(new_content)

    print(f"✓ Updated {SCRIPT_FILE}")
    return True

def add_chapter(movement, chapter_num):
    """Add a revised chapter to a movement"""
    if movement not in MOVEMENTS:
        print(f"Error: Movement {movement} not found")
        return False

    if chapter_num not in MOVEMENTS[movement]["revised_chapters"]:
        MOVEMENTS[movement]["revised_chapters"].append(chapter_num)
        MOVEMENTS[movement]["revised_chapters"].sort()
        print(f"✓ Added chapter {chapter_num} to Movement {movement}")

        # Update state
        state = load_state()
        state["revision_history"].append({
            "timestamp": datetime.now().isoformat(),
            "movement": movement,
            "chapter": chapter_num,
            "action": "added",
            "details": f"Chapter {chapter_num} revised and added to Movement {movement}"
        })
        save_state(state)

        # Update Python script
        update_python_script()
        return True
    else:
        print(f"Chapter {chapter_num} already in Movement {movement}")
        return False

def mark_complete(movement):
    """Mark a movement as completed"""
    if movement not in MOVEMENTS:
        print(f"Error: Movement {movement} not found")
        return False

    MOVEMENTS[movement]["status"] = "completed"
    print(f"✓ Marked Movement {movement} as completed")

    # Update state
    state = load_state()
    if movement not in state["completed_movements"]:
        state["completed_movements"].append(movement)
    state["current_movement"] = movement + 1 if movement < 3 else 3
    state["revision_history"].append({
        "timestamp": datetime.now().isoformat(),
        "movement": movement,
        "chapter": "all",
        "action": "completed",
        "details": f"Movement {movement} marked as complete"
    })
    save_state(state)

    # Update Python script
    update_python_script()
    return True

def record_song(song_title, status, reason=""):
    """Record a song decision"""
    state = load_state()

    song_record = {
        "song": song_title,
        "action": status,  # "removed" or "kept"
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }

    if status == "removed":
        state["songs_removed"].append(song_record)
        print(f"✓ Recorded song removal: {song_title}")
    else:
        state["songs_kept"].append(song_record)
        print(f"✓ Recorded song kept: {song_title}")

    save_state(state)
    return True

def show_status():
    """Display current workflow status"""
    state = load_state()

    print("\n" + "="*70)
    print("WORKFLOW PROGRESS STATUS")
    print("="*70)
    print(f"\nLast Updated: {state.get('last_updated', 'Never')}")
    print(f"Current Movement: {state.get('current_movement', 1)}")
    print(f"Completed Movements: {state.get('completed_movements', [])}")

    print("\n" + "-"*70)
    print("MOVEMENTS:")
    print("-"*70)
    for num, data in MOVEMENTS.items():
        status_icon = "✓" if data['status'] == 'completed' else "○"
        print(f"{status_icon} Movement {num}: {data['name']}")
        print(f"   Original: {len(data['original_chapters'])} chapters | " +
              f"Revised: {len(data['revised_chapters'])} chapters")
        print(f"   Status: {data['status']}")
        if data['revised_chapters']:
            print(f"   Revised chapters: {data['revised_chapters']}")

    print("\n" + "-"*70)
    print("SONGS:")
    print("-"*70)
    print(f"Kept: {len(state.get('songs_kept', []))}")
    print(f"Removed: {len(state.get('songs_removed', []))}")

    print("\n" + "="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(description='Update Workflow 3 progress')
    parser.add_argument('--movement', type=int, help='Movement number (1-3)')
    parser.add_argument('--add-chapter', type=int, help='Add revised chapter number')
    parser.add_argument('--complete', action='store_true', help='Mark movement as complete')
    parser.add_argument('--song', type=str, help='Song title')
    parser.add_argument('--status', nargs='?', const='show', help='Song status (kept/removed) or show workflow status')
    parser.add_argument('--reason', type=str, default='', help='Reason for song decision')

    args = parser.parse_args()

    # Show status if requested
    if args.status == 'show' or (args.status is not None and not args.song):
        show_status()
        return

    # Add chapter
    if args.movement and args.add_chapter:
        add_chapter(args.movement, args.add_chapter)

    # Mark complete
    elif args.movement and args.complete:
        mark_complete(args.movement)

    # Record song
    elif args.song and args.status:
        record_song(args.song, args.status, args.reason)

    # Show help if no valid action
    else:
        print("\nWorkflow Progress Updater")
        print("=" * 50)
        print("\nUsage examples:")
        print("  # Show status")
        print("  python3 workflows/update_workflow_progress.py --status")
        print()
        print("  # Add a revised chapter")
        print("  python3 workflows/update_workflow_progress.py --movement 2 --add-chapter 5")
        print()
        print("  # Mark movement complete")
        print("  python3 workflows/update_workflow_progress.py --movement 2 --complete")
        print()
        print("  # Record song kept")
        print("  python3 workflows/update_workflow_progress.py --song \"Living Waters Edge\" --status kept")
        print()
        print("  # Record song removed (requires reason)")
        print("  python3 workflows/update_workflow_progress.py --song \"Song Title\" --status removed --reason \"Author approved\"")
        print()

if __name__ == "__main__":
    main()
