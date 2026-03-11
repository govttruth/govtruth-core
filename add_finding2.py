import base64
from pathlib import Path

# Load Finding #2 image
img_path = Path('data/satellite/google/Army_Golf_Club_FINDING2.jpg')
with open(img_path, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')

print(f'Image loaded: {len(img_b64)//1024}KB')

# Read dashboard
with open('dashboard.py', encoding='utf-8') as f:
    content = f.read()

# New finding #2 HTML to add after finding #1
finding2_html = f"""
        <div style="background:#0d0d1a;border:1px solid #1a1a3a;border-radius:8px;padding:30px;margin-top:20px;">
            <div style="display:flex;gap:30px;flex-wrap:wrap;align-items:flex-start;">
                <div style="flex:1;min-width:280px;">
                    <div style="color:#ff3355;font-size:0.7em;letter-spacing:2px;margin-bottom:10px;">GOVTRUTH FINDING #2</div>
                    <h3 style="color:#fff;font-size:1.2em;margin-bottom:15px;">Army Golf Club Delhi — Defence Land Misuse</h3>
                    <div style="color:#888;font-size:0.85em;line-height:2.2;">
                        <div><span style="color:#ffaa00;">LAND:</span> 130 Acres Prime Delhi Defence Land</div>
                        <div><span style="color:#ffaa00;">VALUE:</span> 15,000+ Crore at market rates</div>
                        <div><span style="color:#ffaa00;">USED AS:</span> Private Golf Course for Officers</div>
                        <div><span style="color:#ffaa00;">COORDS:</span> 28.6015N, 77.1588E</div>
                    </div>
                    <div style="margin-top:20px;line-height:2.4;">
                        <div style="color:#ff3355;">❌ Delhi has 2 Million housing unit shortage</div>
                        <div style="color:#ff3355;">❌ CAG flagged misuse in 2019</div>
                        <div style="color:#ff3355;">❌ Zero action taken</div>
                        <div style="color:#00ff88;">✅ Golf greens confirmed from satellite</div>
                    </div>
                    <div style="margin-top:20px;background:#ff335522;border:1px solid #ff335544;border-radius:8px;padding:15px;text-align:center;">
                        <div style="color:#ff3355;font-size:1.1em;font-weight:900;">🔴 VERDICT: NOT JUSTIFIED</div>
                    </div>
                </div>
                <div style="flex:2;min-width:300px;">
                    <img src="data:image/jpeg;base64,{img_b64}" style="width:100%;border-radius:8px;border:1px solid #1a1a3a;" alt="Army Golf Club Delhi Satellite"/>
                </div>
            </div>
        </div>
"""

# Insert after the first finding div closes inside satellite section
insert_marker = '                    <div style="margin-top:20px;background:#ffaa0022;border:1px solid #ffaa0044;border-radius:8px;padding:15px;text-align:center;">\n                        <div style="color:#ffaa00;font-size:1.1em;font-weight:900;">⚠️ VERDICT: PARTIAL</div>\n                    </div>\n                </div>\n                <div style="flex:2;min-width:300px;">'

# Find the end of the satellite section div
end_marker = '    </div>\n\n    <div id="cag">'

if end_marker in content:
    content = content.replace(end_marker, finding2_html + '\n    </div>\n\n    <div id="cag">')
    print('Finding #2 added to dashboard!')
else:
    print('ERROR: Could not find insertion point')
    print('Looking for cag section...')
    idx = content.find('<div id="cag">')
    print(f'CAG section at position: {idx}')

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
import ast
try:
    ast.parse(content)
    print('Python syntax OK!')
except SyntaxError as e:
    print(f'Syntax error at line {e.lineno}: {e.msg}')
