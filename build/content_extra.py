"""Extra editorial content for the Anderson Glass site.

Kept separate from build.py so the content model stays readable: guides, expanded
area detail, deeper project stories and the answers hub all live here.

House rules for everything in this file:
  * no prices, no lead times quoted as promises (they are "confirmed at quote")
  * no invented reviews, ratings, certifications or job claims
  * standards referenced only in general terms (AS 1288, AS 2208) — never a
    specific clause or a legal conclusion for someone else's building
"""

# --------------------------------------------------------------------- guides
# Each guide: slug, title, dek, service (related service slug), sections
# (heading, [paragraphs]), points (short takeaway list), faqs [(q, a)]

GUIDES = [
    {
        "slug": "how-glass-thickness-is-chosen",
        "title": "How glass thickness is chosen",
        "dek": "Why the same size opening can need different glass in two different places — and what actually decides it.",
        "service": "commercial-glazing",
        "sections": [
            ("The short answer",
             ["Glass thickness is not chosen by size alone. It is chosen by what the glass has to do: how far it "
              "spans, how high it sits above the floor, whether people walk into it, what is above and below it, "
              "and what it has to keep out. Two openings with identical measurements can legitimately need "
              "different glass because one is a bedroom window and the other is a shopfront people lean on.",
              "That is why a price given over the phone is not a price. The number depends on a decision that "
              "cannot be made until the opening is seen."]),
            ("Span and support decide more than area",
             ["A pane fails where it is unsupported, not where it is biggest. A tall narrow panel carrying "
              "wind load behaves differently from a wide low one, and a panel fixed on four sides behaves "
              "differently again from one held only at the top and bottom.",
              "This is also why the frame, the head channel and the fixings are part of the glass decision "
              "rather than a separate trade. Glass held in a weak frame moves, and moving glass cracks at the "
              "fixings."]),
            ("Human impact drives the safety requirement",
             ["The safety glazing rules exist because ordinary glass in the wrong place behaves like a blade. "
              "Glass in a door, alongside a door, or low enough that a person could fall into it is treated "
              "differently from glass above head height in a fixed panel.",
              "In practice this is where most surprise comes from: a customer replaces a broken low window "
              "with the same glass as before, and the same glass is no longer what the location calls for. "
              "Replacing like-for-like in a location that was already wrong simply resets the clock on the "
              "same problem."]),
            ("Make-up, not just millimetres",
             ["Toughened glass is heat treated so that it fails into small blunt pieces rather than shards. "
              "Laminated glass holds together because a plastic interlayer keeps the fragments attached to a "
              "sheet. Float or annealed glass is the ordinary form and is not suitable where the safety rules "
              "apply.",
              "Adding thickness is one way to satisfy a span; changing the make-up is how you satisfy the "
              "safety requirement. They are different questions and both get answered before the glass is "
              "ordered — once toughened glass is cut, it cannot be cut again."]),
            ("What we look at on site",
             ["The opening as built, not as drawn — frames are rarely square and floors are rarely level. "
              "How the glass is supported and what it is fixed into. The path people take past it: door swing, "
              "stairs, anywhere someone could stumble. And whether the glass is doing a job beyond looking "
              "right: thermal, acoustic, privacy, security.",
              "The answer is written down in the quote — the glass, the make-up and the standard it is selected "
              "under — because a verbal agreement about \"10 mil\" does not survive a change of installer."]),
        ],
        "points": [
            "Two identical openings can need different glass — location decides as much as size",
            "Toughened or laminated is a safety decision, not a thickness upgrade",
            "The frame and fixings are part of the answer, not a separate trade",
            "Once glass is toughened it cannot be cut, so the decision is made once, in writing",
        ],
        "faqs": [
            ("Can you tell me the thickness over the phone?",
             "We can tell you what is typical for that kind of opening, and we will not pretend that is a "
             "specification. The make-up depends on the actual span, support and location, which is why the "
             "measure visit exists and why it is free."),
            ("Is thicker glass always safer?",
             "Not in the way people mean. Thickness helps with span and load; the safety behaviour comes from "
             "the make-up. A thick piece of ordinary glass in a door is still the wrong glass."),
            ("Why does my replacement need different glass to what was there?",
             "Because what was there may have been installed before the current safety requirements applied, or "
             "may never have suited the location. We measure the opening as it is and name the make-up that "
             "suits it now."),
        ],
    },
    {
        "slug": "why-we-measure-after-tiling",
        "title": "Why we measure your shower after tiling",
        "dek": "The single biggest cause of leaking shower screens is a screen made from the drawing.",
        "service": "shower-screens",
        "sections": [
            ("The room is not the drawing",
             ["A frameless shower screen is a set of flat, rigid panels fitted into a space that is almost "
              "never flat. Walls are out of square, tiles sit proud of the wall in one corner and flush in "
              "another, and the floor has a fall so water runs to the waste. Every one of those differences is "
              "a few millimetres, and a few millimetres is the difference between a door that swings clean and "
              "a door that binds on the tile.",
              "Measuring after tiling is not caution, it is the only measurement that means anything. Before "
              "tiling you are measuring a guess about where the finished face will end up."]),
            ("What gets measured, and why",
             ["The opening across the top, the middle and the bottom — three measurements, because a wall that "
              "is out of square is a different width at each height. The height to the finished floor at both "
              "ends. The position of the waste and the fall of the floor, because the bottom edge of the screen "
              "has to clear both. And the hinge side: which wall the door swings from, and what it will hit "
              "when it opens.",
              "Door swing is where cheap screens fail visibly. A door centred for appearance will hit the "
              "vanity, or the towel rail, or the person standing at the basin."]),
            ("Why 10 mm and why hinges rather than a frame",
             ["A frameless screen carries its stiffness in the glass rather than in an aluminium frame, which "
              "is why the panels are heavier and the fixings do more work. Hinges and brackets have to be "
              "rated for the panel weight and fixed into something solid — a stud, not plasterboard.",
              "The glass is toughened, which means it cannot be drilled or cut after tempering. Every hole for "
              "every hinge and every bracket is placed from the site measurements before the glass is made. "
              "There is no second attempt."]),
            ("The details that stop water",
             ["Water does not travel in straight lines. It runs along the bottom edge, creeps through the gap "
              "at a hinge and pools where a seal meets a floor that falls the wrong way. The details that stop "
              "it are unglamorous: a seal that follows the actual floor line, a door that closes against a "
              "fixed panel rather than a wall, and a screen sized so the water has somewhere to go.",
              "This is why we ask what is happening to the floor before the screen is ordered, and why a screen "
              "fitted before the tiler has finished is a screen that gets remade."]),
        ],
        "points": [
            "Measure after tiling — three widths, two heights, the floor fall and the waste position",
            "Door swing is set from what is in the room, not from what looks symmetrical",
            "Toughened glass cannot be re-drilled: every hole is placed from the site measurement",
            "A screen that is 2 mm out at the bottom leaks no matter how good the seal is",
        ],
        "faqs": [
            ("Can you measure before the tiler finishes to save time?",
             "No — and a screen made from a pre-tiling measurement is the most common reason a job gets remade. "
             "The measurement is the part that makes the rest work."),
            ("Do you supply the screen only, or install it?",
             "Supply and install. A frameless screen is a fitted product; the installation is where the "
             "measurement is proved or wasted."),
            ("My wall is out of square. Is that a problem?",
             "It is normal. Out-of-square walls are measured, not corrected — the screen is made to the room "
             "that exists."),
        ],
    },
    {
        "slug": "toughened-or-laminated",
        "title": "Toughened or laminated?",
        "dek": "Two safety glasses that behave completely differently when they break.",
        "service": "glass-replacement",
        "sections": [
            ("What each one does when it fails",
             ["Toughened glass is heated and rapidly cooled so the outer surfaces are in compression. When it "
              "breaks it releases into thousands of small blunt pieces — which is why it is used where "
              "somebody might walk into it. It is strong against impact but it does not stay in the opening "
              "once broken: the whole panel goes.",
              "Laminated glass is two or more sheets bonded to a plastic interlayer. When it breaks the crack "
              "runs but the pieces stay attached to the interlayer. It stays in the frame, keeps the weather "
              "out and keeps the opening closed — which is why it is used where falling glass or staying "
              "secure matters."]),
            ("Where each one belongs",
             ["Doors, door side panels and low glass in residential buildings are the classic toughened "
              "locations: the concern is a person going through it. Overhead glazing, balustrades, shopfronts "
              "in some situations and anywhere the glass is above people or needs to stay in place fall on the "
              "laminated side, because the concern is what comes down.",
              "There are also locations where the requirement is both — and in those cases the make-up is "
              "laminated glass made from toughened sheets. That is not a premium upsell; it is the only way to "
              "satisfy two different requirements at once."]),
            ("Why \"safety glass\" is not a product",
             ["Safety glass is a category, not a thing you can order. A supplier who says \"it's safety glass\" "
              "has told you nothing you can check. The useful sentence names the make-up and the thickness and "
              "the standard it was selected under.",
              "This is the reason we put those three things in writing on the quote. If a job is ever "
              "inspected, or a certificate is needed, the paperwork has to match what is actually in the "
              "opening."]),
            ("What this means when something breaks",
             ["A broken toughened panel usually means the entire panel is gone — there is nothing to patch. A "
              "broken laminated panel may still be holding the weather out while you wait for the replacement. "
              "Knowing which one you have changes what you do in the first hour.",
              "If the broken glass is in a door, a low window, or anywhere a child could reach, treat the "
              "opening as unsafe until it is made safe, even if the remaining glass looks intact."]),
        ],
        "points": [
            "Toughened shatters into blunt pieces; laminated stays in the frame",
            "Location decides which one — not budget, and not preference",
            "\"Safety glass\" is a category; the make-up and standard are what count",
            "Laminated-from-toughened exists where both behaviours are required",
        ],
        "faqs": [
            ("Which is stronger?",
             "They resist different things. Toughened takes a harder direct impact before it fails; laminated "
             "stays in the opening after it fails. Stronger is the wrong question — the right one is what the "
             "glass has to do if it breaks."),
            ("Can I have normal glass if it is high up?",
             "Height is only one of the factors. Being above head height may remove the human-impact concern "
             "but add a falling-glass one, which points at laminated rather than ordinary glass."),
            ("Do I need a certificate?",
             "Some jobs require glazing certification naming what was supplied. We provide certificates where a "
             "job requires one, and the quote says so up front rather than after the invoice."),
        ],
    },
    {
        "slug": "choosing-office-partitions",
        "title": "Framed, frameless or demountable",
        "dek": "Three ways to divide a floor, and the questions that decide between them.",
        "service": "office-partitions",
        "sections": [
            ("Start with what the room has to do",
             ["A meeting room needs acoustic separation and a door that closes properly. A finance team needs "
              "privacy and a place to put a lock. A corridor needs light without turning into a tunnel. Those "
              "three briefs produce three different partition details, even when the drawings look similar.",
              "So the useful first question is not \"framed or frameless\" — it is what happens in the room, "
              "who else is on the floor, and what the ceiling and floor can carry."]),
            ("Framed: the default for a reason",
             ["Framed aluminium partitions carry their structure in the frame, which means the glass can be "
              "thinner, the panels can be larger, and doors hang from something designed to take the weight. "
              "They also give you a place to put a head channel that lands on structure rather than on "
              "plasterboard, and a base detail that survives a floor that is not level.",
              "Most commercial fitouts end up here because it is the cheapest way to get a full-height, "
              "acoustically sensible wall that will still be straight in five years."]),
            ("Frameless: less metal, more discipline",
             ["Frameless glazing puts the structure into the glass and the fittings, which looks better and "
              "forgives less. It needs a floor and ceiling that are actually parallel, and it needs the door "
              "hardware to be right, because there is no frame to hide a hinge in.",
              "It also costs more per square metre than framed glazing, not because the glass is special but "
              "because the setting out and the fixings are unforgiving. Worth it where the sight lines matter; "
              "wasteful in a back-of-house corridor."]),
            ("Demountable: for tenancies that move",
             ["A demountable system is designed to be taken down and rebuilt, which changes the detail "
              "everywhere: how panels lock together, how the head is trimmed, how services are handled. If a "
              "tenancy is a three-year proposition, demountable can be the difference between an asset and a "
              "skip. If it is a ten-year home, it usually buys nothing."]),
            ("The details that decide whether it feels right",
             ["Manifestation — the markings on the glass — is not decoration. It is what stops people walking "
              "into a panel that looks like an opening, and it is required on large glazed areas. Where it goes "
              "and how much of it there is changes how the room feels as much as how safe it is.",
              "The other one is the door. A glass partition with a badly hung door reads as cheap no matter how "
              "good the glass is: closers that drift, gaps at the head, and a latch that needs a shove."]),
        ],
        "points": [
            "Decide from the brief (acoustics, privacy, light), not from a picture",
            "Framed is cheaper and straighter; frameless is quieter visually and unforgiving",
            "Demountable pays only if the tenancy is likely to move",
            "Manifestation is a safety requirement that also sets the look of the room",
        ],
        "faqs": [
            ("Can you match an existing partition?",
             "Usually. Send a photo of the head, base and door detail and we can tell you what system it looks "
             "like before anyone visits."),
            ("How acoustic can a glass partition be?",
             "The glass is rarely the weak point — the frame, the seals and how the head meets the ceiling do "
             "most of the work. If acoustics matter, say so at the brief stage, not after fabrication."),
            ("Do partitions need building approval?",
             "Sometimes, depending on the building, the tenancy and whether the work touches fire-rated "
             "elements. That is a question for the building surveyor; we flag it early where it looks relevant."),
        ],
    },
    {
        "slug": "broken-window-first-hour",
        "title": "A broken window: the first hour",
        "dek": "What to do before anyone arrives, and what not to do.",
        "service": "glass-replacement",
        "sections": [
            ("Make it safe first, tidy second",
             ["Broken glass in an opening is a hazard before it is a repair. The priority is to stop anyone "
              "walking into the opening or handling loose pieces: keep people and pets out of the room, close "
              "internal doors, and do not try to remove a panel that is still held at the top.",
              "Loose shards in a frame can drop without warning when a door is shut or a window is moved. If "
              "the glass is in a door or a low window, tape a temporary barrier across the opening rather than "
              "leaning anything against the glass itself."]),
            ("Temporary cover, done properly",
             ["Cardboard or ply screwed or taped to the frame is the usual temporary measure. Tape it to the "
              "frame, not to broken glass. If the opening is exposed to weather, tape the top edge first so "
              "water runs over the cover rather than behind it.",
              "Do not force a sheet of anything into the opening to wedge it — a panel under load can crack the "
              "remaining glass or damage the frame, which turns a glass replacement into a frame repair."]),
            ("What to tell us when you call",
             ["The suburb, whether the opening is a door, window or shopfront, roughly how big it is, and "
              "whether it is currently open to the weather or to the street. A photo of the whole opening — not "
              "just the break — is worth more than a description.",
              "Also say what the glass was doing: a bedroom window, a shopfront the public walks past, a "
              "balustrade. Those are different urgency levels and sometimes different glass."]),
            ("Why the replacement may not be the same glass",
             ["The pane that broke was the glass that was there, which is not always the glass the location "
              "calls for. Where the opening is in a door, alongside one, or low enough to fall into, the "
              "replacement has to suit that location rather than match the old pane.",
              "That is also why a maker cannot always promise same-day: common sizes in common make-ups can be "
              "quick, but a toughened or laminated panel made to a specific opening has to be manufactured."]),
        ],
        "points": [
            "Keep people out of the room before anything else",
            "Tape temporary cover to the frame, never to broken glass",
            "Photograph the whole opening, not just the break",
            "The right replacement is decided by the location, not by what was there",
        ],
        "faqs": [
            ("Can you come out at night?",
             "We are not an emergency 24-hour service and we will not pretend to be. If an opening is unsafe or "
             "exposed, say so on the phone and we will tell you honestly what is possible and when."),
            ("Will my insurance cover it?",
             "Often, for accidental damage — but that is a question for your insurer. What we can do is provide "
             "the written quote and the glass specification your claim needs."),
            ("Can you replace just one panel of a double-glazed unit?",
             "Usually the sealed unit is replaced as a unit rather than one pane, because the seal is the part "
             "that has failed. We measure the unit and quote on that basis."),
        ],
    },
    {
        "slug": "splashback-or-tiles",
        "title": "Glass splashback or tiles?",
        "dek": "An honest comparison, including when tiles are the better answer.",
        "service": "wardrobes-and-mirrors",
        "sections": [
            ("Where glass wins",
             ["A single pane behind a cooktop has no grout, which is the thing that discolours, cracks and "
              "collects grease. It is wiped in one movement, it reflects light back into a bench run, and it "
              "can be cut around power outlets so there are no awkward cuts at the worst place on the wall.",
              "Glass also suits a kitchen where the cabinetry is the feature, because a plain sheet does not "
              "compete with it the way a patterned tile does."]),
            ("Where tiles win",
             ["If the wall is very out of square, tile follows it and glass does not — a large pane on a wavy "
              "wall shows every deviation. Tiles are also easier to change in part later, and cheaper where the "
              "area is small and awkward.",
              "A tiled splashback can also be replaced by a tiler without touching the kitchen; a glass one has "
              "to be measured, made and fitted, so it is a bigger commitment."]),
            ("The practical details people forget",
             ["Glass needs a gap from the cooktop, and the size of that gap depends on the appliance, not on "
              "taste. It also needs somewhere for the edge to land: a bench that meets the wall cleanly on one "
              "side and a cupboard on the other is easy; a raw plasterboard edge is not.",
              "The cut-outs are the other thing. Every power point, every tap, every range hood fixing is a "
              "hole placed from a site measurement, and once the glass is toughened none of them can move."]),
            ("Choose on the wall you have",
             ["The right question is not which looks better in a photo. It is whether your wall is flat enough "
              "for a pane, whether the bench and cupboards give the glass a clean edge to sit against, and "
              "whether you want to change it again in five years.",
              "If the answer to those is yes, glass is the lower-maintenance choice. If the wall is a mess or "
              "the budget is tight, tile is not a compromise — it is the correct answer."]),
        ],
        "points": [
            "Glass: no grout, easy clean, light into the bench — needs a flat wall",
            "Tile: follows an out-of-square wall and is cheaper to change in part",
            "Appliance clearance decides part of the layout before anything is ordered",
            "Every cut-out is measured once and cannot be moved after tempering",
        ],
        "faqs": [
            ("Can a splashback go behind a freestanding cooker?",
             "Yes, with the correct clearance from the appliance and a suitable make-up. The appliance's "
             "installation instructions set that distance, so bring them to the measure."),
            ("Can you cut around existing power points?",
             "Yes — the cut-outs are measured from the installed positions. That is also why we measure after "
             "the electrician has finished, not before."),
            ("Will a large pane show the wall behind it?",
             "It will show the wall it is fixed to. That is the main argument for tile in an older kitchen."),
        ],
    },
]

# --------------------------------------------------------------------- areas
# Extra paragraphs rendered on each service-area page. Written per corridor so the
# pages are not one template with the suburb swapped.

AREA_DETAIL = {
    "south-east-melbourne": {
        "detail": [
            "This is home. The workshop is in Narre Warren East, so the Casey corridor is where a site visit is "
            "easiest to arrange and where a second trip — for a re-measure after tiling, or a missing bracket — "
            "costs an hour rather than a day.",
            "The housing stock here is mostly 1980s to 2000s brick veneer, which brings its own patterns. "
            "Bathrooms from that period are often out of square by more than the tiles suggest, and original "
            "windows are commonly single-glazed aluminium with frames that have moved. Later estates bring "
            "larger openings and more full-height glass, which changes what the glass has to do structurally.",
            "Commercial work runs along the Princes Highway corridor and through the Dandenong industrial "
            "estates: shopfronts, office fitouts inside warehouses, and glazed entries where the door is used "
            "by the public a hundred times a day.",
        ],
        "common": ["Frameless shower screens after a bathroom renovation",
                   "Broken window and door glass, made safe and replaced",
                   "Office partitions inside warehouse tenancies",
                   "Mirror wardrobe doors and kitchen splashbacks"],
    },
    "inner-east-melbourne": {
        "detail": [
            "The inner east has two very different kinds of job. The first is commercial: offices in Hawthorn, "
            "Richmond and Box Hill where a floor is being divided into meeting rooms and the brief is light "
            "without noise travelling.",
            "The second is period housing — solid brick, lath and plaster, and windows that have been repaired "
            "before. Openings in these houses are rarely true, and a screen or splashback measured off a "
            "drawing rather than the wall will not fit. Where an original window is being replaced, the "
            "interesting question is usually how to keep the look while meeting current requirements.",
        ],
        "common": ["Framed and frameless office partitions in tenancy fitouts",
                   "Period-home window glass replacement",
                   "Shower screens in renovated bathrooms",
                   "Glass balustrades on rear extensions"],
    },
    "northern-melbourne": {
        "detail": [
            "Northern Melbourne is warehouse country: Epping, Campbellfield and Thomastown have large floor "
            "plates where glass is dividing space rather than forming an outside wall. That changes the "
            "details — head channels have to land on structure, doors take heavier use, and manifestation "
            "matters because a forklift driver cannot see a clean pane of glass any more than a pedestrian can.",
            "There is also a steady run of office-to-warehouse conversions where an existing glazed entry "
            "needs to be brought up to what the building is now used for, and shopfront work along the "
            "industrial arterials.",
        ],
        "common": ["Office glazing inside warehouse tenancies",
                   "Shopfront and entry glass",
                   "Safety manifestation on large glazed areas",
                   "Mirrors and shower screens in staff amenity areas"],
    },
    "bayside-melbourne": {
        "detail": [
            "Bayside work leans residential. Renovated bathrooms in Mentone, Mordialloc and Cheltenham, and a "
            "lot of glass where the outside matters: pool fencing, balustrades on upper floors, and doors that "
            "open onto a deck.",
            "Salt air is a real factor here. It attacks fittings before it attacks glass, which is why the "
            "hardware on a balustrade or a pool fence matters as much as the panels, and why a cheaper fitting "
            "can look tired in a couple of years.",
            "The bathroom work is mostly post-renovation screens measured against new tiles, and mirrors where "
            "the wall behind them is doing something unhelpful — a curved or out-of-square wall shows up in a "
            "mirror more than in anything else in the house.",
        ],
        "common": ["Frameless glass pool fencing and balustrades",
                   "Shower screens in renovated bathrooms",
                   "Wall mirrors and mirror wardrobe doors",
                   "Sliding glass doors onto decks and alfrescos"],
    },
    "gippsland": {
        "detail": [
            "Gippsland is scheduled work rather than same-week work. Jobs are grouped into blocks — Warragul, "
            "Drouin, Traralgon, the Latrobe Valley — so the travel is planned rather than repeated, and larger "
            "projects are the ones that make the trip worthwhile.",
            "The work tends to be bigger when it happens: whole-house glazing in a new build, a shopfront "
            "refit, or a commercial fitout where the glass is a large part of the contract. Smaller jobs still "
            "get done, but they are combined with others on the same run rather than given their own day.",
            "Being honest about this is more useful than pretending otherwise: if you are in Gippsland and the "
            "job is one mirror, it may be worth waiting until we are already coming.",
        ],
        "common": ["New-build glazing packages",
                   "Commercial fitout glazing",
                   "Shower screens and mirrors in renovation runs",
                   "Glass replacement grouped into scheduled visits"],
    },
}

# ------------------------------------------------------------------ projects
# Extra paragraphs appended to each case study. These are written as engineering
# narrative — what was found, what was decided, what it changed.
PROJECT_EXTRA = {
    "thorn-office-fitout": [
        "The constraint was light, not space. The tenancy has a single window exposure at one end, so any solid "
        "wall through the middle would have left the back of the office permanently dark. Full-height glass was "
        "the only version of the brief that worked.",
        "Setting out was the part that decided the job. The head channel had to land on structure rather than "
        "on a plasterboard ceiling, and the floor was not level across the run — both of which change the panel "
        "heights before anything is fabricated. Doors were hung with patch fittings so the sight line through "
        "the suite is uninterrupted from the entry to the far wall.",
        "The result reads as one continuous glazed plane rather than a series of rooms with glass in them, "
        "which is what the client was actually buying.",
    ],
    "chen-foods-offices": [
        "This was corridor glazing: offices along a busy thoroughfare that needed daylight without opening "
        "themselves up to everyone walking past.",
        "The head detail follows an existing bulkhead rather than cutting through it, which meant measuring the "
        "bulkhead as built instead of trusting the reflected ceiling plan. Glass was kept clear with manifestation "
        "at door height only, so the corridor borrows light from the offices while the offices keep a visual "
        "connection back to the floor.",
        "Solid timber doors were kept where privacy matters most. The useful outcome is that the corridor no "
        "longer feels like a tunnel and the offices no longer feel like cupboards.",
    ],
    "frameless-shower-screens": [
        "A frameless screen is measured after the tiling, when the finished wall and floor faces exist. On this "
        "job the walls were out of square across the opening, which is normal: the frame is the drawing's idea "
        "of the room, the tiles are the room.",
        "Every hole for every hinge and bracket was placed from those site measurements before the glass was "
        "tempered, because a toughened panel cannot be drilled afterwards. Hinge positions were set so the door "
        "clears the vanity and the floor fall rather than being centred for appearance.",
        "The screen is 10 mm toughened glass with polished edges, hinged off the return wall with a fixed panel. "
        "The visible result is almost nothing — which is the point of a frameless screen.",
    ],
}

# ------------------------------------------------------------------- answers
# The answers hub. Groups of (question, answer). Substantial, non-duplicative
# answers — this is the page answer engines are most likely to quote.
ANSWERS = [
    ("Glass and safety", [
        ("Do you give prices over the phone?",
         "No, and it is not a sales tactic. Glass is cut to the opening, and the make-up that is suitable for "
         "that location changes with the panel size, how high it sits above the floor and what is above and "
         "below it. A number given without seeing the opening is a number that will not hold. The measure and "
         "quote are free across Melbourne metro."),
        ("What does AS 1288 actually cover?",
         "AS 1288 is the Australian Standard for glass in buildings — it sets out how glass is selected for a "
         "given location, taking into account the size of the pane, how it is supported, how high it is above "
         "the floor and what it has to resist. In practical terms it is the reason two similar-looking windows "
         "can need different glass."),
        ("What is AS 2208 then?",
         "AS 2208 covers safety glazing materials in buildings — the materials themselves and where they must "
         "be used. AS 1288 selects the glass for the location; AS 2208 says what counts as safety glazing. Both "
         "turn up in the paperwork on a job that needs certification."),
        ("Is toughened glass the same as safety glass?",
         "Toughened glass is one kind of safety glazing. Laminated glass is another, and laminated glass made "
         "from toughened sheets is a third combination. \"Safety glass\" on its own is a category, not a "
         "specification — the useful description names the make-up and the thickness."),
        ("Can you tell whether glass is toughened by looking at it?",
         "Not reliably. Toughened glass usually carries a permanent mark near a corner, but the absence of a "
         "mark does not prove anything, and some marks are on the edge. If it matters, the paperwork is the "
         "answer, not a guess."),
        ("Do I need a glazing certificate?",
         "Some jobs do — particularly commercial work and anything where a building surveyor or certifier wants "
         "the glass documented. A certificate records the glass supplied, its make-up and the standard it was "
         "selected under. Where a job needs one, we say so on the quote rather than after the invoice."),
    ]),
    ("Shower screens and mirrors", [
        ("When should a shower screen be measured?",
         "After tiling, when the finished wall and floor are in place. Measuring earlier means measuring a guess "
         "about where the finished face will end up, and the gap between the guess and the room is what makes a "
         "screen leak or a door bind."),
        ("How thick should shower screen glass be?",
         "Frameless screens are commonly 10 mm toughened, because the glass carries the structure. Semi-frameless "
         "and framed screens can use thinner glass because the frame does some of that work. The right answer "
         "depends on the system, the panel size and the location — not on a preference."),
        ("Can a frameless screen be fitted to an out-of-square wall?",
         "Yes. Out-of-square is normal and is measured rather than corrected. What it cannot tolerate is a "
         "screen made before the wall was measured."),
        ("Why does my mirror show every mark on the wall behind it?",
         "Because a mirror is flat and the wall is not. Mirror shows every deviation in the surface it is fixed "
         "to, which is why the fixing method matters as much as the glass. On an uneven wall, the answer is "
         "usually to fix to a flat substrate rather than to the wall itself."),
        ("Can you supply mirror wardrobe doors to replace sliding doors?",
         "Yes — measured to the opening, cut with polished or bevelled edges, and hung on hardware rated for the "
         "door weight. Sliding is the usual choice where there is no room for a door to swing."),
        ("What is the difference between a wall mirror and a mirror television?",
         "A mirror television is a display behind a mirrored surface that becomes transparent when the screen is "
         "on. It is a fitout item rather than a glass item, and it needs power and a recess planned before the "
         "wall is closed up."),
    ]),
    ("Commercial and office work", [
        ("Can you work inside an occupied office?",
         "Often yes, with the work sequenced around the floor — but it depends on the building's rules, access "
         "hours and whether the work involves anything fire rated. Say what the building requires at the quote "
         "stage rather than on the day."),
        ("Do you handle the door hardware as well as the glass?",
         "Yes. A partition with a badly hung door reads as cheap no matter how good the glass is, so the closer, "
         "the hinges and the latch are part of the same job."),
        ("What is manifestation and is it required?",
         "Manifestation is the marking applied to glass so people can see it is there. It is a safety "
         "requirement on large glazed areas, and it also sets how the room feels. Where it is required, the "
         "answer is not optional decoration."),
        ("Can you match partitions to an existing system?",
         "Usually — send photographs of the head, base and door detail and we can identify the likely system "
         "before a site visit."),
        ("Do you do shopfronts?",
         "Yes: shopfront glazing, entries, and replacement of damaged shopfront glass. Make-safe comes first "
         "where an opening is exposed to the street."),
    ]),
    ("Process and coverage", [
        ("What areas do you cover?",
         "Melbourne metro, with the south east — Narre Warren, Berwick, Cranbourne, Pakenham, Dandenong — as "
         "home base. Gippsland work is scheduled in blocks rather than same-week. If you are further out, ask: "
         "larger jobs travel."),
        ("How long does a job take?",
         "Shower screens and mirrors are typically one to two weeks from measure, because toughened glass is "
         "made to your dimensions. Replacement glass for common sizes can be same or next day. Installation is "
         "usually a few hours. Lead times are confirmed at quote rather than published, because they move with "
         "supplier load."),
        ("Who measures and who installs?",
         "The same glazier who quoted the job. It is the simplest way to make sure the glass that arrives is the "
         "glass that was measured."),
        ("Do you need access to power and water?",
         "Power for tools, yes. Water is not usually needed for installation. If the job is a commercial site "
         "with induction or sign-in requirements, those need to be arranged before the day."),
        ("Can you work from plans if the building is not finished?",
         "We can quote from drawings, but we will not fabricate glass from them. Glass is made from site "
         "measurements once the finished faces exist."),
        ("How do I get a quote?",
         "Send a photo of the opening, the suburb and a rough size through the quote form, or call. A photo is "
         "usually enough to tell you what is possible before anyone drives out."),
    ]),
]
