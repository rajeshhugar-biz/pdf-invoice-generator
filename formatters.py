"""Number formatting utilities for Indian currency and invoice numbering."""

import random
from datetime import date

_ONES = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen",
]
_TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def fmt_inr(amount: float) -> str:
    """Format a number using Indian numbering system (e.g. 1,23,456.78)."""
    s = f"{amount:.2f}"
    ip, dp = s.split(".")
    if len(ip) > 3:
        last3 = ip[-3:]
        rest = ip[:-3]
        groups: list[str] = []
        while len(rest) > 2:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.insert(0, rest)
        ip = ",".join(groups) + "," + last3
    return f"{ip}.{dp}"


def _w3(n: int) -> str:
    """Convert an integer (0–999) to English words."""
    if n == 0:
        return ""
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + (" " + _ONES[n % 10] if n % 10 else "")
    return _ONES[n // 100] + " Hundred" + (" " + _w3(n % 100) if n % 100 else "")


def amount_in_words(amount: float) -> str:
    """Convert a rupee amount to English words (e.g. 'Rupees One Lakh Only')."""
    paise = round(amount * 100)
    rupees = paise // 100
    paise %= 100

    if rupees == 0:
        rs = "Zero"
    else:
        cr = rupees // 10_000_000
        rupees %= 10_000_000
        lk = rupees // 100_000
        rupees %= 100_000
        th = rupees // 1000
        rupees %= 1000

        parts: list[str] = []
        if cr:
            parts.append(_w3(cr) + " Crore")
        if lk:
            parts.append(_w3(lk) + " Lakh")
        if th:
            parts.append(_w3(th) + " Thousand")
        if rupees:
            parts.append(_w3(rupees))
        rs = " ".join(parts)

    result = f"Rupees {rs}"
    if paise:
        result += f" and {_w3(paise)} Paise"
    return result + " Only"


def random_invoice_no(state_code: str = "27") -> str:
    """Generate a realistic Indian invoice number in one of five common formats."""
    y = date.today().year
    ym = date.today().strftime("%Y%m")
    n = random.randint(1000, 9999)
    s = random.randint(100, 999)
    formats = [
        f"INV-{y}-{n}",
        f"BILL/{y}-{str(y + 1)[-2:]}/{s:03d}",
        f"TAX-INV-{n}{s}",
        f"{state_code}/INV/{ym}/{n}",
        f"{y}-{date.today().month:02d}-{n}",
    ]
    return random.choice(formats)
