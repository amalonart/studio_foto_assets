# Plan 4: don't care about extension (name.md old-name lookup)

## Context
name.md old name must match file exactly. Goal: old `IMG4240.JPG` → find `IMG4240.JPG`, else `IMG4240.webp`; case-insensitive (`img4240.webp` ok).

## Steps
1. `scripts/apply_names.py`:
   - new `resolve(d: Path, old) -> str | None | list` : priority 1 exact file; 2 case-insens same name; 3 case-insens `<stem>.webp`. >1 match in a tier → ambiguous error.
   - `image_dirs`: main dir if `resolve(prefix_dir, old)` found, else full+thumbial (as now).
   - `parse`: per dir resolve actual old name (`dirs` → list of `(dir, actual_old)`); missing → error `missing <d>/<old> (or .webp, any case)`; target = new stem + actual suffix (per dir); clash check per dir; dup-check on new stem.
   - `key_old` = actual stem + `.webp` (from first dir) — altText key of old photo.
   - rename loop uses per-dir actual old; print actual names.
   - docstring update.
2. README (PL) pkt 6.1 + pkt 8: old name lookup — exact, else same stem `.webp`, case-insensitive.
3. `ai/plans/app_description.md`: apply_names line += "old name match: exact → case-insens → stem.webp".
4. Save plan → `ai/plans/claude_output/4_donot_care_about_extension.md`.

## Verification
- `python3 -m py_compile scripts/apply_names.py`.
- Scratchpad copy of assets: main dir `img4240.webp` + row `IMG4240.JPG | 52-x.webp | Alt` → renamed `52-x.webp`, altText key added; `IMG4240.JPG` exists → `52-x.JPG`; published `full/` file referenced by `.jpg` name → renamed in full+thumbial; `a.webp`+`A.webp` → ambiguous error.

## Questions
No questions

## Branch
feature/4-donot-care-about-extension
