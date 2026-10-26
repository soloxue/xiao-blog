"""Check archive fidelity, bilingual completeness, photo order and discovery."""
from collections import defaultdict
import html
import json
import re
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image
from theatre_notes_content import EVENTS

ROOT = Path(__file__).resolve().parents[1]


def text(fragment):
    return html.unescape(re.sub('<[^>]+>', '', fragment.replace('<br>', '\n')))


def compact(value):
    return re.sub(r'\s|\u200b', '', value)


def main():
    total_photos = 0
    font = TTFont(ROOT / 'fonts/lxgw-wenkai-display.woff2').getBestCmap()
    for event in EVENTS:
        directory = ROOT / 'notes' / event['slug']
        source = (directory / 'source.txt').read_text(encoding='utf-8-sig').replace('\u200b', '')
        original = [p.strip() for p in re.split(r'\n\s*\n', source) if p.strip()]
        manifest = json.loads((directory / 'archive.json').read_text(encoding='utf-8'))
        assert manifest['original_paragraphs'] == len(original)
        expected_photos = [photo['name'] for photo in manifest['photos']]
        total_photos += len(expected_photos)
        assert all(ord(c) in font for c in event['title'][0] if not c.isspace()), event['slug']
        for filename in ('cn.html', 'index.html'):
            page = (directory / filename).read_text(encoding='utf-8')
            collected = defaultdict(list)
            for i, fragment in re.findall(r'<p data-source-block="(\d+)">(.*?)</p>', page, re.S):
                collected[int(i)].append(text(fragment))
            assert sorted(collected) == list(range(len(original))), (event['slug'], filename, 'Missing source block')
            for i, block in enumerate(original):
                preserve = (filename == 'cn.html' and 'phantom' not in event['slug']) or (filename == 'index.html' and 'phantom' in event['slug'] and i != 3)
                if preserve:
                    assert compact(''.join(collected[i])) == compact(block), (event['slug'], filename, i, 'Source wording changed')
            rendered_photos = re.findall(r'<img src="(photo-\d+\.webp)"', page)
            assert rendered_photos == expected_photos, (event['slug'], filename, 'Photo order/count')
            assert page.count('data-lightbox') == len(expected_photos)
            assert 'href="' + ('index.html' if filename == 'cn.html' else 'cn.html') + '"' in page
            assert re.search(r'<a href="../index(?:\.cn)?\.html" aria-current="page">', page)
            if filename == 'index.html':
                visible = text(page).replace('中文', '')
                assert not re.search(r'[\u3400-\u9fff]', visible), event['slug']
        for photo in manifest['photos']:
            with Image.open(directory / photo['name']) as image:
                assert image.size == (photo['width'], photo['height'])
        print(event['slug'], 'OK:', len(original), 'source blocks,', len(expected_photos), 'photos, two complete editions')
    assert total_photos == 49, total_photos
    for filename in ('index.cn.html', 'index.html'):
        index = (ROOT / 'notes' / filename).read_text(encoding='utf-8')
        dates = re.findall(r'<p class="notes-entry-date"><time datetime="([\d-]+)"', index)
        assert len(dates) == 9 and dates == sorted(set(dates), reverse=True), dates
        home = (ROOT / filename).read_text(encoding='utf-8')
        ledger = re.search(r'<ul class="work-ledger note-ledger"[^>]*>(.*?)</ul>', home, re.S)[1]
        assert ledger.count('<li>') == 3
        assert re.findall(r'datetime="([\d-]+)"', ledger) == dates[1:4]
        for event in EVENTS:
            assert index.count(f'<h2><a href="{event["slug"]}/') == 1
        for section, catalogue, total in (('works', 'catalogue-item', 6), ('notes', 'notes-entry', 9)):
            full_index = (ROOT / section / filename).read_text(encoding='utf-8')
            assert full_index.count(f'<article class="{catalogue}"') == total
            latest = re.findall(r'<h2\b[^>]*>\s*<a href="([^"]+)"', full_index)[:4]
            preview = re.search(r'<section[^>]+id="' + section + r'".*?</section>', home, re.S)[0]
            actual = list(dict.fromkeys(target for target in re.findall(r'href="(' + section + r'/[^"]+)"', preview) if target.count('/') == 2))
            assert actual == [section + '/' + target for target in latest], (filename, section, actual, latest)
            assert f'class="section-all-link" href="{section}/{filename}"' in preview
    print('49 photographs; 12 new pages; complete 6-work and 9-note indexes; homepage previews show the latest 1+3 in each section; complete title glyph coverage; no residual Han text in new English pages.')


if __name__ == '__main__':
    main()
