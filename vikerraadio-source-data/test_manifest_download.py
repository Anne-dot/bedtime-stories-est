#!/usr/bin/env python3
"""
Test script: Extract manifest URL from ERR.ee page and download with yt-dlp
Tests if manifest download method works for all stories
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manifest_downloader import extract_manifest_url, download_with_ytdlp, verify_audio

# Test story URL
TEST_URL = "https://vikerraadio.err.ee/1609228655/ohtujutt-lugu-tuisumemmest-ja-kolmest-vallatust-tuulesellist"
OUTPUT_FOLDER = "test_downloads"


def main():
    """Test manifest download workflow"""
    print("="*60)
    print("TEST: Manifest Download Method")
    print("="*60)

    # Create output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Step 1: Extract manifest URL
    print(f"\n[1/3] Extract manifest URL from page")
    manifest_url = extract_manifest_url(TEST_URL)

    if not manifest_url:
        print("\n✗ TEST FAILED: Could not extract manifest URL")
        return

    # Step 2: Download with yt-dlp
    print(f"\n[2/3] Download with yt-dlp")
    output_path = os.path.join(OUTPUT_FOLDER, "test_story.mp3")
    success = download_with_ytdlp(manifest_url, output_path)

    if not success:
        print("\n✗ TEST FAILED: Download failed")
        return

    # Step 3: Verify audio
    print(f"\n[3/3] Verify audio file")
    duration = verify_audio(output_path)

    if not duration:
        print("\n✗ TEST FAILED: Could not verify audio")
        return

    # Success!
    print("\n" + "="*60)
    print("✓ TEST PASSED!")
    print("="*60)
    print(f"Manifest URL: {manifest_url}")
    print(f"Downloaded: {output_path}")
    print(f"Duration: {duration:.1f}s")
    print("\n💡 Manifest download method works!")
    print("   Ready to implement for all 2344 stories")


if __name__ == "__main__":
    main()
