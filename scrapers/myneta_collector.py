import requests
import json
import time
import logging
from pathlib import Path
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('GovTruth.MyNeta')


class MyNetaCollector:

    ELECTIONS = {
        'LS2024': 'https://myneta.info/LokSabha2024/index.php?action=show_winners&sort=default',
        'LS2019': 'https://myneta.info/loksabha2019/index.php?action=show_winners&sort=default',
        'LS2014': 'https://myneta.info/loksabha2014/index.php?action=show_winners&sort=toassets',
    }

    def __init__(self, data_dir='data/raw/myneta'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        })

    def parse_amount(self, text):
        """Convert 'Rs 3,09,16,833~ 3 Crore+' to integer"""
        if not text:
            return 0
        text = text.replace('\xa0', ' ').replace(',', '').strip()
        import re
        match = re.search(r'Rs\s*([\d]+)', text)
        if match:
            return int(match.group(1))
        return 0

    def fetch_election(self, name, url):
        logger.info(f"Fetching {name}: {url}")
        try:
            r = self.session.get(url, timeout=30, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')

            tables = soup.find_all('table')
            candidates = []

            for table in tables:
                rows = table.find_all('tr')
                if len(rows) < 100:
                    continue

                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) < 6:
                        continue
                    text = [c.get_text(strip=True).replace('\xa0', ' ') for c in cols]

                    try:
                        candidate = {
                            'sno': text[0],
                            'name': text[1],
                            'constituency': text[2],
                            'party': text[3],
                            'criminal_cases': int(text[4]) if text[4].isdigit() else 0,
                            'education': text[5] if len(text) > 5 else '',
                            'assets_raw': text[6] if len(text) > 6 else '',
                            'liabilities_raw': text[7] if len(text) > 7 else '',
                            'assets': self.parse_amount(text[6] if len(text) > 6 else ''),
                            'liabilities': self.parse_amount(text[7] if len(text) > 7 else ''),
                            'election': name,
                            'source': 'MyNeta/ADR/ECI-Affidavit',
                        }
                        candidates.append(candidate)
                    except Exception as e:
                        continue

                if candidates:
                    break

            logger.info(f"{name}: {len(candidates)} candidates parsed")
            return candidates

        except Exception as e:
            logger.error(f"Error fetching {name}: {e}")
            return []

    def collect_all(self):
        all_data = {}
        total = 0

        for name, url in self.ELECTIONS.items():
            candidates = self.fetch_election(name, url)
            all_data[name] = candidates
            total += len(candidates)

            out = self.data_dir / f'{name}.json'
            with open(out, 'w', encoding='utf-8') as f:
                json.dump(candidates, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {name}: {len(candidates)} records -> {out}")
            time.sleep(2)

        logger.info(f"COMPLETE. Total: {total} MP records across {len(self.ELECTIONS)} elections")
        return all_data


if __name__ == "__main__":
    print("GovTruth - MyNeta Collector")
    print("Collecting MP asset declarations from ECI affidavits via MyNeta/ADR")
    print("=" * 60)
    collector = MyNetaCollector()
    data = collector.collect_all()

    print("\n=== SUMMARY ===")
    for election, candidates in data.items():
        if candidates:
            # Show top 5 by assets
            sorted_by_assets = sorted(candidates, key=lambda x: x['assets'], reverse=True)
            print(f"\n{election}: {len(candidates)} MPs")
            print(f"Top 5 by declared assets:")
            for mp in sorted_by_assets[:5]:
                print(f"  {mp['name']} ({mp['party']}) - {mp['assets_raw']}")
            
            # Criminal cases
            with_cases = [c for c in candidates if c['criminal_cases'] > 0]
            print(f"MPs with criminal cases: {len(with_cases)}/{len(candidates)}")