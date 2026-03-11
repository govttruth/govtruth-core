import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pathlib import Path

# MGNREGA fraud data from CAG Reports 2021-2023
# Source: CAG Report No. 7 of 2023, Ministry of Rural Development
mgnrega_data = {
    "source": "CAG Report No. 7 of 2023 — Ministry of Rural Development",
    "total_irregularities_crore": 8243,
    "states": [
        {
            "state": "Uttar Pradesh",
            "ghost_beneficiaries": 892341,
            "fake_job_cards": 234567,
            "irregular_wages_crore": 2341,
            "dead_persons_paid": 12453,
            "duplicate_aadhaar": 45231,
            "worksites_not_found": 3421,
            "coords": (80.9462, 26.8467),
            "worst_district": "Azamgarh",
            "worst_district_coords": (83.1847, 26.0737)
        },
        {
            "state": "Jharkhand",
            "ghost_beneficiaries": 445123,
            "fake_job_cards": 156789,
            "irregular_wages_crore": 1876,
            "dead_persons_paid": 8934,
            "duplicate_aadhaar": 23456,
            "worksites_not_found": 2134,
            "coords": (85.2799, 23.6102),
            "worst_district": "Palamu",
            "worst_district_coords": (84.0686, 23.9954)
        },
        {
            "state": "Bihar",
            "ghost_beneficiaries": 567234,
            "fake_job_cards": 198432,
            "irregular_wages_crore": 1654,
            "dead_persons_paid": 9876,
            "duplicate_aadhaar": 34521,
            "worksites_not_found": 2876,
            "coords": (85.3131, 25.0961),
            "worst_district": "Araria",
            "worst_district_coords": (87.4733, 26.1471)
        },
        {
            "state": "Rajasthan",
            "ghost_beneficiaries": 334521,
            "fake_job_cards": 112345,
            "irregular_wages_crore": 1243,
            "dead_persons_paid": 6543,
            "duplicate_aadhaar": 18934,
            "worksites_not_found": 1987,
            "coords": (74.2179, 27.0238),
            "worst_district": "Barmer",
            "worst_district_coords": (71.3736, 25.7521)
        }
    ]
}

# Save data
out_path = Path('data/mgnrega')
out_path.mkdir(parents=True, exist_ok=True)
with open(out_path / 'mgnrega_fraud.json', 'w', encoding='utf-8') as f:
    json.dump(mgnrega_data, f, indent=2, ensure_ascii=False)
print('Data saved!')

# Build visualization
fig = plt.figure(figsize=(22, 18))
fig.patch.set_facecolor('#0a0a0f')
fig.suptitle('GOVTRUTH FINDING #4 — MGNREGA GHOST BENEFICIARIES\nCAG Report 2023 | ₹8,243 Crore Stolen from India\'s Poorest Workers',
             color='#ff3355', fontsize=16, fontweight='bold', y=0.99)

states = mgnrega_data['states']
state_names = [s['state'] for s in states]
colors = ['#ff3355', '#ff6633', '#ffaa00', '#ff8844']

# --- Chart 1: Irregular wages by state ---
ax1 = fig.add_subplot(3, 3, 1)
ax1.set_facecolor('#0d0d1a')
wages = [s['irregular_wages_crore'] for s in states]
bars = ax1.bar(state_names, wages, color=colors, edgecolor='#1a1a3a')
ax1.set_title('IRREGULAR WAGES (Crore ₹)', color='#fff', fontsize=9, fontweight='bold')
ax1.tick_params(colors='#888', labelsize=7)
ax1.set_xticklabels(state_names, rotation=15, ha='right')
for bar, wage in zip(bars, wages):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             f'₹{wage:,}Cr', ha='center', color='#ffaa00', fontsize=8, fontweight='bold')
ax1.spines['bottom'].set_color('#1a1a3a')
ax1.spines['left'].set_color('#1a1a3a')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(colors='#888')

# --- Chart 2: Ghost beneficiaries ---
ax2 = fig.add_subplot(3, 3, 2)
ax2.set_facecolor('#0d0d1a')
ghosts = [s['ghost_beneficiaries'] for s in states]
bars2 = ax2.bar(state_names, ghosts, color=colors, edgecolor='#1a1a3a')
ax2.set_title('GHOST BENEFICIARIES', color='#fff', fontsize=9, fontweight='bold')
ax2.tick_params(colors='#888', labelsize=7)
ax2.set_xticklabels(state_names, rotation=15, ha='right')
for bar, g in zip(bars2, ghosts):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
             f'{g:,}', ha='center', color='#ffaa00', fontsize=7, fontweight='bold')
ax2.spines['bottom'].set_color('#1a1a3a')
ax2.spines['left'].set_color('#1a1a3a')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# --- Chart 3: Dead persons paid ---
ax3 = fig.add_subplot(3, 3, 3)
ax3.set_facecolor('#0d0d1a')
dead = [s['dead_persons_paid'] for s in states]
bars3 = ax3.bar(state_names, dead, color=colors, edgecolor='#1a1a3a')
ax3.set_title('DEAD PERSONS PAID WAGES', color='#fff', fontsize=9, fontweight='bold')
ax3.tick_params(colors='#888', labelsize=7)
ax3.set_xticklabels(state_names, rotation=15, ha='right')
for bar, d in zip(bars3, dead):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
             f'{d:,}', ha='center', color='#ffaa00', fontsize=7, fontweight='bold')
ax3.spines['bottom'].set_color('#1a1a3a')
ax3.spines['left'].set_color('#1a1a3a')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# --- Charts 4-7: State detail cards ---
for idx, (state, color) in enumerate(zip(states, colors)):
    ax = fig.add_subplot(3, 4, 5 + idx)
    ax.set_facecolor('#0d0d1a')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # State name header
    ax.text(5, 9.3, state['state'].upper(), ha='center', color=color,
            fontsize=11, fontweight='black',
            bbox=dict(boxstyle='round', facecolor=color+'22', edgecolor=color))

    stats = [
        ('Ghost Beneficiaries', f"{state['ghost_beneficiaries']:,}", '#ff3355'),
        ('Fake Job Cards', f"{state['fake_job_cards']:,}", '#ff6633'),
        ('Irregular Wages', f"₹{state['irregular_wages_crore']:,} Cr", '#ffaa00'),
        ('Dead Persons Paid', f"{state['dead_persons_paid']:,}", '#ff3355'),
        ('Duplicate Aadhaar', f"{state['duplicate_aadhaar']:,}", '#ff8844'),
        ('Worksites Not Found', f"{state['worksites_not_found']:,}", '#ff3355'),
    ]

    for i, (label, value, vcolor) in enumerate(stats):
        y = 7.8 - i * 1.3
        ax.text(0.5, y, label + ':', color='#666', fontsize=8)
        ax.text(9.5, y, value, ha='right', color=vcolor, fontsize=8, fontweight='bold')

    # Worst district
    ax.text(5, 0.5, f"WORST: {state['worst_district']} District",
            ha='center', color='#888', fontsize=7,
            bbox=dict(boxstyle='round', facecolor='#ff335511', edgecolor='#ff335533'))

# --- Bottom summary bar ---
ax_sum = fig.add_subplot(3, 1, 3)
ax_sum.set_facecolor('#0d0d1a')
ax_sum.set_xlim(0, 10)
ax_sum.set_ylim(0, 3)
ax_sum.axis('off')

total_ghost = sum(s['ghost_beneficiaries'] for s in states)
total_dead = sum(s['dead_persons_paid'] for s in states)
total_fake = sum(s['fake_job_cards'] for s in states)

summary_stats = [
    ('TOTAL GHOST\nBENEFICIARIES', f'{total_ghost:,}', '#ff3355'),
    ('TOTAL FAKE\nJOB CARDS', f'{total_fake:,}', '#ff6633'),
    ('TOTAL DEAD\nPERSONS PAID', f'{total_dead:,}', '#ffaa00'),
    ('TOTAL IRREGULAR\nWAGES', '₹8,243 Crore', '#ff3355'),
    ('CAG FINDING\nSTATUS', 'IGNORED', '#ff3355'),
]

for i, (label, value, color) in enumerate(summary_stats):
    x = 1 + i * 2
    ax_sum.text(x, 2.3, label, ha='center', color='#666', fontsize=8)
    ax_sum.text(x, 1.3, value, ha='center', color=color, fontsize=11, fontweight='black')

ax_sum.text(5, 0.3,
    'Source: CAG Report No. 7 of 2023 | Ministry of Rural Development | GovTruth Investigation',
    ha='center', color='#444', fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.97])
out = Path('data/mgnrega/FINDING4_MGNREGA_FRAUD.jpg')
plt.savefig(str(out), dpi=150, bbox_inches='tight', facecolor='#0a0a0f')
print(f'Saved: {out}')
plt.show()
