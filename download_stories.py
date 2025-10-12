#!/usr/bin/env python3
"""
Script to download bedtime stories using manifest method
Downloads stories marked as saved=0 in CSV catalog
Much faster than monitor recording (~5x speedup)
"""

import os
import time
import signal
from csv_manager import CSVManager
from manifest_downloader import extract_manifest_url, download_with_ytdlp, verify_audio

# Configuration - Global constants
OUTPUT_FOLDER = "Õhtujutt"
AUDIO_FORMAT = "mp3"
CSV_PATH = "ohtujutt_catalog.csv"
MAX_CONSECUTIVE_FAILURES = 5  # Stop if this many stories fail in a row (likely network issue)

# Global flag for graceful shutdown
shutdown_requested = False


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global shutdown_requested
    print("\n\n⚠ Shutdown requested. Finishing current story...")
    shutdown_requested = True


def cleanup_temp_files(output_folder):
    """Remove temporary files created by yt-dlp after successful download"""
    import glob

    patterns = [
        os.path.join(output_folder, "*.temp.mp3"),
        os.path.join(output_folder, "*.part"),
        os.path.join(output_folder, "*.ytdl"),
    ]

    removed_count = 0
    for pattern in patterns:
        for temp_file in glob.glob(pattern):
            try:
                os.remove(temp_file)
                removed_count += 1
            except Exception:
                pass  # Ignore errors

    return removed_count


def main():
    """Main function to download stories"""
    global shutdown_requested

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Setup
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Get user input
    user_input = input("How many stories to download? (Enter number or press Enter for all): ").strip()

    if user_input == "":
        max_stories = None
    else:
        try:
            max_stories = int(user_input)
        except ValueError:
            print("Invalid input. Downloading all stories.")
            max_stories = None

    # Initialize CSV manager
    csv_manager = CSVManager(CSV_PATH, OUTPUT_FOLDER, AUDIO_FORMAT)

    # Count total unsaved stories
    total_unsaved = sum(1 for story in csv_manager.stories.values()
                       if csv_manager._is_ready_to_record(story))

    # Statistics tracking
    downloaded_count = 0
    skipped_count = 0
    failed_count = 0
    consecutive_failures = 0
    start_time = time.time()
    total_duration = 0

    print(f"Starting to download stories...")
    print(f"Total unsaved stories in catalog: {total_unsaved}")
    if max_stories:
        print(f"Target: {max_stories} stories")
    else:
        print(f"Target: all unsaved stories")

    try:
        while True:
            # Check graceful shutdown
            if shutdown_requested:
                print("\n⚠ Stopping after current story...")
                break

            # Check limit
            if max_stories and downloaded_count >= max_stories:
                print(f"Reached target: {max_stories} stories")
                break

            # Check consecutive failures (possible network issue)
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print(f"\n⚠ WARNING: {MAX_CONSECUTIVE_FAILURES} consecutive failures detected!")
                print(f"⚠ This usually indicates a network problem.")
                print(f"⚠ Please check your internet connection and restart the script.")
                break

            # Get next story
            story = csv_manager.find_next_original_unsaved()
            if story is None:
                print("No more stories to download!")
                break

            # Progress header
            progress_count = downloaded_count + skipped_count + failed_count + 1
            print(f"\n{'='*60}")
            print(f"[{progress_count}/{total_unsaved}] {story['title']}")

            # Show ETA if we have data
            if downloaded_count > 0:
                elapsed = time.time() - start_time
                avg_time_per_story = elapsed / downloaded_count
                remaining_stories = total_unsaved - progress_count + 1
                eta_seconds = avg_time_per_story * remaining_stories
                eta_hours = eta_seconds / 3600
                print(f"Progress: {downloaded_count} downloaded, {skipped_count} skipped, {failed_count} failed")
                print(f"ETA: {eta_hours:.1f}h remaining (avg {avg_time_per_story:.0f}s/story)")
            print(f"{'='*60}")

            # Try to download story (with retry logic)
            try:
                file_path = os.path.join(OUTPUT_FOLDER, f"{story['title']}.{AUDIO_FORMAT}")
                download_success = False

                # Retry up to 3 times
                for attempt in range(3):
                    if attempt > 0:
                        print(f"  ⚠ Retry attempt {attempt}/2...")
                        # Remove previous broken file
                        if os.path.exists(file_path):
                            os.remove(file_path)

                    # Step 1: Extract manifest URL
                    manifest_url = extract_manifest_url(story['url'])

                    if not manifest_url:
                        print("  ✗ Could not extract manifest URL")
                        continue  # Try again

                    # Step 2: Download with yt-dlp
                    success = download_with_ytdlp(manifest_url, file_path)

                    if not success:
                        print("  ✗ Download failed")
                        continue  # Try again

                    # Step 3: Verify (quality control)
                    if csv_manager.mark_as_saved(story['url']):
                        downloaded_count += 1
                        total_duration += int(story['duration_seconds'])
                        consecutive_failures = 0  # Reset on success

                        # Step 4: Cleanup temp files
                        removed = cleanup_temp_files(OUTPUT_FOLDER)
                        if removed > 0:
                            print(f"  ✓ Cleaned up {removed} temp file(s)")

                        print(f"  ✓ Downloaded successfully")
                        download_success = True
                        break  # Success - exit retry loop
                    else:
                        failed_count += 1
                        print(f"  ✗ File verification failed")
                        # Remove broken file for retry
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        continue  # Try again

                # If all retries failed
                if not download_success:
                    print(f"  ✗ Failed after 3 attempts, skipping")
                    skipped_count += 1
                    consecutive_failures += 1

                csv_manager.save()

            except Exception as e:
                print(f"  ✗ Error: {e}")
                skipped_count += 1
                continue

    finally:
        # Final save
        csv_manager.save()

        # Final stats
        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        if shutdown_requested:
            print(f"⚠ Gracefully stopped by user")
        print(f"Download session complete!")
        print(f"Successfully downloaded: {downloaded_count} stories")
        print(f"Skipped: {skipped_count} stories")
        print(f"Failed verification: {failed_count} stories")
        print(f"Total audio duration: {total_duration}s ({total_duration//60}m)")
        print(f"Session time: {int(elapsed)}s ({int(elapsed)//60}m)")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
