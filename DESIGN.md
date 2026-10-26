# Xiao Site V2 — Design Direction

## Status

`PUBLIC EDITION — approved for publication by the maintainer on 26 October 2026`

This document is the visual contract for the published site. It does not redefine Xiaoxiao; she remains the final owner of the public identity.

## Subject, audience, job

- **Subject:** a young writer who moves among the page, the auditorium, and the ensemble.
- **Primary audience:** Xiaoxiao, family, friends and readers of her writing.
- **Single job of the homepage:** make the visitor want to read one real piece of writing.

## North Star

> **Aperture / 幕缝**

The site opens through one narrow field of light. It may read as a theatre curtain opening, the gutter of a book, or the gap between explanation and experience. It is the only theatrical gesture allowed to dominate the interface.

The rest of the site is quiet editorial space. The design must not become a theatre-themed template.

## Anti-references

- no fantasy maps, coordinates, score lines, decorative paths, stars, fog, or particles;
- no split oversized `Xiao / xiao` fashion-magazine gimmick;
- no rotating quotations;
- no trophy wall or application language;
- no equal card grid for every piece of writing;
- no second “design lab” navigation above the real website;
- no placeholder page presented as a finished section.

## Tokens

| Token | Value | Role |
|---|---:|---|
| Night | `#11131B` | Hero and concert ground |
| Warm ivory | `#F5F0E6` | Reading ground; a restrained trace of yellow, never green |
| Ink | `#191A1E` | Body text on Bone |
| Moon | `#AEB7C6` | Secondary text on Night |
| Cue | `#B93C2F` | One cue light, focus and active states |
| Cue Bright | `#D96B60` | Small cue-coloured text on Night only |
| Haze | `#DCD2C2` | Rules and quiet surfaces |

The Cue colour is intentionally scarce. Cue Bright exists only to keep small red text accessible on Night. Neither may become a broad red-and-black “luxury theatre” treatment.

## Typography

- **English display:** Italiana — restrained, high-contrast, used for titles only.
- **Chinese literary display:** a self-hosted Zhuque Fangsong 400 subset for the homepage writing line, section titles, work titles and navigation. The current preview-release subset is retained for this approved edition; its SIL OFL notice is bundled in fonts/.
- **Chinese note display:** a self-hosted LXGW WenKai 400 subset for the concert-note titles, with restrained sizing and unbroken semantic lines.
- **English reading:** Source Serif 4 — optical-size-aware long-form text.
- **Chinese reading:** Noto Serif SC — generous line-height and stable mixed-script rhythm.
- **Utility:** IBM Plex Sans — navigation, metadata and captions.

Chinese pages are edited as complete Chinese editions rather than partially translated skins. Interface labels, section eyebrows, titles and descriptive copy use Chinese; Latin text remains only where it is the proper form of a person, work, brand, technical abbreviation, source quotation or bibliography entry. Decorative English is not retained merely for atmosphere.

The navigation uses the supplied `logo-main.webp` script-and-pen wordmark. Because the wordmark already carries ornament, page titles remain disciplined rather than competing with it.

## Layout

### Home

```text
┌──────────────────────────────────────────────┐
│ wordmark        Works Notes Stage About  EN │
├───────────────────────────┬──────────────────┤
│ one fixed line of writing │ image aperture   │
│ context + enter           │ opens once       │
├───────────────────────────┴──────────────────┤
│ featured work: image / title / real context │
├──────────────────────────────────────────────┤
│ three recent works + full archive link     │
├───────────────────────┬──────────────────────┤
│ real concert note     │ real photographs     │
├───────────────────────┴──────────────────────┤
│ Stage record                              │
│ About archive                             │
└──────────────────────────────────────────────┘
```

### Long-form

- title and context sit beside one restrained image;
- reading measure is 780–800 px for the long essay, with narrower mobile padding preserved;
- marginal notes move into the reading flow on narrow screens;
- illustrations are not mandatory decoration.

### Photo note

- the original register remains intact;
- Notes is a chronological index of distinct attended events, not a shortcut to one concert;
- each event retains its own bilingual folder and one image-led page;
- this concert note presents its nine supplied photographs as three equal rows of three, placed between the original post's paragraphs rather than in the title area or a separate album;
- all nine occupy equal square cells and open the full original in the lightbox; type-bearing photographs fit wholly inside their cells, while stage photographs may use a square preview crop;
- the three-by-three grid is a deliberate response to this WeChat-origin note, not an automatic rule for every future event.

## Signature interaction

On first load, the hero image aperture opens once. It then stays still. Under `prefers-reduced-motion`, it is fully open from the beginning.

No other major motion competes with reading.

Images on the homepage and Works index are navigational: they open the corresponding work or note, as do work titles. Only images inside a full work or note open the restrained modal lightbox. The overlay supports pointer and keyboard activation, Escape/backdrop dismissal, and focus restoration.

English is the canonical route without a language suffix. Chinese uses `index.cn.html` at section roots and `cn.html` inside a content folder. The wordmark is an unlinked identity mark; Home is an explicit navigation item. The current section is identified by both `aria-current` and a visible underline, including while reading an individual work or note.

## Content rules

- Works, Notes and Stage remain distinct editorial speeds.
- Awards appear only as context attached to a work.
- Stage records experiences, roles and programmes, not certificate counts.
- About cannot impersonate Xiaoxiao’s first-person voice.
- Publish only content explicitly approved by the maintainer; the current edition has been approved for publication in this task.
- Works are ordered by their stated publication month, newest first; dates never imply an unknown day or announcement date.

## Accessibility and stability

- WCAG 2.2 AA contrast target;
- native links and buttons;
- visible keyboard focus in Cue red with offset;
- minimum practical touch targets in compact navigation;
- image dimensions declared;
- responsive navigation remains usable without hover;
- no essential information depends on motion or imagery.

## Reading refinement — 8 September 2026

Runtime values live in `styles.css`. Preserve Night, warm ivory and the supplied wordmark. Reserve Italiana for English opening titles; Chinese literary titles and navigation use Zhuque Fangsong, concert-note titles use LXGW WenKai, and long-form Chinese body copy remains in Noto Serif SC. Chinese essay text is 18px with 1.95 line-height and an 800px maximum reading measure; section headings are 24–32px with 1.4 line-height. Chinese title phrases must remain intact, with no orphaned characters. Image positioning keeps rafflesia visible. Mobile openings use content height, not viewport-sized empty space.

Catalogue rows share a compact left-image alignment. The concert note retains all source material, with paragraph breaks for reading. Its nine photographs share one grid without a secondary tier; the full originals remain available in the lightbox. Emoji labels remain unbroken. Editorial planning notes belong in this document, not in reader-facing prose. Titles and translations remain provisional for Xiaoxiao to review.

## Notes architecture — 23 September 2026

The homepage may feature one event, but the Notes navigation leads to `notes/index.html` or `notes/index.cn.html`. The index is chronological and contains only real supplied events. Each event detail keeps Notes visibly active, offers a return to the index, and reserves the lightbox for detail-page photographs. A title must survive intermediate viewport widths without forced line breaks or single-character wrapping. The Chinese concert note preserves Xiaoxiao's original code-switching and wording; editorial paragraph breaks do not authorize rewriting her voice. English is an edited translation and is labelled accordingly.

## Homepage catalogue structure — 27 September 2026

Works and Notes both use a section heading, the latest featured item and three further catalogue rows, showing the four most recent entries. Each section ends with a full-width “View all” link, the complete archive count and an arrow. The independent indexes retain every entry with its image, date and summary. This compact homepage preview supersedes the earlier complete homepage catalogue.

## Nine-photo note layout — 23 September 2026

The nine photos in the Thomas Bergersen note form three equal rows of three between paragraphs on desktop and mobile. The rows let the concert be seen while her account unfolds, and a pale mat keeps the dark stage photographs connected to the ivory reading surface. No photo is assigned to a smaller "more photos" tier. Every cell is a link to its original image, enhanced into the existing lightbox when JavaScript is available. Previews are square and deliberately compact; poster, programme, and text-bearing portrait use `contain` inside the square, while stage photographs use square cover crops only in the preview.

## English copy, note titles and navigation — 24 October 2026

English pages use English for visible copy and interface labels. Use a verifiable English name or romanization for proper nouns; retain Han characters only when no reliable equivalent exists. After adding a note, verify the LXGW WenKai subset covers its titles on the homepage, Notes index and detail page, then inspect them in a browser. The site header remains visible while scrolling, with offset for anchor targets.

## Stage record — 24 October 2026

Stage opens with the school production of Xu Guangqi and Matteo Ricci. The director’s note has separate Chinese and English pages. The Chinese page preserves the original post and its language mixing; the English page reads as a complete English translation. On both pages, all nine photo collages appear in three groups between paragraphs and open in the lightbox. Stage and About occupy separate homepage sections. The language control uses equal-width options with a centered divider.

## Historical Notes intake — 24 October 2026

Notes contains nine real records in reverse date order. The original-cast Notre-Dame de Paris reunion is explicitly a screen viewing, not a theatre visit. Dates follow the supplied archive folders as dates of record. Every supplied image remains in its original sequence, and collages fit wholly inside their previews. Incomplete photo sets use their actual count; the five-photo Roméo et Juliette note uses groups of three and two.

The West End Phantom note was originally written mostly in English. Its English edition preserves that prose and translates the Chinese introduction; its Chinese edition is a complete translation. Six section anchors and a clearly separate, collapsible reading guide make the long note approachable. Preserve every source paragraph and her exuberant tone; section headings are reading aids, not additional first-person claims. Homepage Notes retains the latest featured note plus three recent links; the complete index holds every record. Rebuild the existing WenKai subset for new titles so homepage, index and detail titles use the same face.

## Illustrated article openings and viewer — 25 October 2026

Works and Notes detail pages open with a relevant existing image behind the title and context. The shared composition is static and responsive: desktop uses an approximately 58svh opening with content-driven growth, and mobile uses a 400px minimum with natural growth for long bilingual titles. Individual images have explicit desktop/mobile focal positions. Directional dark overlays preserve title and metadata contrast. Avoid a mandatory near-full-screen opening or scroll-driven effects.

For Works, the former standalone opening cover is integrated into this header rather than immediately repeated below it. A localized View cover link retains original-image navigation without JavaScript and opens the same image viewer when available; the cover remains the first gallery item. All other illustrations retain their original markup, dimensions, order and figure layout. Notes backgrounds are decorative; every original photo remains in its existing square preview and paragraph-separated group, with its original fit rule.

The 800px Works reading measure and existing Notes reading measure are retained. Works keep their serif reading fonts. Notes body text uses IBM Plex Sans with Noto Sans SC for Chinese, retaining the existing font size and line height. Chinese Notes titles remain LXGW WenKai consistently across homepage, catalogue and detail pages. Stage typography is unchanged.

Each article has a paired accent for ivory and dark backgrounds, drawn from its imagery. Apply it only to existing title rules, metadata, chapter headings, epigraph markers, drop caps and lyric borders. Do not tint the paper, ordinary paragraphs, global navigation or photograph mats. Runtime palette ownership is styles.css [data-article] rules; image/focal-position ownership is scripts/article_presentation.py, shared with the archive generator. Both language editions use the same image, focal positions and accent.

The shared native-dialog viewer supports previous/next, arrow keys, image count, original-size/fit toggle, captions, loading and image-error feedback, Escape/backdrop dismissal and trigger focus restoration. It never rearranges or resizes inline images. Original-size images are scrollable in both axes; changing image resets fit. Background header images are excluded from Notes galleries. Every inline photo and the Works cover retain a normal original-image link as progressive fallback. Lock document scrolling only while the viewer is open and compensate for an actual scrollbar gap without changing normal page geometry.

## Width hierarchy and quotations — 26 October 2026

The pre-existing width hierarchy remains: a centered 1440px outer frame with internal page padding, an 800px long-form text measure, and body illustrations up to 980px. The homepage opening image deliberately reaches the viewport edge while its copy aligns with the centered content grid. Article background covers are also full bleed. These exceptions express the opening image; they do not imply overflow in reading or index content.

Works share one compact epigraph/pull-quote component. Keep quotes within the text measure, use bounded pixel spacing rather than large font-relative margins, and separate source citations into small utility type. An opening epigraph has no extra top margin beyond the prose section padding. This refines the original style, whose large inherited citation font and 3.4em/3.2em margins made The Eighth Rank opening excessively tall. Use the same component for existing interior pull quotes; do not invent quotations or force the same content structure onto every work.

## Works end navigation and footer — 26 October 2026

The reading sequence follows the Works catalogue order (newest first). Left is Previous work, right is Next work, paired across both language editions and labelled with the adjacent title. Use rel=prev/next. At either boundary, retain the empty direction as a clearly labelled static first/last state; do not loop or insert an archive link in its place. The sticky primary Works navigation remains the archive entry.

Keep the dark end-navigation background full width, with an inner 1440px centered frame and the same page padding as the copyright row. Use two equal columns even on mobile, allowing long titles to wrap. End navigation grows with content instead of imposing a 230px minimum. Works detail and catalogue footers use a compact 64px minimum, copyright on the left; remove genre/complete-text badges from detail footers. Notes and Stage also use this compact copyright layout, as specified below.

## Shared reading boundaries and section footers — 26 October 2026

Works, Notes and Stage use the same static end-navigation renderer in scripts/reading_navigation.py, reading each section's existing catalogue order (newest first). Both equal-width columns are always present. Real adjacent items are links with rel=prev/next; the first item's previous slot and last item's next slot are non-focusable divs marked aria-disabled=true, with explicit first/last copy, quieter utility type and a thin top rule. Never make these states fake links or buttons. Chinese Notes neighbour titles use the same WenKai subset as their other title surfaces; boundary status text uses the complete utility font.

Notes details replace the old All notes return row with this navigation, after main content. Keep all original prose and photo grouping/sizes intact. All Works, Notes and Stage footers, including their catalogues, contain only copyright on the left and use the compact 64px baseline. Remove Back home links in both languages. Stage uses the same adjacent-reading navigation; its old return-to-Stage row is removed. The theatre-note generator calls the shared renderer so later regeneration retains this behaviour.

## Stage opening and bookend ornament — 26 October 2026

Stage details join the shared responsive article opening and adjacent-reading renderer. The Xu Guangqi/Matteo Ricci director's note uses stage-08.webp, the curtain-call portrait collage, with a lavender accent and independently selected desktop/mobile focus. The nine inline collages and Stage's serif reading typography remain unchanged. The decorative header image is excluded from the nine-image viewer. Remove the in-content Back to Stage link.

The navigation renderer supports Works, Notes and Stage. A single Stage entry displays both first and last states, reserving both directions without fake links. Existing boundary slots retain explicit first/last status and muted typography, with a restrained floral fleuron and bookend word above it. English uses Beginning / Finis (Latin for end); Chinese uses 开篇 / 终篇. Decorative marks are aria-hidden; the actual status remains readable and non-focusable. Do not add a new font download for this ornament.
