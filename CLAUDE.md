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
├── index.html           # Homepage (substantial inline CSS + JS)
├── blog/index.html      # Custom blog page (substantial inline CSS + JS)
├── css/shared.css       # Shared design tokens, nav/footer styles
├── js/components.js     # Shared nav, footer, and theme behavior (used by blog)
├── netlify/functions/   # Serverless functions proxying external feeds/APIs
│   ├── platformer-feed.js
│   ├── hardfork-feed.js
│   ├── hardfork-podcast.js
│   └── lastfm.js
├── data/book.json       # Manually maintained currently-reading widget data
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
- `cnewton.org/blog/` is a client-side mirror that fetches
  `https://blog.cnewton.org/feed.json`; individual post links lead to
  blog.cnewton.org.
- Micro.blog cannot directly publish the blog at the `cnewton.org/blog/`
  subdirectory. Do not implement HTML scraping or an unapproved reverse-proxy
  workaround.
- Changes to the Micro.blog theme, DNS, custom-domain configuration, or exports
  require explicit approval and external access.

## External services and secrets

The site uses or may call:

- Platformer RSS (via Netlify Function)
- Hard Fork's YouTube feed (via Netlify Function)
- Hard Fork's Simplecast RSS feed (via Netlify Function)
- Last.fm (via Netlify Function)
- Micro.blog's JSON Feed
- Bluesky's public API
- wttr.in weather
- Google Fonts

`LASTFM_API_KEY` is configured externally in Netlify. It must never be written
into the repository, printed in output, or exposed to browser-side code. Do not
expose environment-variable values or secrets.

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
themes (`data-theme` handled in `js/components.js`).

## Testing and verification

- When changing JavaScript, run an available syntax check (e.g.
  `node --check`) and manually inspect the affected pages in a browser.
- Test both light and dark themes where relevant.
- Test desktop and narrow mobile layouts where relevant (breakpoints at 968px
  and 480px in shared.css; blog and homepage also use others inline).
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
