#!/usr/bin/env python3
"""
Sync 'saved' status in CSV with actual files in output folder
"""

import os
import csv
import shutil

# Configuration
PROJECT_FOLDER = "/home/d0021/Automation/ohtujutt-vikerraadio"
OUTPUT_FOLDER = os.path.join(PROJECT_FOLDER, "Õhtujutt")  # MP3 files location
OUTPUT_CSV = os.path.join(PROJECT_FOLDER, "ohtujutt_catalog.csv")
AUDIO_FORMAT = "mp3"

def sync_saved_status():
    """Check which files exist and update CSV saved column"""

    if not os.path.exists(OUTPUT_CSV):
        print(f"CSV not found: {OUTPUT_CSV}")
        return

    # Backup CSV before modifying
    backup_path = OUTPUT_CSV + '.backup'
    shutil.copy2(OUTPUT_CSV, backup_path)
    print(f"Backup created: {backup_path}")

    # Read all stories
    stories = []
    with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stories.append(row)

    print(f"Loaded {len(stories)} stories from CSV")

    # Check each story
    updated_count = 0
    saved_count = 0

    for story in stories:
        title = story.get('title', '')
        old_saved = story.get('saved', '0')

        # Check if file exists
        file_path = os.path.join(OUTPUT_FOLDER, f"{title}.{AUDIO_FORMAT}")
        file_exists = os.path.exists(file_path)

        new_saved = '1' if file_exists else '0'

        if new_saved != old_saved:
            print(f"  Updating: {title}")
            print(f"    Was: saved={old_saved}, Now: saved={new_saved}")
            story['saved'] = new_saved
            updated_count += 1

        if new_saved == '1':
            saved_count += 1

    # Write back to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['index', 'title', 'url', 'duration_seconds', 'duration_formatted', 'saved']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stories)

    print(f"\n{'='*60}")
    print(f"Sync complete!")
    print(f"Total stories: {len(stories)}")
    print(f"Updated: {updated_count}")
    print(f"Currently saved: {saved_count}")
    print(f"Not saved: {len(stories) - saved_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    sync_saved_status()
