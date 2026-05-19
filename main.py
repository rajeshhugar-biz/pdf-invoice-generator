"""
Multilingual GST-compliant invoice generator.

Usage:
  python main.py
  python main.py --count 3 --lang hi
  python main.py --count 10 --lang all --template 2
  python main.py --output ./my_invoices
"""

import argparse
import random
import sys
from pathlib import Path

from builder import LANG_NAMES, LANG_ORDER, build_invoice, load_data
from renderer import pdf_engine_name, render_and_save
from templates import TEMPLATE_NAMES

OUTPUT_DIR = Path(__file__).parent / "output"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Generate random GST-compliant invoices in multiple Indian languages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --count 3 --lang hi
  python main.py --count 10 --lang all --template 2
  python main.py --output ./my_invoices
        """,
    )
    parser.add_argument("--count", type=int, default=5,
                        help="Number of invoices per language (default: 5)")
    parser.add_argument("--lang", default="all", choices=LANG_ORDER + ["all"],
                        help="Language code or 'all' (default: all)")
    parser.add_argument("--output", default=OUTPUT_DIR,
                        help="Output directory (default: output/ next to main.py)")
    parser.add_argument("--template", type=int, default=0, choices=[0, 1, 2, 3, 4, 5],
                        help="Template 1–5, or 0 for random (default: 0)")
    args = parser.parse_args()

    vendors, customers, products = load_data()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    langs = LANG_ORDER if args.lang == "all" else [args.lang]

    print(f"PDF engine : {pdf_engine_name()}")
    print(f"Languages  : {', '.join(langs)}")
    print(f"Count      : {args.count} per language")
    print(f"Output     : {out.resolve()}\n")

    total_pdf = total_html = 0

    for lang in langs:
        lang_name = LANG_NAMES[lang]
        v_pool = vendors[lang]
        c_pool = customers[lang]
        p_pool = products[lang]

        for i in range(1, args.count + 1):
            tmpl_idx = args.template if args.template else random.randint(1, 5)
            vendor = random.choice(v_pool)
            customer = random.choice(c_pool)

            data = build_invoice(lang, vendor, customer, p_pool, tmpl_idx)
            filename = f"sample_{i}_{lang_name}"

            pdf_ok = render_and_save(data, out, filename)
            t_name = TEMPLATE_NAMES[tmpl_idx]

            if pdf_ok:
                print(f"  [PDF]  {filename}.pdf  (T{tmpl_idx}: {t_name})")
                total_pdf += 1
            else:
                print(f"  [HTML] {filename}.html  (T{tmpl_idx}: {t_name})  -- open in browser to print")
                total_html += 1

    print(f"\nDone.  PDF: {total_pdf}  HTML: {total_html}  -> {out.resolve()}")


if __name__ == "__main__":
    main()
