"""HTML and PDF rendering: Jinja2 templating with WeasyPrint / headless browser fallback."""

import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from jinja2 import BaseLoader, Environment

from templates import GOOGLE_FONTS, TEMPLATES

try:
    from weasyprint import HTML as WeasyprintHTML
    WEASYPRINT_AVAILABLE = True
except Exception:
    WEASYPRINT_AVAILABLE = False

_BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    shutil.which("msedge"),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    shutil.which("google-chrome"),
]
_BROWSER_EXE = next((p for p in _BROWSER_CANDIDATES if p and Path(p).exists()), None)
BROWSER_AVAILABLE = _BROWSER_EXE is not None


def _html_to_pdf_browser(html_path: Path, pdf_path: Path, lang: str = "") -> bool:
    """Render PDF via headless Edge/Chrome when WeasyPrint is unavailable."""
    # Edge's --print-to-pdf fails on paths with spaces; use a temp staging dir.
    stage = Path(tempfile.mkdtemp(prefix="inv_stage_"))
    s_html = stage / "invoice.html"
    s_pdf = stage / "invoice.pdf"
    edge_d = tempfile.mkdtemp(prefix=f"edge_{lang}_")
    try:
        shutil.copy(html_path, s_html)
        subprocess.run(
            [
                _BROWSER_EXE,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                f"--user-data-dir={edge_d}",
                "--no-pdf-header-footer",
                f"--print-to-pdf={s_pdf}",
                s_html.as_uri(),
            ],
            capture_output=True,
            timeout=90,
        )
        time.sleep(3)
        if s_pdf.exists() and s_pdf.stat().st_size > 1000:
            shutil.copy(s_pdf, pdf_path)
            return True
        return False
    except Exception:
        return False
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        shutil.rmtree(edge_d, ignore_errors=True)


def render_and_save(data: dict, out_dir: Path, filename: str) -> bool:
    """Render invoice to HTML and attempt PDF conversion. Returns True if PDF was produced."""
    env = Environment(loader=BaseLoader())
    html_str = env.from_string(TEMPLATES[data["template"]]).render(**data, gfonts=GOOGLE_FONTS)

    html_path = out_dir / f"{filename}.html"
    html_path.write_text(html_str, encoding="utf-8")

    pdf_path = out_dir / f"{filename}.pdf"
    pdf_ok = False

    if WEASYPRINT_AVAILABLE:
        try:
            WeasyprintHTML(string=html_str, base_url=str(out_dir)).write_pdf(str(pdf_path))
            pdf_ok = True
        except Exception:
            pass

    if not pdf_ok and BROWSER_AVAILABLE:
        pdf_ok = _html_to_pdf_browser(html_path.resolve(), pdf_path, data["lang"])

    return pdf_ok


def pdf_engine_name() -> str:
    """Return a human-readable label for the active PDF rendering backend."""
    if WEASYPRINT_AVAILABLE:
        return "weasyprint"
    if BROWSER_AVAILABLE:
        return "Edge/Chrome headless"
    return "HTML only (no PDF engine found)"
