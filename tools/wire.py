import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
# Regenerates the "How we built it" images: a screenshot of each demo homepage and a wireframe of the same page.
# Run from the repository folder:  python tools/wire.py
import subprocess, sys, time
from playwright.sync_api import sync_playwright
_srv = subprocess.Popen([sys.executable, '-m', 'http.server', '5613', '--directory', str(ROOT / 'public')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
WIRE='''*,*::before,*::after{color:transparent!important;text-shadow:none!important;box-shadow:none!important;background-image:none!important;animation:none!important;transition:none!important;border-color:#5f6870!important;caret-color:transparent}
html,body{background:#eef0ee!important}
body *{background-color:transparent!important}
h1,h2,h3,h4,p,a,li,span,label,button,small,strong,em,dt,dd,figcaption,blockquote{background-color:#c3c9cd!important;border-radius:2px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
h1,h2,h3{background-color:#7d878e!important}
img,svg,canvas,video,picture,iframe,[class*=art],[class*=photo],[class*=img],[class*=pic],figure{visibility:hidden!important}
img,svg,canvas,video,picture,figure,[class*=art],[class*=photo]{outline:2px dashed #5f6870!important;outline-offset:-2px}
section,header,footer,nav,article,aside,main>div{outline:1px dashed #9aa3a9!important}
#pn-ai-host{display:none!important}
main *:has(> svg[viewBox$="200"]),main *:has(> svg[viewBox$="220"]),main *:has(> svg[viewBox$="240"]),[class~=art],[class*=-art],[class*=hero-art],figure,[class*=photo],[class*=visual],[class*=illus]{visibility:visible!important;background:repeating-linear-gradient(45deg,#d3d8db 0 10px,#e3e6e8 10px 20px)!important;outline:2px dashed #5f6870!important;outline-offset:-2px}
main *:has(> svg[viewBox$="200"]) *,main *:has(> svg[viewBox$="220"]) *,main *:has(> svg[viewBox$="240"]) *,[class~=art] *,[class*=-art] *,[class*=hero-art] *,figure *,[class*=photo] *,[class*=visual] *,[class*=illus] *{visibility:hidden!important}'''
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox'])
    for slug,d in (('olive-and-oak','olive-and-oak'),('the-cut','the-cut'),('nexora-business-solutions','nexora'),('halcyon-bay','halcyon-bay'),('myrtle-beauty-studio','myrtle')):
        pg=b.new_page(viewport={'width':1280,'height':800},device_scale_factor=1)
        pg.emulate_media(reduced_motion='reduce')
        pg.goto(f'http://127.0.0.1:5613/demos/{d}/'); pg.wait_for_timeout(1200)
        pg.add_style_tag(content='#pn-ai-host{display:none!important}*{animation-duration:0s!important;transition:none!important}'); pg.wait_for_timeout(300)
        pg.screenshot(path=str(ROOT/'public'/'images'/'build'/f'{slug}-site.jpg'),type='jpeg',quality=78)
        pg.add_style_tag(content=WIRE); pg.wait_for_timeout(300)
        pg.screenshot(path=str(ROOT/'public'/'images'/'build'/f'{slug}-sketch.jpg'),type='jpeg',quality=78)
        pg.close()
    b.close()

_srv.terminate()
