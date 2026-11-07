#!/usr/bin/env python3
"""Anderson Glass & Glazing — 'drawing sheet' build (v2).

Content model is imported from build.py; this module owns the presentation layer.
Run:  python3 build2.py   ->  ../site
"""
import json, html, shutil
from pathlib import Path

import build as C   # content model + helpers

BASE = Path(__file__).parent
OUT = BASE.parent / "site"
SITE = C.SITE
ORG = C.ORG
NAV = C.NAV
SERVICES = C.SERVICES
AREAS = C.AREAS
PROJECTS = C.PROJECTS
GALLERY = C.GALLERY
HOME_FAQ = C.HOME_FAQ

ARROW = '<svg viewBox="0 0 16 16" width="12" height="12" fill="none" aria-hidden="true"><path d="M3 13L13 3M13 3H5.5M13 3v7.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>'

LOGO = """<svg viewBox="0 0 40 40" fill="none" aria-hidden="true" width="36" height="36">
<rect x="1" y="1" width="38" height="38" stroke="currentColor" stroke-width="1.6"/>
<path d="M1 13.5h38M13.5 1v38" stroke="currentColor" stroke-width="1.6"/>
<path d="M13.5 13.5h25.5v25.5" stroke="currentColor" stroke-width="1.6" opacity=".5"/>
</svg>"""


def img(name, alt="", sizes="100vw", cls="", priority=False):
    widths = (1920, 1280, 800, 480)
    srcset = ", ".join(f"/images/{name}-{w}.webp {w}w" for w in widths)
    lp = ' fetchpriority="high"' if priority else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="/images/{name}-1280.webp" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{alt}" width="1280" height="960"{lp}{c} decoding="async">')


def head(title, desc, path, extra_json=None, og_img="hero-corridor"):
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Organization", "HomeAndConstructionBusiness"],
                "@id": SITE + "/#org",
                "name": ORG["name"], "legalName": ORG["legal"], "url": SITE + "/",
                "telephone": ORG["tel"], "email": ORG["email"],
                "image": SITE + "/images/hero-corridor-1280.webp",
                "logo": SITE + "/assets/favicon.svg",
                "priceRange": "Quote on inspection",
                "address": {"@type": "PostalAddress",
                            "addressLocality": ORG["suburb"], "addressRegion": ORG["state"],
                            "postalCode": ORG["postcode"], "addressCountry": "AU"},
                "areaServed": [{"@type": "City", "name": "Melbourne"}] +
                              [{"@type": "AdministrativeArea", "name": a["name"]} for a in AREAS],
                "knowsAbout": ["Commercial glazing", "Office partitions", "Shower screens",
                               "Glass replacement", "Mirror wardrobe doors", "AS 1288", "AS 2208"],
                "taxID": ORG["abn"], "vatID": "ABN " + ORG["abn"],
            },
            {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
             "name": ORG["name"], "publisher": {"@id": SITE + "/#org"}},
            {"@type": "WebPage", "@id": SITE + path + "#page", "url": SITE + path,
             "name": title, "description": desc, "isPartOf": {"@id": SITE + "/#website"},
             "about": {"@id": SITE + "/#org"}},
        ],
    }
    if extra_json:
        ld["@graph"].extend(extra_json)
    ld_json = json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="geo.region" content="AU-VIC">
<meta name="geo.placename" content="Melbourne">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Anderson Glass &amp; Glazing">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/images/{og_img}-1280.webp">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f1eee6">
<link rel="preload" href="/assets/fonts/Fraunces-up-300_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/IBMPlexMono-up-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts2.css">
<link rel="stylesheet" href="/assets/site2.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/json" href="/facts.json" title="Business facts (JSON)">
<script type="application/ld+json">{ld_json}</script>"""


def header(active):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if active == h else ""}>{l}</a>' for h, l in NAV)
    dl = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV)
    return f"""<header class="tblock">
  <div class="wrap tblock-in">
    <a class="brand" href="/" aria-label="Anderson Glass &amp; Glazing — home">
      <span class="mark">AG</span>
      <span><b>Anderson Glass &amp; Glazing</b><span>Melbourne · est. {ORG['founded']}</span></span>
    </a>
    <nav class="nav" aria-label="Primary">{links}</nav>
    <div class="tools">
      <button class="icon-btn" data-theme-toggle aria-label="Switch to blueprint theme">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>
      </button>
      <a class="btn" href="/quote/">Request a quote {ARROW}</a>
      <button class="icon-btn menu-btn" data-menu aria-expanded="false" aria-label="Menu">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>
</header>
<div class="drawer" aria-label="Menu">
  {dl}
  <a href="/quote/">Request a quote</a>
  <a class="btn" href="tel:{ORG['tel']}">Call {ORG['phone']}</a>
</div>"""


def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{s["title"]}</a></li>' for s in SERVICES)
    ar = "".join(f'<li><a href="/service-areas/{a["slug"]}/">{a["name"]}</a></li>' for a in AREAS)
    return f"""<footer class="footer">
  <div class="wrap" style="padding-bottom:0">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/" aria-label="Anderson Glass &amp; Glazing — home">
          <span class="mark">AG</span>
          <span><b>Anderson Glass &amp; Glazing</b><span>Melbourne · est. {ORG['founded']}</span></span>
        </a>
        <p>Commercial glazing, office partitions, shower screens, glass replacement and mirrors. Measured on site, fabricated to that measurement, installed by the glazier who quoted it.</p>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Areas</h4><ul>{ar}</ul></div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{ORG['tel']}">{ORG['phone']}</a></li>
          <li><a href="mailto:{ORG['email']}">{ORG['email']}</a></li>
          <li><a href="/quote/">Request a quote</a></li>
          <li><a href="/standards/">Standards</a></li>
          <li><a href="/facts/">Business facts</a></li>
          <li><a href="/facts.json">facts.json</a></li>
        </ul>
      </div>
    </div>
    <div class="tb-strip">
      <div><b>Business</b><span>{ORG['legal']}</span></div>
      <div><b>ABN / ACN</b><span>{ORG['abn']} / {ORG['acn']}</span></div>
      <div><b>Based in</b><span>{ORG['location']}</span></div>
      <div><b>Sheet</b><span>© <span data-year>2026</span></span></div>
      <div><b>Rev</b><span>2.0</span></div>
    </div>
  </div>
</footer>"""


def shell(title, desc, path, body, active="", extra_json=None, og_img="hero-corridor"):
    page = f"""<!doctype html>
<html lang="en-AU" data-theme="paper">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head(title, desc, path, extra_json, og_img)}
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
{header(active)}
{body}
{footer()}
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Project image">
  <button class="lightbox-close" aria-label="Close">✕</button>
  <figure><img alt=""><figcaption></figcaption></figure>
</div>
<script src="/assets/site2.js" defer></script>
</body>
</html>"""
    write(path, page)


def write(path, content):
    if path == "/":
        target = OUT / "index.html"
    elif path.endswith("/"):
        target = OUT / path.strip("/") / "index.html"
    else:
        target = OUT / path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def plate(name, cap, ref="", sizes="(max-width:900px) 50vw, 33vw", cls="", alt=""):
    return f"""<figure class="plate {cls} reveal" data-lightbox data-full="/images/{name}-1920.webp">
  {img(name, alt or cap, sizes=sizes)}
  <figcaption><b>{cap}</b><span>{ref}</span></figcaption>
</figure>"""


def phero(kicker, h1, sub, crumbs, fig=None, ref="DETAIL"):
    cb = "".join(f'<a href="{h}">{t}</a><span>/</span>' for h, t in crumbs)
    if fig:
        grid = f"""<div class="phero-grid phero-grid--img">
      <div>{'<span class="lbl lbl--orange">' + kicker + '</span>'}<h1>{h1}</h1><p class="lead">{sub}</p></div>
      <div class="phero-fig">{img(fig, html.unescape(kicker) + ' — Anderson Glass project', sizes='(max-width:860px) 100vw, 46vw', priority=True)}</div>
    </div>"""
    else:
        grid = f"""<div class="phero-grid">
      <div><span class="lbl lbl--orange">{kicker}</span><h1>{h1}</h1><p class="lead">{sub}</p></div>
    </div>"""
    return f"""<section class="phero">
  <div class="wrap">
    <div class="crumbs">{cb}<span>{ref}</span></div>
    {grid}
  </div>
</section>"""


# ---------------------------------------------------------------- home

def build_home():
    ledger = ""
    for i, s in enumerate(SERVICES, 1):
        ledger += (f'<a href="/services/{s["slug"]}/"><span class="n">{i:02d}</span>'
                   f'<span class="nm">{s["title"]}</span><span class="ds">{s["short"]}</span>'
                   f'<span class="ar">{ARROW}</span></a>')

    plates = ""
    layout = ["plate--w", "", "", "", "", "plate--w", "", "plate--w", ""]
    for i, (nm, cap, tags, _cls) in enumerate(GALLERY):
        cls = layout[i % len(layout)]
        plates += plate(nm, cap, f"AG-{i+1:02d}", cls=cls, alt=cap)

    faq = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="a">{a}</div></details>'
                  for q, a in HOME_FAQ)

    faq_ld = {"@type": "FAQPage", "@id": SITE + "/#faq",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in HOME_FAQ]}
    cat_ld = {"@type": "OfferCatalog", "name": "Glazing services",
              "itemListElement": [{"@type": "Offer", "itemOffered": {
                  "@type": "Service", "name": html.unescape(s["title"]),
                  "url": SITE + f"/services/{s['slug']}/"}} for s in SERVICES]}

    body = f"""
<main id="main">
  <section class="hero">
    <div class="wrap">
      <div class="hero-meta">
        <span><b>Sheet 01</b></span><span>General arrangement</span><span>Melbourne, VIC</span><span>Rev. 2.0</span><span style="margin-left:auto">Scale — 1:1 on site</span>
      </div>
      <div class="hero-grid">
        <div class="hero-copy">
          <span class="lbl lbl--orange">Glass &amp; glazing · est. {ORG['founded']}</span>
          <h1>
            <span class="ln">Glass,</span>
            <span class="ln">measured</span>
            <span class="ln">to the <em>mm.</em></span>
          </h1>
          <div class="dim"><span>0</span><i></i><span>opening width</span></div>
          <p class="lead" style="margin-top:22px">Commercial glazing, office partitions, frameless screens, replacement glass and mirrors — supplied and installed across Melbourne by the glazier who quoted it.</p>
          <div class="hero-actions">
            <a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
            <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a>
          </div>
        </div>
        <div class="hero-fig">
          {img('hero-corridor', 'Glass corridor in a Melbourne office fitout', priority=True)}
          <div class="anno anno--tr"><b>10 mm</b><br>toughened<br>AS 1288</div>
          <div class="anno anno--bl"><b>Frameless</b><br>patch fixed</div>
        </div>
      </div>
      <div class="tb-strip" style="border-left:0;border-right:0;border-bottom:0">
        <div><b>Years on the tools</b><span>10+</span></div>
        <div><b>Selected under</b><span>AS 1288</span></div>
        <div><b>Service lines</b><span>Five</span></div>
        <div><b>Coverage</b><span>Melbourne metro</span></div>
        <div><b>Quoting</b><span>After measure</span></div>
      </div>
    </div>
  </section>

  <section class="sect wrap" style="border-top:0">
    <div class="sect-meta">
      <span class="lbl">Sheet 02 — Scope</span>
      <span class="lbl">Five lines of work</span>
    </div>
    <h2 style="max-width:16ch;margin-bottom:clamp(24px,3vw,40px)">What we <em>make.</em></h2>
    <div class="ledger">{ledger}</div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Sheet 03 — Method</span><span class="lbl">Measured once, cut once</span></div>
    <div class="split">
      <div class="split-fig">{plate('thorn-fitout', 'Thorn office fitout', 'AG-014', sizes='(max-width:860px) 100vw, 50vw')}</div>
      <div>
        <h2 style="max-width:18ch">Glass can't be<br>adjusted on <em>site.</em></h2>
        <div class="prose" style="margin-top:22px">
          <p>That single fact decides how a glazing job goes. So the person who quotes also measures — after the tiles and the finished floor, not from the drawing — and the numbers the glass is cut to are the numbers on the quote.</p>
          <ul>
            <li>Site measure taken on the finished opening, not from plans</li>
            <li>Glass make-up and thickness named in writing</li>
            <li>Selection checked against AS 1288 for the actual location</li>
            <li>One glazier accountable from quote to final silicone</li>
          </ul>
        </div>
        <a class="btn btn--ghost" href="/standards/" style="margin-top:26px">How we select glass {ARROW}</a>
      </div>
    </div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta">
      <span class="lbl">Sheet 04 — Plates</span>
      <span class="lbl">Completed jobs, photographed on site</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:26px">
      <h2 style="max-width:14ch">Selected <em>work.</em></h2>
      <div class="filters">
        <button class="chip is-active" data-filter="all">All</button>
        <button class="chip" data-filter="commercial">Commercial</button>
        <button class="chip" data-filter="residential">Residential</button>
      </div>
    </div>
    <div class="plates">{plates}</div>
    <div style="margin-top:26px"><a class="btn btn--ghost" href="/projects/">Project stories {ARROW}</a></div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Sheet 05 — Schedule</span><span class="lbl">Glass selection</span></div>
    <div class="split">
      <div>
        <h2 style="max-width:16ch">Glass is selected,<br>not <em>guessed.</em></h2>
        <div class="prose" style="margin-top:20px">
          <p>The same wall can need different glass depending on how low the pane sits, whether it is in a door, what is above it and how big it is. That is what AS 1288 exists for — which is why a real quote names a make-up and a thickness, not a "type of glass".</p>
        </div>
      </div>
      <div class="detail">
        <h3>Typical make-ups</h3>
        <div class="table-scroll">
          <table class="schedule">
            <thead><tr><th>Application</th><th>Make-up</th><th>mm</th><th>Standard</th></tr></thead>
            <tbody>
              <tr><td>Shopfront, framed</td><td>Toughened</td><td>6–10</td><td>AS 1288</td></tr>
              <tr><td>Glass entry door</td><td>Toughened / laminated</td><td>10–12</td><td>AS 1288</td></tr>
              <tr><td>Frameless screen</td><td>Toughened</td><td>10</td><td>AS 2208</td></tr>
              <tr><td>Acoustic partition</td><td>Double glazed</td><td>6-12-6</td><td>AS 4666</td></tr>
              <tr><td>Balustrade infill</td><td>Toughened laminated</td><td>10+10</td><td>AS 1288</td></tr>
            </tbody>
          </table>
        </div>
        <p class="note" style="margin-top:14px">Indicative only — every job is selected on its measured panel and location. <a href="/standards/">How AS 1288 is applied →</a></p>
      </div>
    </div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Sheet 06 — Sequence</span><span class="lbl">Enquiry to install</span></div>
    <div class="steps">
      <div><span class="n">01</span><h3>Enquire</h3><p>Send a photo, the suburb and a rough size. We tell you what is possible before anyone drives out.</p></div>
      <div><span class="n">02</span><h3>Measure</h3><p>The installing glazier attends and measures the finished opening.</p></div>
      <div><span class="n">03</span><h3>Quote</h3><p>Make-up, thickness, hardware and inclusions in writing.</p></div>
      <div><span class="n">04</span><h3>Install</h3><p>Cut to those measurements, fitted, cleaned down, certified where required.</p></div>
    </div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Sheet 07 — Coverage</span><span class="lbl">Melbourne metro</span></div>
    <h2 style="max-width:18ch;margin-bottom:26px">Where we <em>work.</em></h2>
    <div class="areas">
      {''.join(f'<a class="area" href="/service-areas/{a["slug"]}/"><h3>{a["name"]}</h3><p>{a["blurb"]}</p><span class="go">View area {ARROW}</span></a>' for a in AREAS)}
      <a class="area area--ask" href="/quote/"><h3>Somewhere else?</h3><p>Give us the suburb and the scope — we will tell you honestly whether the drive makes sense.</p><span class="go">Ask us {ARROW}</span></a>
    </div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Sheet 08 — Notes</span><span class="lbl">General</span></div>
    <h2 style="margin-bottom:26px">Asked <em>often.</em></h2>
    <div class="faq">{faq}</div>
  </section>

  <section class="sect cta" id="quote">
    <div class="wrap cta-grid">
      <div>
        <span class="lbl lbl--orange">Start here</span>
        <h2 style="margin-top:14px">Tell us about<br>the <em>opening.</em></h2>
        <p class="lead" style="margin-top:16px">A photo and a rough size is enough to start. Call if it is easier — the number goes to the glazier, not a call centre.</p>
        <div class="contact">
          <a href="tel:{ORG['tel']}"><strong>Phone</strong><span>{ORG['phone']}</span></a>
          <a href="mailto:{ORG['email']}"><strong>Email</strong><span>{ORG['email']}</span></a>
          <div><strong>Based in</strong><span>{ORG['location']}</span></div>
        </div>
      </div>
      <form class="form" data-enquiry novalidate>
        <div class="form-row">
          <div class="field"><label for="n">Name</label><input id="n" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="p">Phone</label><input id="p" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="e">Email</label><input id="e" name="email" type="email" autocomplete="email"></div>
          <div class="field"><label for="s">Suburb</label><input id="s" name="suburb" type="text" autocomplete="address-level2"></div>
        </div>
        <div class="field"><label for="sv">What is it for?</label>
          <select id="sv" name="service">{''.join(f'<option>{s["title"]}</option>' for s in SERVICES)}<option>Mirrors / splashback</option><option>Something else</option></select>
        </div>
        <div class="field"><label for="m">Details</label><textarea id="m" name="message" placeholder="Rough width and height, new build or replacement, anything the photos do not show."></textarea></div>
        <div aria-hidden="true" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden">
          <label for="cw">Company website</label>
          <input id="cw" name="company_website" type="text" tabindex="-1" autocomplete="off">
        </div>
        <button class="btn btn--lg" type="submit">Send enquiry {ARROW}</button>
        <p class="form-note">Goes straight to our inbox — no third-party marketing platform, no tracking. We reply to the email address or phone number you give us; photos can follow by reply.</p>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>
</main>"""

    shell("Anderson Glass & Glazing — Commercial Glazing & Shower Screens, Melbourne",
          "Melbourne commercial glazing, office partitions, frameless shower screens, glass replacement and mirrors. Measured, made and installed by the same glazier — Anderson Glass & Glazing, Narre Warren East.",
          "/", body, extra_json=[faq_ld, cat_ld])


# ---------------------------------------------------------------- services

def build_service(s):
    faq = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="a">{a}</div></details>'
                  for q, a in s["faqs"])
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
               "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]}
    svc_ld = {"@type": "Service", "name": html.unescape(s["title"]),
              "serviceType": html.unescape(s["title"]), "provider": {"@id": SITE + "/#org"},
              "areaServed": {"@type": "City", "name": "Melbourne"},
              "url": SITE + f"/services/{s['slug']}/",
              "description": html.unescape(s["answer"])}
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "/services/"},
        {"@type": "ListItem", "position": 3, "name": html.unescape(s["title"]),
         "item": SITE + f"/services/{s['slug']}/"}]}

    opts = "".join(f"<tr><td>{n}</td><td>{d}</td></tr>" for n, d in s["options"])
    specs = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in s["specs"])
    others = [x for x in SERVICES if x["slug"] != s["slug"]]
    ledger = "".join(f'<a href="/services/{o["slug"]}/"><span class="n">{i:02d}</span>'
                     f'<span class="nm">{o["title"]}</span><span class="ds">{o["short"]}</span>'
                     f'<span class="ar">{ARROW}</span></a>' for i, o in enumerate(others, 1))

    body = f"""
<main id="main">
  {phero("Service", s['title'], s['short'], [("/", "Home"), ("/services/", "Services")], fig=s['img'], ref="DETAIL")}
  <section class="sect sect--tight wrap">
    <p class="answer reveal">{s['answer']}</p>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Scope</span><span class="lbl">What this covers</span></div>
    <div class="split">
      <div class="prose reveal">
        <h2>What it <em>involves.</em></h2>
        <p>{s['intro']}</p>
        <h3>Typical scope</h3>
        <ul>{''.join(f'<li>{i}</li>' for i in s['includes'])}</ul>
      </div>
      <div class="split-fig">{plate(s['img'], html.unescape(s['title']), 'AG-DETAIL', sizes='(max-width:860px) 100vw, 50vw')}</div>
    </div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Options</span><span class="lbl">What the glass can be</span></div>
    <div class="detail reveal">
      <div class="table-scroll"><table class="schedule">
        <thead><tr><th>Option</th><th>When it is used</th></tr></thead><tbody>{opts}</tbody>
      </table></div>
    </div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Selection</span><span class="lbl">Typical make-ups</span></div>
    <div class="table-scroll reveal">
      <table class="schedule">
        <thead><tr><th>Application</th><th>Make-up</th><th>Thickness</th><th>Selected under</th></tr></thead>
        <tbody>{specs}</tbody>
      </table>
    </div>
    <p class="note reveal" style="margin-top:16px">Indicative only. Each job is selected on the measured panel size, the height above floor, what is above and below, and the loads that apply. <a href="/standards/">How AS 1288 is applied →</a></p>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Notes</span><span class="lbl">{html.unescape(s['title'])}</span></div>
    <div class="faq reveal">{faq}</div>
  </section>

  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Also</span><span class="lbl">Other services</span></div>
    <div class="ledger">{ledger}</div>
  </section>

  <section class="sect cta">
    <div class="wrap">
      <span class="lbl lbl--orange">Next step</span>
      <h2 style="margin:14px 0 16px">Send a photo.<br>Get a <em>real answer.</em></h2>
      <p class="lead">A photo of the opening, the suburb and a rough size is enough for us to tell you what is possible.</p>
      <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
      <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
    </div>
  </section>
</main>"""
    shell(f"{html.unescape(s['title'])} Melbourne — Anderson Glass & Glazing",
          html.unescape(s["answer"])[:150], f"/services/{s['slug']}/", body,
          active="/services/", extra_json=[svc_ld, faq_ld, crumbs], og_img=s["img"])


def build_services_index():
    ledger = "".join(f'<a href="/services/{s["slug"]}/"><span class="n">{i:02d}</span>'
                     f'<span class="nm">{s["title"]}</span><span class="ds">{s["short"]}</span>'
                     f'<span class="ar">{ARROW}</span></a>' for i, s in enumerate(SERVICES, 1))
    body = f"""
<main id="main">
  {phero("Services", "Five lines of <em>glass work.</em>",
         "Commercial glazing, office partitions, shower screens, replacement glass and mirrors — supplied and installed across Melbourne by the same glazier.",
         [("/", "Home")], fig="office-floor", ref="INDEX")}
  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Sheet 01 — Scope</span><span class="lbl">All services</span></div>
    <div class="ledger reveal">{ledger}</div>
  </section>
  <section class="sect wrap">
    <div class="split">
      <div class="prose reveal">
        <h2>Three rules,<br>every <em>job.</em></h2>
        <p>Measure the opening as it is now, not as the drawing says it will be. Name the make-up and the standard it is selected under, in writing. Install it with the person who measured it on site.</p>
        <p>It sounds obvious. It is also the difference between a screen that still closes cleanly in five years and one that does not close cleanly in five weeks.</p>
      </div>
      <div class="split-fig">{plate('partition-run', 'Partition run', 'AG-021', sizes='(max-width:860px) 100vw, 50vw')}</div>
    </div>
  </section>
  <section class="sect cta">
    <div class="wrap">
      <span class="lbl lbl--orange">Start here</span>
      <h2 style="margin:14px 0 16px">Not sure which<br>one you <em>need?</em></h2>
      <p class="lead">Send a photo and describe what you are trying to achieve. We will tell you which trade the job actually is.</p>
      <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
      <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
    </div>
  </section>
</main>"""
    shell("Glazing services Melbourne — Anderson Glass & Glazing",
          "Commercial glazing, office partitions, shower screens, glass replacement and mirrors across Melbourne. Measured, made and installed.",
          "/services/", body, active="/services/")


# ---------------------------------------------------------------- projects

def build_projects():
    stories = "".join(f"""<a class="plate reveal" href="/projects/{p['slug']}/" style="display:block">
      {img(p['img'], p['name'], sizes='(max-width:900px) 100vw, 33vw')}
      <figcaption><b>{p['name']}</b><span>{p['facts'][0][1]}</span></figcaption>
    </a>""" for p in PROJECTS)

    layout = ["plate--w", "", "", "", "", "plate--w", "", "plate--w", ""]
    plates = "".join(plate(nm, cap, f"AG-{i+1:02d}", cls=layout[i % len(layout)], alt=cap)
                     for i, (nm, cap, tags, _c) in enumerate(GALLERY))

    body = f"""
<main id="main">
  {phero("Work", "Considered glazing.<br>Real <em>sites.</em>",
         "Offices, fitouts and bathrooms across Melbourne — photographed on completion. No stock imagery passed off as our work.",
         [("/", "Home")], fig="office-floor", ref="PLATES")}
  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Sheet 01 — Project stories</span><span class="lbl">Three jobs in detail</span></div>
    <div class="plates" style="grid-template-columns:repeat(3,1fr)">{stories}</div>
    <style>.plates a.plate{{grid-column:auto!important}}</style>
  </section>
  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Sheet 02 — Plates</span><span class="lbl">Gallery</span></div>
    <div class="plates">{plates}</div>
  </section>
  <section class="sect cta">
    <div class="wrap">
      <span class="lbl lbl--orange">Your job next</span>
      <h2 style="margin:14px 0 16px">Send us the<br><em>opening.</em></h2>
      <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
      <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
    </div>
  </section>
</main>"""
    shell("Projects — Anderson Glass & Glazing, Melbourne",
          "Completed glazing projects across Melbourne: office fitouts, glass partitions, mirrors and frameless shower screens.",
          "/projects/", body, active="/projects/", og_img="office-floor")


def build_case(p):
    facts = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in p["facts"])
    paras = "".join(f"<p>{t}</p>" for t in p["body"])
    body = f"""
<main id="main">
  {phero("Project", p['name'], p['lede'], [("/", "Home"), ("/projects/", "Work")], fig=p['img'], ref="PLATE")}
  <section class="sect wrap">
    <div class="split">
      <div class="prose reveal">{paras}
        <h3>At a glance</h3>
        <div class="table-scroll"><table class="schedule"><tbody>{facts}</tbody></table></div>
      </div>
      <div class="split-fig">{plate(p['img'], p['name'], 'AG-PLATE', sizes='(max-width:860px) 100vw, 50vw')}</div>
    </div>
  </section>
  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Also on this site</span><span class="lbl">Plates</span></div>
    <div class="plates">{''.join(plate(nm, cap, f'AG-{i+1:02d}', cls='', alt=cap) for i, (nm, cap, t, c) in enumerate(GALLERY[:6]))}</div>
  </section>
  <section class="sect cta">
    <div class="wrap">
      <span class="lbl lbl--orange">Similar job?</span>
      <h2 style="margin:14px 0 16px">Let's look at<br>your <em>space.</em></h2>
      <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
      <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
    </div>
  </section>
</main>"""
    shell(f"{p['name']} — Anderson Glass & Glazing", html.unescape(p["lede"]),
          f"/projects/{p['slug']}/", body, active="/projects/", og_img=p["img"])


# ---------------------------------------------------------------- areas

def build_area(a):
    subs = "".join(f"<li>{s}</li>" for s in a["suburbs"])
    ledger = "".join(f'<a href="/services/{s["slug"]}/"><span class="n">{i:02d}</span>'
                     f'<span class="nm">{s["title"]}</span><span class="ds">{s["short"]}</span>'
                     f'<span class="ar">{ARROW}</span></a>' for i, s in enumerate(SERVICES, 1))
    body = f"""
<main id="main">
  {phero("Service area", f"{a['name']}<br><em>glazing.</em>", a['blurb'],
         [("/", "Home"), ("/service-areas/", "Areas")], fig="office-floor", ref="AREA")}
  <section class="sect wrap">
    <div class="split">
      <div class="prose reveal">
        <h2>What we do in <em>{a['name'].split()[0]}.</em></h2>
        <p>Commercial glazing, office partitions, shower screens, glass replacement and mirrors — supplied and installed. Site visits are scheduled by corridor, so the drive is part of the plan rather than an extra.</p>
        <h3>Suburbs we work in</h3>
        <ul style="columns:2;column-gap:24px">{subs}</ul>
        <p class="note">Outside this list? Ask — larger jobs travel further.</p>
      </div>
      <div class="split-fig">{plate('meeting-room', 'Meeting room glazing', 'AG-AREA', sizes='(max-width:860px) 100vw, 50vw')}</div>
    </div>
  </section>
  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Scope</span><span class="lbl">Available in {a['name']}</span></div>
    <div class="ledger reveal">{ledger}</div>
  </section>
  <section class="sect cta">
    <div class="wrap">
      <span class="lbl lbl--orange">{a['name']}</span>
      <h2 style="margin:14px 0 16px">Send a photo.<br>We'll <em>reply.</em></h2>
      <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
      <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
    </div>
  </section>
</main>"""
    shell(f"Glazing {a['name']} — Anderson Glass & Glazing", html.unescape(a["blurb"]),
          f"/service-areas/{a['slug']}/", body, active="/service-areas/")


def build_areas_index():
    body = f"""
<main id="main">
  {phero("Coverage", "Melbourne metro,<br>and <em>beyond.</em>",
         "Site visits are scheduled by corridor. These are the areas we work in most weeks.",
         [("/", "Home")], ref="COVERAGE")}
  <section class="sect wrap">
    <div class="areas reveal">
      {''.join(f'<a class="area" href="/service-areas/{a["slug"]}/"><h3>{a["name"]}</h3><p>{a["blurb"]}</p><span class="go">View area {ARROW}</span></a>' for a in AREAS)}
      <a class="area area--ask" href="/quote/"><h3>Somewhere else?</h3><p>Give us the suburb and the scope. We will tell you honestly whether the drive makes sense.</p><span class="go">Ask us {ARROW}</span></a>
    </div>
  </section>
  <section class="sect cta">
    <div class="wrap">
      <span class="lbl lbl--orange">Not listed?</span>
      <h2 style="margin:14px 0 16px">Ask <em>anyway.</em></h2>
      <p class="lead">Give us the suburb and the scope. If it is outside a regular corridor we will tell you honestly whether the job makes sense to travel for.</p>
      <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
      <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
    </div>
  </section>
</main>"""
    shell("Service areas — Anderson Glass & Glazing, Melbourne",
          "Glazing service areas across Melbourne: south east, inner east, north, bayside and Gippsland.",
          "/service-areas/", body, active="/service-areas/")


# ---------------------------------------------------------------- standards / facts

def build_standards():
    faqs = [
        ("What is AS 1288?", "AS 1288 is the Australian Standard for glass in buildings — selection and installation. It sets out how thick glass must be, and whether it must be safety glass, based on the panel size, the height above the floor, the location in the building and the loads it has to resist."),
        ("What is Grade A safety glass?", "Grade A safety glass is toughened or laminated glass that meets AS 2208. If it breaks, toughened glass breaks into small blunt fragments and laminated glass stays in its frame rather than falling as large shards."),
        ("Why can't one thickness suit every job?", "Because the requirement scales with area and height. A 600mm panel low in a wall and a 2.4m panel in the same wall can need different make-ups, and both are legal. The standard is applied to the actual opening, not to the product name."),
        ("What does a glazing certificate certify?", "It identifies the job, the glass supplied, its make-up and thickness, the standard it was selected under, and who installed it. It is a record of what was installed — not a warranty of the building."),
        ("Does this page specify the glass for my project?", "No. This is an explanation of how selection works. The specification for your job comes from the measured panel, its location and the applicable loads — which is what the quote and certificate record."),
    ]
    faq = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="a">{a}</div></details>' for q, a in faqs)
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
               "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    body = f"""
<main id="main">
  {phero("Standards", "What AS 1288 means<br>for your <em>glazing.</em>",
         "Glass is selected against the opening it goes into — its size, its height above the floor, what is above it and what it has to resist. Not against a product brochure.",
         [("/", "Home")], fig="bathroom-mirrors", ref="REFERENCE")}
  <section class="sect wrap">
    <div class="split">
      <div class="prose reveal">
        <h2>Selection, not <em>preference.</em></h2>
        <p>AS 1288 is the standard that decides what glass is permitted in a given location in a building. It works from measurable things: the area of the pane, the height of the bottom edge above the floor, whether it is in a door or beside one, whether people are likely to walk into it, and the loads — wind, human impact, or what sits above.</p>
        <p>Two consequences follow, and both matter commercially. First, a quote that names a glass "type" without a thickness is not a quote for a compliant installation. Second, replacing broken glass like-for-like is not automatically correct — the requirement belongs to the location, not the old pane.</p>
        <h3>What we record on every job</h3>
        <ul>
          <li>The application and the measured panel size</li>
          <li>The make-up and nominal thickness supplied</li>
          <li>The standard the selection was made under</li>
          <li>Who measured, supplied and installed</li>
        </ul>
      </div>
      <div class="detail reveal">
        <h3>Standards we work to</h3>
        <div class="table-scroll"><table class="schedule">
          <thead><tr><th>Standard</th><th>Covers</th></tr></thead>
          <tbody>
            <tr><td>AS 1288</td><td>Glass in buildings — selection and installation</td></tr>
            <tr><td>AS 2208</td><td>Safety glazing materials (Grade A / Grade B)</td></tr>
            <tr><td>AS 4666</td><td>Insulating glass units</td></tr>
            <tr><td>AS 1178</td><td>Glass in balustrades and barriers</td></tr>
            <tr><td>AS 1428.1</td><td>Visibility of glazed doors and walls</td></tr>
          </tbody>
        </table></div>
        <p class="note" style="margin-top:14px">Where a project has a specification, a builder's detail or a certifier's requirement, that governs.</p>
      </div>
    </div>
  </section>
  <section class="sect wrap">
    <div class="sect-meta"><span class="lbl">Notes</span><span class="lbl">Standards explained</span></div>
    <div class="faq reveal">{faq}</div>
  </section>
  <section class="sect cta">
    <div class="wrap">
      <span class="lbl lbl--orange">Your job</span>
      <h2 style="margin:14px 0 16px">Ask about<br>your <em>opening.</em></h2>
      <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
      <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
    </div>
  </section>
</main>"""
    shell("AS 1288 glass selection explained — Anderson Glass & Glazing",
          "How AS 1288 and AS 2208 decide glass thickness and safety glass for windows, doors, partitions and shower screens in Melbourne.",
          "/standards/", body, active="/standards/", extra_json=[faq_ld])


def build_facts():
    rows = [
        ("Registered name", ORG["legal"]), ("ABN", ORG["abn"]), ("ACN", ORG["acn"]),
        ("Phone", ORG["phone"]), ("Email", ORG["email"]),
        ("Based in", f"{ORG['location']}"),
        ("Service area", "Melbourne metro; Gippsland by schedule"),
        ("Trades", "Commercial glazing · office partitions · shower screens · glass replacement · mirrors"),
        ("Supply model", "Supply and install; measure and quote by appointment"),
        ("Pricing", "Quoted per job after measure — no published rates"),
        ("Machine-readable", "andersonglass.com.au/facts.json"),
    ]
    table = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    body = f"""
<main id="main">
  {phero("Facts", "Business facts,<br>in <em>plain text.</em>",
         "Written for people and for machines: what the business is, who runs it, where it works and what it does. No claim that cannot be checked.",
         [("/", "Home")], ref="FACTS")}
  <section class="sect wrap">
    <div class="table-scroll reveal"><table class="schedule"><tbody>{table}</tbody></table></div>
    <div class="prose reveal" style="margin-top:36px">
      <h2>What we do not do</h2>
      <p>We do not publish price lists, because a compliant glass make-up depends on the measured opening. We do not sell ready-made screens or flat-pack. We do not run a call centre — the number goes to the person who will measure and install the job.</p>
      <h2>Quoting</h2>
      <p>Measure and quote is free across Melbourne metro. The quote names the application, the make-up, the thickness, the hardware and the inclusions, and states the lead time at the time of quoting rather than as a website promise.</p>
      <h2>Records</h2>
      <p>Glazing certificates are issued where the job requires one: construction work, builder-specified work, and safety glass installations. The certificate records the glass supplied and the standard it was selected under.</p>
      <h2>For machines</h2>
      <p>The same facts are published as JSON at <a href="/facts.json">/facts.json</a>, with services, standards, coverage and quoting policy. Crawlers are explicitly welcome — see <a href="/robots.txt">robots.txt</a> and <a href="/llms.txt">llms.txt</a>.</p>
    </div>
  </section>
  <section class="sect cta">
    <div class="wrap">
      <span class="lbl lbl--orange">Contact</span>
      <h2 style="margin:14px 0 16px">Talk to the<br><em>glazier.</em></h2>
      <div class="contact">
        <a href="tel:{ORG['tel']}"><strong>Phone</strong><span>{ORG['phone']}</span></a>
        <a href="mailto:{ORG['email']}"><strong>Email</strong><span>{ORG['email']}</span></a>
      </div>
    </div>
  </section>
</main>"""
    shell("Business facts — Anderson Glass & Glazing",
          "Anderson Glass & Glazing Pty Ltd — ABN, ACN, contact, service area, trades and quoting policy in plain text.",
          "/facts/", body, active="/facts/")


def build_quote():
    body = f"""
<main id="main">
  {phero("Quote", "Tell us about<br>the <em>opening.</em>",
         "A photo, the suburb and a rough size is enough to start. You will get a real answer — which glass, what thickness, why.",
         [("/", "Home")], ref="ENQUIRY")}
  <section class="sect wrap">
    <div class="cta-grid">
      <div class="reveal">
        <div class="contact">
          <a href="tel:{ORG['tel']}"><strong>Phone</strong><span>{ORG['phone']} — fastest for anything broken</span></a>
          <a href="mailto:{ORG['email']}"><strong>Email</strong><span>{ORG['email']}</span></a>
          <div><strong>Based in</strong><span>{ORG['location']}</span></div>
        </div>
        <h3 style="margin:32px 0 14px">What helps most</h3>
        <ul style="display:grid;gap:10px">
          <li style="display:flex;gap:12px"><span class="mono" style="color:var(--orange)">01</span><span style="font-size:.9rem">A photo of the opening, with something for scale</span></li>
          <li style="display:flex;gap:12px"><span class="mono" style="color:var(--orange)">02</span><span style="font-size:.9rem">Rough width and height — a tape measure is fine</span></li>
          <li style="display:flex;gap:12px"><span class="mono" style="color:var(--orange)">03</span><span style="font-size:.9rem">New build or replacement, and the suburb</span></li>
          <li style="display:flex;gap:12px"><span class="mono" style="color:var(--orange)">04</span><span style="font-size:.9rem">Anything the photos do not show — access, stairs, who else is on site</span></li>
        </ul>
      </div>
      <form class="form reveal" data-enquiry novalidate>
        <div class="form-row">
          <div class="field"><label for="n2">Name</label><input id="n2" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="p2">Phone</label><input id="p2" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="e2">Email</label><input id="e2" name="email" type="email" autocomplete="email"></div>
          <div class="field"><label for="s2">Suburb</label><input id="s2" name="suburb" type="text" autocomplete="address-level2"></div>
        </div>
        <div class="field"><label for="sv2">What is it for?</label>
          <select id="sv2" name="service">{''.join(f'<option>{s["title"]}</option>' for s in SERVICES)}<option>Mirrors / splashback</option><option>Something else</option></select>
        </div>
        <div class="field"><label for="m2">Details</label><textarea id="m2" name="message" placeholder="Rough width and height, new build or replacement, anything the photos do not show."></textarea></div>
        <div aria-hidden="true" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden">
          <label for="cw">Company website</label>
          <input id="cw" name="company_website" type="text" tabindex="-1" autocomplete="off">
        </div>
        <button class="btn btn--lg" type="submit">Send enquiry {ARROW}</button>
        <p class="form-note">Goes straight to our inbox — no third-party marketing platform, no tracking. We reply to the email address or phone number you give us; photos can follow by reply.</p>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>
</main>"""
    shell("Request a quote — Anderson Glass & Glazing, Melbourne",
          "Request a glazing quote in Melbourne: send a photo, the suburb and a rough size. Commercial glazing, partitions, shower screens, replacement glass and mirrors.",
          "/quote/", body)


def build_404():
    body = """
<main id="main">
  <section class="sect wrap" style="padding-block:clamp(90px,14vw,180px)">
    <span class="lbl lbl--orange">404 — Sheet not found</span>
    <h1 style="margin:14px 0 18px">That sheet<br>isn't in the <em>set.</em></h1>
    <p class="lead">The link is old, or the glass slipped. Try one of these instead.</p>
    <div class="hero-actions" style="margin-top:26px">
      <a class="btn btn--lg" href="/">Home</a>
      <a class="btn btn--lg btn--ghost" href="/services/">Services</a>
      <a class="btn btn--lg btn--ghost" href="/quote/">Request a quote</a>
    </div>
  </section>
</main>"""
    shell("Page not found — Anderson Glass & Glazing", "That page could not be found.", "/404.html", body)


# ---------------------------------------------------------------- meta files

def build_meta():
    pages = ["/", "/services/", "/projects/", "/service-areas/", "/standards/", "/facts/", "/quote/"]
    pages += [f"/services/{s['slug']}/" for s in SERVICES]
    pages += [f"/service-areas/{a['slug']}/" for a in AREAS]
    pages += [f"/projects/{p['slug']}/" for p in PROJECTS]
    today = "2026-11-07"
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        pri = "1.0" if p == "/" else ("0.9" if p.startswith("/services/") or p == "/quote/" else "0.7")
        sm += f"  <url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority></url>\n"
    sm += "</urlset>\n"
    (OUT / "sitemap.xml").write_text(sm, encoding="utf-8")

    robots = "User-agent: *\nAllow: /\n\n# AI / answer engines — explicitly welcome\n" + "".join(
        f"\nUser-agent: {b}\nAllow: /\n" for b in
        ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-Web", "PerplexityBot",
         "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "CCBot", "Bingbot", "DuckDuckBot"])
    robots += f"\nSitemap: {SITE}/sitemap.xml\n"
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")

    facts = {
        "@context": "https://schema.org",
        "@type": ["Organization", "HomeAndConstructionBusiness"],
        "name": ORG["name"], "legalName": ORG["legal"], "url": SITE + "/",
        "telephone": ORG["tel"], "email": ORG["email"],
        "identifiers": {"ABN": ORG["abn"], "ACN": ORG["acn"]},
        "address": {"addressLocality": ORG["suburb"],
                    "addressRegion": ORG["state"], "postalCode": ORG["postcode"], "addressCountry": "AU"},
        "areaServed": ["Melbourne", "Gippsland"] + [a["name"] for a in AREAS],
        "services": [{"name": html.unescape(s["title"]), "summary": html.unescape(s["short"]),
                      "url": SITE + f"/services/{s['slug']}/",
                      "includes": [html.unescape(i) for i in s["includes"]],
                      "faq": [{"q": html.unescape(q), "a": html.unescape(a)} for q, a in s["faqs"]]}
                     for s in SERVICES],
        "standards": ["AS 1288", "AS 2208", "AS 4666", "AS 1178", "AS 1428.1"],
        "quoting": {
            "model": "Measure and quote after site inspection",
            "pricesPublished": False,
            "leadTimes": "Confirmed at quote",
            "certificates": "Issued where required, recording glass supplied and standard applied",
        },
        "updated": "2026-11-07",
    }
    (OUT / "facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")

    llms = f"""# Anderson Glass & Glazing

> Commercial glazing, office partitions, shower screens, glass replacement and mirrors across Melbourne, Victoria. Supplied and installed by the same glazier who measures and quotes. Enquiry-only — pricing is quoted per job after a site measure.

## Business
- Legal name: {ORG['legal']}
- ABN {ORG['abn']} · ACN {ORG['acn']}
- Workshop: {ORG['location']}
- Phone: {ORG['tel']} · Email: {ORG['email']}
- Service area: Melbourne metro (south east, inner east, north, bayside); Gippsland by schedule
- Machine-readable facts: {SITE}/facts.json

## Services
{chr(10).join(f"- {html.unescape(s['title'])}: {html.unescape(s['short'])} ({SITE}/services/{s['slug']}/)" for s in SERVICES)}

## How quoting works
- Measure and quote free across Melbourne metro; the installing glazier attends.
- No published prices: make-up and thickness depend on the measured panel, height above floor and loads (AS 1288).
- Lead times confirmed at quote, not published.
- Glazing certificates issued where required.

## Standards
AS 1288 (glass in buildings), AS 2208 (safety glazing), AS 4666 (IGUs), AS 1178 (balustrades), AS 1428.1 (visibility).

## Pages
{chr(10).join(f"- {SITE}{p}" for p in pages)}
- {SITE}/standards/ — how glass is selected under AS 1288
- {SITE}/facts/ — business facts in plain text
"""
    (OUT / "llms.txt").write_text(llms, encoding="utf-8")
    (OUT / "llms-full.txt").write_text(
        llms + "\n\n" + "\n\n".join(
            f"## {html.unescape(s['title'])}\n{html.unescape(s['answer'])}\n\n"
            + "\n".join(f"- {html.unescape(i)}" for i in s["includes"])
            + "\n\n" + "\n".join(f"Q: {html.unescape(q)}\nA: {html.unescape(a)}" for q, a in s["faqs"])
            for s in SERVICES), encoding="utf-8")

    headers = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Strict-Transport-Security: max-age=31536000
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' https://static.cloudflareinsights.com; connect-src 'self' https://cloudflareinsights.com; font-src 'self'; form-action 'self' mailto:; base-uri 'self'; frame-ancestors 'none'
  Cross-Origin-Opener-Policy: same-origin

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/images/*
  Cache-Control: public, max-age=31536000, immutable

/facts.json
  Cache-Control: public, max-age=3600

/*.html
  Cache-Control: public, max-age=0, must-revalidate
"""
    (OUT / "_headers").write_text(headers, encoding="utf-8")


def build_assets():
    worker = BASE / "_worker.js"
    if worker.exists():
        shutil.copy2(worker, OUT / "_worker.js")
    for sub in ("assets", "images"):
        src = BASE / sub
        dst = OUT / sub
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    (OUT / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" fill="#f1eee6"/>'
        '<g stroke="#14140e" stroke-width="1.8" fill="none"><rect x="5" y="5" width="30" height="30"/>'
        '<path d="M5 13.5h30M13.5 5v30"/></g>'
        '<rect x="13.5" y="13.5" width="9" height="9" fill="#d9451a"/></svg>', encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    build_assets()
    build_home()
    build_services_index()
    for s in SERVICES:
        build_service(s)
    build_projects()
    for p in PROJECTS:
        build_case(p)
    build_areas_index()
    for a in AREAS:
        build_area(a)
    build_standards()
    build_facts()
    build_quote()
    build_404()
    build_meta()
    n = sum(1 for _ in OUT.rglob("*") if _.is_file())
    print(f"built {n} files into {OUT}")


if __name__ == "__main__":
    main()
