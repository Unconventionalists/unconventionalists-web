#!/usr/bin/env python3
"""Rebuild everything derived from log/entries.json:
  - the Log section in index.html (latest 3 entries, between <!-- log:start --> and <!-- log:end -->)
  - log/index.html (every entry)
  - log/feed.xml (RSS)
Run from the repo root: python3 scripts/build_log.py
"""
import json, re, html, datetime, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
entries = json.loads((ROOT / 'log/entries.json').read_text(encoding='utf-8'))
entries.sort(key=lambda e: e['n'], reverse=True)
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
def nice(d):
    y, m, dd = (int(x) for x in d.split('-'))
    return f"{dd} {MONTHS[m-1]} {y}"
def entry_html(e):
    body = ''.join(f"<p>{p}</p>" for p in e['body'])
    return (f'<li class="entry reveal" id="entry-{e["n"]:03d}"><div class="meta"><b>{e["n"]:03d}</b>{html.escape(e["about"])}<br>{nice(e["date"])}</div>'
            f'<div><h3>{e["title"]}</h3><div class="body">{body}</div></div></li>')
words = ['no','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve']
n = len(entries)
count = f"{words[n].capitalize() if n < len(words) else n} entr{'y' if n==1 else 'ies'} so far. The log updates when something happens, not on a schedule."

# 1. index.html
idx = ROOT / 'index.html'
s = idx.read_text(encoding='utf-8')
block = ('<!-- log:start -->\n    <ol class="entries" reversed>\n      ' + '\n      '.join(entry_html(e) for e in entries[:3]) +
         f'\n    </ol>\n    <p class="count reveal">{count} <a class="all" href="/log/">Every entry →</a></p>\n    <!-- log:end -->')
if '<!-- log:start -->' in s:
    s = re.sub(r'<!-- log:start -->.*?<!-- log:end -->', lambda m: block, s, flags=re.S)
else:
    s = re.sub(r'<ol class="entries" reversed>.*?</ol>\s*<p class="count reveal">.*?</p>', lambda m: block, s, flags=re.S)
idx.write_text(s, encoding='utf-8')

# 2. log/index.html
css = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
symbols = re.search(r'(<svg width="0" height="0".*?</svg>)', s, re.S).group(1)
def rehref(fragment):
    return re.sub(r'(<a\b[^>]*?href=")#', r'\1/#', fragment)
header = rehref(re.search(r'(<header class="top".*?</header>)', s, re.S).group(1)).replace('<a class="brand" href="/#"', '<a class="brand" href="/"')
footer = rehref(re.search(r'(<footer class="site-foot".*?</footer>)', s, re.S).group(1))
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Log — Unconventionalists</title>
<meta name="description" content="What happened at Unconventionalists, written down. Every entry, newest first.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="canonical" href="https://unconventionalists.com/log/">
<link rel="alternate" type="application/rss+xml" title="Unconventionalists log" href="/log/feed.xml">
<meta property="og:title" content="The Unconventionalists log"><meta property="og:description" content="What happened, written down."><meta property="og:image" content="https://unconventionalists.com/share.png">
<style>{css.replace("url(fonts/", "url(/fonts/")}
.logpage{{--bg:var(--paper);background:var(--paper);padding-block:clamp(3rem,7vw,5rem) clamp(4rem,9vw,7rem)}}
.logpage .sec-head h2{{margin-top:.6rem}}
.logpage .rss{{font-size:.85rem;color:var(--mute);margin-top:1.4rem}} .logpage .rss a{{border-bottom:1px solid currentColor}}
.reveal{{opacity:1;transform:none}}
</style>
</head>
<body>
{symbols}
{header}
<main>
<section class="logpage" id="log" aria-labelledby="h-log">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow"><span class="num" style="position:static;transform:none;width:auto;height:auto;border:0;background:none"><span>Log</span></span></p><h2 id="h-log">What happened, written down.</h2></div>
    <ol class="entries" reversed>
      {''.join(entry_html(e) for e in entries)}
    </ol>
    <p class="rss">{count} <a href="/log/feed.xml">RSS</a> · <a href="/">Back to the site</a></p>
  </div>
</section>
</main>
{footer}
</body>
</html>
'''
(ROOT / 'log/index.html').write_text(page, encoding='utf-8')

# 3. RSS
def rfc822(d):
    return datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%a, %d %b %Y 09:00:00 +0000')
items = ''.join(f'''
  <item>
    <title>{html.escape(re.sub('<[^>]+>','',e['title']))}</title>
    <link>https://unconventionalists.com/log/#entry-{e['n']:03d}</link>
    <guid isPermaLink="true">https://unconventionalists.com/log/#entry-{e['n']:03d}</guid>
    <pubDate>{rfc822(e['date'])}</pubDate>
    <description>{html.escape(''.join(f'<p>{p}</p>' for p in e['body']))}</description>
  </item>''' for e in entries)
rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Unconventionalists log</title>
  <link>https://unconventionalists.com/log/</link>
  <description>What happened, written down.</description>
  <language>en-gb</language>{items}
</channel></rss>
'''
(ROOT / 'log/feed.xml').write_text(rss, encoding='utf-8')
print(f"built: {n} entries → index.html (latest 3), log/index.html, log/feed.xml")
