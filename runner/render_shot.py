"""Turn a test log, an HTML file, or a JMeter plan into a PNG via headless Chrome."""

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path


def chrome_bin():
    for name in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("chrome not found")


def shot(html_path, png_path, width, height):
    html_path = Path(html_path).resolve()
    png_path = Path(png_path).resolve()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            chrome_bin(),
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={width},{height}",
            f"--screenshot={png_path}",
            html_path.as_uri(),
        ],
        check=True,
    )
    print(png_path, png_path.stat().st_size)


def write_log_html(log_path, html_path, title):
    text = Path(log_path).read_text(encoding="utf-8", errors="replace")
    rows = []
    for line in text.splitlines():
        kind = ""
        upper = line.upper()
        if "FAIL" in upper or "ERROR" in upper:
            kind = "fail"
        elif "PASS" in upper or "100%" in line:
            kind = "ok"
        rows.append(f'<div class="{kind}">{html.escape(line) or "&nbsp;"}</div>')
    document = f"""<!doctype html><meta charset="utf-8">
<style>
body {{ margin:0; background:#111; color:#e6e6e6; font:18px/1.45 Consolas,monospace; padding:28px 32px 40px; }}
h1 {{ margin:0 0 16px; font:22px Segoe UI,sans-serif; color:#fff; }}
.ok {{ color:#3dd68c; }}
.fail {{ color:#ff6b6b; }}
</style>
<h1>{html.escape(title)}</h1>
{''.join(rows)}
"""
    Path(html_path).write_text(document, encoding="utf-8")


def write_plan_html(jmx_path, html_path, title):
    text = Path(jmx_path).read_text(encoding="utf-8")
    names = re.findall(r'testclass="([^"]+)"[^>]*testname="([^"]+)"', text)
    if not names:
        names = [("item", name) for name in re.findall(r'testname="([^"]+)"', text)]
    items = []
    for kind, name in names:
        if kind in ("hashTree", "Arguments", "LoopController", "SampleSaveConfiguration"):
            continue
        items.append(f"<li><b>{html.escape(kind)}</b> — {html.escape(name)}</li>")
    document = f"""<!doctype html><meta charset="utf-8">
<style>
body {{ margin:0; background:#f4f6f8; color:#1d2430; font:18px/1.4 Segoe UI,sans-serif; padding:28px; }}
h1 {{ margin:0 0 8px; font-size:26px; }}
p {{ margin:0 0 16px; color:#526070; }}
ul {{ background:#fff; border:1px solid #d5dde6; border-radius:8px; padding:18px 18px 18px 36px; }}
li {{ margin:6px 0; }}
</style>
<h1>{html.escape(title)}</h1>
<p>Узлы из файла плана JMeter, в порядке документа.</p>
<ul>{''.join(items)}</ul>
"""
    Path(html_path).write_text(document, encoding="utf-8")


def write_overlay(folder):
    folder = Path(folder)
    desktop = folder / "desktop-chrome.png"
    document = f"""<!doctype html><meta charset="utf-8">
<style>
body {{ margin:0; background:#222; }}
.stage {{ position:relative; width:1200px; height:700px; overflow:hidden; }}
.stage img {{ width:1200px; height:auto; display:block; filter:grayscale(0.15); }}
.frame {{ position:absolute; left:0; top:0; width:100%; height:118px; border:3px solid #e10600; box-sizing:border-box; background:rgba(225,6,0,0.18); }}
.label {{ position:absolute; left:16px; top:128px; background:#e10600; color:#fff; font:16px/1.3 Segoe UI,sans-serif; padding:8px 10px; max-width:520px; }}
</style>
<div class="stage">
  <img src="{desktop.name}" alt="">
  <div class="frame"></div>
  <div class="label">Контрольный каркас шапки 144 px против фактических 176 px на 1920×1080. Заголовка h1 на странице нет. На 360 и 375 px контент шире окна (405 px).</div>
</div>
"""
    html_path = folder / "overlay.html"
    html_path.write_text(document, encoding="utf-8")
    shot(html_path, folder / "perfectpixel-overlay.png", 1200, 760)


def main():
    mode = sys.argv[1]
    if mode == "log":
        log_path, png_path, title = sys.argv[2], sys.argv[3], sys.argv[4]
        html_path = Path(png_path).with_suffix(".html")
        write_log_html(log_path, html_path, title)
        shot(html_path, png_path, 1100, 700)
    elif mode == "plan":
        jmx_path, png_path, title = sys.argv[2], sys.argv[3], sys.argv[4]
        html_path = Path(png_path).with_suffix(".html")
        write_plan_html(jmx_path, html_path, title)
        shot(html_path, png_path, 1100, 760)
    elif mode == "html":
        shot(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif mode == "overlay":
        write_overlay(sys.argv[2])
    else:
        raise SystemExit("mode: log | plan | html | overlay")


if __name__ == "__main__":
    main()
