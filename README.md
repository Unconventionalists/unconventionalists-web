# Unconventionalists — website

Source for [unconventionalists.com](https://unconventionalists.com), the parent-company site.

- Single static page: `index.html` + `favicon.svg`. No build step, no dependencies.
- Served by GitHub Pages from the `main` branch. `CNAME` sets the custom domain.
- Fonts load from Google Fonts; everything else is inline.

To change the site, edit `index.html` and push to `main`. Pages redeploys in about a minute.


## Versions

- `index.html` — v2, live from 7 Oct 2026 (slate/butter/paper, Libre Caslon Text + Figtree, lift-off hero).
- `v1/` — the first site (olive/blueprint), kept for reference.
- `brand/` — marks, guidelines.

## Log

Entries live in `log/entries.json`. To add one:

    python3 scripts/add_entry.py "Title." "First paragraph." "Second paragraph." --about "Venture 01"
    git add -A && git commit -m "Log 003" && git push

`add_entry.py` appends the entry and runs `scripts/build_log.py`, which rewrites the Log section of `index.html` (latest three), `log/index.html` (every entry) and `log/feed.xml` (RSS). Dates default to today; pass `--date 2026-10-08` to override. Simple HTML (`<i>`, `<a>`) is allowed in titles and paragraphs. Nothing else needs touching; the site is live about a minute after the push.
