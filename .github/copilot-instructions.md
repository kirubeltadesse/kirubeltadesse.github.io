## Quick context

- This repository is a personal Hugo site migrated from Jekyll. Main content lives in `content/`, templates in `layouts/`, and public/static assets under `static/` (served at `/` in the running site). The site is served locally with Hugo (port `1313`) — a `docker-compose.yml` is included for convenience.

## What to know up-front (big picture)

- Rendering model: Hugo templates in `layouts/` (including `layouts/_default/`, `layouts/partials/`) generate pages from `content/` front matter and archetypes. Look at `layouts/index.html`, `layouts/_default/single.html`, and `layouts/partials/*` for layout structure.
- Static assets: files under `static/` are published to the site root. Example: `static/css/*` -> `/css/*`, `static/img/*` -> `/img/*`.
- Scripts and theming: theme toggling is implemented in `/assets/js/theme.js` and `/assets/js/dark_mode.js` (loaded via partials). The theme code toggles `data-theme` on the `<html>` element. The toggle UI expects an element with id `light-toggle`.
- Gallery behavior: gallery templates render images with class `gallery-img`. Modal/zoom logic exists in page scripts and expects DOM ids: `myModal`, `img01`, and caption `caption`.

## Developer workflows (commands)

- Run locally (using Docker compose):

  - `docker-compose up`

  This calls Hugo server and exposes `http://localhost:1313`.

- Run Hugo directly (if installed):

  - `hugo server --bind=0.0.0.0`

- Build static site output to `public/`:

  - `hugo`

If a deployment workflow is configured, it should use the generated `public/` folder — do not deploy raw repository files (e.g., `README.md`).

## Common pitfalls / project-specific conventions

- Static path vs. source path: in Hugo, files under `static/` are served from `/`. Do NOT reference `/static/...` in templates. For example, use `/css/gallery.css` (not `/static/css/gallery.css`). This previously caused MIME-type (text/plain) issues when running the dev server.
- Script ordering matters: some scripts use jQuery (e.g., `dark_mode.js` uses `$(document).ready`). Ensure jQuery is included before those scripts in `layouts/partials/head.html` or the head partial used by pages.
- Avoid double-including files: some pages included `dark_mode.js` twice; ensure partials include scripts once to avoid duplicate listeners or unexpected behavior.
- Theme toggling: the code sets `data-theme` on `document.documentElement`. CSS must target `[data-theme="dark"]` or `:root[data-theme="dark"]` — check `assets/css` or `static/css/main.css` for the rules. The toggle element id is `light-toggle` — templates must include it (see `layouts/partials/header.html`).

## Files to inspect for patterns/examples

- `layouts/_default/baseof.html` (site shell)
- `layouts/partials/head.html` (script and stylesheet includes)
- `layouts/partials/header.html` (navigation + toggle element `#light-toggle`)
- `layouts/partials/footer.html` (footer styling and inclusion)
- `static/css/main.css` and `static/css/gallery.css` (styles; ensure they are referenced as `/css/...`)
- `assets/js/dark_mode.js`, `assets/js/theme.js`, `static/js/common.js` (theme & utility scripts)
- `layouts/gallery/list.html` and `content/gallery/_index.md` (gallery template and content)

## Integration points and external dependencies

- CDN libraries used in templates: Bootstrap, MDB, Font Awesome, Masonry, imagesLoaded. These are included via CDN in `head.html` and footer scripts. When testing offline, ensure those resources are available or host local copies in `static/`.
- cal.com: an external embed (iframe) is used in some pages — iframe content is cross-origin and cannot be styled from the parent. Use the cal.com embed only for display; you cannot change internal styles from this site.

## Debugging tips (site-specific)

- If CSS fails with MIME errors, check that the template references `/css/...` (not `/static/css/...`) and verify file exists in `static/css/`.
- If dark/light toggle does nothing: open DevTools, confirm the `data-theme` attribute is being set on `<html>`. If not, check that `dark_mode.js` is loaded and that `#light-toggle` exists and isn't being removed or overwritten by another partial.
- If gallery hover/zoom is broken: verify `static/css/gallery.css` is present and included as `<link rel="stylesheet" href="/css/gallery.css">` and that images have class `gallery-img`. Also ensure modal elements (`myModal`, `img01`) exist in the rendered HTML.

## What an AI agent should do first (practical checklist)

1. Run `docker-compose up` and open `http://localhost:1313` to view the site. Reproduce the user's reported issues (theme toggle, gallery hover/zoom).
2. Inspect `head` partial to confirm ordering of `<script>` and `<link>` tags (jQuery before `dark_mode.js`).
3. Confirm static assets are referenced from `/css/`, `/js/`, `/img/` and exist under `static/`.
4. Search for duplicate script includes (e.g., `dark_mode.js` included twice) and remove duplicates.
5. When changing files, keep modifications minimal and focused; update partials rather than many individual pages.

## Example fixes (copyable)

- Correct static CSS include (in partial/head or footer):

  - wrong: `<link rel="stylesheet" href="/static/css/gallery.css">`
  - correct: `<link rel="stylesheet" href="/css/gallery.css">`

- Ensure jQuery loads before theme script:

  - `<script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>` then `<script src="/js/dark_mode.js"></script>`

## Notes and limitations

- This file documents patterns discoverable in the repository. It does not prescribe new architecture or add tests. If you need to change build/deploy pipelines (GitHub Actions or Pages), provide the workflow files or deployment target for precise changes.

---

If anything here is unclear or you want me to expand on a particular area (deployment rules, a specific partial, or to run and fix an issue), tell me which part to update and I will iterate.
