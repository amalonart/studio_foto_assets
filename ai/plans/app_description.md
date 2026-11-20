# App description
- Assets repo for FE site `kmalon/studio-foto-fe` (photographer site: Start, Portfolio, Galeria). README in Polish.
- `assets/start/` slides (`NN-opis.webp`), `assets/portfolio/full|thumbs/` (`NNN-opis.webp`), `assets/gallery/<N>_<sesja>/full|thumbial/ + overview.md`, `assets/about/`.
- `assets/altText.ts`: map `'<prefix>/<file>.webp': 'alt PL'` (prefix = start/, portfolio/, gallery/<folder>/).
- `assets/slideFocus.ts`: map start file name → object-position (`'30% 50%'`).
- Image resize: `convert-images.sh` lives in FE repo, run locally.
- CI `.github/workflows/notify-fe.yml` (push main): runs `scripts/apply_names.py` (processes `name.md` in prefix dirs: rename old→new in full+thumbs, update altText/slideFocus, archive to `name_<ts>.md`, commit+push), then `repository_dispatch` `assets-updated` to FE.
