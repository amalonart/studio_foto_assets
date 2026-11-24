# App description
- Assets repo for FE site `kmalon/studio-foto-fe` (photographer site: Start, Portfolio, Galeria). README in Polish.
- `assets/start/` slides (`NN-opis.webp`), `assets/portfolio/full|thumbial/` (`NNN-opis.webp`), `assets/gallery/<N>_<sesja>/full|thumbial/ + overview.md`, `assets/about/`.
- Upload: new photos + `name.md` go once to main folder (`portfolio/`, `gallery/<s>/`; start → `start/`); CI distributes to full+thumbial.
- `assets/altText.ts`: map `'<prefix>/<file>.webp': 'alt PL'` (prefix = start/, portfolio/, gallery/<folder>/).
- `assets/slideFocus.ts`: map start file name → object-position (`'30% 50%'`).
- Image resize: `scripts/convert-images.sh [assets]`: stage 1 main-folder images (`STAGE_DIRS`) → full webp ≤2048 q90, copy to `full/`+`thumbial/`, delete from main (non-images kept); stage 2 WebP in place (full/start ≤2048 q90, thumbial 800w q80, deletes originals; oversized webp shrunk, in-limit untouched).
- CI `.github/workflows/notify-fe.yml` (push main): `scripts/apply_names.py` (processes `name.md` in prefix dirs: rename old→new in main folder, fallback full+thumbial; update altText/slideFocus; archive to `name_<ts>.md`), apt imagemagick+webp, `convert-images.sh assets`, commit+push if diff, then `repository_dispatch` `assets-updated` to FE.
