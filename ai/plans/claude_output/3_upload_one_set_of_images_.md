# Plan 3: upload one set of images (main folder → full + thumbial)

## Context
Now: user copies same originals into `full/` + `thumbs|thumbial/`, name.md renames in both. Goal: upload once to `assets/portfolio/` or `assets/gallery/<s>/` (+ name.md there); CI renames, resizes, distributes to `full/`+`thumbial/`, shrinks thumbial, deletes main-folder images. `start/` unchanged. Portfolio `thumbs` → `thumbial`.

## Steps
1. `git mv assets/portfolio/thumbs assets/portfolio/thumbial` (FE path updated by user separately).
2. `scripts/apply_names.py`:
   - `THUMB_DIRS = ('thumbial',)`.
   - per row: dirs = `[prefix_dir]` if `old` in prefix dir (main folder), else fallback `full/`+`thumbial/` (existing `image_dirs` logic). start → `start/` as now.
   - exists-check of target: main-folder rows also check `full/<new stem>.webp`? no → overwrite = replace photo (README 4); only check clash within same dir.
   - docstring update.
3. `scripts/convert-images.sh`: new stage before DIRS loop, `STAGE_DIRS=(portfolio gallery/*)`:
   - for each image in stage dir root (`$SRC` + `*.webp`, not subdirs, not .md): encode full (`FULL_SIZE`, q90) in place → `<stem>.webp` (webp in limit: skip encode).
   - `mkdir -p full thumbial`; cp `<stem>.webp` → `full/` + `thumbial/` (overwrite).
   - rm original + main-folder webp only after success; other files (overview.md, name_*.md) kept. Fail → keep, count failed.
   - name clash (a.jpg + a.png) → SKIP msg, as existing.
   - then existing DIRS pass: `thumb | gallery/*/thumbial` + `thumb | portfolio/thumbial` shrink oversized webp to 800w (= "resize thumbial next step").
   - DIRS: `portfolio/thumbs` → `portfolio/thumbial`; header comments updated.
4. Workflow `notify-fe.yml`: order unchanged (apply_names → tools → convert → commit → dispatch); step names clarify "Distribute + resize". No other change.
5. README (PL): pkt 0 tree (`portfolio/full/ thumbial/`), pkt 1/2/3/4/5/6/8: upload originals + name.md to main folder; AI prompt input = main-folder images; CI copies to full/thumbial; rename fallback for published photos; `thumbs` removed.
6. `ai/plans/app_description.md` update.
7. Save plan → `ai/plans/claude_output/3_upload_one_set_of_images_.md`.

## Files
- `scripts/apply_names.py`, `scripts/convert-images.sh`, `.github/workflows/notify-fe.yml`, `README.md`, `ai/plans/app_description.md`, dir move `assets/portfolio/thumbs`.

## Verification
- `bash -n scripts/convert-images.sh`, `python3 -m py_compile scripts/apply_names.py`.
- apply_names in scratchpad copy of assets: name.md + fake `IMG_1.jpg` in `gallery/X/` → renamed in main; row for existing full/ file → renamed in full+thumbial.
- imagemagick missing locally → convert stage verified in CI run (or in scratchpad if apt possible).

## Decisions (answered)
- scope: gallery + portfolio.
- rename fallback to full+thumbial: yes.
- process main-folder images without name.md: yes.
- FE `portfolio/thumbs` path: user updates FE.

## Questions
No questions

## Branch
feature/3-upload-one-set-of-images
