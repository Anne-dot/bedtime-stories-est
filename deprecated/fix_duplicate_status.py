#!/usr/bin/env python3
"""
Script to fix duplicate_status in CSV based on title and duration
Rules:
1. Group by title (exact match)
2. Exclude: "Õhtujutt lastele", "Õhtujutt.", "Õhtujutt"
3. In each group:
   - Same duration → smallest index = original, rest = duplicate
   - Has duration + no duration → with duration = original, without = duplicate
   - Different durations → all stay original (different episodes)
"""

import csv
import os
from collections import defaultdict

CSV_PATH = "ohtujutt_catalog.csv"
EXCLUDED_TITLES = ["Õhtujutt lastele", "Õhtujutt.", "Õhtujutt"]


def load_csv(csv_path):
    """Load CSV into memory"""
    stories = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stories.append(row)
    return stories


def group_by_title(stories):
    """Group stories by title"""
    groups = defaultdict(list)
    for story in stories:
        title = story.get('title', '').strip()
        if title:
            groups[title].append(story)
    return groups


def should_exclude_title(title):
    """Check if title should be excluded from processing"""
    return title in EXCLUDED_TITLES


def analyze_group(group):
    """Analyze a group and determine which should be original/duplicate"""
    # Only process groups with 2+ stories
    if len(group) <= 1:
        return []

    changes = []

    # Separate stories with/without duration
    with_duration = [s for s in group if s.get('duration_seconds', '').strip()]
    without_duration = [s for s in group if not s.get('duration_seconds', '').strip()]

    # Mark stories without duration as duplicate
    for story in without_duration:
        if story.get('duplicate_status') != 'duplicate':
            changes.append({
                'index': story.get('index'),
                'title': story.get('title'),
                'duration': story.get('duration_seconds', 'EMPTY'),
                'old_status': story.get('duplicate_status'),
                'new_status': 'duplicate',
                'reason': 'No duration (assumed duplicate)'
            })
            story['duplicate_status'] = 'duplicate'

    # Group stories with duration by duration value
    duration_groups = defaultdict(list)
    for story in with_duration:
        duration = story.get('duration_seconds', '').strip()
        duration_groups[duration].append(story)

    # For each duration group, keep smallest index as original
    for duration, stories_with_same_duration in duration_groups.items():
        if len(stories_with_same_duration) > 1:
            # Sort by index (convert to int for proper sorting)
            sorted_stories = sorted(stories_with_same_duration, key=lambda s: int(s.get('index', 0)))

            # First one stays original, rest become duplicate
            for i, story in enumerate(sorted_stories):
                if i == 0:
                    # Keep as original
                    if story.get('duplicate_status') != 'original':
                        changes.append({
                            'index': story.get('index'),
                            'title': story.get('title'),
                            'duration': duration,
                            'old_status': story.get('duplicate_status'),
                            'new_status': 'original',
                            'reason': f'Smallest index with duration {duration}s'
                        })
                        story['duplicate_status'] = 'original'
                else:
                    # Mark as duplicate
                    if story.get('duplicate_status') != 'duplicate':
                        changes.append({
                            'index': story.get('index'),
                            'title': story.get('title'),
                            'duration': duration,
                            'old_status': story.get('duplicate_status'),
                            'new_status': 'duplicate',
                            'reason': f'Same duration ({duration}s) as index {sorted_stories[0].get("index")}'
                        })
                        story['duplicate_status'] = 'duplicate'

    return changes


def main():
    """Main function"""
    print("Analyzing duplicate status in CSV...")
    print()

    # Load CSV
    stories = load_csv(CSV_PATH)
    print(f"Loaded {len(stories)} stories")

    # Group by title
    groups = group_by_title(stories)
    print(f"Found {len(groups)} unique titles")
    print()

    # Analyze each group
    all_changes = []

    for title, group in groups.items():
        if should_exclude_title(title):
            print(f"⊘ Skipping excluded title: \"{title}\" ({len(group)} stories)")
            continue

        if len(group) > 1:
            changes = analyze_group(group)
            if changes:
                all_changes.extend(changes)

    print()
    print("=" * 80)
    print(f"PROPOSED CHANGES: {len(all_changes)}")
    print("=" * 80)
    print()

    if not all_changes:
        print("No changes needed!")
        return

    # Show all changes
    for change in all_changes:
        print(f"Index {change['index']}: \"{change['title']}\"")
        print(f"  Duration: {change['duration']}")
        print(f"  Status: {change['old_status']} → {change['new_status']}")
        print(f"  Reason: {change['reason']}")
        print()

    # Ask for confirmation
    print("=" * 80)
    response = input("Apply these changes to CSV? (yes/no): ").strip().lower()

    if response == 'yes':
        # Create backup
        backup_path = CSV_PATH + '.backup'
        import shutil
        shutil.copy2(CSV_PATH, backup_path)
        print(f"✓ Backup created: {backup_path}")

        # Write updated CSV
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['index', 'title', 'url', 'duration_seconds',
                          'duration_formatted', 'saved', 'duplicate_status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(stories)

        print(f"✓ CSV updated: {CSV_PATH}")
        print(f"✓ Applied {len(all_changes)} changes")
    else:
        print("✗ Changes NOT applied")


if __name__ == "__main__":
    main()
