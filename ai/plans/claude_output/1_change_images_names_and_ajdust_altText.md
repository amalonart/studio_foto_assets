# Plan 1: auto rename images + altText from name.md (CI)

## Context
Now: user renames files manually, pastes AI alt lines to `assets/altText.ts`, `slideFocus.ts`. Goal: AI produces `name.md` (old | new | alt) per image dir; GH Action renames files, updates altText/slideFocus, archives `name.md` → `name_<ts>.md`, commits, then notifies FE repo.

## Steps
0. Create `ai/plans/app_description.md` (concise: assets repo for studio-foto-fe; dirs start/portfolio/gallery; altText.ts, slideFocus.ts; push main → dispatch `assets-updated` to kmalon/studio-foto-fe).
1. `name.md` format (one row per photo, pipe-separated, no header; `#`/blank lines ignored):
   ```
   IMG_1234.webp | 15-para-mloda-w-parku.webp | Para młoda w jesiennym parku
   ```
   - optional 4th col only for start: focus e.g. `30% 50%`.
   - Location = prefix dir: `assets/start/`, `assets/portfolio/`, `assets/gallery/<folder>/` (same as README PREFIKS).
2. New `scripts/apply_names.py` (python3 stdlib, runner has it):
   - find `assets/**/name.md` exactly (ignore `name_*.md` → processed skipped).
   - per row: prefix = dir rel. to `assets/`; image dirs: start → `start/`; portfolio → `full/`+`thumbs/`; gallery → `full/`+`thumbial/`.
   - validate all first (old exists in every image dir, new not taken unless == old, new ends `.webp`, alt non-empty, no dup new names); any error → exit 1, no changes.
   - `git mv`-free plain rename (os.rename); altText: key `prefix+new`; replace existing value if key present, else insert before closing `}`; also drop old key `prefix+old` if present; `'` → `’`.
   - start: slideFocus key `new` = col4 or `'50% 50%'`; rename existing old key keeping its value.
   - rename `name.md` → `name_<YYYYMMDD-HHMMSS>.md` (UTC).
   - print summary; output `changed=true|false` to `$GITHUB_OUTPUT`.
3. `.github/workflows/notify-fe.yml`:
   - `permissions: contents: write`; steps: checkout → `python3 scripts/apply_names.py` → if changed: git config bot user, `git add -A assets`, commit `Apply name.md renames`, push (GITHUB_TOKEN push doesn't retrigger workflow) → dispatch with sha = new HEAD.
4. README: new section "Zmiana nazw przez name.md" (format, location, what CI does, archived files); update pkt 2/6: AI prompt outputs `name.md` rows instead of TS lines; add `START = NN` line (next number) so AI numbers new names; manual steps kept as fallback.

## Files
- new: `scripts/apply_names.py`, `ai/plans/app_description.md`
- edit: `.github/workflows/notify-fe.yml`, `README.md`

## Verification
- copy repo to scratchpad, add fake `IMG_1.webp` in `start/` + `gallery/1_*/full|thumbial`, write name.md, run script: check renames, altText/slideFocus diff, archive name, rerun = no-op; bad row → exit 1, nothing changed.
- `python3 -c` / `npx tsc`-free check: altText.ts still ends with `}` + `export default`.

## Decisions (answered)
- name.md in prefix dir.
- start w/o 4th col → `'50% 50%'`.
- old name any extension, exact match: file renamed to `stem(new)+ext(old)` (no format change); altText/slideFocus keys always `stem(new).webp`.

## Questions
No questions

## Branch
feature/1-auto-rename-from-name-md
