#!/usr/bin/env python3
"""
Script to record bedtime stories based on CSV catalog
Refactored version with class-based architecture following MVP, DRY, and ADHD-friendly principles
"""

import os
import time
import subprocess
import signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from csv_manager import CSVManager

# Configuration - Global constants
OUTPUT_FOLDER = "Õhtujutt"
AUDIO_FORMAT = "mp3"
CSV_PATH = "ohtujutt_catalog.csv"
AUDIO_SOURCE = "alsa_output.pci-0000_00_1b.0.analog-stereo.monitor"

# Playback verification
PLAYBACK_CHECK_DELAY = 5  # seconds to wait before checking
PLAYBACK_CHECK_COUNT = 2  # how many times to check

# Global flag for graceful shutdown
shutdown_requested = False


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global shutdown_requested
    print("\n\n⚠ Shutdown requested. Finishing current story...")
    shutdown_requested = True


class BrowserController:
    """Manages browser operations - opens pages and controls playback"""

    def __init__(self):
        """Initialize browser controller and start Chrome driver"""
        self.driver = None
        self._setup_driver()

    def _setup_driver(self):
        """Helper: initialize Chrome WebDriver"""
        from selenium.webdriver.chrome.service import Service

        chrome_options = Options()
        service = Service('/usr/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def _open_new_tab(self, url):
        """Helper: open URL in new tab with timeout"""
        try:
            old_count = len(self.driver.window_handles)

            self.driver.execute_script("window.open(arguments[0], '_blank');", url)

            # Wait up to 5s for new tab to appear
            for i in range(10):
                time.sleep(0.5)
                new_count = len(self.driver.window_handles)

                if new_count == old_count + 1:
                    # Switch to new tab
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    return True

            # Timeout - tab did not appear
            print(f"  ✗ Timeout: new tab did not appear (waited 5s)")
            return False

        except Exception as e:
            print(f"  ✗ Error opening new tab: {e}")
            return False

    def _wait_for_page_load(self):
        """Helper: wait for page to load"""
        time.sleep(5)

    def open_story_in_new_tab(self, url):
        """Open story in new tab with retry logic"""
        for attempt in range(3):
            if self._open_new_tab(url):
                # Tab opened and switched successfully
                self._wait_for_page_load()
                return True

            # Retry
            if attempt < 2:  # Don't print on last attempt
                print(f"  ⚠ Retry {attempt + 1}/2...")

        # All retries failed
        print(f"  ✗ Failed to open story after 3 attempts")
        return False

    def close_story_tab(self):
        """Close current story tab and switch to remaining tab"""
        try:
            handles = self.driver.window_handles

            if len(handles) < 2:
                # Already only 1 tab (or none) - not an error
                return True

            # Close current tab
            self.driver.close()

            # Switch to remaining tab
            self.driver.switch_to.window(self.driver.window_handles[0])
            return True

        except Exception as e:
            print(f"  ✗ Error closing story tab: {e}")
            return False

    def click_play(self):
        """Find and click play button with mouse simulation"""
        for i in range(10):
            time.sleep(1)
            clicked = self._try_click_play_with_hover()
            if clicked:
                print(f"  ✓ Play button clicked after {i+1}s")
                return True

        print("  ✗ Play button not found after 10s")
        return False

    def _try_click_play_with_hover(self):
        """Helper: try to find play button, hover, and click"""
        try:
            # Find button element
            button = self.driver.find_element(By.CSS_SELECTOR, '.radio-player-play-button')

            if button:
                # Scroll button into view (center)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(0.3)

                # Simulate mouse hover
                ActionChains(self.driver).move_to_element(button).perform()
                time.sleep(0.3)

                # Click
                button.click()
                return True

        except Exception as e:
            # Element not found or not interactable
            return False

        return False

    def close(self):
        """Close browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"Warning: Could not close browser: {e}")
            self.driver = None


class AudioRecorder:
    """Manages audio recording - records browser audio to MP3 files"""

    def __init__(self):
        """Initialize audio recorder"""
        pass

    def _get_unique_filename(self, filepath):
        """Helper: get unique filename (add suffix if exists)"""
        if not os.path.exists(filepath):
            return filepath

        base, ext = os.path.splitext(filepath)
        counter = 2
        while os.path.exists(f"{base}_{counter}{ext}"):
            counter += 1
        return f"{base}_{counter}{ext}"

    def record(self, title, duration_seconds):
        """Record audio to file with fixed duration"""
        file_path = os.path.join(OUTPUT_FOLDER, f"{title}.{AUDIO_FORMAT}")

        # Get unique filename (adds _2, _3 if needed)
        file_path = self._get_unique_filename(file_path)

        duration = int(duration_seconds) + 2

        cmd = [
            'ffmpeg',
            '-f', 'pulse',
            '-i', AUDIO_SOURCE,
            '-t', str(duration),
            '-acodec', 'libmp3lame',
            '-b:a', '128k',
            '-y',
            file_path
        ]

        print(f"  Recording {duration}s to: {file_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"  ✗ FFmpeg error: {result.stderr}")
            return None

        return file_path


def main():
    """Main function to record stories"""
    global shutdown_requested

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Setup
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Get user input
    user_input = input("How many stories to record? (Enter number or press Enter for all): ").strip()

    if user_input == "":
        max_stories = None
    else:
        try:
            max_stories = int(user_input)
        except ValueError:
            print("Invalid input. Recording all stories.")
            max_stories = None

    # Initialize components
    csv_manager = CSVManager(CSV_PATH, OUTPUT_FOLDER, AUDIO_FORMAT)
    browser = BrowserController()
    recorder = AudioRecorder()

    # Statistics tracking
    recorded_count = 0
    skipped_count = 0
    failed_count = 0
    start_time = time.time()
    total_duration = 0

    print(f"Starting to record stories...")
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
            if max_stories and recorded_count >= max_stories:
                print(f"Reached target: {max_stories} stories")
                break

            # Get next story
            story = csv_manager.find_next_original_unsaved()
            if story is None:
                print("No more stories to record!")
                break

            print(f"\n[{recorded_count+1}] {story['title']}")

            # Try to record story
            try:
                # First story - use existing tab (browser just opened)
                if recorded_count == 0:
                    print("  Opening in main tab (first story)...")
                    browser.driver.get(story['url'])
                    time.sleep(5)  # Extra time for first story
                else:
                    # Subsequent stories - open in new tab
                    if not browser.open_story_in_new_tab(story['url']):
                        print("  ✗ Could not open story, skipping")
                        skipped_count += 1
                        continue

                if not browser.click_play():
                    print("  ✗ Play button not found, skipping")
                    if recorded_count > 0:  # Only close tab if not first story
                        browser.close_story_tab()
                    skipped_count += 1
                    continue

                file_path = recorder.record(story['title'], story['duration_seconds'])
                if not file_path:
                    print("  ✗ Recording failed, skipping")
                    if recorded_count > 0:  # Only close tab if not first story
                        browser.close_story_tab()
                    skipped_count += 1
                    continue

                # Verify and mark as saved
                if csv_manager.mark_as_saved(story['url']):
                    recorded_count += 1
                    total_duration += int(story['duration_seconds'])
                    print(f"  ✓ Recorded successfully")
                else:
                    failed_count += 1
                    print(f"  ✗ File not found - recording failed")

                csv_manager.save()

                # Close story tab before next iteration (not for first story)
                if recorded_count > 1:  # recorded_count already incremented
                    browser.close_story_tab()

            except Exception as e:
                print(f"  ✗ Error: {e}")
                browser.close_story_tab()
                skipped_count += 1
                continue

    finally:
        # Cleanup
        browser.close()
        csv_manager.save()

        # Final stats
        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        if shutdown_requested:
            print(f"⚠ Gracefully stopped by user")
        print(f"Recording session complete!")
        print(f"Successfully recorded: {recorded_count} stories")
        print(f"Skipped: {skipped_count} stories")
        print(f"Failed verification: {failed_count} stories")
        print(f"Total audio duration: {total_duration}s ({total_duration//60}m)")
        print(f"Session time: {int(elapsed)}s ({int(elapsed)//60}m)")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
