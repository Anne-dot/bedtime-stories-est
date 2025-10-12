#!/usr/bin/env python3
"""
Test script: Download 3 stories to verify manifest download method works reliably
Imports functions from manifest_downloader.py (DRY principle)
"""

import os
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manifest_downloader import extract_manifest_url, download_with_ytdlp, verify_audio

# Test URLs - 3 different stories (from CSV, saved=0, original)
TEST_STORIES = [
    {
        "title": "Hunt ja seitse kitsetalle",
        "url": "https://vikerraadio.err.ee/1609749707/ohtujutt-hunt-ja-seitse-kitsetalle"
    },
    {
        "title": "Lumivalgeke 2",
        "url": "https://vikerraadio.err.ee/1609749206/ohtujutt-lumivalgeke-2"
    },
    {
        "title": "Haldjas Piripill",
        "url": "https://vikerraadio.err.ee/1609747385/ohtujutt-haldjas-piripill"
    }
]

OUTPUT_FOLDER = "test_downloads"


def main():
    """Test downloading 3 stories sequentially"""
    print("="*60)
    print("TEST: Download 3 Stories with Manifest Method")
    print("="*60)

    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Statistics
    total_start = time.time()
    success_count = 0
    failed_count = 0
    total_duration = 0

    # Process each story
    for i, story in enumerate(TEST_STORIES, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/3] {story['title']}")
        print(f"{'='*60}")

        story_start = time.time()

        # Step 1: Extract manifest URL
        print(f"\n[1/3] Extract manifest URL")
        manifest_url = extract_manifest_url(story['url'])

        if not manifest_url:
            print(f"  ✗ Failed to extract URL")
            failed_count += 1
            continue

        # Step 2: Download
        print(f"\n[2/3] Download with yt-dlp")
        output_path = os.path.join(OUTPUT_FOLDER, f"{story['title']}.mp3")
        success = download_with_ytdlp(manifest_url, output_path)

        if not success:
            print(f"  ✗ Download failed")
            failed_count += 1
            continue

        # Step 3: Verify
        print(f"\n[3/3] Verify audio file")
        duration = verify_audio(output_path)

        if not duration:
            print(f"  ✗ Verification failed")
            failed_count += 1
            continue

        # Success!
        story_elapsed = time.time() - story_start
        success_count += 1
        total_duration += duration

        print(f"\n✓ Story {i}/3 completed in {story_elapsed:.1f}s")

    # Final statistics
    total_elapsed = time.time() - total_start

    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print(f"Successfully downloaded: {success_count}/3 stories")
    print(f"Failed: {failed_count}/3 stories")
    print(f"Total audio duration: {total_duration:.1f}s ({int(total_duration//60)}m{int(total_duration%60)}s)")
    print(f"Total time taken: {total_elapsed:.1f}s ({int(total_elapsed//60)}m{int(total_elapsed%60)}s)")

    if success_count == 3:
        avg_time = total_elapsed / 3
        print(f"\n💡 Average time per story: {avg_time:.1f}s")
        print(f"   Estimated time for 2344 stories: {(avg_time * 2344)/3600:.1f} hours")


if __name__ == "__main__":
    main()
