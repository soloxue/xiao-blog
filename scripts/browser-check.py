"""Browser release checks against local project-prefix hosting or a live URL."""
import argparse,contextlib,importlib.util,json,os,shutil,threading
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote,urljoin,urlsplit,unquote
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--base-url')
parser.add_argument('--widths',default='390,856,1440')
parser.add_argument('--section',choices=('works','notes','stage'))
parser.add_argument('--output',type=Path,default=ROOT/'previews/release-audit')
args=parser.parse_args()
args.output.mkdir(parents=True,exist_ok=True)
widths=[int(x) for x in args.widths.split(',')]
spec=importlib.util.spec_from_file_location('release_audit',ROOT/'scripts/check-site.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
routes=[str(p.relative_to(ROOT)).replace('\\','/') for p in audit.html_files() if 'data-redirect' not in audit.Page(p.read_text(encoding='utf-8-sig')).attrs]
if args.section:routes=[r for r in routes if r.startswith(args.section+'/')]
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  path=unquote(urlsplit(path).path)
  rel=path[len('/xiao-blog/'):] if path.startswith('/xiao-blog/') else '__not_found__'
  target=(ROOT/rel).resolve()
  return str(target if target.is_relative_to(ROOT) else ROOT/'__not_found__')
 def log_message(self,*_):pass
server=None
if args.base_url:base=args.base_url.rstrip('/')+'/'
else:
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
 threading.Thread(target=server.serve_forever,daemon=True).start()
 base=f'http://127.0.0.1:{server.server_port}/xiao-blog/'
report=[];runtime_errors=[]
try:
 with sync_playwright() as p:
  executable=os.environ.get('XIAO_BROWSER') or next((str(x) for x in [Path('C:/Program Files/Google/Chrome/Application/chrome.exe'),Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'),Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')] if x.is_file()),None)
  browser=p.chromium.launch(headless=True,**({'executable_path':executable} if executable else {}))
  page=browser.new_page();page.emulate_media(reduced_motion='reduce')
  page.on('pageerror',lambda error:runtime_errors.append(str(error)))
  for route in routes:
   for width in widths:
    page.set_viewport_size({'width':width,'height':900 if width>760 else 844})
    response=page.goto(urljoin(base,route),wait_until='load',timeout=45000)
    assert response and response.ok,(route,response.status if response else None)
    page.evaluate('document.fonts.ready')
    page.locator('img[src]').evaluate_all("images=>images.forEach(i=>i.loading='eager')")
    page.evaluate("()=>Promise.all([...document.querySelectorAll('img[src]')].map(i=>i.decode()))")
    result=page.evaluate('''() => {
     const active=document.querySelector('.site-nav [aria-current="page"]');
     return {overflow:document.documentElement.scrollWidth-innerWidth,sticky:getComputedStyle(document.querySelector('.site-header')).position,title:document.title,active:active?.textContent,broken:[...document.querySelectorAll('img[src]')].filter(i=>!i.naturalWidth).map(i=>i.src),boundaries:[...document.querySelectorAll('.end-boundary')].map(e=>({tabIndex:e.tabIndex,href:e.getAttribute('href')})),footerLinks:document.querySelectorAll('.site-footer a').length};
    }''')
    assert result['overflow']<=1 and not result['broken'] and result['sticky']=='sticky',(route,width,result)
    assert all(x['tabIndex']==-1 and x['href'] is None for x in result['boundaries'])
    if route.startswith(('works/','notes/','stage/')):assert result['footerLinks']==0
    if width in (390,1440) and route in ('index.html','index.cn.html','stage/2025-11-18-xu-guangqi-matteo-ricci/cn.html','notes/2026-10-23-hamlet/index.html'):
     page.screenshot(path=args.output/(route.replace('/','-').replace('.html','')+f'-{width}.png'))
    report.append({'route':route,'width':width,**result})
   # Each language switch resolves to its actual counterpart.
   switch=page.locator('.language-switch a')
   if switch.count():
    expected=urljoin(page.url,switch.get_attribute('href'))
    switch.click();page.wait_for_url(expected)
   print(route,'OK',flush=True)
  for route in ('works/the-eighth-rank/cn.html','notes/2026-10-23-hamlet/index.html','stage/2025-11-18-xu-guangqi-matteo-ricci/cn.html'):
   if args.section and not route.startswith(args.section+'/'):continue
   page.goto(urljoin(base,route),wait_until='load')
   trigger=page.locator('[data-lightbox]').first;trigger.focus();page.keyboard.press('Enter')
   modal=page.locator('dialog.lightbox');modal.locator('img').wait_for(state='visible')
   page.keyboard.press('ArrowRight');modal.locator('img').wait_for(state='visible')
   modal.locator('.lightbox-zoom').click();assert modal.locator('.lightbox-zoom').get_attribute('aria-pressed')=='true'
   page.keyboard.press('Escape');assert trigger.evaluate('e=>e===document.activeElement')
  redirects=__import__('runpy').run_path(str(ROOT/'scripts/build-redirects.py'))['REDIRECTS']
  for route,target in redirects.items():
   if args.section:continue
   old=urljoin(base,route);expected=urljoin(old,target)
   page.goto(old,wait_until='commit');page.wait_for_url(expected,timeout=30000);page.wait_for_load_state('load')
  assert not runtime_errors,runtime_errors
  browser.close()
 result={'base':base,'pageViewportChecks':len(report),'redirects':0 if args.section else len(redirects),'runtimeErrors':runtime_errors,'checks':report}
 (args.output/'browser-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'pageViewportChecks':len(report),'redirects':result['redirects'],'runtimeErrors':runtime_errors},ensure_ascii=False))
finally:
 if server:server.shutdown();server.server_close()
