# Anderson Glass & Glazing — website

Static site for andersonglass.com.au, deployed on Cloudflare Pages (project `andersonglass`).

## Build
    cd build && python3 build.py

Output goes to `../site`. Deploy with:

    npx wrangler pages deploy site --project-name andersonglass --branch main

## Structure
- `build/build.py` — content model + templates (all pages)
- `build/assets/` — `site.css`, `site.js`, self-hosted fonts, favicon
- `build/images/` — source-derived WebP derivatives (480/800/1280/1920)
- `site/` — generated output; do not hand-edit

## Rules baked in
- No prices anywhere; enquiry-only. Pricing quoted after measure.
- No invented reviews, ratings or certifications.
- Photos are Anderson Glass's own job photos.
- Every page ships answer-first copy, JSON-LD `@graph`, and is verified against the
  live Cloudflare response (status, headers, 404, console) rather than assumed.
