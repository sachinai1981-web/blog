#!/usr/bin/env python3
"""Convert Obsidian markdown notes from obsidian/ to blog HTML posts in posts/.

Only processes notes with status: published in their frontmatter.
Run directly or let .github/workflows/obsidian-publish.yml do it on push.
"""

import re
import sys
import json
import html as html_lib
import yaml
import markdown as md_lib
from datetime import datetime, date
from pathlib import Path

REPO_ROOT    = Path(__file__).parent.parent
OBSIDIAN_DIR = REPO_ROOT / 'obsidian'
POSTS_DIR    = REPO_ROOT / 'posts'
TEMPLATE    = Path(__file__).parent / 'post_template.html'

DEFAULT_HERO = (
    'https://images.unsplash.com/photo-1620712943543-bcc4688e7485'
    '?w=1800&q=90&auto=format&fit=crop'
)


def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    return re.sub(r'[\s_]+', '-', text)


def fmt_display(d):
    if isinstance(d, (datetime, date)):
        return d.strftime('%b %-d, %Y')
    try:
        return datetime.fromisoformat(str(d)).strftime('%b %-d, %Y')
    except Exception:
        return str(d)


def fmt_iso(d):
    if isinstance(d, date):
        return d.isoformat()
    return str(d)


def load_note(path):
    text = Path(path).read_text(encoding='utf-8')
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            return meta, parts[2].strip()
    return {}, text.strip()


def convert_body(text):
    converter = md_lib.Markdown(extensions=['tables', 'fenced_code'])
    html = converter.convert(text)
    html = html.replace('<blockquote>', '<div class="callout">').replace('</blockquote>', '</div>')
    return html


def add_heading_ids(html):
    headings = []

    def repl(m):
        tag, content = m.group(1), m.group(2)
        text = re.sub(r'<[^>]+>', '', content)
        hid = slugify(text)
        headings.append({'id': hid, 'text': text})
        return f'<{tag} id="{hid}">{content}</{tag}>'

    html = re.sub(r'<(h[23])>(.*?)</\1>', repl, html, flags=re.DOTALL)
    return html, headings


def build_toc(headings):
    if not headings:
        return ''
    items = '\n'.join(
        f'            <li><a href="#{h["id"]}">{html_lib.escape(h["text"])}</a></li>'
        for h in headings
    )
    return (
        '        <aside class="article-toc">\n'
        '          <p class="article-toc__label">Contents</p>\n'
        '          <ul class="article-toc__list">\n'
        + items + '\n'
        + '          </ul>\n'
        + '        </aside>'
    )


def build_related(related_list):
    if not related_list:
        return ''
    cards = ''
    for r in related_list:
        cards += (
            f'            <a class="related-post-card" href="/posts/{r["slug"]}.html">\n'
            f'              <img class="related-post-card__image" src="{r["image"]}" alt="" loading="lazy">\n'
            '              <div class="related-post-card__body">\n'
            f'                <p class="related-post-card__category">{html_lib.escape(r.get("category", "Essay"))}</p>\n'
            f'                <p class="related-post-card__title">{html_lib.escape(r["title"])}</p>\n'
            '              </div>\n'
            '            </a>\n'
        )
    return (
        '        <div class="related-posts">\n'
        '          <p class="related-posts__label">Read next</p>\n'
        '          <div class="related-posts__grid">\n'
        + cards
        + '          </div>\n'
        + '        </div>'
    )


def build_ldjson(meta, slug, date_iso, og_img):
    data = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        'headline': meta.get('title', ''),
        'url': f'https://sachinai.com/posts/{slug}.html',
        'datePublished': date_iso,
        'dateModified': date_iso,
        'author': {'@type': 'Person', 'name': 'Sachin Rai', 'url': 'https://sachinai.com/'},
        'publisher': {'@type': 'Person', 'name': 'Sachin Rai', 'url': 'https://sachinai.com/'},
        'description': meta.get('description', ''),
        'image': og_img,
        'keywords': meta.get('keywords', []),
        'articleSection': meta.get('category', 'Essay'),
    }
    return f'<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>'


def render_post(meta, body):
    template = TEMPLATE.read_text(encoding='utf-8')

    title    = meta.get('title', 'Untitled')
    desc     = meta.get('description', '')
    slug     = meta['slug']
    date_val = meta.get('date', datetime.today().date())
    date_iso = fmt_iso(date_val)
    date_disp = fmt_display(date_val)
    category = meta.get('category', 'Essay')
    read_time = meta.get('read_time', '5 min read')
    hero     = meta.get('hero_image') or DEFAULT_HERO
    image2   = meta.get('image2') or hero
    image3   = meta.get('image3') or hero
    og_img   = meta.get('og_image') or hero.replace('w=1800', 'w=1200')

    body_html, headings = add_heading_ids(convert_body(body))

    e = html_lib.escape
    return (
        template
        .replace('__TITLE__',         e(title, quote=True))
        .replace('__DESCRIPTION__',   e(desc,  quote=True))
        .replace('__SLUG__',          slug)
        .replace('__DATE_ISO__',      date_iso)
        .replace('__DATE_DISPLAY__',  date_disp)
        .replace('__READ_TIME__',     read_time)
        .replace('__CATEGORY__',      e(category))
        .replace('__HERO_IMAGE__',    hero)
        .replace('__IMAGE2__',        image2)
        .replace('__IMAGE3__',        image3)
        .replace('__OG_IMAGE__',      og_img)
        .replace('__LDJSON__',        build_ldjson(meta, slug, date_iso, og_img))
        .replace('__TOC__',           build_toc(headings))
        .replace('__ARTICLE_BODY__',  body_html)
        .replace('__RELATED_POSTS__', build_related(meta.get('related', [])))
    )


def main():
    if not OBSIDIAN_DIR.exists():
        print(f'obsidian/ not found at {OBSIDIAN_DIR}')
        sys.exit(0)

    published = skipped = 0

    for md_file in sorted(OBSIDIAN_DIR.glob('*.md')):
        if md_file.name.startswith('_') or md_file.name == 'TEMPLATE.md':
            continue

        meta, body = load_note(md_file)

        if meta.get('status') != 'published':
            print(f'  skip  {md_file.name} (status: {meta.get("status", "draft")})')
            skipped += 1
            continue

        if not meta.get('slug'):
            meta['slug'] = slugify(meta.get('title', md_file.stem))

        html = render_post(meta, body)
        out_path = POSTS_DIR / f'{meta["slug"]}.html'
        out_path.write_text(html, encoding='utf-8')
        print(f'  wrote {out_path}')
        published += 1

    print(f'\nDone. Published: {published}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
