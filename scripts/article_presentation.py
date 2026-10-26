"""Shared static article cover markup. Inline photos keep their original layout."""
from html import escape

COVERS = {'the-eighth-rank': ('8th-01-cover.webp', '42% 48%', '28% 50%'),
 'iatrogenesis': ('iat-01-cover.webp', '54% 42%', '64% 40%'),
 'ozymandias': ('oz-01-cover.webp', '55% 45%', '64% 50%'),
 'florilegium': ('flo-01-cover.webp', '65% 45%', '66% 50%'),
 'florence': ('flr-01-cover.webp', '56% 45%', '62% 50%'),
 'on-neuroscience-and-religious-experience': ('neuro-01-cover.webp', '60% 44%', '60% 45%'),
 '2024-06-28-the-phantom-of-the-opera': ('photo-02.webp', '50% 45%', '58% 45%'),
 '2025-11-14-looking-for-li-ergou': ('photo-01.webp', '50% 50%', '60% 50%'),
 '2025-11-26-notre-dame-reunion': ('photo-02.webp', '50% 0%', '50% 0%'),
 '2025-12-19-romeo-et-juliette': ('photo-08.webp', '50% 0%', '58% 0%'),
 '2026-02-14-notre-dame-de-paris': ('photo-07.webp', '50% 0%', '58% 0%'),
 '2026-05-30-the-orphan-of-zhao': ('photo-08.webp', '50% 50%', '62% 50%'),
 '2026-08-23-thomas-bergersen': ('tb-08.webp', '50% 50%', '58% 50%'),
 '2026-09-24-french-musical-gala': ('fm-05.webp', '50% 50%', '60% 50%'),
 '2026-10-23-hamlet': ('hamlet-08.webp', '52% 50%', '63% 50%'),
 '2025-11-18-xu-guangqi-matteo-ricci': ('stage-08.webp', '50% 0%', '60% 0%')}

COVER_SIZES = {'the-eighth-rank': (1600, 900),
 'iatrogenesis': (1600, 800),
 'ozymandias': (1600, 800),
 'florilegium': (1600, 900),
 'florence': (1600, 900),
 'on-neuroscience-and-religious-experience': (1600, 900),
 '2024-06-28-the-phantom-of-the-opera': (1440, 1080),
 '2025-11-14-looking-for-li-ergou': (1440, 1080),
 '2025-11-26-notre-dame-reunion': (1080, 1080),
 '2025-12-19-romeo-et-juliette': (1440, 1080),
 '2026-02-14-notre-dame-de-paris': (1080, 1440),
 '2026-05-30-the-orphan-of-zhao': (1920, 1080),
 '2026-08-23-thomas-bergersen': (1440, 1080),
 '2026-09-24-french-musical-gala': (1920, 1080),
 '2026-10-23-hamlet': (1920, 1080),
 '2025-11-18-xu-guangqi-matteo-ricci': (1080, 1080)}

def article_attributes(slug):
    _, desktop, mobile = COVERS[slug]
    return f'data-article="{escape(slug)}" style="--cover-position: {desktop}; --cover-position-mobile: {mobile};"'

def hero_image(slug):
    source, _, _ = COVERS[slug]
    width, height = COVER_SIZES[slug]
    return f'<img class="article-backdrop" src="{source}" alt="" width="{width}" height="{height}" aria-hidden="true" fetchpriority="high" decoding="async">'
