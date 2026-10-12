from scrapers.rewe import parse
HTML='''<html><body><p>12.10. bis 18.10.2026</p><h2>Top-Angebote</h2><div><h3>Milka Schokolade</h3><p>je 90-g-Tafel</p><span>Knaller</span><span>0,99 €</span></div><div><h3>Alpro Haferdrink</h3><p>1-l-Pckg.</p><span>Aktion</span><span>1,49 €</span></div></body></html>'''
def test_parse():
    a=parse(HTML)
    assert len(a)==2
    assert a[0]['price']==.99
    assert a[1]['category']=='drinks'
    assert a[0]['start']=='2026-10-12'
