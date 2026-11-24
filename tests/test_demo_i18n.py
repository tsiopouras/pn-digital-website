import os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]          # the repository folder
SITE = str(ROOT / 'public')                                   # the website
AI = os.environ.get('PN_AI_ASSISTANT_DIR', str(ROOT.parent / 'pn-digital-ai-assistant'))  # the engine repo, cloned next to this one
OUT = ROOT / 'tests' / 'output'; OUT.mkdir(exist_ok=True)
PY = sys.executable
import subprocess, time, json, re
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([PY, '-m', 'http.server', '8995', '--directory', SITE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
B = 'http://127.0.0.1:8995'; R = []
def chk(n, ok, d=''):
    R.append((n, bool(ok), str(d)[:200]))
    if not ok: print('FAIL:', n, '|', str(d)[:200])
GREEK = "/[\\u0370-\\u03ff]/.test(document.body.innerText.replace(/ΕΛ/g,''))"
SM = 'html{scroll-behavior:auto!important}'
# Every text node and label the demo shows (hidden pages too), minus brand names and what the visitor typed.
LEAKS = """(allow) => { const out = new Set(), rx = /[A-Za-z][A-Za-z&’'-]{2,}/g, w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  while ((n = w.nextNode())) { const el = n.parentElement; if (!el || el.closest('script,style,[data-no-i18n],#pn-ai-host,.lg')) continue;
    (n.nodeValue.match(rx) || []).forEach(x => { if (!allow.includes(x)) out.add(x + ' «' + n.nodeValue.trim().slice(0, 50) + '»') }) }
  document.querySelectorAll('[aria-label],[title],[alt],[placeholder]').forEach(e => { if (e.closest('[data-no-i18n],#pn-ai-host,.lg')) return; ['aria-label', 'title', 'alt', 'placeholder'].forEach(a => { const v = e.getAttribute(a); if (v) (v.match(rx) || []).forEach(x => { if (!allow.includes(x)) out.add('[' + a + '] ' + x) }) }) });
  return [...out] }"""
ALLOW = ['Halcyon', 'Bay', 'Myrtle', 'Beauty', 'Studio', 'P&N', 'Digital', 'Email', 'email', 'Wi-Fi', 'Fi']
def sweep(p, bag):
    for x in p.evaluate(LEAKS, ALLOW): bag.add(x)
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
    for w in (1440, 390):
      c = br.new_context(viewport={'width': w, 'height': 900}); p = c.new_page(); errs = []
      p.on('pageerror', lambda e: errs.append(str(e))); p.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
      def sw(l):
          if w <= 800 and not p.is_visible('.lg button'): p.click('.mb'); p.wait_for_timeout(450)
          p.click(f'.lg button[data-l={l}]'); p.wait_for_timeout(200)
      nx = lambda: p.click('#wiz [data-a=next]')
      # ---- Halcyon Bay (hotel)
      p.goto(B + '/demos/halcyon-bay/'); p.add_style_tag(content=SM); p.wait_for_timeout(300)
      chk(f'[hotel @{w}] English by default: no Greek, lang=en', not p.evaluate(GREEK) and p.evaluate('document.documentElement.lang') == 'en')
      sw('el'); leak = set()
      chk(f'[hotel @{w}] switch to Greek: headline, lang and title', p.inner_text('.hero h1').replace('\n', ' ') == 'Αργές μέρες δίπλα στη θάλασσα.' and p.evaluate('document.documentElement.lang') == 'el' and p.title().startswith('Αρχική |'), (p.inner_text('.hero h1'), p.title()))
      p.evaluate("document.querySelectorAll('#faq button.q').forEach(b=>b.click())"); sweep(p, leak)
      p.locator('#gal [data-g]').first.click(); p.wait_for_timeout(150); sweep(p, leak)
      chk(f'[hotel @{w}] gallery pop-up in Greek', 'Η πισίνα' in p.inner_text('#dc') and 'Κλείσιμο' in p.inner_text('#dc')); p.keyboard.press('Escape')
      p.evaluate("location.hash='#rooms'"); p.wait_for_timeout(250)
      chk(f'[hotel @{w}] rooms page: Greek count line', p.inner_text('#count') == '6 δωμάτια εμφανίζονται', p.inner_text('#count'))
      p.click('#feats [data-f=fam]'); chk(f'[hotel @{w}] "3 or more" filter works in Greek (2 rooms)', p.locator('#g-rooms .room').count() == 2 and p.inner_text('#count') == '2 δωμάτια εμφανίζονται'); sweep(p, leak)
      p.click('#feats [data-f=fam]'); p.click('#views [data-v=sea]'); chk(f'[hotel @{w}] sea-view filter (3 rooms)', p.locator('#g-rooms .room').count() == 3); p.click('#views [data-v=all]')
      p.locator('#g-rooms [data-rd]').first.click(); p.wait_for_timeout(150); sweep(p, leak)
      chk(f'[hotel @{w}] room pop-up in Greek with price per night', 'τη νύχτα (ενδεικτικά)' in p.inner_text('#dc') and 'Έως 2 άτομα' in p.inner_text('#dc'), p.inner_text('#dc')[:120]); p.keyboard.press('Escape')
      p.evaluate("location.hash='#experiences'"); p.wait_for_timeout(200); sweep(p, leak)
      p.evaluate("location.hash='#book'"); p.wait_for_timeout(250); nx(); sweep(p, leak)
      chk(f'[hotel @{w}] calendar: Greek month and weekdays, error in Greek', bool(re.search('(Ιανουάριος|Φεβρουάριος|Μάρτιος|Απρίλιος|Μάιος|Ιούνιος|Ιούλιος|Αύγουστος|Σεπτέμβριος|Οκτώβριος|Νοέμβριος|Δεκέμβριος) 20', p.inner_text('.calh'))) and 'Δευ' in p.inner_text('.calg') and 'Παρακαλούμε επιλέξτε' in p.inner_text('#wiz'), p.inner_text('.calh'))
      p.click('#wiz [data-a=nm]'); d = p.locator('#wiz .day:not([disabled])'); d.nth(2).click(); p.locator('#wiz .day:not([disabled])').nth(5).click(); sweep(p, leak)
      chk(f'[hotel @{w}] three nights chosen, shown in Greek', '3 νύχτες' in p.inner_text('#sumbox').replace('\n', ' ') and 'Νύχτες' in p.inner_text('#wiz'), p.inner_text('#sumbox')[:120])
      nx(); p.click('#wiz [data-a="ch+"]'); sweep(p, leak); chk(f'[hotel @{w}] guests in Greek (2 ενήλικες, 1 παιδί)', '2 ενήλικες, 1 παιδί' in p.inner_text('#sumbox').replace('\n', ' '), p.inner_text('#sumbox')[:160])
      nx(); sweep(p, leak); chk(f'[hotel @{w}] rooms too small for 3 are disabled, in Greek', p.locator('#wiz [data-a=room][data-v=sea][disabled]').count() == 1 and 'Πολύ μικρό για την ομάδα σας' in p.inner_text('#wiz'))
      p.locator('#wiz [data-a=room]:not([disabled])').first.click(); t1 = p.inner_text('#sumbox output'); nx(); p.click('#wiz [data-a=rate][data-v=hb]'); sweep(p, leak)
      chk(f'[hotel @{w}] half board raises the total', int(p.inner_text('#sumbox output').strip('€')) > int(t1.strip('€')), (t1, p.inner_text('#sumbox output')))
      nx(); p.click('#wiz [data-a=ex][data-v=boat]'); sweep(p, leak); chk(f'[hotel @{w}] extra shown in Greek in the summary', '+ Βαρκάδα στο ηλιοβασίλεμα' in p.inner_text('#sumbox'))
      nx(); p.fill('#fn', 'Maria'); p.fill('#fe', 'm@example.invalid'); p.select_option('#fa', 'eve'); p.fill('#fx', 'Sea view please'); sweep(p, leak)
      chk(f'[hotel @{w}] arrival-time menu shows Greek labels', 'Δεν ξέρω ακόμη' in p.inner_text('#fa'))
      sw('en'); chk(f'[hotel @{w}] switch to English mid-booking: English, typing kept', 'Step 6 of 7: Your details' in p.inner_text('#wiz') and p.input_value('#fx') == 'Sea view please' and p.input_value('#fa') == 'eve' and not p.evaluate(GREEK), p.inner_text('#wiz')[:60])
      sw('el'); nx(); rv = p.inner_text('#wiz'); sweep(p, leak)
      chk(f'[hotel @{w}] review in Greek, typed name untouched', all(x in rv for x in ('Βήμα 7 από 7', 'Ημιδιατροφή', 'Maria', 'νύχτες', 'Βαρκάδα στο ηλιοβασίλεμα')), rv[:200].replace('\n', ' '))
      nx(); cf = p.inner_text('#wiz'); sweep(p, leak); chk(f'[hotel @{w}] Greek confirmation is honest (demo only, nothing sent)', 'Μόνο επίδειξη' in cf and 'δεν στάλθηκε τίποτα' in cf)
      chk(f'[hotel @{w}] Greek sweep: no English left on any page or booking step', not leak, sorted(leak)[:6])
      chk(f'[hotel @{w}] no JS errors', not errs, errs[:2]); errs.clear()
      # ---- Myrtle Beauty Studio (salon)
      p.goto(B + '/demos/myrtle/?lang=el'); p.add_style_tag(content=SM); p.wait_for_timeout(300); leak = set()
      chk(f'[salon @{w}] ?lang=el opens in Greek', p.evaluate('document.documentElement.lang') == 'el' and 'Σαλόνι ομορφιάς επίδειξης' in p.text_content('.hero'))
      p.evaluate("document.querySelectorAll('#faq button.q').forEach(b=>b.click())"); sweep(p, leak)
      p.click('[data-q=f][data-v=hair]'); p.click('[data-q=t][data-v="2"]'); p.click('[data-q=x][data-v=y]'); sweep(p, leak)
      chk(f'[salon @{w}] treatment finder suggests in Greek with the right total', all(x in p.inner_text('#qres') for x in ('Μπαλαγιάζ', '+ Μάσκα μαλλιών', '€105 · 165 λεπτά')), p.inner_text('#qres')[:120])
      p.locator('[data-cat=brows]').click(); p.wait_for_timeout(250); sweep(p, leak)
      chk(f'[salon @{w}] category card opens filtered treatments (2), count in Greek', p.locator('#g-tr .card').count() == 2 and p.inner_text('#count') == '2 θεραπείες εμφανίζονται', p.inner_text('#count'))
      p.click('#cf [data-c=all]'); p.click('#tf [data-f=nopatch]'); chk(f'[salon @{w}] "no patch test" filter (10 treatments)', p.locator('#g-tr .card').count() == 10); p.click('#tf [data-f=nopatch]')
      p.evaluate("location.hash='#team'"); p.wait_for_timeout(200); sweep(p, leak); chk(f'[salon @{w}] team days off in Greek', 'Ρεπό: Τετάρτη' in p.inner_text('#tp'))
      p.click('[data-bb=sofia]'); p.wait_for_timeout(250); nx(); sweep(p, leak); chk(f'[salon @{w}] error in Greek when no treatment chosen', 'Παρακαλούμε επιλέξτε θεραπεία.' in p.inner_text('#wiz'))
      p.click('#wiz [data-a=svc][data-v=colour]'); sweep(p, leak); chk(f'[salon @{w}] patch-test reminder in Greek', 'τεστ ευαισθησίας' in p.inner_text('#wiz') and 'Χρειάζεται τεστ ευαισθησίας' in p.text_content('#sumbox'))
      nx(); p.click('#wiz [data-a=add][data-v=mask]'); chk(f'[salon @{w}] add-on updates total (€65 · 105 λεπτά)', p.inner_text('#sumbox output').strip() == '€65 · 105 λεπτά', p.inner_text('#sumbox output'))
      nx(); chk(f'[salon @{w}] specialists who do not offer colour are disabled', p.locator('#wiz [data-a=who][data-v=maria][disabled]').count() == 1 and p.get_attribute('#wiz [data-a=who][data-v=sofia]', 'aria-pressed') == 'true'); sweep(p, leak)
      nx(); sweep(p, leak); chk(f'[salon @{w}] day off and closed days in Greek', 'Ρεπό: Σοφία' in p.inner_text('#wiz') and 'Κλειστά' in p.inner_text('#wiz'))
      p.locator('#wiz [data-a=date]:not([disabled])').first.click(); nx(); sweep(p, leak); chk(f'[salon @{w}] times in Greek ("λήξη")', 'λήξη' in p.inner_text('#wiz'))
      p.locator('#wiz [data-a=time]:not([disabled])').first.click(); nx(); p.fill('#fn', 'Sofia'); p.fill('#fe', 's@example.invalid'); p.check('#fv'); p.fill('#fx', 'Sensitive scalp'); sweep(p, leak)
      sw('en'); chk(f'[salon @{w}] switch to English mid-booking: English, typing kept', 'Step 6 of 7: Your details' in p.inner_text('#wiz') and p.input_value('#fx') == 'Sensitive scalp' and p.is_checked('#fv') and not p.evaluate(GREEK))
      sw('el'); nx(); rv = p.inner_text('#wiz'); sweep(p, leak)
      chk(f'[salon @{w}] review in Greek; a visitor named Sofia stays "Sofia"', all(x in rv for x in ('Βήμα 7 από 7', 'Ολική βαφή', 'Μάσκα μαλλιών', 'Σοφία', 'Sofia', 'Ναι')), rv[:220].replace('\n', ' '))
      nx(); cf = p.inner_text('#wiz'); sweep(p, leak); chk(f'[salon @{w}] Greek confirmation is honest', 'Μόνο επίδειξη' in cf and 'δεν στάλθηκε τίποτα' in cf)
      chk(f'[salon @{w}] Greek sweep: no English left on any page or booking step', not leak, sorted(leak)[:6])
      p.goto(B + '/demos/myrtle/'); p.wait_for_timeout(250); chk(f'[salon @{w}] plain URL stays English (no Greek)', not p.evaluate(GREEK))
      chk(f'[salon @{w}] no JS errors', not errs, errs[:2])
      c.close()
    # ---- previews follow the portfolio language
    for lp, L in (('/work/', 'en'), ('/el/work/', 'el')):
      c = br.new_context(viewport={'width': 1440, 'height': 900}); p = c.new_page()
      for slug, h1 in (('olive-and-oak', {'en': 'A Taste of the Mediterranean.', 'el': 'Μια γεύση από τη Μεσόγειο.'}), ('the-cut', None), ('halcyon-bay', None), ('myrtle-beauty-studio', None)):
        p.goto(B + lp); p.click(f'[data-preview="{slug}"]'); p.wait_for_function("document.querySelector('#pv-msg').hidden===true"); p.wait_for_timeout(300)
        fr = p.query_selector('#pv iframe').content_frame()
        chk(f'[preview {L}] {slug} opens in {L}', fr.evaluate('document.documentElement.lang') == L, fr.evaluate('document.documentElement.lang'))
        p.click('#pv-close'); p.wait_for_timeout(300)
      c.close()
    br.close()
finally: srv.terminate()
f = [r for r in R if not r[1]]; print(f'DEMO-I18N TOTAL {len(R)} | PASSED {len(R)-len(f)} | FAILED {len(f)}')
