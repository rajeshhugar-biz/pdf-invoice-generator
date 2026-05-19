"""Five Jinja2 HTML invoice templates and Google Fonts import string."""

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
_T1 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
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
tbody td.r{text-align:right}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end}
.totals{width:300px;border:1px solid #d5d8dc;border-top:none}
.trow{display:flex;justify-content:space-between;padding:5px 11px;font-size:10pt;border-bottom:1px solid #eee}
.trow.grand{background:#1a5276;color:#fff;font-weight:bold;font-size:11pt;border:none}
.trow span:last-child{}
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
_T2 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
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
tbody td.r{text-align:right}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end;margin-bottom:16px}
.totals{width:290px}
.trow{display:flex;justify-content:space-between;padding:5px 10px;font-size:10pt;border-bottom:1px solid #e0e0e0}
.trow.grand{background:#1e8449;color:#fff;font-weight:bold;font-size:11.5pt;border:none;margin-top:2px;padding:7px 10px}
.trow span:last-child{}
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

# ── Template 3: Saffron Indian ────────────────────────────────────────────────
_T3 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
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
tbody td.r{text-align:right}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end}
.totals{width:295px;border:1px solid #f0b27a;border-top:none}
.trow{display:flex;justify-content:space-between;padding:5px 11px;font-size:10pt;border-bottom:1px solid #fad7a0}
.trow.grand{background:#e67e22;color:#fff;font-weight:bold;font-size:11pt;border:none}
.trow span:last-child{}
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
_T4 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
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
tbody td.r{text-align:right}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end}
.totals{width:285px}
.trow{display:flex;justify-content:space-between;padding:5px 10px;font-size:10pt;border-bottom:1px solid #dde}
.trow.grand{background:#1c2833;color:#fff;font-weight:bold;font-size:11.5pt;border:none;padding:8px 10px}
.trow span:last-child{}
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

# ── Template 5: Maroon Classic ────────────────────────────────────────────────
_T5 = r"""<!DOCTYPE html><html lang="{{ lang }}"><head><meta charset="UTF-8"/>
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
tbody td.r{text-align:right}
tbody td.c{text-align:center}
.totals-wrap{display:flex;justify-content:flex-end;border-bottom:2px solid #7b241c}
.totals{width:290px;border-left:2px solid #7b241c}
.trow{display:flex;justify-content:space-between;padding:5px 11px;font-size:10pt;border-bottom:1px solid #f5b7b1}
.trow.grand{background:#7b241c;color:#fff;font-weight:bold;font-size:11pt;border:none}
.trow span:last-child{}
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

TEMPLATES: dict[int, str] = {1: _T1, 2: _T2, 3: _T3, 4: _T4, 5: _T5}

TEMPLATE_NAMES: dict[int, str] = {
    1: "Blue Corporate",
    2: "Emerald Green",
    3: "Saffron Indian",
    4: "Dark Executive",
    5: "Maroon Classic",
}
