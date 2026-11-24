#!/usr/bin/env python3
"""Apply name.md files: rename photos, update altText.ts / slideFocus.ts, archive name.md.

name.md lives in a prefix dir (assets/start/, assets/portfolio/, assets/gallery/<folder>/).
Photos are renamed where they are: in the prefix (main) dir, where new uploads go (CI
convert-images.sh later copies them to full/ + thumbial/), or, if not there, in full/ +
thumbial/ (renaming already published photos). start/ has no subdirs.
Row: `old_name | new_name.webp | Alt text [| focus]` (focus only for start/, e.g. `30% 50%`).
old_name lookup per dir: exact, else same name any case, else `<old stem>.webp` any case
(e.g. `IMG4240.JPG` finds `IMG4240.JPG`, `img4240.jpg`, `IMG4240.webp`, `img4240.WEBP`).
Renamed file keeps its actual extension.
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
THUMB_DIRS = ('thumbial',)
NEW_NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*\.webp$')
FOCUS_RE = re.compile(r'^\d{1,3}% \d{1,3}%$')


def resolve(d: Path, old: str) -> str | list[str] | None:
    """Actual file name in d for `old`: exact, else same name any case, else `<stem>.webp`
    any case. Returns name, None (not found) or list of candidates (ambiguous)."""
    if (d / old).is_file():
        return old
    if not d.is_dir():
        return None
    files = [p.name for p in d.iterdir() if p.is_file()]
    webp = (Path(old).stem + '.webp').lower()
    for want in (old.lower(), webp):
        hits = sorted(f for f in files if f.lower() == want)
        if hits:
            return hits[0] if len(hits) == 1 else hits
    return None


def image_dirs(prefix_dir: Path, old: str) -> list[Path]:
    """Main (upload) dir if the photo is there, else full/ + thumbial/ (published photo)."""
    full = prefix_dir / 'full'
    if resolve(prefix_dir, old) is not None or not full.is_dir():
        return [prefix_dir]
    return [full] + [prefix_dir / t for t in THUMB_DIRS if (prefix_dir / t).is_dir()]


def clean_alt(alt: str) -> str:
    return alt.strip().replace("'", '’').rstrip('.').strip()


def parse(name_md: Path, assets: Path, errors: list[str]) -> list[dict]:
    prefix_dir = name_md.parent
    prefix = prefix_dir.relative_to(assets).as_posix() + '/'
    is_start = prefix == 'start/'
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
        new_stem = Path(new).stem
        if new_stem in seen:
            errors.append(f'{where}: duplicate new name "{new}"')
        seen.add(new_stem)
        moves = []  # (dir, actual old name, target name)
        for d in image_dirs(prefix_dir, old):
            actual = resolve(d, old)
            if actual is None:
                errors.append(f'{where}: missing {d / old} (or {Path(old).stem}.webp, any case)')
                continue
            if isinstance(actual, list):
                errors.append(f'{where}: ambiguous {d / old}: {", ".join(actual)}')
                continue
            target = new_stem + Path(actual).suffix
            if target != actual and (d / target).exists():
                errors.append(f'{where}: {d / target} already exists')
            moves.append((d, actual, target))
        key_old = Path(moves[0][1] if moves else old).stem + '.webp'
        rows.append(dict(moves=moves, key_old=key_old,
                         key_new=Path(new).stem + '.webp', alt=alt, focus=focus,
                         prefix=prefix, is_start=is_start))
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
            for d, actual, target in r['moves']:
                if actual != target:
                    os.rename(d / actual, d / target)
                print(f"{d.relative_to(assets).as_posix()}/{actual} -> {target}")
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
