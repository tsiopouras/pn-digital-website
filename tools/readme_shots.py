# Refreshes the screenshots used in README.md (docs/screenshots/). Run: python tools/readme_shots.py
import pathlib, subprocess, sys, time
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]; OUT = ROOT / 'docs' / 'screenshots'; OUT.mkdir(parents=True, exist_ok=True)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '5615', '--directory', str(ROOT / 'public')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
O = 'http://127.0.0.1:5615'
CALM = 'html{scroll-behavior:auto}.reveal,.rv{opacity:1!important;transform:none!important}header.top{position:static!important}'
def shot(pg, name, sel=None, full=False):
    p = str(OUT / f'{name}.jpg')
    (pg.locator(sel).first.screenshot(path=p, type='jpeg', quality=80) if sel else pg.screenshot(path=p, type='jpeg', quality=80, full_page=full))
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    pg.goto(O + '/'); pg.wait_for_timeout(2200); shot(pg, 'home-desktop')
    pg.add_style_tag(content=CALM)
    pg.goto(O + '/services/'); pg.add_style_tag(content=CALM); pg.wait_for_timeout(400)
    pg.check('#quote input[name=size][value="2"]', force=True); pg.click('#quote .st-b[data-step="1"]'); pg.check('#quote input[value=gallery]'); pg.check('#quote input[name=maint]'); pg.wait_for_timeout(800)
    shot(pg, 'quote-calculator', '#quote')
    pg.goto(O + '/contact/'); pg.add_style_tag(content=CALM); pg.wait_for_timeout(400); shot(pg, 'contact', 'main')
    pg.goto(O + '/projects/the-cut/'); pg.add_style_tag(content=CALM); pg.locator('.cmp-box').scroll_into_view_if_needed(); pg.wait_for_timeout(3400); shot(pg, 'how-we-built-it', '.build')
    pg.goto(O + '/projects/olive-and-oak/'); pg.add_style_tag(content=CALM); pg.wait_for_timeout(300); pg.click('[data-preview]'); pg.wait_for_timeout(2500); shot(pg, 'live-preview')
    pg.goto(O + '/'); pg.wait_for_timeout(600); pg.locator('#pn-ai-host .launcher').click(); pg.wait_for_timeout(500)
    h = pg.locator('#pn-ai-host'); h.locator('textarea').fill('How much does a website cost?'); h.locator('textarea').press('Enter'); pg.wait_for_timeout(1200); shot(pg, 'ai-assistant')
    for d in ('olive-and-oak', 'the-cut', 'nexora', 'halcyon-bay', 'myrtle'):
        pg.goto(O + f'/demos/{d}/'); pg.wait_for_timeout(1500); pg.add_style_tag(content='#pn-ai-host{display:none}'); shot(pg, f'demo-{d}')
    ph = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    ph.goto(O + '/el/'); ph.wait_for_timeout(2200); shot(ph, 'home-phone-greek')
    b.close()
srv.terminate()
