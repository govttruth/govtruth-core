import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Load data
with open('data/electoral_bonds/bonds_analysis.json', encoding='utf-8') as f:
    data = json.load(f)

fig = plt.figure(figsize=(20, 16))
fig.patch.set_facecolor('#0a0a0f')
fig.suptitle('GOVTRUTH FINDING #3 — ELECTORAL BONDS QUID PRO QUO\nSupreme Court Forced SBI Disclosure — March 2024',
             color='#ff3355', fontsize=16, fontweight='bold', y=0.98)

# --- CHART 1: Party-wise bonds (top left) ---
ax1 = fig.add_subplot(2, 2, 1)
ax1.set_facecolor('#0d0d1a')
parties = [p['party'] for p in data['party_wise']]
amounts = [p['amount_crore'] for p in data['party_wise']]
colors = ['#ff3355' if p == 'BJP' else '#3399ff' if p == 'INC' else '#ffaa00' for p in parties]
bars = ax1.barh(parties, amounts, color=colors, edgecolor='#1a1a3a')
ax1.set_xlabel('Amount (Crore ₹)', color='#888', fontsize=9)
ax1.set_title('PARTY-WISE BONDS RECEIVED', color='#fff', fontsize=10, fontweight='bold', pad=10)
ax1.tick_params(colors='#888', labelsize=8)
ax1.spines['bottom'].set_color('#1a1a3a')
ax1.spines['left'].set_color('#1a1a3a')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
for bar, amount in zip(bars, amounts):
    ax1.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2,
             f'₹{amount:,} Cr', va='center', color='#ffaa00', fontsize=8, fontweight='bold')

# --- CHART 2: Quid pro quo cases (top right) ---
ax2 = fig.add_subplot(2, 2, 2)
ax2.set_facecolor('#0d0d1a')
cases = data['quid_pro_quo_cases']
companies = [c['company'][:25] for c in cases]
donated = [c['bond_amount_crore'] for c in cases]
received = [c['govt_contracts_crore'] for c in cases]

x = np.arange(len(companies))
width = 0.35
bars1 = ax2.bar(x - width/2, donated, width, label='Bonds Donated (Cr)', color='#ff3355', alpha=0.9)
bars2 = ax2.bar(x + width/2, received, width, label='Contracts Received (Cr)', color='#00ff88', alpha=0.9)
ax2.set_title('DONATED vs CONTRACTS RECEIVED', color='#fff', fontsize=10, fontweight='bold', pad=10)
ax2.set_xticks(x)
ax2.set_xticklabels([c[:15] for c in companies], rotation=45, ha='right', color='#888', fontsize=7)
ax2.tick_params(colors='#888', labelsize=8)
ax2.legend(fontsize=8, facecolor='#0d0d1a', labelcolor='#888', edgecolor='#1a1a3a')
ax2.spines['bottom'].set_color('#1a1a3a')
ax2.spines['left'].set_color('#1a1a3a')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_ylabel('Amount (Crore ₹)', color='#888', fontsize=9)

# --- CHART 3: Key findings text (bottom left) ---
ax3 = fig.add_subplot(2, 2, 3)
ax3.set_facecolor('#0d0d1a')
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 10)
ax3.axis('off')
ax3.set_title('KEY FINDINGS', color='#fff', fontsize=10, fontweight='bold', pad=10)

findings = data['key_findings']
for i, finding in enumerate(findings):
    y_pos = 8.5 - i * 1.6
    ax3.text(0.3, y_pos, '⚠️', fontsize=12, va='center')
    # Wrap text
    words = finding.split()
    lines = []
    line = ''
    for word in words:
        if len(line + word) < 55:
            line += word + ' '
        else:
            lines.append(line.strip())
            line = word + ' '
    lines.append(line.strip())
    for j, l in enumerate(lines[:2]):
        ax3.text(1.0, y_pos - j*0.5, l, color='#ffaa00' if i < 2 else '#ccc',
                fontsize=8, fontweight='bold' if i < 2 else 'normal', va='center')

# --- CHART 4: Biggest scandal highlight (bottom right) ---
ax4 = fig.add_subplot(2, 2, 4)
ax4.set_facecolor('#0d0d1a')
ax4.axis('off')
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)

ax4.text(5, 9.2, 'BIGGEST QUID PRO QUO', ha='center', color='#ff3355',
         fontsize=11, fontweight='bold', transform=ax4.transAxes,
         bbox=dict(boxstyle='round', facecolor='#ff335522', edgecolor='#ff3355'))

ax4.text(5, 8.0, 'Megha Engineering', ha='center', color='#fff', fontsize=14, fontweight='black')
ax4.text(5, 7.2, '& Infrastructures', ha='center', color='#fff', fontsize=14, fontweight='black')

ax4.text(5, 6.0, 'DONATED', ha='center', color='#888', fontsize=10)
ax4.text(5, 5.3, '₹966 Crore', ha='center', color='#ff3355', fontsize=20, fontweight='black')
ax4.text(5, 4.5, 'in Electoral Bonds to BJP + BRS', ha='center', color='#888', fontsize=9)

ax4.annotate('', xy=(5, 3.5), xytext=(5, 4.0),
    arrowprops=dict(arrowstyle='->', color='#ffaa00', lw=3))

ax4.text(5, 2.8, 'RECEIVED', ha='center', color='#888', fontsize=10)
ax4.text(5, 2.0, '₹14,400 Crore', ha='center', color='#00ff88', fontsize=20, fontweight='black')
ax4.text(5, 1.3, 'Kaleshwaram Irrigation Contract', ha='center', color='#888', fontsize=9)

ax4.text(5, 0.4, 'RETURN: 14.9x THE INVESTMENT',
         ha='center', color='#ffaa00', fontsize=10, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='#ffaa0022', edgecolor='#ffaa00'))

plt.tight_layout(rect=[0, 0, 1, 0.96])
out = Path('data/electoral_bonds/FINDING3_ELECTORAL_BONDS.jpg')
plt.savefig(str(out), dpi=150, bbox_inches='tight', facecolor='#0a0a0f')
print(f'Saved: {out}')
plt.show()
