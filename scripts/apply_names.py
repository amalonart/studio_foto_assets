#!/usr/bin/env python3
"""Apply name.md files: rename photos, update altText.ts / slideFocus.ts, archive name.md.

name.md lives in a prefix dir (assets/start/, assets/portfolio/, assets/gallery/<folder>/).
Row: `old_name | new_name.webp | Alt text [| focus]` (focus only for start/, e.g. `30% 50%`).
Blank lines and lines starting with `#` are ignored. Only files named exactly `name.md`
are processed; archived `name_<timestamp>.md` are skipped.

Usage: python3 scripts/apply_names.py [assets_dir]   (default: assets)
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_FOCUS = '50% 50%'
THUMB_DIRS = ('thumbs', 'thumbial')
NEW_NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*\.webp$')
FOCUS_RE = re.compile(r'^\d{1,3}% \d{1,3}%$')


def image_dirs(prefix_dir: Path) -> list[Path]:
    full = prefix_dir / 'full'
    if not full.is_dir():
        return [prefix_dir]
    return [full] + [prefix_dir / t for t in THUMB_DIRS if (prefix_dir / t).is_dir()]


def clean_alt(alt: str) -> str:
    return alt.strip().replace("'", '’').rstrip('.').strip()


def parse(name_md: Path, assets: Path, errors: list[str]) -> list[dict]:
    prefix_dir = name_md.parent
    prefix = prefix_dir.relative_to(assets).as_posix() + '/'
    is_start = prefix == 'start/'
    dirs = image_dirs(prefix_dir)
    rows, seen = [], set()
    for no, line in enumerate(name_md.read_text(encoding='utf-8').splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        where = f'{name_md}:{no}'
        cols = [c.strip() for c in line.strip('|').split('|')]
        if len(cols) not in (3, 4):
            errors.append(f'{where}: expected 3 or 4 columns, got {len(cols)}')
            continue
        old, new, alt = cols[0], cols[1], clean_alt(cols[2])
        focus = cols[3] if len(cols) == 4 else None
        if not NEW_NAME_RE.match(new):
            errors.append(f'{where}: bad new name "{new}" (lowercase, a-z0-9 and "-", .webp)')
        if not alt:
            errors.append(f'{where}: empty alt text')
        if focus is not None and (not is_start or not FOCUS_RE.match(focus)):
            errors.append(f'{where}: focus "{focus}" allowed only for start/ as "NN% NN%"')
        target = Path(new).stem + Path(old).suffix
        if target in seen:
            errors.append(f'{where}: duplicate new name "{new}"')
        seen.add(target)
        for d in dirs:
            if not (d / old).is_file():
                errors.append(f'{where}: missing {d / old}')
            if target != old and (d / target).exists():
                errors.append(f'{where}: {d / target} already exists')
        rows.append(dict(old=old, target=target, key_old=Path(old).stem + '.webp',
                         key_new=Path(new).stem + '.webp', alt=alt, focus=focus,
                         prefix=prefix, dirs=dirs, is_start=is_start))
    return rows


def upsert(ts_file: Path, entries: list[tuple[str | None, str, str | None]]) -> None:
    """entries: (old_key, new_key, value). value None -> keep old value (or skip if absent)."""
    lines = ts_file.read_text(encoding='utf-8').split('\n')

    def find(key: str) -> int | None:
        start = f"    '{key}':"
        return next((i for i, l in enumerate(lines) if l.startswith(start)), None)

    for old_key, new_key, value in entries:
        old_i = find(old_key) if old_key and old_key != new_key else None
        if old_i is not None:
            if value is None:
                m = re.match(r"^    '[^']*': '(.*)',\s*$", lines[old_i])
                value = m.group(1) if m else None
            del lines[old_i]
        if value is None:
            continue
        line = f"    '{new_key}': '{value}',"
        i = find(new_key)
        if i is not None:
            lines[i] = line
        else:
            close = max(i for i, l in enumerate(lines) if l.startswith('}'))
            lines.insert(close, line)
    ts_file.write_text('\n'.join(lines), encoding='utf-8')


def main() -> int:
    assets = Path(sys.argv[1] if len(sys.argv) > 1 else 'assets')
    name_files = sorted(assets.rglob('name.md'))
    changed = bool(name_files)
    if not name_files:
        print('No name.md found, nothing to do.')
    else:
        errors: list[str] = []
        rows = [r for f in name_files for r in parse(f, assets, errors)]
        if errors:
            print('name.md errors, nothing changed:\n  ' + '\n  '.join(errors), file=sys.stderr)
            return 1
        for r in rows:
            for d in r['dirs']:
                if r['old'] != r['target']:
                    os.rename(d / r['old'], d / r['target'])
            print(f"{r['prefix']}{r['old']} -> {r['target']}")
        upsert(assets / 'altText.ts',
               [(r['prefix'] + r['key_old'], r['prefix'] + r['key_new'], r['alt']) for r in rows])
        start_rows = [r for r in rows if r['is_start']]
        if start_rows:
            focus_file = assets / 'slideFocus.ts'
            existing = focus_file.read_text(encoding='utf-8')
            entries = []
            for r in start_rows:
                if r['focus']:
                    value = r['focus']
                elif f"    '{r['key_old']}':" in existing or f"    '{r['key_new']}':" in existing:
                    value = None  # keep current focus (moved to new key if renamed)
                else:
                    value = DEFAULT_FOCUS
                entries.append((r['key_old'], r['key_new'], value))
            upsert(focus_file, entries)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
        for f in name_files:
            f.rename(f.with_name(f'name_{stamp}.md'))
            print(f'archived {f} -> name_{stamp}.md')
    out = os.environ.get('GITHUB_OUTPUT')
    if out:
        with open(out, 'a', encoding='utf-8') as fh:
            fh.write(f"changed={'true' if changed else 'false'}\n")
    return 0


if __name__ == '__main__':
    sys.exit(main())
