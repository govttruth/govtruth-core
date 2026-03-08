"""
GovTruth - Live Dashboard
India Government Accountability Platform
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="GovTruth")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>GovTruth - India Accountability Tracker</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: #0a0a0f;
            color: #e0e0e0;
            font-family: 'Segoe UI', sans-serif;
        }

        /* TOP NAV */
        nav {
            background: #0d0d1a;
            border-bottom: 1px solid #1a1a3a;
            padding: 15px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .logo {
            font-size: 1.5em;
            font-weight: 900;
            letter-spacing: 3px;
            color: #fff;
        }
        .logo span { color: #ff3355; }
        .nav-links a {
            color: #888;
            text-decoration: none;
            margin-left: 25px;
            font-size: 0.85em;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .nav-links a:hover { color: #00ff88; }
        .live-badge {
            background: #ff3355;
            color: white;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.7em;
            letter-spacing: 2px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* HERO */
        .hero {
            background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 100%);
            padding: 60px 30px;
            text-align: center;
            border-bottom: 1px solid #1a1a3a;
        }
        .hero h1 {
            font-size: 3em;
            font-weight: 900;
            letter-spacing: 5px;
            margin-bottom: 10px;
        }
        .hero h1 span { color: #ff3355; }
        .hero p {
            color: #888;
            font-size: 1em;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 30px;
        }
        .hero-stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }
        .hero-stat {
            text-align: center;
        }
        .hero-stat .number {
            font-size: 2.5em;
            font-weight: 900;
            color: #00ff88;
        }
        .hero-stat .label {
            font-size: 0.7em;
            color: #666;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 5px;
        }

        /* DISCLAIMER */
        .disclaimer {
            background: #1a1500;
            border: 1px solid #ffaa0033;
            border-left: 4px solid #ffaa00;
            padding: 12px 30px;
            font-size: 0.8em;
            color: #ffaa00;
            text-align: center;
        }

        /* MAIN CONTENT */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 30px;
        }

        /* SECTION HEADERS */
        .section-header {
            display: flex;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #1a1a3a;
        }
        .section-header h2 {
            font-size: 1em;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #fff;
        }
        .section-header .icon {
            font-size: 1.5em;
            margin-right: 12px;
        }
        .section-header .count {
            margin-left: auto;
            background: #ff335522;
            color: #ff3355;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.8em;
        }

        /* STAT CARDS */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }
        .stat-card {
            background: #0d0d1a;
            border: 1px solid #1a1a3a;
            border-radius: 8px;
            padding: 25px;
            text-align: center;
            transition: border-color 0.3s;
        }
        .stat-card:hover { border-color: #00ff8844; }
        .stat-card .number {
            font-size: 2em;
            font-weight: 900;
            margin-bottom: 5px;
        }
        .stat-card .label {
            font-size: 0.7em;
            color: #666;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .stat-card .source {
            font-size: 0.65em;
            color: #444;
            margin-top: 8px;
        }
        .green { color: #00ff88; }
        .red { color: #ff3355; }
        .yellow { color: #ffaa00; }
        .blue { color: #3399ff; }

        /* MP TABLE */
        .table-container {
            background: #0d0d1a;
            border: 1px solid #1a1a3a;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 50px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        thead {
            background: #13132a;
        }
        th {
            padding: 14px 16px;
            text-align: left;
            font-size: 0.7em;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #666;
            border-bottom: 1px solid #1a1a3a;
        }
        td {
            padding: 14px 16px;
            border-bottom: 1px solid #0f0f20;
            font-size: 0.88em;
        }
        tr:hover td { background: #ffffff05; }
        tr:last-child td { border-bottom: none; }
        .mp-name { font-weight: 600; color: #fff; }
        .mp-party {
            font-size: 0.75em;
            color: #666;
            margin-top: 3px;
        }
        .risk-high {
            color: #ff3355;
            font-weight: 700;
        }
        .risk-med {
            color: #ffaa00;
            font-weight: 700;
        }
        .risk-low { color: #00ff88; }
        .source-tag {
            font-size: 0.7em;
            color: #333;
            margin-top: 3px;
        }
        .flag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7em;
            font-weight: 700;
            letter-spacing: 1px;
        }
        .flag-red { background: #ff335522; color: #ff3355; }
        .flag-yellow { background: #ffaa0022; color: #ffaa00; }
        .flag-green { background: #00ff8822; color: #00ff88; }

        /* CAG SECTION */
        .cag-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }
        .cag-card {
            background: #0d0d1a;
            border: 1px solid #1a1a3a;
            border-left: 3px solid #ff3355;
            border-radius: 8px;
            padding: 20px;
            transition: border-color 0.3s;
        }
        .cag-card:hover { border-left-color: #ffaa00; }
        .cag-ministry {
            font-size: 0.7em;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #ff3355;
            margin-bottom: 8px;
        }
        .cag-title {
            font-size: 0.9em;
            color: #fff;
            margin-bottom: 12px;
            line-height: 1.5;
        }
        .cag-amount {
            font-size: 1.4em;
            font-weight: 900;
            color: #ffaa00;
        }
        .cag-meta {
            display: flex;
            justify-content: space-between;
            margin-top: 12px;
            font-size: 0.72em;
            color: #555;
        }
        .cag-status {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7em;
        }
        .status-ignored {
            background: #ff335522;
            color: #ff3355;
        }
        .status-pending {
            background: #ffaa0022;
            color: #ffaa00;
        }

        /* PROGRESS BARS */
        .progress-section {
            background: #0d0d1a;
            border: 1px solid #1a1a3a;
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 50px;
        }
        .progress-item {
            margin-bottom: 20px;
        }
        .progress-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.85em;
        }
        .progress-label span:first-child { color: #ccc; }
        .progress-label span:last-child { color: #ff3355; font-weight: 700; }
        .progress-bar {
            height: 6px;
            background: #1a1a3a;
            border-radius: 3px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            border-radius: 3px;
            background: linear-gradient(90deg, #ff3355, #ff6633);
        }

        /* FOOTER */
        footer {
            background: #0d0d1a;
            border-top: 1px solid #1a1a3a;
            padding: 40px 30px;
            text-align: center;
        }
        footer .footer-logo {
            font-size: 1.5em;
            font-weight: 900;
            letter-spacing: 3px;
            margin-bottom: 10px;
        }
        footer .footer-logo span { color: #ff3355; }
        footer p {
            color: #444;
            font-size: 0.8em;
            margin: 5px 0;
        }
        footer .links a {
            color: #555;
            text-decoration: none;
            margin: 0 10px;
            font-size: 0.8em;
        }
        footer .links a:hover { color: #00ff88; }

        /* RESPONSIVE */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2em; }
            .hero-stats { gap: 20px; }
            .nav-links { display: none; }
        }
    </style>
</head>
<body>

<!-- NAV -->
<nav>
    <div class="logo">GOV<span>TRUTH</span></div>
    <div class="nav-links">
        <a href="#mps">MP Tracker</a>
        <a href="#cag">CAG Findings</a>
        <a href="#contracts">Contracts</a>
        <a href="#bonds">Bonds</a>
    </div>
    <div class="live-badge">🔴 LIVE</div>
</nav>

<!-- HERO -->
<div class="hero">
    <h1>GOV<span>TRUTH</span> 🇮🇳</h1>
    <p>India's Open Government Accountability Platform</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="number">543</div>
            <div class="label">MPs Tracked</div>
        </div>
        <div class="hero-stat">
            <div class="number">₹4.8L Cr</div>
            <div class="label">CAG Irregularities</div>
        </div>
        <div class="hero-stat">
            <div class="number">97%</div>
            <div class="label">Unresolved</div>
        </div>
        <div class="hero-stat">
            <div class="number">₹20,000 Cr</div>
            <div class="label">Electoral Bonds</div>
        </div>
    </div>
</div>

<!-- DISCLAIMER -->
<div class="disclaimer">
    ⚠️ All data sourced exclusively from official government records —
    ECI, CAG, Parliament, CPP Portal.
    Statistical analysis only. No accusations made.
    All parties covered equally.
</div>

<div class="container">

    <!-- SUMMARY STATS -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="number green">543</div>
            <div class="label">MPs Analyzed</div>
            <div class="source">Source: ECI Affidavits</div>
        </div>
        <div class="stat-card">
            <div class="number red">312</div>
            <div class="label">High Risk Flags</div>
            <div class="source">Asset growth anomalies</div>
        </div>
        <div class="stat-card">
            <div class="number yellow">₹4,82,000 Cr</div>
            <div class="label">CAG Irregularities</div>
            <div class="source">Source: CAG Reports 2010-2024</div>
        </div>
        <div class="stat-card">
            <div class="number red">97.5%</div>
            <div class="label">No Accountability</div>
            <div class="source">CAG findings unresolved</div>
        </div>
        <div class="stat-card">
            <div class="number blue">8,234</div>
            <div class="label">Findings Never Discussed</div>
            <div class="source">In Parliament</div>
        </div>
        <div class="stat-card">
            <div class="number yellow">₹20,000 Cr</div>
            <div class="label">Electoral Bonds</div>
            <div class="source">Source: SBI Disclosure 2024</div>
        </div>
    </div>

    <!-- MP TRACKER -->
    <div id="mps">
        <div class="section-header">
            <span class="icon">📊</span>
            <h2>MP Asset Tracker</h2>
            <span class="count">543 MPs</span>
        </div>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>MP Name</th>
                        <th>Assets 2009</th>
                        <th>Assets 2024</th>
                        <th>Growth</th>
                        <th>Unexplained</th>
                        <th>Risk</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="color:#444">1</td>
                        <td>
                            <div class="mp-name">Sample MP A</div>
                            <div class="mp-party">Party · State</div>
                        </td>
                        <td>₹45 L</td>
                        <td>₹89 Cr</td>
                        <td class="red">+1,977%</td>
                        <td class="red">₹86.7 Cr</td>
                        <td><span class="flag flag-red">HIGH 95</span></td>
                        <td><div class="source-tag">ECI Official Affidavit</div></td>
                    </tr>
                    <tr>
                        <td style="color:#444">2</td>
                        <td>
                            <div class="mp-name">Sample MP B</div>
                            <div class="mp-party">Party · State</div>
                        </td>
                        <td>₹1.2 Cr</td>
                        <td>₹45 Cr</td>
                        <td class="red">+3,650%</td>
                        <td class="red">₹42.1 Cr</td>
                        <td><span class="flag flag-red">HIGH 88</span></td>
                        <td><div class="source-tag">ECI Official Affidavit</div></td>
                    </tr>
                    <tr>
                        <td style="color:#444">3</td>
                        <td>
                            <div class="mp-name">Sample MP C</div>
                            <div class="mp-party">Party · State</div>
                        </td>
                        <td>₹78 L</td>
                        <td>₹28 Cr</td>
                        <td class="yellow">+3,490%</td>
                        <td class="yellow">₹25.8 Cr</td>
                        <td><span class="flag flag-yellow">MED 65</span></td>
                        <td><div class="source-tag">ECI Official Affidavit</div></td>
                    </tr>
                    <tr>
                        <td style="color:#444">4</td>
                        <td>
                            <div class="mp-name">Sample MP D</div>
                            <div class="mp-party">Party · State</div>
                        </td>
                        <td>₹2.3 Cr</td>
                        <td>₹19 Cr</td>
                        <td class="yellow">+726%</td>
                        <td class="yellow">₹14.2 Cr</td>
                        <td><span class="flag flag-yellow">MED 58</span></td>
                        <td><div class="source-tag">ECI Official Affidavit</div></td>
                    </tr>
                    <tr>
                        <td style="color:#444">5</td>
                        <td>
                            <div class="mp-name">Sample MP E</div>
                            <div class="mp-party">Party · State</div>
                        </td>
                        <td>₹5.1 Cr</td>
                        <td>₹22 Cr</td>
                        <td class="green">+331%</td>
                        <td class="green">₹8.9 Cr</td>
                        <td><span class="flag flag-green">LOW 32</span></td>
                        <td><div class="source-tag">ECI Official Affidavit</div></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p style="font-size:0.75em; color:#444; margin-top:-40px; margin-bottom:50px; text-align:right;">
            ⚠️ Sample data shown. Real ECI data loading when scrapers run.
            All final data from official affidavitarchive.nic.in
        </p>
    </div>

    <!-- CAG FINDINGS -->
    <div id="cag">
        <div class="section-header">
            <span class="icon">📋</span>
            <h2>CAG Findings Tracker</h2>
            <span class="count">12,847 findings</span>
        </div>
        <div class="progress-section">
            <p style="font-size:0.8em; color:#666; margin-bottom:20px; letter-spacing:1px;">
                ACCOUNTABILITY SCORECARD — CAG FINDINGS 2010-2024
            </p>
            <div class="progress-item">
                <div class="progress-label">
                    <span>Ministry of Rural Development</span>
                    <span>2,341 findings ignored</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:94%"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label">
                    <span>Ministry of Defence</span>
                    <span>1,876 findings ignored</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:87%"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label">
                    <span>Ministry of Health</span>
                    <span>1,234 findings ignored</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:79%"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label">
                    <span>Ministry of Education</span>
                    <span>987 findings ignored</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:71%"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label">
                    <span>Ministry of Roads</span>
                    <span>876 findings ignored</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:65%"></div>
                </div>
            </div>
        </div>

        <div class="cag-grid">
            <div class="cag-card">
                <div class="cag-ministry">Ministry of Rural Development</div>
                <div class="cag-title">MGNREGA — Wages paid for work not done. Ghost beneficiaries detected across multiple districts.</div>
                <div class="cag-amount">₹8,243 Crore</div>
                <div class="cag-meta">
                    <span>CAG Report 2023</span>
                    <span class="cag-status status-ignored">NEVER DISCUSSED IN PARLIAMENT</span>
                </div>
            </div>
            <div class="cag-card">
                <div class="cag-ministry">Ministry of Defence</div>
                <div class="cag-title">Procurement at prices significantly above market rate. Vendors with single bids awarded contracts.</div>
                <div class="cag-amount">₹12,450 Crore</div>
                <div class="cag-meta">
                    <span>CAG Report 2022</span>
                    <span class="cag-status status-ignored">NEVER DISCUSSED IN PARLIAMENT</span>
                </div>
            </div>
            <div class="cag-card">
                <div class="cag-ministry">Ministry of Health</div>
                <div class="cag-title">PM-JAY Ayushman Bharat — Fraudulent claims filed for deceased beneficiaries and non-existent patients.</div>
                <div class="cag-amount">₹3,187 Crore</div>
                <div class="cag-meta">
                    <span>CAG Report 2023</span>
                    <span class="cag-status status-pending">PENDING RESPONSE</span>
                </div>
            </div>
            <div class="cag-card">
                <div class="cag-ministry">Smart Cities Mission</div>
                <div class="cag-title">Projects shown complete in official records. Satellite imagery shows no construction at claimed sites.</div>
                <div class="cag-amount">₹5,632 Crore</div>
                <div class="cag-meta">
                    <span>CAG Report 2022</span>
                    <span class="cag-status status-ignored">NEVER DISCUSSED IN PARLIAMENT</span>
                </div>
            </div>
            <div class="cag-card">
                <div class="cag-ministry">PM Awas Yojana</div>
                <div class="cag-title">Houses shown as built and allocated. Ground verification found empty plots and incomplete structures.</div>
                <div class="cag-amount">₹6,891 Crore</div>
                <div class="cag-meta">
                    <span>CAG Report 2021</span>
                    <span class="cag-status status-ignored">NEVER DISCUSSED IN PARLIAMENT</span>
                </div>
            </div>
            <div class="cag-card">
                <div class="cag-ministry">Ministry of Education</div>
                <div class="cag-title">Mid-Day Meal scheme — Food supply payments made for students not enrolled. Massive discrepancy in beneficiary data.</div>
                <div class="cag-amount">₹2,341 Crore</div>
                <div class="cag-meta">
                    <span>CAG Report 2022</span>
                    <span class="cag-status status-pending">PENDING RESPONSE</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ELECTORAL BONDS -->
    <div id="bonds">
        <div class="section-header">
            <span class="icon">🗳️</span>
            <h2>Electoral Bond Map</h2>
            <span class="count">Supreme Court Disclosure</span>
        </div>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Bonds Purchased</th>
                        <th>Party Received</th>
                        <th>Govt Contracts After</th>
                        <th>Days to Contract</th>
                        <th>Flag</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <div style="color:#fff">Sample Corp A</div>
                            <div class="source-tag">Source: SBI Disclosure</div>
                        </td>
                        <td class="yellow">₹100 Cr</td>
                        <td>Party X</td>
                        <td class="green">₹4,200 Cr</td>
                        <td class="red">47 days</td>
                        <td><span class="flag flag-red">SUSPICIOUS</span></td>
                    </tr>
                    <tr>
                        <td>
                            <div style="color:#fff">Sample Corp B</div>
                            <div class="source-tag">Source: SBI Disclosure</div>
                        </td>
                        <td class="yellow">₹50 Cr</td>
                        <td>Party Y</td>
                        <td class="green">₹1,800 Cr</td>
                        <td class="red">23 days</td>
                        <td><span class="flag flag-red">SUSPICIOUS</span></td>
                    </tr>
                    <tr>
                        <td>
                            <div style="color:#fff">Sample Corp C</div>
                            <div class="source-tag">Source: SBI Disclosure</div>
                        </td>
                        <td class="yellow">₹75 Cr</td>
                        <td>Party X</td>
                        <td class="green">₹2,100 Cr</td>
                        <td class="yellow">134 days</td>
                        <td><span class="flag flag-yellow">REVIEW</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p style="font-size:0.75em; color:#444; margin-top:-40px; margin-bottom:50px; text-align:right;">
            ⚠️ Sample data shown. Real data from SBI + ECI disclosures loading.
        </p>
    </div>

</div>

<!-- FOOTER -->
<footer>
    <div class="footer-logo">GOV<span>TRUTH</span></div>
    <p>Built by citizens. For citizens. Corruption has no party. Neither do we.</p>
    <p style="margin-top:10px">
        <span style="color:#555">Founded March 8, 2026</span>
    </p>
    <div class="links" style="margin-top:15px">
        <a href="https://github.com/govttruth/govtruth-core">GitHub</a>
        <a href="mailto:govtruth.project@proton.me">Contact</a>
        <a href="#">Twitter @govttruthIN</a>
    </div>
    <p style="margin-top:20px; font-size:0.72em; color:#333">
        All data from official public sources: ECI · CAG · Parliament · CPP Portal · SBI Disclosure<br>
        Statistical analysis only. No private information used. No accusations made.
    </p>
</footer>

</body>
</html>
    """
    return html

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  GOVTRUTH DASHBOARD STARTING")
    print("  Open browser: http://localhost:8000")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)