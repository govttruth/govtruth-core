import base64
from pathlib import Path

# Load Finding #3 image
img_path = Path('data/electoral_bonds/FINDING3_ELECTORAL_BONDS.jpg')
with open(img_path, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')

print(f'Image loaded: {len(img_b64)//1024}KB')

# Read dashboard
with open('dashboard.py', encoding='utf-8') as f:
    content = f.read()

# Finding #3 HTML
finding3_html = f"""
        <div style="background:#0d0d1a;border:1px solid #1a1a3a;border-radius:8px;padding:30px;margin-top:20px;">
            <div style="display:flex;gap:30px;flex-wrap:wrap;align-items:flex-start;">
                <div style="flex:1;min-width:280px;">
                    <div style="color:#ff3355;font-size:0.7em;letter-spacing:2px;margin-bottom:10px;">GOVTRUTH FINDING #3</div>
                    <h3 style="color:#fff;font-size:1.2em;margin-bottom:15px;">Electoral Bonds — Quid Pro Quo</h3>
                    <div style="color:#888;font-size:0.85em;line-height:2.2;">
                        <div><span style="color:#ffaa00;">TOTAL BONDS:</span> ₹20,000 Crore (2018-2024)</div>
                        <div><span style="color:#ffaa00;">BJP RECEIVED:</span> ₹6,566 Crore (47%)</div>
                        <div><span style="color:#ffaa00;">SOURCE:</span> Supreme Court — SBI Disclosure 2024</div>
                    </div>
                    <div style="margin-top:20px;line-height:2.4;">
                        <div style="color:#ff3355;">❌ Megha Engg: Donated ₹966 Cr → Got ₹14,400 Cr contract</div>
                        <div style="color:#ff3355;">❌ 14 companies under ED/CBI donated ₹3,731 Cr</div>
                        <div style="color:#ff3355;">❌ SBI asked 30 years to disclose — SC gave 15 days</div>
                        <div style="color:#ffaa00;">⚠️ Return on investment: 14.9x</div>
                    </div>
                    <div style="margin-top:20px;background:#ff335522;border:1px solid #ff335544;border-radius:8px;padding:15px;text-align:center;">
                        <div style="color:#ff3355;font-size:1.1em;font-weight:900;">🔴 VERDICT: QUID PRO QUO CONFIRMED</div>
                    </div>
                </div>
                <div style="flex:2;min-width:300px;">
                    <img src="data:image/jpeg;base64,{img_b64}" style="width:100%;border-radius:8px;border:1px solid #1a1a3a;" alt="Electoral Bonds Analysis"/>
                </div>
            </div>
        </div>
"""

# Insert before CAG section
end_marker = '    </div>\n\n    <div id="cag">'
if end_marker in content:
    content = content.replace(end_marker, finding3_html + '\n    </div>\n\n    <div id="cag">')
    print('Finding #3 added!')
else:
    print('ERROR: insertion point not found')

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

import ast
try:
    ast.parse(content)
    print('Python syntax OK!')
except SyntaxError as e:
    print(f'Syntax error at line {e.lineno}: {e.msg}')
