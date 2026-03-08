"""
CAG Report Downloader
=====================
Downloads audit reports from Comptroller &
Auditor General of India.

Source: https://cag.gov.in/en/audit-report
Legal: Publicly available constitutional audit reports
"""

import requests
import os
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('GovTruth.CAG')


class CAGDownloader:
    """
    Downloads official CAG audit reports.
    These reports document government irregularities
    and are public constitutional documents.
    """

    BASE_URL = "https://cag.gov.in"
    REPORTS_URL = "https://cag.gov.in/en/audit-report"

    def __init__(self, data_dir='data/raw/cag'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': (
                'GovTruth-Research/1.0 '
                'India Accountability Research '
                'Contact: govtruth.project@proton.me'
            )
        })
        logger.info(f"CAGDownloader ready. Dir: {self.data_dir}")

    def get_report_links(self):
        """Scrape list of available CAG reports"""
        logger.info("Fetching CAG report index...")

        try:
            response = self.session.get(
                self.REPORTS_URL,
                timeout=30
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find PDF links
            pdf_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)

                if '.pdf' in href.lower():
                    full_url = href
                    if not href.startswith('http'):
                        full_url = self.BASE_URL + href

                    pdf_links.append({
                        'url': full_url,
                        'title': text,
                        'filename': href.split('/')[-1]
                    })

            logger.info(f"Found {len(pdf_links)} CAG reports")
            return pdf_links

        except Exception as e:
            logger.error(f"Failed to fetch index: {e}")
            return []

    def download_report(self, report_info):
        """Download single CAG report PDF"""
        filepath = self.data_dir / report_info['filename']

        # Skip if already downloaded
        if filepath.exists():
            logger.info(f"Already have: {report_info['filename']}")
            return {'status': 'skipped', 'file': str(filepath)}

        try:
            logger.info(f"Downloading: {report_info['filename']}")
            response = self.session.get(
                report_info['url'],
                timeout=60
            )
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                f.write(response.content)

            size_mb = len(response.content) / 1024 / 1024
            logger.info(f"Saved: {report_info['filename']} ({size_mb:.1f}MB)")

            # Respectful delay
            time.sleep(2)

            return {
                'status': 'success',
                'file': str(filepath),
                'size_mb': round(size_mb, 2),
                'title': report_info['title']
            }

        except Exception as e:
            logger.error(f"Failed {report_info['filename']}: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'url': report_info['url']
            }

    def download_all(self, limit=30):
        """Download all available CAG reports"""
        logger.info("=" * 50)
        logger.info("GovTruth - CAG Download Starting")
        logger.info("=" * 50)

        reports = self.get_report_links()

        if not reports:
            logger.error("No reports found. Check connection.")
            return

        # Download up to limit
        to_download = reports[:limit]
        logger.info(f"Downloading {len(to_download)} reports...")

        results = []
        for i, report in enumerate(to_download, 1):
            logger.info(f"Progress: {i}/{len(to_download)}")
            result = self.download_report(report)
            results.append(result)

        # Summary
        success = sum(1 for r in results if r['status'] == 'success')
        skipped = sum(1 for r in results if r['status'] == 'skipped')

        summary = {
            'date': datetime.now().isoformat(),
            'source': 'CAG of India - cag.gov.in',
            'total_found': len(reports),
            'downloaded': success,
            'skipped': skipped,
            'results': results
        }

        summary_path = self.data_dir / 'download_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Done! Downloaded: {success}, Skipped: {skipped}")
        logger.info(f"Next step: Run analyzers/cag_parser.py")

        return summary


if __name__ == "__main__":
    print("\nGovTruth - CAG Report Downloader")
    print("Source: Comptroller & Auditor General of India")
    print("=" * 40)

    downloader = CAGDownloader()
    summary = downloader.download_all(limit=30)

    if summary:
        print(f"\nDownloaded: {summary['downloaded']} reports")
        print(f"Saved to: data/raw/cag/")
```

Commit message:
```
Add CAG report downloader - government audit data pipeline
```

---

**Step 8 — Fourth file**

Name:
```
analyzers/mp_asset_analyzer.py
