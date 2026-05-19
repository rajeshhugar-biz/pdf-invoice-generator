"""Delete intermediate HTML files left behind after PDF generation."""

import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"


def clean(directory: Path = OUTPUT_DIR) -> None:
    removed = 0
    for html_file in directory.rglob("*.html"):
        html_file.unlink()
        print(f"Deleted: {html_file}")
        removed += 1
    print(f"\nRemoved {removed} HTML file(s) from {directory}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else OUTPUT_DIR
    clean(target)
