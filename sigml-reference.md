# SiGML Reference

Supported syntax for this CWASA build. Use the `/playground` page to test any snippet live.

---

## Document structure

```xml
<sigml>
  <hns_sign gloss="word">
    <hamnosys_nonmanual> ... </hamnosys_nonmanual>
    <hamnosys_manual> ... </hamnosys_manual>
  </hns_sign>
</sigml>
```

Multiple `<hns_sign>` blocks inside one `<sigml>` play sequentially.

---

## Element ordering

**Order matters.** CWASA parses elements top-to-bottom and builds the pose incrementally. The correct order inside `<hamnosys_manual>` is:

```
handshape  →  thumb modifier  →  finger modifier  →  extended finger direction  →  palm orientation  →  location  →  movement  →  movement modifier
```

Getting this wrong produces no visible error — the avatar either does nothing or falls back to the idle pose.

---

## Critical: palm orientation vs finger direction

Palm orientation and extended finger direction work **together** to define the full hand orientation. They are **not** independent — the visual result depends on their combination.

The 8 palm tokens cover compass directions only: `u`, `ur`, `r`, `dr`, `d`, `dl`, `l`, `ul`. There is **no** `hampalmi` or `hampalmo` — those do not exist and will cause silent failure (avatar does nothing).

### Verified pattern: back of hand toward viewer

To keep the **back of the hand facing the viewer** while changing the finger direction, the palm suffix **mirrors** the extended finger suffix. Verified against the avatar:

| Extended finger direction | Palm to use | Result |
|---|---|---|
| `hamextfingeru` | `hampalmu` | Finger straight up |
| `hamextfingerur` | `hampalmr` | Finger 45° upper-right |
| `hamextfingerul` | `hampalml` | Finger 45° upper-left |

The rule: **palm suffix = finger suffix, but drop the `u`** (e.g. `ur` → `r`, `ul` → `l`, `u` → `u`). Apply the same logic to other directions you need to test.

---

## Minimal working example

Number 1 — index finger pointing up, back of hand toward viewer:

```xml
<sigml>
  <hns_sign gloss="1">
    <hamnosys_nonmanual></hamnosys_nonmanual>
    <hamnosys_manual>
      <hamfinger2/>
      <hamextfingeru/>
      <hampalmu/>
      <hamshouldertop/>
      <hammoveo/>
      <hamsmallmod/>
    </hamnosys_manual>
  </hns_sign>
</sigml>
```

---

## Verified numbers (1–10)

All tested and confirmed working against the avatar. These use a consistent template:
`handshape → [thumb mod] → [finger mod] → hamextfingeru → hampalmu → hamshouldertop → hammoveo → hamsmallmod`

**1** — index finger up:
```xml
<hamnosys_manual>
  <hamfinger2/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**2** — index + middle spread, thumb across:
```xml
<hamnosys_manual>
  <hamfinger23spread/>
  <hamthumbacrossmod/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**3** — index + middle + ring up, thumb across, pinky bent:
```xml
<hamnosys_manual>
  <hamfinger2345/>
  <hamthumbacrossmod/>
  <hampinky/>
  <hamfingerbendmod/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**4** — four fingers up, thumb across:
```xml
<hamnosys_manual>
  <hamfinger2345/>
  <hamthumbacrossmod/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**5** — all fingers up including thumb:
```xml
<hamnosys_manual>
  <hamfinger2345/>
  <hamthumboutmod/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**6** — thumb only up (fist + thumb out):
```xml
<hamnosys_manual>
  <hamfist/>
  <hamthumboutmod/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**7** — thumb + index up:
```xml
<hamnosys_manual>
  <hamfinger2/>
  <hamthumboutmod/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**8** — thumb + index + middle spread up:
```xml
<hamnosys_manual>
  <hamfinger23spread/>
  <hamthumboutmod/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**9** — thumb + index + middle + ring up, pinky bent:
```xml
<hamnosys_manual>
  <hamfinger2345/>
  <hamthumboutmod/>
  <hampinky/>
  <hamfingerbendmod/>
  <hamextfingeru/>
  <hampalmu/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**10 (tilted right)** — like 1 but 45° to the right:
```xml
<hamnosys_manual>
  <hamfinger2/>
  <hamextfingerur/>
  <hampalmr/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

**10 (tilted left)** — like 1 but 45° to the left:
```xml
<hamnosys_manual>
  <hamfinger2/>
  <hamextfingerul/>
  <hampalml/>
  <hamshouldertop/>
  <hammoveo/>
  <hamsmallmod/>
</hamnosys_manual>
```

---

## Hand shape

| Element | Meaning |
|---|---|
| `<hamflathand/>` | Flat / open hand |
| `<hamfist/>` | Closed fist |
| `<hamfinger2/>` | Index finger extended |
| `<hamfinger23/>` | Index + middle extended |
| `<hamfinger23spread/>` | Index + middle spread (V) |
| `<hamfinger2345/>` | Four fingers extended |
| `<hampinch12/>` | Pinch (index + thumb) |
| `<hampinch12open/>` | Open pinch |
| `<hampinchall/>` | All-finger pinch |
| `<hamcee12/>` | C-shape (index + thumb) |
| `<hamceeall/>` | Full C-shape |

### Individual finger selectors

Used **after** the base handshape to target a specific finger for a modifier (e.g. bend just the pinky):

| Element | Finger |
|---|---|
| `<hamthumb/>` | Thumb (1) |
| `<hamindexfinger/>` | Index (2) |
| `<hammiddlefinger/>` | Middle (3) |
| `<hamringfinger/>` | Ring (4) |
| `<hampinky/>` | Pinky (5) |

### Finger modifiers

Applied **after** the finger selector (or directly after the handshape if targeting all fingers):

| Element | Meaning |
|---|---|
| `<hamfingerbendmod/>` | Bend the selected finger(s) — use this, NOT `hamfingerbent` |
| `<hamfingerstraightmod/>` | Straighten the selected finger(s) |
| `<hamdoublebent/>` | Double bent |
| `<hamdoublehooked/>` | Double hooked |
| `<hamfingerhookmod/>` | Hook / claw bend |
| `<hamfingerplay/>` | Wiggling fingers |

> **Note:** The correct token is `<hamfingerbendmod/>`. Using `<hamfingerbent/>` will silently fail.

### Thumb modifiers

Applied **immediately after** the base handshape, before any finger modifiers:

| Element | Meaning |
|---|---|
| `<hamthumbacrossmod/>` | Thumb folded across palm (use for numbers 2–4) |
| `<hamthumboutmod/>` | Thumb extended outward (use for numbers 5–9) |
| `<hamthumbopenmod/>` | Thumb open (wider gap) |
| `<hamthumbball/>` | Thumb ball contact |
| `<hamthumbside/>` | Thumb side reference |

---

## Extended finger direction

`<hamextfinger{dir}/>` — replace `{dir}` with one of:

| Suffix | Direction |
|---|---|
| `u` | Up |
| `d` | Down |
| `l` | Left |
| `r` | Right |
| `i` | Inward (toward body) |
| `o` | Outward (away from body) |
| `ul` `ur` `dl` `dr` | Diagonal combinations |
| `ui` `uo` `di` `do` | Up/down + in/out combinations |
| `il` `ir` `ol` `or` | In/out + left/right combinations |

Examples: `<hamextfingeru/>`, `<hamextfingerdo/>`, `<hamextfingeril/>`

---

## Palm orientation

Only these 8 tokens exist. There is no `hampalmi` or `hampalmo`.

| Element | Direction |
|---|---|
| `<hampalmu/>` | Palm up — use this when finger points up and back of hand faces viewer |
| `<hampalmur/>` | Palm up-right |
| `<hampalmr/>` | Palm right |
| `<hampalmdr/>` | Palm down-right |
| `<hampalmd/>` | Palm down |
| `<hampalmdl/>` | Palm down-left |
| `<hampalml/>` | Palm left |
| `<hampalmul/>` | Palm up-left |

---

## Location

| Element | Meaning |
|---|---|
| `<hamneutralspace/>` | Neutral signing space (in front of body) |
| `<hamhead/>` | Head |
| `<hamheadtop/>` | Top of head |
| `<hamforehead/>` | Forehead |
| `<hamcheek/>` | Cheek |
| `<hamchin/>` | Chin |
| `<hamunderchin/>` | Under chin |
| `<hamneck/>` | Neck |
| `<hamlips/>` | Lips |
| `<hamteeth/>` | Teeth |
| `<hamtongue/>` | Tongue |
| `<hamnose/>` | Nose |
| `<hamnostrils/>` | Nostrils |
| `<hamear/>` | Ear |
| `<hamearlobe/>` | Earlobe |
| `<hamchest/>` | Chest |
| `<hamshoulders/>` | Shoulders |
| `<hamshouldertop/>` | Top of shoulder |
| `<hamstomach/>` | Stomach |
| `<hambelowstomach/>` | Below stomach |
| `<hamelbow/>` | Elbow |
| `<hamelbowinside/>` | Inner elbow |
| `<hamlowerarm/>` | Lower arm |
| `<hamwristback/>` | Back of wrist |
| `<hamhandback/>` | Back of hand |
| `<hampalm/>` | Palm |

---

## Movement

### Linear moves

`<hammove{dir}/>` — replace `{dir}` with one of the same direction suffixes as extended finger direction.

Examples: `<hammoveu/>`, `<hammovedr/>`, `<hammoveo/>`

### Arcs

`<hamarc{dir}/>` — `d` `l` `r` `u`

### Circles

`<hamcircle{dir}/>` — same direction suffixes as linear moves.

Examples: `<hamcircleu/>`, `<hamcircleol/>`

### Clock sweeps

`<hamclock{dir}/>` — `d` `dl` `dr` `full` `l` `r` `u` `ul` `ur`

### Ellipses

| Element | Meaning |
|---|---|
| `<hamellipseh/>` | Horizontal ellipse |
| `<hamellipsev/>` | Vertical ellipse |
| `<hamellipseul/>` | Ellipse upper-left |
| `<hamellipseur/>` | Ellipse upper-right |

### Wrist motions

| Element | Meaning |
|---|---|
| `<hamtwisting/>` | Wrist twist |
| `<hamswinging/>` | Swinging |
| `<hamnodding/>` | Wrist nod |
| `<hambrushing/>` | Brushing |
| `<hamstircw/>` | Stirring clockwise |
| `<hamstirccw/>` | Stirring counter-clockwise |
| `<hamwavy/>` | Wavy |
| `<hamzigzag/>` | Zigzag |
| `<hamwristpulse/>` | Wrist pulse |

### Hold / contact

| Element | Meaning |
|---|---|
| `<hamnomotion/>` | Hold — no movement |
| `<hamhalt/>` | Stop motion |
| `<hamtouch/>` | Touch |
| `<hambetween/>` | Between two locations |
| `<hambehind/>` | Behind |

---

## Timing, speed, size

| Element | Meaning |
|---|---|
| `<hamfast/>` | Fast |
| `<hamslow/>` | Slow |
| `<hamtense/>` | Tense / sharp |
| `<hamincreasing/>` | Increasing speed |
| `<hamdecreasing/>` | Decreasing speed |
| `<hamlargemod/>` | Large movement |
| `<hamsmallmod/>` | Small movement |

---

## Repetition

| Element | Meaning |
|---|---|
| `<hamrepeatfromstart/>` | Repeat from start |
| `<hamrepeatcontinue/>` | Continue repeating |
| `<hamrepeatreverse/>` | Repeat in reverse |
| `<hamrepeatfromstartseveral/>` | Several repetitions from start |
| `<hamrepeatcontinueseveral/>` | Several repetitions continuing |

---

## Symmetry and two-hand

| Element | Meaning |
|---|---|
| `<hamsymmlr/>` | Mirror left-right (both hands) |
| `<hamsymmpar/>` | Parallel (both hands same direction) |
| `<hamlrat/>` | Left-right alternating |
| `<hamlrbeside/>` | Hands beside each other |
| `<haminterlock/>` | Interlocked |
| `<hamarmextended/>` | Arm extended |
| `<hamnondominant>...</hamnondominant>` | Non-dominant (passive) hand block |

---

## Sequencing and grouping

| Element | Meaning |
|---|---|
| `<hamparbegin/>` / `<hamparend/>` | Parallel (simultaneous) block |
| `<hamplus/>` | Separator between two simultaneous elements inside a `<hamparbegin>` block |
| `<hamseqbegin/>` / `<hamseqend/>` | Sequential block |
| `<hamaltbegin/>` / `<hamaltend/>` | Alternating block |
| `<hamfusionbegin/>` / `<hamfusionend/>` | Fusion (blended transition) block |
| `<hamreplace/>` | Replace the current hand shape / orientation mid-sign |
| `<hamrest/>` | Rest pose |

---

## Non-manual (facial expressions)

Inside `<hamnosys_nonmanual>`:

| Element | Meaning |
|---|---|
| `<hameyebrows/>` | Eyebrow raise / furrow |
| `<hameyes/>` | Eye shape |
| `<hamnodding/>` | Head nod |

Leave the block empty (`<hamnosys_nonmanual></hamnosys_nonmanual>`) for no facial expression.
