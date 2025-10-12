#!/usr/bin/env python3
"""
Manifest download module for ERR.ee stories
Extracts manifest URLs and downloads audio with yt-dlp
Used by download_stories.py and test scripts
"""

import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def extract_manifest_url(story_url):
    """
    Open story page with Selenium and extract manifest URL from pageControlData
    Returns: manifest.mpd URL or None
    """
    print(f"Opening: {story_url}")

    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in background
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open page
        driver.get(story_url)

        # Wait for page to load
        time.sleep(3)

        # Extract manifest URL from JavaScript object
        manifest_url = driver.execute_script("""
            try {
                // Get mediaId from pageControlData
                var mediaId = window.pageControlData.playerInit.media.config.mediaId;

                // Construct manifest URL
                var manifestUrl = 'https://vod.err.ee/dash/viker/' + mediaId + '/a/manifest.mpd';

                return manifestUrl;
            } catch(e) {
                return null;
            }
        """)

        if manifest_url:
            print(f"  ✓ Manifest URL: {manifest_url}")
        else:
            print(f"  ✗ Could not extract manifest URL")

        return manifest_url

    finally:
        driver.quit()


def download_with_ytdlp(manifest_url, output_path, show_progress=True):
    """
    Download audio using yt-dlp
    Returns: True if successful, False otherwise
    """
    start = time.time()

    if show_progress:
        print(f"Downloading with yt-dlp...")
    else:
        print(f"Downloading with yt-dlp (progress hidden)...")

    cmd = [
        'yt-dlp',
        manifest_url,
        '-o', output_path,
    ]

    # Add progress flag if requested
    if show_progress:
        cmd.append('--progress')
    else:
        cmd.append('--no-warnings')

    try:
        if show_progress:
            # Show progress - don't capture output
            result = subprocess.run(cmd, timeout=300)
        else:
            # Hide progress - capture output
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            # Debug: show stderr if there were any issues
            if result.stderr and ('error' in result.stderr.lower() or 'warning' in result.stderr.lower()):
                print(f"  ⚠ yt-dlp messages: {result.stderr[:300]}")

        elapsed = time.time() - start

        # Check if file exists (ignore postprocessing errors)
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"  ✓ Downloaded: {output_path}")
            print(f"  ✓ Size: {file_size:.2f} MB")
            print(f"  ✓ Time: {elapsed:.1f}s")
            return True
        else:
            print(f"  ✗ File not created")
            return False

    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout (5 min)")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def verify_audio(file_path):
    """
    Verify downloaded audio file with ffmpeg
    Returns: duration in seconds or None
    """
    print(f"Verifying audio...")

    cmd = ['ffmpeg', '-i', file_path, '-hide_banner']

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse duration from stderr
        for line in result.stderr.split('\n'):
            if 'Duration:' in line:
                # Extract: Duration: 00:08:47.21
                parts = line.split('Duration:')[1].split(',')[0].strip()
                h, m, s = parts.split(':')
                duration = int(h) * 3600 + int(m) * 60 + float(s)

                print(f"  ✓ Duration: {duration:.1f}s ({int(duration//60)}m{int(duration%60)}s)")
                return duration

        print(f"  ✗ Could not parse duration")
        return None

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None
