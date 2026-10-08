#!/usr/bin/env python3
"""Add a log entry and rebuild.
  python3 scripts/add_entry.py "Title." "First paragraph." ["Second paragraph." ...] [--about "Venture 01"] [--date 2026-10-08]
Title and paragraphs may contain simple HTML (<i>, <a>). Then: git add -A && git commit -m "Log 003" && git push
"""
import json, sys, datetime, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent
args = sys.argv[1:]
about, date = 'Unconventionalists', datetime.date.today().isoformat()
if '--about' in args: i = args.index('--about'); about = args[i+1]; del args[i:i+2]
if '--date' in args: i = args.index('--date'); date = args[i+1]; del args[i:i+2]
if len(args) < 2: sys.exit(__doc__)
path = ROOT / 'log/entries.json'
entries = json.loads(path.read_text(encoding='utf-8'))
n = max(e['n'] for e in entries) + 1 if entries else 1
entries.append({'n': n, 'date': date, 'about': about, 'title': args[0], 'body': args[1:]})
path.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f"added entry {n:03d}: {args[0]}")
subprocess.run([sys.executable, str(ROOT / 'scripts/build_log.py')], check=True)
