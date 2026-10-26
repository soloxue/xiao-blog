"""Portable static release audit. Does not need private intake records."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.stack=[];self.ids=set();self.refs=[];self.images=[];self.visible=[];self.h1=[];self.attrs={};self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.attrs=a
  if 'id' in a:self.ids.add(a['id'])
  for key in ('href','src'):
   if a.get(key):self.refs.append(a[key])
  if tag=='img':self.images.append(a)
  if tag not in VOID:self.stack.append((tag,a))
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):
  if any(t in ('script','style') or 'language-switch' in a.get('class','').split() for t,a in self.stack):return
  self.visible.append(data)
  if any(t=='h1' for t,a in self.stack):self.h1.append(data)

def html_files():
 return sorted(p for p in ROOT.rglob('*.html') if not any(x in p.relative_to(ROOT).parts for x in ('.git','previews','audits','node_modules','.venv')))
def main():
 errors=[];pages={p:Page(p.read_text(encoding='utf-8-sig')) for p in html_files()};canonical=[];redirects=[]
 def check_ref(source,ref):
  u=urlsplit(ref)
  if u.scheme in ('https','http','mailto','tel','data','blob') or u.netloc:return
  if u.scheme:errors.append(f'{source.relative_to(ROOT)}: unsupported reference {ref}');return
  if u.path.startswith('/'):errors.append(f'{source.relative_to(ROOT)}: root-relative URL breaks project Pages: {ref}');return
  target=(source.parent/unquote(u.path)).resolve() if u.path else source
  if target.is_dir():target=target/'index.html'
  if not target.is_relative_to(ROOT):errors.append(f'{source.relative_to(ROOT)}: reference escapes site: {ref}');return
  if not target.is_file():errors.append(f'{source.relative_to(ROOT)}: missing {ref}');return
  if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{source.relative_to(ROOT)}: missing anchor {ref}')
 for path,page in pages.items():
  rel=path.relative_to(ROOT).as_posix();text=path.read_text(encoding='utf-8-sig')
  for ref in page.refs:check_ref(path,ref)
  if 'data-redirect' in page.attrs:
   redirects.append(rel);check_ref(path,page.attrs['data-redirect']);continue
  canonical.append(rel)
  if not page.h1:errors.append(f'{rel}: no h1')
  expected='zh' if path.name in ('cn.html','index.cn.html') else 'en'
  if not page.attrs.get('lang','').startswith(expected):errors.append(f'{rel}: wrong language')
  if expected=='en' and re.search('[\u3400-\u9fff]',''.join(page.visible)):errors.append(f'{rel}: residual Han text in English edition')
  for image in page.images:
   if 'alt' not in image:errors.append(f'{rel}: missing image alt')
   if not all(str(image.get(k,'')).isdigit() for k in ('width','height')):errors.append(f'{rel}: image lacks dimensions: {image.get("src")}')
  if rel.startswith(('works/','notes/','stage/')):
   footer=re.search(r'<footer class="site-footer">.*?</footer>',text,re.S)
   if not footer or '<a ' in footer[0]:errors.append(f'{rel}: footer must contain copyright only')
  parts=rel.split('/')
  if len(parts)==3 and parts[0] in ('works','notes','stage'):
   from reading_navigation import render_reading_navigation
   expected_nav=render_reading_navigation(ROOT,parts[0],parts[1],0 if expected=='zh' else 1)
   actual=re.search(r'<nav class="end-nav reading-nav".*?</nav>',text,re.S)
   if not actual or actual[0]!=expected_nav:errors.append(f'{rel}: navigation differs from catalogue renderer')
   counterpart=path.with_name('index.html' if expected=='zh' else 'cn.html')
   if not counterpart.exists():errors.append(f'{rel}: missing language counterpart')
 for stylesheet in ROOT.glob('*.css'):
  for ref in re.findall(r'url\([\"\']?([^\"\')]+)',stylesheet.read_text(encoding='utf-8')):check_ref(stylesheet,ref)
 for required in ('.nojekyll','README.md','AGENTS.md','fonts/OFL-Zhuque.txt','fonts/OFL-LXGW-WenKai.txt'):
  if not (ROOT/required).is_file():errors.append(f'Missing required release file: {required}')
 from reading_navigation import catalogue_entries
 counts={section:len(catalogue_entries(ROOT,section,1)) for section in ('works','notes','stage')}
 for section,count in counts.items():
  details=[r for r in canonical if r.startswith(section+'/') and r.count('/')==2]
  if len(details)!=count*2:errors.append(f'{section}: catalogue/detail edition mismatch')
 result={'canonicalPages':len(canonical),'legacyRedirects':len(redirects),'articles':counts,'errors':errors}
 print(json.dumps(result,ensure_ascii=False,indent=2));return bool(errors)
if __name__=='__main__':sys.exit(main())
