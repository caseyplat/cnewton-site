# cnewton.org

Personal website for Casey Newton, tech journalist.

## Project overview

- **Local path:** `/Users/caseynewton/cnewton-site`
- **GitHub:** `https://github.com/caseyplat/cnewton-site.git`
- **Live URL:** `https://cnewton.org`
- Hand-written static site: HTML, CSS, and vanilla JavaScript. No application
  framework, no Hugo, no package.json, no package manager, no lockfile, no
  build command. There is currently no lint, type-check, test, or CI setup.

## Repository structure

```
cnewton-site/
├── index.html           # Homepage (substantial inline CSS + JavaScript)
├── about/index.html     # Biography, press photo, and public contact page
├── work/index.html      # Generated static Selected Work page
├── data/
│   └── selected-work.json  # Source of truth for Selected Work entries
├── scripts/
│   └── render_selected_work.py  # Renders and validates the work list
├── css/shared.css       # Design tokens and styles shared across site pages
├── netlify/functions/   # Serverless functions proxying homepage feeds
│   ├── platformer-feed.js
│   └── hardfork-feed.js
├── netlify.toml         # Netlify Functions directory config
├── headshot.jpg, favicon.svg, platformer-logo.svg, hardfork-logo.png
```

## Local development

- No build step. Preview with any ordinary static HTTP server, e.g.:

  ```
  python3 -m http.server 8000
  ```

- Netlify Functions do not run under a basic static server; failed function
  requests during that kind of preview are expected.
- After editing `data/selected-work.json`, render and validate the static page:

  ```
  python3 scripts/render_selected_work.py
  python3 scripts/render_selected_work.py --check
  ```

- After changing page metadata, canonical URLs, feeds, sitemap.xml, robots.txt,
  or 404.html, run:

  ```
  python3 scripts/validate_site_metadata.py
  ```

## Hosting and deployment

- Hosted on Netlify. The repository root is the publish directory.
- Production deploys from the `main` branch of `github.com/caseyplat/cnewton-site`.
- `netlify.toml` configures the functions directory (`netlify/functions`).
- Functions use the classic `exports.handler` format and the built-in `fetch`
  API, so the effective runtime must support fetch (Node 18+).
- Do not push, deploy, alter DNS, change Netlify settings, or modify external
  services unless Casey explicitly asks.
- Do not commit, push, or deploy unless explicitly asked.

## Blog architecture

- `blog.cnewton.org` is the canonical blog, hosted by Micro.blog. It is not
  generated from this repository. Individual posts, the RSS feed, JSON Feed,
  sitemap, robots.txt, and post canonical metadata are served there.
- `cnewton.org/blog/` and paths beneath it permanently redirect to
  `https://blog.cnewton.org/` through `netlify.toml`.
- The Micro.blog custom theme is maintained through Micro.blog's theme editor,
  not in this repository.
- The main site and blog share the `cnewton-theme` cookie across subdomains so
  a visitor's light or dark choice follows them between the two sites. With no
  saved choice, both sites default to light.
- Micro.blog cannot directly publish the blog at the `cnewton.org/blog/`
  subdirectory. Do not implement HTML scraping or an unapproved reverse-proxy
  workaround.
- Changes to the Micro.blog theme, DNS, custom-domain configuration, or exports
  require explicit approval and external access.

## External services and secrets

The site uses or may call:

- Platformer RSS (via Netlify Function)
- Hard Fork's YouTube feed (via Netlify Function)
- Google Fonts

Optional external services should degrade cleanly: a failure in a feed, API, or
widget must not prevent the site's primary static content from rendering.

## Design system

**Color palette (CSS variables in shared.css):**
- `--cyan`: Accent color (links, highlights)
- `--magenta`: Secondary accent
- `--darker`: Background
- `--dark`: Section backgrounds
- `--gray`: Card backgrounds
- `--light`: Text color

**Fonts:**
- `Silkscreen` — pixel/retro labels and UI elements
- `Syne` — headlines (weight 800)
- `Space Mono` — body text, monospace elements

**Visual style:** Cyberpunk/retro aesthetic with pixel decorations, gradient
borders, cursor trails, and hover animations. The site has light and dark
themes (`data-theme` handled in `index.html`) and defaults to light.

## Testing and verification

- When changing JavaScript, run an available syntax check (e.g.
  `node --check`) and manually inspect the affected pages in a browser.
- Test both light and dark themes where relevant.
- Test desktop and narrow mobile layouts where relevant (breakpoints at 968px
  and 480px in shared.css; the homepage also uses others inline).
- Keep animations performant.
- Inspect `git diff` before declaring a task complete.

## Editing constraints

- Inspect `git status` before editing; preserve unrelated pre-existing changes.
- Make the smallest maintainable change that satisfies the task; do not broadly
  refactor during a contained editorial or maintenance request.
- Preserve the existing visual identity — the CN_ mark, typography, color
  system, navigation structure, and light/dark theme — unless Casey explicitly
  requests a redesign.
- Do not mention, create placeholders for, or anticipate an unannounced future
  podcast unless Casey explicitly asks.
- Do not invent biographical facts, awards, dates, audience figures, article
  titles, URLs, contact details, or image credits. Reuse only public
  information already present in the repository or explicitly supplied by
  Casey.
- Do not add analytics to secure-contact or Signal links.
