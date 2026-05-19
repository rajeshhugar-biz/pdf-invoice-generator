"""Invoice data assembly: loads JSON data files and builds invoice dicts."""

import json
import random
from datetime import date, timedelta
from pathlib import Path

from formatters import amount_in_words, fmt_inr, random_invoice_no
from labels import LABELS

DATA_DIR = Path(__file__).parent / "data"

LANG_ORDER = ["en", "hi", "mr", "kn", "bn", "ta", "te"]
LANG_NAMES = {
    "en": "english",
    "hi": "hindi",
    "mr": "marathi",
    "kn": "kannada",
    "bn": "bengali",
    "ta": "tamil",
    "te": "telugu",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_data() -> tuple[dict, dict, dict]:
    """Return (vendors, customers, products) dicts keyed by language code."""
    return (
        load_json(DATA_DIR / "vendors.json"),
        load_json(DATA_DIR / "customers.json"),
        load_json(DATA_DIR / "products.json"),
    )


def build_invoice(
    lang: str,
    vendor: dict,
    customer: dict,
    products: list[dict],
    template_idx: int,
) -> dict:
    """Assemble all data needed to render a single invoice."""
    num_items = random.randint(2, 5)
    selected = random.sample(products, min(num_items, len(products)))

    items: list[dict] = []
    subtotal = 0.0
    for idx, prod in enumerate(selected, 1):
        qty = random.randint(1, 8)
        price = round(prod["unit_price"] * random.uniform(0.92, 1.10), 2)
        amt = round(qty * price, 2)
        subtotal += amt
        items.append({**prod, "sr": idx, "qty": qty, "unit_price": price, "amount": amt})

    gst_type = random.choice(["cgst_sgst", "igst"])
    if gst_type == "cgst_sgst":
        cgst = round(subtotal * 0.09, 2)
        sgst = round(subtotal * 0.09, 2)
        igst = 0.0
        total = subtotal + cgst + sgst
    else:
        cgst = 0.0
        sgst = 0.0
        igst = round(subtotal * 0.18, 2)
        total = subtotal + igst

    days_ago = random.randint(0, 30)
    inv_date = date.today() - timedelta(days=days_ago)
    due_offset = random.choice([15, 30, 45, 60])
    due_date = inv_date + timedelta(days=due_offset)

    return {
        "lang": lang,
        "labels": LABELS[lang],
        "vendor": vendor,
        "customer": customer,
        "invoice_no": random_invoice_no(vendor["gstin"][:2]),
        "invoice_date": inv_date.strftime("%d %b %Y"),
        "due_date": due_date.strftime("%d %b %Y"),
        "line_items": items,
        "subtotal": subtotal,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "gst_type": gst_type,
        "total": total,
        "fmt_inr": fmt_inr,
        "amount_words": amount_in_words(total),
        "template": template_idx,
    }
