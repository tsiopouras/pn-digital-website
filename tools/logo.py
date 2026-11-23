import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
# Regenerates the logo files in docs/brand/. Run: python tools/logo.py
from playwright.sync_api import sync_playwright
OUT=str(ROOT/'docs'/'brand')+'/'
import itertools; _n=itertools.count()
def mark(ink, teal):
    i=next(_n)  # all strokes share one top (y=4) and bottom (y=42); the teal diagonal is clipped to that band
    return (f'<svg viewBox="0 0 48 48" fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="butt"><defs><clipPath id="c{i}"><rect x="0" y="4" width="48" height="38"/></clipPath></defs>'
            f'<path d="M6 42V6h12a9 9 0 0 1 0 18H6"/><path d="M28 42V4M44 42V4"/><path d="M27.34 2L44.67 44" stroke="{teal}" clip-path="url(#c{i})"/></svg>')
V={ # name: (background, ink, teal)
 'dark':('#101315','#f3eee3','#3cc4c0'),
 'light':('#fbfbfa','#1b1d20','#0e7c7b'),
 'transparent-white':(None,'#f3eee3','#3cc4c0'),
 'transparent-black':(None,'#1b1d20','#0e7c7b')}
CSS='*{margin:0}body{background:transparent;font-family:Inter,sans-serif}'
def full(bg,ink,teal):
    return f'''<div id="x" style="display:inline-flex;align-items:center;gap:44px;padding:110px 140px;{'background:'+bg if bg else ''}">
<div style="width:220px;height:220px">{mark(ink,teal)}</div><span style="font:700 132px/1 Inter;letter-spacing:-.02em;color:{ink}">P&amp;N Digital</span></div>'''
def icon(bg,ink,teal,pad):
    return f'<div id="x" style="width:1024px;height:1024px;display:grid;place-items:center;{"background:"+bg if bg else ""}"><div style="width:{1024-2*pad}px;height:{1024-2*pad}px">{mark(ink,teal)}</div></div>'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':2400,'height':1400})
    for name,(bg,ink,teal) in V.items():
        for kind,html in (('logo',full(bg,ink,teal)),('icon',icon(bg,ink,teal,190 if bg else 120))):
            pg.set_content(f'<style>{CSS}</style>{html}'); pg.wait_for_timeout(100)
            pg.locator('#x').screenshot(path=f'{OUT}pn-digital-{kind}-{name}.png', omit_background=bg is None)
    b.close()
# vector SVG of the mark too
for name,(bg,ink,teal) in V.items():
    if bg: open(f'{OUT}pn-digital-icon-{name}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -12 72 72"><rect x="-12" y="-12" width="72" height="72" fill="{bg}"/>'+mark(ink,teal).replace('<svg viewBox="0 0 48 48" ','<g ').replace('</svg>','</g>')+'</svg>')
