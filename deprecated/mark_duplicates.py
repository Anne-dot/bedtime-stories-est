#!/usr/bin/env python3
"""
Mark duplicate stories in CSV with 'original' or 'duplicate' flag
"""

import csv
import shutil
from collections import defaultdict

CSV_PATH = "/home/d0021/Automation/ohtujutt-vikerraadio/ohtujutt_catalog.csv"

# Exclude these problematic titles
EXCLUDE_TITLES = {
    "Õhtujutt lastele",
    "Õhtujutt.",
}

def normalize_title(title):
    """Remove trailing punctuation for comparison"""
    return title.rstrip('.').strip()

def mark_duplicates():
    """Add 'duplicate_status' column: 'original' or 'duplicate'"""

    # Backup CSV
    backup_path = CSV_PATH + '.backup'
    shutil.copy2(CSV_PATH, backup_path)
    print(f"Backup created: {backup_path}")

    # Read all stories
    stories = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stories.append(row)

    print(f"Loaded {len(stories)} stories from CSV")

    # Group by normalized title + duration
    # Key: (normalized_title, duration_seconds)
    # Value: list of (index, original_row)
    grouped = defaultdict(list)

    for row in stories:
        title = row.get('title', '').strip()
        duration = row.get('duration_seconds', '').strip()
        index = int(row.get('index', 0))

        # Skip excluded titles
        if title in EXCLUDE_TITLES:
            continue

        # Skip if no duration (can't determine if duplicate)
        if not duration:
            continue

        # Normalize title (remove trailing punctuation)
        norm_title = normalize_title(title)

        key = (norm_title, duration)
        grouped[key].append((index, row))

    # Mark duplicates
    original_count = 0
    duplicate_count = 0
    excluded_count = 0

    # First pass: mark everything as original by default
    for row in stories:
        row['duplicate_status'] = 'original'

    # Second pass: mark duplicates
    for key, entries in grouped.items():
        if len(entries) > 1:
            # Sort by index (lowest first)
            entries.sort(key=lambda x: x[0])

            # First one is original, rest are duplicates
            for i, (index, row) in enumerate(entries):
                if i == 0:
                    row['duplicate_status'] = 'original'
                    original_count += 1
                else:
                    row['duplicate_status'] = 'duplicate'
                    duplicate_count += 1

    # Count excluded
    for row in stories:
        title = row.get('title', '').strip()
        if title in EXCLUDE_TITLES:
            row['duplicate_status'] = 'excluded'
            excluded_count += 1

    # Write back to CSV with new column
    fieldnames = ['index', 'title', 'url', 'duration_seconds', 'duration_formatted', 'saved', 'duplicate_status']

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stories)

    print(f"\n{'='*60}")
    print(f"Duplicate marking complete!")
    print(f"Total stories: {len(stories)}")
    print(f"Unique originals: {len([s for s in stories if s['duplicate_status'] == 'original'])}")
    print(f"Duplicates marked: {duplicate_count}")
    print(f"Excluded (ambiguous titles): {excluded_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    mark_duplicates()
