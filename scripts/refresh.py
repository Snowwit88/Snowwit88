"""Refresh a public contribution animation and RSS/Atom article links. Stdlib only."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import date, datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import html, json, re, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def fetch(url):
    if urlparse(url).scheme != 'https':
        raise ValueError('Only HTTPS sources are supported')
    with urlopen(Request(url, headers={'User-Agent': 'Snowwit-Profile/1.0'}), timeout=30) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError('Source exceeds 2 MB')
    return data

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__(); self.days = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a and 'data-level' in a:
            d = date.fromisoformat(a['data-date']); level = int(a['data-level'])
            if not 0 <= level <= 4: raise ValueError('Invalid contribution level')
            self.days[d] = level

def parse_calendar(source):
    parser = Calendar(); parser.feed(source)
    if len(parser.days) < 300: raise ValueError('Incomplete contribution calendar; preserving previous image')
    return sorted(parser.days.items())

def make_snake(days):
    start = days[0][0]; cells = []
    for d, level in days:
        delta = (d-start).days
        cells.append((delta//7, delta%7, d, level))
    route = sorted(cells, key=lambda c:(c[0], c[1] if c[0]%2==0 else 6-c[1]))
    positions = {d:i for i,(_,_,d,_) in enumerate(route)}
    path = ' '.join(('M' if i==0 else 'L')+f'{35+x*17},{77+y*17}' for i,(x,y,_,_) in enumerate(route))
    path += f' L{35+route[-1][0]*17},201 L35,201 L35,77'
    out=['''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="235" viewBox="0 0 1000 235" role="img" aria-labelledby="title desc"><title id="title">Snowwit88 contribution snake</title><desc id="desc">A snake travels across the real public GitHub contribution calendar. Cell colors represent GitHub activity levels, not exact counts.</desc><style>.bg{fill:#f1f5f2}.label{fill:#476570}.c0{fill:#e0e8e3}.c1{fill:#accbc0}.c2{fill:#72aa9b}.c3{fill:#427e75}.c4{fill:#235850}.snake{fill:#b89250}
@media(prefers-color-scheme:dark){.bg{fill:#10232e}.label{fill:#a8c2c9}.c0{fill:#203642}.c1{fill:#335e60}.c2{fill:#4f8983}.c3{fill:#82b7a4}.c4{fill:#bad5ba}.snake{fill:#e2c68d}}
@media(prefers-reduced-motion:reduce){.snake,.eaten{display:none}}
</style><rect class="bg" width="1000" height="235" rx="16"/><g font-family="Arial, sans-serif" class="label"><text x="28" y="33" font-size="13" letter-spacing="2">SMALL STEPS, OVER TIME.</text>''']
    out.append(f'<text x="28" y="222" font-size="10">PUBLIC GITHUB ACTIVITY / {days[0][0]} — {days[-1][0]}</text></g>')
    for x,y,d,level in cells:
        out.append(f'<rect x="{29+x*17}" y="{71+y*17}" width="12" height="12" rx="3" class="c{level}"><title>{d}: activity level {level}</title></rect>')
        # Overlay fades active cells after the head visits them. The base remains in reduced-motion mode.
        if level:
            progress = positions[d]/(len(route)+16)
            p=max(.001,min(.95,progress)); q=min(.97,p+.008)
            out.append(f'<rect x="{29+x*17}" y="{71+y*17}" width="12" height="12" rx="3" class="bg eaten" opacity="0"><animate attributeName="opacity" values="0;0;.9;.9;0" keyTimes="0;{p:.4f};{q:.4f};.98;1" dur="42s" repeatCount="indefinite"/></rect>')
    for i in range(5,-1,-1):
        out.append(f'<circle class="snake" r="{5.7-i*.45:.2f}" opacity="{1-i*.12:.2f}"><animateMotion dur="42s" begin="{i*.11}s" calcMode="linear" repeatCount="indefinite" path="{path}"/></circle>')
    out.append('</svg>'); return ''.join(out)

def parse_feed(data):
    root=ET.fromstring(data)
    entries=root.findall('./channel/item') if root.tag=='rss' else root.findall('{http://www.w3.org/2005/Atom}entry')
    result=[]
    for entry in entries:
        atom='{http://www.w3.org/2005/Atom}' if entry.tag.startswith('{') else ''
        title=' '.join(''.join(entry.findtext(atom+'title', default='')).split())
        if atom:
            links=entry.findall(atom+'link')
            url=next((a.get('href','') for a in links if a.get('rel','alternate')=='alternate'),'')
        else: url=entry.findtext('link',default='').strip()
        if not title or urlparse(url).scheme not in ('https','http'): continue
        result.append((title,url))
        if len(result)==3: break
    if not result: raise ValueError('No usable feed articles; preserving previous links')
    return result

def articles_markup(entries):
    return '\n'.join(f'- <a href="{html.escape(url,quote=True)}">{html.escape(title)}</a>' for title,url in entries)

def main():
    config=json.loads((ROOT/'content/sources.json').read_text())
    account=config['github_username']
    if not re.fullmatch(r'[A-Za-z0-9-]+',account): raise ValueError('Invalid username')
    days=parse_calendar(fetch(f'https://github.com/users/{account}/contributions').decode())
    svg=make_snake(days); ET.fromstring(svg)
    (ROOT/'assets/contribution-snake.svg').write_text(svg)
    if config.get('feed_url'):
        block=articles_markup(parse_feed(fetch(config['feed_url'])))
        for filename in ['README.md','README.en.md']:
            p=ROOT/filename; text=p.read_text()
            text,n=re.subn(r'(?s)<!-- ARTICLES:START -->.*?<!-- ARTICLES:END -->',lambda _: '<!-- ARTICLES:START -->\n'+block+'\n<!-- ARTICLES:END -->',text)
            if n!=1: raise ValueError('Expected one article block')
            p.write_text(text)
        print('Updated article feed')
    else: print('No article source configured; labeled examples retained')
    print(f'Generated animation from {len(days)} public calendar days')

if __name__=='__main__': main()
