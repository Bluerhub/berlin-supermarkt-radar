"""REWE Berlin Pankstr. 39 public offer-page adapter. No private API or login."""
import re
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

URL = 'https://www.rewe.de/angebote/berlin/410561/rewe-pankstr-39/'
PRICE = re.compile(r'(?<!\d)(\d{1,3}[.,]\d{2})\s*€')
DATE_RANGE = re.compile(r'(\d{1,2})\.(\d{1,2})\.\s*(?:bis|–|-)\s*(\d{1,2})\.(\d{1,2})\.(\d{4})')
TRANSLATIONS = {'Schokolade':'巧克力','Milch':'牛奶','Haferdrink':'燕麦饮','Soyadrink':'豆奶','Weichkäse':'软奶酪','Pasta Sauce':'意面酱','Müsli':'麦片','Pizza':'披萨','Saft':'果汁','Kaffee':'咖啡','Tee':'茶','Wasser':'水','Waschmittel':'洗衣液','Joghurt':'酸奶','Butter':'黄油','Salami':'萨拉米香肠'}

def category(name):
    n=name.lower()
    if any(x in n for x in ('wasser','saft','cola','limonade','bier','wein','kaffee','tee','drink','limo')): return 'drinks'
    if any(x in n for x in ('waschmittel','reiniger','shampoo','windeln','zahnpasta','papier','seife')): return 'household'
    if any(x in n for x in ('kleidung','spielzeug','batterie','elektronik')): return 'other'
    return 'food'

def translate(name):
    for de,zh in sorted(TRANSLATIONS.items(),key=lambda x:-len(x[0])):
        if de.lower() in name.lower(): return name + '（'+zh+'）'
    return name + '（中文待补充）'

def dates_from_page(text):
    m=DATE_RANGE.search(text)
    if not m: return None
    d1,m1,d2,m2,y=map(int,m.groups())
    try: return date(y,m1,d1).isoformat(),date(y,m2,d2).isoformat()
    except ValueError: return None

def parse(html, source=URL):
    soup=BeautifulSoup(html,'html.parser')
    for tag in soup(['script','style','noscript']):tag.decompose()
    text=soup.get_text(' ',strip=True)
    dates=dates_from_page(text[:2500])
    if not dates: raise ValueError('未找到明确的促销日期，拒绝发布')
    result=[];seen=set()
    for h in soup.find_all(['h3']):
        name=h.get_text(' ',strip=True)
        if not name or len(name)>150 or name in seen:continue
        # Product price generally follows the h3, separated by a description and 'Aktion'/'Knaller'.
        chunks=[]
        for el in h.next_elements:
            if getattr(el,'name',None) in ('h2','h3','h4'):break
            if isinstance(el,str):
                t=el.strip()
                if t:chunks.append(t)
            if len(' '.join(chunks))>600:break
        detail=' '.join(chunks)
        promo=re.search(r'\b(?:Knaller|Aktion)\b\s*(\d{1,3}[.,]\d{2})\s*€',detail,re.I)
        if not promo:continue
        price=float(promo.group(1).replace(',','.'))
        if price<=0 or price>1000:continue
        unit=detail.split('Knaller')[0].split('Aktion')[0].strip()[:180]
        result.append(dict(store='rewe',category=category(name),zh=translate(name),de=name,price=price,oldPrice=None,unit=unit,start=dates[0],end=dates[1],url=source,verified=True,notes='REWE Berlin Pankstr. 39；原价未核实；中文为辅助翻译'))
        seen.add(name)
    if not result:raise ValueError('未解析到明确商品与促销价，拒绝发布')
    return result

def fetch():
    r=requests.get(URL,headers={'User-Agent':'Mozilla/5.0 (compatible; BerlinDealsPersonal/1.0)'},timeout=25)
    r.raise_for_status()
    return parse(r.text)
