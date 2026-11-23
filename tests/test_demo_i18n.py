import os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]          # the repository folder
SITE = str(ROOT / 'public')                                   # the website
AI = os.environ.get('PN_AI_ASSISTANT_DIR', str(ROOT.parent / 'pn-digital-ai-assistant'))  # the engine repo, cloned next to this one
OUT = ROOT / 'tests' / 'output'; OUT.mkdir(exist_ok=True)
PY = sys.executable
import subprocess, time, json
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([PY, '-m', 'http.server', '8995', '--directory', SITE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
B = 'http://127.0.0.1:8995'; R = []
def chk(n, ok, d=''):
    R.append((n, bool(ok), str(d)[:200]))
    if not ok: print('FAIL:', n, '|', str(d)[:200])
GREEK = "/[\\u0370-\\u03ff]/.test(document.body.innerText.replace(/ΕΛ/g,''))"
SM = 'html{scroll-behavior:auto!important}'
try:
  with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--no-sandbox'])
    for w in (1440, 390):
      c = br.new_context(viewport={'width': w, 'height': 900}); p = c.new_page(); errs = []
      p.on('pageerror', lambda e: errs.append(str(e))); p.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
      # ---- Olive & Oak
      p.goto(B + '/demos/olive-and-oak/'); p.add_style_tag(content=SM); p.wait_for_timeout(300)
      chk(f'[olive @{w}] English by default: no Greek on the page, lang=en', not p.evaluate(GREEK) and p.evaluate('document.documentElement.lang') == 'en')
      def sw(l):
          if w <= 700 and not p.is_visible('.lg button'): p.click('.mb'); p.wait_for_timeout(450)
          p.click(f'.lg button[data-l={l}]'); p.wait_for_timeout(200)
      sw('el'); chk(f'[olive @{w}] switch to Greek: headline + lang + title', p.inner_text('.hero h1') == 'Μια γεύση από τη Μεσόγειο.' and p.evaluate('document.documentElement.lang') == 'el' and p.title().startswith('Αρχική |'), p.title())
      chk(f'[olive @{w}] switcher shows ΕΛ selected', p.get_attribute('.lg button[data-l=el]', 'aria-pressed') == 'true')
      p.evaluate("location.hash='#menu'"); p.wait_for_timeout(250)
      chk(f'[olive @{w}] Greek menu: categories + count line', 'Θαλασσινά' in p.inner_text('#cats') and p.inner_text('#count') == '18 πιάτα εμφανίζονται', p.inner_text('#count'))
      p.click('#diet [data-d=vg]'); chk(f'[olive @{w}] dietary filter still works in Greek (8 vegan)', p.locator('#g-menu .dish').count() == 8 and p.inner_text('#count') == '8 πιάτα εμφανίζονται')
      p.click('#diet [data-d=vg]'); p.locator('#g-menu .dish').first.click(); chk(f'[olive @{w}] dish pop-up in Greek', 'Χαλλούμι' in p.inner_text('#dc') and 'ενδεικτική τιμή' in p.inner_text('#dc')); p.click('#dx')
      p.evaluate("location.hash='#reserve'"); p.wait_for_timeout(250)
      p.click('#wiz [data-a=inc]'); p.click('#wiz [data-a=next]')
      chk(f'[olive @{w}] booking step text in Greek', 'Βήμα 2 από 7: Ημερομηνία' in p.inner_text('#wiz'), p.inner_text('#wiz')[:60])
      d0 = p.locator('#wiz .opt[data-a=date]:not([disabled])').first; chk(f'[olive @{w}] date buttons in Greek (e.g. "Τρί 24 Νοε")', any(x in d0.inner_text() for x in ('Δευ','Τρί','Τετ','Πέμ','Παρ','Σάβ','Κυρ')), d0.inner_text())
      d0.click(); p.click('#wiz [data-a=next]'); p.locator('#wiz .opt[data-a=time]:not([disabled])').first.click(); p.click('#wiz [data-a=next]')
      p.click('#wiz [data-a=seat][data-v=Terrace]'); chk(f'[olive @{w}] seating labels Greek and selection works', 'Βεράντα' in p.inner_text('#wiz') and p.get_attribute('#wiz [data-a=seat][data-v=Terrace]', 'aria-pressed') == 'true')
      p.click('#wiz [data-a=next]'); p.fill('#fn', 'Maria'); p.fill('#fe', 'm@example.invalid'); p.click('#wiz [data-a=next]')
      p.select_option('#fo', 'Birthday'); chk(f'[olive @{w}] occasion menu shows Greek labels', 'Γενέθλια' in p.inner_text('#fo'))
      p.fill('#fx', 'Window table'); sw('en')
      chk(f'[olive @{w}] switch back to English mid-booking: English, choices kept', 'Step 6 of 7: Special requests' in p.inner_text('#wiz') and p.input_value('#fx') == 'Window table' and p.input_value('#fo') == 'Birthday' and not p.evaluate(GREEK), p.inner_text('#wiz')[:60])
      sw('el'); p.click('#wiz [data-a=next]'); rv = p.inner_text('#wiz')
      chk(f'[olive @{w}] review in Greek with typed text untouched', all(x in rv for x in ('Βήμα 7 από 7', 'Βεράντα', 'Γενέθλια', 'Maria', 'Window table', 'Νοεμβρίου')) or all(x in rv for x in ('Βήμα 7 από 7', 'Βεράντα', 'Γενέθλια', 'Maria', 'Window table', 'Δεκεμβρίου')), rv[:140].replace('\n', ' '))
      p.click('#wiz [data-a=next]'); cf = p.inner_text('#wiz'); chk(f'[olive @{w}] Greek confirmation is honest (demo only, nothing sent)', 'Μόνο επίδειξη' in cf and 'δεν στάλθηκε τίποτα' in cf)
      chk(f'[olive @{w}] no JS errors', not errs, errs[:2]); errs.clear()
      # ---- THE CUT
      p.goto(B + '/demos/the-cut/?lang=el'); p.add_style_tag(content=SM); p.wait_for_timeout(300)
      chk(f'[cut @{w}] ?lang=el opens in Greek', p.evaluate('document.documentElement.lang') == 'el' and 'Κουρείο επίδειξης' in p.text_content('.hero'))
      p.evaluate("location.hash='#book'"); p.wait_for_timeout(250); p.click('#wiz [data-a=svc][data-v=combo]')
      chk(f'[cut @{w}] live total in Greek units', p.inner_text('#sumbox output').strip() == '€24 · 50 λεπτά', p.inner_text('#sumbox output'))
      p.click('#wiz [data-a=next]'); p.click('#wiz [data-a=add][data-v=towel]')
      chk(f'[cut @{w}] add-on updates total (€28 · 55 λεπτά) and summary line', p.inner_text('#sumbox output').strip() == '€28 · 55 λεπτά' and '+ Τελείωμα με ζεστή πετσέτα' in p.inner_text('#sumbox'))
      p.click('#wiz [data-a=next]'); p.click('#wiz [data-a=barber][data-v=nikos]'); p.click('#wiz [data-a=next]')
      chk(f'[cut @{w}] barber day off shown in Greek', 'Ρεπό: Νίκος' in p.inner_text('#wiz') and 'Κλειστά' in p.inner_text('#wiz'))
      p.locator('#wiz .opt[data-a=date]:not([disabled])').first.click(); p.click('#wiz [data-a=next]')
      chk(f'[cut @{w}] time slots in Greek ("λήξη")', 'λήξη' in p.inner_text('#wiz') and 'Δεν εμφανίζονται ώρες' in p.inner_text('#wiz'))
      p.locator('#wiz .opt[data-a=time]:not([disabled])').first.click(); chk(f'[cut @{w}] summary shows Greek date + time range', 'Νοεμβρίου' in p.inner_text('#sumbox') or 'Δεκεμβρίου' in p.inner_text('#sumbox'), p.inner_text('#sumbox')[:100])
      p.evaluate("location.hash='#services'"); p.wait_for_timeout(250); p.locator('#svc [data-bs=fade]').click(); p.wait_for_timeout(300)
      chk(f'[cut @{w}] "Book this" in Greek keeps working (service switched, earlier add-on kept: €22 · 45 λεπτά)', 'Σκιν φέιντ' in p.inner_text('#sumbox') and p.inner_text('#sumbox output').strip() == '€22 · 45 λεπτά', p.inner_text('#sumbox output'))
      p.goto(B + '/demos/the-cut/'); p.wait_for_timeout(250); chk(f'[cut @{w}] plain URL stays English (no Greek)', not p.evaluate(GREEK))
      chk(f'[cut @{w}] no JS errors', not errs, errs[:2])
      c.close()
    # ---- previews follow the portfolio language
    for lp, L in (('/work/', 'en'), ('/el/work/', 'el')):
      c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page()
      for slug, h1 in (('olive-and-oak', {'en': 'A Taste of the Mediterranean.', 'el': 'Μια γεύση από τη Μεσόγειο.'}), ('the-cut', None)):
        p.goto(B + lp); p.click(f'[data-preview="{slug}"]'); p.wait_for_function("document.querySelector('#pv-msg').hidden===true"); p.wait_for_timeout(300)
        fr = p.query_selector('#pv iframe').content_frame()
        chk(f'[preview {L}] {slug} opens in {L}', fr.evaluate('document.documentElement.lang') == L, fr.evaluate('document.documentElement.lang'))
        p.click('#pv-close'); p.wait_for_timeout(300)
      c.close()
    br.close()
finally: srv.terminate()
f = [r for r in R if not r[1]]; print(f'DEMO-I18N TOTAL {len(R)} | PASSED {len(R)-len(f)} | FAILED {len(f)}')
