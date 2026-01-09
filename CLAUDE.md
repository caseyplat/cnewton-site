# cnewton.org

Personal website for Casey Newton, tech journalist.

## Project Info

- **Local path:** `/Users/caseynewton/cnewton-site`
- **GitHub:** `https://github.com/caseyplat/cnewton-site.git`
- **Live URL:** `https://cnewton.org`

## Structure

```
cnewton-site/
├── index.html          # Main homepage
├── css/shared.css      # Shared styles (nav, footer, colors)
├── js/                 # JavaScript files
├── blog/               # Blog content (Hugo-generated)
├── blog-theme/         # Hugo theme for blog
├── data/               # Data files
├── headshot.jpg        # Profile photo
├── favicon.svg         # Site favicon
├── platformer-logo.svg # Platformer project logo
└── hardfork-logo.png   # Hard Fork podcast logo
```

## Tech Stack

- Static HTML/CSS/JS (no build step for main site)
- Hugo for blog (`blog-theme/` directory)
- Hosted via GitHub Pages or similar static host

## Design System

**Color palette (CSS variables in shared.css):**
- `--cyan`: Accent color (links, highlights)
- `--magenta`: Secondary accent
- `--darker`: Background
- `--dark`: Section backgrounds
- `--gray`: Card backgrounds
- `--light`: Text color

**Fonts:**
- `Silkscreen` - Pixel/retro labels and UI elements
- `Syne` - Headlines (weight 800)
- `Space Mono` - Body text, monospace elements

**Visual style:** Cyberpunk/retro aesthetic with pixel decorations, gradient borders, cursor trails, and hover animations.

## Dynamic Content

The homepage fetches:
- Recent Platformer posts via RSS (`https://www.platformer.news/rss/`)
- Recent Hard Fork YouTube videos via channel RSS

## Deployment

Push to `main` branch on GitHub. Site mirrors to cnewton.org.

## Preferences

- Maintain the existing cyberpunk aesthetic
- Keep animations performant
- Test responsiveness (mobile breakpoint at 968px and 480px)
