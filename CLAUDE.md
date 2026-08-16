# CLAUDE.md — ODSP-12 · `ODSP12-MB-A` rev A

Project constitution. Scope, authority, and decision protocol.
Read this, `STATE.md`, and `REQUIREMENTS.md` at the start of every session. Update
`STATE.md` during the session; update this file only when the objective itself changes.

**Status: SCHEMATIC INTAKE NEARLY CLOSED.** Electrical architecture specified
(`REQUIREMENTS.md` v0.2); tooling is KiCad 10.0.5 and verified (§7). Mechanical and fabrication
remain ⬜ UNSET and are governed by §0 — **layout is still blocked, capture is not.**

---

## 0. The UNSET rule

**⬜ UNSET is a constraint, not a blank.** It means *this value is unknown and no work may
depend on it.*

1. An UNSET value is **never** filled by inference, convention, "typical practice", or a
   plausible default. Not silently, not in a draft, not "just to have something to work with".
2. Work that depends on an UNSET value **does not start**. Work that does not depend on it
   proceeds normally.
3. UNSET resolves exactly one way: the operator states the value, it is recorded in
   `STATE.md` §1 as **T1 by decree** (or T1 with a verification note if it came from a file or
   datasheet), and this file is edited to replace the marker.
4. If a default genuinely is the right answer, it still gets **stated and logged as a decision**
   in `STATE.md` §6 with what would reopen it. A default that was chosen is fine. A default that
   was assumed is a drift.

**One standing exception, granted by the requirements doc:** `REQUIREMENTS.md` §11 explicitly
delegates five decisions to the designer. Those are not UNSET — they are *ours to decide*, under
§4 below.

---

## 1. What this project is

A single-board **automotive car-audio DSP processor**: 4 differential analog inputs (line and
speaker level), 12 differential-buffered single-ended analog outputs at ≥4.5 Vrms, coax SPDIF in,
Bluetooth A2DP sink, and a BLE/WiFi control plane, running from 12 V automotive power with
sequenced turn-on/turn-off. Signal chain per `REQUIREMENTS.md` §1: INA1650 → AK5574 → ADAU1466
SigmaDSP → 2× AK4458 → OPA1656 → RCA, with BM83 (Bluetooth) and AK4118A (SPDIF) entering through
on-chip ASRCs, and an ESP32-S3 owning all device state.

**Deliverable, in two phases:**
1. **Schematic capture** — the immediate work. `REQUIREMENTS.md` is the "architecture baseline
   for schematic capture"; no schematic exists yet, so this is greenfield.
2. **PCB layout** — placement, routing, and stackup, explicitly delegated to us by
   `REQUIREMENTS.md` header. Blocked on mechanical and fab intake (§6, Block D/E).

Everything in this repo that is not the design files is **context**, not work.

**Context:** ⬜ UNSET — who the client is, whether the process is visible as well as the result.

---

## 2. The deliverable (this is the acceptance gate)

Done means all of the following, **verifiable, not asserted**:

| # | Gate | How it is proven |
|---|---|---|
| **G0-S** | **Schematic intake complete** — tooling known, `REQUIREMENTS.md` [VERIFY] items resolved, findings register dispositioned | `STATE.md` §4 Block B closed; §7 findings all dispositioned; §8 [VERIFY] list all T1 |
| **G0-L** | **Layout intake complete** — mechanical + fab + stackup known | `STATE.md` §4 Blocks D/E closed |
| G1 | DRC: 0 errors, 0 unconnected, schematic parity clean | `kicad-cli pcb drc --severity-all --schematic-parity --exit-code-violations --format json`, report shipped with delivery |
| G1b | ERC: 0 errors; every net in §10 naming scheme; no unconnected pins without explicit no-connect flags | `kicad-cli sch erc --severity-all --exit-code-violations --format json` |
| G2 | Shipped design rules and severities used unmodified; exclusions list empty | `--severity-exclusions` on both DRC and ERC returns an **empty** violation set — a direct machine check, no baseline diff needed |
| G3 | Layer count ⬜ UNSET | stackup in the board file |
| G4 | Controlled-impedance nets meet targets — SPDIF coax 75 Ω, USB D±  90 Ω differential ⬜ *targets proposed, not yet decreed* | stated stackup + impedance calculation |
| G5 | Silkscreen legible, pin-1/polarity marks present, 0 silk errors | DRC report + operator visual check |
| G5b | Both antenna keepouts honoured **[HARD]**; no copper, no parts, board-edge relief per module datasheets | keepout zones in the board file + operator visual check |
| G6 | Fab package: gerbers, drill, CPL, BOM (with DNP column for the stuffing options) | exported files |
| G7 | Design note: everything changed, everything not honored, every assumption, every §11 delegated decision with its justification | written note |
| G8 | Post-fab electrical acceptance per `REQUIREMENTS.md` §12 | bench measurement — **not a PCB-design gate**; recorded here so the design is traceable to it |

**G0-S gates capture. G0-L gates layout.** Splitting them is deliberate: the electrical
architecture is specified well enough to capture a schematic, but the outline, stackup, and fab
capability are not known, and relocating a placed-and-routed board when those change is the
expensive failure this ordering prevents.

**Nothing counts as done because it looks done.** A gate closes when a tool output or an
operator's direct observation says so.

---

## 3. Authority order (source of truth)

Two different kinds of truth. Do not confuse them.

**Truth about what *is* (current state) — the design files:**
1. Schematic ⬜ UNSET *(does not exist yet)* — connectivity truth. Absolute, once it exists.
2. Board ⬜ UNSET *(does not exist yet)* — geometry, footprints, layers, zones.
3. Project file ⬜ UNSET — netclasses, design rules, DRC severities.
4. Exported netlists — derived views, never an override. Disagreement with the schematic is a
   **finding to log**, not a thing to silently reconcile.

**Truth about what *must be* (requirements) — [`REQUIREMENTS.md`](REQUIREMENTS.md) v0.1.**
It carries requirements not present in the files at all. Where it *describes* file state, the
files win; where it *demands* something, it wins.

Its own internal authority order, which this project adopts:
- **[HARD]** — non-negotiable. Never changed without an explicit new instruction. Currently:
  §3 clock architecture, §4 TDM map, §6.2 4.5 Vrms, §7.1 ISO 7637-2, §7.2/§7.3 sequencing,
  §8 antenna keepouts, §10 channel-to-slot naming.
- **[VERIFY]** — must be confirmed against a current datasheet *before* capture, not after.
  Tracked as a checklist in `STATE.md` §8. A [VERIFY] item is T2 at best until confirmed.
- **§11 delegated** — ours to decide, with written justification (§4 below).
- Everything else — normative, but a well-argued deviation is a question, not a violation.

**It is v0.1 and labelled a baseline — it will revise.** Cite it by section *and* version.
A v0.2 supersedes; do not merge revisions silently.

**Advisory only — never cite as evidence:** the chat message that delivered v0.1, and any
summary of it including this file's §6 digest. Read the source.

---

## 4. Scope boundaries

**In scope — do freely:** schematic capture per `REQUIREMENTS.md`; component selection within
the stated BOM; the five §11 delegated decisions; supporting calculations; layout once G0-L closes.

**Out of scope — never, without an explicit new instruction:**
- Change anything flagged **[HARD]**.
- Remap analog channel numbers against the §4 TDM slot map (§10 **[HARD]**).
- Substitute a part not named in `REQUIREMENTS.md` §2 — including the AKM→TI substitution, which
  is *approved but not authorised*: it changes TDM formats and must be flagged before use.
- Populate a DNP stuffing option (WM8804, TJA1051T-Q1, 25AA1024) on v1.
- Assign ESP32-S3 GPIO19/20 to anything but USB D±.
- Relax DRC severities or add DRC exclusions.
- Edit the schematic once it is frozen for layout — no renumbering, renaming, adding or removing
  parts.
- "Update footprints from library" over deliberate instance-level edits.
- Change board outline, mounting holes, or connector positions once set.
- Edit `REQUIREMENTS.md` to resolve a finding. Findings go in `STATE.md` §7; revisions come from
  the operator.

**Approval-gated:** AKM↔TI converter substitution · any resolution of a [VERIFY] that changes
architecture (notably BM83 master/slave, which moves a serial port) · exceeding the 200 × 140 mm
envelope · adding a rail not in §7.1 · anything that makes a §12 acceptance criterion unmeetable.

### Delegated decisions — the closed-book protocol applies

`REQUIREMENTS.md` §11 hands us five decisions outright. For these, **nothing waits**: pick the
defensible option, say why it is defensible *against the requirements' own stated intent*, state
the assumption in writing at the point of use, log it in `STATE.md` §6, and surface it in the G7
note. **A silent workaround is the failure; a documented, reversible assumption is not.**

The delegated five: AKM vs TI converters · BM83 I2S master/slave · relay vs FET mute (needs THD
justification) · SEPIC vs dual-boost for ±13V5_A (noise budget < 50 µVrms, 20 Hz–20 kHz, at the
op-amp rails) · board form factor (≤ 200 × 140 mm assumed until told otherwise).

### Channel policy — SET (Q2, 2026-08-15)

**Closed-book by default, with batched escalation.** Settled by observation rather than design:
the project had been running this for five rounds before it was written down.

| Authority | Handling |
|---|---|
| **T2 and below** | **Decide and log.** No escalation. The decision goes in `STATE.md` §6 with its reopen condition, and into the G7 note |
| **[HARD] amendments · decree conflicts · respin-class consequences** — footprints, package changes, rail architecture | **Escalate.** Do not apply, even when the fix looks obvious |
| **Stop-the-line** — anything that would invalidate work already in flight | **Escalate immediately**, interrupting the current block |

**Escalations batch at natural checkpoints**, not mid-block — finish the unit of work, then raise
them together. The exception is the stop-the-line class: F1 was one of those, and interrupting
for it was correct.

Note what this does *not* license. Closed-book applies to decisions inside our authority. It does
**not** license filling an ⬜ UNSET in §0's sense, and it does not license routing around a decree
because the workaround is available — F23's SPI escape hatch was rejected on exactly that ground:
it would have contradicted §5 to avoid a problem the decree's author would rather solve
differently. **When a decree blocks the obvious fix, that is an escalation, not an obstacle.**

Note the asymmetry: closed-book applies to *delegated* decisions. It does **not** license filling
an ⬜ UNSET in §0's sense — those are questions to the operator sitting right here.

---

## 5. Evidence and confidence protocol

**This is the core discipline and it transfers to every project.** Unknowns treated as knowns
become drifts that surface fifty decisions later, when they are expensive.

Every claim that steers a decision carries a tier. Write the tier down. Never let a claim gain
confidence it did not earn.

### T1 — Source of truth
Verified against hard evidence: a file read directly, a tool output, a datasheet, or an
operator's direct observation of the thing itself. **Highest priority when weighing any unknown.**
If a decision hinges on something not yet T1, the first move is to make it T1 — not to proceed on
the best guess. Establishing T1 almost always costs less than the drift.

**On this project specifically: a part number is not a datasheet.** Pin counts, package pitches,
full-scale output voltages, MCLK ratios, maximum SCLK, and supply currents are T2 until read from
the manufacturer's current document. `REQUIREMENTS.md` names parts; it does not characterise them.

### T2 — Highly probable
Strong reasoning, consistent with T1 facts, not directly confirmed. **Actionable** — build on it,
move forward. But it stays tagged T2 in every document and message until confirmed, and everything
downstream inherits the tag. Promote on evidence; demote and unwind if it fails.

### T3 — Likely / moderate confidence
Plausible. **Theories may branch from T3, but the branch is provisional and the root gets checked
quickly** — before the branch grows expensive. A T3 that has spawned work and is still unchecked
is itself a defect.

### T4 — Speculation
Fine to name and discuss. Never drives work. Never enters a document untagged.

**Rules of movement:** a claim rises a tier only on new evidence — never on repetition, never
because it has been useful. If a downstream fact contradicts an upstream claim, the *upstream*
claim is re-examined first.

### The operator's glance beats the clever test
The operator has the tool open. If a question can be answered by them looking at the screen for
five seconds, **ask** — do not build a script, parse a file format, or construct an experiment to
avoid asking. Autonomy is not the objective; correctness at low cost is.

Ask well: one specific question, name exactly what to look at, say what answer would change.

Prefer the **tool** for counts, coordinates, DRC results, net membership. Prefer the **operator's
eyes** for judgment, appearance, "does this look right", physical/mechanical reality, and anything
about intent.

**Ask for a screenshot whenever something fails in a way the files do not explain.** Ask *early*,
when a result is weird — not after several failed fix attempts.

**Corollary on the assistant:** a failure message must say **what blocked**, not merely that
something did. "No clear slot found" is useless; "no clear slot — the U3 module sits between them"
is the answer. Any search that can fail must report the obstacle it lost to.

### Operator statements are evidence, not truth
Treat them as strong evidence — the operator often knows things the files do not record — but not
as source of truth. Cross-check against harder evidence when cheap.

**When operator-supplied information looks anomalous, ordinary human error is the most likely
explanation and is what gets checked first:** a typo or transposed digit, a stale file or unsaved
buffer, the wrong window or wrong net selected, a misread designator or pin number, units
confusion, a stale screenshot, or memory of a previous revision.

Do not build an exotic theory until the simple mistakes are ruled out. Do not silently "correct"
it either — say plainly what does not reconcile, name the most likely simple cause, and ask.
**A wrong number accepted politely becomes a T1 that is not true**, which is the single most
expensive failure mode this protocol exists to prevent.

**This extends to the requirements document.** It is authored by a person and inherits the same
failure modes. A [HARD] flag makes a requirement binding; it does not make it correct. Where two
[HARD] statements conflict, that is a finding for `STATE.md` §7 and a question — never a
silent choice between them.

---

## 6. Hard constraints digest

*Digest of `REQUIREMENTS.md`. On any doubt, re-read the source rather than trusting this.*

### Fixed by decree

| Slot | Value |
|---|---|
| System sample rate | 48 kHz, 32-bit slots, board-wide **[HARD]** |
| Master clock | single 24.576 MHz low-jitter XO → ADAU1466 MCLK; DSP PLL to 48 kHz core **[HARD]** |
| Clock distribution | XO → low-additive-jitter fanout buffer to ADC/DAC MCLK; **no daisy-chaining**, **no spread-spectrum anywhere in the audio clock tree** **[HARD]** |
| Foreign-rate isolation | BM83 and SPDIF paths both through on-chip ASRC — "no exceptions" **[HARD]** |
| SPDIF link mastering | **AK4118A is clock master on SDATA_IN2**; the DSP port is a clock consumer of that link only; recovered clock terminates at the ASRC boundary **[HARD, v0.2]** |
| Environment | **−20 °C…+70 °C. Not an AEC-Q board.** Industrial grade throughout the signal path; AEC-Q100 only where parts face the battery/harness — input protection, bucks, CAN PHY, remote-out driver |
| Output buffer | **OPA1656**, decided — no OPA1612 alternate. Filter values computed against it alone |
| Input attenuator | Divider **ahead of** the switch element; resistors **0.1 % matched or better** (BOM requirement, sets the CMRR spec) |
| ±13V5_A budget | 200 mA continuous, 250 mA peak, per rail |
| Channel↔slot map | AOUT1–6 = AK4458 #1 slots 1–6; AOUT7–12 = AK4458 #2 slots 1–6. Net names follow the **system** channel number, never the per-device slot |
| **Mute is the zero-energy state** | De-energised = muted, by construction **[HARD, v0.3]**. §7.2/§7.3 sequencing makes the *orderly* path quiet; §7.4 is the only thing that survives crank sag, a blown fuse or a pulled connector. Latching relays prohibited; enhancement-mode devices excluded by construction |
| Mute topology | **Series–shunt [HARD, v0.4].** Series = Form A photoMOS, energised-to-pass, open when unpowered. Shunt = depletion FET pair, **back-to-back source-to-source** (a single one rectifies), biased off from −13V5_A. Each fails safe in its own polarity; failed-state depth is the product. Fail-safe polarity is a property of the **topology**, not the device class — see ledger. ~60 mA continuous on +5V_D as a line item |
| Mute depth | Bounded by the amp's remote-mute latency, not indefinite — remote-out is fail-safe and drops first. V-16 models DAC residual × mute attenuation × amp gain × amp latency |
| Acceptance, HF | **CCIF twin-tone IMD ≤ 0.003 %**, 19 + 20 kHz at 2 Vrms, product at 1 kHz — *alongside* the 1 kHz THD line. This is the only criterion that can see nonlinear off-capacitance; both 1 kHz and 20 kHz THD are blind to it |
| Rail monitoring | **ADS1015-class I2C ADC on I2C0**, not the ESP32-S3 ADC. §9 dividers unchanged; −13V5 divider referenced to a positive rail |
| EMC posture | **FCC Part 15 Class B practices, no chamber test for v1. CISPR 25 out of scope.** Spread-spectrum **stays on** for the bucks — §3's prohibition covers the audio clock tree only. Input LC serves ISO 7637-2 and conducted emissions both; the RCA ground-field RC is an EMC component |
| TDM map | per §4 table, ports IN0–3 / OUT0–3 **[HARD]** |
| DAC split | 6+6 across two AK4458, slots 7–8 reserved on each **[HARD]** |
| Output level | ≥ 4.5 Vrms before clip into 10 kΩ **[HARD]** — drives the ±13V5_A rail |
| Output impedance | ≤ 100 Ω |
| Input impedance | ≥ 20 kΩ, line mode |
| Input ranges | line ≤ 2 Vrms; speaker ≤ 30 Vrms full-scale; switched by relay or analog switch under MCU control, **never jumpers** |
| Signal-sense threshold | ~10 mVrms nominal, resistor-settable |
| Power rails | VBATT_PROT, +5V_D, +3V3_D, +1V2_CORE, ±13V5_A, +5V_A, +3V3_A — names exactly as in §7.1 |
| Battery-facing regulators | AEC-Q100 |
| Transient immunity | ISO 7637-2 at the input **[HARD]** |
| Sequencing | §7.2 on / §7.3 off, both **[HARD]**; no audible pop is acceptance, not aspiration |
| Antenna keepouts | BM83SM1 and ESP32-S3-WROOM-1 module keepouts enforced **[HARD]**; separate the two 2.4 GHz antennas as far as geometry allows, do not stack |
| Net naming | §10 scheme, exactly; channel numbers match TDM slots with **no remapping** **[HARD]** |
| Grounding | single ground plane, analog/digital partitioned **by placement not splits**; chassis star-connect at the RCA ground field through an RC network; flag deviations |
| ±13V5_A noise budget | < 50 µVrms, 20 Hz–20 kHz, at the op-amp rails after LDO/filtering |
| USB pins | GPIO19/20 reserved for USB D± — do not assign elsewhere |
| DNP on v1 | WM8804, TJA1051T-Q1, 25AA1024 |

### Derived, not decreed — T2, see `STATE.md` §2

BCLK rates at 48 kHz / 32-bit: TDM8 = 12.288 MHz, TDM4 = 6.144 MHz, I2S = 3.072 MHz; MCLK = 512 fs.
No parallel memory bus anywhere on the board. Finest pitch is the 72-LQFP DSP at 0.5 mm if the
LQFP option is taken; **no BGA**, unless WLCSP is chosen instead.

### Still ⬜ UNSET — layout cannot start

| Slot | Value |
|---|---|
| Board outline / dimensions | ⬜ — *envelope only:* ≤ 200 × 140 mm assumed per §11 |
| Mounting holes and keepouts | ⬜ |
| Enclosure, height limits (top / bottom) | ⬜ |
| Layer count and stackup | ⬜ |
| Copper weight, surface finish | ⬜ |
| Fab house and capability limits (min trace/space, min drill, annular ring, via types) | ⬜ |
| Source of the shipped design rules / DRC severities (G2 baseline) | ⬜ |
| Controlled-impedance targets | ⬜ *proposed:* 75 Ω SPDIF coax, 90 Ω USB differential |
| Assembly sidedness | ⬜ |

---

## 7. Tooling

**KiCad 10.0.5** — all paths below verified 2026-08-15 (`STATE.md` T1-05…T1-08).

| What | Where |
|---|---|
| Install root | `C:\Program Files\KiCad\10.0\` |
| CLI | `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` — **NOT on PATH.** Always invoke by full path, always quoted |
| Bundled Python | `C:\Program Files\KiCad\10.0\bin\python.exe` — 3.11.5, `pcbnew` 10.0.5 imports clean |
| Stock libraries | `C:\Program Files\KiCad\10.0\share\kicad\` — 224 symbol, 155 footprint, 105 3D-model |

**The system Python does not have `pcbnew`.** Always call the bundled one by full path.

Verified subcommands: `pcb {drc,export,import,render,upgrade}` · `sch {erc,export,upgrade}`.
Both `drc` and `erc` accept `--severity-all`, `--severity-exclusions`, `--exit-code-violations`,
`--format json`; `pcb drc` also takes `--schematic-parity`, `--refill-zones`, `--save-board`.

**KiCad 10 postdates this assistant's training.** Its CLI flags and `pcbnew` API are **T2 from
memory and T1 only from `--help` or `dir()`.** Check the actual interface before scripting
against it; do not port KiCad 7/8/9 idioms on the assumption they survived. This applies with
most force to the `pcbnew` Python API, which has broken across major versions before.

- **Autorouter:** ⬜ UNSET — not needed until layout, and per the ledger, placement quality
  decides the outcome long before router choice does.
- **Units and grid policy: mm.** Decided, not assumed — KiCad is nm-internal and mm-native, every
  datasheet in this BOM is mm, and the only imperial dimension in `REQUIREMENTS.md` is the 0.1"
  test-header pitch, which is exactly 2.54 mm and lives inside a footprint where it belongs.
  Logged as `STATE.md` DL-09. All numbers written in any document carry an explicit unit; a bare
  number is a defect. Grid quantization rounds **outward** (see the ledger).
- **Designator and net naming convention:** **SET** — `REQUIREMENTS.md` §10, locked, [HARD] on
  the channel-to-slot mapping.
- **Library policy: SET** (DL-14). **Project-local, in-repo** symbol and footprint library — not a
  submodule; a submodule earns its pain only when a second board shares the library. Sourcing, in
  priority order:
  1. **Vendor-published footprint verbatim where one exists** — Microchip publishes the BM83SM1
     pattern; use it as issued, do not redraw it.
  2. **IPC-generated** for everything else. Boringly reliable for passives and SOICs.
  3. **Hand-built only as a last resort**, and the burden of proof is on it.

  **Verification is an adversarial pass, not a glance:** each footprint rasterised over the
  datasheet's land-pattern drawing and compared, logged per part in `STATE.md`. The operator
  personally eyeballs exactly five — **ADAU1466 LQFP, AK5574, AK4458, AK4118A, BM83SM1 keepout.**
  That is the respin set; the rest is passives and SOICs.

  Applies to symbols too, in a different currency: a wrong footprint is a respin, a wrong **pin
  number** on a symbol is a respin that ERC will not catch, because ERC checks electrical types
  against each other and cannot know the datasheet says pin 34 rather than pin 43. Pin maps are
  verified against the datasheet's **pin-function table, not the package drawing** — vendors have
  shipped datasheets where the two disagree, and the table is normative.

**Before any batch edit to the board file: take a copy.** It is a large s-expression file and a
bad write is not trivially undoable. Record the copy's path and SHA256 in `STATE.md` §0.

**The EDA GUI must not hold the board file open while it is edited outside the GUI.** The GUI
keeps an in-memory copy and writes it back wholesale on its next save, silently discarding
external edits — and the reverse, an external write under an open GUI, is invisible until the
operator saves over it. Before any scripted or manual edit, confirm with the operator that the
board is **closed** in the GUI. After the edit, the operator reopens it.

**Version control: git, initialised 2026-08-15** (DL-15). Library lives **in this repo**, not as a
submodule. `.gitignore` excludes KiCad backups/autosaves/lock files, generated output (`out/`,
`gerbers/`, `reports/`) and the `baseline/` safety copies — the baseline's path and SHA256 go in
`STATE.md` §0, the blobs stay out of history.

Generated output is not tracked because it is derivable; a **delivered** fab package is a
different thing and gets committed deliberately against a tag, so that what shipped can always be
reconstructed exactly.

---

## 8. Working rules

1. **Start of session:** read `STATE.md`.
2. **End of any meaningful step:** update `STATE.md` — promote/demote tiers, log decisions, log
   mistakes caught.
3. **A mistake caught is a permanent ledger entry**, not a fixed-and-forgotten event. Wrong
   belief, correction, and *the tell* that would have caught it sooner. Old mistakes returning is
   the failure mode these documents prevent.
4. **Do not report a gate closed on inference.** Run the check or ask for the glance.
5. **Ambiguity is a question, not a judgment call** — except for the five §11 delegated items,
   which are a documented decision.
6. **Prefer the mature tool over a hand-written one.** If a purpose-built tool exists for a
   problem, the burden of proof is on writing your own.
7. **Stop signals — when any of these appear, change approach rather than iterate:**
   - a metric that stays *constant* across iterations (it is not being worked on — the cause is
     in the fixed input)
   - an error count that *oscillates* rather than descends (the abstraction is wrong, not the
     implementation)
   - three consecutive fixes that each reveal a new bug of the same kind
8. **⬜ UNSET is checked before it is used, not after it fails.** Before any step, name which §6
   slots it depends on. If any are UNSET, the step does not run — ask instead.
9. **No pin, package, or electrical parameter enters the schematic from memory.** It comes from
   the datasheet, and the datasheet revision goes in `STATE.md` §1 next to the fact.
10. **A [VERIFY] resolved is a T1 promotion with a citation**, recorded in `STATE.md` §8 — not a
    mental note.
