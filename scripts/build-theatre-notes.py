"""Build the six supplied theatre archives, their bilingual pages and catalogues.

Run from any directory. Sources live beside the site in 朋友圈 on first intake;
each content folder then retains source.txt as an unchanged record of the wording.
"""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

from theatre_notes_content import EVENTS
from article_presentation import article_attributes, hero_image
from reading_navigation import render_reading_navigation

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT.parent / '朋友圈'
VERSION = '20261026-stage-bookends'
HOME_VERSION = '20261025-article-design'


def paragraphs(text):
    return [p.strip() for p in re.split(r'\n\s*\n', text.replace('\u200b', '')) if p.strip()]


def esc(value):
    return html.escape(str(value), quote=True)


def date_label(value, language):
    d = date.fromisoformat(value)
    return f'{d.year}年{d.month}月{d.day}日' if language == 0 else f'{d.day} {d:%b %Y}'


def reading_paragraphs(text, index):
    # Insert only whitespace at sentence boundaries; the source wording is intact.
    threshold = 450 if re.search(r'[\u3400-\u9fff]', text) else 1000
    units = re.split(r'(?<=[。！？])|(?<=[.!?])\s+', text)
    chunks, current = [], ''
    for unit in units:
        if not unit:
            continue
        separator = ' ' if current and not current.endswith(tuple('。！？')) else ''
        current += separator + unit
        if len(current) >= threshold:
            chunks.append(current)
            current = ''
    if current:
        chunks.append(current)
    return '\n'.join(f'<p data-source-block="{index}">{esc(chunk).replace(chr(10), "<br>")}</p>' for chunk in chunks)


def photos(event, photo_items, language):
    size_class = ' note-photo-row--two' if len(photo_items) == 2 else ''
    label = '照片' if language == 0 else 'Photographs'
    rows = [f'<div class="note-photo-row{size_class}" role="group" aria-label="{label}">']
    for photo in photo_items:
        alt = event['alts'][photo['position']][language]
        verb = '放大照片' if language == 0 else 'Enlarge photo'
        rows.append(f'<a href="{photo["name"]}" class="note-grid-item note-grid-item--preserve" data-lightbox aria-label="{verb}: {esc(alt)}"><img src="{photo["name"]}" width="{photo["width"]}" height="{photo["height"]}" alt="{esc(alt)}" loading="lazy" decoding="async"></a>')
    return '\n'.join(rows + ['</div>'])


def guide(language):
    if language == 0:
        return '''<details class="note-reading-guide"><summary>阅读提示：人物、歌名与缩写</summary>
<p>Jon Robyns 饰魅影（Erik），Lily Kerhoas 饰克里斯汀（Christine），Joe Griffiths-Brown 饰拉乌尔（Raoul）。文中会交替使用演员名和角色名；她比较的也是这一晚的演法。</p>
<dl><dt>STYDI</dt><dd>Stranger Than You Dreamt It，第一次摘下面具后的场景。</dd><dt>MotN / AIAOY / PoNR</dt><dd>The Music of the Night / All I Ask of You / The Point of No Return。</dd><dt>OLC / 25RAH</dt><dd>伦敦原版卡司录音 / 皇家阿尔伯特音乐厅25周年演出。</dd><dt>句尾颤音</dt><dd>一个长音先保持平直，到末尾才开始颤动；这是她反复对比的歌唱细节。</dd></dl></details>'''
    return '''<details class="note-reading-guide"><summary>Reading guide: people, songs and abbreviations</summary>
<p>Jon Robyns plays the Phantom (Erik), Lily Kerhoas plays Christine, and Joe Griffiths-Brown plays Raoul. The note moves between actor and character names while discussing that evening’s performances.</p>
<dl><dt>STYDI</dt><dd>Stranger Than You Dreamt It, following the first unmasking.</dd><dt>MotN / AIAOY / PoNR</dt><dd>The Music of the Night / All I Ask of You / The Point of No Return.</dd><dt>OLC / 25RAH</dt><dd>Original London cast recording / the 25th-anniversary performance at the Royal Albert Hall.</dd><dt>Terminal vibrato</dt><dd>Vibrato introduced towards the end of a sustained note, a recurring detail in her comparisons.</dd></dl></details>'''


def build_page(event, blocks, photo_items, language):
    filename = 'cn.html' if language == 0 else 'index.html'
    template = (ROOT / 'notes/2026-10-23-hamlet' / filename).read_text(encoding='utf-8')
    header = re.search(r'  <header class="site-header">.*?</header>', template, re.S).group()
    footer = re.search(r'  <footer class="site-footer">.*?</footer>', template, re.S).group()
    phantom = 'phantom' in event['slug']
    title = event['title'][language]
    moment = ('中文译文 · 译自英文为主的朋友圈原文' if language == 0 else 'Original English note · Chinese introduction translated') if phantom else ('散场之后 · 朋友圈原文' if language == 0 else 'Translated from the Chinese post')
    if event['date'] == '2025-11-26':
        moment = '影像观演 · 朋友圈原文（含后续更新）' if language == 0 else 'Screen viewing · Translated from the Chinese post, including its update'
    opening = [f'<p class="moment-head">{moment}</p>']
    headings = event.get('headings', {})
    if phantom:
        items = ''.join(f'<li><a href="#part-{i}">{esc(labels[language])}</a></li>' for i, labels in headings.items())
        opening += [guide(language), f'<nav class="note-contents" aria-label="{"本文目录" if language == 0 else "In this note"}"><ol>{items}</ol></nav>']
    body, group = [], 0
    for i, block in enumerate(blocks):
        if i in headings:
            body.append(f'<h2 class="note-subheading" id="part-{i}">{esc(headings[i][language])}</h2>')
        body.append(reading_paragraphs(block, i))
        if i in event['photos_after']:
            body.append(photos(event, photo_items[group*3:(group+1)*3], language))
            group += 1
    assert group * 3 >= len(photo_items), event['slug']
    lang = 'zh-CN' if language == 0 else 'en'
    skip = '跳到札记' if language == 0 else 'Skip to the note'
    counterpart = 'index.html' if language == 0 else 'cn.html'
    byline = '笑笑' if language == 0 else 'Xiaoxiao'
    date_prefix = '记录于' if language == 0 else 'Note dated'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(event['summary'][language])}">
  <title>{esc(title)} — {byline}</title>
  <link rel="icon" href="../../favicon.svg" type="image/svg+xml">
  <link rel="alternate" hreflang="{'en' if language == 0 else 'zh-CN'}" href="{counterpart}">
  <link rel="stylesheet" href="../../styles.css?v={VERSION}">
  <script src="../../app.js?v=20261025-article-design" defer></script>
</head>
<body class="note-page archive-note{' phantom-note' if phantom else ''}" {article_attributes(event["slug"])}>
  <a class="skip-link" href="#main">{skip}</a>
{header}
  <main id="main">
    <header class="note-hero article-hero">{hero_image(event["slug"])}<div class="note-hero-copy section-shell">
      <p class="eyebrow">{esc(event['kind'][language])} · {date_prefix} <time datetime="{event['date']}">{date_label(event['date'], language)}</time></p>
      <h1>{esc(title)}</h1>
      <p class="note-deck">{esc(event['deck'][language])}</p>
    </div></header>
    <article class="note-body" aria-label="{esc(title)}">
      <div class="note-verbatim">
{chr(10).join(opening + body)}
      </div>
    </article>
  </main>
{render_reading_navigation(ROOT, "notes", event["slug"], language)}
{footer}
</body>
</html>
'''


def index_entry(event, language):
    filename = 'cn.html' if language == 0 else 'index.html'
    target = event['slug'] + '/' + filename
    cover = event['photos'][event['cover_position']]
    d = date.fromisoformat(event['date'])
    day = f'{d.month}月{d.day}日' if language == 0 else f'{d.day} {d:%b}'
    year = f'{d.year}年' if language == 0 else str(d.year)
    read = '阅读这则札记' if language == 0 else 'Read this note'
    return f'''      <article class="notes-entry">
        <p class="notes-entry-date"><time datetime="{event['date']}"><span>{day}</span><span>{year}</span></time></p>
        <div class="notes-entry-copy"><p class="eyebrow">{esc(event['kind'][language])}</p>
          <h2><a href="{target}">{esc(event['title'][language])}</a></h2>
          <p>{esc(event['summary'][language])}</p>
          <a class="text-link" href="{target}">{read}</a>
        </div>
        <a class="notes-entry-image notes-entry-image--preserve" href="{target}" aria-label="{esc(read + ': ' + event['title'][language])}"><img src="{event['slug']}/{cover['name']}" width="{cover['width']}" height="{cover['height']}" alt="{esc(event['alts'][event['cover_position']][language])}" loading="lazy" decoding="async"></a>
      </article>'''


def update_catalogues():
    events = sorted(EVENTS, key=lambda e:e['date'], reverse=True)
    for language, filename in enumerate(('index.cn.html', 'index.html')):
        path = ROOT / 'notes' / filename
        page = path.read_text(encoding='utf-8')
        for event in events:
            page = re.sub(r'\s*<article class="notes-entry">(?:(?!<article).)*?' + re.escape(event['slug']) + r'(?:(?!<article).)*?</article>', '', page, flags=re.S)
        entries = '\n'.join(index_entry(event, language) for event in events)
        page = page.replace('    </section>', entries + '\n    </section>', 1)
        page = page.replace('散场以后，还想说的话。音乐会、话剧、音乐剧，还有那些留在心里的夜晚。照片和当时写下的文字，记录每一次到场。', '散场以后，还想说的话。音乐会、话剧、音乐剧，以及屏幕前的重聚。照片和当时写下的文字，记住那些留在心里的夜晚。')
        page = page.replace('Concerts, plays and other evenings that stayed with her. Photographs and words from the audience, kept together as a record of each occasion.', 'Concerts, plays, musicals and a reunion on screen. Photographs and words, keeping the evenings that stayed with her.')
        page = re.sub(r'styles\.css\?v=[^"\s]+', 'styles.css?v=' + VERSION, page)
        path.write_text(page, encoding='utf-8')
        total_notes = page.count('<article class="notes-entry">')
        path = ROOT / filename
        page = path.read_text(encoding='utf-8')
        for event in events:
            page = re.sub(r'\s*<li><a href="notes/' + re.escape(event['slug']) + r'/.*?</li>', '', page, flags=re.S)
        ledger = []
        for event in events:
            target = f'notes/{event["slug"]}/{"cn.html" if language == 0 else "index.html"}'
            ledger.append(f'          <li><a href="{target}"><span class="work-type">{esc(event["kind"][language])}</span><h3>{esc(event["title"][language])}</h3><span class="work-context"><time datetime="{event["date"]}">{date_label(event["date"], language)}</time></span></a></li>')
        pattern = r'(<ul class="work-ledger note-ledger"[^>]*>)(.*?)(\s*</ul>)'
        def recent_rows(match):
            rows = re.findall(r'<li>.*?</li>', match[2], re.S) + ledger
            rows.sort(key=lambda row: re.search(r'datetime="([\d-]+)"', row)[1], reverse=True)
            return match[1] + '\n' + '\n'.join('          ' + row.strip() for row in rows[:3]) + match[3]

        page = re.sub(pattern, recent_rows, page, count=1, flags=re.S)
        label = '查看全部札记' if language == 0 else 'View all notes'
        count = f'共 {total_notes} 则' if language == 0 else f'{total_notes} notes'
        all_link = f'<a class="section-all-link" href="notes/{filename}"><span class="section-all-label">{label}</span><span class="section-all-meta"><span>{count}</span><span class="section-all-arrow" aria-hidden="true">→</span></span></a>'
        page = re.sub(r'<a class="section-all-link" href="notes/index(?:\.cn)?\.html">.*?</a>', lambda _: all_link, page, count=1, flags=re.S)
        page = page.replace('音乐会与话剧，三个留在心里的夜晚。照片与散场后写下的话。', '从伦敦西区到法语音乐剧与中文舞台，还有屏幕前的重聚。照片与散场后写下的话。')
        page = page.replace('A play and two concerts, three evenings that stayed with her. Photographs and words written after the curtain.', 'Concerts, musicals, plays and a reunion on screen. Photographs and words after the curtain.')
        page = re.sub(r'styles\.css\?v=[^"\s]+', 'styles.css?v=' + HOME_VERSION, page)
        path.write_text(page, encoding='utf-8')


def main():
    for event in EVENTS:
        event['date'] = event['folder'][:10]
        source_folder = ARCHIVE / event['folder']
        target = ROOT / 'notes' / event['slug']
        target.mkdir(exist_ok=True)
        source_path = target / 'source.txt'
        if not source_path.exists():
            source_path.write_bytes((source_folder / 'note.txt').read_bytes())
        source_blocks = paragraphs(source_path.read_text(encoding='utf-8-sig'))
        phantom = 'phantom' in event['slug']
        if phantom:
            chinese = paragraphs(event['zh'])
            english = source_blocks.copy()
            english[3] = 'This was such a close call: Jon Robyns injured his foot last Wednesday and nearly couldn’t make it, and Joe had been travelling a couple of days ago and almost missed his principal performance. But all three principals are on today. All I can say is that I’m ridiculously lucky 😏❤️'
        else:
            chinese = source_blocks
            english = paragraphs(event['en'])
        assert len(chinese) == len(english) == len(source_blocks), (event['slug'], len(source_blocks), len(chinese), len(english))
        assert not re.search(r'[\u3400-\u9fff]', ''.join(english)), event['slug']
        originals = sorted(source_folder.glob('*.jpg'), key=lambda p:int(p.stem))
        assert len(originals) == len(event['alts']), event['slug']
        photo_items = []
        for position, original in enumerate(originals):
            filename = f'photo-{int(original.stem):02d}.webp'
            image = ImageOps.exif_transpose(Image.open(original)).convert('RGB')
            image.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
            image.save(target / filename, quality=88, method=6)
            photo_items.append(dict(position=position, original=original.name, name=filename, width=image.width, height=image.height))
        event['photos'] = photo_items
        event['cover_position'] = next(i for i,p in enumerate(photo_items) if int(Path(p['original']).stem) == event['cover'])
        for language, blocks in enumerate((chinese, english)):
            filename = 'cn.html' if language == 0 else 'index.html'
            (target / filename).write_text(build_page(event, blocks, photo_items, language), encoding='utf-8')
        (target / 'archive.json').write_text(json.dumps(dict(date=event['date'], date_source='Supplied archive folder; date of record', source_folder=event['folder'], source_language='English and Chinese' if phantom else 'Chinese with multilingual quotations', chinese_edition='Translation' if phantom else 'Original post', english_edition='Original post with Chinese introduction translated' if phantom else 'Translation', original_paragraphs=len(source_blocks), photos=photo_items), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(event['slug'], f'{len(source_blocks)} source paragraphs; {len(photo_items)} photos; 2 pages')
    update_catalogues()


if __name__ == '__main__':
    main()
