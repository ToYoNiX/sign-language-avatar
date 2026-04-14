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
[symmetry]  →  hand shape  →  thumb modifier  →  finger direction  →  palm orientation  →  location  →  [contact]  →  movement  →  [movement modifier]  →  [repeat]
```

Getting this wrong produces no visible error — the avatar either does nothing or falls back to the idle pose.

---

## Minimal working example

Based directly on a real sign from the dictionary (`1.sigml` — the number 1):

```xml
<sigml>
  <hns_sign gloss="1">
    <hamnosys_nonmanual></hamnosys_nonmanual>
    <hamnosys_manual>
      <hamfist/>
      <hamthumboutmod/>
      <hamextfingero/>
      <hampalml/>
      <hamshouldertop/>
      <hammoveo/>
      <hamsmallmod/>
    </hamnosys_manual>
  </hns_sign>
</sigml>
```

Two-handed mirror example (number 6 — `6.sigml`):

```xml
<sigml>
  <hns_sign gloss="6">
    <hamnosys_nonmanual></hamnosys_nonmanual>
    <hamnosys_manual>
      <hamparbegin/>
        <hamfist/>
        <hamthumboutmod/>
        <hamextfingero/>
        <hampalml/>
      <hamplus/>
        <hamfinger2345/>
        <hamthumboutmod/>
        <hamextfingeru/>
        <hampalmd/>
      <hamparend/>
      <hamparbegin/>
        <hamshoulders/>
        <hamlrat/>
      <hamplus/>
        <hamlrat/>
        <hamshoulders/>
      <hamparend/>
    </hamnosys_manual>
  </hns_sign>
</sigml>
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
| `<hamindexfinger/>` | Index only |
| `<hammiddlefinger/>` | Middle only |
| `<hampinky/>` | Pinky only |
| `<hamringfinger/>` | Ring only |
| `<hamthumb/>` | Thumb only |

### Finger modifiers

| Element | Meaning |
|---|---|
| `<hamfingerbent/>` | Bent fingers |
| `<hamdoublebent/>` | Double bent |
| `<hamdoublehooked/>` | Double hooked |
| `<hamfingerbase/>` | Bend at base joint |
| `<hamfingermidjoint/>` | Bend at mid joint |
| `<hamfingernail/>` | Fingernail contact |
| `<hamfingerpad/>` | Finger pad |
| `<hamfingerside/>` | Finger side |
| `<hamfingertip/>` | Fingertip |
| `<hamfingerplay/>` | Wiggling fingers |

### Thumb modifiers

| Element | Meaning |
|---|---|
| `<hamthumbacrossmod/>` | Thumb across palm |
| `<hamthumbopenmod/>` | Thumb open |
| `<hamthumboutmod/>` | Thumb out |
| `<hamthumbside/>` | Thumb side |
| `<hamthumbball/>` | Thumb ball |

---

## Palm orientation

| Element | Meaning |
|---|---|
| `<hampalmd/>` | Palm down |
| `<hampalmdr/>` | Palm down-right |
| `<hampalmdl/>` | Palm down-left |
| `<hampalmu/>` | Palm up |
| `<hampalmul/>` | Palm up-left |
| `<hampalmur/>` | Palm up-right |
| `<hampalml/>` | Palm left |
| `<hampalmr/>` | Palm right |

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

## Location

| Element | Meaning |
|---|---|
| `<hamneutralspace/>` | Neutral signing space (in front of body) |
| `<hamneutral/>` | Neutral |
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
| `<hamwristtothumb/>` | Wrist — thumb side |
| `<hamwristtopinky/>` | Wrist — pinky side |
| `<hamwristtoback/>` | Wrist — back |

---

## Movement

### Linear moves

`<hammove{dir}/>` — replace `{dir}` with one of the same direction suffixes as extended finger direction, plus `cross`.

Examples: `<hammoveu/>`, `<hammovedr/>`, `<hammovecross/>`

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
| `<hamreplace/>` | Replace the current hand shape / orientation mid-sign (transition to next pose) |
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
