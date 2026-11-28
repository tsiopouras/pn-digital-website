"""Builds the single-file test copy of the site (for the claude.ai test link).

Every page of public/ becomes a hidden section; links become #routes; the five demos
are embedded and shown with srcdoc. "Open full website" opens a full-screen view of the real
demo inside the page (#full-<slug>), because a sandboxed artifact page cannot open temporary
blob: links in a new tab. The real site (zip) still opens /demos/<name>/ in a new tab.
"""
import html, json, os, re, glob

import pathlib as _p
ROOT = _p.Path(__file__).resolve().parents[1]
SITE = str(ROOT / 'public')
(ROOT / 'tests' / 'output').mkdir(exist_ok=True)
OUT = str(ROOT / 'tests' / 'output' / 'pn-digital-preview.html')
DEMO_DIR = {'olive-and-oak': 'olive-and-oak', 'the-cut': 'the-cut', 'nexora-business-solutions': 'nexora', 'halcyon-bay': 'halcyon-bay', 'myrtle-beauty-studio': 'myrtle'}
NAMES = {'olive-and-oak': 'Olive & Oak', 'the-cut': 'THE CUT', 'nexora-business-solutions': 'Nexora Business Solutions', 'halcyon-bay': 'Halcyon Bay', 'myrtle-beauty-studio': 'Myrtle Beauty Studio'}
PAGE_RE = r'^(/el)?/(?:(work|services|about|contact|privacy)/|projects/([a-z-]+)/)?$'


def rd(p):
    return open(os.path.join(SITE, p), encoding='utf-8').read()


def pack(bid):
    # The test copy is not served from an allowed website address, so the engine would refuse it: its
    # assistants always run in labelled demo mode (no engine address, nothing sent).
    return re.sub(r'"endpoint":"[^"]*"', '"endpoint":""', rd(f'assets/assistant/packs/{bid}.js'))


def route(path):
    m = re.match(PAGE_RE, path.split('?')[0].split('#')[0])
    if not m:
        return None
    pre = 'el-' if m.group(1) else ''
    return pre + (m.group(2) or ('project-' + m.group(3) if m.group(3) else 'home'))


secs, dialog = [], ''
for f in sorted(glob.glob(SITE + '/**/index.html', recursive=True)):
    rel = os.path.relpath(f, SITE).replace('\\', '/')
    if rel.startswith('demos/'):
        continue
    path = '/' + rel[:-len('index.html')]
    t = open(f, encoding='utf-8').read()
    lang = re.search(r'<html lang="(\w+)"', t).group(1)
    title = html.unescape(re.search(r'<title>(.*?)</title>', t).group(1))
    body = t.split('<body>', 1)[1]
    inner = body.split('<dialog id="pv"', 1)[0]
    inner = inner.replace('<script src="/assets/assistant/packs/pn-digital.js"></script><script src="/assets/assistant/assistant.js" data-business="pn-digital"></script>', '')
    if not dialog:
        dialog = '<dialog id="pv"' + body.split('<dialog id="pv"', 1)[1].split('</dialog>', 1)[0] + '</dialog>'
    inner = re.sub(r'<a class="skip"[^>]*>.*?</a>', '', inner).replace(' id="main"', '')
    inner = re.sub(r'href="(/[^"]*)"', lambda mm: f'href="#{route(mm.group(1))}"' if route(mm.group(1)) else mm.group(0), inner)
    secs.append(f'<div class="route" data-route="{route(path)}" data-lang="{lang}" data-title="{html.escape(title)}" hidden>{inner}</div>')

def fonts_inline(c):
    # a single file has no /fonts/ folder: embed the self-hosted fonts as data URLs
    import base64
    return re.sub(r'url\(/fonts/([\w.-]+\.woff2)\)', lambda m: 'url(data:font/woff2;base64,' + base64.b64encode(open(os.path.join(SITE, 'fonts', m.group(1)), 'rb').read()).decode() + ')', c)


css = rd('css/styles.css') + (fonts_inline(rd('css/refresh.css')) if '/css/refresh.css' in rd('index.html') else '')  # the style refresh, while it is switched on
js = ''.join(rd(f'js/{n}.js') + '\n' for n in ('site-config', 'projects', 'preview', 'main', 'forms', 'fx'))
LINKMAP = r'''window.PN_ASSISTANT_LINK=function(href,lang){if(href.charAt(0)==='#')return href;var m=href.match(/^(\/el)?\/(?:(work|services|about|contact)\/|projects\/([a-z-]+)\/)?(#.*)?$/);if(!m)return href;var pre=(lang==='el'||m[1])?'el-':'';return '#'+pre+(m[2]||(m[3]?'project-'+m[3]:'home'));};'''
agency_ai = pack('pn-digital').replace('</', '<\\/') + "window.PN_ASSISTANT_ID='pn-digital';\n" + LINKMAP + '\n'
ASSIST = rd('assets/assistant/assistant.js').replace('</', '<\\/')  # an inline script must not contain '</script'
def inline_assistant(page, bid):
    tag = f'<script src="/assets/assistant/packs/{bid}.js"></script><script src="/assets/assistant/assistant.js" data-business="{bid}"></script>'
    assert tag in page, bid
    return page.replace(tag, '<script>' + pack(bid).replace('</', '<\\/') + f'window.PN_ASSISTANT_ID={json.dumps(bid)};</script><script>' + ASSIST + '</script>')
demos = {slug: inline_assistant(rd(f'demos/{d}/index.html'), {'nexora': 'nexora'}.get(d, d)) for slug, d in DEMO_DIR.items()}
demos_js = 'window.PN_DEMOS=' + json.dumps(demos, ensure_ascii=False).replace('</', '<\\/') + ';\n'
names_js = 'window.PN_NAMES=' + json.dumps(NAMES, ensure_ascii=False) + ';\n'

FULL = '''<div id="full" hidden><div class="full-bar"><a id="full-back" href="#work">← <span id="full-back-t">Back to P&amp;N Digital</span></a><strong id="full-name"></strong><span id="full-note"></span></div><iframe id="full-frame" title="Demo website"></iframe></div>'''
FULL_CSS = '''#full{position:fixed;inset:0;z-index:100;display:flex;flex-direction:column;background:#0b0d0e}#full[hidden]{display:none}
.full-bar{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem 1rem;padding:.55rem 1rem;background:#101315;border-bottom:1px solid #2a2f33;color:#f3eee3;font:500 .9rem system-ui,sans-serif}
.full-bar a{color:#f3eee3;text-decoration:none;border:1px solid #4b5157;padding:.4rem .8rem}.full-bar a:hover{border-color:#3cc4c0}.full-bar span{color:#a9afb3;font-size:.85rem}
#full-frame{flex:1;width:100%;border:0;background:#fff}
#full:not([hidden])~.wa-float{display:none}'''

ROUTER = r'''(function(){
var secs=[].slice.call(document.querySelectorAll('.route')),dlg=document.getElementById('pv'),full=document.getElementById('full'),ff=document.getElementById('full-frame'),cur='home',curLang='en',shown='';
if(window.PN){PN.full=function(slug){return '#full-'+slug};}
var TX={en:{back:'Back to P&N Digital',note:'Demo website · fictional business · nothing is sent'},el:{back:'Επιστροφή στην P&N Digital',note:'Ιστοσελίδα επίδειξης · φανταστική επιχείρηση · τίποτα δεν αποστέλλεται'}};
function showFull(slug,lang){var html=window.PN_DEMOS&&PN_DEMOS[slug];if(!html){location.hash='#work';return}
 full.hidden=false;document.documentElement.style.overflow='hidden';var ah=document.getElementById('pn-ai-host');if(ah)ah.style.display='none';var t=TX[lang]||TX.en;
 document.getElementById('full-back-t').textContent=t.back;document.getElementById('full-note').textContent=t.note;document.getElementById('full-name').textContent=PN_NAMES[slug]||slug;
 document.getElementById('full-back').setAttribute('href','#'+(lang==='el'?'el-':'')+'project-'+slug);
 if(shown!==slug){ff.onload=function(){try{ff.contentWindow.postMessage({pnLang:lang},'*')}catch(e){}};ff.srcdoc=html;shown=slug}else{try{ff.contentWindow.postMessage({pnLang:lang},'*')}catch(e){}}
 ff.title=(PN_NAMES[slug]||slug)+(lang==='el'?' — ιστοσελίδα επίδειξης':' — demo website');document.title=(PN_NAMES[slug]||slug)+(lang==='el'?' | Επίδειξη':' | Demo');document.documentElement.lang=lang}
function go(){var h=(location.hash||'#home').slice(1),m=h.match(/^full-([a-z-]+)(?:\?lang=(el|en))?$/);
 if(dlg&&dlg.open)dlg.close();
 if(m){showFull(m[1],m[2]||curLang);return}
 full.hidden=true;document.documentElement.style.overflow='';var ah2=document.getElementById('pn-ai-host');if(ah2)ah2.style.display='';
 if(!secs.some(function(x){return x.dataset.route===h})){var cs=secs.filter(function(x){return x.dataset.route===cur})[0],tg=cs&&/^[a-z][\w-]*$/.test(h)&&cs.querySelector('[id="'+h+'"]');if(tg){tg.scrollIntoView();return}}
 var s=secs.filter(function(x){return x.dataset.route===h})[0]||secs.filter(function(x){return x.dataset.route===cur})[0]||secs[0];
 cur=s.dataset.route;curLang=s.dataset.lang;secs.forEach(function(x){x.hidden=x!==s});document.documentElement.lang=curLang;document.title=s.dataset.title;
 var n=s.querySelector('nav');if(n)n.classList.remove('open');window.scrollTo(0,0);if(window.PNrefresh)PNrefresh()}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#full-"]');if(!a)return;e.preventDefault();e.stopPropagation();if(dlg&&dlg.open)dlg.close();location.hash=a.getAttribute('href')},true);
addEventListener('hashchange',go);go();})();'''

safe = ':root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}'
doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
       '<script>document.documentElement.classList.add("js")</script><title>P&amp;N Digital | Preview</title>'
       '<meta name="description" content="Test preview of the P&amp;N Digital website in English and Greek.">'
       f'<style>{css}{FULL_CSS}{safe}</style></head><body>' + ''.join(secs) + dialog + FULL +
       f'<script>{demos_js}{names_js}{js}{ROUTER}</script><script>{agency_ai}</script><script>{ASSIST}</script></body></html>')
import base64
def _inline_img(m):  # a single-file copy cannot load /images/... so embed them
    path = os.path.join(SITE, m.group(1).lstrip('/'))
    return 'src="data:image/jpeg;base64,' + base64.b64encode(open(path, 'rb').read()).decode() + '"'
doc = re.sub(r'src="(/images/[^"]+\.jpg)"', _inline_img, doc)
open(OUT, 'w', encoding='utf-8').write(doc)
print('pages:', len(secs), '| bytes:', len(doc.encode('utf-8')))
