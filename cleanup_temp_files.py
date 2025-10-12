#!/usr/bin/env python3
"""
Cleanup script - removes temporary files left by yt-dlp
Run this after download_stories.py completes
"""

import os
import glob

# Configuration
OUTPUT_FOLDER = "Õhtujutt"

def cleanup_temp_files():
    """Remove yt-dlp temporary files"""

    print("="*60)
    print("Cleanup: Removing yt-dlp temporary files")
    print("="*60)

    # Patterns to clean
    patterns = [
        os.path.join(OUTPUT_FOLDER, "*.temp.mp3"),
        os.path.join(OUTPUT_FOLDER, "*.part"),
        os.path.join(OUTPUT_FOLDER, "*.ytdl"),
    ]

    total_removed = 0
    total_size = 0

    for pattern in patterns:
        files = glob.glob(pattern)

        if files:
            print(f"\nFound {len(files)} files matching: {os.path.basename(pattern)}")

            for file_path in files:
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    total_removed += 1
                    total_size += file_size
                    print(f"  ✓ Removed: {os.path.basename(file_path)} ({file_size} bytes)")
                except Exception as e:
                    print(f"  ✗ Error removing {os.path.basename(file_path)}: {e}")

    print("\n" + "="*60)
    if total_removed > 0:
        print(f"✓ Cleanup complete!")
        print(f"  Removed: {total_removed} files")
        print(f"  Freed: {total_size} bytes ({total_size / 1024:.2f} KB)")
    else:
        print("✓ No temporary files found - folder is clean!")
    print("="*60)

if __name__ == "__main__":
    cleanup_temp_files()
