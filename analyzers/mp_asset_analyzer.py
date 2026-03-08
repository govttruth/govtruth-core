"""
MP Asset Analyzer
=================
Analyzes MP asset declarations from ECI affidavits.
Flags statistical anomalies for public awareness.

Source: Election Commission of India
Legal: All data from official public records
Note: Flags anomalies only. Not accusations.
      Asset growth may have legitimate explanations.
"""

import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GovTruth.AssetAnalyzer')

# Parliamentary salary is public record
# Basic pay + allowances (approximate)
PARLIAMENTARY_SALARY = {
    2004: 432000,    # ₹4.32 lakh/year
    2009: 528000,    # ₹5.28 lakh/year
    2014: 1800000,   # ₹18 lakh/year
    2019: 2400000,   # ₹24 lakh/year
    2024: 2400000,   # ₹24 lakh/year
}


class MPAssetAnalyzer:
    """
    Analyzes MP wealth declarations across elections.
    Uses only official ECI affidavit data.
    """

    def analyze_mp(self, mp_data):
        """
        Analyze single MP across multiple elections.
        mp_data = list of affidavit records by year
        """
        if len(mp_data) < 2:
            return None  # Need at least 2 elections to compare

        # Sort by year
        records = sorted(mp_data, key=lambda x: x['election_year'])

        name = records[0]['mp_name']
        party = records[0]['party']
        state = records[0]['state']

        first = records[0]
        latest = records[-1]

        # Asset growth
        total_growth = (
            (latest['total_assets'] or 0) -
            (first['total_assets'] or 0)
        )

        # Estimate maximum legitimate income
        # Salary + declared non-salary income
        legitimate_income = 0
        for i in range(len(records) - 1):
            years_in_term = records[i+1]['election_year'] - records[i]['election_year']
            annual_salary = PARLIAMENTARY_SALARY.get(
                records[i]['election_year'], 2400000
            )
            legitimate_income += annual_salary * years_in_term

        # Add declared income from affidavits
        declared_other = sum(
            r.get('declared_income', 0) or 0
            for r in records
        )
        legitimate_income += declared_other

        # Unexplained = growth minus what salary could explain
        unexplained = max(0, total_growth - legitimate_income)

        # Risk score
        risk_score = self._calculate_risk(
            unexplained,
            total_growth,
            records[0].get('criminal_cases', 0)
        )

        return {
            'name': name,
            'party': party,
            'state': state,
            'elections_analyzed': len(records),
            'first_year': first['election_year'],
            'latest_year': latest['election_year'],
            'assets_first': first.get('total_assets', 0),
            'assets_latest': latest.get('total_assets', 0),
            'total_growth': total_growth,
            'legitimate_income_estimate': legitimate_income,
            'unexplained_growth': unexplained,
            'growth_multiple': round(
                total_growth / legitimate_income
                if legitimate_income > 0 else 0, 2
            ),
            'criminal_cases': records[-1].get('criminal_cases', 0),
            'risk_score': risk_score,
            'data_source': 'Election Commission of India',
            'source_url': 'https://affidavitarchive.nic.in',
            'disclaimer': (
                'Statistical anomaly flag only. '
                'Asset growth may have legitimate explanations. '
                'All figures from official ECI affidavits.'
            ),
            'analyzed_at': datetime.now().isoformat()
        }

    def _calculate_risk(self, unexplained, total_growth, criminal_cases):
        """Calculate risk score 0-100"""
        score = 0

        # Unexplained growth thresholds
        if unexplained > 1_00_00_00_000:    # 100 crore
            score += 50
        elif unexplained > 10_00_00_000:    # 10 crore
            score += 35
        elif unexplained > 1_00_00_000:     # 1 crore
            score += 20
        elif unexplained > 10_00_000:       # 10 lakh
            score += 10

        # Growth ratio
        if total_growth > 0 and unexplained > 0:
            ratio = unexplained / total_growth
            if ratio > 0.9:
                score += 30
            elif ratio > 0.7:
                score += 20
            elif ratio > 0.5:
                score += 10

        # Criminal cases
        if criminal_cases and criminal_cases > 0:
            score += min(criminal_cases * 5, 20)

        return min(score, 100)

    def generate_report(self, all_mp_data):
        """
        Generate full analysis report for all MPs
        all_mp_data = dict of {mp_name: [list of records]}
        """
        logger.info("Starting MP asset analysis...")

        results = []
        for mp_name, records in all_mp_data.items():
            analysis = self.analyze_mp(records)
            if analysis and analysis['risk_score'] > 0:
                results.append(analysis)

        # Sort by unexplained growth
        results.sort(
            key=lambda x: x['unexplained_growth'],
            reverse=True
        )

        # Summary stats
        total_unexplained = sum(r['unexplained_growth'] for r in results)
        high_risk = [r for r in results if r['risk_score'] >= 70]
        medium_risk = [r for r in results if 40 <= r['risk_score'] < 70]

        report = {
            'generated_at': datetime.now().isoformat(),
            'data_source': 'Election Commission of India',
            'source_url': 'affidavitarchive.nic.in',
            'disclaimer': (
                'This report flags statistical anomalies only. '
                'All data from official ECI public affidavits. '
                'No accusations are made. Asset growth may '
                'have legitimate explanations.'
            ),
            'summary': {
                'total_mps_analyzed': len(results),
                'high_risk_flags': len(high_risk),
                'medium_risk_flags': len(medium_risk),
                'total_unexplained_growth_crore': round(
                    total_unexplained / 10_00_000, 2
                )
            },
            'findings': results
        }

        return report

    def print_report(self, report, top_n=20):
        """Print human readable report"""
        print("\n" + "=" * 65)
        print("GOVTRUTH — MP ASSET ANALYSIS")
        print("Source: Election Commission of India — Official Affidavits")
        print("=" * 65)

        s = report['summary']
        print(f"\nTotal MPs analyzed:      {s['total_mps_analyzed']}")
        print(f"High risk flags (70+):   {s['high_risk_flags']}")
        print(f"Medium risk flags:       {s['medium_risk_flags']}")
        print(
            f"Total unexplained growth: "
            f"₹{s['total_unexplained_growth_crore']:,.2f} crore"
        )

        print(f"\nTOP {top_n} STATISTICAL ANOMALIES:")
        print("-" * 65)

        for i, mp in enumerate(report['findings'][:top_n], 1):
            print(f"\n{i:3}. {mp['name']}")
            print(f"     Party: {mp['party']} | State: {mp['state']}")
            print(
                f"     {mp['first_year']} Assets:  "
                f"₹{mp['assets_first']:>15,}"
            )
            print(
                f"     {mp['latest_year']} Assets:  "
                f"₹{mp['assets_latest']:>15,}"
            )
            print(
                f"     Total Growth:     "
                f"₹{mp['total_growth']:>15,}"
            )
            print(
                f"     Salary (estimate):₹{mp['legitimate_income_estimate']:>15,}"
            )
            print(
                f"     Unexplained:      "
                f"₹{mp['unexplained_growth']:>15,}"
            )
            print(f"     Risk Score:       {mp['risk_score']}/100")
            if mp['criminal_cases'] > 0:
                print(f"     Criminal Cases:   {mp['criminal_cases']}")
            print(f"     Source: {mp['data_source']}")

        print("\n" + "=" * 65)
        print("DISCLAIMER:", report['disclaimer'])
        print("=" * 65)


if __name__ == "__main__":
    # Example with sample data
    # In production this reads from PostgreSQL database
    print("GovTruth MP Asset Analyzer")
    print("Connect to database and run analyze_mp() for each MP")
    print("Source data: affidavitarchive.nic.in")
```

Commit message:
```
Add MP asset analyzer - statistical anomaly detection
```

---

**After all 4 files — your repo looks like:**
```
govttruth/govtruth-core
├── README.md               ✅
├── ROADMAP.md              ✅
├── LICENSE                 ✅
├── .gitignore              ✅
├── database/
│   └── schema.sql          ✅ NEW
├── scrapers/
│   ├── eci_collector.py    ✅ NEW
│   └── cag_downloader.py   ✅ NEW
├── analyzers/
│   └── mp_asset_analyzer.py ✅ NEW
└── docs/
    └── (existing)
