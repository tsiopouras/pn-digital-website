import os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]          # the repository folder
SITE = str(ROOT / 'public')                                   # the website
AI = os.environ.get('PN_AI_ASSISTANT_DIR', str(ROOT.parent / 'pn-digital-ai-assistant'))  # the engine repo, cloned next to this one
OUT = ROOT / 'tests' / 'output'; OUT.mkdir(exist_ok=True)
PY = sys.executable
import json
from playwright.sync_api import sync_playwright
U = (OUT / 'pn-digital-preview.html').as_uri(); R = []
def chk(n, ok, d=''):
    R.append((n, bool(ok), str(d)[:200]))
    if not ok: print('FAIL:', n, '|', str(d)[:200])
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    for w in (1440, 390):
        c = br.new_context(viewport={'width': w, 'height': 900}); p = c.new_page(); errs = []
        p.on('pageerror', lambda e: errs.append(str(e))); p.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        for start, L, slug, expect in (('#work', 'en', 'olive-and-oak', 'A Taste of the Mediterranean.'), ('#el-work', 'el', 'the-cut', 'Κουρείο επίδειξης'), ('#work', 'en', 'nexora-business-solutions', 'Clear advice for growing businesses.')):
            p.goto(U + start); p.wait_for_timeout(400)
            p.locator(f'.route:not([hidden]) [data-preview="{slug}"]').first.click(); p.wait_for_function("document.querySelector('#pv-msg').hidden===true", timeout=9000)
            ol = p.locator('#pv-open'); chk(f'[{w} {L}] {slug}: "Open full website" visible in preview', ol.is_visible(), ol.get_attribute('href'))
            n0 = len(c.pages); ol.click(); p.wait_for_timeout(900)
            chk(f'[{w} {L}] {slug}: opens full-screen view in the same page (no blank tab)', len(c.pages) == n0 and p.is_visible('#full') and not p.evaluate("document.getElementById('pv').open"), (len(c.pages), p.evaluate('location.hash')))
            fr = p.frame_locator('#full-frame'); txt = fr.locator('body').text_content()
            chk(f'[{w} {L}] {slug}: the real demo is shown full-screen and in {L}', expect.lower() in txt.lower(), txt[:70].replace('\n', ' '))
            fb = p.locator('#full-frame').bounding_box(); chk(f'[{w} {L}] {slug}: full view fills the screen', fb['width'] >= w - 2 and fb['height'] > 700, fb)
            tgt = {'olive-and-oak': 'menu', 'the-cut': 'services', 'nexora-business-solutions': 'services'}[slug]
            if w <= 820: fr.locator('.mb').click(); p.wait_for_timeout(500)
            fr.locator(f'nav a[href="#{tgt}"]').first.click(); p.wait_for_timeout(500)
            chk(f'[{w} {L}] {slug}: demo inside the full view is interactive (its own navigation works)', fr.locator(f'[data-p={tgt}]').is_visible())
            back = p.locator('#full-back'); chk(f'[{w} {L}] back button labelled in the right language', ('Επιστροφή' in back.inner_text()) == (L == 'el'), back.inner_text())
            back.click(); p.wait_for_timeout(400)
            chk(f'[{w} {L}] {slug}: back returns to the project page', not p.is_visible('#full') and p.evaluate('location.hash') == ('#el-' if L == 'el' else '#') + 'project-' + slug, p.evaluate('location.hash'))
            a = p.locator('.route:not([hidden]) a[data-open]'); chk(f'[{w} {L}] {slug}: project page "Open full website" link present', a.is_visible() and a.get_attribute('href').startswith('#full-'), a.get_attribute('href'))
            a.click(); p.wait_for_timeout(700); chk(f'[{w} {L}] {slug}: project page link opens the full view too', p.is_visible('#full'))
            p.go_back(); p.wait_for_timeout(400); chk(f'[{w} {L}] browser Back closes the full view', not p.is_visible('#full'))
        p.goto(U + '#work'); p.wait_for_timeout(300)
        p.locator('.route:not([hidden]) [data-preview="olive-and-oak"]').first.click(); p.wait_for_function("document.querySelector('#pv-msg').hidden===true")
        if w >= 720:
            p.click('#pv [data-mode=phone]'); p.wait_for_timeout(700)
            chk(f'[{w}] phone/desktop switching still works in the test copy', p.frame_locator('#pv iframe').locator('html').evaluate('e=>innerWidth') == 390)
        p.click('#pv-close'); p.wait_for_timeout(400)
        p.goto(U + '#home'); p.wait_for_timeout(300)
        if w == 390:
            p.locator('.route:not([hidden]) .menu-btn').click(); p.wait_for_timeout(600)
            b = p.locator('.route:not([hidden]) header nav .cta .btn'); col = b.evaluate('e=>getComputedStyle(e).color')
            chk('[390] test copy: mobile menu "Get a quote" button readable (dark text)', col == 'rgb(16, 19, 21)', col)
        chk(f'[{w}] no JS errors in the test copy', not errs, errs[:3])
        c.close()
    br.close()
f = [r for r in R if not r[1]]; print(f'HOSTED TOTAL {len(R)} | PASSED {len(R)-len(f)} | FAILED {len(f)}')
json.dump(R, open(str(OUT / 'results-hosted.json'), 'w'))

# ---- assistant inside the single-file test copy
R2 = []
def chk2(n, ok, d=''):
    R2.append((n, bool(ok), str(d)[:200]))
    if not ok: print('FAIL:', n, '|', str(d)[:200])
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox']); c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page(); errs = []
    p.on('pageerror', lambda e: errs.append(str(e)))
    p.goto(U + '#el-home'); p.wait_for_timeout(500)
    chk2('test copy: agency assistant present once', p.locator('#pn-ai-host').count() == 1)
    p.locator('#pn-ai-host .launcher').click(); p.wait_for_timeout(300)
    chk2('test copy: assistant in Greek on Greek pages', p.evaluate("document.getElementById('pn-ai-host').shadowRoot.querySelector('.tag.ai').textContent") == 'Βοηθός AI')
    p.locator('#pn-ai-host textarea').fill('Πώς επικοινωνώ μαζί σας;'); p.locator('#pn-ai-host textarea').press('Enter'); p.wait_for_timeout(900)
    href = p.evaluate("[...document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('a.act')].pop().getAttribute('href')")
    chk2('test copy: assistant links become in-page routes (#el-contact)', href == '#el-contact', href)
    p.evaluate("[...document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('a.act')].pop().click()"); p.wait_for_timeout(400)
    chk2('test copy: the link opens the Greek contact page', p.evaluate('location.hash') == '#el-contact' and p.is_visible('.route[data-route=el-contact]'))
    p.goto(U + '#project-the-cut'); p.wait_for_timeout(400); p.locator('.route:not([hidden]) a[data-open]').click(); p.wait_for_timeout(900)
    chk2('test copy: agency assistant button hidden while a demo is full-screen', not p.locator('#pn-ai-host .launcher').is_visible())
    fr = p.frame_locator('#full-frame'); fr.locator('#pn-ai-host .launcher').click(); p.wait_for_timeout(300)
    fr.locator('#pn-ai-host textarea').fill('How much is a skin fade?'); fr.locator('#pn-ai-host textarea').press('Enter'); p.wait_for_timeout(900)
    ans = p.frame(url=lambda u: 'srcdoc' in u).evaluate("[...document.getElementById('pn-ai-host').shadowRoot.querySelectorAll('.msg.bot')].pop().textContent")
    chk2('test copy: THE CUT assistant answers inside the full-screen demo', '€18' in ans, ans[:100])
    p.locator('#full-back').click(); p.wait_for_timeout(400); chk2('test copy: agency assistant button comes back after leaving the demo', p.locator('#pn-ai-host .launcher').is_visible())
    chk2('test copy: no JS errors with the assistant', not errs, errs[:2]); br.close()
f2 = [r for r in R2 if not r[1]]; print(f'HOSTED-ASSISTANT TOTAL {len(R2)} | PASSED {len(R2)-len(f2)} | FAILED {len(f2)}')
