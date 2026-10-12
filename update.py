"""Fail-closed REWE updater. Keeps previous data when source fetch/parse fails."""
import json
from datetime import datetime,timezone,date
from pathlib import Path
from scrapers.rewe import fetch
ROOT=Path(__file__).resolve().parent
PATH=ROOT/'deals.json'

def main():
    previous=json.loads(PATH.read_text(encoding='utf-8')) if PATH.exists() else {'updated':None,'deals':[]}
    try:
        deals=fetch()
    except Exception as e:
        print('REWE 获取失败；保留旧数据:',repr(e))
        return 1
    # Keep other-store data, but replace REWE with current source only.
    other=[d for d in previous.get('deals',[]) if d.get('store')!='rewe']
    payload={'updated':datetime.now(timezone.utc).isoformat(timespec='seconds'),'deals':other+deals}
    PATH.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('REWE 已采集',len(deals),'条')
    return 0
if __name__=='__main__':raise SystemExit(main())
