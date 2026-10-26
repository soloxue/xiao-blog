"""Shared static reading navigation, ordered by the corresponding catalogue."""
from html import escape, unescape
from pathlib import Path
import re


def catalogue_entries(root, section, language):
    if section not in ('works', 'notes', 'stage'):
        raise ValueError('Reading navigation supports Works, Notes and Stage')
    index_name = 'index.cn.html' if language == 0 else 'index.html'
    catalogue = (Path(root) / section / index_name).read_text(encoding='utf-8')
    targets = re.findall(r'<h2\b[^>]*>\s*<a href="([^"]+)"', catalogue)
    entries = []
    for target in targets:
        source = (Path(root) / section / target).read_text(encoding='utf-8')
        heading = re.search(r'<h1\b[^>]*>(.*?)</h1>', source, re.S)
        if not heading:
            raise ValueError(f'Missing article title: {target}')
        raw = re.sub(r'>\s+<', '><', heading[1])
        title = unescape(re.sub('<[^>]+>', '', raw))
        title = ' '.join(title.split())
        entries.append((target, title))
    if not entries or len({target for target, _ in entries}) != len(entries):
        raise ValueError(f'Empty or duplicate catalogue: {section}/{index_name}')
    return entries


def render_reading_navigation(root, section, slug, language):
    entries = catalogue_entries(root, section, language)
    filename = 'cn.html' if language == 0 else 'index.html'
    current = f'{slug}/{filename}'
    position = [target for target, _ in entries].index(current)
    zh = language == 0
    noun = {'works': 'work', 'notes': 'note', 'stage': 'entry'}[section]
    label = {'works': '作品间导航', 'notes': '札记间导航', 'stage': '舞台记录间导航'}[section] if zh else 'Continue reading'
    items = []
    for direction, index, arrow in [('prev', position - 1, '←'), ('next', position + 1, '→')]:
        word = ('上一篇' if direction == 'prev' else '下一篇') if zh else ('Previous ' if direction == 'prev' else 'Next ') + noun
        wording = f'{arrow} {word}' if direction == 'prev' else f'{word} {arrow}'
        if 0 <= index < len(entries):
            target, title = entries[index]
            items.append(f'    <a class="end-{direction}" href="../{escape(target, quote=True)}" rel="{direction}"><span class="end-label">{wording}</span><span class="end-title">{escape(title)}</span></a>')
        else:
            state = ('已是第一篇' if direction == 'prev' else '已是最后一篇') if zh else f'This is the {"first" if direction == "prev" else "last"} {noun}'
            bookend = ('开篇' if direction == 'prev' else '终篇') if zh else ('Beginning' if direction == 'prev' else 'Finis')
            items.append(f'    <div class="end-{direction} end-boundary" aria-disabled="true"><span class="end-label">{wording}</span><span class="end-mark" aria-hidden="true"><span class="end-ornament">❦</span><span>{bookend}</span></span><span class="end-status">{state}</span></div>')
    return f'<nav class="end-nav reading-nav" aria-label="{label}">\n  <div class="end-nav-inner">\n' + '\n'.join(items) + '\n  </div>\n</nav>'
