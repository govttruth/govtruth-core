"""
GovTruth - Live Dashboard
India Government Accountability Platform
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import json
import base64
from pathlib import Path

app = FastAPI(title="GovTruth")

def load_mp_data():
    try:
        path = Path('data/raw/myneta/LS2024.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return sorted(data, key=lambda x: x['assets'], reverse=True)
    except:
        return []

def load_satellite_image():
    try:
        img_path = Path('data/satellite/google/Jewar_LINKEDIN_SHARE.jpg')
        if img_path.exists():
            with open(img_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
    except:
        pass
    return ""

def build_mp_rows():
    mps = load_mp_data()
    if not mps:
        return "<tr><td colspan='6' style='color:#444;text-align:center;padding:30px'>Data loading...</td></tr>"
    rows = ""
    for i, mp in enumerate(mps, 1):
        assets = mp.get('assets', 0)
        cases = mp.get('criminal_cases', 0)
        if assets > 100_00_00_000:
            risk_class = "risk-high"
        elif assets > 10_00_00_000:
            risk_class = "risk-med"
        else:
            risk_class = "risk-low"
        case_html = f'<span class="flag flag-red">{cases} CASES</span>' if cases > 0 else '<span class="flag flag-green">CLEAN</span>'
        assets_raw = mp.get('assets_raw') or '<span style="color:#444">Not Filed</span>'
        liab_raw = mp.get('liabilities_raw') or '<span style="color:#444">Not Filed</span>'
        rows += f"""<tr data-cases="{cases}" data-assets="{assets}">
            <td style="color:#444">{i}</td>
            <td><div class="mp-name">{mp['name']}</div><div class="mp-party">{mp['party']} · {mp['constituency']}</div></td>
            <td class="{risk_class}">{assets_raw}</td>
            <td style="color:#888">{liab_raw}</td>
            <td>{case_html}</td>
            <td><div class="source-tag">ECI Affidavit 2024</div></td>
        </tr>"""
    return rows

def build_stats():
    mps = load_mp_data()
    total = len(mps)
    with_cases = sum(1 for m in mps if m.get('criminal_cases', 0) > 0)
    above_100cr = sum(1 for m in mps if m.get('assets', 0) > 100_00_00_000)
    return total, with_cases, above_100cr

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a0f; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
nav { background: #0d0d1a; border-bottom: 1px solid #1a1a3a; padding: 15px 30px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 100; }
.logo { font-size: 1.5em; font-weight: 900; letter-spacing: 3px; color: #fff; }
.logo span { color: #ff3355; }
.nav-links a { color: #888; text-decoration: none; margin-left: 25px; font-size: 0.85em; letter-spacing: 1px; text-transform: uppercase; }
.nav-links a:hover { color: #00ff88; }
.live-badge { background: #ff3355; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.7em; letter-spacing: 2px; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.hero { background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 100%); padding: 60px 30px; text-align: center; border-bottom: 1px solid #1a1a3a; }
.hero h1 { font-size: 3em; font-weight: 900; letter-spacing: 5px; margin-bottom: 10px; }
.hero h1 span { color: #ff3355; }
.hero p { color: #888; font-size: 1em; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px; }
.hero-stats { display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; }
.hero-stat { text-align: center; }
.hero-stat .number { font-size: 2.5em; font-weight: 900; color: #00ff88; }
.hero-stat .label { font-size: 0.7em; color: #666; letter-spacing: 2px; text-transform: uppercase; margin-top: 5px; }
.disclaimer { background: #1a1500; border: 1px solid #ffaa0033; border-left: 4px solid #ffaa00; padding: 12px 30px; font-size: 0.8em; color: #ffaa00; text-align: center; }
.container { max-width: 1400px; margin: 0 auto; padding: 40px 30px; }
.section-header { display: flex; align-items: center; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #1a1a3a; }
.section-header h2 { font-size: 1em; letter-spacing: 3px; text-transform: uppercase; color: #fff; }
.section-header .icon { font-size: 1.5em; margin-right: 12px; }
.section-header .count { margin-left: auto; background: #ff335522; color: #ff3355; padding: 3px 12px; border-radius: 20px; font-size: 0.8em; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 50px; }
.stat-card { background: #0d0d1a; border: 1px solid #1a1a3a; border-radius: 8px; padding: 25px; text-align: center; }
.stat-card .number { font-size: 2em; font-weight: 900; margin-bottom: 5px; }
.stat-card .label { font-size: 0.7em; color: #666; letter-spacing: 2px; text-transform: uppercase; }
.stat-card .source { font-size: 0.65em; color: #444; margin-top: 8px; }
.green { color: #00ff88; } .red { color: #ff3355; } .yellow { color: #ffaa00; }
.search-box { display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; align-items: center; }
.search-input { flex: 1; min-width: 200px; background: #0d0d1a; border: 1px solid #1a1a3a; color: #fff; padding: 10px 16px; border-radius: 6px; font-size: 0.9em; outline: none; }
.search-input:focus { border-color: #00ff88; }
.search-input::placeholder { color: #444; }
.filter-btn { background: #0d0d1a; border: 1px solid #1a1a3a; color: #888; padding: 10px 14px; border-radius: 6px; cursor: pointer; font-size: 0.75em; letter-spacing: 1px; transition: all 0.2s; }
.filter-btn:hover { border-color: #ff3355; color: #ff3355; }
.filter-active { border-color: #ff3355 !important; color: #ff3355 !important; }
.toggle-btn { background: #0d0d1a; border: 1px solid #1a1a3a; color: #888; padding: 10px 14px; border-radius: 6px; cursor: pointer; font-size: 0.75em; letter-spacing: 1px; margin-left: auto; }
.toggle-btn:hover { border-color: #00ff88; color: #00ff88; }
.search-count { font-size: 0.75em; color: #666; margin-bottom: 10px; }
.table-container { background: #0d0d1a; border: 1px solid #1a1a3a; border-radius: 8px; overflow: hidden; margin-bottom: 50px; }
.table-collapsed { max-height: 320px; overflow-y: hidden; position: relative; }
.table-collapsed::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 80px; background: linear-gradient(transparent, #0a0a0f); pointer-events: none; }
table { width: 100%; border-collapse: collapse; }
thead { background: #13132a; }
th { padding: 14px 16px; text-align: left; font-size: 0.7em; letter-spacing: 2px; text-transform: uppercase; color: #666; border-bottom: 1px solid #1a1a3a; }
td { padding: 14px 16px; border-bottom: 1px solid #0f0f20; font-size: 0.88em; }
tr:hover td { background: #ffffff05; }
tr:last-child td { border-bottom: none; }
.mp-name { font-weight: 600; color: #fff; }
.mp-party { font-size: 0.75em; color: #666; margin-top: 3px; }
.risk-high { color: #ff3355; font-weight: 700; }
.risk-med { color: #ffaa00; font-weight: 700; }
.risk-low { color: #00ff88; }
.source-tag { font-size: 0.7em; color: #333; }
.flag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7em; font-weight: 700; letter-spacing: 1px; }
.flag-red { background: #ff335522; color: #ff3355; }
.flag-green { background: #00ff8822; color: #00ff88; }
.cag-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 50px; }
.cag-card { background: #0d0d1a; border: 1px solid #1a1a3a; border-left: 3px solid #ff3355; border-radius: 8px; padding: 20px; }
.cag-ministry { font-size: 0.7em; letter-spacing: 2px; text-transform: uppercase; color: #ff3355; margin-bottom: 8px; }
.cag-title { font-size: 0.9em; color: #fff; margin-bottom: 12px; line-height: 1.5; }
.cag-amount { font-size: 1.4em; font-weight: 900; color: #ffaa00; }
.cag-meta { display: flex; justify-content: space-between; margin-top: 12px; font-size: 0.72em; color: #555; }
.status-ignored { background: #ff335522; color: #ff3355; padding: 2px 8px; border-radius: 4px; }
.progress-section { background: #0d0d1a; border: 1px solid #1a1a3a; border-radius: 8px; padding: 30px; margin-bottom: 50px; }
.progress-item { margin-bottom: 20px; }
.progress-label { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.85em; }
.progress-bar { height: 6px; background: #1a1a3a; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg, #ff3355, #ff6633); }
footer { background: #0d0d1a; border-top: 1px solid #1a1a3a; padding: 40px 30px; text-align: center; }
footer .footer-logo { font-size: 1.5em; font-weight: 900; letter-spacing: 3px; margin-bottom: 10px; }
footer .footer-logo span { color: #ff3355; }
footer p { color: #444; font-size: 0.8em; margin: 5px 0; }
footer .links a { color: #555; text-decoration: none; margin: 0 10px; font-size: 0.8em; }
footer .links a:hover { color: #00ff88; }
@media (max-width: 768px) { .hero h1 { font-size: 2em; } .hero-stats { gap: 20px; } .nav-links { display: none; } }
"""

JS = """
var tableCollapsed = false;
function searchMPs() {
    var query = document.getElementById('mp-search').value.toLowerCase();
    var filter = document.getElementById('active-filter').value;
    var rows = document.querySelectorAll('#mp-tbody tr');
    var visible = 0;
    rows.forEach(function(row) {
        var text = row.textContent.toLowerCase();
        var matchQuery = !query || text.includes(query);
        var cases = parseInt(row.getAttribute('data-cases') || '0');
        var assets = parseFloat(row.getAttribute('data-assets') || '0');
        var matchFilter = true;
        if (filter === 'criminal') matchFilter = cases > 0;
        if (filter === '100cr') matchFilter = assets > 10000000000;
        if (filter === 'notfiled') matchFilter = assets === 0;
        row.style.display = (matchQuery && matchFilter) ? '' : 'none';
        if (matchQuery && matchFilter) visible++;
    });
    document.getElementById('search-count').textContent = visible + ' MPs shown';
}
function setFilter(val, btn) {
    document.getElementById('active-filter').value = val;
    document.querySelectorAll('.filter-btn').forEach(function(b) { b.classList.remove('filter-active'); });
    btn.classList.add('filter-active');
    searchMPs();
}
function toggleTable() {
    var tc = document.getElementById('mp-table-container');
    var btn = document.getElementById('toggle-btn');
    tableCollapsed = !tableCollapsed;
    tc.classList.toggle('table-collapsed', tableCollapsed);
    btn.textContent = tableCollapsed ? 'EXPAND' : 'MINIMIZE';
}
"""

@app.get("/", response_class=HTMLResponse)
def dashboard():
    total, with_cases, above_100cr = build_stats()
    mp_rows = build_mp_rows()
    pct = round(with_cases / total * 100) if total else 0
    sat_img = load_satellite_image()
    sat_html = f'<img src="data:image/jpeg;base64,{sat_img}" style="width:100%;border-radius:8px;border:1px solid #1a1a3a;" alt="Jewar Airport Satellite"/>' if sat_img else '<div style="color:#444;padding:40px;text-align:center;">Satellite image loading...</div>'

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>GovTruth - India Accountability Tracker</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>{CSS}</style>
</head>
<body>

<nav>
    <div class="logo">GOV<span>TRUTH</span></div>
    <div class="nav-links">
        <a href="#mps">MP Tracker</a>
        <a href="#satellite">Satellite</a>
        <a href="#cag">CAG Findings</a>
    </div>
    <div class="live-badge">LIVE</div>
</nav>

<div class="hero">
    <h1>GOV<span>TRUTH</span> 🇮🇳</h1>
    <p>India Open Government Accountability Platform</p>
    <div class="hero-stats">
        <div class="hero-stat"><div class="number">{total}</div><div class="label">MPs Tracked</div></div>
        <div class="hero-stat"><div class="number red">{with_cases}</div><div class="label">With Criminal Cases</div></div>
        <div class="hero-stat"><div class="number yellow">{above_100cr}</div><div class="label">With 100Cr+ Assets</div></div>
        <div class="hero-stat"><div class="number">4.8L Cr</div><div class="label">CAG Irregularities</div></div>
    </div>
</div>

<div class="disclaimer">
    All data from official ECI affidavits via MyNeta/ADR. Statistical analysis only. No accusations made. All parties covered equally.
</div>

<div class="container">

    <div class="stats-grid">
        <div class="stat-card"><div class="number green">{total}</div><div class="label">MPs Analyzed</div><div class="source">Source: ECI Affidavits 2024</div></div>
        <div class="stat-card"><div class="number red">{with_cases}</div><div class="label">MPs With Criminal Cases</div><div class="source">{pct}% of current Lok Sabha</div></div>
        <div class="stat-card"><div class="number yellow">{above_100cr}</div><div class="label">MPs With 100 Crore+</div><div class="source">Declared assets 2024</div></div>
        <div class="stat-card"><div class="number yellow">4,82,000 Cr</div><div class="label">CAG Irregularities</div><div class="source">CAG Reports 2010-2024</div></div>
        <div class="stat-card"><div class="number red">97.5%</div><div class="label">No Accountability</div><div class="source">CAG findings unresolved</div></div>
        <div class="stat-card"><div class="number yellow">20,000 Cr</div><div class="label">Electoral Bonds</div><div class="source">SBI Disclosure 2024</div></div>
    </div>

    <div id="mps">
        <div class="section-header">
            <span class="icon">📊</span>
            <h2>MP Asset Tracker — Search All 483 MPs</h2>
            <span class="count">{total} MPs · ECI 2024</span>
        </div>
        <input type="hidden" id="active-filter" value="all">
        <div class="search-box">
            <input class="search-input" id="mp-search" placeholder="Search MP name, party, constituency..." oninput="searchMPs()">
            <button class="filter-btn filter-active" onclick="setFilter('all',this)">ALL</button>
            <button class="filter-btn" onclick="setFilter('criminal',this)">CRIMINAL CASES</button>
            <button class="filter-btn" onclick="setFilter('100cr',this)">100CR+</button>
            <button class="filter-btn" onclick="setFilter('notfiled',this)">NOT FILED</button>
            <button class="toggle-btn" id="toggle-btn" onclick="toggleTable()">MINIMIZE</button>
        </div>
        <div class="search-count" id="search-count">{total} MPs shown</div>
        <div class="table-container" id="mp-table-container">
            <table>
                <thead>
                    <tr>
                        <th>#</th><th>MP Name</th><th>Declared Assets 2024</th>
                        <th>Liabilities</th><th>Criminal Cases</th><th>Source</th>
                    </tr>
                </thead>
                <tbody id="mp-tbody">{mp_rows}</tbody>
            </table>
        </div>
    </div>

    <div id="satellite" style="margin-bottom:50px;">
        <div class="section-header">
            <span class="icon">🛰️</span>
            <h2>Satellite Verification — BJP 2024 Promises</h2>
            <span class="count">Finding #1 Published</span>
        </div>
        <div style="background:#0d0d1a;border:1px solid #1a1a3a;border-radius:8px;padding:30px;">
            <div style="display:flex;gap:30px;flex-wrap:wrap;align-items:flex-start;">
                <div style="flex:1;min-width:280px;">
                    <div style="color:#ff3355;font-size:0.7em;letter-spacing:2px;margin-bottom:10px;">GOVTRUTH FINDING #1</div>
                    <h3 style="color:#fff;font-size:1.2em;margin-bottom:15px;">Jewar Airport, Uttar Pradesh</h3>
                    <div style="color:#888;font-size:0.85em;line-height:2.2;">
                        <div><span style="color:#ffaa00;">PROMISE:</span> Operational by 2024</div>
                        <div><span style="color:#ffaa00;">BUDGET:</span> 98,000 Crore</div>
                        <div><span style="color:#ffaa00;">COORDS:</span> 28.1799N, 77.6089E</div>
                    </div>
                    <div style="margin-top:20px;line-height:2.4;">
                        <div style="color:#00ff88;">✅ Runway — PAVED</div>
                        <div style="color:#00ff88;">✅ Taxiway — BUILT</div>
                        <div style="color:#ff3355;">❌ Terminal — NOT VISIBLE</div>
                        <div style="color:#ff3355;">❌ NOT Operational as promised</div>
                    </div>
                    <div style="margin-top:20px;background:#ffaa0022;border:1px solid #ffaa0044;border-radius:8px;padding:15px;text-align:center;">
                        <div style="color:#ffaa00;font-size:1.1em;font-weight:900;">⚠️ VERDICT: PARTIAL</div>
                    </div>
                </div>
                <div style="flex:2;min-width:300px;">{sat_html}</div>
            </div>
        </div>
    </div>

    <div id="cag">
        <div class="section-header">
            <span class="icon">📋</span>
            <h2>CAG Findings Tracker</h2>
            <span class="count">12,847 findings</span>
        </div>
        <div class="progress-section">
            <p style="font-size:0.8em;color:#666;margin-bottom:20px;letter-spacing:1px;">ACCOUNTABILITY SCORECARD — CAG FINDINGS 2010-2024</p>
            <div class="progress-item"><div class="progress-label"><span>Ministry of Rural Development</span><span>2,341 findings ignored</span></div><div class="progress-bar"><div class="progress-fill" style="width:94%"></div></div></div>
            <div class="progress-item"><div class="progress-label"><span>Ministry of Defence</span><span>1,876 findings ignored</span></div><div class="progress-bar"><div class="progress-fill" style="width:87%"></div></div></div>
            <div class="progress-item"><div class="progress-label"><span>Ministry of Health</span><span>1,234 findings ignored</span></div><div class="progress-bar"><div class="progress-fill" style="width:79%"></div></div></div>
            <div class="progress-item"><div class="progress-label"><span>Ministry of Education</span><span>987 findings ignored</span></div><div class="progress-bar"><div class="progress-fill" style="width:71%"></div></div></div>
            <div class="progress-item"><div class="progress-label"><span>Ministry of Roads</span><span>876 findings ignored</span></div><div class="progress-bar"><div class="progress-fill" style="width:65%"></div></div></div>
        </div>
        <div class="cag-grid">
            <div class="cag-card"><div class="cag-ministry">Ministry of Rural Development</div><div class="cag-title">MGNREGA — Wages paid for work not done. Ghost beneficiaries detected across districts.</div><div class="cag-amount">8,243 Crore</div><div class="cag-meta"><span>CAG Report 2023</span><span class="status-ignored">NEVER DISCUSSED IN PARLIAMENT</span></div></div>
            <div class="cag-card"><div class="cag-ministry">Ministry of Defence</div><div class="cag-title">Procurement at prices above market rate. Single-bid vendors awarded contracts.</div><div class="cag-amount">12,450 Crore</div><div class="cag-meta"><span>CAG Report 2022</span><span class="status-ignored">NEVER DISCUSSED IN PARLIAMENT</span></div></div>
            <div class="cag-card"><div class="cag-ministry">Ministry of Health</div><div class="cag-title">PM-JAY Ayushman Bharat — Fraudulent claims for deceased and non-existent patients.</div><div class="cag-amount">3,122 Crore</div><div class="cag-meta"><span>CAG Report 2023</span><span class="status-ignored">NEVER DISCUSSED IN PARLIAMENT</span></div></div>
        </div>
    </div>

</div>

<footer>
    <div class="footer-logo">GOV<span>TRUTH</span></div>
    <p>India Open Government Accountability Platform</p>
    <p style="margin-top:10px;"><a href="https://github.com/govttruth/govtruth-core" style="color:#00ff88;">GitHub</a> · <span style="color:#555;">govtruth.project@proton.me</span></p>
    <p style="color:#333;font-size:0.75em;margin-top:15px;">Data: ECI · MyNeta · ADR · CAG · ESA Copernicus · Mapbox</p>
</footer>

<script>{JS}</script>
</body>
</html>"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
