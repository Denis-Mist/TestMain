"""Capture viewport screenshots and a few computed styles. Chrome, plus Firefox and Edge when installed."""

import json
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

URL = "https://www.detmir.ru/"
SIZES = [(1920, 1080), (1366, 768), (1024, 768), (768, 1024), (375, 812), (360, 640)]
ROOT = Path(__file__).resolve().parents[1]
SHOTS10 = ROOT / "10" / "screenshots"
SHOTS11 = ROOT / "11" / "screenshots"

SCRIPT = """
const body = getComputedStyle(document.body);
const header = document.querySelector('header');
const h1 = document.querySelector('h1');
const h1Style = h1 ? getComputedStyle(h1) : null;
return {
  title: document.title,
  url: location.href,
  scrollWidth: document.documentElement.scrollWidth,
  innerWidth: window.innerWidth,
  overflowX: document.documentElement.scrollWidth > window.innerWidth + 2,
  bodyBackground: body.backgroundColor,
  bodyFont: body.fontFamily,
  headerHeight: header ? Math.round(header.getBoundingClientRect().height) : null,
  h1: h1 ? { text: (h1.innerText || '').slice(0, 120), fontSize: h1Style.fontSize, color: h1Style.color } : null
};
"""


def chrome():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=ru-RU")
    return webdriver.Chrome(options=options)


def firefox():
    if not shutil.which("firefox"):
        return None
    options = FirefoxOptions()
    options.add_argument("-headless")
    return webdriver.Firefox(options=options)


def edge():
    binary = shutil.which("microsoft-edge") or shutil.which("microsoft-edge-stable")
    if not binary:
        return None
    options = EdgeOptions()
    options.binary_location = binary
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Edge(options=options)


def capture(driver, browser):
    rows = []
    for width, height in SIZES:
        driver.set_window_size(width, height)
        driver.get(URL)
        driver.implicitly_wait(3)
        metrics = driver.execute_script(SCRIPT)
        name = f"{width}x{height}-{browser}.png"
        driver.save_screenshot(str(SHOTS11 / name))
        if width == 1920 and browser == "chrome":
            driver.save_screenshot(str(SHOTS10 / "desktop-chrome.png"))
        rows.append({"browser": browser, "viewport": f"{width}x{height}", **metrics})
        print(browser, width, height, "overflow", metrics.get("overflowX"), "title", metrics.get("title"))
    return rows


def main():
    SHOTS10.mkdir(parents=True, exist_ok=True)
    SHOTS11.mkdir(parents=True, exist_ok=True)
    results = []
    errors = []
    for name, factory in (("chrome", chrome), ("firefox", firefox), ("edge", edge)):
        driver = None
        try:
            driver = factory()
            if driver is None:
                errors.append({"browser": name, "error": "not installed"})
                continue
            results.extend(capture(driver, name))
        except Exception as error:
            errors.append({"browser": name, "error": str(error)})
            print("FAIL", name, error)
        finally:
            if driver is not None:
                driver.quit()
    payload = {"url": URL, "results": results, "errors": errors}
    (SHOTS11 / "layout.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    desktop = next((row for row in results if row["browser"] == "chrome" and row["viewport"] == "1920x1080"), None)
    (SHOTS10 / "measured.json").write_text(json.dumps(desktop or {"error": errors}, ensure_ascii=False, indent=2), encoding="utf-8")
    if not any(row["browser"] == "chrome" for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
