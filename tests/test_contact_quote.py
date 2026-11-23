import os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]          # the repository folder
SITE = str(ROOT / 'public')                                   # the website
AI = os.environ.get('PN_AI_ASSISTANT_DIR', str(ROOT.parent / 'pn-digital-ai-assistant'))  # the engine repo, cloned next to this one
OUT = ROOT / 'tests' / 'output'; OUT.mkdir(exist_ok=True)
PY = sys.executable
import subprocess, time, re, glob, urllib.parse as up
from playwright.sync_api import sync_playwright
PORT='9171'; O=f'http://127.0.0.1:{PORT}'
srv=subprocess.Popen([PY,'-m','http.server',PORT,'--directory',SITE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
R=[]
def chk(n,ok,d=''):
    R.append((n,bool(ok)))
    if not ok: print('FAIL:',n,'|',str(d)[:300])
def qtext(url): return up.parse_qs(up.urlparse(url).query).get('text',[''])[0]
pages=[f for f in glob.glob(SITE + '/**/*.html',recursive=True) if '/demos/' not in f and '/test-report' not in f]
for f in pages:
    t=open(f,encoding='utf-8').read(); short=f.replace(SITE,'').replace(os.sep,'/'); el='lang="el"' in t[:80]
    chk(f'{short}: no contact placeholders or service area', 'to confirm' not in t and 'προς επιβεβαίωση' not in t and 'data-contact="area"' not in t)
    chk(f'{short}: share image tags ({"el" if el else "en"})', 'summary_large_image' in t and f'/assets/og/og-{"el" if el else "en"}.jpg' in t and 'og:image:width" content="1200"' in t and 'og:image:alt' in t)
    chk(f'{short}: forms.js loaded', '/js/forms.js' in t)
HOOK="window.__nav=[];window.PN_NAV=function(u){window.__nav.push(u)};"
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']); errs=[]
    ctx=b.new_context(viewport={'width':1440,'height':900}); ctx.add_init_script(HOOK)
    ctx.route('https://wa.me/**', lambda r: r.fulfill(status=200, content_type='text/html', body='<p>fake WhatsApp</p>'))  # no internet in tests
    pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    for path,L in (('/','en'),('/el/','el'),('/projects/the-cut/','en'),('/el/contact/','el')):
        pg.goto(O+path); pg.wait_for_timeout(250); h=pg.get_attribute('.wa-float','href')
        chk(f'[{path}] WhatsApp button opens +35794426190 with a {L} greeting, labelled', h.startswith('https://wa.me/35794426190?') and (('Γεια σας' in qtext(h)) if L=='el' else ('Hi P&N Digital' in qtext(h))) and 'WhatsApp' in pg.get_attribute('.wa-float','aria-label'), h)
    pg.goto(O+'/contact/'); pg.wait_for_timeout(300)
    hrefs=pg.eval_on_selector_all('.ccard','e=>e.map(a=>a.href)')
    chk('contact: WhatsApp, email and phone cards use the real details', hrefs[0].startswith('https://wa.me/35794426190') and hrefs[1]=='mailto:pndigitalwebsites@gmail.com' and hrefs[2]=='tel:+35794426190', hrefs)
    pg.click('.cform button[value=wa]'); pg.wait_for_timeout(200)
    chk('form: empty submit shows both errors, focuses name, opens nothing', pg.locator('#cf-en-name-err').is_visible() and pg.locator('#cf-en-msg-err').is_visible() and pg.evaluate('document.activeElement.id')=='cf-en-name' and len(ctx.pages)==1 and pg.get_attribute('#cf-en-name','aria-invalid')=='true')
    pg.fill('#cf-en-name','Maria'); pg.wait_for_timeout(100)
    chk('form: an error clears as soon as it is fixed', not pg.locator('#cf-en-name-err').is_visible())
    pg.fill('#cf-en-msg','short'); pg.click('.cform button[value=mail]'); pg.wait_for_timeout(200)
    chk('form: message under 10 characters is refused', pg.locator('#cf-en-msg-err').is_visible() and not pg.evaluate('window.__nav.length'))
    pg.fill('#cf-en-biz','Maria’s Bakery'); pg.select_option('#cf-en-type','Shop'); pg.check('input[name=need][value="A redesign of my current site"]',force=True); pg.fill('#cf-en-langs','Greek, English, Russian')
    pg.fill('#cf-en-msg','We bake bread & cakes and want a site with our menu.')
    with ctx.expect_page() as npi: pg.click('.cform button[value=wa]')
    np_=npi.value; np_.wait_for_timeout(300); url=np_.url
    tx=qtext(url)
    chk('form → WhatsApp: opens wa.me/35794426190 with every field in the message', url.startswith('https://wa.me/35794426190') and all(x in tx for x in ['Name: Maria','Business: Maria’s Bakery','Type of business: Shop','I need: A redesign of my current site','Languages: Greek, English, Russian','bread & cakes']), (url[:90],tx))
    chk('form → WhatsApp: status line explains what happened, and the site stays open in its own tab', 'Opening WhatsApp' in pg.inner_text('.fstatus') and pg.url.endswith('/contact/'))
    np_.close()
    pg.click('.cform button[value=mail]'); pg.wait_for_timeout(200); m=pg.evaluate('window.__nav[0]||""')
    mq=up.parse_qs(up.urlparse(m).query)
    chk('form → email: mailto to pndigitalwebsites@gmail.com with subject and full body', m.startswith('mailto:pndigitalwebsites@gmail.com?') and mq['subject'][0]=='Website enquiry from Maria' and 'Business: Maria’s Bakery' in mq['body'][0] and 'bread & cakes' in mq['body'][0], m[:160])
    # Greek form
    pg.goto(O+'/el/contact/'); pg.wait_for_timeout(300); pg.click('.cform button[value=wa]'); pg.wait_for_timeout(150)
    chk('form (el): Greek error messages', 'όνομά σας' in pg.inner_text('#cf-el-name-err'))
    pg.fill('#cf-el-name','Νίκος'); pg.fill('#cf-el-msg','Θέλω ιστοσελίδα για το κουρείο μου.')
    with ctx.expect_page() as npi: pg.click('.cform button[value=wa]')
    np_=npi.value; np_.wait_for_timeout(300); tx=qtext(np_.url); np_.close()
    chk('form (el) → WhatsApp: Greek message', 'Γεια σας P&N Digital' in tx and 'Όνομα: Νίκος' in tx and 'Χρειάζομαι: Νέα ιστοσελίδα' in tx, tx)
    # quote calculator
    pg.goto(O+'/services/'); pg.wait_for_timeout(400)
    def res(): return pg.inner_text('#quote .q-out')
    def num(): pg.wait_for_timeout(650); return pg.inner_text('#quote .q-num')
    chk('calc: default (new site, 2–5 pages, 2 languages) → Business €450', 'Business' in res() and num()=='€450' and 'up to 3 languages' in res())
    pg.check('#quote input[name=size][value="1"]',force=True); chk('calc: one page → Starter €250', 'Starter' in res() and num()=='€250' and 'up to 2 languages' in res())
    pg.click('#quote .st-b[data-step="1"]'); chk('calc: one page but 3 languages → Business €450, reason given', num()=='€450' and 'Business includes up to 3 languages' in res())
    pg.click('#quote .st-b[data-step="1"]'); chk('calc: 4 languages → Premium from €750', 'Premium' in res() and num()=='€750' and 'from' in pg.inner_text('#quote .q-price'))
    for _ in range(3): pg.click('#quote .st-b[data-step="1"]')
    chk('calc: 7 languages → Premium + "2 extra languages" quoted separately', '2 extra languages' in res() and 'Quoted separately' in res())
    for _ in range(10): pg.click('#quote .st-b[data-step="-1"]')
    chk('calc: languages stop at 1', pg.inner_text('#quote .st-v')=='1')
    pg.check('#quote input[name=need][value=landing]',force=True)
    chk('calc: landing page disables the size question and gives Starter', pg.evaluate("document.querySelector('#quote .q-size').disabled") and num()=='€250')
    pg.check('#quote input[value=ai]'); chk('calc: AI assistant is "quoted separately", price unchanged', 'AI chat assistant' in pg.inner_text('#quote .q-sep') and num()=='€250')
    pg.check('#quote input[value=integr]'); chk('calc: integrations → Premium, quoted separately', num()=='€750' and 'need an external service' in res())
    pg.check('#quote input[name=maint]'); chk('calc: maintenance adds €50 a month (€600 a year)', '€50 a month' in res() and '€600 a year' in res())
    chk('calc: never shows a made-up total', not re.search(r'€(1[0-9]{3}|8\d\d|9\d\d)', res()), res())
    wa=pg.get_attribute('#quote .q-wa','href'); tx=qtext(wa)
    chk('calc → WhatsApp: estimate message lists choices and the price', wa.startswith('https://wa.me/35794426190') and 'Premium — from €750' in tx and 'plus €50 a month' in tx and 'AI chat assistant' in tx and 'Could you give me a quote?' in tx, tx)
    mh=pg.get_attribute('#quote .q-mail','href'); chk('calc → email: mailto with subject', mh.startswith('mailto:pndigitalwebsites@gmail.com?subject=Quote%20request'), mh[:80])
    pg.click('#quote .q-form-link'); pg.wait_for_url('**/contact/**'); pg.wait_for_timeout(300)
    chk('calc → contact form: the estimate is pre-filled in the message', 'Premium — from €750' in pg.input_value('#cf-en-msg'))
    pg.goto(O+'/el/services/'); pg.wait_for_timeout(400)
    chk('calc (el): Greek labels and price', 'Business' in pg.inner_text('#quote .q-out') and 'έως 3 γλώσσες' in pg.inner_text('#quote .q-out'))
    pg.goto(O+'/'); pg.wait_for_timeout(200)
    chk('home: "Estimate your price" links to the calculator', pg.get_attribute('.q-cta a','href')=='/services/#quote')
    # build section
    for path in ('/projects/olive-and-oak/','/el/projects/the-cut/','/projects/nexora-business-solutions/'):
        pg.goto(O+path); pg.wait_for_timeout(300)
        n=pg.eval_on_selector_all('.b-stats .count','e=>e.map(x=>+x.dataset.to)'); steps=pg.locator('.b-steps li').count()
        chk(f'{path}: build section with 5 real stats and 6 steps', len(n)==5 and all(x>0 for x in n) and n[4]==6 and steps==6, (n,steps))
        pg.locator('.cmp-box').scroll_into_view_if_needed(); pg.wait_for_timeout(3200)
        ok=pg.evaluate("[...document.querySelectorAll('.cmp-box img')].every(i=>i.complete&&i.naturalWidth===1280)")
        chk(f'{path}: wireframe and finished images load', ok)
        pg.locator('.cmp-box input').focus(); pg.keyboard.press('End'); pg.wait_for_timeout(100)
        chk(f'{path}: slider works with the keyboard (End shows the whole wireframe)', pg.evaluate("getComputedStyle(document.querySelector('.cmp-box')).getPropertyValue('--x').trim()")=='100%')
        chk(f'{path}: slider is labelled', bool(pg.get_attribute('.cmp-box input','aria-label')))
    # phone: buttons do not cover each other
    ph=b.new_context(viewport={'width':390,'height':844}); q=ph.new_page(); q.goto(O+'/'); q.wait_for_timeout(500)
    a=q.locator('.wa-float').bounding_box(); c=q.locator('#pn-ai-host .launcher').bounding_box()
    chk('phone: WhatsApp (left) and AI chat (right) buttons do not overlap, both 52px', a['x']+a['width']<c['x'] and abs(a['width']-52)<1 and a['y']>760, (a,c))
    q.goto(O+'/contact/'); q.wait_for_timeout(300); chk('phone: contact page has no sideways scroll', q.evaluate('document.documentElement.scrollWidth')==390)
    q.goto(O+'/services/'); q.wait_for_timeout(300); chk('phone: calculator has no sideways scroll', q.evaluate('document.documentElement.scrollWidth')==390)
    ph.close()
    # reduced motion: slider does not auto-sweep
    rm=b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce'); q=rm.new_page(); q.goto(O+'/projects/the-cut/'); q.locator('.cmp-box').scroll_into_view_if_needed(); q.wait_for_timeout(1200)
    chk('reduced motion: comparison slider stays still', q.evaluate("getComputedStyle(document.querySelector('.cmp-box')).getPropertyValue('--x').trim()")=='50%'); rm.close()
    chk('no JavaScript errors', not errs, errs[:3])
    b.close()
srv.terminate()
print('CONTACT-QUOTE TOTAL',len(R),'| PASSED',sum(1 for _,o in R if o),'| FAILED',sum(1 for _,o in R if not o))
