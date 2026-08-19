# bhunaksha_helper.py
# Opens official Bhunaksha portal + optional screenshot

import webbrowser
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def open_bhunaksha_in_browser(district=None, tehsil=None, village=None):
    """
    Official Bhunaksha portal browser mein kholta hai.
    User manually District → Tehsil → Village select karke plot dekh sakta hai.
    """
    url = "https://upbhunaksha.gov.in/"
    webbrowser.open(url)
    return True


def take_bhunaksha_screenshot(save_path="bhunaksha_map.png"):
    """
    Playwright se Bhunaksha homepage ka screenshot leta hai.
    (Full automatic plot selection complex hai, isliye homepage + guidance)
    """
    if not PLAYWRIGHT_AVAILABLE:
        return None, "Playwright install nahi hai. Run: pip install playwright && playwright install chromium"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto("https://upbhunaksha.gov.in/", timeout=60000)
            page.wait_for_timeout(4000)  # page load ke liye
            page.screenshot(path=save_path, full_page=False)
            browser.close()
        return save_path, None
    except Exception as e:
        return None, str(e)