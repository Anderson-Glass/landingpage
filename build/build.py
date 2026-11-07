#!/usr/bin/env python3
"""Anderson Glass & Glazing static site generator."""
import json, os, shutil, html
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE.parent / "agsite"
SITE = "https://andersonglass.com.au"

ORG = {
    "name": "Anderson Glass & Glazing",
    "legal": "Anderson Glass & Glazing Pty Ltd",
    "abn": "24 202 344 169",
    "acn": "169 467 216",
    "phone": "0414 441 192",
    "tel": "+61414441192",
    "email": "ben@andersonglass.com.au",
    "street": "",
    "suburb": "Narre Warren East",
    "state": "VIC",
    "postcode": "3804",
    "location": "Narre Warren East, VIC",
    "founded": 2014,
}

NAV = [
    ("/services/", "Services"),
    ("/projects/", "Work"),
    ("/service-areas/", "Areas"),
    ("/standards/", "Standards"),
    ("/facts/", "Facts"),
]

# ---------------------------------------------------------------- content

SERVICES = [
    {
        "slug": "commercial-glazing",
        "title": "Commercial glazing",
        "short": "Shopfronts, entries and full-height glass for commercial fitouts.",
        "img": "office-floor",
        "tags": "commercial",
        "answer": "Anderson Glass &amp; Glazing supplies and installs commercial glazing across Melbourne — shopfronts, automatic and manual glass entries, full-height partition glazing, mirrors and glass balustrades. Work is measured on site, fabricated to those measurements and installed by the same glazier who quoted it.",
        "intro": "Commercial work is judged on the things you only notice when they are wrong: door closers that drift, silicone lines that wander, glass that is 2mm out over a 4m run. We measure, fabricate and install with one person accountable for all three.",
        "includes": [
            "Shopfront framing and glass replacement",
            "Manual and automatic glass entry doors",
            "Full-height and over-height partition glazing",
            "Glass balustrades and pool fencing",
            "Mirrors, splashbacks and wall linings",
            "Make-safe and same-week glass replacement",
        ],
        "options": [
            ("6mm–12mm toughened glass", "Standard for doors, partitions and balustrades where people can come into contact with it."),
            ("Laminated safety glass", "Where the spec calls for it — overhead, sloped, or where a broken pane must stay in the frame."),
            ("Framed and frameless systems", "Aluminium framed shopfront, or frameless with patch fittings and structural silicone."),
            ("Low-iron / ultra-clear", "Removes the green edge tint — used where the glass is the finish, not just the barrier."),
        ],
        "specs": [
            ("Shopfront glass (framed)", "Toughened monolithic", "6mm / 8mm / 10mm", "AS 1288, AS 2208"),
            ("Glass entry door", "Toughened, or laminated where specified", "10mm / 12mm", "AS 1288, AS 2208"),
            ("Full-height partition", "Toughened monolithic or double glazed", "10mm / 12mm / 6-12-6 IGU", "AS 1288, AS 4666"),
            ("Glass balustrade (infill)", "Toughened laminated", "10mm + 10mm or 12mm", "AS 1288, AS 1178"),
            ("Mirror", "Silvered float, safety backed where required", "6mm", "AS 1288"),
        ],
        "faqs": [
            ("Do you work on occupied commercial sites?", "Yes. Most of our work is in operating offices, shops and warehouses. Glass is measured outside working hours where needed, and installations are staged around your trading or staff hours."),
            ("Can you match existing shopfront framing?", "Usually. Send a photo and a couple of dimensions when you enquire and we can tell you before anyone visits whether the existing frame takes new glass or whether the frame needs replacing too."),
            ("Do you provide glazing certificates?", "Yes — the certificate identifies the glass, the make-up, the standard it was selected under (AS 1288) and the installer. It is issued for the job, not copied from a template."),
            ("Who measures?", "The person who quotes measures. That is deliberate: a quote built on someone else's measurements is a quote for a different job."),
        ],
    },
    {
        "slug": "office-partitions",
        "title": "Office partitions",
        "short": "Framed, frameless and demountable glass partition systems.",
        "img": "partition-run",
        "tags": "commercial",
        "answer": "Office partition glazing turns floor area into rooms without losing light. Anderson Glass installs framed aluminium, frameless and demountable glass partition systems for Melbourne offices and warehouses — measured to the tenancy, with doors, manifestation and acoustic detailing resolved before fabrication.",
        "intro": "A partition is a small building inside a building. Head channels have to land on something solid, floors are never as level as the drawings say, and the acoustic result depends on the detail at the frame, not the glass alone.",
        "includes": [
            "Framed aluminium partition systems",
            "Frameless butt-jointed glass walls",
            "Demountable and relocatable partitions",
            "Glass and timber doors, patch fittings, closers",
            "Manifestation and privacy film to AS 1428 sight lines",
            "Acoustic and double-glazed options",
        ],
        "options": [
            ("10mm frameless", "Maximum light, minimum visual weight — patch fittings or channel fixed."),
            ("Aluminium framed", "More economical over long runs, takes integrated doors and blinds."),
            ("Double glazed", "Where acoustic separation matters — meeting rooms, consulting rooms, workshops."),
            ("Demountable", "Built to come down when the lease ends, without destroying the glass."),
        ],
        "specs": [
            ("Frameless partition", "Toughened monolithic", "10mm / 12mm", "AS 1288, AS 2208"),
            ("Framed partition", "Toughened or laminated", "6mm – 10mm", "AS 1288, AS 2208"),
            ("Acoustic partition", "Double glazed unit", "6-12-6 or 6-16-6", "AS 1288, AS 4666"),
            ("Partition door", "Toughened, patch fitted", "10mm / 12mm", "AS 1288"),
            ("Manifestation", "Applied film", "—", "AS 1428.1 sight lines"),
        ],
        "faqs": [
            ("Can partitions be added while we keep working?", "Usually yes. Partition glazing is staged in sections, and the noisiest work — cutting, drilling, silicone — is scheduled before hours or in a defined window."),
            ("Do I need consent or a permit?", "That depends on the building and whether the work touches base build services, fire systems or egress. We will tell you when a partition run is likely to need building approval before we quote it."),
            ("Can I reuse partitions when I move?", "If they were built demountable. A frameless system is generally fixed to the tenancy — worth deciding at the start."),
        ],
    },
    {
        "slug": "shower-screens",
        "title": "Shower screens",
        "short": "Frameless and semi-frameless screens, measured and installed.",
        "img": "frameless-shower",
        "tags": "residential",
        "answer": "A frameless shower screen is 10mm toughened safety glass, cut and drilled to your opening and fixed with hinges and brackets rather than a frame. Anderson Glass measures the actual opening — walls are never square — fabricates to those millimetres, and installs with the door swing and screen heights set before the glass is tempered.",
        "intro": "Shower screens fail at the measurements, not the glass. Out-of-square walls, a fall in the floor, a tile edge that sits proud — each one millimetres, and each one enough to make a pre-made screen leak or a door bind.",
        "includes": [
            "Frameless 10mm screens and doors",
            "Semi-frameless and framed screens",
            "Pivot, hinged and sliding configurations",
            "Return panels and fixed panels",
            "Mirrors and bathroom splashbacks",
            "Replacement glass for existing screens",
        ],
        "options": [
            ("Frameless 10mm", "Toughened, polished edges, minimal hardware — the cleanest result."),
            ("Semi-frameless", "A frame on the fixed panels, frameless door — a middle ground on cost."),
            ("Sliding", "Where the door cannot swing out into the room."),
            ("Easy-clean coating", "Applied to the glass face to slow mineral build-up."),
        ],
        "specs": [
            ("Frameless screen", "Toughened monolithic", "10mm", "AS 1288, AS 2208"),
            ("Semi-frameless screen", "Toughened monolithic", "6mm / 8mm", "AS 1288, AS 2208"),
            ("Sliding screen", "Toughened monolithic", "6mm / 8mm", "AS 1288, AS 2208"),
            ("Fixed return panel", "Toughened monolithic", "8mm / 10mm", "AS 1288"),
        ],
        "faqs": [
            ("Do you measure before or after tiling?", "After. Screen dimensions need the finished tile face and floor fall, so measuring happens once tiling and waterproofing are complete."),
            ("Can you replace just the glass?", "Often — if the hinges and brackets are reusable and the opening has not moved. Send a photo of the hardware and the screen and we will tell you."),
            ("How long between measure and install?", "Typically one to two weeks, because toughened glass has to be cut, drilled and heat-treated to your exact dimensions. Confirm the date at quote."),
        ],
    },
    {
        "slug": "glass-replacement",
        "title": "Glass replacement",
        "short": "Broken windows, doors and shopfronts — make safe and replace.",
        "img": "cubicle-2",
        "tags": "residential commercial",
        "answer": "Glass replacement covers broken or cracked windows, doors, shopfronts and mirrors. Anderson Glass makes the opening safe first, measures the frame as it actually is, and replaces the pane in the correct make-up and thickness for that location under AS 1288 — not simply the thickness the old pane happened to be.",
        "intro": "A broken pane is rarely just a broken pane. The glass broke for a reason — impact, movement, or a make-up that was never right for the location — and replacing like-for-like can mean replacing it again.",
        "includes": [
            "Emergency make-safe and board-up",
            "Window and door glass replacement",
            "Shopfront and entry glass",
            "Mirror and splashback replacement",
            "Upgrade to safety glass where required",
            "Insurance documentation and photos",
        ],
        "options": [
            ("Standard float", "Where the location does not require safety glass."),
            ("Toughened safety glass", "Doors, side panels, low glass and wet areas."),
            ("Laminated safety glass", "Where the pane must hold together — overhead, security, balustrades."),
            ("Obscure and textured", "Privacy glass for bathrooms and street-facing windows."),
        ],
        "specs": [
            ("Window glass (above 500mm)", "Float or toughened", "4mm – 6mm", "AS 1288"),
            ("Glass in doors and side panels", "Toughened or laminated", "5mm – 6mm", "AS 1288, AS 2208"),
            ("Low-level glazing", "Grade A safety glass", "6mm – 10mm", "AS 1288, AS 2208"),
            ("Shopfront", "Toughened", "6mm – 10mm", "AS 1288"),
        ],
        "faqs": [
            ("Can you make it safe today?", "Most days, yes — board-up or removal of loose glass can usually be arranged the same day across Melbourne metro. Call rather than email for anything unsafe."),
            ("Will insurance cover it?", "Depends on your policy. We photograph the damage, note the make-up replaced and provide an invoice you can submit."),
            ("The old glass was thinner — do I have to upgrade?", "If the location now requires safety glass, yes. A glazier replacing glass in a regulated location is bound by AS 1288 regardless of what was there before."),
        ],
    },
    {
        "slug": "wardrobes-and-mirrors",
        "title": "Wardrobes &amp; mirrors",
        "short": "Mirror wardrobe doors, splashbacks and wall mirrors.",
        "img": "timber-grid",
        "tags": "residential",
        "answer": "Anderson Glass supplies and installs mirror wardrobe doors, glass splashbacks and wall mirrors — measured to the opening, cut with polished or bevelled edges, and fixed with hardware rated for the door weight. Sliding mirror doors are the usual choice where swing space is tight.",
        "intro": "Mirror is unforgiving: it shows every millimetre of an out-of-square wall and every mark left on the back of the glass. The installation matters as much as the mirror itself.",
        "includes": [
            "Sliding mirror wardrobe doors",
            "Hinged mirror doors",
            "Glass splashbacks",
            "Gym and wall mirrors",
            "Replacement mirror for existing tracks",
            "Safety-backed mirror where required",
        ],
        "options": [
            ("2mm / 4mm mirror", "For wall mirrors over a flat, prepared surface."),
            ("6mm safety-backed", "Where glass must not fall as shards — bathrooms and gyms."),
            ("Sliding door systems", "Top-hung and bottom-rolling tracks sized to the opening."),
            ("Glass splashback", "Painted or printed toughened glass, cut around outlets and benches."),
        ],
        "specs": [
            ("Wall mirror", "Silvered float", "4mm / 6mm", "AS 1288"),
            ("Wardrobe mirror door", "Silvered float, safety backed", "4mm / 6mm", "AS 1288"),
            ("Splashback", "Toughened, painted back", "6mm", "AS 1288, AS 2208"),
            ("Gym mirror", "Safety-backed", "6mm", "AS 1288"),
        ],
        "faqs": [
            ("Can you replace mirror only, keeping the tracks?", "Often yes, if the track is sound and the door size is standard. Photograph the track and the top roller and we can advise."),
            ("Do mirrors need safety backing?", "Where they could be struck or where Council or a spec calls for it. In gyms and bathrooms we default to safety-backed."),
        ],
    },
]

AREAS = [
    {
        "slug": "south-east-melbourne",
        "name": "South East Melbourne",
        "blurb": "Home base. Narre Warren, Berwick, Cranbourne, Pakenham, Dandenong and the Casey corridor — same-week site visits are normal here.",
        "suburbs": ["Narre Warren", "Berwick", "Cranbourne", "Pakenham", "Dandenong", "Hallam", "Officer", "Beaconsfield"],
    },
    {
        "slug": "inner-east-melbourne",
        "name": "Inner East Melbourne",
        "blurb": "Office fitouts and period-home glazing from Hawthorn out through Camberwell, Kew and Balwyn.",
        "suburbs": ["Hawthorn", "Camberwell", "Kew", "Balwyn", "Surrey Hills", "Glen Iris", "Richmond", "Box Hill"],
    },
    {
        "slug": "northern-melbourne",
        "name": "Northern Melbourne",
        "blurb": "Warehouse and commercial glazing through Epping, Preston, Thomastown and Craigieburn.",
        "suburbs": ["Epping", "Preston", "Thomastown", "Craigieburn", "Campbellfield", "Reservoir", "Coburg", "Bundoora"],
    },
    {
        "slug": "bayside-melbourne",
        "name": "Bayside Melbourne",
        "blurb": "Shower screens, mirrors and glass replacement through Mentone, Mordialloc and the beachside suburbs.",
        "suburbs": ["Mentone", "Mordialloc", "Cheltenham", "Moorabbin", "Bentleigh", "Brighton", "Sandringham", "Hampton"],
    },
    {
        "slug": "gippsland",
        "name": "Gippsland",
        "blurb": "Larger jobs and scheduled installs through Warragul, Drouin, Traralgon and the Latrobe Valley.",
        "suburbs": ["Warragul", "Drouin", "Traralgon", "Moe", "Morwell", "Leongatha", "Wonthaggi", "Sale"],
    },
]

PROJECTS = [
    {
        "slug": "thorn-office-fitout",
        "name": "Thorn office fitout",
        "tags": "commercial",
        "img": "thorn-fitout",
        "lede": "Full-height framed glass partitions turning an open floor into a suite of offices — with light still reaching the back wall.",
        "body": [
            "An open floor plate was divided into a reception, two enclosed offices and a meeting room using framed aluminium partitions with full-height glass. Keeping the glass to ceiling height was the whole point: the tenancy has a single window exposure, and any solid wall through the middle would have left the rear of the office permanently dark.",
            "Doors were glass with patch fittings so the sight lines through the suite stay uninterrupted. Runs were set out from the finished floor and the ceiling grid so head channels land on structure rather than on plasterboard.",
        ],
        "facts": [("Scope", "Framed glass partitions, doors"), ("Glass", "Toughened, 6–10mm"), ("Standard", "AS 1288, AS 2208")],
    },
    {
        "slug": "chen-foods-offices",
        "name": "Chen Foods offices",
        "tags": "commercial",
        "img": "chen-foods",
        "lede": "Glass partition wall along a corridor, giving offices daylight without opening the space up to a busy thoroughfare.",
        "body": [
            "Office glazing along a working corridor: solid timber doors, full-height glass panels and a framed head detail that follows an existing bulkhead. The brief was privacy for meetings and calls, without the corridor turning into a tunnel.",
            "Glass was kept clear with manifestation at door height only, so the corridor borrows light from the offices and the offices keep a visual connection to the rest of the floor.",
        ],
        "facts": [("Scope", "Corridor partition glazing"), ("Glass", "Toughened, framed"), ("Standard", "AS 1288, AS 2208")],
    },
    {
        "slug": "frameless-shower-screens",
        "name": "Frameless shower screens",
        "tags": "residential",
        "img": "frameless-shower",
        "lede": "10mm frameless screens in a tiled bathroom — door swing and screen heights set before the glass was tempered.",
        "body": [
            "A frameless screen is measured after tiling, when the finished wall and floor faces exist. Here the walls were out of square across the opening, which is normal: the frame is the drawing's idea of the room, the tiles are the room.",
            "Measured to the millimetre, 10mm toughened glass with polished edges, hinged off the return wall with a fixed panel. Hinge positions were set so the door clears the vanity and the floor fall rather than being centred for looks.",
        ],
        "facts": [("Scope", "Frameless screen and fixed panel"), ("Glass", "10mm toughened"), ("Standard", "AS 1288, AS 2208")],
    },
]

GALLERY = [
    ("office-floor", "Open-plan office glazing", "commercial", "tile--wide"),
    ("meeting-room", "Meeting room glass wall", "commercial", "tile"),
    ("open-plan", "Partition run, finished floor to ceiling", "commercial", "tile"),
    ("bathroom-mirrors", "Bathroom mirrors and shower screen", "residential", "tile"),
    ("cubicle-1", "Framed partition with a view through", "commercial", "tile"),
    ("frameless-shower", "Frameless shower screen, 10mm", "residential", "tile--tall"),
    ("timber-grid", "Timber-framed glass partition", "commercial", "tile"),
    ("cubicle-3", "Office cubicle glazing", "commercial", "tile"),
    ("hero-corridor", "Glass corridor, warm light", "commercial", "tile--wide"),
]

HOME_FAQ = [
    ("Do you give prices over the phone?",
     "No — and it is not a sales tactic. Glass is cut to the opening, and the make-up that is legal for that location (AS 1288) changes with the application, the panel size and what is above and below it. A number given without seeing the opening is a number that will not hold. Measure and quote is free across Melbourne metro; the quote names the glass, the thickness and what is included."),
    ("Are you licensed and insured?",
     "Anderson Glass &amp; Glazing Pty Ltd is a registered company (ACN 169 467 216, ABN 24 202 344 169) working across Melbourne metro. Current public liability and workers compensation details are provided with any quote or site induction pack."),
    ("What areas do you cover?",
     "Melbourne metro, with same-week visits across the south east, inner east, north and bayside. Gippsland work is scheduled in blocks. If you are further out, ask — larger jobs travel."),
    ("How long does a job take?",
     "Shower screens and mirrors are typically one to two weeks from measure, because toughened glass is made to your dimensions. Replacement glass can be same-day or next-day for common sizes. Installation itself is usually a few hours. Lead times are confirmed at quote, not published, because they move with supplier load."),
    ("Do you supply and install, or install only?",
     "Both supply and install. That is the point: one party accountable for the measurement, the glass, the hardware and the finished result."),
    ("What should I send with an enquiry?",
     "A photo of the opening, a rough width and height if you can, the suburb, and whether it is a new build or a replacement. A photo tells us more than a paragraph, and rough dimensions let us tell you what is possible before a site visit."),
]


# ---------------------------------------------------------------- helpers

def esc(s):
    return html.escape(s, quote=False)

def url(path):
    return SITE + path if path != "/" else SITE + "/"

def picture(name, alt, widths=(1920, 1280, 800, 480), sizes="100vw", cls="", loading="lazy", priority=False):
    srcset = ", ".join(f"/images/{name}-{w}.webp {w}w" for w in widths)
    lp = ' fetchpriority="high"' if priority else f' loading="{loading}"'
    return (
        f'<img src="/images/{name}-1280.webp" srcset="{srcset}" sizes="{sizes}" '
        f'alt="{alt}" width="1280" height="960"{lp}{" class="+chr(34)+cls+chr(34) if cls else ""} decoding="async">'
    )


def head(title, desc, path, extra_json=None, og_img="hero-corridor"):
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["Organization", "HomeAndConstructionBusiness"],
                "@id": SITE + "/#org",
                "name": ORG["name"],
                "legalName": ORG["legal"],
                "url": SITE + "/",
                "telephone": ORG["tel"],
                "email": ORG["email"],
                "image": SITE + "/images/hero-corridor-1280.webp",
                "logo": SITE + "/assets/favicon.svg",
                "priceRange": "Quote on inspection",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": ORG["suburb"],
                    "addressRegion": ORG["state"],
                    "postalCode": ORG["postcode"],
                    "addressCountry": "AU",
                },
                "areaServed": [{"@type": "City", "name": "Melbourne"}]
                + [{"@type": "AdministrativeArea", "name": a["name"]} for a in AREAS],
                "knowsAbout": [
                    "Commercial glazing", "Office partitions", "Shower screens",
                    "Glass replacement", "Mirror wardrobe doors", "AS 1288", "AS 2208",
                ],
                "vatID": "ABN " + ORG["abn"],
                "taxID": ORG["abn"],
            },
            {
                "@type": "WebSite",
                "@id": SITE + "/#website",
                "url": SITE + "/",
                "name": ORG["name"],
                "publisher": {"@id": SITE + "/#org"},
            },
            {
                "@type": "WebPage",
                "@id": url(path) + "#page",
                "url": url(path),
                "name": title,
                "description": desc,
                "isPartOf": {"@id": SITE + "/#website"},
                "about": {"@id": SITE + "/#org"},
            },
        ],
    }
    if extra_json:
        ld["@graph"].extend(extra_json)
    ld_json = json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url(path)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="geo.region" content="AU-VIC">
<meta name="geo.placename" content="Melbourne">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Anderson Glass &amp; Glazing">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{SITE}/images/{og_img}-1280.webp">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a0a0b">
<link rel="preload" href="/assets/fonts/Inter-normal-300_700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts.css">
<link rel="stylesheet" href="/assets/site.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{ld_json}</script>"""


LOGO = """<svg viewBox="0 0 40 40" fill="none" aria-hidden="true">
<rect x="1" y="1" width="38" height="38" stroke="currentColor" stroke-width="1.4"/>
<path d="M1 14h38M14 1v38" stroke="currentColor" stroke-width="1.4"/>
<path d="M14 14h25v25" stroke="currentColor" stroke-width="1.4" opacity=".45"/>
</svg>"""

ARROW = """<svg viewBox="0 0 16 16" width="14" height="14" fill="none" aria-hidden="true"><path d="M3 13L13 3M13 3H5.5M13 3v7.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>"""


def header(active):
    CUR = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}"{CUR if active == href else ""}>{label}</a>'
        for href, label in NAV
    )
    drawer_links = "".join(f'<a href="{href}">{label}</a>' for href, label in NAV)
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="Anderson Glass &amp; Glazing — home">
      {LOGO}
      <span class="brand-txt"><strong>Anderson</strong><span>Glass &amp; Glazing</span></span>
    </a>
    <nav class="nav" aria-label="Primary">{links}</nav>
    <div class="header-tools">
      <button class="icon-btn" data-theme-toggle aria-label="Switch theme">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="1.4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
      </button>
      <a class="btn" href="/quote/">Request a quote {ARROW}</a>
      <button class="icon-btn menu-btn" data-menu aria-expanded="false" aria-label="Menu">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>
</header>
<div class="drawer" aria-label="Menu">
  {drawer_links}
  <a href="/quote/">Request a quote</a>
  <a class="btn btn--lg" href="tel:{ORG['tel']}">Call {ORG['phone']}</a>
</div>"""


def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{s["title"]}</a></li>' for s in SERVICES)
    areas = "".join(f'<li><a href="/service-areas/{a["slug"]}/">{a["name"]}</a></li>' for a in AREAS)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="/" aria-label="Anderson Glass &amp; Glazing — home">
          {LOGO}
          <span class="brand-txt"><strong>Anderson</strong><span>Glass &amp; Glazing</span></span>
        </a>
        <p>Commercial glazing, office partitions, shower screens, glass replacement and mirrors across Melbourne. Measured, made and installed by the same glazier.</p>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Areas</h4><ul>{areas}</ul></div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{ORG['tel']}">{ORG['phone']}</a></li>
          <li><a href="mailto:{ORG['email']}">{ORG['email']}</a></li>
          <li><a href="/quote/">Request a quote</a></li>
          <li><a href="/standards/">Standards</a></li>
          <li><a href="/facts/">Business facts</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {ORG['legal']} · ABN {ORG['abn']} · ACN {ORG['acn']}</span>
      <span>{ORG['location']}</span>
    </div>
  </div>
</footer>"""


def shell(title, desc, path, body, active="", extra_json=None, og_img="hero-corridor"):
    page = f"""<!doctype html>
<html lang="en-AU" data-theme="dark">
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
<script src="/assets/site.js" defer></script>
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


def page_hero(kicker, h1, sub, crumbs, img=None):
    crumb_html = "".join(
        f'<a href="{h}">{t}</a><span>/</span>' for h, t in crumbs
    )
    media = ""
    if img:
        media = f'<div class="hero-media">{picture(img, "", sizes="100vw", priority=True)}</div>'
    return f"""<section class="page-hero{' page-hero--plain' if not img else ''}"{' style="min-height:min(78svh,720px)"' if img else ''}>
  {media}
  <div class="wrap">
    <div class="crumbs">{crumb_html}<span style="color:var(--ink-2)">{h1 if len(h1) < 30 else kicker}</span></div>
    <span class="kicker">{kicker}</span>
    <h1>{h1}</h1>
    <p class="lead">{sub}</p>
  </div>
</section>"""


# ---------------------------------------------------------------- pages

def build_home():
    svc_cards = ""
    for s in SERVICES:
        svc_cards += f"""    <a class="svc reveal" href="/services/{s['slug']}/" data-delay="{min(len(svc_cards)//300, 4)}">
      {picture(s['img'], '', sizes='(max-width:620px) 100vw, (max-width:1000px) 50vw, 33vw')}
      <h3>{s['title']}</h3>
      <p>{s['short']}</p>
      <span class="svc-go">Explore {ARROW}</span>
    </a>
"""

    tiles = ""
    for i, (img, cap, tags, cls) in enumerate(GALLERY):
        if i == len(GALLERY) - 1:
            cls = "tile--full"
        tiles += f"""      <figure class="{cls} tile reveal" data-tags="{tags}" data-lightbox data-full="/images/{img}-1920.webp" data-delay="{i%3}">
        {picture(img, cap, sizes='(max-width:620px) 100vw, (max-width:900px) 50vw, 33vw')}
        <figcaption>{cap}</figcaption>
      </figure>
"""

    faq_html = ""
    for q, a in HOME_FAQ:
        faq_html += f"""      <details>
        <summary>{q}<i aria-hidden="true"></i></summary>
        <div class="answer">{a}</div>
      </details>
"""

    faq_ld = {
        "@type": "FAQPage",
        "@id": SITE + "/#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in HOME_FAQ
        ],
    }
    services_ld = {
        "@type": "OfferCatalog",
        "name": "Glazing services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"], "url": url(f"/services/{s['slug']}/")}}
            for s in SERVICES
        ],
    }

    body = f"""
<main id="main">
  <section class="hero">
    <div class="hero-media">{picture('hero-corridor', '', sizes='100vw', priority=True)}</div>
    <div class="wrap hero-inner">
      <span class="kicker">Melbourne · glass &amp; glazing</span>
      <h1>
        <span class="line"><span>Glass that makes</span></span>
        <span class="line"><span>a space <em class="serif gold" style="font-style:italic">work.</em></span></span>
      </h1>
      <div class="hero-foot">
        <div>
          <p class="lead">Commercial glazing, office partitions, shower screens, replacements and mirrors. Measured, made and installed — by the same glazier who quoted it.</p>
          <div class="hero-actions" style="margin-top:26px">
            <a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
            <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a>
          </div>
        </div>
        <div class="hero-note">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v18M12 21l-5-5M12 21l5-5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
          <span>From measure and quote<br>to supply and install.</span>
        </div>
      </div>
    </div>
    <div class="scroll-cue"><span>Scroll</span><i></i></div>
  </section>

  <section class="wrap">
    <div class="facts reveal">
      <div><b data-count="10" data-suffix="+">10+</b><span>Years on the tools</span></div>
      <div><b data-count="5">5</b><span>Service lines</span></div>
      <div><b>AS 1288</b><span>Selected to standard</span></div>
      <div><b>Melbourne</b><span>Metro-wide coverage</span></div>
    </div>
  </section>

  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
      <span>Shopfronts</span><span>Office partitions</span><span>Frameless screens</span><span>Glass replacement</span><span>Mirror wardrobes</span><span>Splashbacks</span><span>Balustrades</span>
      <span>Shopfronts</span><span>Office partitions</span><span>Frameless screens</span><span>Glass replacement</span><span>Mirror wardrobes</span><span>Splashbacks</span><span>Balustrades</span>
    </div>
  </div>

  <section class="section wrap" id="services">
    <div class="head head--split reveal">
      <div>
        <span class="kicker">What we do</span>
        <h2 style="margin-top:16px">Five trades,<br>one <span class="serif">standard.</span></h2>
      </div>
      <p class="lead">Every job runs the same way: measure the opening as it actually is, name the glass and the standard it is selected under, then install it.</p>
    </div>
    <div class="services">
{svc_cards}    </div>
  </section>

  <section class="section section--line wrap">
    <div class="split">
      <div class="split-media reveal">
        {picture('thorn-fitout', 'Full-height glass partitions in a Melbourne office fitout', sizes='(max-width:860px) 100vw, 50vw')}
      </div>
      <div class="split-body reveal" data-delay="1">
        <span class="kicker">Why it matters</span>
        <h2>Measured once.<br>Cut <span class="serif">once.</span></h2>
        <p class="lead">Glass cannot be adjusted on site. That single fact decides how a glazing job goes — so the person who quotes also measures, and the measurements are the ones the glass is cut to.</p>
        <ul>
          <li>Site measure after finishes, not from drawings</li>
          <li>Glass make-up and thickness named in writing</li>
          <li>Compliance checked against AS 1288 for the actual location</li>
          <li>One glazier accountable from quote to final silicone</li>
        </ul>
        <a class="btn btn--ghost" href="/standards/" style="justify-self:start">How we select glass {ARROW}</a>
      </div>
    </div>
  </section>

  <section class="section section--line wrap" id="work">
    <div class="head head--split reveal">
      <div>
        <span class="kicker">Selected work</span>
        <h2 style="margin-top:16px">Real jobs,<br>on <span class="serif">real sites.</span></h2>
      </div>
      <div>
        <p class="lead">Offices, fitouts, bathrooms. Photographed on completion — no stock imagery dressed up as our work.</p>
        <div class="filters" style="margin-top:22px">
          <button class="chip is-active" data-filter="all">All</button>
          <button class="chip" data-filter="commercial">Commercial</button>
          <button class="chip" data-filter="residential">Residential</button>
        </div>
      </div>
    </div>
    <div class="gallery">
{tiles}    </div>
    <div style="margin-top:34px">
      <a class="btn btn--ghost" href="/projects/">Project stories {ARROW}</a>
    </div>
  </section>

  <section class="section section--line wrap">
    <div class="panel reveal">
      <div class="head" style="margin-bottom:0">
        <span class="kicker">Standards</span>
        <h2>Glass is selected,<br>not <span class="serif">guessed.</span></h2>
        <p class="lead" style="margin-top:6px">The same window can need different glass depending on how low it sits, whether it is a door, what is above it and how big the panel is. That is what AS 1288 exists for — and it is why a quote names a make-up rather than a "type of glass".</p>
      </div>
      <div class="table-scroll">
        <table class="spec">
          <thead><tr><th>Application</th><th>Typical make-up</th><th>Thickness</th><th>Selected under</th></tr></thead>
          <tbody>
            <tr><td>Shopfront, framed</td><td>Toughened monolithic</td><td>6–10mm</td><td>AS 1288 / AS 2208</td></tr>
            <tr><td>Glass entry door</td><td>Toughened or laminated</td><td>10–12mm</td><td>AS 1288 / AS 2208</td></tr>
            <tr><td>Frameless shower screen</td><td>Toughened monolithic</td><td>10mm</td><td>AS 1288 / AS 2208</td></tr>
            <tr><td>Acoustic partition</td><td>Double glazed unit</td><td>6-12-6</td><td>AS 1288 / AS 4666</td></tr>
            <tr><td>Balustrade infill</td><td>Toughened laminated</td><td>10+10mm</td><td>AS 1288 / AS 1178</td></tr>
          </tbody>
        </table>
      </div>
      <p class="muted" style="font-size:.8rem;margin-top:20px">Indicative only — every job is selected on its own measurements and location. <a href="/standards/" style="color:var(--gold)">Read how AS 1288 is applied</a>.</p>
    </div>
  </section>

  <section class="section section--line wrap">
    <div class="head reveal">
      <span class="kicker">How a job runs</span>
      <h2>Four steps,<br>no <span class="serif">surprises.</span></h2>
    </div>
    <div class="steps">
      <div class="step reveal"><h3>Enquire</h3><p>Send a photo, the suburb and rough dimensions. We tell you what is possible before anyone drives out.</p></div>
      <div class="step reveal" data-delay="1"><h3>Measure</h3><p>The glazier who will install attends, measures the finished opening and checks what the location requires.</p></div>
      <div class="step reveal" data-delay="2"><h3>Quote</h3><p>Glass make-up, thickness, hardware and inclusions in writing. No allowances, no "plus extras".</p></div>
      <div class="step reveal" data-delay="3"><h3>Install</h3><p>Fabricated to those measurements, fitted, cleaned down — and certified where a certificate applies.</p></div>
    </div>
  </section>

  <section class="section section--line wrap">
    <div class="head reveal">
      <span class="kicker">Where we work</span>
      <h2>Melbourne metro,<br>and <span class="serif">beyond.</span></h2>
    </div>
    <div class="areas reveal">
      {''.join(f'<a class="area" href="/service-areas/{a["slug"]}/"><h3>{a["name"]}</h3><p>{a["blurb"]}</p><span class="area-link">View area {ARROW}</span></a>' for a in AREAS)}
      <a class="area area--ask" href="/quote/"><h3>Somewhere else?</h3><p>Give us the suburb and the scope. We will tell you honestly whether the drive makes sense.</p><span class="area-link">Ask us {ARROW}</span></a>
    </div>
  </section>

  <section class="section section--line wrap">
    <div class="head reveal"><span class="kicker">Questions</span><h2>Asked <span class="serif">often.</span></h2></div>
    <div class="faq reveal">
{faq_html}    </div>
  </section>

  <section class="section cta" id="quote">
    <div class="wrap cta-grid">
      <div class="reveal">
        <span class="kicker">Start here</span>
        <h2 style="margin-top:16px">Tell us about<br>the <span class="serif">opening.</span></h2>
        <p class="lead" style="margin-top:18px">A photo and a rough size is enough to start. If it is easier, call — you will speak to the glazier, not a call centre.</p>
        <div class="contact-list">
          <a href="tel:{ORG['tel']}"><svg viewBox="0 0 24 24" fill="none"><path d="M4 5c0-.6.4-1 1-1h3l2 5-2 1a12 12 0 006 6l1-2 5 2v3c0 .6-.4 1-1 1A16 16 0 014 5z" stroke="currentColor" stroke-width="1.4"/></svg><span><strong>Phone</strong>{ORG['phone']}</span></a>
          <a href="mailto:{ORG['email']}"><svg viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="14" rx="1.5" stroke="currentColor" stroke-width="1.4"/><path d="M3 7l9 6 9-6" stroke="currentColor" stroke-width="1.4"/></svg><span><strong>Email</strong>{ORG['email']}</span></a>
          <div><svg viewBox="0 0 24 24" fill="none"><path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z" stroke="currentColor" stroke-width="1.4"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="1.4"/></svg><span><strong>Based in</strong>{ORG['location']}</span></div>
        </div>
      </div>
      <form class="form reveal" data-enquiry data-delay="1" novalidate>
        <div class="form-row">
          <div class="field"><label for="n">Name</label><input id="n" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="p">Phone</label><input id="p" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="e">Email</label><input id="e" name="email" type="email" autocomplete="email"></div>
          <div class="field"><label for="s">Suburb</label><input id="s" name="suburb" type="text" autocomplete="address-level2"></div>
        </div>
        <div class="field"><label for="sv">What is it for?</label>
          <select id="sv" name="service">
            {''.join(f'<option>{s["title"]}</option>' for s in SERVICES)}
            <option>Mirrors / splashback</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="field"><label for="m">Details</label><textarea id="m" name="message" placeholder="Rough width and height, new build or replacement, and anything the photos do not show."></textarea></div>
        <button class="btn btn--lg" type="submit">Send enquiry {ARROW}</button>
        <p class="form-note">Opening your email app, pre-filled — no form service, no tracking. Photos can be attached there directly.</p>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>
</main>"""

    shell(
        "Anderson Glass & Glazing — Commercial Glazing & Shower Screens, Melbourne",
        "Melbourne commercial glazing, office partitions, frameless shower screens, glass replacement and mirrors. Measured, made and installed by the same glazier — Anderson Glass & Glazing, Narre Warren East.",
        "/", body, active="", extra_json=[faq_ld, services_ld],
    )


def build_service(s):
    others = [x for x in SERVICES if x["slug"] != s["slug"]]
    opt_rows = "".join(
        f'<tr><td>{n}</td><td>{d}</td></tr>' for n, d in s["options"]
    )
    spec_rows = "".join(
        f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in s["specs"]
    )
    faq_html = "".join(
        f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="answer">{a}</div></details>'
        for q, a in s["faqs"]
    )
    faq_ld = {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in s["faqs"]
        ],
    }
    service_ld = {
        "@type": "Service",
        "name": s["title"].replace("&amp;", "&"),
        "serviceType": s["title"].replace("&amp;", "&"),
        "provider": {"@id": SITE + "/#org"},
        "areaServed": {"@type": "City", "name": "Melbourne"},
        "url": url(f"/services/{s['slug']}/"),
        "description": html.unescape(s["answer"]),
    }
    crumb_ld = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": url("/services/")},
            {"@type": "ListItem", "position": 3, "name": html.unescape(s["title"]), "item": url(f"/services/{s['slug']}/")},
        ],
    }
    rel = "".join(
        f'<a class="svc reveal" href="/services/{o["slug"]}/">{picture(o["img"], "", sizes="(max-width:620px) 100vw, 33vw")}<h3>{o["title"]}</h3><p>{o["short"]}</p><span class="svc-go">Explore {ARROW}</span></a>'
        for o in others[:3]
    )

    body = f"""
<main id="main">
  {page_hero("Service", s['title'], s['short'], [("/", "Home"), ("/services/", "Services")], img=s['img'])}
  <section class="section--tight wrap" style="padding-top:clamp(20px,3vw,40px)">
    <p class="answer-box reveal">{s['answer']}</p>
  </section>

  <section class="section wrap">
    <div class="split">
      <div class="prose reveal">
        <h2>What it <span class="serif">involves</span></h2>
        <p>{s['intro']}</p>
        <h3 style="margin-top:10px">Typical scope</h3>
        <ul>{''.join(f'<li>{i}</li>' for i in s['includes'])}</ul>
      </div>
      <div class="split-media reveal" data-delay="1">{picture(s['img'], s['title'], sizes="(max-width:860px) 100vw, 50vw")}</div>
    </div>
  </section>

  <section class="section section--line wrap">
    <div class="panel reveal">
      <span class="kicker">Options</span>
      <h2 style="margin-top:16px;font-size:clamp(1.8rem,3.4vw,2.8rem)">What the glass <span class="serif">can be.</span></h2>
      <div class="table-scroll">
        <table class="spec">
          <thead><tr><th>Option</th><th>When it is used</th></tr></thead>
          <tbody>{opt_rows}</tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="section section--line wrap">
    <div class="head reveal"><span class="kicker">Selection</span><h2>Typical make-ups<br>for <span class="serif">this work.</span></h2></div>
    <div class="table-scroll reveal">
      <table class="spec">
        <thead><tr><th>Application</th><th>Make-up</th><th>Thickness</th><th>Selected under</th></tr></thead>
        <tbody>{spec_rows}</tbody>
      </table>
    </div>
    <p class="muted reveal" style="font-size:.82rem;margin-top:18px;max-width:70ch">Indicative only. Each job is selected on the measured panel size, the height above floor, what is above and below, and the wind or impact loads that apply. <a href="/standards/" style="color:var(--gold)">How AS 1288 is applied →</a></p>
  </section>

  <section class="section section--line wrap">
    <div class="head reveal"><span class="kicker">Questions</span><h2>Asked about<br><span class="serif">{s['title'].lower()}.</span></h2></div>
    <div class="faq reveal">{faq_html}</div>
  </section>

  <section class="section section--line wrap">
    <div class="head reveal"><span class="kicker">Also</span><h2>Other <span class="serif">services.</span></h2></div>
    <div class="services">{rel}</div>
  </section>

  <section class="section cta">
    <div class="wrap" style="display:grid;gap:26px;justify-items:start">
      <span class="kicker">Next step</span>
      <h2>Send a photo.<br>Get a <span class="serif">real answer.</span></h2>
      <p class="lead">A photo of the opening, the suburb and a rough size is enough for us to tell you what is possible.</p>
      <div class="hero-actions">
        <a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a>
        <a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a>
      </div>
    </div>
  </section>
</main>"""
    shell(
        f"{html.unescape(s['title'])} Melbourne — Anderson Glass & Glazing",
        html.unescape(s["answer"])[:150],
        f"/services/{s['slug']}/", body, active="/services/",
        extra_json=[service_ld, faq_ld, crumb_ld], og_img=s["img"],
    )


def build_services_index():
    cards = "".join(
        f'<a class="svc reveal" href="/services/{s["slug"]}/" data-delay="{i%3}">{picture(s["img"], "", sizes="(max-width:620px) 100vw, 33vw")}<h3>{s["title"]}</h3><p>{s["short"]}</p><span class="svc-go">Explore {ARROW}</span></a>'
        for i, s in enumerate(SERVICES)
    )
    body = f"""
<main id="main">
  {page_hero("Services", "Five lines of <span class='serif'>glass work.</span>", "Commercial glazing, office partitions, shower screens, replacement glass and mirrors — supplied and installed across Melbourne by the same glazier.", [("/", "Home")])}
  <section class="section--tight wrap"><div class="services">{cards}</div></section>
  <section class="section wrap">
    <div class="prose reveal">
      <h2>How we work</h2>
      <p>Every line above runs on the same three rules. Measure the opening as it is now, not as the drawing says it will be. Name the glass make-up and the standard it is selected under, in writing. Install it with the person who measured it on site.</p>
      <p>It sounds obvious. It is also the difference between a screen that closes cleanly in five years and one that does not close cleanly in five weeks.</p>
    </div>
  </section>
  <section class="section cta"><div class="wrap" style="display:grid;gap:26px;justify-items:start">
    <span class="kicker">Start here</span>
    <h2>Not sure which<br>one you <span class="serif">need?</span></h2>
    <p class="lead">Send a photo and describe what you are trying to achieve. We will tell you which trade the job actually is.</p>
    <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a><a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
  </div></section>
</main>"""
    shell("Glazing services Melbourne — Anderson Glass & Glazing",
          "Commercial glazing, office partitions, shower screens, glass replacement and mirrors across Melbourne. Measured, made and installed.",
          "/services/", body, active="/services/")


def build_projects():
    all_items = GALLERY
    tiles = ""
    for i, (img, cap, tags, cls) in enumerate(all_items):
        tiles += f"""      <figure class="{cls if cls != 'tile--wide' else 'tile'} tile reveal" data-tags="{tags}" data-lightbox data-full="/images/{img}-1920.webp" data-delay="{i%3}">
        {picture(img, cap, sizes='(max-width:620px) 100vw, (max-width:900px) 50vw, 33vw')}
        <figcaption>{cap}</figcaption>
      </figure>
"""
    stories = "".join(
        f"""<a class="svc reveal" href="/projects/{p['slug']}/" data-delay="{i%3}">
  {picture(p['img'], '', sizes='(max-width:620px) 100vw, 33vw')}
  <h3>{p['name']}</h3><p>{p['lede'][:110]}…</p><span class="svc-go">Read the job {ARROW}</span></a>"""
        for i, p in enumerate(PROJECTS)
    )
    body = f"""
<main id="main">
  {page_hero("Work", "Considered glazing.<br>Real <span class='serif'>sites.</span>", "Offices, fitouts and bathrooms across Melbourne — photographed on completion. No stock imagery passed off as our work.", [("/", "Home")], img="office-floor")}
  <section class="section--tight wrap">
    <div class="head reveal"><span class="kicker">Project stories</span><h2 style="font-size:clamp(1.7rem,3vw,2.4rem)">Three jobs, <span class="serif">in detail.</span></h2></div>
    <div class="services">{stories}</div>
  </section>
  <section class="section section--line wrap">
    <div class="head head--split reveal">
      <div><span class="kicker">Gallery</span><h2 style="margin-top:16px">From the <span class="serif">floor.</span></h2></div>
      <p class="lead">Every image below is a completed Anderson Glass job. Tap any to enlarge.</p>
    </div>
    <div class="gallery">{tiles}</div>
  </section>
  <section class="section cta"><div class="wrap" style="display:grid;gap:26px;justify-items:start">
    <span class="kicker">Your job next</span>
    <h2>Send us the<br><span class="serif">opening.</span></h2>
    <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a><a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
  </div></section>
</main>"""
    shell("Projects — Anderson Glass & Glazing, Melbourne",
          "Completed glazing projects across Melbourne: office fitouts, glass partitions, mirrors and frameless shower screens.",
          "/projects/", body, active="/projects/", og_img="office-floor")


def build_case(p):
    facts = "".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in p["facts"])
    paras = "".join(f"<p>{t}</p>" for t in p["body"])
    body = f"""
<main id="main">
  {page_hero("Project", p['name'], p['lede'], [("/", "Home"), ("/projects/", "Work")], img=p['img'])}
  <section class="section wrap">
    <div class="split">
      <div class="prose reveal">{paras}
        <h3 style="margin-top:14px">At a glance</h3>
        <div class="table-scroll"><table class="spec"><tbody>{facts}</tbody></table></div>
      </div>
      <div class="split-media reveal" data-delay="1">{picture(p['img'], p['name'], sizes="(max-width:860px) 100vw, 50vw")}</div>
    </div>
  </section>
  <section class="section section--line wrap">
    <div class="gallery">{''.join(f'<figure class="tile reveal" data-lightbox data-full="/images/{img}-1920.webp">{picture(img, cap, sizes="(max-width:900px) 50vw, 33vw")}<figcaption>{cap}</figcaption></figure>' for img, cap, tags, cls in GALLERY[:3])}</div>
  </section>
  <section class="section cta"><div class="wrap" style="display:grid;gap:26px;justify-items:start">
    <span class="kicker">Similar job?</span><h2>Let's look at<br>your <span class="serif">space.</span></h2>
    <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a><a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
  </div></section>
</main>"""
    shell(f"{p['name']} — Anderson Glass & Glazing",
          html.unescape(p["lede"]), f"/projects/{p['slug']}/", body, active="/projects/", og_img=p["img"])


def build_area(a):
    subs = "".join(f"<li>{s}</li>" for s in a["suburbs"])
    body = f"""
<main id="main">
  {page_hero("Service area", f"{a['name']}<br><span class='serif'>glazing.</span>", a['blurb'], [("/", "Home"), ("/service-areas/", "Areas")])}
  <section class="section wrap">
    <div class="split">
      <div class="prose reveal">
        <h2>What we do in <span class="serif">{a['name'].split()[0]}</span></h2>
        <p>Commercial glazing, office partitions, shower screens, glass replacement and mirrors — supplied and installed. Site visits are scheduled by corridor, so the drive is part of the plan rather than an extra.</p>
        <h3 style="margin-top:10px">Suburbs we work in</h3>
        <ul style="columns:2;column-gap:24px">{subs}</ul>
        <p class="muted" style="font-size:.86rem">Outside this list? Ask — larger jobs travel further.</p>
      </div>
      <div class="split-media reveal" data-delay="1">{picture('office-floor', f'Glazing work in {a["name"]}', sizes="(max-width:860px) 100vw, 50vw")}</div>
    </div>
  </section>
  <section class="section section--line wrap">
    <div class="head reveal"><span class="kicker">Services</span><h2>Available in <span class="serif">{a['name'].split()[0]}.</span></h2></div>
    <div class="services">{''.join(f'<a class="svc reveal" href="/services/{s["slug"]}/">{picture(s["img"], "", sizes="(max-width:620px) 100vw, 33vw")}<h3>{s["title"]}</h3><p>{s["short"]}</p><span class="svc-go">Explore {ARROW}</span></a>' for s in SERVICES[:3])}</div>
  </section>
  <section class="section cta"><div class="wrap" style="display:grid;gap:26px;justify-items:start">
    <span class="kicker">{a['name']}</span><h2>Send a photo.<br>We'll <span class="serif">reply.</span></h2>
    <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a><a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
  </div></section>
</main>"""
    shell(f"Glazing {a['name']} — Anderson Glass & Glazing",
          html.unescape(a["blurb"]), f"/service-areas/{a['slug']}/", body, active="/service-areas/")


def build_areas_index():
    body = f"""
<main id="main">
  {page_hero("Coverage", "Melbourne metro,<br>and <span class='serif'>beyond.</span>", "Site visits are scheduled by corridor. These are the areas we work in most weeks.", [("/", "Home")])}
  <section class="section wrap">
    <div class="areas reveal">{''.join(f'<a class="area" href="/service-areas/{a["slug"]}/"><h3>{a["name"]}</h3><p>{a["blurb"]}</p><span class="area-link">View area {ARROW}</span></a>' for a in AREAS)}</div>
  </section>
  <section class="section cta"><div class="wrap" style="display:grid;gap:26px;justify-items:start">
    <span class="kicker">Not listed?</span><h2>Ask <span class="serif">anyway.</span></h2>
    <p class="lead">Give us the suburb and the scope. If it is outside a regular corridor we will tell you honestly whether the job makes sense to travel for.</p>
    <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a><a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
  </div></section>
</main>"""
    shell("Service areas — Anderson Glass & Glazing, Melbourne",
          "Glazing service areas across Melbourne: south east, inner east, north, bayside and Gippsland.",
          "/service-areas/", body, active="/service-areas/")


def build_standards():
    faqs = [
        ("What is AS 1288?", "AS 1288 is the Australian Standard for glass in buildings — selection and installation. It sets out how thick glass must be, and whether it must be safety glass, based on the panel size, the height above the floor, the location in the building and the loads it has to resist."),
        ("What is Grade A safety glass?", "Grade A safety glass is toughened or laminated glass that meets AS 2208. If it breaks, toughened glass breaks into small blunt fragments and laminated glass stays in its frame rather than falling as large shards."),
        ("Why can't one thickness suit every job?", "Because the requirement scales with area and height. A 600mm panel low in a wall and a 2.4m panel in the same wall can need different make-ups, and both are legal. The standard is applied to the actual opening, not to the product name."),
        ("What does a glazing certificate certify?", "It identifies the job, the glass supplied, its make-up and thickness, the standard it was selected under, and who installed it. It is a record of what was installed — not a warranty of the building."),
        ("Does this page specify the glass for my project?", "No. This is an explanation of how selection works. The specification for your job comes from the measured panel, its location and the applicable loads — which is what the quote and certificate record."),
    ]
    faq_html = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="answer">{a}</div></details>' for q, a in faqs)
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    body = f"""
<main id="main">
  {page_hero("Standards", "What AS 1288 means<br>for your <span class='serif'>glazing.</span>", "The short version: glass is selected against the opening it goes into — its size, its height above the floor, what is above it and what it has to resist. Not against a product brochure.", [("/", "Home")])}
  <section class="section wrap">
    <div class="split">
      <div class="prose reveal">
        <h2>Selection, not <span class="serif">preference.</span></h2>
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
      <div class="split-media reveal" data-delay="1">{picture('bathroom-mirrors', 'Frameless glazing and mirrors', sizes="(max-width:860px) 100vw, 50vw")}</div>
    </div>
  </section>
  <section class="section section--line wrap">
    <div class="panel reveal">
      <span class="kicker">Reference</span>
      <h2 style="margin-top:16px;font-size:clamp(1.7rem,3vw,2.4rem)">Standards we <span class="serif">work to.</span></h2>
      <div class="table-scroll"><table class="spec">
        <thead><tr><th>Standard</th><th>What it covers</th></tr></thead>
        <tbody>
          <tr><td>AS 1288</td><td>Glass in buildings — selection and installation</td></tr>
          <tr><td>AS 2208</td><td>Safety glazing materials in buildings (Grade A / Grade B)</td></tr>
          <tr><td>AS 4666</td><td>Insulating glass units (double glazing)</td></tr>
          <tr><td>AS 1178</td><td>Glass in balustrades and barriers (as referenced)</td></tr>
          <tr><td>AS 1428.1</td><td>Access — including visibility of glazed doors and walls</td></tr>
        </tbody>
      </table></div>
      <p class="muted" style="font-size:.8rem;margin-top:20px;max-width:70ch">Where a project has a specification, a builder's detail or a certifier's requirement, that governs. This page explains the default position, not a substitute for project documentation.</p>
    </div>
  </section>
  <section class="section section--line wrap">
    <div class="head reveal"><span class="kicker">Questions</span><h2>Standards, <span class="serif">explained.</span></h2></div>
    <div class="faq reveal">{faq_html}</div>
  </section>
  <section class="section cta"><div class="wrap" style="display:grid;gap:26px;justify-items:start">
    <span class="kicker">Your job</span><h2>Ask about<br>your <span class="serif">opening.</span></h2>
    <div class="hero-actions"><a class="btn btn--lg" href="/quote/">Request a quote {ARROW}</a><a class="btn btn--lg btn--ghost" href="tel:{ORG['tel']}">{ORG['phone']}</a></div>
  </div></section>
</main>"""
    shell("AS 1288 glass selection explained — Anderson Glass & Glazing",
          "How AS 1288 and AS 2208 decide glass thickness and safety glass for windows, doors, partitions and shower screens in Melbourne.",
          "/standards/", body, active="/standards/", extra_json=[faq_ld])


def build_facts():
    rows = [
        ("Registered name", ORG["legal"]),
        ("ABN", ORG["abn"]),
        ("ACN", ORG["acn"]),
        ("Phone", ORG["phone"]),
        ("Email", ORG["email"]),
        ("Based in", f"{ORG['location']}"),
        ("Service area", "Melbourne metro; Gippsland by schedule"),
        ("Trades", "Commercial glazing · office partitions · shower screens · glass replacement · mirrors"),
        ("Supply model", "Supply and install; measure and quote by appointment"),
        ("Pricing", "Quoted per job after measure — no published rates"),
    ]
    table = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    body = f"""
<main id="main">
  {page_hero("Facts", "Business facts,<br>in <span class='serif'>plain text.</span>", "Written for people and for machines: what the business is, who runs it, where it works and what it actually does. No claims that cannot be checked.", [("/", "Home")])}
  <section class="section wrap">
    <div class="table-scroll reveal"><table class="spec"><tbody>{table}</tbody></table></div>
    <div class="prose reveal" style="margin-top:44px">
      <h2>What we do not do</h2>
      <p>We do not publish price lists, because a compliant glass make-up depends on the measured opening. We do not sell ready-made screens or flat-pack. We do not run a call centre — the number goes to the person who will measure and install the job.</p>
      <h2>Quoting</h2>
      <p>Measure and quote is free across Melbourne metro. The quote names the application, the make-up, the thickness, the hardware and the inclusions, and states the lead time at the time of quoting rather than as a website promise.</p>
      <h2>Records</h2>
      <p>Glazing certificates are issued where the job requires one: construction work, builder-specified work, and safety glass installations. The certificate records the glass supplied and the standard it was selected under.</p>
    </div>
  </section>
  <section class="section cta"><div class="wrap" style="display:grid;gap:26px;justify-items:start">
    <span class="kicker">Contact</span><h2>Talk to the<br><span class="serif">glazier.</span></h2>
    <div class="contact-list">
      <a href="tel:{ORG['tel']}"><strong>Phone</strong>{ORG['phone']}</a>
      <a href="mailto:{ORG['email']}"><strong>Email</strong>{ORG['email']}</a>
    </div>
  </div></section>
</main>"""
    shell("Business facts — Anderson Glass & Glazing",
          "Anderson Glass & Glazing Pty Ltd — ABN, ACN, contact, service area, trades and quoting policy in plain text.",
          "/facts/", body, active="/facts/")


def build_quote():
    body = f"""
<main id="main">
  {page_hero("Quote", "Tell us about<br>the <span class='serif'>opening.</span>", "A photo, the suburb and a rough size is enough to start. You will get a real answer — which glass, what thickness, why.", [("/", "Home")])}
  <section class="section--tight wrap" style="padding-top:clamp(24px,4vw,56px)">
    <div class="cta-grid">
      <div class="reveal">
        <div class="contact-list">
          <a href="tel:{ORG['tel']}"><svg viewBox="0 0 24 24" fill="none"><path d="M4 5c0-.6.4-1 1-1h3l2 5-2 1a12 12 0 006 6l1-2 5 2v3c0 .6-.4 1-1 1A16 16 0 014 5z" stroke="currentColor" stroke-width="1.4"/></svg><span><strong>Phone — fastest for anything broken</strong>{ORG['phone']}</span></a>
          <a href="mailto:{ORG['email']}"><svg viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="14" rx="1.5" stroke="currentColor" stroke-width="1.4"/><path d="M3 7l9 6 9-6" stroke="currentColor" stroke-width="1.4"/></svg><span><strong>Email</strong>{ORG['email']}</span></a>
          <div><svg viewBox="0 0 24 24" fill="none"><path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z" stroke="currentColor" stroke-width="1.4"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="1.4"/></svg><span><strong>Based in</strong>{ORG['location']}</span></div>
        </div>
        <h2 style="margin-top:44px;font-size:clamp(1.5rem,2.4vw,2rem)">What helps most</h2>
        <ul style="display:grid;gap:12px;margin-top:18px">
          <li style="display:flex;gap:12px"><span style="color:var(--gold)">01</span><span>A photo of the opening, with something for scale</span></li>
          <li style="display:flex;gap:12px"><span style="color:var(--gold)">02</span><span>Rough width and height — a tape measure is fine</span></li>
          <li style="display:flex;gap:12px"><span style="color:var(--gold)">03</span><span>New build or replacement, and the suburb</span></li>
          <li style="display:flex;gap:12px"><span style="color:var(--gold)">04</span><span>Anything the photos do not show — access, stairs, who else is on site</span></li>
        </ul>
      </div>
      <form class="form reveal" data-enquiry data-delay="1" novalidate>
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
        <div class="field"><label for="m2">Details</label><textarea id="m2" name="message" placeholder="Rough width and height, new build or replacement, and anything the photos do not show."></textarea></div>
        <button class="btn btn--lg" type="submit">Send enquiry {ARROW}</button>
        <p class="form-note">This opens your email app pre-filled — no third-party form service, nothing stored on this site. Attach photos there.</p>
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
  <section class="section wrap" style="padding-top:clamp(140px,20vw,240px)">
    <span class="kicker">404</span>
    <h1 style="margin-top:18px">That page<br>isn't <span class="serif">here.</span></h1>
    <p class="lead" style="margin-top:20px">The link is old, or the glass slipped. Either way — try one of these.</p>
    <div class="hero-actions" style="margin-top:30px">
      <a class="btn btn--lg" href="/">Home</a>
      <a class="btn btn--lg btn--ghost" href="/services/">Services</a>
      <a class="btn btn--lg btn--ghost" href="/quote/">Request a quote</a>
    </div>
  </section>
</main>"""
    shell("Page not found — Anderson Glass & Glazing", "That page could not be found.", "/404.html", body)


def build_assets():
    # copy assets, images, fonts
    for sub in ("assets", "images"):
        src = BASE / sub
        dst = OUT / sub
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    (OUT / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" fill="#0a0a0b"/><g stroke="#d8b46a" stroke-width="1.6" fill="none"><rect x="6" y="6" width="28" height="28"/><path d="M6 16h28M16 6v28"/></g></svg>',
        encoding="utf-8")


def build_meta():
    pages = ["/", "/services/", "/projects/", "/service-areas/", "/standards/", "/facts/", "/quote/"]
    pages += [f"/services/{s['slug']}/" for s in SERVICES]
    pages += [f"/service-areas/{a['slug']}/" for a in AREAS]
    pages += [f"/projects/{p['slug']}/" for p in PROJECTS]
    today = "2026-11-07"
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        pri = "1.0" if p == "/" else ("0.9" if p.startswith("/services/") or p == "/quote/" else "0.7")
        sitemap += f"  <url><loc>{url(p)}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority></url>\n"
    sitemap += "</urlset>\n"
    (OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    robots = f"""User-agent: *
Allow: /

# AI / answer engines — explicitly welcome
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Bingbot
Allow: /

Sitemap: {SITE}/sitemap.xml
"""
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")

    llms = f"""# Anderson Glass & Glazing

> Commercial glazing, office partitions, shower screens, glass replacement and mirrors across Melbourne, Victoria. Supplied and installed by the same glazier who measures and quotes. Enquiry-only — pricing is quoted per job after a site measure.

## Business
- Legal name: {ORG['legal']}
- ABN {ORG['abn']} · ACN {ORG['acn']}
- Workshop: {ORG['location']}
- Phone: {ORG['phone']}
- Email: {ORG['email']}
- Service area: Melbourne metro (south east, inner east, north, bayside); Gippsland by schedule

## Services
{chr(10).join(f"- {html.unescape(s['title'])}: {html.unescape(s['short'])} ({SITE}/services/{s['slug']}/)" for s in SERVICES)}

## How quoting works
- Measure and quote free across Melbourne metro; attendee is the installing glazier.
- No published prices: glass make-up and thickness depend on the measured panel, its height above the floor and the applicable loads (AS 1288).
- Lead times confirmed at quote, not published.
- Glazing certificates issued where the job requires one (glass supplied, make-up, standard, installer).

## Standards
- AS 1288 (glass in buildings — selection and installation)
- AS 2208 (safety glazing materials)
- AS 4666 (insulating glass units)
- AS 1428.1 (visibility of glazed doors/walls)

## Pages
{chr(10).join(f"- {SITE}{p}" for p in pages)}
- {SITE}/standards/ — how glass is selected under AS 1288
- {SITE}/facts/ — business facts in plain text
"""
    (OUT / "llms.txt").write_text(llms, encoding="utf-8")
    (OUT / "llms-full.txt").write_text(llms + "\n\n" + "\n\n".join(
        f"## {html.unescape(s['title'])}\n{html.unescape(s['answer'])}\n" + "\n".join(f"- {i}" for i in s["includes"])
        for s in SERVICES
    ), encoding="utf-8")

    headers = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Strict-Transport-Security: max-age=31536000
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; form-action 'self' mailto:; base-uri 'self'; frame-ancestors 'none'
  Cross-Origin-Opener-Policy: same-origin

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/images/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
"""
    (OUT / "_headers").write_text(headers, encoding="utf-8")


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
