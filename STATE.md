# STATE.md — ODSP-12 · `ODSP12-MB-A` rev A

Working scope, tiered fact base, open unknowns, findings, and the anti-drift ledger.
Governed by `CLAUDE.md` §5. **Read at session start. Update as work happens.**

Tiers: **T1** source of truth (verified) · **T2** highly probable (actionable, tagged) ·
**T3** likely (branchable, check quickly) · **T4** speculation (never drives work).

Last updated: 2026-08-15

---

## 0. Where we are

### RESUME HERE — read order after a context compaction

Everything needed to continue is **in the repo**; nothing load-bearing lives only in conversation.
Read in this order, then act:

| # | File | What it gives you |
|---|---|---|
| 1 | `CLAUDE.md` | The constitution. §0 UNSET rule, §4 channel policy, §5 evidence tiers, §8 working rules. **Non-negotiable.** |
| 2 | **`STATE.md` §0** (this section) | Current position, next action, session boundary |
| 3 | `STATE.md` §5 | **The ledger — read the method rules M1–M7a before doing any datasheet or file work.** They are why the mistakes below were caught |
| 4 | `REQUIREMENTS.md` **v1.2** | The authority. Cite by section **and** version |
| 5 | `hw/README.md` | Mechanical how-to: tool paths, build/verify commands, KiCad-10 format traps |
| 6 | `STATE.md` §7 / §8 / §9 | Findings register, [VERIFY] checklist, I2C bus map |
| 7 | `BRINGUP.md` | Sequence findings as bench checklist lines |
| 8 | `DATASHEETS.md` | 15 datasheets held locally in `datasheets/` (untracked); this is the register |

**Git is the memory of record — 21 commits, working tree clean.** Commit messages carry the
reasoning, not just the change; `git log` is a usable narrative of why things are as they are.

**Three habits that account for most of what went right**, all now in the ledger:
1. **Read datasheets by rendering the page** (`pdftoppm`), not by text extraction. Text extraction
   produced three wrong T1 facts here (T1-25, T1-28, and a permuted pin map).
2. **Verify the artefact, not the receipt.** ERC on an empty sheet is clean; a 200 response can be
   the wrong PDF. Check the netlist, the page content, the pin map.
3. **Run the recorded constraints against the artefact.** The `RT` error was caught because a
   *consequence* contradicted a written requirement — not by re-deriving anything (M7).



**Phase:** **Capture begun** (2026-08-15). Architecture specified at `REQUIREMENTS.md` v0.7,
governance closed, tooling verified. Mechanical and fabrication still unspecified — layout remains
blocked, capture does not.

**Board state:** KiCad project `hw/ODSP12-MB.kicad_pro` exists with a **10-page hierarchy**
(index + 9 sheets), all empty of components. **ERC: 0 violations.** PDF export renders 10 pages,
which is the proof KiCad *traverses* the hierarchy rather than merely parsing the root. Nothing
placed, nothing routed.

**`03_control.kicad_sch` is drawn** (page 4, 2026-08-16). 28 devices — ESP32-S3-WROOM-1-N8R2,
USB-C receptacle, USBLC6-2SC6 ESD array, reset/boot switches, status LED, and the strapping,
bulk, divider and pull-up networks. **100 global labels, no collisions** (the F41 guard ran).
**Cross-sheet integration is live**: `I2C0_SDA/SCL` now joins the ESP to the ADS1015 and TMP461,
and `PG_5V_D`/`PG_6V2_A`/`PG_1V2` join the bucks' open-drain PGOOD pins to their sense GPIOs.
**ERC 78 → 77**, and `pin_not_driven` fell 15 → 11 as the controller terminated four nets.

**Sheet plan** — mirrors the architecture, not the BOM, so that a [HARD] section maps to one sheet:

| Page | File | Contents |
|---|---|---|
| 1 | `ODSP12-MB.kicad_sch` | Index |
| 2 | `01_power.kicad_sch` | §7 rails, sequencing, monitor. **9 rails incl. +6V2_A and +3V3_CLK** |
| 3 | `02_dsp.kicad_sch` | ADAU1466, XO, MCLK fanout, PLL — the [HARD] §3 tree in one place |
| 4 | `03_control.kicad_sch` | ESP32-S3, USB-C, I2C0, GPIO |
| 5 | `04_bluetooth.kicad_sch` | BM83SM1 |
| 6 | `05_spdif.kicad_sch` | AK4118A, transformer-coupled coax, WM8804 DNP |
| 7 | `06_analog_in.kicad_sch` | 4× front end → AK5574 |
| 8 | `07_dac_a.kicad_sch` | AK4458 #1 + AOUT1-6 |
| 9 | `08_dac_b.kicad_sch` | AK4458 #2 + AOUT7-12 |
| 10 | `09_io.kicad_sch` | RCA field, power connector, test headers |

The 6+6 output split gets **two sheets rather than one instantiated twice** — §10's [HARD]
no-remapping rule wants the channel numbers written literally, not derived from an instance path.

**Tool-verified format facts:** native schematic version is **20260306** (from `sch upgrade`, not
memory — DL-13). Sheet UUIDs are `uuid5` from a fixed namespace, so regeneration is stable rather
than randomised.

**Gate status:** G0-S **open, and now blocked only on datasheets** — Blocks A–C and F closed
except Q2 (channel policy) and Q4 (board name/PN/rev), neither of which blocks drawing.
The §8 [VERIFY] checklist is the gate: **13 of 16 open, every one a datasheet read.**
G0-L **open** — blocked on Blocks D and E, unchanged.

**Symbol library** — `hw/lib/ODSP12.kicad_sym`. First symbol done:

| Symbol | Pins | Verification | Status |
|---|---|---|---|
| `ADAU1466` | 72 + EP, 3 units (Power / Serial Audio / Control) | Table 18 rendered pp.18-21 **and** Figure 11, independently read, 100% agreement (T1-37) | Ready for eyeball |
| `AK5574` | 48, 2 units (Analog / Digital) | Pin Functions pp.5-6 rendered and read (T1-47) | Ready for eyeball |
| `AK4458` | 48, 2 units (Analog / Digital) | Pin Functions pp.8-9 rendered and read (T1-47) | Ready for eyeball |
| `BM83SM1` | 50, 2 units (Power+Audio / Host+GPIO) | Table 2-2 pp.13-15 rendered and read (T1-56). **Names are the Host-mode function**; config-dependent pins carry `*` so the sheet shows which meanings depend on the flashed config (F32) | Ready for eyeball |

All four generated by `hw/lib/gen_symbols.py`, which **asserts every pin number appears exactly
once and that the set is exactly 1..N (+EP)** — the generator refuses to emit an incomplete symbol.
`kicad-cli sym upgrade` reports no change needed; all **9 units** export to SVG.
**The DL-14 eyeball set is complete — all four parts ready, reviewable as a batch.**

**Still open on the BM83:** V-12's keepout dimensions. Pages 54-55 are rendered but **not yet
read** — the antenna keepout, no-ground-under-antenna zone and mounting clearances come off the
mechanical drawing together, and they belong with the footprint rather than the symbol.

**Layer count: ≥ 4, decreed** (F25) — a floor from the silicon, not a routing estimate. 6 stays
live. This is the first Block E slot to close, and it closed from a datasheet rather than a fab
conversation.

**First sheet drawn: `02_dsp.kicad_sch`** (page 3). ADAU1466 as U1A/U1B/U1C, **all 73 pins
dispositioned — 60 nets + 13 explicit no-connects**, generator-asserted so an undispositioned pin
is a build failure rather than an oversight (F28 made mechanical). Net names per §10 [HARD].

**Verified by netlist, not by ERC** — see the ledger entry. `+1V2_CORE` reaches pins 20/35/53/71;
`GND` reaches all 13 ground-class pins including `VDRIVE` (T1-41) and the exposed pad; 54 nets
total.

**ERC is not clean, and should not be yet:** 38 `isolated_pin_label`, 11 `pin_not_driven`,
4 `power_pin_not_driven` — every one of them a label or pin whose counterpart lives on a sheet not
drawn yet. They retire as sheets fill. **G1b is not met and is not claimed.** Off-grid endpoints
were found and fixed; that one *was* a real defect.

**`01_power.kicad_sch` is drawn** (page 2). 14 devices — 3× LM61460-Q1, TPS62823, 5× LT3045,
ADS1015, TMP461, and the R2/R3/R4 PG→EN network — **every pin dispositioned**, 10 rail testpoints,
and the F34 divider arithmetic written on the sheet where a BOM cost-pass will trip over it.

**Cross-sheet integration is live and netlist-verified:** `+3V3_PLL` joins U9's output to the DSP's
`PVDD`; `DSP_THD_P`/`_M` join the TMP461's remote channel to the DSP's thermal diode;
`PG_3V3_D` → R4 → `EN_3V3_PLL` → U9 `EN/UV` is the complete F34 chain.

**Passive pass done — 69 devices, and ERC fell 118 → 82** as predicted: the rails are now *driven*
through their inductors, with feedback dividers closing each loop.

**Divider values computed from datasheet references, not assumed** (M2) and snapped to E96 —
LM61460 `VREF = 1.0 V`, LT3045 `ISET = 100 µA ±1 %`:

| Rail | Network | Actual | Err |
|---|---|---|---|
| +5V_D | Rt 40.2k / Rb 10k | 5.020 V | +0.40 % |
| +3V3_D | Rt 23.2k / Rb 10k | 3.320 V | +0.61 % |
| +6V2_A | Rt 52.3k / Rb 10k | 6.230 V | +0.48 % |
| +5V_A | Rset 49.9k | 4.990 V | −0.20 % |
| +3V3_A / _CLK / _PLL | Rset 33.2k | 3.320 V | +0.61 % |
| +3V6_BT | Rset 35.7k | 3.570 V | −0.83 % |

**Err column is E96-snap error only** — the full stack is snap + resistor ±1 % on both legs +
reference tolerance. Every rail here has a wide window and clears comfortably, but **the caveat
travels with the format** so a future tight-window rail reusing this table inherits it. +3V6_BT at
−0.83 % is the loosest fit and still holds ~28 % of its window as margin; it is recomputed for the
AP2127K-ADJ under V-23 anyway, where the FB reference tolerance joins the stack.

**Closed since:** **V-24** — TPS62823 `VFB = 0.6 V`, so +1V2_CORE takes equal legs, 100k/100k,
exactly 1.2 V; datasheet fetched into the archive (32 pp, Rev. C). **V-25** — LM61460 spread
deviation is **±2 %**, so at 2.2 MHz typ the worst-case instantaneous fundamental is
1.98 × 0.98 = **1.94 MHz, clear of the AM band's 1710 kHz top.** `RT = 5.76 kΩ` is **decided**,
and it is a datasheet point rather than an interpolation.

**Deliberate non-action, logged so it is not re-proposed:** the two battery-side bucks could be
synchronised via `EN/SYNC` to a common clock to avoid beat products. **Do not.** Beyond the pin and
net cost, the datasheet is explicit that *"a valid synchronization signal overrides spread
spectrum, turning it off"* — **syncing would disable the very mechanism that decorrelates them**,
and the beat between two spread carriers is itself spread. The non-action is now supported by the
part's own behaviour, not only by economy.

**±13V5_A is drawn** (F39, decreed and built 2026-08-16). Four devices — **U13** LM5156-Q1 SEPIC
→ +15V5_A, **U14** LM61460-Q1 as an inverting buck-boost → −15V5_A, **U15** LT3045 → +13V5_A,
**U16** LT3094 → −13V5_A — plus their passives. **116 devices on the sheet, every pin
dispositioned.** Two new symbols built from datasheet pin tables (LM5156-Q1, LT3094), library now
**9 symbols / 14 units**. Rail count 10 → 12; testpoints 10 → 14.

**Two defects found and fixed during the draw, both in already-committed work:**
- **F40** — every LT3045 carried `R_ILIM = 20 kΩ`, which programs a **7.5 mA** limit against
  rails budgeted 15–200 mA. All five analog rails would have current-limited into collapse.
- **F41** — growing the testpoint grid silently **shorted three net pairs** by landing global
  labels on identical coordinates. Every assertion passed; only the netlist showed it.

Both are now guarded: ILIM ties to GND per the datasheet, and a **`LABEL COLLISION` assertion**
(negative-tested) makes the second class a build failure rather than a discovery.

**VBATT_PROT is drawn** — F1 5 A fuse → D2 TVS → Q2 reverse P-FET (drain to battery, source to
load, so the body diode is forward in normal flow and blocks on reverse) → damped LC → VBATT_PROT.
**125 devices on the sheet.** All five published criteria are answered *on the sheet*, including
the Middlebrook inequality with values: undamped, the filter's peak output impedance is **47 Ω
against a −4.05 Ω load — violated by 21 dB**; with R<sub>d</sub> = 0.68 Ω and C<sub>d</sub> =
47 µF it is **0.69 Ω, a 15.4 dB margin**. **One criterion does not close: F42, escalated** — the
SMBJ24A misses the load-dump energy by 40–165×, and the board currently makes that scope claim
silently.

**THE POWER SHEET'S OPEN LIST IS EMPTY.** The three mechanical items ran 2026-08-16:

- **PWR_FLAG pass** — 9 flags on the nets whose source is a passive (every switcher rail formed
  after an inductor or diode, plus GND and the battery input). **`power_pin_not_driven` 8 → 0.**
  Flags were placed *only* where no active source exists; the LDO rails already carry a
  `power_out`, and flagging those would suppress a check still doing work. It surfaced one real
  modelling defect: `VDRIVE` was typed `output` while the datasheet directs grounding it, so an
  Output met the GND flag's Power output. **Retyped `passive`** — a pin the datasheet tells you
  to tie to a rail is a terminated node, not a driver. **`pin_to_pin` 1 → 0**, without an ERC
  exclusion, which §4 forbids anyway.
- **Saturation / DC-bias sweep** — every inductor **derived, snapped to E12, then re-derived at
  the snapped value**, because the ripple a 2.2 µH part gives is not the ripple a 1.98 µH
  calculation asked for. Emitting the raw number would have been **the 135 kΩ defect in another
  component class.** Results: +5V_D 10 µH · +3V3_D 1.8 µH · +6V2_A 15 µH · +1V2_CORE 2.2 µH ·
  IBB 15 µH · SEPIC 10 µH coupled. `Isat` quoted at 1.6× peak *operating* current with the gap
  to the converter's ~7 A fault limit **named as a choice, not left as an oversight**. The
  ceramic rule — rated ≥ 2× working, effective capacitance where a number is load-bearing — is
  on the sheet with its two live cases.
- **V-23 closed** — AP2127 **V<sub>REF</sub> = 0.8 V ±2 %**; 34.8 k / 10 k → **3.584 V**, inside
  `BAT_IN`'s 3.2–4.2 V across the full stack, with the datasheet-recommended feed-forward cap.
  **F36 closes with it**: the PROVISIONAL LT3045 is off the sheet and U10 is an AP2127K-ADJ.

**Still open on this sheet:** nothing. Remaining traps — **inductor saturation current** (the spec that matters, not RMS
heating; the 10 µH values on this sheet are **placeholders marked PROVISIONAL**, not derivations)
and **ceramic DC-bias derating** (sheet values must be *effective* capacitance at working voltage,
and the IBB's input caps span the full 31 V). **ERC 87**, in four enumerated classes:
50 `isolated_pin_label`, 15 `pin_not_driven`, 14 `label_dangling` — all counterparts on undrawn
sheets — plus **8 `power_pin_not_driven`, which are a real class needing a PWR_FLAG pass** before
G1b can close. **G1b remains unmet and unclaimed.**

### Open items at the boundary — the complete list

**Operator-owned (nothing else is):** none. Q2 and Q4 closed; no ⬜ UNSET remains in the
governance layer.

**Next action, prepared and waiting:** the **±13V5_A topology proposal** (assistant brings it,
operator dispositions against the four published criteria below).

**Open [VERIFY]s:** V-04 (AK5574 MCLK ratios, ADC side) · V-06 (OPA1656 output swing) ·
V-12 (BM83/WROOM-1 keepout *dimensions* — pages rendered, not yet read; belongs with footprints) ·
V-14/V-15/V-16 (mute part Ron/Coff + disorderly-transient measurement) · V-17 (AKM AVDD currents,
sizes +6V2_A) · V-18 (ADAU1466 core ripple tolerance) · V-23 (AP2127K-ADJ FB reference).

**Open findings:** F4 (impedance targets — layout) · F12 (output-stage gain vs noise budget) ·
F13 (ESP32-S3 GPIO map against the **module** datasheet, three specific checks logged) ·
F15 (MCLK/LRCK phase coherence) · **F37** (pin the SS-enabled LM61460 PN) ·
**F38** (the eight-line PN-pinning sweep, run once at first BOM emission).

**Undrawn:** sheets 03–09 (control, BT, SPDIF, analog in, both DAC/output sheets, IO) ·
±13V5_A and VBATT_PROT blocks on 01_power · all footprints · the whole PCB.

**Gates:** G0-S closed except datasheet residue · **G1b unmet and unclaimed** (ERC 80) ·
G0-L still blocked on Blocks D/E (mechanical + fab), which remain the largest unknown on the
project — **layer count has a floor of 4 (F25) but no outline, no stackup, no fab house.**

### Session boundary — deliberate, 2026-08-16 (second)

**Stopped before the ±13V5_A disposition, not partway through it.** `01_power` is drawn to the
passive pass and ERC sits at **80, falling for enumerated reasons**. Nothing is half-wired.

**The next move is a single delegated decision**, prepared and waiting: **±13V5_A topology
(SEPIC vs dual-boost)**, carrying its "designer's call" tag since v0.1. The operator has stated
the disposition criteria **in advance**, so the proposal is built against them rather than
defended after:

| # | Criterion |
|---|---|
| **a** | **<50 µVrms, 20 Hz–20 kHz** at the op-amp rails after LDO/filtering — with the LDO's **actual PSRR curve at the topology's switching frequency** doing the work. **The proposal must state f_sw**, because PSRR at 100 kHz and at 2 MHz differ by decades |
| **b** | **Asymmetric load reality** — the op-amp rails draw class-A-ish quiescent plus signal current, so **regulation under imbalance** matters more than total capacity |
| **c** | **Magnetics honesty** — SEPIC's coupled inductor vs dual-boost's two inductors plus an inverting stage is where the real BOM difference lives |
| **d** | **F38 applied at birth** — whatever controller is proposed, **PN pinned with options stated** |

*"If the proposal survives those four, it's decreed on arrival."*

Queued behind it: **VBATT_PROT** (ISO 7637-2 front end — reverse-FET, TVS, LC, with the gate
zener and standoff-vs-clamp arithmetic getting the on-sheet-inequality treatment, because load
dump is where nominally-fine boards die), **V-23** (AP2127K-ADJ divider), and the two remaining
traps — **inductor saturation current** and **ceramic DC-bias derating** — which land *with* those
blocks, not after them.

### Earlier session boundary — read this before reconstructing anything

**`01_power.kicad_sch` is deliberately undrawn.** It is **not** stopped partway through: the file
is the empty stub `gen_hier.py` created, no components were placed, and nothing is half-wired.
The stop was chosen, not hit.

~~**The first move is symbols, not the sheet**~~ — **done 2026-08-16.** `LM61460-Q1`,
`LMK1C1104` and `INA1650` are built and verified; the library now holds **7 symbols / 12 units**,
and **no part on the power sheet is missing a symbol.** F34's open [VERIFY] closed in the same
pass (T1-64: `PGOOD` is open-drain).

**The next move is `01_power` itself**, built to the three conventions below. Nothing else blocks
it: topology settled through F34, all ten rails sourced and budgeted, PG-to-EN resolved,
sequencing-as-nets on file. **F35 is an open observation, not a blocker** — it affects the clock
sheet, not this one.

**01_power's design is settled, and F34 gated it** — it changes the sheet's enable topology, so it was raised
before drawing rather than after. Three conventions are set for that sheet: **(1)** every rail
gets a testpoint with its §7.1 name silkscreened — one namespace across silk, schematic and
`BRINGUP.md`, so bring-up is a multimeter walking a checklist; **(2)** sequencing signals are
**nets, not annotations** — enables, rail-monitor dividers into the ADS1015, PDN/reset lines all
originate or terminate here, so §7.2/§7.3 and the sheet can be checked against each other
mechanically; **(3)** footprints for the +3V6_BT and +3V3_PLL LDOs accommodate the likely
alternates (SOT-23-5 / SOT-89 class) while their [VERIFY]s are open — free now, a respin later.

**Next action:** three findings await operator disposition, two of them respin- or [HARD]-class:
**F30** (AK5574 wake-up silences the whole I2C bus — §7.2 amendment), **F31** (BM83 supply rail:
`BAT_IN` is 3.2-4.2 V, not 5 V, and 3.3 V −5 % is below its minimum), **F32** (module ships in
Embedded mode; who flashes Host mode, and when). Then V-12 keepouts + footprints, then the first
sheet.

**Two confirmations folded in:** the output-stage **13.2 dB gain is now derived from verified
endpoints at both ends** — AK4458 full-scale measured 2.8 Vpp at AVDD 5 V (T1-11/T1-49) and the
4.5 Vrms [HARD] requirement — rather than assumed at either. And `VDD18` on both AKM parts is an
**internal-LDO output, not a supply input**: it wants an explicit *do-not-load* label per F28,
because a node with a capacitor and a voltage on it looks exactly like a rail to whoever probes it
next — V-04 ADC side + F15 phase
coherence, V-06 output swing, V-12 keepout dimensions via `pdftoppm`, V-17 (analog AVDD currents,
to size +6V2_A), and F13's module-datasheet pass. **One item is escalated and awaiting the
operator:** a third LT3045 dedicated to the MCLK fanout buffer (§7.1 note 6) — not fitted until
approved, per the new `CLAUDE.md` §4 rail-architecture rule.

**Governance is closed.** Q2 and Q4 both settled; no ⬜ UNSET remains in the constitution's
decision layer. The open set is purely technical.

**Zero-slack note for a future ODSP-16:** a third AK4458 has no address to live at — the
0b00100 prefix is full at four devices. I2C1 comes out of reserve at that point, not before.

**Datasheets:** 14 held and verified (`DATASHEETS.md`). ADAU1466 Rev. C and LT3045 Rev. D supplied
by the operator 2026-08-15; analog.com remains unreachable from here for anything further.

**Layout-blocked list gained an entry:** the ADAU1466's **5.3 mm exposed-pad via array** is now a
Block E stackup input (F17). Logged here so it is not rediscovered at fab-quote time. Its paste
aperture wants **windowed openings rather than one flood** and is called out in the DL-14
verification pass.

**Baseline safety copy:** none — nothing to copy yet. The first board file that lands here gets a
copy with its SHA256 recorded in this section **before** any edit.

**Standing risks:**

| Risk | Status |
|---|---|
| ~~Directory not under version control~~ | **Closed** — git initialised 2026-08-15, T1-D38 / DL-15 |
| No baseline copy exists yet | Open — vacuous until files arrive, then immediate. Note git now covers *history*, which is not the same thing as a pre-batch-edit restore point |
| `REQUIREMENTS.md` is v0.4 and still a baseline | Open — cite by section **and** version; a v0.5 supersedes and does not merge silently |
| KiCad 10 postdates the assistant's training | Open, permanent — CLI and `pcbnew` API are T2 from memory, T1 only from `--help`/`dir()`. See ledger |
| 4 findings open (§7): F4, F12, F13, F15 | Open |
| Mute topology decided (series–shunt, DL-19); parts not yet chosen | Open — V-14/V-15. Much lower risk than at v0.3: two lax requirements on two cheap parts rather than one constrained optimisation |
| **Only the operator can close Q2** (channel policy) | Open — owed next round. Does not block drawing |
| **F17 — ADAU1466 may have no LQFP option** | Open, T2 — if it is LFCSP-only, §2's hand-rework rationale fails and a thermal-via requirement enters the stackup. Settles at V-01 |
| analog.com unreachable (T1-15) | Open — needs a manual download; blocks V-01 and therefore the first sheet |

---

## 1. T1 — Source of truth

Each entry names **how it was verified**. Nothing enters on reasoning alone.

| ID | Fact | Verified by |
|---|---|---|
| T1-01 | Project directory contained no files before this document set | directory listing, 2026-08-15 |
| T1-02 | The directory is not a git repository | environment report + `git rev-parse`, 2026-08-15 |
| T1-03 | Constitution derives from the template at `C:\Users\nick\.claude\templates\pcb-project\` | both template files read in full, 2026-08-15 |
| T1-04 | `REQUIREMENTS.md` reproduces the operator's v0.1 text with formatting normalised only; v0.2 changes are each traceable to an operator disposition in its revision history | transcribed and re-read, 2026-08-15 |
| T1-05 | KiCad **10.0.5** installed at `C:\Program Files\KiCad\10.0\` | `kicad-cli --version`, 2026-08-15 |
| T1-06 | `kicad-cli.exe` is at `...\10.0\bin\` and is **not on PATH** | `Get-Command kicad-cli` → not found; direct invocation at full path succeeded |
| T1-07 | Bundled Python 3.11.5 at `...\10.0\bin\python.exe`; `pcbnew` 10.0.5 imports | `python.exe -c "import pcbnew; pcbnew.GetBuildVersion()"` |
| T1-08 | `pcb drc` and `sch erc` both support `--severity-exclusions`, `--exit-code-violations`, `--format json`; `pcb drc` also `--schematic-parity` | `kicad-cli pcb drc --help`, `sch erc --help` |
| T1-09 | Stock libraries present: 224 symbol, 155 footprint, 105 3D-model | directory count under `share\kicad\` |
| T1-10 | **AK4118A has no internal SRC** — PLL clock recovery only; rate conversion was never on that die | Operator confirmation, 2026-08-15. Closes V-02 and is the basis of the F1 disposition |
| T1-11 | **AK4458 full-scale output = 2.8 Vpp differential** at (VREFH−VREFL) = 5 V, per DAC channel | `AK4458_AKM.pdf` (90 pp, official AKM), 2026-08-15. Closes V-05 |
| T1-12 | **INA1650 is dual-channel**; INA1651 is the single-channel sibling | `INA1650_TI.pdf` p.1 (official TI), 2026-08-15. Closes V-11 and re-grounds T1-D27 on the manufacturer document |
| T1-13 | 12 manufacturer datasheets held locally in `datasheets/`, each verified by page count and first-page content after download; register in `DATASHEETS.md` | Retrieval + `pdfinfo`/`pdftotext` verification, 2026-08-15 |
| T1-14 | poppler 25.07.0 installed (winget, user scope), on user PATH; provides `pdftotext`, `pdfinfo`, `pdftoppm` | `winget install`, binaries exercised on the archive, 2026-08-15 |
| T1-26 | **AK4458 MCLK ratio at 48 kHz: 512fs or 768fs** (30-54 kHz band). Our 24.576 MHz XO is exactly **512fs at 48 kHz** — compatible. "In PCM mode, master clock is divided automatically by fs rate auto detection" | `AK4458_AKM.pdf`. Closes V-04 for the DAC side |
| T1-27 | **All four AKM parts select I2C vs 3-wire serial by pin strap.** AK4458: I2C mode requires `I2C` pin = H **and `PS` pin = L** (PS = H gives *parallel* mode). AK5574: `I2C` pin = H selects I2C (L selects 3-wire). AK4118A: `IIC` pin = H selects I2C | The three AKM datasheets. **Closes V-09** |
| ~~T1-28~~ | ~~AK4118A has C1 fixed at 0, leaving two addresses~~ — **WRONG, RETRACTED 2026-08-15.** That clause belongs to the AK4118A's **4-wire serial mode (IIC pin = "L")**, not I2C. Superseded by T1-32 | Retracted after a figure-level read; see ledger |
| T1-32 | **All three AKM families share one 7-bit slave-address space: `0b00100` + CAD1 + CAD0 = 0x10, 0x11, 0x12, 0x13.** Identical for AK5574, AK4458 and AK4118A in I2C mode; each device can be strapped to any of the four | Rendered figure reads: AK4458 Fig. 73 (p.70), AK5574 Fig. 63 (p.57), AK4118A Fig. 38 (p.38) + §(2)-1-4 verbatim. **Closes F23** |
| T1-33 | **AK5574 3-wire serial has a drive-conflict hazard:** "The I2C interface block continues to run, even when the 3-wire serial interface is selected." A CDTI(SDA) H→L while CCLK(SCL) is H reads as a START; if the following bits match the slave address the I2C block drives ACK onto the shared pin, conflicting with the 3-wire input, and "the data cannot be reliably written". Mitigation: change CDTI only on the CCLK falling edge | `AK5574_AKM.pdf` p.57. **Independent support for rejecting the SPI escape hatch** |
| T1-29 | **OPA1656 quiescent current = 3.9 mA per channel**, 100 mA output drive | `OPA1656_TI.pdf`. Confirms the ~96 mA figure in the T1-D30 rail budget (24 × 3.9 = 93.6 mA) |
| T1-30 | **LMK1C110x supply is 3.3 V / 2.5 V / 1.8 V — it is not a 5 V part.** Additive jitter 7.5 fs typ specified at VDD = 3.3 V | `LMK1C1104_TI.pdf`. Drives F22 |
| T1-31 | **Both modules mandate an antenna keepout.** BM83: "Figure 7-4. Recommended Keep-out Area for PCB Antenna" — "No copper, No component" and no ground plane under the antenna on the host PCB. ESP32-S3-WROOM-1 has an antenna keepout zone; **the -1U variant does not, because it uses an external antenna** | `BM83_Microchip.pdf`, `ESP32-S3-WROOM-1_Espressif.pdf`. **V-12 partially closed** — existence and mandate confirmed; exact dimensions live in figures and need a `pdftoppm` render |
| T1-16 | **ADAU1462/ADAU1466 ship in ONE package: 72-lead LFCSP, `CP-72-6`, 10 x 10 mm, 5.3 mm exposed pad.** The ordering guide lists six orderable models and every one is LFCSP. **There is no LQFP and no WLCSP.** Temp range -40 C to +105 C | `adau1462-1466.pdf` Rev. C p.202 ordering guide + p.1 features. **Closes V-01 (package), confirms F17** |
| T1-17 | **4 serial input ports, 4 serial output ports.** Up to **8 stereo ASRCs**, ratio 1:8 to 7.75:1, 139 dB dynamic range, THD+N -120 dB, I/O sample rate 6-192 kHz | Rev. C p.1 features + spec tables. Closes V-01 (ports/ASRC); `REQUIREMENTS.md` §2/§4 confirmed correct |
| T1-18 | **Serial ports are independently master/slave, per port.** `SERIAL_BYTE_x_0` at 0xF200 / 0xF204 / 0xF208 / 0xF20C (SDATA_IN0…IN3), Bit 9 `LRCLK_MODE`, Bit 8 `BCLK_MODE`. Pin descriptions state per port that "Serial Input Port *n* is a master or slave" | Rev. C register map + pin table. **Closes V-13 — the F1 disposition is confirmed against the document** |
| T1-19 | **SPI slave-port max SCLK = 20 MHz**, read and write (`fSCLKWRITE`, `fSCLKREAD`) | Rev. C timing specs. **Closes V-07** — the 10 MHz target has 2x margin |
| T1-20 | **DVDD = 1.2 V ±5% (1.14-1.26 V). ADAU1466 core current: 213 mA minimal program, 220 mA typical, 233 mA typ / 495 mA max for maximum program.** The typical figure is measured with 16-channel I/O, 10-band EQ per channel, all ASRCs active. IOVDD current 53 mA at 3.3 V with all serial ports as clock masters | Rev. C Tables 2/3. **Closes V-08** |
| T1-21 | **The on-chip 1.2 V regulator is a controller, not a self-contained LDO** — pin 3 `VDRIVE` is a "PNP Bipolar Junction Transistor-Base Drive Bias Pin for the Digital Supply Regulator"; DVDD is derived from IOVDD "in combination with an external pass transistor", up to an 800 mA load | Rev. C pin table + regulator spec |
| T1-22 | **Supply sequence depends on the DVDD method.** Internal regulator: DVDD comes up **after** AVDD, IOVDD and PVDD. DVDD supplied directly: **"no special sequence is required"** | Rev. C power supplies section |
| T1-23 | **The control port is dead while the PLL locks.** "While the PLL is attempting to lock, the I2C slave and SPI slave control ports are inactive… all attempts to write to the control port fail." Max lock 10.666 ms at 48 kHz (3.072 MHz post-prescaler); typically ~3.5 ms. Poll `PLL_LOCK` at 0xF004 Bit 0 | Rev. C power-up / PLL section |
| T1-24 | **Firmware contract, first pass:** PLL registers 0xF000 `PLL_CTRL0`, 0xF001 `PLL_CTRL1`, 0xF002 `PLL_CLK_SRC`, 0xF003 `PLL_ENABLE`, 0xF004 `PLL_LOCK`. Output routing `SOUT_SOURCEx` at 0xF180-0xF197. Software safeload via `num_SafeLoad_Lower` / `num_SafeLoad_Upper`, 1-5 parameters per transaction, page-split addressing | Rev. C register map + Software Safeload section |
| ~~T1-25~~ | ~~SELFBOOT pin 34: floating -> SPI self-boot, 10 kOhm pull-down -> I2C self-boot~~ — **PARTIALLY WRONG, corrected 2026-08-16.** The protocol-select behaviour belongs to **pin 26**, not pin 34. Superseded by T1-34/T1-35 | Text-extraction error across table rows; caught by the figure-level read |
| T1-34 | **Pin 34 `SELFBOOT`: internal pull-up.** Logic high (IOVDD) initiates self boot on the **next rising edge of `RESET`**; tied to ground = no self boot. May be strapped directly or through a >=1.0 kOhm resistor | Table 18 p.20, rendered. **F21's disposition is confirmed** — floating means high means self-boot from a DNP EEPROM |
| T1-35 | **Pin 26 `SS_M/MP0` selects the self-boot *protocol*** — internal 250 kOhm pull-up; when SELFBOOT is high at the RESET rising edge, **floating = SPI, 10 kOhm pull-down to DGND = I2C**. Irrelevant while SELFBOOT is grounded, but it is a second strap that must be deliberate if self-boot is ever stuffed | Table 18 p.19, rendered |
| T1-36 | **Pin 24 `RESET` is active low with an internal pull-DOWN** — the part is held in reset by default at power-up and must be *actively released*. Triggers on high->low, exits on low->high | Table 18 p.19. Confirms the §7.2 step-3 model is safe by default |
| T1-37 | **Complete ADAU1466 pin map verified: all 72 pins + exposed pad.** Table 18 (pp. 18-21, normative per T1-D45) rendered at 170 dpi and read, cross-checked against Figure 11 (p.18). **100% agreement, zero discrepancies** | Figure-level render of four pages + independent diagram read. This is the M2 method record for the symbol |
| T1-38 | **Exposed pad is ground and thermally mandatory:** soldered to a copper square of equivalent size, "**identical copper squares must exist on all layers** of the board, connected by vias, and they must be connected to a **dedicated copper ground layer within the PCB**" | Table 18 p.21 + Figure 11 note. Drives **F25** |
| T1-39 | **The ADAU1466 has an integrated S/PDIF receiver AND transmitter** — pin 4 `SPDIFIN` ("Input to the Integrated Sony/Philips Digital Interconnect Format Receiver"), pin 5 `SPDIFOUT`. Both internally biased to IOVDD/2 | Table 18 p.18. Drives **F26** |
| T1-40 | **Pins 63/64 `THD_M`/`THD_P` are a thermal diode**, intended for "the D- / D+ pin of an external temperature sensor IC" — a *remote-diode* sensor, not a local one | Table 18 p.21. Drives **F27** |
| T1-68 | **LMK1C1104 `1G` has an internal 300 kOhm pull-DOWN and "switches the outputs into a low state when 1G is low"** — so **left floating, the entire clock fanout is disabled** and no MCLK reaches any converter. Must be actively pulled/driven high. **`Y3` unused: "Unused outputs can be left floating"** — the datasheet's own guidance | TI SNAS791D pp.3, 7. Textbook F21: floating is a state someone chose, and here it chose *off*. Failure presents as "the converters don't work" |
| T1-69 | **MIC5504 is fixed-output only** — 1.2 / 1.8 / 2.5 / 2.8 / 3.3 V, **no 3.6 V variant** | Stock `Regulator_Linear.kicad_sym` enumeration. Drives **F36** |
| T1-70 | **Stock symbol pin maps, read as name+number pairs from single matches:** `TPS62823DLC` 8 pins (4 = `NC`); `LT3045xDD` **11** pins (2 = second `IN`, 11 = second `GND`); `ADS1015IDGS` 10; `TMP461xxRUN` 10 | Direct extraction. **Supersedes an earlier zipped-regex map that was permuted** — see ledger |
| T1-64 | **LM61460-Q1 `PGOOD` (pin 5) is open-drain** — *"Pull this pin up to a suitable voltage supply through a current limiting resistor. High = power OK, low = fault. PGOOD goes low when EN = low, VIN > 1 V."* | TI SNVSB70F Table 7-1 p.4, rendered. **Closes F34's open [VERIFY]** |
| T1-65 | **LM61460-Q1 pins that must not float: `FB` (4), `RT` (6), `EN/SYNC` (7).** `RT` additionally must not be grounded — it needs 5.76-66.5 kOhm to set 200-2200 kHz. `VCC` (2) is an internal-LDO output: **"do not connect to any external loads"** | Same table. F28 dispositions required for all four |
| T1-66 | **LMK1C1104 is 8-pin TSSOP with FOUR outputs** — `Y0` (3), `Y1` (8), `Y2` (5), `Y3` (7); `CLKIN` (1), `1G` output-enable (2), `VDD` (6), `GND` (4) | TI SNAS791D Figure 6-4 p.3. Drives **F35** |
| T1-67 | **INA1650 is 14-pin TSSOP**; `REF A` (12) and `REF B` (9) **"must be driven from a low impedance"** — not left to a divider. `VMID_IN` (11) takes a noise-reduction capacitor; `VMID_OUT` (10) is the buffered supply-divider output | TI SBOS818B p.3, rendered |
| T1-61 | **V-22, end-to-end read of Power Supplies / Voltage Regulator / Hardware Reset (pp.33-34). No third ordering constraint exists** — IOVDD-first (T1-59) is the only one. But **two mandatory-supply rules** that are easy to optimise away: **`AVDD` "must be supplied even if the auxiliary ADCs are not in use"** and **`PVDD` "must be supplied even if the PLL is not in use"**. Table 23 externally-supplied: IOVDD **yes**, DVDD **optional**, AVDD **yes**, PVDD **yes** | Rev. C pp.33-34, rendered. **Closes V-22** — the section is now read exhaustively, not sampled |
| T1-62 | **`VDRIVE` grounded still draws ~100 µA from IOVDD**, and the internal regulator has **no control registers**. ADI also states *"do not use the regulator to provide a voltage supply to external ICs"* — not applicable here, DVDD is external | Rev. C p.33. Completes T1-41 |
| T1-63 | **`RESET` wants an external pull-down of several kΩ** *"to guarantee that the device is held in reset in the event that the reset supervisory [circuit fails]"* — in addition to the internal pull-down (T1-36). Also: **RAM is not guaranteed cleared by a reset; the DSP program must clear it manually** | Rev. C p.34. Second half is a firmware-contract item |
| T1-58 | **ADAU1466 `PVDD` current: 8.3 / 10.1 / 12.9 mA (25 °C), 15 mA max over temperature.** PVDD range 2.97-3.63 V; absolute max 0-4.0 V | Rev. C Tables 2/3. **Closes V-21** — settles the F33 LDO as a small part, ~44 mW |
| T1-59 | **ADAU1466 supply ordering [HARD]:** all power pins may be applied simultaneously; if not, **`IOVDD` must be first** because it references the internal ESD protection diodes. `AVDD`, `DVDD`, `PVDD` may follow in any order but **must not precede IOVDD** | Rev. C Power-Up Sequence, p.24. Drives **F34** |
| T1-60 | **Stock KiCad 10 already carries LT3045, TPS62823, MIC5504, ADS1015, TMP461, OPA1656 and ESP32-S3-WROOM-1.** Absent and needing project symbols: LM61460-Q1, LMK1C1104, INA1650 | `grep` over `share/kicad/symbols`. **DL-14's stock-first rule pays off** — 7 of 10 power-sheet parts need no symbol work |
| T1-54 | **AK5574 `OVF` is a summary flag, not per-channel.** "The OVF pin outputs 'H' if **one of AIN1-4** channel overflows (**more than -0.3 dBFS**)… returns to 'L' when overflows are resolved. The OVF output has the **same group delay as the ADC**." No per-channel overflow register found in the overflow sections | AK5574 pp.51 + notes. Shapes the F29 disposition |
| T1-55 | **AK5574 wake-up blocks the whole I2C bus, not just itself.** After `PDN` release the internal PDN clears only after 16384 internal-oscillator cycles (**max 10 ms**); register writes are unavailable until then. **"During this period, digital output and digital in/output pins may output an instantaneous pulse… therefore, referring the output of digital pins and data transmission with a device on the same 3-wire serial/I2C bus as the AK5574 should be avoided in this period to prevent system errors."** Initialisation completes in 583/fs (12.1 ms at 48 kHz) | AK5574 timing notes, rendered. Drives **F30** |
| T1-56 | **BM83SM1 has 50 pins.** `BAT_IN` (23) is the main supply at **3.2-4.2 V**; `ADAP_IN` (22) is a **5 V** adapter/charger input, "otherwise it can be left floating". `SYS_PWR` (24) and `VDD_IO` (25) are **internal-use, do-not-connect** (SYS_PWR may feed LED1/LED2 only). I2S: `MCLK1` (5) is **output-only**; `SCLK1` (3) and `RFS1` (2) are I/O, so the module can be I2S master or slave | BM83 Table 2-2, pp.13-15, rendered. Drives **F31** |
| T1-57 | **The BM83 ships pre-configured in Embedded mode**, and pin functions are config-dependent: *"The BM83 module is pre-configured with Embedded mode… The GPIOs mentioned in the preceding table can be configured using the Config Tool or the SDK."* Pin 49 shows the split explicitly — external codec reset (Embedded) vs `UART_TX_IND` host wake (Host). Pin 31 `P3_4/UART_RTS` is additionally a **system configuration pin (Application vs Test mode)** | BM83 p.15 note + Table 2-2. Drives **F32** |
| T1-47 | **AK5574 and AK4458 pin maps verified, 48 pins each.** AK5574 "Pin Functions" pp.5-6; AK4458 pp.8-9 | Figure-level render at 175 dpi and read. M2 method record for both symbols |
| T1-48 | **Neither AKM part needs a 1.8 V rail.** Both have `LDOE`: **H = internal LDO enabled**, and `VDD18` then becomes an output/stabilisation node (AK4458: 1.0 uF to DVSS; AK5574: stabilisation cap). AK5574 TVDD is 1.7-1.98 V when LDOE=L but **3.0-3.6 V when LDOE=H** | AK5574 p.5 pin 17/19/45; AK4458 p.9 pin 44/47 + Note 4. **Confirms §7.1 needs no 1.8 V entry** |
| T1-49 | **Supply rails: AK5574 AVDD 4.75-5.25 V; AK4458 AVDD 3.0-5.5 V; both TVDD 3.0-3.6 V.** AK4458 VREFH/VREFL are per channel-pair and tie to AVDD/AVSS | AK5574 p.5; AK4458 p.9. **At AVDD = 5 V the T1-11 full-scale formula gives exactly 2.8 Vpp** — the 13.2 dB gain figure stands |
| T1-50 | **I2C-mode straps, complete:** AK5574 `I2C` (42) = H **and `PSN` (41) = L**; AK4458 `I2C` (17) = H **and `PS` (16) = L**. On both, the second pin high selects **parallel** mode. Addresses: AK5574 `CAD0_I2C` (32) / `CAD1` (34); AK4458 `CAD0_I2C` (15) / `CAD1` (12) | Both pin tables, rendered. **Refines T1-27** — the AK5574's PSN requirement was not previously recorded |
| T1-51 | **AK5574 `MSN` (24) is a hardware master/slave select**, and `TEST` (15) has a 100 kOhm internal pull-down. `PDN` (20): L = reset/power-down. AK4458 `PDN` (48): L = power-down, registers reset to default | Both pin tables |
| T1-52 | **AK4458 "Handling of Unused Pin" is explicit and counter-intuitive:** unused analog outputs (`AOUTL/Rn P/N`) **must be OPEN**; `DZF` must be open; unused `SDTI1-4`, `DSDR3`, `DSDL4`, `DSDR4` **must be connected to DVSS** | AK4458 p.9. **Directly binding on this design** — T1-D08 reserves slots 7-8 on each DAC, so the AOUT4 pairs are unused and **must be left open, not grounded** |
| T1-53 | **AK5574 pin 30 `OVF` is an analog-input overflow flag output** | AK5574 p.5. Drives **F29** |
| T1-42 | **ADAU1466 S/PDIF receiver lock range: 18 kHz to 192 kHz.** Clock recovery is "completely digital". Ports designed to meet AES/EBU jitter of 0.25 UI p-p at ≥8 kHz and 10 UI p-p below 200 Hz | `adau1462-1466.pdf` pp. 74-75, rendered. Closes V-19 condition 1 |
| T1-43 | **Integrated S/PDIF RX is ASRC-coupled on-die:** "because the S/PDIF input data is most likely asynchronous to the DSP core, **it must be routed through an ASRC**". No serial port and no external recovered-clock net involved. 16 ASRC channels in 8 stereo sets; we need 2 | p.74, rendered. Closes V-19 condition 2 |
| T1-44 | **Pins 4/5 are dedicated `SPDIFIN`/`SPDIFOUT`** with no alternate/multipurpose functions and no current assignment — no conflict. RX input is a comparator centred at IOVDD/2 requiring **≥200 mV p-p**, accepting TTL or bipolar, and **requiring an AC coupling capacitor on the pin** | Table 18 + p.74. Closes V-19 condition 3 |
| T1-45 | **Integrated S/PDIF TX outputs two channels directly from the core at core rate** and **consumes no serial output port**; non-audio bits copyable from the RX or programmed. Auxiliary Output Mode (metadata onto TDM8) exists but is optional and unused. Interface meets **consumer** S/PDIF, **not AES3 professional** | p.75, rendered. Retires the WM8804 stuffing option |
| T1-46 | **S/PDIF status registers:** `SPDIF_LOCK_DET` 0xF600, `SPDIF_RX_CTRL` 0xF601, `SPDIF_RESTART` 0xF604, `SPDIF_LOSS_OF_LOCK` 0xF605, plus channel-status / user-data / validity / parity blocks 0xF610-0xF68B. `ASRC_LOCK` 0xF580, `ASRC_MUTE` 0xF581, per-ASRC ratio 0xF582-0xF589 | p.74-75. Makes §12's SPDIF-lock criterion a register poll (M3) |
| T1-41 | **Pin 3 `VDRIVE` disposition is explicit:** "If an external supply is provided directly to DVDD, **connect the VDRIVE pin to ground**." Recommended PNP, if ever used, is ON Semi NSS1C300ET4G | Table 18 p.18. **Closes the F18 loose end** — VDRIVE goes to GND, not left floating |
| T1-15 | **analog.com is unreachable from this environment** — ADAU1466 and LT3045 PDFs and the HTML product page all timed out via `Invoke-WebRequest`, `curl` and `WebFetch`; Verical 403 | Four independent fetch attempts, 2026-08-15 |
| T1-71 | **LT3045 PSRR vs input-to-output differential, the criterion-(a) number.** At **2 V headroom: 100 kHz ≈ 77 dB, 500 kHz ≈ 72 dB, 1 MHz ≈ 70 dB, 2 MHz ≈ 84 dB.** At 1.5 V: 74 / 63 / 62 / 84 dB. **The curve has a notch at 500 kHz–1 MHz and recovers by 2 MHz** — the part is *better* at 2 MHz than at half that. Below ~1 V headroom every curve collapses | Curve G45 p.10 cropped to 400 dpi and read, `LT3045.pdf` Rev. D. Conditions on the figure: I<sub>L</sub> = 500 mA, R<sub>SET</sub> 30.1k, C<sub>OUT</sub> 10 µF, C<sub>SET</sub> 0.47 µF |
| T1-72 | **LT3045 audio-band PSRR and noise.** G41: with C<sub>SET</sub> = 4.7 µF, PSRR ≈ 98 dB at 10 Hz, peaks ~117 dB near 200 Hz, ~110 dB at 1 kHz, still ≈ 80 dB at 200 kHz. G46/G48: **integrated output noise is 0.8 µV<sub>RMS</sub> (10 Hz–100 kHz), flat across 0–500 mA load and flat across output voltage to 15 V** | Curves G41 p.9, G46/G48 p.10, rendered at 175 dpi |
| T1-73 | **LT3045's output side is a 16 V part.** Abs max **OUT, OUTS and SET pins = −0.3 V / 16 V**; electricals specified over **0 V < V<sub>OUT</sub> < 15 V**. IN pin ±22 V. Dropout **260 mV typ at 500 mA**. θ<sub>JA</sub> = 33 °C/W (DFN-12) | `LT3045.pdf` Rev. D abs-max block + electrical table. **At 13.5 V this is the closest to a ceiling any LT3045 on this board runs** — the other five sit at 3.3–5 V |
| T1-74 | **LM61460-Q1 abs max V<sub>IN</sub> = 42 V; recommended operating 3–36 V.** Also abs max: BIAS 16 V, FB 16 V, PGOOD 20 V, PGND-to-AGND ±0.3 V DC. Output range for the adjustable version **1 V to 0.95 × V<sub>IN</sub>**; f<sub>SW</sub> 200–2200 kHz | `LM61460-Q1_TI.pdf` §8.1/§8.3. **Decides F39** — an inverting buck-boost stresses the IC at V<sub>IN</sub> + \|V<sub>OUT</sub>\|, so this rail cannot sit on VBATT_PROT |
| T1-75 | **LM5156-Q1: 3.5–60 V operating, 65 V abs max, AEC-Q100 grade 1, WSON-12 3×2 mm, external FET.** V<sub>REF</sub> = **1.000 V ±1 %** — the same reference as the LM61460, so the divider helper is reused unchanged. RT = 9.09 kΩ → **2200 kHz (1980 min / 2420 max)**; RT = 220 kΩ → 100 kHz. t<sub>ON(MIN)</sub> = 50 ns at 2.2 MHz; D<sub>MAX</sub> = 80 % min / 85 % typ | `LM5156-Q1_TI.pdf` SNVSBI7B Rev. B, features + electrical table |
| T1-76 | **LM5156-Q1 dual random spread spectrum: triangular modulation runs at 0.156 × f<sub>SW</sub>**, and *"the frequency of the triangular modulation is further modulated randomly **to reduce the likelihood of any audible tones**."* Selectable live via `DITHOFF` — grounded enables dither, tied to VCC disables it | §9.3.5 + Figure 9-10. **The deviation percentage is not specified anywhere in the datasheet** — see V-26 |
| T1-77 | **TI states the boost pass-through problem in its own words:** *"Boost converters have a natural pass-through path from the supply to the load through the high-side power diode (D1). Because of this path and the minimum on-time limitation of the device, boost converters cannot provide current limit protection when the output voltage is close to or less than the input supply voltage."* | `LM5156-Q1_TI.pdf` §9.3.8. **This is the citation under F39's rejection of a plain boost** — not our inference |
| T1-78 | **The eliminated candidates, each by a number in its own datasheet.** LM5155-Q1: 45 V operating / 50 V transient. LM5157-Q1: **integrated 50 V** switch. TPS55340-Q1: 2.9–38 V in, **40 V** switch, f<sub>SW</sub> to 2.5 MHz. LM5175-Q1 (4-switch buck-boost, one plain inductor): **operating frequency range 100–600 kHz, full stop** | The four datasheets, now held. LM5175's range lands squarely in T1-71's PSRR notch |
| T1-93 | **TPS62823 f<sub>SW</sub> = 2.2 MHz typ**, and *"as the load current decreases, the converter enters PSM, reducing the switching frequency."* | `TPS62823_TI.pdf` Rev. C §8.5 + §9.3. Aligns +1V2_CORE with the other four stages, **and the PSM note is a named instance of V-27's pulse-skip class — this part documents that it skips, where the LM5156/LM61460 only say they can** |
| T1-94 | **ESP32-S3-WROOM-1 module pin table, all 41 pins extracted** — 1/40 GND, 2 3V3, 3 EN, 41 EPAD(GND), and IO4/5/6/7/15/16/17/18/8/19/20/3/46/9/10/11/12/13/14/21/47/48/45/0/35/36/37/38/39/40/41/42/RXD0(44)/TXD0(43)/2/1 on pins 4–39. **The stock `RF_Module:ESP32-S3-WROOM-1` symbol is self-contained (no extends), 41 pins, and matches** — its pins 13/14 are named `USB_D-`/`USB_D+`, i.e. the [HARD] reservation is pre-encoded | Datasheet Table 3 pp.10–12, parsed as rows and spot-checked against the symbol. Five rows needed a second pass (line-wrapped) — **recovered rather than assumed**, which is the whole point of counting them |
| T1-95 | **F13(a) CLOSES: IO35/36/37 are free on the N8R2.** *"For modules with Octal SPI PSRAM, i.e. modules embedded with ESP32-S3R8 or ESP32-S3R16V, pins IO35, IO36 and IO37 are connected to the Octal SPI PSRAM and are not available for other uses."* **N8R2 is quad PSRAM**, so the reservation does not apply | Datasheet p.12 footnote b. **This is the F38 pinned-PN rule with teeth** — three power-good sense lines now sit on those pins, so an R8/R16V substitution shorts them into the PSRAM bus |
| T1-96 | **Strapping-pin defaults, Table 4-1:** GPIO0 **weak pull-up (1)** · GPIO3 **FLOATING (no default)** · GPIO45 weak pull-down (0) · GPIO46 weak pull-down (0). Strapping set: **GPIO0, GPIO3, GPIO45, GPIO46**; latched at reset and unchangeable until power-down | Datasheet §4 + Table 4-1. **GPIO3 is the one with no internal default at all**, so it is the one that cannot be left to chance |
| T1-97 | **AP2127 adjustable: V<sub>REF</sub> = 0.8 V, min 0.784 / max 0.816 (±2 %)**, V<sub>OUT</sub> = V<sub>REF</sub>(1 + R1/R2), 300 mA, and a feed-forward cap is datasheet-recommended for noise and stability. Ordering code: **`K` = SOT-23-5, `ADJ` = adjustable** | `AP2127_Diodes.pdf` §Adjustable Operation + electrical table. **Closes V-23 and F36** |
| T1-90 | **V-28 CLOSED — `SM8S24AHM3` is electrically IDENTICAL to the NRND `SM8S24A` on every figure this design uses.** V<sub>WM</sub> 24.0 V · V<sub>BR</sub> 26.7/28.1/29.5 V · I<sub>PPM</sub> **170 A** · V<sub>C</sub> **38.9 V** · α<sub>T</sub> 0.087 %/°C · R<sub>θJA</sub> 55, R<sub>θJM</sub> 0.35 °C/W · P<sub>D</sub> 8 W · I<sub>FSM</sub> 700 A. Family now runs to **85 V** standoff. **`P_PPM` 6600 W (10/1000 µs) and 5200 W (10/10 000 µs) are BOTH listed for the same UNIDIRECTIONAL part** | Vishay **doc 98647, rev. 14-Oct-2025**, pp.1–2 rendered. **Settles the three-way reading: the two-waveform interpretation is correct and the uni-vs-bi one is wrong.** The distributor's 43 V/153 A is not reproducible from the table — **43 V is the *standoff* of SM8S43AHM3**, a mis-mapped field |
| T1-91 | **Package designation changed DO-218AB → DO-218AC, and the land pattern did NOT change.** Mounting pad **15.30 × 10.70 mm** (main 9.80 × 10.70, lead 2.15 × 2.60, gap 3.35), body 13.3–13.7 × 8.3–8.7 mm, height 4.7–5.0 mm — the same drawing. AC adds a **0.10 mm nominal standoff** dimension. Heatsink is still the **anode** | Doc 98647 p.5 rendered, compared against doc 88387 p.5. **No footprint rework**, and the Block E pad note stands unchanged |
| T1-92 | **vishay.com IS reachable from this environment.** The shortlink form `https://www.vishay.com/doc?NNNNN` resolves server-side to the current revision and returns a PDF. It also **returned a different, newer file for doc 88387 than the held copy** — same content, but with a text layer the held copy lacks | Direct fetch, HTTP 200, `application/pdf`, final URL `docs/88387/sm8s.pdf`. **Retracts the standing "vishay.com refused this environment" claim** — see the ledger entry |
| T1-86 | **SM8S24A confirmed at figure level — and it promotes the three-distributor T2 to T1.** V<sub>WM</sub> **24.0 V** · V<sub>BR</sub> **26.7 / 28.1 / 29.5 V** at I<sub>T</sub> = 5 mA · V<sub>C</sub> **38.9 V at I<sub>PPM</sub> = 170 A** · leakage 10 µA at 25 °C but **150 µA at T<sub>J</sub> = 175 °C** · α<sub>T</sub> **0.087 %/°C**. Package DO-218AB, P<sub>PPM</sub> **6600 W (10/1000 µs) / 5200 W (10/10 000 µs)**, P<sub>D</sub> 8 W on infinite heatsink, I<sub>FSM</sub> **700 A** (8.3 ms), T<sub>J</sub> max 175 °C, AEC-Q101, **unidirectional only**, **heatsink tab is the ANODE**. R<sub>θJA</sub> 55 °C/W, **R<sub>θJM</sub> 0.35 °C/W** | `sm8s.pdf` (Vishay 88387, rev. 06-Feb-2026) pp.1–2, **rendered** — the file has no text layer at all, so this is a figure-level read by necessity as well as by policy |
| T1-87 | **The derived number that actually governs: dynamic resistance r<sub>d</sub> = (V<sub>C</sub> − V<sub>BR,nom</sub>)/I<sub>PPM</sub> = (38.9 − 28.1)/170 = 63.5 mΩ.** At the currents this circuit sees, the clamp is **28.9 V at 12 A, 29.7 V at 25 A, 31.1 V at 48 A** (25 °C), rising to **34.2 V at 48 A / 150 °C** once V<sub>BR</sub> is scaled by α<sub>T</sub>. The 38.9 V headline is the clamp at a current this design never reaches | Derived from T1-86. **Drives M10** — quoting 38.9 V outside its test condition and adding tempco gives 44 V and condemns a sound design |
| T1-88 | **ISO 7637-2 pulse 5 for 14 V powertrains, from the vendor's own table:** V<sub>TOTAL</sub> **78.5–100.5 V**, U<sub>S</sub> **65–87 V**, V<sub>A</sub> 13.5 V, **R<sub>i</sub> 0.5–4.0 Ω**, **t<sub>d</sub> 400 ms**, 1 cycle. JASO A-1 alongside it at 70–88 V / 0.8–1.0 Ω / 200 ms | `tvs.pdf` (Vishay 88490) Table 1. **Corrects the working assumption**: the 35 V figure used earlier is the *suppressed* level, not pulse 5 itself |
| T1-89 | **DO-218AB land pattern: 15.30 × 10.70 mm overall** — main pad 9.80 × 10.70 mm, lead pad 2.15 × 2.60 mm, gap 3.35 mm. Body 13.3–13.7 × 8.3–8.7 mm, height **5.0 mm max**, IPC-7351. **Does not stuff on an SMC land** | `sm8s.pdf` p.5, rendered. **Block E input** — and since the tab is the anode (ground), R<sub>θJM</sub> = 0.35 °C/W is only as good as the copper poured under it |
| T1-80 | **LT3094 confirmed against its own document, and it is NOT the LT3045 mirrored.** −20 V / 500 mA, dropout 235 mV, output range 0 to −19.5 V, 0.8 µV<sub>RMS</sub> (10 Hz–100 kHz), SET sinks 100 µA ±1 %. Pin map **1,2 IN · 3 EN/UV · 4 PG · 5 PGFB · 6 ILIM · 7 VIOC · 8 SET · 9 GND · 10 OUTS · 11,12 OUT · EP 13 = IN**. **The exposed pad is IN, where the LT3045's is GND**, and `DD` is DFN-**12** here against DFN-**10** on the LT3045 | Rev. B Pin Functions p.15 **and** the Pin Configuration diagram p.3, read independently — 100 % agreement (M2). Diagram caption states *"EXPOSED PAD (PIN 13) IS IN"* outright |
| T1-81 | **LT3094's PSRR curve is its own shape, not the LT3045's.** At 2 V headroom: **76 / 66 / 72 / 72 dB** at 100 kHz / 500 kHz / 1 MHz / 2 MHz — it **peaks at 100 kHz** where the LT3045 peaks at 2 MHz, and **declines as headroom grows beyond ~2 V**, the opposite of the LT3045. Audio band (G46, V<sub>OUT</sub> ≤ −1.5 V): ~112 dB peak near 30 Hz, ~107 dB to 1 kHz, **≥ 93 dB at 20 kHz** | Curves G47 and G46 p.12, cropped to 400 dpi and read. **The operator's instruction not to inherit G45 was correct** — inheriting it would have overstated the negative rail by ~12 dB at 2.2 MHz |
| T1-82 | **LT3045 current-limit programming: `Current Limit = 150 mA·kΩ / R_ILIM`**, with the datasheet's own worked example — *"a 1kΩ resistor programs the current limit to 150mA and a 2kΩ resistor programs 75mA."* ILIM threshold 300 mV; the pin sources current 1:500 to output current. **"If the programmable current limit functionality is not needed, tie ILIM to GND."** LT3094's equivalent scale is **3.75 A·kΩ** — a 25× different constant on the sibling part | Rev. D Applications Information p.19 + p.15. **Drives F40** |
| T1-83 | **LT3045 `PGFB` unused disposition:** *"If fast start-up capability is not used, tie PGFB to IN or to OUT for output voltages above 300mV. **Note that doing so also disables power good functionality.**"* So PGFB→OUT is datasheet-sanctioned and knowingly gives up PG | Rev. D p.19. The five housekeeping LDOs take this; U15 gets a real divider instead |
| T1-84 | **LM5156-Q1 pin map, 12-pin WSON (DSS):** 1 BIAS · 2 VCC · 3 GATE · 4 GND · 5 CS · 6 COMP · 7 DITHOFF · 8 FB · 9 SS · 10 RT · 11 PGOOD · 12 UVLO/SYNC/EN · EP. **EP "must be connected to GND"** — electrical, not thermal-only. **Pin 12 "must not be left floating."** DITHOFF polarity: **VCC disables** dither, **GND enables** it | Table 7-1 p.4 cross-checked against Figure 7-1, same page — 100 % agreement (M2) |
| T1-85 | **LM61460-Q1 `BIAS` has an explicit high-output-voltage rule:** *"Input to internal LDO. Connect to output voltage point to improve efficiency… **If output voltage is above 12 V, connect this pin to ground.**"* Below 3.1 V on BIAS, VIN powers the internal LDO directly | SNVSB70F Table 7-1 p.4 + §9.3.6. **Settles the IBB's BIAS disposition from the document** rather than from the 16 V abs-max argument alone |
| T1-79 | **TI's documented inverting buck-boost is a reconfigured *buck*, not a boost** — SNVA856 "Working With Inverting Buck-Boost Converters", 20 pp. Carries §4.1 voltage stress, §5 component selection, and **§7.1/§7.2/§7.3 level shifters for enable, sync and power-good** — the three practical problems a negative-referenced controller creates. Worked examples use LMR33640 and LMR14020 | `SNVA856_TI_InvertingBuckBoost.pdf` Rev. B, contents + §2. **None of the five switching datasheets held documents an inverting configuration** |

**Twenty-one datasheets now held and read to varying depth** (`DATASHEETS.md`). `CLAUDE.md` §5's
*a part number is not a datasheet* still governs every parameter not in this table. T1-10 remains
the one fact resting on operator confirmation rather than a document — worth the 60-second
re-check next time the AK4118A file is open, since the whole F1 disposition stood on it.

### T1 by decree — requirements

Binding because `REQUIREMENTS.md` is the authority, not because the underlying state has been
independently confirmed. Section references are to `REQUIREMENTS.md` **v0.1**.

| ID | Requirement | Src | Tag |
|---|---|---|---|
| T1-D01 | Single-board automotive DSP: 4 diff analog in, 12 buffered SE out, coax SPDIF in, BT A2DP sink, BLE+WiFi control, 12 V automotive power | §1 | |
| T1-D02 | fs = 48 kHz system-wide, 32-bit slots | §4 | HARD |
| T1-D03 | Single 24.576 MHz low-jitter XO is the master clock; ADAU1466 PLL to 48 kHz core | §3 | HARD |
| T1-D04 | ADC/DAC MCLK distributed via low-additive-jitter fanout buffer, **not** daisy-chained | §3 | HARD |
| T1-D05 | No spread-spectrum anywhere in the audio clock tree | §3 | HARD |
| T1-D06 | BM83 and SPDIF paths both traverse an on-chip ASRC — "no exceptions" | §3 | HARD |
| T1-D07 | TDM/port map exactly per the §4 table; spare IN3/OUT3 to 0.1" headers with interleaved grounds | §4 | HARD |
| T1-D08 | DAC split is 6+6 across two AK4458; slots 7–8 reserved on each | §4 | HARD |
| T1-D09 | ESP32-S3 is sole owner of all device state; SPI slave-boot + safeload to DSP, ≥10 MHz target | §5 | |
| T1-D10 | GPIO19/20 reserved for USB D± — not assignable elsewhere; USB-C device role, ESD-protected | §5 | |
| T1-D11 | Input ranges: line ≤2 Vrms, speaker ≤30 Vrms FS; MCU-controlled relay or analog switch; **never jumpers**; Zin ≥ 20 kΩ line | §6.1 | |
| T1-D12 | Signal-sense per input (or summed node), ~10 mVrms threshold, resistor-settable | §6.1 | |
| T1-D13 | ≥ 4.5 Vrms before clip into 10 kΩ on all 12 outputs; Zout ≤ 100 Ω | §6.2 | HARD |
| T1-D14 | Shunt mute at each RCA on a single MCU-driven mute rail; relay preferred, FET acceptable only if THD contribution < DAC floor | §6.2 | |
| T1-D15 | Single ground plane; analog/digital partitioned **by placement, not splits**; chassis star-connect at RCA ground field via RC network; deviations flagged | §6.3 | |
| T1-D16 | Rail set and names exactly per §7.1; all battery-facing regulators AEC-Q100 | §7.1 | |
| T1-D17 | ±13V5_A noise budget < 50 µVrms, 20 Hz–20 kHz, at the op-amp rails after LDO/filtering | §11 | |
| T1-D18 | ISO 7637-2 survival at the input | §7.1 | HARD |
| T1-D19 | Turn-on sequence §7.2 and turn-off sequence §7.3, in order; no audible pop is acceptance | §7.2/7.3 | HARD |
| T1-D20 | BM83SM1 and ESP32-S3-WROOM-1 antenna keepouts enforced; the two 2.4 GHz antennas separated as far as geometry allows, not stacked | §8 | HARD |
| T1-D21 | Net naming per §10; analog channel numbers match §4 TDM slots with no remapping | §10 | HARD |
| T1-D22 | WM8804, TJA1051T-Q1, 25AA1024 are DNP on v1 | §2 | |
| T1-D23 | AKM→TI substitution (PCM1865/PCM1690) is pre-approved but changes TDM formats and must be flagged if exercised | §2 | |
| T1-D24 | Board envelope ≤ 200 × 140 mm assumed until told otherwise | §11 | |
| T1-D25 | Post-fab acceptance criteria per §12 (8 items) | §12 | |
| T1-D26 | **AK4118A is clock master on SDATA_IN2**; DSP port is clock consumer of that link only; ASRC does the rate conversion; recovered clock terminates at the ASRC boundary | §3 v0.2 | HARD |
| T1-D27 | **2×** INA1650, not 4 — 4 diff inputs = 4 channels at 2 ch/pkg | §2 v0.2 | |
| T1-D28 | **Not an AEC-Q board.** Operating range −20 °C…+70 °C; industrial grade acceptable throughout the signal path; AEC-Q100 only where parts face the battery/harness directly — input protection, bucks, CAN PHY, remote-out driver | §7.0 v0.2 | |
| T1-D29 | **OPA1656**, decided. OPA1612 alternate dropped; filter values computed against OPA1656 only | §2/§6.2 v0.2 | |
| T1-D30 | ±13V5_A: **200 mA continuous, 250 mA peak, per rail** | §7.1 v0.2 | |
| T1-D31 | Input attenuator: divider **ahead of** the switch element; resistors **0.1 % matched or better** as a BOM requirement | §6.1 v0.2 | |
| T1-D32 | AOUT1–6 = AK4458 #1 slots 1–6; AOUT7–12 = AK4458 #2 slots 1–6. Net names follow the **system** channel number, never the per-device slot | §10 v0.2 | HARD |
| T1-D33 | EDA tool is **KiCad** | Operator instruction, 2026-08-15 | |
| T1-D34 | **Mute is the zero-energy state.** De-energised = muted by construction. §7.2/§7.3 cover the orderly path; §7.4 is the only thing that survives crank sag, blown fuse or pulled connector | §7.4 v0.3 | HARD |
| T1-D35 | Latching relays **prohibited**. Non-latching relays permitted only energised-to-unmute, and if chosen the +5V_D budget grows ~0.5 A and the LM61460-Q1 is re-checked. Semiconductor shunt is the default and a relay must justify itself | §6.4 v0.3 | |
| T1-D36 | Rail monitoring via **ADS1015-class 4-ch I2C ADC on I2C0** — VBATT, +13V5, −13V5, 3V3_A. Not the ESP32-S3 ADC. §9 dividers unchanged; −13V5 referenced to a positive rail | §5/§9 v0.3 | |
| T1-D37 | **FCC Part 15 Class B design practices; no chamber test for v1; CISPR 25 out of scope.** Spread-spectrum **stays enabled on the bucks** — §3's prohibition is on the audio clock tree only | §7.5 v0.3 | |
| T1-D38 | Version control is **git**, library **in-repo** not a submodule | Operator, 2026-08-15 | |
| T1-D39 | Footprint sourcing: vendor-published verbatim → IPC-generated → hand-built as last resort. Verification is an adversarial rasterise-over-datasheet pass logged per part; operator personally checks ADAU1466, AK5574, AK4458, AK4118A, BM83SM1 | Operator, 2026-08-15 | |
| T1-D40 | **Series–shunt mute.** Series = Form A photoMOS (TLP3475-class), energised-to-pass, open when unpowered. Shunt = depletion-mode FET pair, back-to-back source-to-source, biased off from −13V5_A, conducting when unpowered. Both fail safe independently; failed-state depth is the product | §6.4 v0.4 | HARD |
| T1-D41 | Mute continuous cost: ~60 mA on +5V_D (12 × 2–5 mA photoMOS LED drive), ~0.3 W, held for the operating life. A **line item in the +5V_D budget**, not a rounding error | §6.4 v0.4 | |
| T1-D42 | **CCIF twin-tone IMD ≤ 0.003 %** — 19 kHz + 20 kHz at 2 Vrms, product at 1 kHz. Added alongside the existing 1 kHz THD criterion, not replacing it | §12 v0.4 | |
| T1-D43 | Mute depth requirement is **bounded by the amp's remote-mute latency**, not indefinite — remote-out is fail-safe and drops before anything else notices. V-16 models DAC residual × mute attenuation × amp gain × amp mute latency, with a pessimistic latency | §7.4 v0.4 | |
| T1-D44 | Board is **ODSP-12**, PN `ODSP12-MB-A`, revision scheme A/B/C… for fab revisions with the running change log in git | Operator, 2026-08-15 | |
| T1-D45 | Symbol pin maps verified against the datasheet's **pin-function table**, not the package drawing — vendors have shipped datasheets where the two disagree and the table is normative | Operator, 2026-08-15 | |

---

## 2. T2 — Highly probable (actionable, still tagged)

Derived by calculation or strong inference from T1-D. Actionable; still tagged; downstream work
inherits the tag.

| ID | Claim | What promotes it |
|---|---|---|
| T2-01 | BCLK rates at 48 kHz / 32-bit slots: **TDM8 = 12.288 MHz**, **TDM4 = 6.144 MHz**, **I2S stereo = 3.072 MHz**. MCLK = 24.576 MHz = **512 fs**. | Arithmetic from T1-D02/D03 — solid; confirm each peer accepts these ratios (§8 V-04) |
| T2-02 | No parallel memory bus exists anywhere on this board — ADAU1466 uses internal RAM, ESP32-S3-WROOM-1 has flash/PSRAM inside the module. **The usual dominant layer-count driver is absent.** | BOM read; confirm no external DSP program memory beyond the DNP EEPROM |
| T2-03 | Finest pitch is the ADAU1466 72-LQFP at **0.5 mm**, and there is **no BGA**, if the LQFP option is taken. WLCSP would change this materially. | Datasheet package drawing (§8 V-01) |
| T2-04 | Controlled impedance is required on exactly two things: **SPDIF coax at 75 Ω** and **USB D± at 90 Ω differential**. All TDM/I2S at ≤12.288 MHz is slow enough not to need it; both antennas are module-integrated so there is **no 50 Ω RF trace to route**. | Operator decree — currently a proposal, see F4 |
| T2-05 | Reaching 4.5 Vrms SE from an AK4458 differential output requires roughly **13 dB of gain** in the diff-to-SE stage (if FS is ~2.8 Vpp diff ≈ 1.0 Vrms). This sets the output-stage noise budget and the resistor values, and it multiplies DAC-referred noise by ~4.5×. | AK4458 FS output voltage from datasheet (§8 V-05) |
| T2-06 | ±13.5 V rails give OPA1656 roughly ±12 V of usable swing into 10 kΩ, i.e. ~8.5 Vrms capability against a 4.5 Vrms requirement — **comfortable headroom**, ~5.5 dB. | OPA1656 output swing spec (§8 V-06) |
| T2-07 | ESP32-S3 pin budget drops to **~21 GPIO** after T1-D36 moves rail sensing to I2C: SPI 4, UART 2, I2C 2, signal-sense 4 (comparator outputs, digital), remote-in 1, mute 1, remote-out 1, BM83 MFB+reset 2, DSP reset 1, LED 1, USB 2. Was 22–24 with three ADC channels on the SoC. | The explicit pin map, which §5 requires before capture — not yet done |
| ~~T2-12~~ | ~~`Ron × Coff` constrains a single shunt device, so depth and linearity compete~~ | **Retired by topology, not disproved.** The analysis was correct *for a shunt-only design* and is what motivated the split into series–shunt (T1-D40). It no longer constrains the part choice, because no single device is now asked for both |
| T2-13 | Off-state distortion from a shunt's nonlinear capacitance is negligible at 1 kHz and rises ~20 dB/decade. **1 kHz THD cannot see it; 20 kHz THD cannot either**, because the harmonics land at 40/60 kHz outside the band. Only an in-band distortion *product* catches it. | Resolved into T1-D42 (CCIF twin-tone). Retained here because the reasoning, not just the criterion, is what transfers |
| T2-14 | A **single** MOSFET shunting a bipolar audio signal conducts through its body diode on one half-cycle. Discretes must be **back-to-back, source-to-source**. | Standard device physics — high confidence, but it goes in the schematic as a reviewed detail, not an assumption. Survives the v0.4 topology change unchanged |
| T2-15 | Series photoMOS off-isolation alone is frequency-dependent — a few pF of Coff against a 10 kΩ load gives roughly 70 dB at 1 kHz falling to ~45 dB at 20 kHz. **This is exactly the leakage the shunt exists to kill**, and it is why the shunt's Ron requirement is lax (100–500 Ω against a ~MΩ leakage source impedance still buys ~70 dB). | V-14/V-15 with real part numbers. The point that matters is the *ratio*, and it is comfortable by two orders of magnitude |
| ~~T2-08~~ | CMRR ≥ 60 dB is set by attenuator resistor matching, implying 0.1 % or better | **Promoted → T1-D31.** Decreed as a BOM requirement 2026-08-15. A tolerance analysis before the BOM freezes is still worth doing — 0.1 % is the estimate that generated the decree, not a measured margin |
| T2-11 | **RCA-class jack count is 17 populated, 18 positions**: 4 line in + 12 out + 1 SPDIF coax in, plus 1 DNP SPDIF out. Differential inputs are tip-vs-shield on a single jack, so 4 inputs = 4 jacks, not 8. | Confirmed against `REQUIREMENTS.md` §8 by the operator, 2026-08-15, after the assistant stated 28 in error. See ledger |
| T2-09 | The ADAU1466's PLL locks to the same 24.576 MHz XO that feeds the converters' MCLK, so LRCLK and MCLK are frequency-coherent by construction. Phase/jitter relationship is not thereby guaranteed. | AKM MCLK/LRCK synchronisation requirement in TDM slave mode (§8 V-04) |
| T2-10 | Schematic capture can proceed on the §4/§5/§6/§7 architecture **without** any Block D/E answer. Only footprint assignment and layout depend on mechanical and fab data. | — structural, acted on in `CLAUDE.md` §2 (G0-S / G0-L split) |

---

## 3. T3 — Likely / moderate confidence

Branchable, but check the root before the branch gets expensive.

| ID | Theory | Check |
|---|---|---|
| ~~T3-01~~ | ~~The EDA tool is KiCad~~ | **Closed, and it was right — which is the trap.** Operator decreed KiCad (T1-D33) and the install verified at T1-05…T1-09. A correct guess held at T3 cost nothing; the same guess acted on would have been indistinguishable from luck. Note it did not predict **version 10**, which is the part that actually matters (see ledger) |
| T3-02 | This board wants **6 layers** (sig / GND / pwr / pwr / GND / sig or similar), not 4: mixed-signal with a mandated single unsplit ground plane, seven rails, ±13.5 V analog distribution, two 2.4 GHz modules, and switching regulators — even without a memory bus. | Q22. **Not acted on.** Layer count is a fab and cost decision, and T2-02 cuts the other way. |
| ~~T3-03~~ | ~~"4× INA1650" is a channel count in a package column~~ | **Confirmed by operator → T1-D27.** 2× INA1650 |

---

## 4. Open unknowns — remaining intake

Rows are **BLOCKING** unless marked. Closed rows are struck and promoted to §1.

### Block A — Engagement and role

| ID | Question | Why it matters | Status |
|---|---|---|---|
| ~~Q1~~ | ~~What is being delivered?~~ | | **Closed** → schematic capture then layout, greenfield. `CLAUDE.md` §1 |
| ~~Q2~~ | ~~Channel policy~~ | | **Closed 2026-08-15** → closed-book by default, batched escalation, stop-the-line exception. Written into `CLAUDE.md` §4. Settled **by observation** — the project had been running it for five rounds |
| ~~Q3~~ | ~~Version control?~~ | | **Closed** → git, initialised 2026-08-15, library in-repo. T1-D38 / DL-15 |
| ~~Q4~~ | ~~Board name/PN/revision~~ | | **Closed** → **ODSP-12**, PN `ODSP12-MB-A`, rev A/B/C… per fab revision, change log in git. T1-D44 |
| Q5 | Is the process visible to the client as well as the result? | Changes how much reasoning is written for an outside reader | Non-blocking |

### Block B — Tooling · *gates: G0-S, and therefore capture*

| ID | Question | Why it matters | Status |
|---|---|---|---|
| ~~Q6~~ | ~~EDA tool, version, install path~~ | | **Closed** → KiCad 10.0.5, T1-D33 / T1-05 |
| ~~Q7~~ | ~~CLI on PATH?~~ | | **Closed** → no. Full path always, T1-06 |
| ~~Q8~~ | ~~Bundled Python path~~ | | **Closed** → T1-07 |
| ~~Q10~~ | ~~Units: mm or mil?~~ | | **Closed** → mm, decided and logged DL-09 |
| Q9 | Autorouter in play? Which, and what runtime? | Changes routing strategy and which ledger entries apply | BLOCKING (layout) |
| ~~Q30~~ | ~~Footprint library verification~~ | | **Closed** → T1-D39, DL-14 |

### Block C — Electrical

| ID | Question | Why it matters | Status |
|---|---|---|---|
| ~~Q12–Q18~~ | | | **Closed** by `REQUIREMENTS.md` §1–§10 → T1-D01…D25 |
| ~~Q29~~ | ~~INA1650 quantity~~ | | **Closed** → 2×, T1-D27 |
| ~~Q33~~ | ~~OPA1656 or OPA1612~~ | | **Closed** → OPA1656, T1-D29 |
| ~~Q31~~ | ~~±13V5_A current budget~~ | | **Closed** → 200 mA cont / 250 mA peak, T1-D30. *Mute-rail budget still open below* |
| ~~Q32~~ | ~~Rail monitor: distinct device or ESP32 ADC?~~ | | **Closed** → ADS1015-class on I2C0, T1-D36 |
| ~~Q38~~ | ~~Mute rail budget~~ | | **Closed in principle** → T1-D34/D35 make it a GPIO-class load with no §7.1 entry beyond a line item, *conditional on* the semiconductor shunt surviving V-14/V-15. If a relay is justified instead, +5V_D grows ~0.5 A and the LM61460-Q1 is re-checked |

### Block D — Mechanical · *gates: G0-L, and therefore all layout*

| ID | Question | Why it matters | Status |
|---|---|---|---|
| Q19 | Board outline and dimensions, or the DXF/STEP that defines them | ≤200×140 mm is an *envelope*, not an outline. Hardest constraint; changing it after placement invalidates the layout | BLOCKING (layout) |
| Q20 | Mounting holes, keepouts, enclosure interference | Placement anchors, not adjustments | BLOCKING (layout) |
| Q21 | Component height limits, top and bottom | Silently violated otherwise, discovered at assembly | BLOCKING (layout) |
| Q34 | Connector part numbers — RCA jacks (16 of them), automotive power connector, speaker-level strip terminal | 28 RCA-class jacks dominate the board edges and the area budget. Footprints are needed before any placement | BLOCKING (layout) |

### Block E — Stackup and fabrication · *gates: G0-L, G2, G3, G4*

**The TVS land pattern is an ELECTRICAL rating input, not an outline** *(2026-08-16, F42)*. Vishay
states the load-dump capability figures are *"based on normal room temperature **with the
recommended pad size as listed in the datasheet**, but the actual capability varies by PCB type,
pad size, and temperature conditions"* (doc 49748). So **§12's whole verdict column is conditional
on the layout honouring the recommended pad** — DO-218AB, land **15.30 × 10.70 mm**, tab is the
**anode**, so it pours into the ground plane. R<sub>θJM</sub> = 0.35 °C/W is junction-to-*mount*
and is only as good as the copper under it. **This is the first case on the project where a
layout choice moves a number in the acceptance criteria**, which is a different class from
"placement affects performance" — shrink this pad at layout and §12 becomes false.

**New input, logged 2026-08-16 (F39):** the SEPIC's **FET, Schottky and coupled inductor are now
the board's dominant heat sources** — ≈ 8.5 W through that stage, ~1.65 A input at crank. Copper
allocation there is a **stackup input**, alongside the ADAU1466's 5.3 mm exposed-pad via array.
Two thermal claims on the layer count now, from opposite ends of the board.

| ID | Question | Why it matters | Status |
|---|---|---|---|
| Q22 | Layer count and intended stackup | G3. T3-02 is a guess and is not acted on | BLOCKING (layout) |
| Q23 | Fab house and capability limits: min trace/space, min drill, annular ring, allowed via types | These *are* the design rules | BLOCKING (layout) |
| Q24 | Copper weight and surface finish | Affects trace width for the ±13V5 and battery rails, and fine-pitch assembly | BLOCKING (layout) |
| Q25 | Source of the shipped design rules and DRC severities | G2 requires a baseline that exists before work starts | BLOCKING (layout) |
| Q35 | Confirm or replace the proposed impedance targets: 75 Ω SPDIF coax, 90 Ω USB differential | F4. Feeds directly into the stackup | BLOCKING (layout) |

### Block F — Assembly, thermal, EMC

| ID | Question | Why it matters | Status |
|---|---|---|---|
| Q26 | Single- or double-sided assembly | Drives silkscreen, courtyards, fiducials, and whether the 12 mute relays can go on the bottom | BLOCKING (layout) |
| Q27 | Thermal: airflow, hot parts, expected dissipation | Automotive enclosure, ±13.5 V switcher, 24 op-amps and possibly 12 relay coils in a sealed box | BLOCKING (layout) |
| ~~Q36~~ | ~~Operating temperature range and AEC-Q grade~~ | | **Closed** → −20…+70 °C, not an AEC-Q board, T1-D28 |
| ~~Q37~~ | ~~Emissions target~~ | | **Closed** → FCC Part 15 Class B practices, no chamber for v1, CISPR 25 out of scope. T1-D37 |

---

## 5. Anti-drift ledger

**Permanent.** Entries are never deleted once corrected — the point is that a corrected belief
cannot quietly return.

Format: the wrong belief → the correction → **the tell** that catches it.

### Method rules — promoted from specific entries because they generalise

**M5 — "Nothing is missing" needs "and there were N things."** A check passes **vacuously** when
its input is empty. Every completeness assertion needs a companion assertion that the input was
non-empty **and plausibly sized against an independent expectation**. Four instances now: ERC on
an empty sheet, `file` reporting 10 pages, HTTP 200 on the wrong PDF, and a pin-set assertion over
an empty pin map. Stating the rule is what stops the fifth from needing to be caught by luck.

**M7a — The convention caught its own author.** The FB leakage term was first stated
conversationally as **"5 µV"**; 100 nA × 50 kΩ is **5 mV** — off by three orders of magnitude, by
the operator, in the same round that specified the convention. **The conclusion survived** (the
window is wide either way) **and the derivation under it was broken** — M1a's exact shape, this
time on the operator's side rather than the assistant's.
*What caught it:* the convention **required the inequality to be written on the sheet**, and
**written arithmetic gets checked in a way conversational arithmetic does not.** The sheet now
carries the correct figure: 50 nA × 50 kΩ = **2.5 mV against a 60 mV window, 24× margin**.
*Why it belongs beside M7:* consequences are cheaper to check than derivations **and they check
both parties.** A method whose whole claim is that written constraints catch what confidence
misses is only evidenced when it catches the people who wrote it. It now has that evidence from
both sides of the desk, in the same session — the `RT` error and this one.

**The "vishay.com is unreachable" claim was wrong, and it shaped two rounds of asks.** *(caught
2026-08-16.)* It came from **one** failed fetch — `docs/88361/smbj.pdf`, which returned HTML —
and was generalised to the host, then repeated in `DATASHEETS.md` and in two escalations as a
reason the operator had to fetch things manually. The shortlink `vishay.com/doc?88387` returns a
PDF, HTTP 200, first try. **A single failed request is evidence about that request, not about the
host** — the same shape as M1 (confidence attaches to the method) and the same shape as the grep
errors, one observation promoted to a general rule. *The tell:* a negative claim about
infrastructure should name what was tried and stay scoped to it, and it costs one retry to check
before it becomes an ask on someone else's time.
*Technique worth keeping, since it is what actually found the successor:* **PDF hyperlinks are
extractable** — `/URI (...)` entries, including inside compressed streams — so a datasheet that
cross-references other documents hands you their doc numbers directly. That is how doc **98647**
was located after the NRND banner text turned out not to be a link.

**M13 — A PDF's cross-reference graph is machine-readable navigation, not decoration.**
Embedded `/URI` entries — including inside compressed streams — turn "hunt the successor
document" into a parse. Doc **98647** was found this way after the NRND banner's *text* turned
out not to be a link while the "Related Documents" icon was. **This pays on every vendor whose
site search is worse than their own documents, which is most of them**, and it is strictly better
than guessing doc numbers or trusting a distributor's link. *Companion to M11:* when a document
points at a successor, the pointer is usually **in** the file, so the redirect boundary M11 warns
about is normally crossable without leaving the archive.

**M12 — An elimination carries its evidence and its scope, exactly like a promotion.** *(operator,
2026-08-16.)* The project already tagged every T1 with how it was verified; **eliminations had no
such discipline**, and F44(b) is what that costs — "ruled out" entered the record as a bare verdict
and survived because nothing prompted a re-read of its basis. **Every "ruled out" now travels with
(a) the evidence that ruled it out and (b) the scope that evidence covers**, so it is re-openable by
a scope check rather than by luck or by a second party happening to hold different data.
*The held-for-elimination datasheet practice was half of this* — the document was kept, but the
*claim* was not tagged, and the claim is what gets consulted. **Concretely:** a wrongly-eliminated
option is worse than a wrong number, because a number gets re-derived when something downstream
disagrees with it, while an eliminated option is simply never revisited — nothing downstream
depends on it, so nothing can contradict it.
*It paid immediately:* the very next round, `SM8S24AHM3`'s own datasheet also says
*"Unidirectional"*, so a bidirectional member remains **unverified rather than disproven** — a
distinction M12 forces and the old habit would have collapsed in whichever direction was convenient.

**M11 — A superseded document is authoritative about the past, not about its redirect target.**
`sm8s.pdf` says *"available in unidirectional polarity only"*, and that sentence is **true of the
SM8S10A–43A family it describes**. It was carried forward as a fact about the **AHM3 successors**,
where it is false — a parallel **SM8S10CA–85CA** bidirectional series exists. **An NRND datasheet
is structurally incapable of describing what its replacement added**, so its scope statements
expire at the redirect boundary while its numbers do not.
*The tell — and it is the same one as T1-28 and M1a:* **a claim inherits the scope of the heading
it was read under**, and here the heading was the document itself. When a document names a
successor, every "only", "never" and "not available" in it is scoped to the old family and must be
re-read against the new one before it can be used to eliminate an option.
*Cost of the miss:* it eliminated a design route (bidirectional TVS ahead of Q2) that is in fact
available — the most expensive kind of error, because a wrongly-eliminated option is never
revisited. Caught only because the operator held distributor evidence from the successor family.

**M10 — A worst-case number quoted outside its test condition is not conservative, it is wrong.**
**Generalised: conservatism is a property of an *analysis*, not of a number — a number is only
conservative at its stated conditions.** Transplanted elsewhere it is simply a different number,
and its error has whatever sign the transplant gives it. **Safe-direction errors are the dangerous
ones**, because they survive review by looking like prudence: the 44 V phantom would have sat in
the document forever as margin nobody audited, and the part change it justified would never have
been questioned. *Practical form:* when a figure is doing work, write its test condition beside it
— and when it crosses into a new analysis, re-derive at the new operating point rather than
carrying the endpoint.
The SM8S24A's 38.9 V clamp is specified **at I<sub>PPM</sub> = 170 A**. Carried into an analysis
where the real current is 12–48 A, and then scaled by the breakdown tempco, it says 44 V and
condemns a design whose actual worst case is **34.2 V**. The fix is structural: **datasheet
maxima come with test conditions, and the condition travels with the number or the number does
not travel.** Where a part gives a slope — here r<sub>d</sub> = (V<sub>C</sub> −
V<sub>BR</sub>)/I<sub>PPM</sub> = 63.5 mΩ — use the slope at the operating point, not the endpoint.
*Why it belongs beside M7:* both are about running numbers against reality rather than reciting
them, and this one bites in the **safe** direction, which is worse — an over-conservative wrong
number gets rewarded with a part change nobody questions.

**M9 — A guard that has never fired is itself unverified.** You do not know an assertion checks
what you think it checks until you have fed it a known failure. The F41 collision guard was made
to fire on a synthetic duplicate *before* its green was believed — mutation testing in miniature,
and the enforcement clause M5 and M6 were missing. **The vacuous-completeness family has five
instances precisely because the guards that would have caught them were assumed to work.**
*Applies to:* every new assertion, every new lint, every new check-script. Show it a defect it
must catch, watch it fail, then trust its pass. The cost is one throwaway test; the alternative is
a green light that means nothing and is believed for months.

**M8 — Near-symmetric parts are more dangerous than unrelated ones, because the mistake is
*productive*.** The LT3045 and LT3094 are sold as a matched ± pair, share the SET architecture,
the 100 µA reference, the 0.8 µV<sub>RMS</sub> figure and the `DD` package suffix — and differ in
**lead count (10 vs 12), exposed-pad net (GND vs IN), pin order (ILIM/PGFB/SET vs PGFB/ILIM/VIOC)
and current-limit scale constant (150 mA·kΩ vs 3.75 A·kΩ, a 25× difference)**. Every one of those
is invisible if the negative channel is drawn by mirroring the positive one, and mirroring is
exactly what a symmetric supply invites. *The tell:* when two parts are marketed as a pair, look
for what the marketing flattens — **verify the sibling independently, at figure level, and never
by diff against the one you already read.** Recorded as a rule because the same shape recurs
wherever a vendor ships an inverting/complementary/mirror variant.

**M7 — A design rationale is also a test, and consequences are cheaper to check than
derivations.** Every constraint written down is a check that can be **executed against the
artefact** — and executing them is not the same as having written them. The `RT` error was caught
**not** by re-deriving the RT-to-frequency relation, but because a **consequence** of the value
(fundamental lands at 360 kHz) contradicted a **recorded requirement** (stay above the AM band).
*Why this compounds:* the document is now full of consequences. **It gets more protective as it
grows, not merely longer** — provided the constraints are periodically run against the artefact
rather than only consulted when someone remembers them.

**M6 — Ask of any passing check: "what failure would this not have caught?"** A check is only
sensitive to the failure modes it was designed around. **Completeness checks see omission, never
misassignment** — a pin-set assertion cannot see a permutation, so a symbol with every net wrong
and nothing missing passes it cleanly. **The general shape of the bug is extracting correlated
fields in separate passes and zipping them**; it recurs in every scraping context, not just
symbols. The countermeasure is structural: extract correlated fields **as pairs from a single
match**, so a dropped entry loses one whole record instead of shifting every record after it —
and verify the pairs against a figure-level read, not the sets.

**M1 — Confidence attaches to the method, not the claim.** When a method is known-ragged, *every*
claim it produced inherits the raggedness, **including the ones later verification happens to
bless.** The T1-28 retraction and the `00100`-prefix suspicion came from one careless grep in one
pass; one was false and one was true, and nothing in the output distinguished them. The response
to a broken claim is therefore to **re-derive everything the method touched with the better
method**, not just the claim that broke.

**M1a — the third instance, logged because it proves the rule was needed.** T1-25 said pin 34
`SELFBOOT` selects the self-boot *protocol* by float-vs-pulldown. It does not — **pin 26**
(`SS_M/MP0`) does, and pin 34 merely enables self boot. Same failure as T1-28: a grep crossing
table rows, attributing one row's sentence to another's mnemonic. It was caught by exactly the
method M1 and M2 prescribe, one round after they were written. **F21's disposition survived
unchanged** — pin 34's internal pull-up still means an unstuffed strap boots from an absent
EEPROM — so the conclusion was right for a wrong stated reason, which is its own hazard: a correct
conclusion is not evidence that the reasoning under it was sound.

**M2 — A T1 promotion records the method that produced it.** Provenance is part of the fact, so a
later reader can see "ragged grep" in the citation and discount accordingly. `STATE.md` §1's
"Verified by" column is that field; it is not decoration. Load-bearing claims get a figure-level
read *before* T1 status, not after something downstream breaks.

**M3 — Guarantee by construction, then test that the construction holds.** Acceptance tests are
for what design cannot guarantee. Anything guaranteeable by construction should be, and then
checked cheaply — the F15 cross-DAC alignment rule is one register comparison at boot, not a
bench measurement. Cheaper, and it fails loudly instead of subtly.

**M4 — A decree can be right for reasons its author did not know.** §5's "strap consistently to
I2C" was written for control-plane coherence; it also happened to dodge the AK5574's
I2C-block-active-during-3-wire drive-conflict hazard (T1-33), which neither party knew about when
the decree was written. **Route around a decree and you may be discarding reasons nobody has
articulated yet.** This is why the escalation ladder exists rather than a judgement call.

### Caught on this project

**"28 RCA-class jacks will dominate your board edges"** — assistant, 2026-08-15
*Correction:* **17 populated, 18 positions.** 4 line in + 12 out = 16 RCA, +1 SPDIF coax in,
+1 DNP SPDIF out. The error was pure arithmetic: `STATE.md` Q34 already read "RCA jacks (16 of
them)" — a subtotal containing the outputs — and the 12 outputs were then added to it a second
time in chat.
*The tell:* **the same count existing in two places with two values, where the larger one was
never written as its addends.** A total is an assertion; a sum is checkable. Any count that
steers a decision gets written as `4 + 12 + 1 + 1`, in the document, not as `28` in prose.
*Second tell, and the more useful one:* the operator's first hypothesis was interesting — that
differential inputs were being counted as jack pairs — and the truth was boring. `CLAUDE.md` §5
says to check ordinary human error before building an exotic theory when *operator* data looks
anomalous. **The rule is symmetric.** When the assistant's number is challenged, the first
candidate is a slipped digit or a double-count, not a subtle modelling difference.
*Standing:* the underlying point survived at 18 — connectors still dominate the board edge, and
board-mount vs. flying-lead RCA is still an early decision (Q34). **A conclusion that survives its
own broken evidence is not thereby vindicated;** it was re-derived, and the re-derivation is what
it now rests on.

**"A grep hit is a fact about the part"** — assistant, 2026-08-15, retracting T1-28
*Correction:* it is a fact about **one line**, and a line in a multi-mode datasheet is scoped to
whichever mode's section it sits in. "Chip address (1bit, C1 is fixed to 0)" was pulled from the
AK4118A and filed as its I2C addressing. It is the **4-wire serial mode** description, twelve
lines under a heading the grep never showed. In I2C the part has full CAD1/CAD0 like its
siblings. **A wrong T1 sat in the fact base for one round**, and it was load-bearing — F23's whole
"the address space may be too narrow" framing was built on it.
*The tell:* **a spec extracted from a datasheet that documents more than one interface mode.**
AKM, TI and ADI parts routinely describe I2C, SPI and parallel control in adjacent sections using
the same vocabulary. Before a control-interface fact becomes T1, confirm the **section heading it
lives under**, not just the sentence — `grep -B` to the nearest heading, or render the page.
*Second-order:* the earlier `00100`-prefix suspicion came from the same ragged grep and happened
to be **right**, which is worse, not better — one careless method produced one true and one false
belief in the same pass, and nothing in the output distinguished them. This is why
`CLAUDE.md` §5 says a claim rises a tier on evidence, never on having been useful.

**"An unconnected pin is an undefined pin"** — 2026-08-15, from F21
*Correction:* `SELFBOOT` floating is not undefined — a 250 kΩ internal pull-up makes it a
**chosen** state, and the state it chooses is *boot over SPI from an EEPROM that is DNP on v1*.
An unpopulated strap would have silently selected a boot path to a part that is not on the board.
*The tell:* **floating is a state someone chose. Find out who and why before trusting it.** Every
strap, mode and configuration pin gets its idle level read out of the pin table and stated in the
schematic — an unfitted resistor is a decision, not an absence.

**"A PowerShell round-trip through a text file is lossless"** — assistant, 2026-08-15
*Correction:* Windows PowerShell 5.1 `Get-Content -Raw` reads a UTF-8 file **without a BOM using
the system ANSI codepage**. Every multibyte character becomes separate CP1252 characters, and
`Set-Content -Encoding utf8` then writes that mojibake back as valid UTF-8. One
read-modify-write **double-encoded 204 characters across the whole file** — and it silently
"succeeded". Recovery was `git checkout` plus re-applying the edits through the Edit tool.
*The tell:* **any read-modify-write of a text file through PowerShell 5.1.** Use the Edit tool for
file edits; reserve the shell for running programs, which is what `CLAUDE.md` §7 already implies
and this made concrete. If a shell round-trip is truly unavoidable, force encoding on **both**
ends — and a blanket reverse is not a fix once new correctly-encoded text has been mixed in.
*Why it was cheap:* the damage was one commit deep, so `git checkout` cost only re-work. That is
DL-15 earning its keep on the same day it was made — and an argument for committing before any
bulk edit, not only after.

**"The revision history protects the document"** — assistant, 2026-08-16
*Correction:* it protects everything **except itself**. `REQUIREMENTS.md` carried F30–F34 while its
header still read v0.9 and the v1.0/v1.1 rows did not exist — the mechanism that exists to stop a
version being merged silently had itself merged silently. **The integrity check that guards
everything else has no guard of its own**, and the only thing standing behind it is commit
discipline: the version bump belongs in the same commit as the content it describes, never as a
follow-up.
*The tell:* content edits and the version header living in **different edits**. If a change is
worth a revision row, the row goes in before the content does, not after.

**"A plausible-looking component value is in the right ballpark"** — assistant, 2026-08-16
*Correction:* I placed **`RT = 36.5 kΩ` as "a ~2.1 MHz starting point."** The LM61460's RT-to-
frequency relation is **inverse**: 5.76 kΩ → 2.2 MHz, 33.2 kΩ → 0.4 MHz, 66.5 kΩ → 0.2 MHz.
36.5 kΩ gives roughly **360 kHz — inside the AM broadcast band**, on a **car audio** board whose
antenna is feet away. Off by ~6×, in the one direction that matters.
*The tell:* **a value stated with a frequency next to it that was never derived from the
datasheet's own table.** "Starting point" is not a tier — it is an untagged T4 wearing a number,
and `CLAUDE.md` §5 says speculation never enters a document untagged.
*What caught it:* being asked to **apply the reasoning to the number**. The operator's AM-band
argument existed already; running it against the placed value is what exposed the error. **A
design rationale is also a test** — every constraint written down is a check that can be executed
against the artefact, and executing them is not the same as having written them.
*Now:* `RT = 5.76 kΩ`, a **datasheet-specified point** (2.2 MHz typ, 1.98-2.42 MHz) rather than an
interpolation. Worst case under ±2 % spread: 1.98 × 0.98 = **1.94 MHz, still clear of 1710 kHz.**

**"The completeness assertion passed, so the part is fully connected"** — assistant, 2026-08-16
*Correction:* the F28 assertion is `set(pin_geometry) - set(assigned_nets)`. My pin-extraction
regex required a newline that **this project's own compact symbol format never emits**, so
`pin_geometry` came back **empty** for all three project symbols — and an empty set has nothing
missing. **The assertion passed vacuously and three LM61460-Q1 bucks were placed with every pin
unconnected**, which the netlist showed as 14 `unconnected-(U3-…)` stubs.
*The tell:* **an assertion over a set you did not also assert is non-empty is not a check.** Any
"nothing is missing" test needs a companion "and there was something to miss." Both guards are now
in: `assert pins` at extraction, `assert geo` at placement, plus `assert not extra` to catch a
stale pin map pointing at pins that do not exist.
*Family:* ERC on an empty sheet, `file` reporting 10 pages, HTTP 200 on the wrong PDF. **Fourth
instance of a check that answers the question it was asked while the thing it guards is absent.**

**"Zip the names and the numbers"** — assistant, 2026-08-16, caught before it shipped
*Correction:* I extracted stock-symbol pin names and pin numbers with **two independent regexes
and zipped the results.** Where either list dropped an entry — and both did, on `NC` pins and
duplicated `IN`/`GND` pads — every subsequent pair silently **shifted by one**. It produced a
complete-looking map in which the LT3045's `EN/UV` was pin 2 instead of 3, `PG` was 3 instead of
4, and so on down the part. Had the two lists happened to be the same length, **the pin-set
assertion would have passed and every net on the part would have been wrong.**
*The tell:* **pairing data from two separate passes over the same source.** Extract name and
number from **one match**, so a dropped entry loses the whole record rather than shifting the rest.
*Why it matters more than it looks:* a pin-set assertion checks **completeness, not correctness.**
It cannot see a permutation. This is the M1a shape — the check passed, the reasoning under it was
unsound — and the only reason it surfaced is that the lists were *unequal*.

**"The file parsed, so the file is right"** — assistant, 2026-08-16
*Correction:* the first `02_dsp.kicad_sch` **parsed cleanly, passed ERC with zero violations, and
exported as part of a 10-page PDF — while containing no components at all.** Every available check
said fine except the one that mattered. The cause was that `lib_symbols` sub-symbols had been
given the `LIB:` prefix that belongs only to the parent (`CM5IO:C` contains `C_0_1`, not
`CM5IO:C_0_1`), so KiCad silently discarded every instance.
*The tell:* **for a schematic, the artefact is the netlist, not the file.** ERC on an empty sheet
is vacuously clean; a PDF of an empty sheet still has the right page count. Verify by extracting
**pin-to-net connectivity** and checking it against intent — `+1V2_CORE` must reach pins
20/35/53/71, or the sheet is decoration.
*Family:* this is the same species as *"a download that returned 200 is the document I asked for"*
and the `file`-says-10-pages artefact. Three instances now of **a cheap indicator standing in for
the actual thing**. The rule that keeps earning: check the payload, not the receipt.
*What resolved it:* reading a real KiCad 10 schematic from `share/kicad/demos/` rather than
reasoning harder about the format — DL-13's "T1 only from the tool" applied to file format as
well as CLI flags.

**"A download that returned 200 is the document I asked for"** — assistant, 2026-08-15
*Correction:* an LCSC URL for the ADAU1466 returned **HTTP 200, a `.pdf` extension and a
plausible 47 KB** — and the content was an **HTML page for a Toshiba TLP185 optocoupler**, an
unrelated part from a different manufacturer. Had it been filed unchecked, the V-01 gate would
have shown as satisfied by a document that never mentions the part.
*The tell:* **verify the artefact, not the transfer.** Page count and first-page text against the
expected part number, every time, before a file is recorded as held. Transfer success is a fact
about the network; content correctness is a fact about the document, and only the second one is
what was wanted.
*Second instance, same class, same day:* `file` reported "10 page(s)" for every TI PDF — a
linearized-PDF artefact, not the truth. Both errors are a **metadata proxy trusted over content**.
When a cheap indicator and the actual thing can disagree, read the actual thing.

**"The zero-energy requirement excludes enhancement-mode devices"** — assistant, 2026-08-15
*Correction:* it excludes them **in a shunt**. In **series** the polarity inverts — unpowered, an
enhancement-mode device is open, and an open series path is mute. Form A photoMOS, ruled out one
sentence earlier, is the correct series element. The exclusion was a property of the **topology**
and was stated as a property of the **device class**, which closed a design space that was open,
and left a real depth-vs-capacitance conflict looking irreducible when it was only irreducible
*for a shunt*.
*The tell:* **a conclusion that names a component class rather than a configuration.** Fail-safe
polarity is topological. Any statement of the form "X devices are excluded" must be re-read as "X
devices are excluded *here*" and then tested in the other topology before the space is declared
closed.
*The sharper tell:* this happened **immediately after** correctly solving the shunt sub-case. The
frame that produced the sub-answer was carried forward without re-deriving. Solving a sub-case is
the moment of maximum risk for over-generalising from it — the reasoning is fresh, fluent and
still scoped to conditions that are no longer stated aloud.
*Cost if uncaught:* the design would have gone to capture with a single-device shunt, a
constrained part search that probably fails, and relays waiting as the fallback — carrying 0.5 A
and a watt of coil heat, forever, to solve a problem that two cheap parts solve better.

**"An acceptance criterion covers the failure mode it was written for"** — corollary, 2026-08-15
*Correction:* it covers the failure mode **at the stimulus and frequency it specifies**. §12's
1 kHz THD is blind to nonlinear off-capacitance because the mechanism is negligible at 1 kHz. The
obvious repair — test THD at 20 kHz — is *also* blind, because the harmonics land at 40/60 kHz,
outside the measurement band. Only a stimulus whose distortion **product** falls in band catches
it: CCIF 19 + 20 kHz, product at 1 kHz.
*The tell:* when a new failure mode is identified, ask **which existing criterion would catch it**
and at what stimulus. If the answer is "none, as written", the criterion needs amending — and
amending it means choosing the test, not moving the number. A number tightened at a frequency
where the mechanism is silent buys nothing and reads like diligence.

**"Mute is a state the MCU commands"** — implicit in v0.1 §7.2/§7.3, corrected 2026-08-15
*Correction:* the sequenced mute is the **orderly** path. Rails also collapse by crank sag, blown
fuse, harness fault and pulled connector, and none of those involve the MCU. **Mute must therefore
be the zero-energy state** (T1-D34), which decided the topology outright — it ruled out latching
relays entirely and every enhancement-mode device by construction, before THD was even considered.
*The tell:* **a requirement written as a sequence.** A sequence describes what happens when things
work. Ask what holds the requirement when the sequence never runs — and treat any answer of the
form "the controller sets it" as a gap, because the controller is powered by the thing that just
failed.

**"The EDA tool's CLI and Python API work the way I remember"**
*Correction:* the install is **KiCad 10.0.5**, which postdates this assistant's training. `pcbnew`
has broken API compatibility across major versions before, and CLI flags have moved. Everything
recalled about KiCad tooling is **T2 from memory and T1 only from `--help` or `dir()`.**
*The tell:* a version number higher than any release you can recall notes for. That is not a
detail — it is the whole basis of your confidence about the interface evaporating, silently.

### Pre-seeded from this project's own source document

**A [HARD] flag makes a requirement binding, so it must be right**
*Correction:* [HARD] is a statement about **authority**, not about correctness. `REQUIREMENTS.md`
§3 carries two [HARD] bullets that cannot both be built (F1). Binding and correct are independent
properties, and where they diverge the answer is a logged finding and a question — never a silent
choice between them.
*The tell:* two requirements that are each individually sensible but name the same interface from
opposite ends. Read every clock, bus, and power statement **from both peers' point of view**
before accepting it.

**The board envelope is the board outline**
*Correction:* "≤ 200 × 140 mm" (§11) is a **maximum**, offered as an assumption in the section
titled *Open Items*. It fixes no edge, no origin, no mounting hole and no connector position.
Placement against it would be placement against nothing.
*The tell:* a dimension that arrives with "assume" or "unless told otherwise" attached. That is
an unknown wearing a number.

### Carried forward from previous boards — read before starting

These recurred across a full board build and are not project-specific.

**Netclass track width is a minimum**
*Correction:* netclass widths are **defaults for newly drawn track**, not minima. The floor is the
board minimum. A 1.0 mm trace and 0.8 mm via cannot attach to a 0.25 mm pad on a 0.5 mm-pitch
package. Traces neck at the pad and widen in open copper.
*The tell:* a connection between two **adjacent pads of the same package** failing to route. That
is never topology; it is always width or clearance.
*Live risk here:* T2-03 puts a 0.5 mm-pitch LQFP on this board alongside a ±13.5 V rail that wants
wide copper.

**Via-in-pad is an electrical rule**
*Correction:* it is a **manufacturing** rule — solder wicks down the barrel during reflow — so it
applies **regardless of net**. Clearance checks correctly skip same-net copper, which lets a GND
via land happily on a GND pad. Nets are irrelevant to that check; test every pad.

**Pre-placing helper copper makes the router's job easier**
*Correction:* it makes it **impossible**. Plane stitching, fanout vias and escape stubs become
**fixed wiring** the router cannot move or rip up, and they sit exactly in the escape corridors.
Two independent routers plateaued at the identical completion percentage because of it.
*Correct order:* **route first, stitch the residue afterwards**, where the free space is known. The
same stitching code that caused 145 violations before routing caused zero after it.

**Critical nets can be routed last**
*Correction:* impedance-controlled pairs, crystal nets and RF feeds must be routed **first, on
empty copper**. Anything routed earlier takes the corridor they need, and carving it back out just
displaces the next net into it.
*Live risk here:* MCLK_XO and the four MCLK fanout branches, plus the SPDIF 75 Ω path, are the
first-routed nets on this board.

**Placement may fill the space in front of fine-pitch pads**
*Correction:* reserve an escape corridor in the **placement** stage. Without it the packer parks
decoupling caps where the differential pairs must escape, and the failure only surfaces during
routing.

**An obstacle model built from pads sees the whole board**
*Correction:* it must also read existing **tracks and vias**, or each pass is blind to the copper
the previous pass laid down. Symptom: violations between objects the tool itself created, always
at pass boundaries, never within a pass.

**Grid quantization is a rounding detail**
*Correction:* rounding to nearest lets an obstacle be modelled **smaller than it is**. Round
**outward** — floor the low edge, ceil the high edge, inflate discs by the cell diagonal — and use
`ceil` for dilation radii.
*The tell:* clearance violations whose actual value is just under the rule (0.1485 against 0.150).
Systematic near-misses are a model error, not luck.

**Geometry checks can ignore layers**
*Correction:* a bottom-layer trace obstructs nothing on the top layer. A layer-blind check will
confidently name an innocent object as the blocker.

**A bare `except: pass` around an API call is harmless**
*Correction:* if the call raises on *every* invocation, the fallback is not a fallback — it is the
only path. A silent fallback that fires 100 % of the time is indistinguishable from a working call.
If an except branch substitutes defaults, it must **count and report** how often it fires.

**Bool-returning API calls succeed**
*Correction:* several EDA scripting calls report failure as a **return value**, not an exception.
An import that silently returns `False` looks exactly like one that did nothing. **Check the
return value of every one.**

**A footprint needs only a reference, value, position and pads**
*Correction:* without a library id it exports to Specctra as `(component "")` and the returned
session can never be matched back — the import fails silently. Always set a proper FPID on
programmatically created footprints.

**More autorouter passes means a better result**
*Correction:* a good autorouter self-terminates on its own convergence criterion. Forcing 3× the
passes produced a *worse* result. When it stops improving, the limit is placement and topology,
not effort.

**"The search found nothing" is a fact about the board**
*Correction:* it is a fact about **the search**. A coarse lattice sampled six points under an
exposed pad, hit routed traces at every one, and reported no room for thermal vias — a fine scan
found fifteen.

---

## 6. Decision log

| ID | Date | Decision | Evidence tier | Reopens if |
|---|---|---|---|---|
| DL-01 | 2026-08-15 | Install the constitution before board details, with unknowns marked ⬜ UNSET rather than defaulted | Operator instruction | Operator asks for provisional defaults instead |
| DL-02 | 2026-08-15 | G0 (intake) gates G1–G7 | Reasoning from `CLAUDE.md` §5 | — |
| DL-03 | 2026-08-15 | Do not infer the EDA tool from the template's KiCad references; hold at T3-01 pending Q6 | `CLAUDE.md` §0 | Operator states the tool |
| DL-04 | 2026-08-15 | **G0 split into G0-S (schematic intake) and G0-L (layout intake).** Capture proceeds on the electrical architecture; layout waits for mechanical and fab | T2-10 | A mechanical or fab constraint arrives that changes part selection, not just placement |
| DL-05 | 2026-08-15 | `REQUIREMENTS.md` v0.1 committed to the repo verbatim as the §3 requirements authority; findings logged in §7 rather than corrected in place | `CLAUDE.md` §3 | — |
| DL-06 | 2026-08-15 | The five §11 delegated decisions run **closed book** — decide, justify against stated intent, log, surface in G7. Everything else holds pending Q2 | `REQUIREMENTS.md` §11 | Q2 answers "channel open" |
| DL-07 | 2026-08-15 | Impedance targets **proposed** as 75 Ω SPDIF / 90 Ω USB diff and recorded as T2-04, **not** entered as a constraint, pending Q35 | `CLAUDE.md` §0 | Operator decrees targets |
| DL-08 | 2026-08-15 | No datasheet parameter enters the schematic from memory; §8 checklist governs | `CLAUDE.md` §8 rule 9 | — |
| DL-09 | 2026-08-15 | **Units are mm.** Chosen, not assumed: KiCad is nm-internal and mm-native, every datasheet in this BOM is mm, and the only imperial dimension in the requirements is the 0.1" header pitch = exactly 2.54 mm, which lives inside a footprint | T1-05 + `REQUIREMENTS.md` §4/§11 | Operator prefers imperial, or a mechanical drawing arrives in inches |
| DL-10 | 2026-08-15 | **G2 proven by `--severity-exclusions` returning empty**, not by a baseline file diff — the CLI exposes it directly on both DRC and ERC | T1-08 | A KiCad update changes the flag's semantics |
| DL-11 | 2026-08-15 | Project-local KiCad symbol/footprint library is the default structure; stock libs used where they cover the part | T1-09 | Operator mandates a vendor library service |
| DL-12 | 2026-08-15 | `REQUIREMENTS.md` advanced to **v0.2** under operator disposition of F1/F2/F5/F7/F8/F9/F10/F14, with a revision history rather than silent edits | `CLAUDE.md` §4 | — |
| DL-13 | 2026-08-15 | KiCad 10 CLI/API treated as T2-from-memory, T1-only-from-`--help`; verified before scripting | Ledger, this session | — |
| DL-14 | 2026-08-15 | **Footprint policy:** vendor verbatim → IPC-generated → hand-built last. Adversarial rasterise-over-datasheet verification logged per part; operator personally checks the 5-part respin set | Operator proposal, adopted | A vendor pattern is found to disagree with its own datasheet — then the datasheet wins and the finding is logged |
| DL-15 | 2026-08-15 | **git initialised**; library in-repo, not a submodule; generated output untracked but delivered fab packages committed against a tag | Operator, T1-D38 | A second board shares the library — then reconsider the submodule |
| DL-16 | 2026-08-15 | `REQUIREMENTS.md` → **v0.3** under operator disposition of F6, F11, F16 and Q38 | `CLAUDE.md` §4 | — |
| DL-17 | 2026-08-15 | **Semiconductor shunt mute is the default**, relay must justify itself — decided by the §7.4 zero-energy requirement, **not** by THD. Depletion-mode/JFET topology; part deferred to V-14/V-15 | T1-D34/D35 | V-14/V-15 show no part meets both mute depth and off-capacitance — then energised-to-unmute relays return, with the +5V_D budget consequence |
| DL-18 | 2026-08-15 | Rail monitoring on an ADS1015-class I2C ADC rather than the SoC ADC — also returns ~3 GPIO to the F13 budget | T1-D36 | — |
| DL-19 | 2026-08-15 | **DL-17 superseded: series–shunt mute.** Enhancement-mode series photoMOS + depletion-mode shunt pair, each fail-safe in its own polarity. Relays now out on merit, not on burden of proof | T1-D40, operator correction of an assistant over-generalisation | V-14/V-15 show the series part cannot meet the voltage rating, or the shunt Coff fails T1-D42 |
| DL-20 | 2026-08-15 | **CCIF twin-tone IMD added to §12**, not substituted for the 1 kHz THD line — the failure mode needed a different *test*, not a tighter *number* | T1-D42, ledger corollary | — |
| DL-21 | 2026-08-15 | Board named **ODSP-12** / `ODSP12-MB-A`; fab revisions A/B/C with the change log in git rather than rev-suffix proliferation | T1-D44 | — |
| DL-22 | 2026-08-15 | V-01 expanded to a **single-pass ADAU1466 read** covering V-07, V-08, V-13 and the firmware contract (safeload register addresses, slave-boot header format) | Operator | — |

---

## 7. Findings register

Discrepancies, gaps and risks found in `REQUIREMENTS.md` v0.1. Per `CLAUDE.md` §3 these are
**logged, not silently reconciled**. Disposition is the operator's.

**Severity:** ⛔ blocks capture · ⚠ affects capture · ▫ affects layout or later · ✅ **closed by
operator disposition** (folded into `REQUIREMENTS.md` v0.2 — rows kept, never deleted).

**18 of 24 closed** 2026-08-15: F1, F2, F3, F5, F6, F7, F8, F9, F10, F11, F14, F16, F17, F18,
F19, F20, F21, F22 — the last five dispositioned into `REQUIREMENTS.md` v0.5.
**Six open: F4** (impedance, layout), **F12**, **F13** (capture), **F15**, and two new from the
second datasheet sweep — **F23** (AKM I2C address space may be too narrow) and **F24** (LT3045
input rails unspecified; +5V_A cannot come from +5V_D).

| ID | Sev | Finding | Proposed disposition |
|---|---|---|---|
| **F13** | ✅ | **CLOSED 2026-08-16 — all three module-level checks answered from the module datasheet, and one of them turned out to be load-bearing.** **(a)** IO35/36/37 free on the N8R2 (T1-95) — the octal-PSRAM reservation applies only to R8/R16V. **(b)** Strapping pins are GPIO0/3/45/46 (T1-96); nothing that drives during reset is on any of them, and each gets a **deterministic idle level** rather than inheriting an internal weak pull — including **GPIO3, which has no internal default at all**. **(c)** GPIO19/20 carry USB D± and nothing else; the stock symbol names those pins `USB_D-`/`USB_D+`, so the [HARD] reservation is visible on the sheet rather than living in a comment. | **The (a) result is why F38 exists.** Three power-good sense lines now sit on IO35/36/37, so ordering an R8 or R16V variant does not degrade performance — it shorts three nets into the PSRAM bus. The suffix is a **pinout**, not a stocking preference, and that sentence is on the sheet |
| **V-30** | ⛔ | **NEW — the USBLC6-2SC6 pin map is T2 and I could not make it T1.** It is taken from KiCad's `USBLC6-2P6` parent symbol, **not from ST's datasheet**, which st.com would not serve to this environment (unlike vishay.com — see T1-92, that claim was retracted after one retry, so this one is recorded as *tried and failed*, not *unreachable*). **Low risk and not exempt:** the part is symmetric on I/O1/I/O2, so only GND (2) and VBUS (5) are orientation-bearing — but CLAUDE.md §8 rule 9 has no low-risk clause, and a swapped GND/VBUS on an ESD array is a part that clamps to the wrong node. | Fetch `USBLC6-2SC6` from st.com by the manual route, or accept an alternate ESD array whose datasheet is reachable. **Not blocking** — it is one 6-pin part on a debug port |
| **F45** | ⚠ | **UPDATED 2026-08-16 — the retraction stands, but the decision it reopened has collapsed into an improvement.** Doc 98647 (the successor) **also says "Unidirectional"**, and covers the unidirectional series only. So a bidirectional `SM8S..CA` would be a **separate document that is not held**: the operator's distributor evidence keeps it **unverified rather than disproven**, which is precisely the distinction M12 exists to preserve. **Two things dissolved the staged asymmetry:** the uni's real clamp is **38.9 V at 170 A**, which clears the LM61460's 42 V absmax *even at full rated current* — so the M10 dynamic-resistance argument is comfort for the uni, not load-bearing, and the CA's advantage there evaporates. And the **6600-vs-5200 framing was never a polarity split**, so the uni's case never rested on it. **Disposition, closed-book:** fit the **evidenced** part. `SM8S24AHM3` is fully T1 and passes §12; the CA remains a cheap, reversible improvement worth taking if its document ever lands, since **the land pattern is identical and the swap is a value change, not a respin.** The thermal elimination of D2-behind-Q2 is polarity-independent and permanent. *Original text below.* |
| ~~**F45-orig**~~ | | **F44's premise (b) is RETRACTED, and the retraction restores a design route I had eliminated.** `SM8S24CA` **does exist**: the HM3-era catalogue carries a parallel bidirectional series, **SM8S10CA thru SM8S85CA**, `SM8S24CAHM3/I` in DO-218AB, 5200 W, 24 V standoff / 26.7 V min breakdown / 38.9 V clamp at 170 A, AEC-Q101, distributor-stocked. My "unidirectional polarity only" was read from the **NRND** document, where it is true of *that* family — see **M11**. **The consequence is the expensive kind: I eliminated an available option, and a wrongly-eliminated option is normally never revisited.** It was caught only because the operator's distributor evidence was already HM3-era. | **The direction question reopens — but only halfway.** The **thermal elimination is permanent and polarity-independent**: D2 *behind* Q2 routes 48 A for 400 ms through the FET (~117 W, ~176 °C rise) whatever is clamping, so that branch stays dead. What revives is **CA ahead of Q2**: reverse battery blocked by the TVS itself so **F1 does not clear and seamless recovery returns**, Q2 as the second line, negative fast pulses clamped at −38.9 V with Q2's body diode holding them off the load, **and F43's assembly-polarity hazard structurally eliminated** because a bidirectional part has no orientation. **Price to be verified, not assumed:** the CA's load-dump capability against the §12 rows. The binding row is the *suppressed* condition, which passes at 3–5× on the uni part. If the CA's M-curves hold comparable margin there, seamless returns **for a one-letter BOM change**; if bidirectional construction gives up long-pulse capability, the uni-plus-fuse-clear resolution stands and the seamless property has been **priced rather than assumed**. **Decision is explicitly downstream of the HM3 read** |
| **F44** | ⚠ | **Two of three premises stand; the middle one was corrected back — by the rule that produced it.** *(b) RETRACTED — see F45.* Premises (a) NRND and (c) the waveform-pair reading are unaffected by the retraction, but see **V-28**: (c) now has three competing readings and none of them is T1. *Original text below.* |
| ~~**F44-orig**~~ | | **Three premises in the F42 decree do not survive the datasheet. The decree's *outcome* stands; two of its stated reasons do not.** **(a) The family is NRND.** `sm8s.pdf` carries a banner on every page: *"Not For New Designs — Alternative Device: SM8S10AHM3 thru SM8S85AHM3."* Pinning `SM8S24A` pins a discontinued part; the target is **`SM8S24AHM3`**, whose datasheet **is not held**, so every figure below is read from the NRND document and inherits a re-verification. **(b) There is no `SM8S24CA`.** The family is *"available in unidirectional polarity only"* (p.1), and the ordering table's position 5 offers only *"A — ±5 %, unidirectional."* **The operator's preferred route — a bidirectional CA ahead of Q2 solving four constraints at once — does not exist in this family.** **(c) The 6600 W / 5200 W pair is not uni-vs-bi**; it is the two *waveform* ratings of the same unidirectional part, 10/1000 µs and 10/10 000 µs (p.1 Primary Characteristics). Ordinary misreading of adjacent table rows — the same shape as T1-25/T1-28 on my side, logged symmetrically. | **`SM8S24AHM3` pinned**, F38 line added: **the `H` is AEC-Q101** and this part faces the harness, so §7.0 requires it — dropping the suffix silently buys industry grade (the F37 shape again). **The AHM3 datasheet is the next manual-fetch ask.** The CA route being unavailable is what forces F42's direction answer below |
| **F42** | ✅ | **CLOSED — SM8S24AHM3 ahead of Q2, and the scope is now a capability statement backed by the table.** The decree's substance survives intact: same 24 V standoff, same 26.7 V minimum breakdown, same 38.9 V clamp, in a 6600 W DO-218AB body with a molded heatsink. **The consequence-check fired and confirmed** — Q1 stays at 68 % of its 80 V rating, not 92 %. **Direction, worked closed-book and derived rather than asserted:** D2 must sit **ahead** of Q2. Behind it *would* give seamless reverse (Q2 blocks, D2 sits unbiased) — but then the entire clamp current flows **through Q2**: at Us 79 V / R<sub>i</sub> 1 Ω that is **48 A for 400 ms**, ~117 W at hot R<sub>DS(on)</sub>, ~176 °C rise in a D2PAK. **Q2 is destroyed.** The seamless property costs the FET, so it is not bought: **reverse battery is a fuse-clearing event**, D2 forward-conducts (V<sub>F</sub> 1.8 V, I<sub>FSM</sub> 700 A/8.3 ms so it survives), and Q2 still earns its place by blocking reverse downstream during the fuse-clear interval. **Capability by the table** (ISO 7637-2 pulse 5 is Us = **65–87 V**, R<sub>i</sub> 0.5–4 Ω, 400 ms — Vishay 88490 Table 1; the 35 V figure was the *suppressed* level only), against P(400 ms) = (175 − T<sub>mount</sub>)/0.30 from Fig. 6: **suppressed Us\* 35 V → 95 W, passes 3–5×; unsuppressed 79 V/4 Ω → 362 W, passes cold and marginal hot; 79 V/2 Ω → 732 W, exceeded; 87 V/0.5 Ω → 3631 W, exceeded 7–12×.** **The board is specified for centrally-suppressed load-dump vehicles** — bounded, evidenced, and now in §12 rather than implied. | **One correction to my own earlier alarm, worth keeping:** I had the clamp threatening the bucks. It does not. Using the **dynamic resistance** r<sub>d</sub> = (38.9 − 28.1)/170 = **63.5 mΩ** rather than the 38.9 V headline, the worst realistic clamp is **34.2 V** (48 A, T<sub>J</sub> 150 °C) against the LM61460's 42 V — **7.8 V of margin**. The headline is the clamp at 170 A, a current this circuit never reaches; taking it at face value and adding tempco says 44 V and condemns a sound design. *A worst-case number quoted outside its test condition is not conservative, it is wrong.* |
| ~~**F42-orig**~~ | | **The SMBJ24A analysis that started it, and the design has never said it doesn't have to.** Standoff axis is fine: 24 V clears 16 V max operating and a 24 V jump start, which is evidently what the part was sized for. **The energy axis fails by 40–165×.** A suppressed load dump (ISO 16750-2, Us\* = 35 V, t<sub>d</sub> = 400 ms, R<sub>i</sub> = 0.5–4 Ω) sits **above** the 26.7 V breakdown, so the TVS conducts for the whole 400 ms: at R<sub>i</sub> = 2 Ω holding ~31 V that is 2 A × 31 V = 62 W → **24.8 J**; at 0.5 Ω, 250 W → **100 J**. The part is rated 600 W for 1 ms = **0.6 J**. It is destroyed, and the fuse then clears. **So the board as drawn makes an unstated claim — "no load dump reaches this input."** That may well be true and defensible for a suppressed-load-dump vehicle, but it is a scope statement, not a default, and it is currently written nowhere. **This is exactly the shape of the standing-exception problem §0 exists for**: a value that looks specified because a part number is present. | **Operator's call, three rungs.** **(a) Declare the scope** — state in §12 and the G7 note that the design assumes centrally-suppressed load dump, keep SMBJ24A, and accept that a raw dump is a fuse-and-TVS sacrificial event. Cheapest, honest, and probably correct for the target vehicle. **(b) Raise the standoff to ~36 V** (SMCJ36A, 1500 W) so the TVS *does not conduct* at 35 V and the converters ride it on their own ratings — LM61460-Q1's recommended max is 36 V, so 35 V is inside it, but the clamp rises to 58.1 V and **that propagates**: SEPIC switch stress becomes 73.6 V, putting the pinned 80 V FET at 92 % of rating. **(c) Active transient blocker** (LTC4364 / TPS2660 class) — correct at any severity, and a new part class plus board area. **Note the footprint is already DO-214AB (SMC)** so (b) stuffs without a respin. Numbers are **T2 — three agreeing distributor listings, no manufacturer PDF**; st.com and vishay.com both refused this environment, so the SMBJ/SMCJ datasheet is a second manual-fetch ask alongside the LT3094 |
| **F43** | ✅ | **CLOSED in the drawing — `Device:D_TVS` is the BIDIRECTIONAL symbol and would have been wrong for this part.** Its pins are named **`A1`/`A2`** — two anodes, no cathode. The SMBJ24**A** is unidirectional (**CA** is the bidirectional member), and its polarity is load-bearing in both directions: cathode-to-battery is what clamps positive transients *and* what lets it forward-conduct negative ones. A polarity-blind symbol on a polarity-critical part hands assembly a coin flip, and **a unidirectional TVS fitted backwards across a 12 V battery is a dead short, not a degraded clamp.** | Drawn with `Device:D_Zener` (K/A), which is what a unidirectional TVS physically is, with the reason on the sheet so it is not "corrected" back to the TVS symbol by someone tidying up. **Generalises with M8:** the stock library's naming does not distinguish the variant your BOM line names |
| **F41** | ✅ | **CLOSED, fixed and made unrepeatable — a silent three-way short that every assertion passed.** Growing `TESTPOINTS` from 10 to 14 pushed the label grid onto a third row at y = 254 mm, which is the U2 buck's passive row. Three pairs of global labels landed on identical coordinates and **merged into single nets: `+5V_D`+`+15V5_A`, `GND`+`+13V5_A`, `U2_CBOOT`+`−15V5_A`.** Connectivity on this sheet is by global label at a pin endpoint, so a shared coordinate *is* a short. **Nothing caught it:** the symbol pin-set assertions passed, the F28 pin-coverage assertions passed, the device count was right, and ERC was unremarkable — the only visible symptom was the netlist reporting the DSP's ground pins as members of `+13V5_A`. **This is M6 exactly: a completeness check sees omission, never collision.** | **Fixed two ways.** Testpoints moved to their own column at x = 700, clear of every device row — the old layout interleaved them with passives, which is what made it possible. And a **`LABEL COLLISION` assertion** now guards every emitted label: two different nets at one coordinate is a build failure. **Negative-tested** — the assertion was made to fire before being trusted (M5: a check that has never fired has not been checked). Net count 136 → 139 |
| **F40b** | ▫ | **Forward note, pre-empting the wrong question at V-17 closure** *(operator, 2026-08-16)*. When V-17 lands, the question is **not "what value"** but **whether to program a limit at all.** Programmable `ILIM` earns its resistor in current-sharing arrays and in load-fault isolation, and **these rails have neither** — each LDO feeds one domain, and a fault there is not a fault to be isolated from anything. The internal limit plus thermal foldback is very likely the permanent answer. Recorded now specifically to head off the *"surely we should set it to something"* instinct arriving with the new number. | Decide at V-17 closure; a decision either way goes in the G7 note |
| **F40** | ✅ | **CLOSED, corrected in place — every LT3045 on the sheet was programmed to a 7.5 mA current limit.** All five carried `R_ILIM = 20 kΩ`, a placeholder that was never run through the scale factor. T1-82: **`Current Limit = 150 mA·kΩ / R_ILIM`**, so 20 kΩ = **7.5 mA** against rails budgeted 15 mA (+3V3_PLL) to ~100 mA (+3V6_BT, feeding a radio). **Every analog rail on the board would have current-limited into collapse**, and the failure would have presented as "the converters and the Bluetooth module don't work" — a bring-up week. **The tell is M7 again: the value was plausible, the *consequence* was not**, and the consequence is checkable against a budget already written down. Same shape as the `RT` error, and found the same way — by running a recorded constraint against the artefact rather than re-deriving anything. | **`ILIM` ties to GND on all five**, which is the datasheet's own disposition when the programmable limit is unused, leaving the internal limit to govern. **Deliberately not re-programmed to a "correct" value:** V-17 (AKM AVDD currents) is still open, and a limit set against an unknown load is the same mistake wearing a better number. Revisit when V-17 closes. **Sibling trap logged:** the LT3094's scale constant is **3.75 A·kΩ**, 25× different — the two parts do not share this arithmetic |
| **F39** | ✅ | **CLOSED — decreed on arrival, 2026-08-16, and drawn.** See the original entry below for the proposal. Built as specified with two operator amendments: **V-26 decree — `DITHOFF` fitted, dither OFF** on the SEPIC (populated leg to VCC, DNP leg to GND), so the AM-band clearance rests on the specified f<sub>SW</sub> floor of 1980 kHz rather than on an unstated deviation; and the **fail-order property promoted out of this block** into §7's rationale. Amended on evidence during the draw: **the two rails are not symmetric.** T1-81 — the LT3094 peaks at 100 kHz where the LT3045 peaks at 2 MHz, so the negative rail sees **72 dB at 2.2 MHz, not 84**, and its budget lands at **4.5 µV<sub>RMS</sub> (21 dB margin)** against the positive rail's 2.0 µV<sub>RMS</sub> (28 dB). Both clear the [HARD] 50 µV<sub>RMS</sub>; the asymmetry is now on the sheet. **Devices: U13 LM5156-Q1 SEPIC · U14 LM61460-Q1 IBB · U15 LT3045 · U16 LT3094** | — |
| ~~**F39-orig**~~ | |  **NEW — ±13V5_A topology proposal, built against the four criteria published in advance.** *Awaiting disposition; nothing drawn yet.* **Recommendation: SEPIC → +15V5_A from VBATT_PROT; inverting buck-boost → −15V5_A from +15V5_A; LT3045 / LT3094 post-regulators to ±13V5_A.** **The cascade is forced, not preferred** — an IBB stresses its regulator at V<sub>IN</sub> + \|V<sub>OUT</sub>\| (T1-79 §4.1), so on VBATT_PROT an LM61460-Q1 sees ≥ 26.7 + 15.5 = **42.2 V the instant the TVS conducts at all**, past its 42 V abs max (T1-74). That exclusion holds without knowing the clamp voltage, because any 12 V-system TVS breaks down above 26.5 V. Fed from the regulated +15V5_A it sees a **fixed 31 V**. Likewise a plain boost on the positive rail is rejected on TI's own sentence (T1-77): it passes the input straight through when V<sub>OUT</sub> ≤ V<sub>IN</sub>, putting a clamped load dump on a 20 V LDO. **f<sub>SW</sub> = 2.2 MHz on both stages**, chosen on three independent legs — T1-71's PSRR notch at 500 kHz–1 MHz vs 84 dB at 2 MHz; T1-76's dither tone at 0.156 × f<sub>SW</sub> = 343 kHz rather than 15.6 kHz; and no harmonic below the fundamental, so nothing lands in the AM band. **Budget: ≈ 2.0 µV<sub>RMS</sub> against 50 µV<sub>RMS</sub>, 28 dB of margin**, and it is carried by the LDO's *audio-band* PSRR (100–117 dB) rather than by f<sub>SW</sub> — which is why the unspecified pulse-skip onset (V-27) cannot break it. **Honest cost:** the SEPIC carries both rails, ≈ 8.5 W, ~1.65 A input at crank; independent stages would be half that each. **PNs:** LM5156-Q1 · LM61460-Q1 (fourth instance) · LT3045 · **LT3094 (T2 — datasheet not held)** | **Operator disposition against criteria (a)–(d).** One ask attached: the **LT3094** datasheet, via the same manual route used for the ADAU1466 and LT3045 (T1-15). The negative post-regulator is the only part in the block chosen from memory rather than a document. If LT3094 is not the 500 mA negative sibling it is believed to be, the fallback is 2× LT3093 in parallel — **LT3093 alone is 200 mA and does not cover the 250 mA peak** |
| **F1** | ✅ | **CLOSED — operator accepted, v0.2 §3 amended, AK4118A removed from the slaved-port list; V-02 closed by T1-10.** → T1-D26. *Original finding:* **clock architecture contradiction, [HARD] vs [HARD].** §3 bullet 2 lists "AK4118A output port" among the ports for which the ADAU1466 generates BCLK/LRCLK — i.e. the AK4118A as I2S slave. §3 bullet 3 requires its recovered clock to stay out of the system tree, with the ASRC downstream. **These cannot both be built.** A SPDIF receiver reconstructs audio at the *source's* rate; the AK4118A has no internal SRC. Clocked as a slave to our 48 kHz while receiving 44.1 kHz, it slips samples — and the downstream ASRC sees a perfectly synchronous input and corrects nothing, because the corruption already happened upstream of it. Directly threatens §12's "SPDIF lock across 32/44.1/48/96 kHz". | **AK4118A is clock master on that link**; ADAU1466 SDATA_IN2 is a clock *consumer of that port only*; ASRC does 44.1→48. This is exactly the shape §3 already prescribes as the BM83 fallback, and it **preserves bullet 3's intent** — the recovered clock terminates at the ASRC boundary and never reaches the system tree. Needs operator sign-off as a [HARD] change. T2, pending V-02/V-03. |
| **F2** | ✅ | **CLOSED — 2× INA1650, v0.2 §2 corrected** → T1-D27. *Original:* **INA1650 quantity.** §2 says "4× INA1650" with "2ch/pkg". Four differential inputs at two channels per package is **2** packages, not 4. | Q29. Most likely a channel count in a package-count column (T3-03). Affects BOM, cost, area. |
| **F3** | ✅ | **CLOSED — mm, DL-09.** *Original:* **Mixed units.** mm for the board envelope (§11), 0.1" for test headers (§4). | Q10. Pick one file unit, convert at the footprint. `CLAUDE.md` §7. |
| **F4** | ⚠ | **No controlled-impedance targets stated**, though the board carries coax SPDIF and USB. | T2-04 / Q35: 75 Ω SPDIF, 90 Ω USB diff. Both antennas are module-integrated, so no 50 Ω trace work. |
| **F5** | ✅ | **CLOSED — −20…+70 °C, not an AEC-Q board; AEC-Q100 follows exposure not product category. New v0.2 §7.0** → T1-D28. *Original:* **no operating temperature range or AEC-Q grade.** §7.1 requires AEC-Q100 on battery-facing regulators but never says Grade 1 (−40…+125 °C), Grade 2 (−40…+105 °C), or commercial elsewhere. Parts cannot be selected without it — and the AKM converters and OPA1656 are not automotive-qualified parts. | Q36. Note the tension with §2's TI substitutes: PCM1690 is called out as AEC-Q100 while the AKM primaries are not. |
| **F6** | ✅ | **CLOSED — FCC Part 15 Class B practices, no chamber for v1, CISPR 25 out of scope; new v0.3 §7.5** → T1-D37. Note the useful clarification it forced: **spread-spectrum stays on for the bucks**, because §3's prohibition covers the audio clock tree only and those are different nets. *Original:* **no emissions requirement.** Automotive product, two 2.4 GHz radios, several switching regulators, and no CISPR 25 class or equivalent stated. Filtering, shielding and stitching decisions are made at layout and are a respin to retrofit. | Q37. |
| **F7** | ✅ | **CLOSED — ±13V5_A at 200 mA cont / 250 mA peak per rail** → T1-D30. Mute rail still unbudgeted → Q38. *Original:* **no per-rail current budget.** §7.1 names loads but no currents. The ±13V5_A topology choice is delegated to us (§11) and cannot be sized without it. | Q31. First-pass estimate: 24 OPA1656 channels at ~4 mA quiescent ≈ 95 mA, plus signal current, which is small into 10 kΩ. |
| **F8** | ✅ | **CLOSED — divider ahead of the switch element, v0.2 §6.1** → T1-D31. *Original:* **speaker-level range switch sees ~42 V peak.** §6.1 permits "relay or analog switch" for a 30 Vrms full-scale range. Common analog switches will not survive ±42 V. | Constrain the topology: the divider must sit **ahead** of the switch so the switch only ever sees attenuated signal — or use a relay. Either way it is a capture-time decision, not a layout one. |
| **F9** | ✅ | **CLOSED — 0.1 % matched attenuator resistors on the BOM as a requirement, v0.2 §6.1** → T1-D31. *Original:* **CMRR ≥ 60 dB is a resistor-matching requirement, not an amplifier one.** In speaker mode the attenuator's own leg-to-leg mismatch sets it; the INA1650 has far more rejection than the ladder in front of it. | T2-08: implies ~0.1 % or better matching. Budget matched networks or 0.05 % parts. Do the tolerance analysis before the BOM is frozen. |
| **F10** | ✅ | **CLOSED — v0.2 §10 states it explicitly: AOUT7–12 = AK4458 #2 slots 1–6; net names follow the system channel number** → T1-D32. *Original:* **channel-to-slot naming ambiguous for AOUT7–12.** §10 says channel numbers match the §4 slot map with no remapping [HARD], but AOUT7 lands on **AK4458 #2 slot 1**. "Match" is therefore true of the logical output index and false of the per-device slot index. | State it explicitly once, in the schematic and the G7 note: AOUTn ↔ (device ⌈n/6⌉, slot ((n−1) mod 6)+1). Cheap to fix now; expensive if a netlist is built on the other reading. |
| **F11** | ✅ | **CLOSED, and it turned out to decide the topology.** Working the current budget surfaced the §7.4 zero-energy requirement, which ruled out latching relays outright and reversed the burden of proof onto the relay option → T1-D34/D35, DL-17, new v0.3 §6.4. *Original:* **twelve mute relays is a real load and a real area cost.** §6.2 prefers relays for zero distortion. At ~25–40 mA per coil that is roughly **0.3–0.5 A** on the mute rail, plus 12 footprints. | Feeds Q31 and Q26. Consider latching relays (drive current only during transition) — but note they hold state through a rail collapse, which interacts with §7.3. |
| **F12** | ⚠ | **Output-stage gain is unstated but forced.** T2-05: ~13 dB is needed to reach 4.5 Vrms from the DAC's differential full scale, which multiplies DAC-referred noise by ~4.5× against the §12 noise floor of −105 dBV. | Not a conflict — a budget to check explicitly before committing the filter topology. |
| **F13** | ⚠ | **ESP32-S3-WROOM-1 N8R2 GPIO availability.** The 22–24 GPIO budget (T2-07) assumes the module's exposed pins are all usable. Flash/PSRAM variants consume internal GPIOs and several exposed pins are strapping pins with boot-time level constraints. | **Still open, but now scoped to three specific checks** (operator input, 2026-08-15) — do them against the **module** datasheet, not the SoC datasheet: **(a) GPIO35/36/37** — consumed by octal PSRAM on R8-suffix modules; the specified **N8R2 is quad PSRAM so they should be free, verify**. **(b) GPIO0/45/46** — strapping pins, usable but constrained at boot; hang nothing on them that drives during reset. **(c) GPIO19/20** — already reserved for USB per §5. T2-07's budget dropped to ~21 after F16 moved rail sensing to I2C, which buys margin here. |
| **F14** | ✅ | **CLOSED — OPA1656, decided; alternate dropped from v0.2 §2 and §6.2** → T1-D29. *Original:* **"OPA1656 (or OPA1612)" is not a substitution.** JFET vs bipolar input: different noise optima, different source-impedance sweet spots, different bias-current behaviour through the filter network. Same package is not the same design. | Q33. Pick one before capture; the filter resistor values follow from it. |
| **F15** | ▫ | **MCLK and BCLK/LRCLK reach the converters by different paths** — MCLK direct from the XO fanout, BCLK/LRCLK through the ADAU1466 PLL. Frequency-coherent (T2-09), but AKM parts in TDM slave mode have specific MCLK/LRCK synchronisation requirements. | Sharpens the doc's own [VERIFY] (V-04). If the parts require phase-locked MCLK, the fanout topology may need to change. |
| **F38** | ⛔ | **NEW, F37's general form: an argument that depends on a part *option* must pin the orderable PN, not the part family.** F37's failure mode is that **the board works on the bench with the wrong variant while the argument evaporates silently** — a bench cannot detect an absent option whose job is regulatory or statistical. Only BOM discipline can. **Sweep required: every BOM line where a suffix changes behaviour gets its PN pinned with a one-line why.** Known option-sensitive lines so far: **(1)** LM61460 — SS-enabled variant, or F35/Q37/the sync non-action all collapse (F37). **(2)** ADAU1466 — the ordering guide lists **six** models; `WBCPZ300` is ours (1462 vs 1466 = memory, 150 vs 300 = core MHz, `RL` = tape-and-reel). **[VERIFY]** before one is picked by autocomplete. **(3)** ESP32-S3-WROOM-1 **N8R2 specifically** — the F13 GPIO analysis assumes **quad** PSRAM; an **R8** octal module consumes GPIO35-37 and breaks it. **(4)** BM83SM1 — firmware variant / config state per F32. **(5)** TPS6282x — the family spans **1 A / 2 A / 3 A** by suffix. **(6)** AK4458**VN** / AK5574**EN** — suffix is package. **(7)** TMP461 address-strap variant — **V-20 folds into this sweep** rather than running separately; same deliverable, PN plus the why against the §9 bus map. **(8)** AP2127K-**ADJ** — **the `ADJ` suffix is the load-bearing option**; the fixed-output members of that same family are **the MIC5504 trap wearing a different logo** (F36), so this line is pinned for exactly the reason F36 exists. | **Eight lines.** Run as a single sweep when the BOM is first emitted, not per-part as they come up. **The one-line why is the deliverable**, not just the PN — a pinned number with no reason attached gets "optimised" by the next cost pass exactly like an un-pinned one, and the cost pass then inherits the argument along with the number |
| **F37** | ⛔ | **NEW. Spread-spectrum on the LM61460 is a FACTORY OPTION, not a universal feature.** *"Spread spectrum is a factory option. To find which devices have spread spectrum enabled, see Section 6."* The entire Q37/F35 emissions posture — SS permitted on the power stages, SS decorrelating the two bucks, SS smearing harmonics — **assumes SS is present.** Order the wrong orderable part number and every one of those arguments silently evaporates while the board still works on the bench. | **The orderable PN must be chosen from the SS-enabled variants and pinned in the BOM with a note saying why.** This is not a preference; three separate design arguments rest on it |
| **F36** | ✅ | **CLOSED — adjustable LDO, divider-set to 3.6 V.** The F31 intent was *small, cheap, transient-friendly, ~140 mW*, and that intent picks the replacement rather than the named part. **`AP2127K-ADJ` is the target** (stock symbol exists, correct economy class); the LT3045 stays on the sheet marked **PROVISIONAL only until the divider is computed**, then comes off entirely. **The LT3045 is the wrong *grade*, not merely the wrong price:** `BAT_IN` feeds the BM83's own internal regulation, so reference-grade PSRR here buys quiet the module immediately re-regulates away. **[VERIFY] V-23:** AP2127K-ADJ's FB reference and tolerance, stacked with divider tolerance, landing inside 3.2-4.2 V — trivially true across a 1 V window, but the arithmetic goes on the sheet where the inequality lives. **Sheet annotation required:** a divider on an **FB** pin is correct and designed-for; this must not be misgeneralised from the INA1650 **REF** rule. *The distinction: FB is a feedback input inside a loop that regulates it; REF is a reference input that believes whatever it sees.* | — |
| ~~**F36-orig**~~ | | **The MIC5504-3.3 near-miss, rejected properly.** ±2 % is the **initial accuracy term only**. Stack line regulation, load regulation, temperature drift and trace drop, and the real minimum at the BM83's pin sits **meaningfully below 3.234 V** — so it does not reliably clear the 3.2 V floor at all once the error budget is honest. "Clears on tolerance alone" was the right rejection; this is the version that survives scrutiny. *Original:* **the decreed part class cannot reach 3.6 V.** MIC5504 is **fixed-output only** — stock variants run 1.2 / 1.8 / 2.5 / 2.8 / **3.3 V max**, with no 3.6 V option. The F31 decree named "AP2112/MIC5504-class at 3.6 V", and that combination does not exist in the MIC5504 line. **An LT3045 stands in provisionally on the sheet** (adjustable via `SET`, already in the BOM three times, and its transient behaviour suits a radio) — **marked PROVISIONAL in the Value field, not silently substituted.** | Operator's call: an **adjustable** small LDO (TLV757P / AP7361 class), a different fixed-3.6 V part, or accept the LT3045 on BOM-consolidation grounds. Worth noting the near-miss alternative: MIC5504-3.3 at ±2 % gives 3.234-3.366 V, which **does** clear BAT_IN's 3.2 V floor — but on tolerance alone, with no margin, which is the kind of "it fits" that F31 already rejected once |
| **F35** | ✅ | **CLOSED — split kept. XO→DSP direct, three buffer outputs, `Y3` spare.** The equalisation argument dissolves on inspection: the converters care about BCLK/LRCLK skew **relative to each other**, and those are regenerated by the DSP's serial ports from the PLL — not from MCLK's arrival time. Matching the DSP's MCLK path equalises a delay **nothing downstream can perceive**. The cost side is asymmetric and real: the PLL reference is the root of every clock on the board, so jitter there multiplies through the PLL into everything, while the same jitter on a converter leg touches one device. **When one side of a trade is "no benefit", the error bar on the other side is irrelevant.** `Y3` disposition per datasheet: **"Unused outputs can be left floating"** — annotated as *datasheet-sanctioned*, explicitly not a convenient future tap. *Original text below.* | — |
| ~~**F35-orig**~~ | | *Original:* **observation. The clock buffer has exactly one more output than §3 currently uses.** T1-66: the LMK1C1104 has **four** outputs. §3 routes the XO **directly** to the ADAU1466's MCLK and puts only the three converters behind the buffer — which leaves `Y3` spare and gives the DSP a *different* path from every device it clocks. Driving all four from the buffer (`Y0`→DSP, `Y1`→ADC, `Y2`→DAC1, `Y3`→DAC2) equalises loading and propagation delay across the whole tree and still satisfies §3's "distribute from the XO through a buffer, not daisy-chained". | **Escalated, not applied** — §3 is [HARD] and this is clock-tree topology. Counter-consideration: it inserts the buffer's additive jitter (7.5 fs) into the DSP's PLL reference, where today the DSP sees the XO raw. That is almost certainly below the PLL's own contribution, but it is the operator's call, not an obvious win |
| **F34** | ⛔ | **NEW, and it is a direct consequence of F33's own fix — stop-the-line.** The ADAU1466 requires **`IOVDD` first**: *"IOVDD… is the reference for the ESD protection diodes situated inside the input and output pins, must be applied first to avoid stressing these diodes."* F33 moves `PVDD` onto the **+6V2_A branch**, a different limb of the tree from `IOVDD` (+3V3_D) — so nothing guarantees their order, and if the analog branch wins the race **PVDD precedes IOVDD and stresses the ESD diodes on every single power-up.** Raised **before** drawing 01_power because it changes the sheet's enable topology, and drawing first would have been work invalidated in flight. | **Gate the PVDD LDO's enable from +3V3_D** (rail or power-good). The shared ancestor becomes a *logic* signal, never a current path, so **F33's noise isolation survives intact — sequencing and noise isolation are separable, and are separated deliberately.** `AVDD` (shares +3V3_D) and `DVDD` (from the +1V2_CORE buck fed by +3V3_D) are safe by construction; **re-parenting either re-opens this** |
| **F33** | ✅ | **CLOSED — dedicated LDO from +6V2_A, and both cheap fixes rejected on their merits.** *Against a +3V3_CLK tap:* the fanout buffer is a pure victim, but **the PLL is a victim and an aggressor** — charge pump and VCO switching current appears across a shared regulator's output impedance and would modulate the fanout's supply, putting the noisiest clock-domain device on the rail built to be the quietest. *Against a ferrite/RC off +3V3_D:* the contamination is **low-frequency** (WiFi TX envelope, hundreds of Hz to low kHz) where a ferrite does nothing and an adequate RC burns headroom out of a ±10 % window. **An LDO's PSRR is strongest exactly where a ferrite is weakest**, and +6V2_A removes the shared ancestor below the battery input. V-21 settles the sizing at **15 mA max → ~44 mW**: any small LDO, MIC5504/TPS7A02 class, not reference-grade. *Original text below.* | Spawned **F34** |
| ~~**F33-orig**~~ | | *Original:* **The DSP's PLL supply is on the digital rail, and the PLL generates every serial clock on the board.** `PVDD` (pin 15) is the ADAU1466's PLL supply, 3.3 V ±10 %. In the current architecture that means +3V3_D — a switcher rail shared with the ESP32's WiFi bursts. **This is F22's argument one level in:** the fanout buffer was moved to a clean rail because its supply noise becomes jitter on every converter, and the PLL that *generates* BCLK/LRCLK for all of them has exactly the same property. | **Escalated, not applied** (rail architecture, `CLAUDE.md` §4). The DSP sheet labels it as its own net **`+3V3_PLL`** so the decision is visible and deferred rather than silently baked into +3V3_D. Cheapest resolutions: an RC/ferrite filter off +3V3_D, or a tap from +3V3_CLK which already exists for exactly this class of problem |
| **F30** | ⛔ | **NEW. AK5574 wake-up silences the entire I2C0 bus — §7.2 step 5 collides with it.** T1-55: after `PDN` release, up to **10 ms** passes before register writes are accepted, and during that window the part may emit spurious pulses on its digital pins. AKM's instruction is explicit and *bus-wide*: **avoid data transmission with any device on the same I2C bus during this period.** Our bus also carries 2× AK4458, ADS1015 and the temp sensor, so "configure the ADC/DACs over I2C" immediately after power-up can corrupt traffic to parts that are themselves fine. **Third instance of the F20 family** — a [HARD] sequence step that omits a device's readiness precondition. | Amend §7.2: after releasing the converters' `PDN`, hold **the whole bus quiet ≥10 ms** (then allow 583/fs ≈ 12.1 ms for initialisation to complete) before any I2C traffic. Escalated as a [HARD] amendment |
| **F31** | ⛔ | **NEW. §7.1 puts the BM83 on +5V_D, but its main supply pin wants 3.2-4.2 V.** T1-56: `BAT_IN` is 3.2-4.2 V; `ADAP_IN` is the 5 V path and is described as an adapter/charger input. **A nominal 3.3 V rail is not a safe answer either** — 3.3 V −5 % = 3.135 V, **below the 3.2 V minimum**. So the options are: feed `ADAP_IN` from +5V_D and accept the module's internal path, or provide a dedicated ~3.6-3.8 V rail for `BAT_IN`, or tighten +3V3_D's tolerance. | Escalated — rail architecture is respin-class. Note this interacts with F19: +5V_D's load shrinks or grows depending on the choice |
| **F32** | ⚠ | **NEW. The BM83 ships in Embedded mode; this design needs Host mode.** T1-57: several pin meanings differ between the two, and the module is *pre-configured* for Embedded. §5's architecture (ESP32 as sole state owner, UART control + transparent data) is Host mode. **The schematic must be drawn against our config, not the datasheet default** — and the config step itself has to exist in the production flow. Pin 31 is also an Application/Test mode strap. | Config-dependent pins carry a `*` in the symbol so the sheet shows which meanings depend on the flashed config. Needs a decision on **who flashes the config and when** — factory-programmed part, or a production step |
| **F28** | ✅ | **CLOSED — policy: no pin leaves the schematic unannotated.** Every unused pin on every part gets an explicit disposition (open / GND / pull) **sourced from that part's own datasheet**, annotated on the sheet. **No board-wide default exists**, because any convention is guaranteed wrong somewhere: "disconnect when not in use" and "must not float" coexist here, and the AK4458 flips *within itself* between analog outputs (open) and digital inputs (DVSS). The DL-14 verification pass gains a check of unused-pin dispositions against each datasheet's own unused-pin language. **Immediate binding case:** the AOUT4 pairs on both DACs stay **open, not grounded** — precisely what a well-meaning "ground all unused pins" cleanup would break silently, which is why the annotation belongs **on the sheet where the cleanup would happen**, not in a document the cleanup would not read. *Original text below.* | — |
| ~~**F28-orig**~~ | | *Original:* **opposite unused-pin conventions, and mixing them is a live error.** The ADAU1466 pin table says **"Disconnect this pin when not in use"** on most unused I/O. Both AKM parts say the reverse — AK5574 Note 1: **"All digital input pins must not be allowed to float"**; AK4458 Note 2: same, plus an explicit table where unused *analog outputs* **must be open** while unused *digital inputs* **must go to DVSS**. So on one board, "leave it floating" is correct for one device, forbidden for another, and the correct answer even flips between the analog and digital pins of the same AKM part. | **Per-part unused-pin policy, stated on each sheet**, never a board-wide habit. This is F21's "floating is a state someone chose" with a second edge: *the right choice is per-datasheet, and the intuition that generalises is that none of them do* |
| **F29** | ✅ | **CLOSED — approved, one GPIO, and the shape is settled by T1-54.** `OVF` is a **summary flag across all four channels** at **−0.3 dBFS**, with **the same group delay as the ADC**, and there is **no per-channel overflow register** — so the pin/register split the operator asked about resolves to *pin-only*. That is still the right buy: clip detection **at the ADC is the only authoritative place**, since §6.1's comparators fire at ~10 mVrms (the opposite end of the range) and downstream detection cannot distinguish upstream clip from our own. **Channel attribution comes free on the DSP side** — the ADAU1466 sees all four channels on TDM and can meter them in-program, which beats an I2C read on both latency and resolution. Wire `OVF` → ESP32 GPIO as an interrupt-capable edge; expose through the control API and the status LED from day one; log in the firmware contract. Spends the margin F16 bought — on observability at the analog boundary. *Original text below.* | — |
| ~~**F29-orig**~~ | | *Original:* **`OVF` is a free analog-overflow flag.** §6.1 specifies signal-sense comparators for auto turn-on but the design has **no clip detection anywhere**. OVF is an existing output on a part already fitted; one GPIO turns it into input-clip indication for the control API and the status LED. | Cheap to route now, impossible to add later without a respin. Raise with the operator; not applied — it consumes a GPIO against the T2-07 budget |
| **F26** | ✅ | **CLOSED — V-19 passed on all three conditions; AK4118A and WM8804 both deleted.** (1) **Lock range 18 kHz–192 kHz**, against §12's 32/44.1/48/96 — wide margin. (2) **Clock path is fully on-die:** *"because the S/PDIF input data is most likely asynchronous to the DSP core, it must be routed through an ASRC"*, with **completely digital** clock recovery — no serial port in clock-consumer mode, no external recovered-clock net at all. §3's intent is satisfied *more* completely than by the external part. (3) **Pins 4/5 are dedicated**, no alternate functions, currently unassigned — no conflict. **Bonus:** the integrated TX takes data straight from the core at core rate and **costs zero serial ports**, so the WM8804 stuffing option goes too. Recovered: 2 parts, 2 serial ports, area, address 0x13, and an unspent verification tail. *Original finding text below.* | Caveat recorded, not material here: the interface meets **consumer** S/PDIF, **not AES3 professional** — correct for car audio. Auxiliary Output Mode (metadata onto a TDM8 port) exists but is unused |
| ~~**F26-orig**~~ | | *Original:* **an architecture question, not a detail. The ADAU1466 has an integrated S/PDIF receiver *and* transmitter** (T1-39, pins 4 and 5). The design carries an external **AK4118A** for SPDIF RX and a DNP **WM8804** for TX. If the integrated receiver suffices, the AK4118A becomes redundant — and it is not a small saving: it frees a part, a serial input port, board area, **and I2C address 0x13**, which un-zeroes the F23 bus slack that was just logged as a constraint for the next revision. | **Escalated** — respin-class, `CLAUDE.md` §4. Not applied. **The counter-argument is real:** §2 chose the AK4118A for its *8-input mux* ("spare inputs allow future optical"), which the integrated receiver almost certainly does not have. So this is a trade — one coax input with fewer parts, versus a multiplexed input path with room to grow. Operator's call, and it wants the integrated receiver's spec read first |
| **F25** | ✅ | **CLOSED — ≥ 4 layers decreed, promoted out of Block E.** The silicon mandates an internal ground plane (T1-38), so there is **no compliant 2-layer build of this board**. T3-02's 6-layer guess is now a **floor of 4, not a ceiling**; 6 stays live pending routing reality. Provenance matters here: "the exposed pad note forces it" is a far cleaner basis than "we assumed", and every Block E conversation now starts from 4 as **given** rather than open. *Original text below.* | — |
| ~~**F25-orig**~~ | | *Original:* **a Block E stackup input with teeth.** T1-38 requires identical copper squares on **all layers**, via-stitched, connected to "a **dedicated copper ground layer within the PCB**". On a 2-layer board there is no "within". **The part therefore mandates an internal ground plane** — an argument for >=4 layers arriving from the silicon rather than from routing density, and independent support for T3-02's 6-layer estimate. | Fold into the layout-blocked list alongside the pad's via array. It **strengthens** §6.3's single-unsplit-ground-plane mandate rather than competing with it |
| **F27** | ✅ | **CLOSED — TMP461-class replaces TMP102**, remote channel wired to the DSP thermal diode on pins 63/64. Die temperature was free money sitting unclaimed. One [VERIFY] rides along as **V-20**: the chosen variant's address straps against the §9 map, since the 0x48 range already holds the ADS1015 and two parts default-collided there once already. *Original text below.* | — |
| ~~**F27-orig**~~ | | *Original:* **thermal diode and specified sensor do not fit together.** T1-40: pins 63/64 are a remote thermal diode wanting a sensor with D+/D- inputs (TMP461/ADT7461 class). §9 specifies a **TMP102**, which measures its *own* die and has no remote channel. As written, the DSP's junction temperature cannot be read at all. | Either accept local-only sensing near the output stage and leave THD_P/M disconnected (the datasheet permits it), or swap to a remote-diode part and get DSP die temperature for free. Low urgency; decide before the BOM freezes |
| **F23** | ✅ | **CLOSED — it packs, with zero slack.** T1-32: all three AKM families share `0b00100` + CAD1 + CAD0 = **0x10–0x13**, and every device can take any of the four slots — the AK4118A is *less* constrained than the retracted T1-28 claimed. Four devices, four addresses, **no spare in the AKM prefix.** Bus map logged below; the second I2C controller is **not** needed and stays in reserve. | **Logged as §9 bus map.** The zero-slack condition is the thing the next revision must see coming: a fifth AKM part on this bus is impossible without splitting it |
| ~~**F23-orig**~~ | | *Original text retained:* **The AKM parts may not all fit on one I2C bus — which would defeat §5's "strap consistently to I2C".** T1-28: AK5574 and AK4458 have a **2-bit** chip address; AK4118A has C1 fixed at 0, so **one selectable bit**. The bus must carry AK5574 + **two** AK4458 + AK4118A + ADS1015 + TMP102. If the AKM families share a base slave address — and a ragged first-pass extraction showed the same `00100` prefix near all three — the two DACs plus the ADC plus the SPDIF receiver may not be uniquely addressable. | **Extract the exact slave-address bytes for all three AKM parts and lay them out against each other before capture.** If they collide, the escape is to put one part on 3-wire serial instead (all three support it), which *contradicts* §5's [VERIFY] instruction to strap consistently to I2C — so it is an operator decision, not a workaround |
| **F24** | ⚠ | **NEW. The LT3045 input rails are unspecified, and +5V_A cannot come from +5V_D.** §7.1 has always said "+5V_A / +3V3_A — LT3045-class ultra-low-noise LDOs" without naming what feeds them. An LDO needs headroom; **+5V_D at 5.0 V cannot produce a clean +5V_A**. It needs a higher intermediate rail, or derivation from ±13V5_A at a cost of (13.5 − 5) × I dissipated in the LDO. | Resolve before capture. Flagged in v0.5 §7.1 note 4 rather than silently inventing a rail |
| **F22** | ✅ | **CLOSED in v0.5 — the MCLK fanout was on the wrong rail, twice over.** T1-30: the LMK1C110x is a 1.8/2.5/3.3 V part, so §7.1's placement of "fanout" on **+5V_D** was wrong on its face. And it is the most jitter-critical device in the [HARD] §3 clock tree, with its 7.5 fs additive-jitter figure specified on a clean supply — so it belongs on **+3V3_A**, not the +3V3_D switcher. Moved to +3V3_A | — |
| **F20** | ⛔ | **NEW. §7.2 step 3 cannot work as written — the control port is dead while the PLL locks.** The [HARD] turn-on sequence says "ESP32 releases DSP reset, slave-boots program over SPI, verifies readback". But T1-23: while the PLL is locking, the SPI slave port is **inactive and every write fails** — up to **10.666 ms**, typically ~3.5 ms. Firmware that releases reset and immediately begins the slave boot has every write silently discarded. **Same shape as F1** — a [HARD] sequence omitting a hardware precondition, failing in a way that looks like a wiring fault. | Insert a step between current 3 and 4: after releasing reset, **configure the PLL (0xF000-0xF003), then poll `PLL_LOCK` 0xF004 Bit 0 until set, before any program write.** Needs operator sign-off as a [HARD] amendment |
| **F19** | ⛔ | **NEW. The DSP core draws far more than §7.1 anticipates, and it lands on +3V3_D.** T1-20: **495 mA maximum, 220 mA typical** at 1.2 V. Because DVDD derives from IOVDD, that current is drawn **from the 3.3 V rail**, and the 3.3->1.2 V drop dissipates **~1 W at maximum program** wherever the pass element sits. §7.1 offers "+3V3_D - buck **or LDO** from 5 V": with ~500 mA for the DSP plus the ESP32-S3 (several hundred mA peak on WiFi TX) plus BM83 plus IOVDD's own 53 mA, +3V3_D is a **1 A-class rail**, and an LDO from 5 V would burn ~2 W. | **+3V3_D must be a buck, not an LDO** — the "or LDO" option should be struck. Also feeds a thermal requirement §9 does not currently carry |
| **F18** | ⚠ | **NEW. §7.1's "+1V2_CORE - LDO from 3V3" is one of two valid methods, and the datasheet's own is the other.** T1-21: the on-chip regulator is a **controller driving an external PNP pass transistor** (`VDRIVE`, pin 3), rated to 800 mA. Real tradeoff: **the PNP path** moves ~1 W into a discrete you can give copper to rather than into an LDO package, but T1-22 imposes supply ordering (DVDD after AVDD/IOVDD/PVDD). **The external-LDO path** has *"no special sequence required"* but puts ~1 W in the LDO. | Operator's call — it trades thermal placement freedom against sequencing complexity, and both interact with the [HARD] §7.2. Not decided unilaterally |
| **F21** | ⚠ | **NEW. `SELFBOOT` (pin 34) needs a deliberate strap.** T1-25: floating = SPI self-boot, 10 kOhm pull-down = I2C self-boot, tied to GND = no self-boot. The 25AA1024 is DNP on v1 (T1-D22) and the ESP32 is boot master, so **the intended state is tied to GND** — but the pin has a 250 kOhm internal pull-up, so leaving it unpopulated **silently selects SPI self-boot from an absent EEPROM**. | Fit a resistor option so self-boot can be enabled later without a cut: GND strap fitted by default, pull-down/float alternatives as DNP pads |
| **F17** | ✅ | **CLOSED - CONFIRMED, and worse than suspected.** T1-16: the ordering guide lists six orderable models and **every one is 72-lead LFCSP `CP-72-6`**. There is **no LQFP *and no WLCSP*** — so §2's "(WLCSP/LQFP - prefer 72-LQFP for hand-rework)" is wrong on both counts and the hand-rework rationale has no package to rest on. Consequences: hot air with preheat, not an iron; stencil aperture and thermal vias for the 5.3 mm exposed pad, which is a **Block E stackup input we do not have**; T2-03's "no BGA" survives, "hand-rework friendly" does not. **Needs an operator decision, not just a note** — it changes the assembly plan. *Original finding:* **the ADAU1466 appears to have no LQFP option.** `REQUIREMENTS.md` §2 specifies "(WLCSP/LQFP — prefer 72-LQFP for hand-rework)". Two independent sources describe the ADAU1462/ADAU1466 as **72-lead 10 × 10 mm LFCSP with a 5.3 mm exposed pad**, and the orderable part `ADAU1466WBCPZ300` carries ADI's `CP` package code, which is LFCSP — `ST` would be LQFP. If this holds: **the hand-rework rationale in §2 does not survive.** LFCSP is leadless, so there are no leads to touch with an iron; it needs hot air with preheat, and the exposed pad needs a paste stencil aperture and thermal vias. It also puts a thermal-via requirement into the stackup, which is a **Block E** input we do not have. T2-03's "no BGA" claim survives — LFCSP is not BGA — but "0.5 mm pitch, hand-rework friendly" does not. | **T2, pending V-01.** Not acted on. The whole point of V-01 is to settle this from the document; two web sources plus a decoded part suffix is strong but is not the datasheet. Raise with the operator once V-01 opens — it may change the package choice, the assembly plan, or both |
| **F16** | ✅ | **CLOSED — ADS1015-class I2C ADC on I2C0; §9 dividers unchanged, only the converter moves; −13V5 divider referenced to a positive rail** → T1-D36. Side benefit: ~3 GPIO returned to the F13 budget. *Original:* **"rail monitor" described two ways.** §5 lists it as an I2C peer; §9 describes rail voltage dividers into the ESP32 ADC. §7.2 step 5 gates output unmute on it, so which one it is matters. Separately: **the −13.5 V rail cannot be measured by a plain divider to ground** — it needs a divider referenced to a positive rail to bring the tap into the ADC's range. | Q32. |

---

## 9. I2C0 bus map

Logged per the F23 disposition, because **a bus with zero spare slots in a family prefix is a
constraint the next revision needs to see coming.** Every device, every strap, every resulting
address. 400 kHz, single bus — the ESP32-S3's second I2C controller stays unused and in reserve.

| Device | 7-bit | Strap | Slack |
|---|---|---|---|
| AK5574 (ADC) | **0x10** | CAD1 = 0, CAD0 = 0 | |
| AK4458 #1 (AOUT1-6) | **0x11** | CAD1 = 0, CAD0 = 1 | |
| AK4458 #2 (AOUT7-12) | **0x12** | CAD1 = 1, CAD0 = 0 | |
| ~~AK4118A~~ | ~~0x13~~ | **part deleted (F26)** | **0x13 returned to the pool** |
| ADS1015 (rail monitor) | **0x48** | ADDR → GND | |
| TMP461-class (temp, F27) | **0x49** | strap TBD — **V-20** | 0x4A, 0x4B spare |

**Zero-slack note amended 2026-08-16.** F26's deletion of the AK4118A **frees 0x13**, so the
0b00100 prefix now holds three devices in four slots with **one spare**. A future ODSP-16's third
AK4458 therefore *does* have an address to live at, and I2C1 stays in reserve. This reverses the
constraint logged one round earlier — recorded rather than silently overwritten, because the
earlier note may already have been read.

**Two separate contention zones, and the second nearly bit us too.** The AKM parts occupy
0x10–0x13 with no room left. Independently, **ADS1015 and TMP102 both default to the 0x48–0x4B
range** and would collide at 0x48 if both were left at their default strap — assignments above
separate them and leave two spare.

**Mode straps that must accompany the addresses** (T1-27): `I2C`/`IIC` pin = **H** on all four
AKM parts, and the AK4458s additionally need **`PS` = L** — `PS` = H selects *parallel* mode, not
I2C. Per the F21 ledger entry, all of these get their idle level annotated in the schematic.

---

## 8. [VERIFY] checklist

`REQUIREMENTS.md` requires these confirmed against current datasheets **before capture**
(`CLAUDE.md` §3). Each is T2 at best until closed, and closing one is a T1 promotion **with a
citation** — part number, document revision, and section.

| ID | Item | Src | Status |
|---|---|---|---|
| V-28 | ~~The SM8S24 HM3 datasheet~~ | F42/F44/F45 | **CLOSED 2026-08-16 → T1-90/T1-91.** Found by extracting the PDF's own embedded hyperlinks (doc **98647**); the NRND banner text is not a link, but the "Related Documents" icon is. **Results: all four sub-questions answered and none of them moved a conclusion.** The successor is electrically identical, so §12's table stands as written; the **6600/5200 pair is two waveforms of one unidirectional part**, settling the three-way reading against the uni-vs-bi interpretation; the **43 V/153 A distributor figure is a mis-mapped field**; and the package changed **AB → AC with an identical land pattern**. *The pre-fired chain was never needed — which is the point of firing it.* |
| V-29 | ~~Multi-pulse derating~~ | F42 | **CLOSED BY ANALYSIS 2026-08-16**, using §12's own v0.1 escape clause — *"or documented protection analysis if untested"* — because Vishay publishes no multi-pulse curve for this part. **Per pulse:** 95 W × 400 ms × R<sub>θJM</sub> 0.30 °C/W = **ΔT<sub>J</sub> 28.5 °C** → 113.5 °C even from an 85 °C mount, against 175 °C. **Between pulses:** 0.67 % duty → **0.63 W average against an 8 W steady-state rating, 13× headroom**, so heating does not accumulate and the 10-pulse case reduces to the per-pulse case. **Assumptions are ours and tagged:** R<sub>θJM</sub> read off the transient curve at 0.4 s, and a mount temperature that depends on the Block E copper. *Original text below.* |
| ~~V-29-open~~ | | | **The gap, as located before closure.** The HM3 datasheet carries the same single-pulse figure set as its predecessor (Fig. 1 P<sub>PPM</sub> vs pulse width; Fig. 3 load-dump power for a **10 ms exponential**) and **publishes no M-suffix/S-suffix multi-pulse curves** — those appear in the EDN article for the *SM5S* family, not here. So ISO 16750-2's **10 pulses in 10 minutes** remains uncharacterised for this part. **Bound, not closed:** P<sub>D</sub> = 8 W steady-state sets the recovery rate between pulses, and at 1-minute intervals the junction fully recovers, so the binding case is per-pulse rather than cumulative heating — **but that is reasoning, not the vendor's curve.** Route: Vishay applications, or accept it as consumption of the suppressed row's 3–5× margin and say so in G7 |
| ~~V-29-orig~~ | | | **Open.** ISO **16750-2** superseded the load-dump test between the power sheet and full T1.** Read at figure level: **(1)** the **6600 W / 5200 W** pair, which now has **three competing readings and no T1** — mine-and-operator's-original (uni vs bi, supported by the distributor pattern of uni at 6.6 kW and bi at 5200 W), mine-second (two waveform ratings of one part, 10/1000 µs vs 10/10 000 µs, which is what the NRND table literally shows), and the possibility that **both are true at different levels** — family-wide polarity split *and* a waveform pair within each. **(2)** The clamp endpoints: held document says **38.9 V at 170 A**, an HM3-era distributor listing says **43 V at 153 A**. **(3)** The **M-suffix (multi-pulse, ISO 16750-2) vs S-suffix (single-pulse, ISO 7637-2)** capability curves. **(4)** The CA member's curves, which settle F45's direction decision. **Pre-fired, so the read cannot surprise us:** the consequence chain was run against *both* clamp endpoints — with 43 V/153 A, r<sub>d</sub> becomes 97 mΩ, Q1 sits at **73 %** of its 80 V rating (58 % on the realistic 48 A clamp), and **every §12 verdict row is unchanged** (93 / 364 / 739 / 3717 W against the same thresholds). **The pending read can refine numbers; it cannot move a conclusion.** That is criterion 5 and M7 doing exactly the job they were installed for |
| V-29 | **Multi-pulse derating: §12's table is a SINGLE-pulse analysis** | F42 | **Open.** ISO **16750-2** superseded the load-dump test with **10 pulses in 10 minutes**, and Vishay's own article states that *"10 continuous pulses affected the surge suppressing capability of the load dump TVS."* Our §12 rows compute one pulse. **The 3–5× margin on the suppressed row is the buffer this has to come out of**, and it is probably sufficient, but it is not yet evidenced. Settles from the HM3 M-suffix curves in the same read as V-28 |
| V-26 | ~~LM5156-Q1 spread-spectrum deviation percentage~~ | F39 | **CLOSED by decree, 2026-08-16 — not by finding the number, but by removing the dependency.** `DITHOFF` is fitted as a stuffing pair with the **populated leg to VCC: dither OFF**. The fundamental then sits deterministically at 2.2 MHz with an RT-tolerance floor of 1980 kHz — **15.8 % above the AM band on specified numbers only**, where the dithered case rested on 4 % of margin against a parameter the datasheet declines to state (the F37 shape). The decorrelation argument is untouched: beat suppression needs only one party spread, and both LM61460s carry ±2 % SS on their pinned PNs. A DNP leg to GND re-enables dither if EMI measurement ever asks. **Second use this round of "close it by making the number irrelevant"** — see V-27 |
| ~~V-26-orig~~ | | | **Open — and the datasheet does not contain it.** T1-76 gives the modulation *frequency* (0.156 × f<sub>SW</sub>) but never the deviation. Bounded meanwhile: f<sub>SW</sub> min is 1980 kHz, so even ±10 % dither reaches only 1782 kHz — above the AM band's 1710 kHz top, **but by 4 %**, which is margin-by-luck rather than by design. `DITHOFF` is a one-resistor escape hatch either way. Source: TI E2E or the EVM report, not the datasheet |
| V-27 | **LM5156-Q1 / LM61460-Q1 pulse-skip onset current, and the repetition rate when skipping** | F39 | **Open — unspecified by both datasheets**, which mention light-load pulse skipping only in prose. Matters because the analog rails idle near 50 mA against a 200 mA budget, i.e. permanently at ~25 % load. **Bounded, not blocking:** even 100 mV<sub>PP</sub> of in-band skip artefact meets 0.35 µV<sub>RMS</sub> at the op-amp rail through T1-72's audio-band PSRR. Settles on the bench, not before capture |
| V-01 | ADAU1466 package, ports, ASRCs + V-07/V-08/V-13 + firmware contract, in one pass | §2 | **CLOSED 2026-08-15 → T1-16…T1-25.** Single pass as planned (DL-22). Confirmed F17 and produced F18/F19/F20/F21 |
| V-02 | AK4118A: confirm it has no internal SRC, and its output-port master/slave capability | §3 / F1 | **Closed** → T1-10, operator confirmation. Re-check on the datasheet when it is open for pinout anyway — F1's whole disposition rests on it |
| V-03 | BM83 I2S master/slave capability in the chosen firmware config | §3 | Open |
| V-04 | AK5574 and AK4458 MCLK ratio and MCLK/LRCK synchronisation requirements at 48 kHz TDM | §3 / F15 | **DAC side closed → T1-26** (512fs or 768fs at 48 kHz; our 24.576 MHz XO is exactly 512fs). **ADC side still open** — AK5574 ratio table needs a second look, and the F15 MCLK/LRCK phase-coherence question is unanswered for both |
| V-05 | AK4458 differential full-scale output voltage | §6.2 / F12 | **CLOSED → T1-11.** 2.8 Vpp differential at (VREFH−VREFL)=5 V. `AK4458_AKM.pdf`, see `DATASHEETS.md` |
| V-06 | OPA1656 output swing and quiescent current at ±13.5 V | §6.2 / F7 | **Iq closed → T1-29:** 3.9 mA/channel, confirming the 96 mA figure behind T1-D30. **Output swing still open** — it sits in a spec table that needs a targeted read, and it is what confirms the 4.5 Vrms [HARD] headroom claim in T2-06 |
| V-07 | ADAU1466 slave-port maximum SPI SCLK (target ≥10 MHz) | §5 | **CLOSED → T1-19.** 20 MHz read and write — 2x margin on the target |
| V-08 | ADAU1466 core voltage and current | §7.1 | **CLOSED → T1-20.** 1.2 V ±5%; 220 mA typical, **495 mA max**. Drove F18 and F19 |
| V-09 | AKM control-port mode strapping — each part, strapped consistently to I2C | §5 | **CLOSED → T1-27.** I2C/IIC pin = H on all three; **AK4458 additionally needs `PS` = L**, since PS = H selects *parallel* mode. But see **F23** — whether they can all *coexist* on one bus is a separate question the strapping answer exposed |
| V-10 | AKM part lifecycle and lead time; decide AKM vs TI (PCM1865 / PCM1690) | §2 / §11 | Open |
| V-11 | INA1650 channel count per package | §2 / F2 | **CLOSED → T1-12.** Dual-channel, confirmed against the TI datasheet, no longer resting on operator confirmation alone |
| V-13 | ADAU1466 per-port serial master/slave configurability | §3 v0.2 / F1 | **CLOSED → T1-18.** Per-port `SERIAL_BYTE_x_0` registers with `LRCLK_MODE` / `BCLK_MODE` bits, plus per-port pin-table wording. **The F1 disposition is confirmed against the document**, and the operator's T2 was correct. The fallback (dedicated ASRC pair) is not needed |
| V-14 | **Series photoMOS** (TLP3475-class): Ron, off-state Coff, voltage rating vs ±6.4 V peak plus rail-collapse excursion, LED drive current | §6.4 v0.4 | Open — **restated at v0.4.** No longer a constrained optimisation: Ron 1–2 Ω against ≥10 kΩ is inaudible and off-isolation is the easy half of the pair |
| V-15 | **Shunt depletion FET pair**: Ron (100–500 Ω is ample), off-state Coff **and its nonlinearity**, Vgs(off) against the −13V5-derived bias | §6.4 v0.4 | Open — **restated at v0.4.** Small-die part; Coff is now the only tight number and it is tight against T1-D42, not against mute depth |
| V-19 | ADAU1466 integrated S/PDIF receiver: lock range, clock/ASRC path, pin conflicts, and whether the TX covers the digital-out option | §2 / F26 | **CLOSED 2026-08-16 → T1-42…T1-45.** All three conditions passed; TX covers it too. Figure-level read of pp. 74-75 per M2 |
| V-20 | **TMP461-class variant address straps** against the §9 bus map — the 0x48 range already holds the ADS1015 | §9 v0.8 / F27 | Open — **folded into the F38 sweep** as line 7. Same deliverable: PN pinned with the one-line why against the bus map. Pick from the strap table, not from aesthetics |
| V-17 | **AVDD currents for AK5574 and AK4458** — sizes the +6V2_A buck and **all three** LT3045 stages | §7.1 v0.7 / F24 | Open. Read alongside V-04's ADC side, same tables. **Sizing note:** the +6V2_A budget is the sum of +5V_A, +3V3_A **and the newly approved +3V3_CLK fanout load** — the escalation changed this buck's budget on the same turn it was raised |
| V-18 | **ADAU1466 core-supply ripple tolerance** from the electrical table — designs the +1V2_CORE buck's output filter against a number rather than vibes | §7.1 v0.5 / F18 | Open — **new at v0.5**, rides with the F18 disposition |
| V-16 | Disorderly-path transient, modelled as the **full stack**: DAC brown-out residual × mute attenuation × amp gain × amp remote-mute latency | §7.4 v0.4 | Open — bench, first board. **Bounded, not indefinite:** remote-out is fail-safe and drops first, so the window is the amp's own mute latency (tens to ~200 ms), and the source is a resetting DAC well under −20 dBFS, not programme material. Use a pessimistic latency — it belongs to someone else's amplifier |
| V-12 | BM83SM1 and ESP32-S3-WROOM-1 antenna keepout dimensions and board-edge requirements | §8 | **Partially closed → T1-31.** Both mandates confirmed: BM83 needs no copper, no component **and no ground plane** under the antenna; WROOM-1 has a keepout zone. **Dimensions live in figures** and need a `pdftoppm` render — fold into the DL-14 footprint pass, where the operator already eyeballs the BM83 keepout. **Escape hatch noted:** the **-1U** variant has no keepout because it takes an external antenna — the answer if T1-D20's antenna-separation requirement fights the outline |
