"""Check built local links, media, anchors and explicitly excluded pages."""
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for attr in ('href', 'src', 'poster'):
            if attrs.get(attr):
                self.links.append(attrs[attr])

pages = {p.resolve(): Page(p) for p in SITE.rglob('*.html')}
errors = []
checks = 0
for path, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (SITE / unquote(url.path).lstrip('/') if url.path.startswith('/')
                  else path.parent / unquote(url.path) if url.path else path).resolve()
        if target.is_dir():
            target /= 'index.html'
        checks += 1
        if not target.exists():
            errors.append(f'{path.relative_to(SITE)}: missing {link}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{path.relative_to(SITE)}: missing anchor {link}')

config = tomllib.loads((ROOT / 'zensical.toml').read_text(encoding='utf-8'))
for pattern in config['project'].get('exclude_docs', '').splitlines():
    # Check exact Markdown exclusions; wildcard patterns are handled by Zensical.
    destination = pattern.strip().lstrip('/')
    if not destination.endswith('.md') or any(c in destination for c in '*?!['):
        continue
    stem = Path(destination).with_suffix('')
    target = SITE / ('index.html' if destination == 'index.md' else str(stem / 'index.html'))
    if target.exists():
        errors.append(f'Excluded page still built: {destination}')
if not pages:
    errors.append('No built pages found. Run zensical build first.')
print(f'Checked {len(pages)} HTML pages and {checks} local references.')
for error in sorted(set(errors)):
    print(error)
raise SystemExit(1 if errors else 0)
