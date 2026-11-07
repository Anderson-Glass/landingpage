# Anderson Glass & Glazing — website

Deployed on Cloudflare Pages (project `andersonglass`), live at https://andersonglass.pages.dev
Apex `andersonglass.com.au` still points at GitHub Pages until the DNS nameserver move.

## Two build files — read this first
- `build.py` — the **content model** (services, areas, projects, org facts, FAQ copy). Import it, don't run it.
- `build2.py` — the **presentation layer** (templates, "drawing sheet" design). This is the one you run.

```bash
cd build && python3 build2.py      # → ../site
cd .. && npx wrangler pages deploy site --project-name andersonglass --branch main
```

`build.py` still has its own older `main()` and `site.css`; it is kept only as the content source and a
previous design. If you edit copy, edit the data structures at the top of `build.py`.

## Design
Paper + ink + safety orange, Fraunces display + IBM Plex Mono labels, blueprint grid, dimension lines
and annotation callouts over real job photography. Dark mode is "blueprint". No prices anywhere.

## AI retrieval layer
- `/facts.json` — structured business facts (services, standards, quoting policy, per-service FAQ)
- `/llms.txt`, `/llms-full.txt` — plain-language summaries
- one JSON-LD `@graph` per page + `FAQPage`/`Service`/`BreadcrumbList`
- `robots.txt` explicitly allowing GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot
