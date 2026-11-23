import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
# Regenerates the social share images (public/assets/og/og-en.jpg and og-el.jpg). Run: python tools/og.py
from playwright.sync_api import sync_playwright
from PIL import Image
import os
MARK='<svg viewBox="0 0 48 48" fill="none" stroke="#f3eee3" stroke-width="4"><defs><clipPath id="c"><rect x="0" y="4" width="48" height="38"/></clipPath></defs><path d="M6 42V6h12a9 9 0 0 1 0 18H6"/><path d="M28 42V4M44 42V4"/><path d="M27.34 2L44.67 44" stroke="#3cc4c0" clip-path="url(#c)"/></svg>'
TX={'en':('Websites for businesses in Cyprus.','Fast, mobile-first, and in any language your customers speak.',['Ελληνικά','English','Русский','עברית','Deutsch']),
    'el':('Ιστοσελίδες για επιχειρήσεις στην Κύπρο.','Γρήγορες, φτιαγμένες πρώτα για κινητό, σε όποια γλώσσα μιλούν οι πελάτες σας.',['Ελληνικά','English','Русский','עברית','Deutsch'])}
def page(L):
    h,sub,langs=TX[L]
    chips=''.join(f'<span>{x}</span>' for x in langs)
    return f'''<html><head><style>*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#101315;font-family:Inter,sans-serif;color:#f3eee3;position:relative;overflow:hidden}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#1c2226 1px,transparent 1px),linear-gradient(90deg,#1c2226 1px,transparent 1px);background-size:60px 60px;opacity:.55;mask-image:radial-gradient(ellipse at 75% 40%,#000 0,transparent 70%)}}
.glow{{position:absolute;width:760px;height:760px;right:-220px;top:-260px;background:radial-gradient(circle,rgba(60,196,192,.28),transparent 62%)}}
.bar{{position:absolute;left:0;top:0;bottom:0;width:10px;background:#3cc4c0}}
.wrap{{position:absolute;left:96px;top:92px;right:96px}}
.logo{{display:flex;align-items:center;gap:30px}}
.logo svg{{width:118px;height:118px}}
.logo b{{font:800 88px/1 Inter;letter-spacing:-.03em}}
h1{{margin-top:64px;font:700 50px/1.12 'Bitstream Charter',Charter,Georgia,serif;max-width:900px}}
p{{margin-top:18px;font:500 26px/1.4 Inter;color:#a9afb3;max-width:900px}}
.chips{{position:absolute;left:96px;bottom:54px;display:flex;gap:12px}}
.chips span{{padding:9px 18px;border:1px solid #2f4a4a;color:#7fd9d6;font:600 20px Inter;border-radius:999px;background:rgba(60,196,192,.07)}}
</style></head><body><div class="grid"></div><div class="glow"></div><div class="bar"></div>
<div class="wrap"><div class="logo">{MARK}<b>P&amp;N Digital</b></div><h1>{h}</h1><p>{sub}</p></div><div class="chips">{chips}</div></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']); pg=b.new_page(viewport={'width':1200,'height':630})
    for L in ('en','el'):
        pg.set_content(page(L)); pg.wait_for_timeout(200)
        pg.screenshot(path=str(ROOT/'public'/'assets'/'og'/f'og-{L}.png'))
    b.close()
for L in ('en','el'):
    p=ROOT/'public'/'assets'/'og'/f'og-{L}.png'; Image.open(p).convert('RGB').save(p.with_suffix('.jpg'),quality=88,optimize=True,progressive=True); os.remove(p)
