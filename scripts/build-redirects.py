"""Maintain redirects for URLs published by the previous xiao-blog edition."""
from pathlib import Path
from html import escape
import json
ROOT = Path(__file__).resolve().parents[1]
REDIRECTS = {
 'index.zh.html':'index.cn.html',
 'works.html':'works/index.html','works.zh.html':'works/index.cn.html',
 'notes.html':'notes/index.html','notes.zh.html':'notes/index.cn.html',
 'stage.html':'stage/index.html','stage.zh.html':'stage/index.cn.html',
 'about.html':'index.html#about','about.zh.html':'index.cn.html#about',
}
for slug in ('florence','florilegium','iatrogenesis','on-neuroscience-and-religious-experience','ozymandias','the-eighth-rank'):
 REDIRECTS[f'works/{slug}/zh.html']='cn.html'
REDIRECTS['notes/2026-08-23-thomas-bergersen/zh.html']='cn.html'

def main():
 for source,target in REDIRECTS.items():
  path=ROOT/source
  assert (path.parent/target.split('#')[0]).is_file(),(source,target)
  zh=source.endswith('zh.html')
  label='页面已更新，正在前往新版。' if zh else 'This page has moved to the new edition.'
  lang='zh-CN' if zh else 'en'
  script_target=json.dumps(target,ensure_ascii=False)
  source_text=f'''<!doctype html>
<html lang="{lang}" data-redirect="{escape(target,quote=True)}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{'页面已更新' if zh else 'Page moved'} — Xiaoxiao</title>
<meta http-equiv="refresh" content="0;url={escape(target,quote=True)}">
<script>const destination = new URL({script_target}, location.href); if (location.hash && !destination.hash) destination.hash = location.hash; location.replace(destination.href);</script>
</head><body><p><a href="{escape(target,quote=True)}">{label}</a></p></body></html>
'''
  path.write_text(source_text,encoding='utf-8')
 print(f'{len(REDIRECTS)} legacy redirects generated.')
if __name__=='__main__':main()
