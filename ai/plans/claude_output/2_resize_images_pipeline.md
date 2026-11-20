# Plan 2: resize images in CI pipeline

## Context
Resize done locally via `convert-images.sh` (from FE repo, DIRS = `src/assets/...`). Goal: CI step runs it on push. Check: thumbs as full-size webp?
- Finding: **does not work**. In-place lines convert only non-webp (`SRC` glob) → full-res webp in `thumbs/`/`thumbial/` skipped ("Nothing new to convert").
- Existing state: all thumbs ≤800w, all full/start ≤2048 → width-based check safe, no bulk re-encode on first run.

## Steps
1. Move `convert-images.sh` → `scripts/convert-images.sh` (git add; now untracked).
   - Arg 1 = assets dir (default `assets`), `cd` into it; DIRS relative: `start`, `portfolio/full`, `portfolio/thumbs`, `gallery/*/full`, `gallery/*/thumbial`.
2. Oversized webp in place:
   - in-place `thumb` lines: also take `*.webp` with width > 800 (`identify -format %w`) → re-encode `THUMB_SIZE`/q80, same name (write tmp, mv; no delete since src==out).
   - same for `full` lines: webp width or height > 2048 → `FULL_SIZE`/q90 (see Q1).
   - webp within limits never touched (idempotent).
   - `add_job` del flag: 0 when src == out.
3. Workflow `notify-fe.yml` order: checkout → `apply_names.py` (renames before convert, so name.md old names w/ `.jpg` still match) → install `imagemagick webp libheif1` (apt) → `bash scripts/convert-images.sh assets` → commit step: `git add -A assets; git diff --cached --quiet || commit "Apply name.md renames / resize images" + push` (replaces `if: changed`) → dispatch.
   - convert fail count > 0 → exit 1 (no notify).
4. README: pkt 2.3 / 4 / 8: resize runs in CI, local run optional (`bash scripts/convert-images.sh`); full-size webp may be copied to thumbs (CI shrinks); originals deleted by CI commit (kept in git history).
5. Update `ai/plans/app_description.md` (resize now in CI).

## Files
- move+edit: `convert-images.sh` → `scripts/convert-images.sh`
- edit: `.github/workflows/notify-fe.yml`, `README.md`, `ai/plans/app_description.md`

## Verification
- `bash -n`; local deps missing → test in scratchpad copy only if imagemagick installable, else verify in CI run.
- scratchpad copy: put full webp in `portfolio/thumbs/`, jpg in `start/`, run → thumb 800w, jpg→webp, rerun = "Nothing new".

## Decisions (answered)
- shrink full/start webp > 2048: yes.
- script → `scripts/`: yes.

## Questions
No questions

## Branch
feature/2-resize-images-pipeline
