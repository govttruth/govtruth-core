"""
ECI Affidavit Collector
=======================
Collects MP asset declarations from
Election Commission of India official archive.

Source: https://affidavitarchive.nic.in
Legal: Supreme Court mandated public disclosure
"""

import requests
import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('GovTruth.ECI')


class ECICollector:

    BASE_URL = "https://affidavitarchive.nic.in"

    ELECTIONS = {
        'GE2024': 'S18',
        'GE2019': 'S17',
        'GE2014': 'S16',
        'GE2009': 'S15',
    }

    def __init__(self, data_dir='data/raw/eci'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': (
                'GovTruth-Research/1.0 '
                'Contact: govtruth.project@proton.me'
            )
        })
        logger.info(f"ECICollector ready. Dir: {self.data_dir}")

    def collect_election(self, code, name):
        logger.info(f"Collecting: {name}")
        url = f"{self.BASE_URL}/DynamicAffidavit.aspx"
        try:
            response = self.session.get(
                url, params={'ecode': code}, timeout=30
            )
            response.raise_for_status()
            filepath = self.data_dir / f"{name}.html"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info(f"Saved {name}: {len(response.text):,} bytes")
            time.sleep(3)
            return {'election': name, 'status': 'success',
                    'file': str(filepath)}
        except Exception as e:
            logger.error(f"Failed {name}: {e}")
            return {'election': name, 'status': 'failed', 'error': str(e)}

    def collect_all(self):
        logger.info("GovTruth - ECI Collection Starting")
        results = []
        for name, code in self.ELECTIONS.items():
            result = self.collect_election(code, name)
            results.append(result)
        report = {
            'date': datetime.now().isoformat(),
            'source': 'Election Commission of India',
            'source_url': 'https://affidavitarchive.nic.in',
            'successful': sum(1 for r in results if r['status'] == 'success'),
            'results': results
        }
        report_path = self.data_dir / 'collection_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Done. Success: {report['successful']}/{len(results)}")
        return report


if __name__ == "__main__":
    print("GovTruth - ECI Affidavit Collector")
    print("Source: Election Commission of India")
    collector = ECICollector()
    report = collector.collect_all()
    print(f"Complete: {report['successful']} elections downloaded")
```

Then scroll up and click **"Commit changes"**

Commit message:
```
Fix eci_collector.py - clean Python code only
