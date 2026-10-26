"""Inspect the imported bilingual notes in Chromium at four viewport widths."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from theatre_notes_content import EVENTS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews/theatre-archive-20261024'
OUT.mkdir(exist_ok=True)

routes = [] if '--details-only' in sys.argv else ['index.cn.html', 'index.html', 'notes/index.cn.html', 'notes/index.html']
routes += [f'notes/{e["slug"]}/{name}' for e in EVENTS for name in ('cn.html', 'index.html')]
report = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', headless=True, args=['--disable-gpu', '--disable-crash-reporter'])
    page = browser.new_page()
    page.emulate_media(reduced_motion='reduce')
    for route in routes:
        for width in (320, 390, 856, 1440):
            page.set_viewport_size({'width': width, 'height': 1000 if width > 760 else 844})
            page.goto((ROOT / route).as_uri(), wait_until='load', timeout=45000)
            page.evaluate('() => document.fonts.ready')
            # Lazy images must be fetched before asserting their natural dimensions.
            page.locator('img').evaluate_all("images => images.forEach(image => image.loading = 'eager')")
            page.wait_for_function("() => [...document.images].every(image => image.complete)", timeout=20000)
            page.evaluate("() => Promise.all([...document.querySelectorAll('img[src]')].map(image => image.decode()))")
            result = page.evaluate('''() => ({
                width: innerWidth,
                scroll: document.documentElement.scrollWidth,
                broken: [...document.querySelectorAll('img[src]')].filter(i => !i.naturalWidth).map(i => i.getAttribute('src')),
                sticky: getComputedStyle(document.querySelector('.site-header')).position,
                photoCount: document.querySelectorAll('[data-lightbox]').length,
                photoFrames: [...document.querySelectorAll('[data-lightbox] img')].map(image => {
                    const box = image.getBoundingClientRect();
                    const frame = image.closest('[data-lightbox]').getBoundingClientRect();
                    return {square: Math.abs(box.width-box.height) < 1,
                        contained: box.top >= frame.top-1 && box.left >= frame.left-1 && box.bottom <= frame.bottom+1 && box.right <= frame.right+1,
                        fit: getComputedStyle(image).objectFit};
                }),
                activeSection: document.querySelector('.site-nav a[aria-current="page"]').textContent,
                fontLoaded: document.fonts.check('20px "LXGW WenKai Display"')
            })''')
            assert result['scroll'] <= width + 1, (route, width, result)
            assert not result['broken'], (route, width, result)
            assert result['sticky'] == 'sticky'
            if route.endswith('cn.html'):
                assert result['fontLoaded'], (route, width, 'Chinese title font not loaded')
            if route.startswith('notes/'):
                assert result['activeSection'] in ('Notes', '札记'), (route, width, 'Wrong active section')
            if '/202' in route:
                expected = next(len(e['alts']) for e in EVENTS if e['slug'] in route)
                assert result['photoCount'] == expected
                assert all(frame['square'] and frame['contained'] and frame['fit'] == 'contain' for frame in result['photoFrames']), (route, width, result['photoFrames'])
            if 'phantom' in route:
                page.locator('.note-reading-guide summary').click()
                assert page.locator('.note-reading-guide').get_attribute('open') is not None
                page.locator('.note-contents a').nth(3).click()
                target = page.locator('#part-16').bounding_box()
                header = page.locator('.site-header').bounding_box()
                assert header['height'] <= target['y'] < page.viewport_size['height'], (route, width, 'Anchor obscured or offscreen')
                trigger = page.locator('[data-lightbox]').nth(4)
                trigger.focus()
                page.keyboard.press('Enter')
                assert page.locator('dialog.lightbox').evaluate('el => el.open')
                page.keyboard.press('Escape')
                assert not page.locator('dialog.lightbox').evaluate('el => el.open')
                assert trigger.evaluate('el => el === document.activeElement')
                page.locator('.note-reading-guide summary').click()
            if width in (390, 1440) and (route in ('notes/index.cn.html', 'notes/index.html') or 'phantom' in route):
                page.evaluate('scrollTo(0,0)')
                page.screenshot(path=OUT / (route.replace('/', '-').replace('.html', '') + f'-{width}.png'))
            if 'phantom' in route and route.endswith('cn.html') and width == 1440:
                page.locator('.note-subheading').first.scroll_into_view_if_needed()
                page.screenshot(path=OUT / 'phantom-cn-reading-final.png')
            if 'romeo' in route and route.endswith('cn.html') and width == 390:
                page.locator('.note-photo-row--two').screenshot(path=OUT / 'romeo-two-photos-final.png')
            report.append({'route': route, 'viewport': width, **result})
        print(route, 'OK at 320, 390, 856 and 1440px', flush=True)
    # Check one short note’s two-photo row and language destination.
    page.goto((ROOT / 'notes/2025-12-19-romeo-et-juliette/cn.html').as_uri(), wait_until='load')
    assert page.locator('.note-photo-row--two a').count() == 2
    page.locator('.language-switch a').click()
    assert page.url.endswith('/notes/2025-12-19-romeo-et-juliette/index.html')
    browser.close()

(OUT / 'browser-checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(f'{len(report)} page/viewport checks; Phantom anchors, reading guide, keyboard lightbox and focus restoration; language switch OK.')
