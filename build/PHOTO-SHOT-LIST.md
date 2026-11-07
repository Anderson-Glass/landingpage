# Photography shot list — Anderson Glass & Glazing

The site currently runs on 13 photos from the old site. Most are office partitions, several are only
500px wide. A half-day with a phone would lift the site more than any further design work.

## Before you leave the ute

- Wipe the glass. A microfibre and a squirt bottle is the difference between "clean job" and "streaky job".
- Clear the site: no tradie bags, no coffee cups, no ladders in frame.
- Turn the lights on inside so glass reads as glass, not grey panels.

## How to shoot (phone is fine)

| Do | Don't |
|---|---|
| Landscape, 4:3, held level | Portrait for wide shots |
| Natural light; no flash | Overhead lights alone (reflections) |
| Stand square to the wall, eye height | Shoot from waist height looking up |
| Take 2–3 of every subject | One shot and move on |
| Step back so the frame edges are visible | Crop the frame out of shot |
| Include one person or a chair for scale | Empty rooms with nothing to size against |

Watch your own reflection — a phone-shaped dark rectangle in the glass ruins the shot. Shift sideways
until it's out of frame.

## The 20 frames worth having

**Every job — the essentials**
1. Wide, straight-on: the whole run, floor to ceiling.
2. Through-glass: stand inside looking out, so the glass reads as transparent.
3. Detail: the junction — head channel, patch fitting, hinge, or the door edge.
4. Edge-on: the glass edge showing thickness (this is what sells "10mm toughened").

**Commercial (2 jobs)**
5. Shopfront from the street, straight on, sign visible.
6. Entry door detail — handle, closer, bottom rail.
7. Corridor of glass, shot down its length (the strongest hero image you can give me).
8. Meeting room seen through partition glass, lights on inside.

**Residential (2 jobs)**
9. Frameless shower screen, wide, door closed, towel and bath mat for warmth.
10. Shower screen detail — hinge and seal.
11. Mirror wardrobe doors, wide, with the room reflected.
12. Wall mirror or splashback, angled slightly so the reflection shows the room.

**Glass replacement**
13. Before: the break, honest and clear.
14. After: same angle, same distance. (This pair is worth more than ten finished shots.)

**Bonus if you have them**
15. Balustrade with a view behind it.
16. Over-height glazing shot from below.
17. Glass being installed — hands, suction cups, the moment of the lift.
18. Your ute/workshop with glass racked.
19. A finished job at dusk with interior lights on (gold for the hero position).
20. Anything where the glass is doing something clever — a corner, a curve, a frameless join.

## Which ones I need first

Priority order if you only get 10 shots: **7, 1, 9, 2, 5, 3, 11, 12, 13+14, 19.**

## Rights and privacy

- Only your own completed work.
- For named commercial jobs (Thorn, Chen Foods and similar), confirm the client is happy to be named. If not, the caption becomes "Commercial fitout, south east Melbourne".
- Don't photograph anything showing a client's documents, screens, whiteboards or stock.

## Delivery

Drop originals into `~/Documents/Anderson-Glass-Website/photos-in/`.

Name them: `project-suburb-01.jpg` (e.g. `thorn-richmond-01.jpg`). Phone HEIC and JPEG are both fine.
Then run:

```bash
cd ~/Documents/Anderson-Glass-Website && python3 build/import_photos.py
```

That rotates, resizes to 480/800/1280/1920 WebP and writes them into `build/images/` with a manifest.
Tell me when they're in and I'll pick the best frames, place them in the page templates and rebuild.
