#!/usr/bin/env python3
"""
CSV Manager module - single source of truth for story catalog data
Used by both record_stories.py and download_stories.py
"""

import os
import csv


class CSVManager:
    """Manages CSV operations - single source of truth for story data"""

    def __init__(self, csv_path, output_folder, audio_format):
        """Initialize CSV manager and load stories from file"""
        self.csv_path = csv_path
        self.output_folder = output_folder
        self.audio_format = audio_format
        self.stories = {}  # Dict: {url: story_row_dict}
        self.load()  # Load CSV immediately

    def load(self):
        """Load CSV file into memory"""
        if not os.path.exists(self.csv_path):
            print(f"Error: CSV file not found: {self.csv_path}")
            print("Please run collect_story_info.py first to create catalog.")
            exit(1)

        self._read_csv_file()
        print(f"Loaded {len(self.stories)} stories from CSV")

    def _read_csv_file(self):
        """Helper: read CSV and populate self.stories dict"""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('url', '').strip()
                if url:  # Skip empty rows
                    self.stories[url] = row

        if not self.stories:
            print("Warning: CSV file is empty or has no valid entries")
            print("Please run collect_story_info.py first to populate catalog.")

    def find_next_original_unsaved(self):
        """Find first story ready to record"""
        for url, story in self.stories.items():
            if self._is_ready_to_record(story):
                return story
        return None  # No stories left to record

    def _is_ready_to_record(self, story):
        """Helper: check if story is ready to record"""
        # Must have title, url, duration
        if not story.get('title', '').strip():
            return False
        if not story.get('url', '').strip():
            return False
        if not story.get('duration_seconds', '').strip():
            return False

        # Must be unsaved
        if story.get('saved') != '0':
            return False

        # Must be original (not duplicate)
        if story.get('duplicate_status') != 'original':
            return False

        return True

    def mark_as_saved(self, story_url):
        """Mark story as saved (only if file actually exists and duration is correct)"""
        story = self.stories[story_url]
        title = story['title']
        file_path = os.path.join(self.output_folder, f"{title}.{self.audio_format}")

        if not os.path.exists(file_path):
            print(f"Warning: File not found, not marking as saved: {title}")
            return False

        # Check file duration (quality control)
        try:
            from mutagen import File as MutagenFile
            audio = MutagenFile(file_path)
            if audio and audio.info:
                actual_duration = int(audio.info.length)
                expected_duration = int(story['duration_seconds'])
                difference = abs(actual_duration - expected_duration)

                if difference > 10:
                    # Log duration mismatch
                    with open('duration_mismatch.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{title}: expected {expected_duration}s, got {actual_duration}s (diff: {difference}s)\n")
                    print(f"  ⚠ Duration mismatch: expected {expected_duration}s, got {actual_duration}s")
                    print(f"  ✗ File rejected due to duration mismatch (not marking as saved)")
                    return False
        except Exception as e:
            print(f"  ⚠ Could not verify duration: {e}")
            # If we can't verify, don't mark as saved (safer)
            return False

        self.stories[story_url]['saved'] = '1'
        return True

    def save(self):
        """Save stories back to CSV with backup"""
        self._create_backup()
        self._write_csv_file()
        print(f"CSV saved: {self.csv_path}")

    def _create_backup(self):
        """Helper: backup existing CSV file"""
        if os.path.exists(self.csv_path):
            backup_path = self.csv_path + '.backup'
            import shutil
            shutil.copy2(self.csv_path, backup_path)

    def _write_csv_file(self):
        """Helper: write stories dict to CSV"""
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['index', 'title', 'url', 'duration_seconds',
                          'duration_formatted', 'saved', 'duplicate_status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.stories.values())
