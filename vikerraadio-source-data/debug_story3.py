#!/usr/bin/env python3
"""
Debug script: Check why story 3 extraction failed
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

URL = "https://vikerraadio.err.ee/1609812924/ohtujutt-lastele-tondilossi-ounapuu"

# Setup Chrome (NOT headless - so we can see what happens)
chrome_options = Options()
# chrome_options.add_argument("--headless=new")  # Commented out to see browser
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print(f"Opening: {URL}")
    driver.get(URL)

    print("Waiting 3s...")
    time.sleep(3)

    # Try to extract
    print("\nAttempting to extract manifest URL...")

    result = driver.execute_script("""
        try {
            // Check if pageControlData exists
            if (typeof window.pageControlData === 'undefined') {
                return {error: 'pageControlData undefined'};
            }

            // Check structure
            if (!window.pageControlData.playerInit) {
                return {error: 'playerInit missing'};
            }

            if (!window.pageControlData.playerInit.media) {
                return {error: 'media missing'};
            }

            if (!window.pageControlData.playerInit.media.config) {
                return {error: 'config missing'};
            }

            var mediaId = window.pageControlData.playerInit.media.config.mediaId;

            if (!mediaId) {
                return {error: 'mediaId missing', config: window.pageControlData.playerInit.media.config};
            }

            // Success
            var manifestUrl = 'https://vod.err.ee/dash/viker/' + mediaId + '/a/manifest.mpd';
            return {success: true, url: manifestUrl, mediaId: mediaId};

        } catch(e) {
            return {error: e.toString(), stack: e.stack};
        }
    """)

    print("\nResult:")
    print(result)

    # Wait so we can see browser
    print("\nKeeping browser open for 10s so you can inspect...")
    time.sleep(10)

finally:
    driver.quit()
