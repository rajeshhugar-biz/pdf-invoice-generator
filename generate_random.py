"""
Random Multilingual Invoice Generator
Generates GST-compliant invoices in 5 visual formats across 7 Indian languages.

Usage:
  python generate_random.py --count 5
  python generate_random.py --count 3 --lang hi
  python generate_random.py --count 10 --lang all --output ./my_invoices
"""

import argparse
import json
import random
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

try:
    from jinja2 import Environment, BaseLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

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
_BROWSER_EXE   = next((p for p in _BROWSER_CANDIDATES if p and Path(p).exists()), None)
BROWSER_AVAILABLE = _BROWSER_EXE is not None

DATA_DIR   = Path(__file__).parent / "data"
LANG_ORDER = ["en", "hi", "mr", "kn", "bn", "ta", "te"]
LANG_NAMES = {"en": "english", "hi": "hindi", "mr": "marathi",
              "kn": "kannada", "bn": "bengali", "ta": "tamil", "te": "telugu"}

# ── Labels (all UI text in each language) ─────────────────────────────────────

LABELS = {
    "en": {"font": "Arial, sans-serif",
           "invoice": "TAX INVOICE", "invoice_no": "Invoice No.", "date": "Date",
           "due_date": "Due Date", "bill_to": "Bill To", "ship_to": "Ship To",
           "vendor": "Vendor", "gstin": "GSTIN", "pan": "PAN", "hsn": "HSN",
           "description": "Description", "qty": "Qty", "unit": "Unit",
           "unit_price": "Unit Price (₹)", "amount": "Amount (₹)",
           "subtotal": "Subtotal", "cgst": "CGST (9%)", "sgst": "SGST (9%)",
           "igst": "IGST (18%)", "total": "Total",
           "amount_in_words": "Amount in Words", "bank_details": "Bank Details",
           "bank_name": "Bank Name", "account_no": "Account No.", "ifsc": "IFSC Code",
           "terms": "Terms & Conditions",
           "terms_text": "Payment due within 30 days of invoice date. Goods once sold will not be taken back.",
           "authorized_signatory": "Authorized Signatory", "original": "ORIGINAL"},
    "hi": {"font": "'Noto Sans Devanagari', Mangal, Arial, sans-serif",
           "invoice": "कर चालान", "invoice_no": "चालान संख्या", "date": "दिनांक",
           "due_date": "देय तिथि", "bill_to": "बिल प्राप्तकर्ता", "ship_to": "शिपिंग पता",
           "vendor": "विक्रेता", "gstin": "जीएसटीआईएन", "pan": "पैन", "hsn": "एचएसएन",
           "description": "विवरण", "qty": "मात्रा", "unit": "इकाई",
           "unit_price": "इकाई मूल्य (₹)", "amount": "राशि (₹)",
           "subtotal": "उप-योग", "cgst": "सीजीएसटी (9%)", "sgst": "एसजीएसटी (9%)",
           "igst": "आईजीएसटी (18%)", "total": "कुल राशि",
           "amount_in_words": "राशि शब्दों में", "bank_details": "बैंक विवरण",
           "bank_name": "बैंक का नाम", "account_no": "खाता संख्या", "ifsc": "आईएफएससी कोड",
           "terms": "नियम और शर्तें",
           "terms_text": "चालान दिनांक के 30 दिनों के भीतर भुगतान देय है। बेचे गए माल वापस नहीं लिए जाएंगे।",
           "authorized_signatory": "अधिकृत हस्ताक्षरकर्ता", "original": "मूल प्रति"},
    "mr": {"font": "'Noto Sans Devanagari', Mangal, Arial, sans-serif",
           "invoice": "कर बीजक", "invoice_no": "बीजक क्रमांक", "date": "दिनांक",
           "due_date": "देय तारीख", "bill_to": "बिल प्राप्तकर्ता", "ship_to": "शिपिंग पत्ता",
           "vendor": "विक्रेता", "gstin": "जीएसटीआयएन", "pan": "पॅन", "hsn": "एचएसएन",
           "description": "वर्णन", "qty": "प्रमाण", "unit": "एकक",
           "unit_price": "एकक किंमत (₹)", "amount": "रक्कम (₹)",
           "subtotal": "उप-एकूण", "cgst": "सीजीएसटी (9%)", "sgst": "एसजीएसटी (9%)",
           "igst": "आयजीएसटी (18%)", "total": "एकूण रक्कम",
           "amount_in_words": "रक्कम शब्दात", "bank_details": "बँक तपशील",
           "bank_name": "बँकेचे नाव", "account_no": "खाते क्रमांक", "ifsc": "आयएफएससी कोड",
           "terms": "अटी व शर्ती",
           "terms_text": "बीजक दिनांकापासून 30 दिवसांत पैसे भरणे आवश्यक आहे। विकलेला माल परत घेतला जाणार नाही।",
           "authorized_signatory": "अधिकृत स्वाक्षरीकर्ता", "original": "मूळ प्रत"},
    "kn": {"font": "'Noto Sans Kannada', Tunga, Arial, sans-serif",
           "invoice": "ತೆರಿಗೆ ಇನ್‌ವಾಯಿಸ್", "invoice_no": "ಇನ್‌ವಾಯಿಸ್ ಸಂಖ್ಯೆ", "date": "ದಿನಾಂಕ",
           "due_date": "ಪಾವತಿ ದಿನಾಂಕ", "bill_to": "ಬಿಲ್ ಸ್ವೀಕರಿಸುವವರು", "ship_to": "ಶಿಪ್ಪಿಂಗ್ ವಿಳಾಸ",
           "vendor": "ಮಾರಾಟಗಾರರು", "gstin": "ಜಿಎಸ್‌ಟಿಐಎನ್", "pan": "ಪ್ಯಾನ್", "hsn": "ಎಚ್‌ಎಸ್‌ಎನ್",
           "description": "ವಿವರಣೆ", "qty": "ಪ್ರಮಾಣ", "unit": "ಘಟಕ",
           "unit_price": "ಘಟಕ ಬೆಲೆ (₹)", "amount": "ಮೊತ್ತ (₹)",
           "subtotal": "ಉಪ-ಮೊತ್ತ", "cgst": "ಸಿಜಿಎಸ್‌ಟಿ (9%)", "sgst": "ಎಸ್‌ಜಿಎಸ್‌ಟಿ (9%)",
           "igst": "ಐಜಿಎಸ್‌ಟಿ (18%)", "total": "ಒಟ್ಟು ಮೊತ್ತ",
           "amount_in_words": "ಪದಗಳಲ್ಲಿ ಮೊತ್ತ", "bank_details": "ಬ್ಯಾಂಕ್ ವಿವರಗಳು",
           "bank_name": "ಬ್ಯಾಂಕ್ ಹೆಸರು", "account_no": "ಖಾತೆ ಸಂಖ್ಯೆ", "ifsc": "ಐಎಫ್‌ಎಸ್‌ಸಿ ಕೋಡ್",
           "terms": "ನಿಯಮಗಳು ಮತ್ತು ಷರತ್ತುಗಳು",
           "terms_text": "ಇನ್‌ವಾಯಿಸ್ ದಿನಾಂಕದಿಂದ 30 ದಿನಗಳಲ್ಲಿ ಪಾವತಿ ಮಾಡಬೇಕು. ಮಾರಿದ ಸರಕನ್ನು ಹಿಂತಿರುಗಿಸಲಾಗದು.",
           "authorized_signatory": "ಅಧಿಕೃತ ಸಹಿಗಾರ", "original": "ಮೂಲ ಪ್ರತಿ"},
    "bn": {"font": "'Noto Sans Bengali', Vrinda, Arial, sans-serif",
           "invoice": "কর চালান", "invoice_no": "চালান নম্বর", "date": "তারিখ",
           "due_date": "দেয় তারিখ", "bill_to": "বিল প্রাপক", "ship_to": "শিপিং ঠিকানা",
           "vendor": "বিক্রেতা", "gstin": "জিএসটিআইএন", "pan": "প্যান", "hsn": "এইচএসএন",
           "description": "বিবরণ", "qty": "পরিমাণ", "unit": "একক",
           "unit_price": "একক মূল্য (₹)", "amount": "মোট (₹)",
           "subtotal": "উপ-মোট", "cgst": "সিজিএসটি (9%)", "sgst": "এসজিএসটি (9%)",
           "igst": "আইজিএসটি (18%)", "total": "মোট পরিমাণ",
           "amount_in_words": "কথায় পরিমাণ", "bank_details": "ব্যাংক বিবরণ",
           "bank_name": "ব্যাংকের নাম", "account_no": "অ্যাকাউন্ট নম্বর", "ifsc": "আইএফএসসি কোড",
           "terms": "শর্তাবলী",
           "terms_text": "চালানের তারিখ থেকে ৩০ দিনের মধ্যে পেমেন্ট করতে হবে। বিক্রীত পণ্য ফেরত নেওয়া হবে না।",
           "authorized_signatory": "অনুমোদিত স্বাক্ষরকারী", "original": "মূল কপি"},
    "ta": {"font": "'Noto Sans Tamil', Latha, Arial, sans-serif",
           "invoice": "வரி விலைப்பட்டியல்", "invoice_no": "விலைப்பட்டியல் எண்", "date": "தேதி",
           "due_date": "செலுத்த வேண்டிய தேதி", "bill_to": "பில் பெறுநர்", "ship_to": "அனுப்பும் முகவரி",
           "vendor": "விற்பனையாளர்", "gstin": "ஜிஎஸ்டிஐஎன்", "pan": "பான்", "hsn": "எச்எஸ்என்",
           "description": "விவரம்", "qty": "அளவு", "unit": "அலகு",
           "unit_price": "அலகு விலை (₹)", "amount": "தொகை (₹)",
           "subtotal": "துணை மொத்தம்", "cgst": "சிஜிஎஸ்டி (9%)", "sgst": "எஸ்ஜிஎஸ்டி (9%)",
           "igst": "ஐஜிஎஸ்டி (18%)", "total": "மொத்த தொகை",
           "amount_in_words": "வார்த்தைகளில் தொகை", "bank_details": "வங்கி விவரங்கள்",
           "bank_name": "வங்கியின் பெயர்", "account_no": "கணக்கு எண்", "ifsc": "ஐஎஃப்எஸ்சி குறியீடு",
           "terms": "விதிமுறைகள்",
           "terms_text": "விலைப்பட்டியல் தேதியிலிருந்து 30 நாட்களுக்குள் கட்டணம் செலுத்தவும். விற்கப்பட்ட பொருட்கள் திரும்பப் பெறப்படாது.",
           "authorized_signatory": "அங்கீகரிக்கப்பட்ட கையொப்பமிடுபவர்", "original": "அசல் நகல்"},
    "te": {"font": "'Noto Sans Telugu', Gautami, Arial, sans-serif",
           "invoice": "పన్ను ఇన్వాయిస్", "invoice_no": "ఇన్వాయిస్ నంబర్", "date": "తేదీ",
           "due_date": "చెల్లింపు తేదీ", "bill_to": "బిల్ స్వీకర్త", "ship_to": "షిప్పింగ్ చిరునామా",
           "vendor": "విక్రేత", "gstin": "జిఎస్టిఐఎన్", "pan": "పాన్", "hsn": "హెచ్‌ఎస్‌ఎన్",
           "description": "వివరణ", "qty": "పరిమాణం", "unit": "యూనిట్",
           "unit_price": "యూనిట్ ధర (₹)", "amount": "మొత్తం (₹)",
           "subtotal": "ఉప-మొత్తం", "cgst": "సిజిఎస్టి (9%)", "sgst": "ఎస్జిఎస్టి (9%)",
           "igst": "ఐజిఎస్టి (18%)", "total": "మొత్తం",
           "amount_in_words": "మాటలలో మొత్తం", "bank_details": "బ్యాంక్ వివరాలు",
           "bank_name": "బ్యాంక్ పేరు", "account_no": "ఖాతా నంబర్", "ifsc": "ఐఎఫ్ఎస్సి కోడ్",
           "terms": "నిబంధనలు",
           "terms_text": "ఇన్వాయిస్ తేదీ నుండి 30 రోజులలోపు చెల్లించాలి. అమ్మిన వస్తువులు తిరిగి తీసుకోబడవు.",
           "authorized_signatory": "అధికారిక సంతకం చేసేవారు", "original": "అసలు కాపీ"},
}

# ── Number helpers ────────────────────────────────────────────────────────────

def fmt_inr(amount: float) -> str:
    s = f"{amount:.2f}"
    ip, dp = s.split(".")
    if len(ip) > 3:
        last3 = ip[-3:]
        rest  = ip[:-3]
        groups = []
        while len(rest) > 2:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.insert(0, rest)
        ip = ",".join(groups) + "," + last3
    return f"{ip}.{dp}"


_ONES = ["","One","Two","Three","Four","Five","Six","Seven","Eight","Nine",
         "Ten","Eleven","Twelve","Thirteen","Fourteen","Fifteen","Sixteen",
         "Seventeen","Eighteen","Nineteen"]
_TENS = ["","","Twenty","Thirty","Forty","Fifty","Sixty","Seventy","Eighty","Ninety"]


def _w3(n):
    if n == 0: return ""
    if n < 20: return _ONES[n]
    if n < 100: return _TENS[n//10] + (" " + _ONES[n%10] if n%10 else "")
    return _ONES[n//100] + " Hundred" + (" " + _w3(n%100) if n%100 else "")


def amount_in_words(amount: float) -> str:
    paise   = round(amount * 100)
    rupees  = paise // 100
    paise  %= 100
    if rupees == 0:
        rs = "Zero"
    else:
        cr = rupees // 10_000_000; rupees %= 10_000_000
        lk = rupees // 100_000;    rupees %= 100_000
        th = rupees // 1000;       rupees %= 1000
        parts = []
        if cr: parts.append(_w3(cr) + " Crore")
        if lk: parts.append(_w3(lk) + " Lakh")
        if th: parts.append(_w3(th) + " Thousand")
        if rupees: parts.append(_w3(rupees))
        rs = " ".join(parts)
    result = f"Rupees {rs}"
    if paise: result += f" and {_w3(paise)} Paise"
    return result + " Only"


# ── Invoice number formats ────────────────────────────────────────────────────

def random_invoice_no(state_code="27"):
    y  = date.today().year
    ym = date.today().strftime("%Y%m")
    n  = random.randint(1000, 9999)
    s  = random.randint(100,  999)
    formats = [
        f"INV-{y}-{n}",
        f"BILL/{y}-{str(y+1)[-2:]}/{s:03d}",
        f"TAX-INV-{n}{s}",
        f"{state_code}/INV/{ym}/{n}",
        f"{y}-{date.today().month:02d}-{n}",
    ]
    return random.choice(formats)


# ── Build invoice data dict ───────────────────────────────────────────────────

def build_invoice(lang, vendor, customer, products, template_idx):
    num_items = random.randint(2, 5)
    selected  = random.sample(products, min(num_items, len(products)))

    items    = []
    subtotal = 0.0
    for idx, prod in enumerate(selected, 1):
        qty = random.randint(1, 8)
        # randomise price ±10%
        price = round(prod["unit_price"] * random.uniform(0.92, 1.10), 2)
        amt   = round(qty * price, 2)
        subtotal += amt
        items.append({**prod, "sr": idx, "qty": qty, "unit_price": price, "amount": amt})

    gst_type = random.choice(["cgst_sgst", "igst"])
    if gst_type == "cgst_sgst":
        cgst  = round(subtotal * 0.09, 2)
        sgst  = round(subtotal * 0.09, 2)
        igst  = 0.0
        total = subtotal + cgst + sgst
    else:
        cgst  = 0.0
        sgst  = 0.0
        igst  = round(subtotal * 0.18, 2)
        total = subtotal + igst

    days_ago   = random.randint(0, 30)
    inv_date   = date.today() - timedelta(days=days_ago)
    due_offset = random.choice([15, 30, 45, 60])
    due_date   = inv_date + timedelta(days=due_offset)

    return {
        "lang":         lang,
        "labels":       LABELS[lang],
        "vendor":       vendor,
        "customer":     customer,
        "invoice_no":   random_invoice_no(vendor["gstin"][:2]),
        "invoice_date": inv_date.strftime("%d %b %Y"),
        "due_date":     due_date.strftime("%d %b %Y"),
        "line_items":   items,
        "subtotal":     subtotal,
        "cgst":         cgst,
        "sgst":         sgst,
        "igst":         igst,
        "gst_type":     gst_type,
        "total":        total,
        "fmt_inr":      fmt_inr,
        "amount_words": amount_in_words(total),
        "template":     template_idx,
    }


# ── 5 HTML templates ──────────────────────────────────────────────────────────

GOOGLE_FONTS = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Noto+Sans:wght@400;700"
    "&family=Noto+Sans+Devanagari:wght@400;700"
    "&family=Noto+Sans+Kannada:wght@400;700"
    "&family=Noto+Sans+Bengali:wght@400;700"
    "&family=Noto+Sans+Tamil:wght@400;700"
    "&family=Noto+Sans+Telugu:wght@400;700"
    "&display=swap');"
)

# ── Template 1: Blue Corporate ────────────────────────────────────────────────
T1 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
<style>
{{ gfonts }}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:{{ labels.font }};font-size:11pt;color:#222;padding:32px 40px;background:#fff}
.page{max-width:800px;margin:auto}
.header{display:flex;justify-content:space-between;align-items:flex-start;
         border-bottom:3px solid #1a5276;padding-bottom:14px;margin-bottom:18px}
.co-name{font-size:18pt;font-weight:bold;color:#1a5276}
.co-meta{font-size:9pt;color:#555;margin-top:4px;line-height:1.7}
.inv-title{text-align:right}.inv-title h1{font-size:22pt;color:#1a5276}
.inv-title .badge{display:inline-block;background:#1a5276;color:#fff;font-size:8pt;
                   padding:2px 8px;border-radius:3px;margin-bottom:4px}
.inv-title .inv-no{font-size:10pt;color:#444;margin-top:4px}
.info-row{display:flex;gap:14px;margin-bottom:18px}
.info-box{flex:1;border:1px solid #d5d8dc;border-radius:4px;padding:10px 13px;background:#f8f9fa}
.info-box h3{font-size:8.5pt;text-transform:uppercase;color:#7f8c8d;letter-spacing:.5px;
              margin-bottom:5px;border-bottom:1px solid #eaecee;padding-bottom:3px}
.info-box p{font-size:10pt;line-height:1.7;white-space:pre-line}
.info-box .sub{font-size:9pt;color:#555;margin-top:3px}
.date-box{min-width:175px;flex:0 0 auto}
.drow{display:flex;justify-content:space-between;font-size:10pt;padding:3px 0}
.drow span:first-child{color:#7f8c8d}.drow span:last-child{font-weight:bold}
table{width:100%;border-collapse:collapse}
thead th{background:#1a5276;color:#fff;padding:8px 9px;font-size:9pt;text-align:left}
thead th.r{text-align:right}
tbody tr:nth-child(even){background:#eaf0fb}
tbody td{padding:7px 9px;font-size:10pt;border-bottom:1px solid #e8e8e8}
tbody td.r{text-align:right;font-family:'Courier New',monospace}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end}
.totals{width:300px;border:1px solid #d5d8dc;border-top:none}
.trow{display:flex;justify-content:space-between;padding:5px 11px;font-size:10pt;border-bottom:1px solid #eee}
.trow.grand{background:#1a5276;color:#fff;font-weight:bold;font-size:11pt;border:none}
.trow span:last-child{font-family:'Courier New',monospace}
.words{margin-top:13px;padding:9px 13px;background:#eaf0fb;border-left:4px solid #1a5276;font-size:10pt}
.words strong{color:#1a5276}
.foot-row{display:flex;gap:14px;margin-top:15px}
.bank-box,.terms-box{flex:1;border:1px solid #d5d8dc;border-radius:4px;padding:10px 13px}
.bank-box h3,.terms-box h3{font-size:8.5pt;text-transform:uppercase;color:#7f8c8d;letter-spacing:.5px;margin-bottom:5px}
.brow{display:flex;gap:8px;font-size:10pt;padding:2px 0}
.brow span:first-child{color:#7f8c8d;min-width:105px}
.terms-box p{font-size:9.5pt;color:#444;line-height:1.6}
.sig{margin-top:28px;text-align:right;padding-right:18px}
.sig-line{border-top:1px solid #444;width:190px;display:inline-block;margin-bottom:3px}
.sig-co{font-size:10pt;font-weight:bold;color:#1a5276}.sig-lbl{font-size:9.5pt;color:#555}
.pg-foot{margin-top:22px;border-top:2px solid #1a5276;padding-top:7px;
          text-align:center;font-size:8.5pt;color:#7f8c8d}
</style></head><body><div class="page">
<div class="header">
  <div>
    <div class="co-name">{{ vendor.name }}</div>
    <div class="co-meta">{{ vendor.address }}<br>
      {{ vendor.phone }} &nbsp;|&nbsp; {{ vendor.email }}<br>
      {{ labels.gstin }}: {{ vendor.gstin }} &nbsp;|&nbsp; {{ labels.pan }}: {{ vendor.pan }}
    </div>
  </div>
  <div class="inv-title">
    <div class="badge">{{ labels.original }}</div>
    <h1>{{ labels.invoice }}</h1>
    <div class="inv-no">{{ labels.invoice_no }}: <strong>{{ invoice_no }}</strong></div>
  </div>
</div>
<div class="info-row">
  <div class="info-box">
    <h3>{{ labels.bill_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
    <p class="sub">{{ labels.gstin }}: {{ customer.gstin }}</p>
  </div>
  <div class="info-box">
    <h3>{{ labels.ship_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
  </div>
  <div class="info-box date-box">
    <h3>{{ labels.date }}</h3>
    <div class="drow"><span>{{ labels.date }}</span><span>{{ invoice_date }}</span></div>
    <div class="drow"><span>{{ labels.due_date }}</span><span>{{ due_date }}</span></div>
  </div>
</div>
<table>
  <thead><tr>
    <th style="width:30px">#</th><th>{{ labels.description }}</th>
    <th style="width:60px">{{ labels.hsn }}</th>
    <th class="r" style="width:44px">{{ labels.qty }}</th>
    <th style="width:46px">{{ labels.unit }}</th>
    <th class="r" style="width:100px">{{ labels.unit_price }}</th>
    <th class="r" style="width:100px">{{ labels.amount }}</th>
  </tr></thead>
  <tbody>
  {% for i in line_items %}
    <tr><td class="c">{{ i.sr }}</td><td>{{ i.description }}</td>
    <td class="c">{{ i.hsn }}</td>
    <td class="r">{{ i.qty }}</td><td class="c">{{ i.unit }}</td>
    <td class="r">{{ fmt_inr(i.unit_price) }}</td>
    <td class="r">{{ fmt_inr(i.amount) }}</td></tr>
  {% endfor %}
  </tbody>
</table>
<div class="totals-wrap"><div class="totals">
  <div class="trow"><span>{{ labels.subtotal }}</span><span>₹ {{ fmt_inr(subtotal) }}</span></div>
  {% if gst_type == 'cgst_sgst' %}
  <div class="trow"><span>{{ labels.cgst }}</span><span>₹ {{ fmt_inr(cgst) }}</span></div>
  <div class="trow"><span>{{ labels.sgst }}</span><span>₹ {{ fmt_inr(sgst) }}</span></div>
  {% else %}
  <div class="trow"><span>{{ labels.igst }}</span><span>₹ {{ fmt_inr(igst) }}</span></div>
  {% endif %}
  <div class="trow grand"><span>{{ labels.total }}</span><span>₹ {{ fmt_inr(total) }}</span></div>
</div></div>
<div class="words"><strong>{{ labels.amount_in_words }}:</strong> {{ amount_words }}</div>
<div class="foot-row">
  <div class="bank-box"><h3>{{ labels.bank_details }}</h3>
    <div class="brow"><span>{{ labels.bank_name }}:</span><span>{{ vendor.bank_name }}</span></div>
    <div class="brow"><span>{{ labels.account_no }}:</span><span>{{ vendor.account_no }}</span></div>
    <div class="brow"><span>{{ labels.ifsc }}:</span><span>{{ vendor.ifsc }}</span></div>
  </div>
  <div class="terms-box"><h3>{{ labels.terms }}</h3><p>{{ labels.terms_text }}</p></div>
</div>
<div class="sig">
  <div class="sig-line"></div><br>
  <div class="sig-co">{{ vendor.name }}</div>
  <div class="sig-lbl">{{ labels.authorized_signatory }}</div>
</div>
<div class="pg-foot">{{ vendor.name }} | {{ vendor.gstin }} | {{ vendor.email }} | Computer generated invoice</div>
</div></body></html>"""


# ── Template 2: Emerald Green ─────────────────────────────────────────────────
T2 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
<style>
{{ gfonts }}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:{{ labels.font }};font-size:11pt;color:#1a1a1a;padding:0;background:#fff}
.page{max-width:800px;margin:auto}
.header{background:#1e8449;color:#fff;padding:22px 32px;display:flex;justify-content:space-between;align-items:center}
.co-name{font-size:16pt;font-weight:bold;letter-spacing:.3px}
.co-sub{font-size:8.5pt;opacity:.85;margin-top:3px;line-height:1.6}
.inv-badge{text-align:right}
.inv-badge h1{font-size:20pt;font-weight:bold;letter-spacing:1px}
.inv-badge .no{font-size:9.5pt;margin-top:5px;opacity:.9}
.body{padding:22px 32px}
.meta-row{display:flex;gap:18px;margin-bottom:20px}
.meta-box{flex:1;border-bottom:2px solid #1e8449;padding-bottom:10px}
.meta-box h3{font-size:8pt;text-transform:uppercase;color:#1e8449;letter-spacing:.6px;margin-bottom:5px}
.meta-box p{font-size:10pt;line-height:1.7;white-space:pre-line}
.meta-box .sub{font-size:9pt;color:#666;margin-top:2px}
table{width:100%;border-collapse:collapse;margin-bottom:0}
thead th{background:#1e8449;color:#fff;padding:8px 10px;font-size:9pt;text-align:left}
thead th.r{text-align:right}
tbody tr{border-bottom:1px solid #e0e0e0}
tbody tr:nth-child(even){background:#f0fff4}
tbody td{padding:7px 10px;font-size:10pt}
tbody td.r{text-align:right;font-family:'Courier New',monospace}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end;margin-bottom:16px}
.totals{width:290px}
.trow{display:flex;justify-content:space-between;padding:5px 10px;font-size:10pt;border-bottom:1px solid #e0e0e0}
.trow.grand{background:#1e8449;color:#fff;font-weight:bold;font-size:11.5pt;border:none;margin-top:2px;padding:7px 10px}
.trow span:last-child{font-family:'Courier New',monospace}
.words{margin:0 0 16px;padding:9px 14px;background:#f0fff4;border-left:4px solid #1e8449;font-size:10pt}
.words strong{color:#1e8449}
.foot-row{display:flex;gap:18px;margin-bottom:20px}
.bank-box,.terms-box{flex:1;border:1px solid #b2dfdb;border-radius:5px;padding:10px 13px}
.bank-box h3,.terms-box h3{font-size:8pt;text-transform:uppercase;color:#1e8449;letter-spacing:.5px;margin-bottom:5px}
.brow{display:flex;gap:8px;font-size:10pt;padding:2px 0}
.brow span:first-child{color:#666;min-width:100px}
.terms-box p{font-size:9.5pt;color:#444;line-height:1.6}
.sig{text-align:right;padding-right:20px;margin-bottom:20px}
.sig-line{border-top:1px solid #1e8449;width:200px;display:inline-block;margin-bottom:3px}
.sig-co{font-size:10pt;font-weight:bold;color:#1e8449}.sig-lbl{font-size:9.5pt;color:#555}
.pg-foot{background:#1e8449;color:#fff;text-align:center;padding:8px;font-size:8.5pt}
</style></head><body><div class="page">
<div class="header">
  <div>
    <div class="co-name">{{ vendor.name }}</div>
    <div class="co-sub">{{ vendor.address | replace('\n',', ') }}<br>
      {{ vendor.phone }} | {{ vendor.email }}<br>
      {{ labels.gstin }}: {{ vendor.gstin }} | {{ labels.pan }}: {{ vendor.pan }}
    </div>
  </div>
  <div class="inv-badge">
    <h1>{{ labels.invoice }}</h1>
    <div class="no">{{ labels.invoice_no }}: {{ invoice_no }}</div>
  </div>
</div>
<div class="body">
<div class="meta-row">
  <div class="meta-box">
    <h3>{{ labels.bill_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
    <p class="sub">{{ labels.gstin }}: {{ customer.gstin }}</p>
  </div>
  <div class="meta-box" style="max-width:200px">
    <h3>{{ labels.date }}</h3>
    <p><strong>{{ invoice_date }}</strong></p>
    <p class="sub">{{ labels.due_date }}: {{ due_date }}</p>
  </div>
</div>
<table>
  <thead><tr>
    <th style="width:28px">#</th><th>{{ labels.description }}</th>
    <th style="width:60px">{{ labels.hsn }}</th>
    <th class="r" style="width:44px">{{ labels.qty }}</th>
    <th style="width:46px">{{ labels.unit }}</th>
    <th class="r" style="width:105px">{{ labels.unit_price }}</th>
    <th class="r" style="width:105px">{{ labels.amount }}</th>
  </tr></thead>
  <tbody>
  {% for i in line_items %}
    <tr><td class="c">{{ i.sr }}</td><td>{{ i.description }}</td>
    <td class="c">{{ i.hsn }}</td>
    <td class="r">{{ i.qty }}</td><td class="c">{{ i.unit }}</td>
    <td class="r">{{ fmt_inr(i.unit_price) }}</td>
    <td class="r">{{ fmt_inr(i.amount) }}</td></tr>
  {% endfor %}
  </tbody>
</table>
<div class="totals-wrap"><div class="totals">
  <div class="trow"><span>{{ labels.subtotal }}</span><span>₹ {{ fmt_inr(subtotal) }}</span></div>
  {% if gst_type == 'cgst_sgst' %}
  <div class="trow"><span>{{ labels.cgst }}</span><span>₹ {{ fmt_inr(cgst) }}</span></div>
  <div class="trow"><span>{{ labels.sgst }}</span><span>₹ {{ fmt_inr(sgst) }}</span></div>
  {% else %}
  <div class="trow"><span>{{ labels.igst }}</span><span>₹ {{ fmt_inr(igst) }}</span></div>
  {% endif %}
  <div class="trow grand"><span>{{ labels.total }}</span><span>₹ {{ fmt_inr(total) }}</span></div>
</div></div>
<div class="words"><strong>{{ labels.amount_in_words }}:</strong> {{ amount_words }}</div>
<div class="foot-row">
  <div class="bank-box"><h3>{{ labels.bank_details }}</h3>
    <div class="brow"><span>{{ labels.bank_name }}:</span><span>{{ vendor.bank_name }}</span></div>
    <div class="brow"><span>{{ labels.account_no }}:</span><span>{{ vendor.account_no }}</span></div>
    <div class="brow"><span>{{ labels.ifsc }}:</span><span>{{ vendor.ifsc }}</span></div>
  </div>
  <div class="terms-box"><h3>{{ labels.terms }}</h3><p>{{ labels.terms_text }}</p></div>
</div>
<div class="sig">
  <div class="sig-line"></div><br>
  <div class="sig-co">{{ vendor.name }}</div>
  <div class="sig-lbl">{{ labels.authorized_signatory }}</div>
</div>
</div>
<div class="pg-foot">{{ vendor.name }} &nbsp;|&nbsp; {{ vendor.gstin }} &nbsp;|&nbsp; {{ vendor.email }}</div>
</div></body></html>"""


# ── Template 3: Saffron / Indian ──────────────────────────────────────────────
T3 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
<style>
{{ gfonts }}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:{{ labels.font }};font-size:11pt;color:#222;padding:28px 36px;background:#fff}
.page{max-width:800px;margin:auto}
.top-stripe{height:8px;background:linear-gradient(90deg,#e67e22,#f39c12,#e67e22)}
.header{display:flex;justify-content:space-between;align-items:flex-start;
         padding:14px 0 14px;border-bottom:2px solid #e67e22;margin-bottom:18px}
.co-name{font-size:17pt;font-weight:bold;color:#d35400}
.co-meta{font-size:9pt;color:#555;margin-top:4px;line-height:1.7}
.inv-box{text-align:right;background:#fef9e7;border:2px solid #f39c12;
          border-radius:6px;padding:10px 16px}
.inv-box h1{font-size:16pt;color:#d35400;font-weight:bold}
.inv-box .no{font-size:10pt;color:#7d6608;margin-top:4px}
.info-row{display:flex;gap:14px;margin-bottom:18px}
.info-box{flex:1;border:1px solid #f0b27a;border-radius:4px;padding:10px 12px;background:#fef9e7}
.info-box h3{font-size:8.5pt;text-transform:uppercase;color:#d35400;letter-spacing:.5px;margin-bottom:5px}
.info-box p{font-size:10pt;line-height:1.7;white-space:pre-line}
.info-box .sub{font-size:9pt;color:#666;margin-top:3px}
table{width:100%;border-collapse:collapse}
thead th{background:#e67e22;color:#fff;padding:8px 9px;font-size:9pt;text-align:left}
thead th.r{text-align:right}
tbody tr:nth-child(even){background:#fef9e7}
tbody td{padding:7px 9px;font-size:10pt;border-bottom:1px solid #f0b27a}
tbody td.r{text-align:right;font-family:'Courier New',monospace}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end}
.totals{width:295px;border:1px solid #f0b27a;border-top:none}
.trow{display:flex;justify-content:space-between;padding:5px 11px;font-size:10pt;border-bottom:1px solid #fad7a0}
.trow.grand{background:#e67e22;color:#fff;font-weight:bold;font-size:11pt;border:none}
.trow span:last-child{font-family:'Courier New',monospace}
.words{margin-top:12px;padding:9px 13px;background:#fef9e7;border-left:4px solid #e67e22;font-size:10pt}
.words strong{color:#d35400}
.foot-row{display:flex;gap:14px;margin-top:14px}
.bank-box,.terms-box{flex:1;border:1px solid #f0b27a;border-radius:4px;padding:10px 12px}
.bank-box h3,.terms-box h3{font-size:8.5pt;text-transform:uppercase;color:#d35400;letter-spacing:.5px;margin-bottom:5px}
.brow{display:flex;gap:8px;font-size:10pt;padding:2px 0}
.brow span:first-child{color:#666;min-width:100px}
.terms-box p{font-size:9.5pt;color:#444;line-height:1.6}
.sig{margin-top:26px;text-align:right;padding-right:18px}
.sig-line{border-top:2px solid #e67e22;width:190px;display:inline-block;margin-bottom:3px}
.sig-co{font-size:10pt;font-weight:bold;color:#d35400}.sig-lbl{font-size:9.5pt;color:#555}
.pg-foot{margin-top:20px;border-top:2px solid #e67e22;padding-top:7px;
          text-align:center;font-size:8.5pt;color:#7f8c8d}
.bot-stripe{height:8px;background:linear-gradient(90deg,#e67e22,#f39c12,#e67e22);margin-top:14px}
</style></head><body><div class="page">
<div class="top-stripe"></div>
<div class="header">
  <div>
    <div class="co-name">{{ vendor.name }}</div>
    <div class="co-meta">{{ vendor.address }}<br>
      {{ vendor.phone }} &nbsp;|&nbsp; {{ vendor.email }}<br>
      {{ labels.gstin }}: {{ vendor.gstin }} &nbsp;|&nbsp; {{ labels.pan }}: {{ vendor.pan }}
    </div>
  </div>
  <div class="inv-box">
    <h1>{{ labels.invoice }}</h1>
    <div class="no">{{ labels.invoice_no }}: <strong>{{ invoice_no }}</strong></div>
  </div>
</div>
<div class="info-row">
  <div class="info-box">
    <h3>{{ labels.bill_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
    <p class="sub">{{ labels.gstin }}: {{ customer.gstin }}</p>
  </div>
  <div class="info-box">
    <h3>{{ labels.ship_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
  </div>
  <div class="info-box" style="max-width:175px">
    <h3>{{ labels.date }}</h3>
    <p><strong>{{ invoice_date }}</strong></p>
    <p class="sub">{{ labels.due_date }}:<br>{{ due_date }}</p>
  </div>
</div>
<table>
  <thead><tr>
    <th style="width:28px">#</th><th>{{ labels.description }}</th>
    <th style="width:60px">{{ labels.hsn }}</th>
    <th class="r" style="width:44px">{{ labels.qty }}</th>
    <th style="width:46px">{{ labels.unit }}</th>
    <th class="r" style="width:105px">{{ labels.unit_price }}</th>
    <th class="r" style="width:105px">{{ labels.amount }}</th>
  </tr></thead>
  <tbody>
  {% for i in line_items %}
    <tr><td class="c">{{ i.sr }}</td><td>{{ i.description }}</td>
    <td class="c">{{ i.hsn }}</td>
    <td class="r">{{ i.qty }}</td><td class="c">{{ i.unit }}</td>
    <td class="r">{{ fmt_inr(i.unit_price) }}</td>
    <td class="r">{{ fmt_inr(i.amount) }}</td></tr>
  {% endfor %}
  </tbody>
</table>
<div class="totals-wrap"><div class="totals">
  <div class="trow"><span>{{ labels.subtotal }}</span><span>₹ {{ fmt_inr(subtotal) }}</span></div>
  {% if gst_type == 'cgst_sgst' %}
  <div class="trow"><span>{{ labels.cgst }}</span><span>₹ {{ fmt_inr(cgst) }}</span></div>
  <div class="trow"><span>{{ labels.sgst }}</span><span>₹ {{ fmt_inr(sgst) }}</span></div>
  {% else %}
  <div class="trow"><span>{{ labels.igst }}</span><span>₹ {{ fmt_inr(igst) }}</span></div>
  {% endif %}
  <div class="trow grand"><span>{{ labels.total }}</span><span>₹ {{ fmt_inr(total) }}</span></div>
</div></div>
<div class="words"><strong>{{ labels.amount_in_words }}:</strong> {{ amount_words }}</div>
<div class="foot-row">
  <div class="bank-box"><h3>{{ labels.bank_details }}</h3>
    <div class="brow"><span>{{ labels.bank_name }}:</span><span>{{ vendor.bank_name }}</span></div>
    <div class="brow"><span>{{ labels.account_no }}:</span><span>{{ vendor.account_no }}</span></div>
    <div class="brow"><span>{{ labels.ifsc }}:</span><span>{{ vendor.ifsc }}</span></div>
  </div>
  <div class="terms-box"><h3>{{ labels.terms }}</h3><p>{{ labels.terms_text }}</p></div>
</div>
<div class="sig">
  <div class="sig-line"></div><br>
  <div class="sig-co">{{ vendor.name }}</div>
  <div class="sig-lbl">{{ labels.authorized_signatory }}</div>
</div>
<div class="pg-foot">{{ vendor.name }} | {{ vendor.gstin }} | {{ vendor.email }}</div>
<div class="bot-stripe"></div>
</div></body></html>"""


# ── Template 4: Dark Executive ────────────────────────────────────────────────
T4 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
<style>
{{ gfonts }}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:{{ labels.font }};font-size:11pt;color:#2c3e50;padding:0;background:#fff}
.page{max-width:800px;margin:auto}
.header{background:#1c2833;color:#fff;padding:24px 36px;display:grid;
         grid-template-columns:1fr auto;gap:20px;align-items:center}
.co-name{font-size:17pt;font-weight:bold;letter-spacing:.4px}
.co-meta{font-size:8.5pt;color:#aab7b8;margin-top:4px;line-height:1.6}
.inv-section{text-align:right}
.inv-section h1{font-size:13pt;letter-spacing:2px;text-transform:uppercase;
                  border:1px solid #aab7b8;padding:5px 12px;display:inline-block}
.inv-section .no{font-size:10pt;color:#aab7b8;margin-top:6px}
.body{padding:24px 36px}
.info-row{display:flex;gap:16px;margin-bottom:20px}
.info-box{flex:1;border-left:3px solid #2c3e50;padding:8px 12px;background:#f2f3f4}
.info-box h3{font-size:8pt;text-transform:uppercase;color:#7f8c8d;letter-spacing:.6px;margin-bottom:4px}
.info-box p{font-size:10pt;line-height:1.7;white-space:pre-line}
.info-box .sub{font-size:9pt;color:#666;margin-top:2px}
table{width:100%;border-collapse:collapse}
thead th{background:#2c3e50;color:#fff;padding:8px 10px;font-size:9pt;text-align:left}
thead th.r{text-align:right}
tbody tr:nth-child(even){background:#f2f3f4}
tbody td{padding:7px 10px;font-size:10pt;border-bottom:1px solid #dde}
tbody td.r{text-align:right;font-family:'Courier New',monospace}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end}
.totals{width:285px}
.trow{display:flex;justify-content:space-between;padding:5px 10px;font-size:10pt;border-bottom:1px solid #dde}
.trow.grand{background:#1c2833;color:#fff;font-weight:bold;font-size:11.5pt;border:none;padding:8px 10px}
.trow span:last-child{font-family:'Courier New',monospace}
.words{margin-top:12px;padding:9px 13px;background:#f2f3f4;border-left:4px solid #1c2833;font-size:10pt}
.words strong{color:#1c2833}
.foot-row{display:flex;gap:16px;margin-top:14px}
.bank-box,.terms-box{flex:1;padding:10px 13px;background:#f2f3f4}
.bank-box h3,.terms-box h3{font-size:8pt;text-transform:uppercase;color:#7f8c8d;letter-spacing:.5px;margin-bottom:5px}
.brow{display:flex;gap:8px;font-size:10pt;padding:2px 0}
.brow span:first-child{color:#666;min-width:100px}
.terms-box p{font-size:9.5pt;color:#444;line-height:1.6}
.sig{margin-top:28px;text-align:right;padding-right:18px}
.sig-line{border-top:2px solid #1c2833;width:200px;display:inline-block;margin-bottom:3px}
.sig-co{font-size:10pt;font-weight:bold;color:#1c2833}.sig-lbl{font-size:9.5pt;color:#555}
.pg-foot{margin-top:22px;background:#1c2833;color:#aab7b8;text-align:center;
          padding:8px;font-size:8.5pt}
</style></head><body><div class="page">
<div class="header">
  <div>
    <div class="co-name">{{ vendor.name }}</div>
    <div class="co-meta">{{ vendor.address | replace('\n',', ') }}<br>
      {{ vendor.phone }} | {{ vendor.email }}<br>
      {{ labels.gstin }}: {{ vendor.gstin }} | {{ labels.pan }}: {{ vendor.pan }}
    </div>
  </div>
  <div class="inv-section">
    <h1>{{ labels.invoice }}</h1>
    <div class="no">{{ labels.invoice_no }}: {{ invoice_no }}</div>
  </div>
</div>
<div class="body">
<div class="info-row">
  <div class="info-box">
    <h3>{{ labels.bill_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
    <p class="sub">{{ labels.gstin }}: {{ customer.gstin }}</p>
  </div>
  <div class="info-box">
    <h3>{{ labels.ship_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
  </div>
  <div class="info-box" style="max-width:180px;border-left-color:#e74c3c">
    <h3>{{ labels.date }}</h3>
    <p><strong>{{ invoice_date }}</strong></p>
    <p class="sub">{{ labels.due_date }}: {{ due_date }}</p>
  </div>
</div>
<table>
  <thead><tr>
    <th style="width:28px">#</th><th>{{ labels.description }}</th>
    <th style="width:60px">{{ labels.hsn }}</th>
    <th class="r" style="width:44px">{{ labels.qty }}</th>
    <th style="width:46px">{{ labels.unit }}</th>
    <th class="r" style="width:105px">{{ labels.unit_price }}</th>
    <th class="r" style="width:105px">{{ labels.amount }}</th>
  </tr></thead>
  <tbody>
  {% for i in line_items %}
    <tr><td class="c">{{ i.sr }}</td><td>{{ i.description }}</td>
    <td class="c">{{ i.hsn }}</td>
    <td class="r">{{ i.qty }}</td><td class="c">{{ i.unit }}</td>
    <td class="r">{{ fmt_inr(i.unit_price) }}</td>
    <td class="r">{{ fmt_inr(i.amount) }}</td></tr>
  {% endfor %}
  </tbody>
</table>
<div class="totals-wrap"><div class="totals">
  <div class="trow"><span>{{ labels.subtotal }}</span><span>₹ {{ fmt_inr(subtotal) }}</span></div>
  {% if gst_type == 'cgst_sgst' %}
  <div class="trow"><span>{{ labels.cgst }}</span><span>₹ {{ fmt_inr(cgst) }}</span></div>
  <div class="trow"><span>{{ labels.sgst }}</span><span>₹ {{ fmt_inr(sgst) }}</span></div>
  {% else %}
  <div class="trow"><span>{{ labels.igst }}</span><span>₹ {{ fmt_inr(igst) }}</span></div>
  {% endif %}
  <div class="trow grand"><span>{{ labels.total }}</span><span>₹ {{ fmt_inr(total) }}</span></div>
</div></div>
<div class="words"><strong>{{ labels.amount_in_words }}:</strong> {{ amount_words }}</div>
<div class="foot-row">
  <div class="bank-box"><h3>{{ labels.bank_details }}</h3>
    <div class="brow"><span>{{ labels.bank_name }}:</span><span>{{ vendor.bank_name }}</span></div>
    <div class="brow"><span>{{ labels.account_no }}:</span><span>{{ vendor.account_no }}</span></div>
    <div class="brow"><span>{{ labels.ifsc }}:</span><span>{{ vendor.ifsc }}</span></div>
  </div>
  <div class="terms-box"><h3>{{ labels.terms }}</h3><p>{{ labels.terms_text }}</p></div>
</div>
<div class="sig">
  <div class="sig-line"></div><br>
  <div class="sig-co">{{ vendor.name }}</div>
  <div class="sig-lbl">{{ labels.authorized_signatory }}</div>
</div>
</div>
<div class="pg-foot">{{ vendor.name }} &nbsp;|&nbsp; {{ vendor.gstin }} &nbsp;|&nbsp; {{ vendor.email }}</div>
</div></body></html>"""


# ── Template 5: Maroon Classic (full-border traditional) ─────────────────────
T5 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
<style>
{{ gfonts }}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:{{ labels.font }};font-size:11pt;color:#222;padding:28px 36px;background:#fff}
.page{max-width:800px;margin:auto;border:2px solid #7b241c}
.top-bar{background:#7b241c;color:#fff;text-align:center;padding:8px;font-size:8.5pt;letter-spacing:1px}
.header{display:flex;justify-content:space-between;padding:16px 20px;border-bottom:2px solid #7b241c}
.co-name{font-size:16pt;font-weight:bold;color:#7b241c}
.co-meta{font-size:9pt;color:#555;margin-top:4px;line-height:1.7}
.inv-box{text-align:right}
.inv-box h1{font-size:14pt;color:#7b241c;border-bottom:2px solid #7b241c;
             display:inline-block;padding-bottom:3px;margin-bottom:5px}
.inv-box .no{font-size:10pt;color:#444}
.info-row{display:flex;border-bottom:2px solid #7b241c}
.info-box{flex:1;padding:10px 14px;border-right:1px solid #c0392b}
.info-box:last-child{border-right:none}
.info-box h3{font-size:8.5pt;text-transform:uppercase;color:#7b241c;letter-spacing:.5px;margin-bottom:5px}
.info-box p{font-size:10pt;line-height:1.7;white-space:pre-line}
.info-box .sub{font-size:9pt;color:#666;margin-top:3px}
table{width:100%;border-collapse:collapse;border-bottom:2px solid #7b241c}
thead th{background:#7b241c;color:#fff;padding:8px 10px;font-size:9pt;text-align:left;border:1px solid #c0392b}
thead th.r{text-align:right}
tbody td{padding:7px 10px;font-size:10pt;border:1px solid #f5b7b1}
tbody tr:nth-child(even) td{background:#fdedec}
tbody td.r{text-align:right;font-family:'Courier New',monospace}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end;border-bottom:2px solid #7b241c}
.totals{width:290px;border-left:2px solid #7b241c}
.trow{display:flex;justify-content:space-between;padding:5px 11px;font-size:10pt;border-bottom:1px solid #f5b7b1}
.trow.grand{background:#7b241c;color:#fff;font-weight:bold;font-size:11pt;border:none}
.trow span:last-child{font-family:'Courier New',monospace}
.words{padding:9px 14px;background:#fdedec;border-bottom:2px solid #7b241c;font-size:10pt}
.words strong{color:#7b241c}
.foot-row{display:flex;border-bottom:2px solid #7b241c}
.bank-box{flex:1;padding:10px 14px;border-right:1px solid #c0392b}
.terms-box{flex:1;padding:10px 14px}
.bank-box h3,.terms-box h3{font-size:8.5pt;text-transform:uppercase;color:#7b241c;letter-spacing:.5px;margin-bottom:5px}
.brow{display:flex;gap:8px;font-size:10pt;padding:2px 0}
.brow span:first-child{color:#666;min-width:100px}
.terms-box p{font-size:9.5pt;color:#444;line-height:1.6}
.sig{padding:16px 20px;text-align:right;border-bottom:2px solid #7b241c}
.sig-line{border-top:1px solid #7b241c;width:190px;display:inline-block;margin-bottom:3px}
.sig-co{font-size:10pt;font-weight:bold;color:#7b241c}.sig-lbl{font-size:9.5pt;color:#555}
.bot-bar{background:#7b241c;color:#fff;text-align:center;padding:7px;font-size:8.5pt}
</style></head><body><div class="page">
<div class="top-bar">{{ labels.original }} | {{ labels.invoice }}</div>
<div class="header">
  <div>
    <div class="co-name">{{ vendor.name }}</div>
    <div class="co-meta">{{ vendor.address }}<br>
      {{ vendor.phone }} &nbsp;|&nbsp; {{ vendor.email }}<br>
      {{ labels.gstin }}: {{ vendor.gstin }} &nbsp;|&nbsp; {{ labels.pan }}: {{ vendor.pan }}
    </div>
  </div>
  <div class="inv-box">
    <h1>{{ labels.invoice }}</h1>
    <div class="no">{{ labels.invoice_no }}: <strong>{{ invoice_no }}</strong><br>
      {{ labels.date }}: {{ invoice_date }}<br>
      {{ labels.due_date }}: {{ due_date }}
    </div>
  </div>
</div>
<div class="info-row">
  <div class="info-box">
    <h3>{{ labels.bill_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
    <p class="sub">{{ labels.gstin }}: {{ customer.gstin }}</p>
  </div>
  <div class="info-box">
    <h3>{{ labels.ship_to }}</h3>
    <p><strong>{{ customer.name }}</strong></p>
    <p>{{ customer.address }}</p>
  </div>
</div>
<table>
  <thead><tr>
    <th style="width:28px">#</th><th>{{ labels.description }}</th>
    <th style="width:60px">{{ labels.hsn }}</th>
    <th class="r" style="width:44px">{{ labels.qty }}</th>
    <th style="width:46px">{{ labels.unit }}</th>
    <th class="r" style="width:105px">{{ labels.unit_price }}</th>
    <th class="r" style="width:105px">{{ labels.amount }}</th>
  </tr></thead>
  <tbody>
  {% for i in line_items %}
    <tr><td class="c">{{ i.sr }}</td><td>{{ i.description }}</td>
    <td class="c">{{ i.hsn }}</td>
    <td class="r">{{ i.qty }}</td><td class="c">{{ i.unit }}</td>
    <td class="r">{{ fmt_inr(i.unit_price) }}</td>
    <td class="r">{{ fmt_inr(i.amount) }}</td></tr>
  {% endfor %}
  </tbody>
</table>
<div class="totals-wrap"><div class="totals">
  <div class="trow"><span>{{ labels.subtotal }}</span><span>₹ {{ fmt_inr(subtotal) }}</span></div>
  {% if gst_type == 'cgst_sgst' %}
  <div class="trow"><span>{{ labels.cgst }}</span><span>₹ {{ fmt_inr(cgst) }}</span></div>
  <div class="trow"><span>{{ labels.sgst }}</span><span>₹ {{ fmt_inr(sgst) }}</span></div>
  {% else %}
  <div class="trow"><span>{{ labels.igst }}</span><span>₹ {{ fmt_inr(igst) }}</span></div>
  {% endif %}
  <div class="trow grand"><span>{{ labels.total }}</span><span>₹ {{ fmt_inr(total) }}</span></div>
</div></div>
<div class="words"><strong>{{ labels.amount_in_words }}:</strong> {{ amount_words }}</div>
<div class="foot-row">
  <div class="bank-box"><h3>{{ labels.bank_details }}</h3>
    <div class="brow"><span>{{ labels.bank_name }}:</span><span>{{ vendor.bank_name }}</span></div>
    <div class="brow"><span>{{ labels.account_no }}:</span><span>{{ vendor.account_no }}</span></div>
    <div class="brow"><span>{{ labels.ifsc }}:</span><span>{{ vendor.ifsc }}</span></div>
  </div>
  <div class="terms-box"><h3>{{ labels.terms }}</h3><p>{{ labels.terms_text }}</p></div>
</div>
<div class="sig">
  <div class="sig-line"></div><br>
  <div class="sig-co">{{ vendor.name }}</div>
  <div class="sig-lbl">{{ labels.authorized_signatory }}</div>
</div>
<div class="bot-bar">{{ vendor.name }} &nbsp;|&nbsp; {{ vendor.gstin }} &nbsp;|&nbsp; {{ vendor.email }}</div>
</div></body></html>"""

TEMPLATES = {1: T1, 2: T2, 3: T3, 4: T4, 5: T5}
TEMPLATE_NAMES = {1: "Blue Corporate", 2: "Emerald Green", 3: "Saffron Indian",
                  4: "Dark Executive", 5: "Maroon Classic"}


# ── PDF rendering ─────────────────────────────────────────────────────────────

def _html_to_pdf_browser(html_path: Path, pdf_path: Path, lang: str = "") -> bool:
    import time
    # Edge's --print-to-pdf fails on paths with spaces — use a temp staging area
    stage  = Path(tempfile.mkdtemp(prefix="inv_stage_"))
    s_html = stage / "invoice.html"
    s_pdf  = stage / "invoice.pdf"
    edge_d = tempfile.mkdtemp(prefix=f"edge_{lang}_")
    try:
        shutil.copy(html_path, s_html)
        subprocess.run(
            [_BROWSER_EXE, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--no-first-run", "--no-default-browser-check", "--disable-extensions",
             f"--user-data-dir={edge_d}", "--no-pdf-header-footer",
             f"--print-to-pdf={s_pdf}", s_html.as_uri()],
            capture_output=True, timeout=90,
        )
        time.sleep(3)
        if s_pdf.exists() and s_pdf.stat().st_size > 1000:
            shutil.copy(s_pdf, pdf_path)
            return True
        return False
    except Exception:
        return False
    finally:
        shutil.rmtree(stage,  ignore_errors=True)
        shutil.rmtree(edge_d, ignore_errors=True)


def render_and_save(data: dict, out_dir: Path, filename: str) -> bool:
    env      = Environment(loader=BaseLoader())
    tmpl_str = TEMPLATES[data["template"]]
    html_str = env.from_string(tmpl_str).render(**data, gfonts=GOOGLE_FONTS)

    html_path = out_dir / f"{filename}.html"
    html_path.write_text(html_str, encoding="utf-8")

    pdf_path = out_dir / f"{filename}.pdf"
    pdf_ok   = False

    if WEASYPRINT_AVAILABLE:
        try:
            WeasyprintHTML(string=html_str, base_url=str(out_dir)).write_pdf(str(pdf_path))
            pdf_ok = True
        except Exception:
            pass

    if not pdf_ok and BROWSER_AVAILABLE:
        pdf_ok = _html_to_pdf_browser(html_path.resolve(), pdf_path, data["lang"])

    return pdf_ok


# ── Data loading ──────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Generate random multilingual invoices")
    parser.add_argument("--count",  type=int, default=5,
                        help="Number of invoices per language (default: 5)")
    parser.add_argument("--lang",   default="all",
                        choices=LANG_ORDER + ["all"],
                        help="Language code or 'all' (default: all)")
    parser.add_argument("--output", default="output/random",
                        help="Output directory (default: output/random)")
    parser.add_argument("--template", type=int, default=0, choices=[0,1,2,3,4,5],
                        help="Force a specific template 1-5 (default: 0 = random)")
    args = parser.parse_args()

    vendors   = load_json(DATA_DIR / "vendors.json")
    customers = load_json(DATA_DIR / "customers.json")
    products  = load_json(DATA_DIR / "products.json")

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    langs = LANG_ORDER if args.lang == "all" else [args.lang]

    pdf_engine = ("weasyprint" if WEASYPRINT_AVAILABLE
                  else f"Edge headless" if BROWSER_AVAILABLE
                  else "HTML only")
    print(f"PDF engine : {pdf_engine}")
    print(f"Languages  : {', '.join(langs)}")
    print(f"Count      : {args.count} per language")
    print(f"Output     : {out.resolve()}\n")

    total_pdf = total_html = 0

    for lang in langs:
        lang_name  = LANG_NAMES[lang]
        v_pool     = vendors[lang]
        c_pool     = customers[lang]
        p_pool     = products[lang]

        for i in range(1, args.count + 1):
            tmpl_idx = args.template if args.template else random.randint(1, 5)
            vendor   = random.choice(v_pool)
            customer = random.choice(c_pool)

            data     = build_invoice(lang, vendor, customer, p_pool, tmpl_idx)
            filename = f"sample_{i}_{lang_name}"

            pdf_ok   = render_and_save(data, out, filename)
            t_name   = TEMPLATE_NAMES[tmpl_idx]

            if pdf_ok:
                print(f"  [PDF]  {filename}.pdf  (T{tmpl_idx}: {t_name})")
                total_pdf  += 1
            else:
                print(f"  [HTML] {filename}.html  (T{tmpl_idx}: {t_name})  -- open in browser to print")
                total_html += 1

    print(f"\nDone.  PDF: {total_pdf}  HTML: {total_html}  -> {out.resolve()}")


if __name__ == "__main__":
    main()
