#!/usr/bin/env python3
"""
Find duplicate titles in CSV and report with their indices
"""

import csv
from collections import defaultdict

CSV_PATH = "/home/d0021/Automation/ohtujutt-vikerraadio/ohtujutt_catalog.csv"
OUTPUT_PATH = "/home/d0021/Automation/ohtujutt-vikerraadio/duplicates.txt"

def find_duplicates():
    """Find stories that appear multiple times in CSV"""

    # Dictionary: title -> list of indices
    title_indices = defaultdict(list)

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('title', '').strip()
            index = row.get('index', '')
            if title:
                title_indices[title].append(index)

    # Find duplicates (titles with more than 1 index)
    duplicates = {title: indices for title, indices in title_indices.items() if len(indices) > 1}

    # Write to file
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        if duplicates:
            f.write(f"Found {len(duplicates)} duplicate titles\n")
            f.write("="*80 + "\n\n")

            for title, indices in sorted(duplicates.items()):
                f.write(f"{title}\n")
                f.write(f"  Indices: {', '.join(indices)}\n")
                f.write(f"  Count: {len(indices)}\n\n")
        else:
            f.write("No duplicates found!\n")

    print(f"Analysis complete!")
    print(f"Total unique titles: {len(title_indices)}")
    print(f"Duplicate titles: {len(duplicates)}")
    if duplicates:
        total_dupes = sum(len(indices) - 1 for indices in duplicates.values())
        print(f"Total duplicate entries: {total_dupes}")
    print(f"Results written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    find_duplicates()
