"""Conservative refresh: verify locally supplied deals and remove expired ones.

No unaudited third-party scraper results are represented as verified promotions.
Extend FEED_ADAPTERS after testing each official retailer source.
"""
import json
from datetime import date, timedelta
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'deals.json'
data = json.loads(path.read_text(encoding='utf-8'))
today = date.today()
retained = []
for d in data.get('deals', []):
    if not d.get('verified') or not d.get('url') or not d.get('start') or not d.get('end'):
        continue
    try:
        if date.fromisoformat(d['end']) < today:
            continue
        if date.fromisoformat(d['start']) > today + timedelta(days=120):
            continue
    except ValueError:
        continue
    retained.append(d)
data['deals'] = retained
# Do not change the updated timestamp if no fresh offer was verified.
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
status = {
    'lastChecked': today.isoformat(),
    'automatedProductExtraction': False,
    'message': '已自动检查现有商品有效期；11家商家完整商品采集尚未接通，不能保证所有优惠。',
    'verifiedDeals': len(retained)
}
(ROOT / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
