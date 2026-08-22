# ODSP-12 — System Architecture & Requirements

**Project:** ODSP-12 — open DSP, 12 out. Custom automotive DSP, 4 analog in / 12 analog out,
BT audio + wireless control
**Part number:** `ODSP12-MB-A` · **Revision scheme:** A/B/C… for fab revisions, running change
log in git rather than rev-suffix soup
**Doc status:** v1.8 — architecture baseline for schematic capture *(capture in progress)*
**Audience:** EE/PCB design agent. This doc defines system-level decisions. Layout-level
decisions (placement, routing, stackup) are delegated, but constraints flagged **[HARD]** are
non-negotiable and constraints flagged **[VERIFY]** require confirmation against current
datasheets before capture.

> **Provenance note.** v0.1 supplied by the operator 2026-08-15, reproduced verbatim with only
> table and heading *formatting* normalised. This file is the requirements authority per
> `CLAUDE.md` §3. Findings against it are logged in `STATE.md` §7 and are **not** silently
> corrected here — every change below came from an explicit operator disposition, listed in the
> revision history.

## Revision history

**v1.8 — 2026-08-21.** **Two [HARD] amendments, both the operator's act, sent DIRECTLY rather than
through the review bus.** Recorded here per this file's provenance note; neither agent may edit this
document to resolve a finding, and neither did — the text below is the operator's, transcribed.

| Amendment | Change | Section |
|---|---|---|
| **Audio interface format** | The three **converter** links — `SDATA_IN0`, `SDATA_OUT0`, `SDATA_OUT1` — are **32-bit MSB-justified, LRCK RISING edge**. **`SDATA_IN1` (BM83) is excluded**: it is 16-/24-bit I2S and can meet neither the word length nor the justification, and its format lives in the Config Tool binary. **The exclusion is not optional** — without it, a literal implementation sets that port to a format its peer cannot produce | §4 |
| **Master oscillator** | Replaces *“low-jitter XO”*. Duty cycle **tighter than 45/55 (e.g. 48/52)** so the converters' 45–55 % is met **with the buffer in the path**; **−20…+70 °C as a BASE specification, not an order-code option**; **jitter is not a selection criterion**. *The budget is 7.09 ps RMS at 20 kHz for 121 dB and any commodity part clears it ~140× — so the old wording was satisfiable by a part that fails the real requirement* | §3 |

*Closes the two rewording escalations standing since 2026-08-17 (§4 from F67/F69/F70, §3 from F56).
Both had previously arrived RELAYED THROUGH THE REVIEW BUS and were refused on that route —
`CLAUDE.md` §9 places review outside the authority order precisely so a decree cannot arrive through
it. This is the same content by the correct route.*


**v0.2 — 2026-08-15.** Operator dispositions of findings F1, F2, F5, F7, F8, F9, F10, F14
(`STATE.md` §7). Changed text is marked *(v0.2)* at the point of use.

| Finding | Change | Section |
|---|---|---|
| F1 | AK4118A removed from the DSP-slaved port list; it is **master** on its link. Bullet 3's intent unchanged | §3 |
| F2 | `4× INA1650` → `2× INA1650` — count error, 4 diff inputs = 4 channels = 2 packages | §2 |
| F5 | Operating range decreed −20 °C…+70 °C; **not an AEC-Q board**. AEC-Q100 required only on battery/harness-facing parts | §7.1 (new §7.0) |
| F7 | ±13V5_A budget: 200 mA continuous, 250 mA peak per rail | §7.1 |
| F8 | Attenuator divider sits **ahead** of the switch element | §6.1 |
| F9 | 0.1 % matched attenuator resistors — a BOM requirement | §6.1 |
| F10 | AOUT7–12 ↔ DAC#2 TDM slots 1–6 stated explicitly | §10 |
| F14 | `OPA1656 (or OPA1612)` → **OPA1656**, decided | §2, §6.2 |

**v0.3 — 2026-08-15.** Operator dispositions of F6, F11, F16 and the Q38 mute-budget gap.

| Finding | Change | Section |
|---|---|---|
| Q38 / F11 | **Mute must be the zero-energy state** — new [HARD] requirement. Latching relays ruled out; non-latching relays must be energised-to-unmute; semiconductor shunt preferred with the burden of proof reversed | new §6.4, §7.4 |
| F16 | Rail monitoring moves off the ESP32-S3 ADC to an **ADS1015-class I2C ADC** on I2C0. §9 dividers unchanged; only the converter behind them changes | §5, §9 |
| F6 | **FCC Part 15 Class B design practices, no formal chamber test for v1.** CISPR 25 explicitly out of scope — same industrial fork taken at F5 | new §7.5 |

**v0.4 — 2026-08-15.** Mute topology resolved; acceptance criteria amended; board named.

| Origin | Change | Section |
|---|---|---|
| Operator, correcting an assistant over-generalisation | **Series–shunt mute.** The zero-energy exclusion of enhancement-mode devices holds for a *shunt* and inverts for a *series* element — unpowered, a series Form A photoMOS is open, which is muted. Both halves fail safe independently and the depth-vs-capacitance conflict dissolves | §6.4 rewritten |
| Operator | **CCIF twin-tone IMD criterion added** — 19 kHz + 20 kHz at 2 Vrms, IMD ≤ 0.003 %. Added *alongside* the 1 kHz THD line, not replacing it | §12 |
| Operator | V-16 transient analysis gains a second layer: remote-out is itself fail-safe, so the requirement is bounded by the amp's remote-mute latency, not by indefinite suppression | §7.4 |
| Operator | Board named **ODSP-12**, PN `ODSP12-MB-A` | header |

**v0.5 — 2026-08-15.** Operator dispositions of the V-01 datasheet pass (F17–F21), plus F22
found in the same sweep. **§7 power section re-emitted as a unit** at operator request rather
than patched three times.

| Finding | Change | Section |
|---|---|---|
| F17 | ADAU1466 package corrected to **72-lead LFCSP `CP-72-6`**; the LQFP/WLCSP hand-rework parenthetical deleted — it was never an available option | §2 |
| F20 | **New step 3a in the [HARD] turn-on sequence**: configure PLL, poll `PLL_LOCK` with a 15 ms timeout, *then* boot. Timeout is a distinct fault code, not a retry | §7.2 |
| F19 | "+3V3_D — buck **or LDO**" → **buck only**, from VBATT_PROT, **2 A continuous design point** | §7.1 |
| F18 | +1V2_CORE becomes a **dedicated buck** (TPS62823-class); on-chip controller and `VDRIVE` unused, no PNP footprint at all | §7.1 note 3 |
| F22 | MCLK fanout buffer is a 3.3 V part, not 5 V — moved off +5V_D **to +3V3_A**, the clean rail, because it is the most jitter-critical device in the tree | §7.1 note 5 |
| — | +5V_A LDO input rail flagged as unresolved: it cannot come from +5V_D, which has no headroom | §7.1 note 4 |

**v0.6 — 2026-08-15.** F23 and F24 closed; §7.1 completes — **no rail without a source, no source
without a budget.** The power section is now stable pending V-17.

| Finding | Change | Section |
|---|---|---|
| F24 | **New +6V2_A rail** — small Q1-rated buck from VBATT_PROT, pre-regulating both LT3045 stages. Deriving +5V_A from ±13V5_A would burn 1.3-1.7 W in a low-noise LDO; from +5V_D it is impossible | §7.1, notes 4 and 6 |
| F23 | I2C0 packs: all four AKM parts into 0x10-0x13 with **zero spare**. Full bus map at `STATE.md` §9. Second I2C controller not needed | §5 |
| F15 | Cross-DAC alignment reduces to a firmware rule — see §5 firmware note | §5 |
| — | *Escalated, not applied:* a third LT3045 dedicated to the MCLK fanout buffer | §7.1 note 6 |

**v0.7 — 2026-08-15.** Escalation approved: **the MCLK fanout buffer gets its own LT3045**, rail
`+3V3_CLK`, with a cross-reference planted in §3 so the rail's reason travels with the tree it
protects. Capture begins.

**v0.8 — 2026-08-16.** V-19 passed on all three conditions; F26, F25 and F27 dispositioned.
**Two parts deleted.**

| Finding | Change | Section |
|---|---|---|
| F26 | **AK4118A and WM8804 deleted.** S/PDIF RX *and* TX are integrated in the ADAU1466. SDATA_IN2 and SDATA_OUT2 return to spare; I2C address 0x13 returns to the pool; coax front end reduces to termination + transformer + AC coupling into pin 4. Rationale recorded in §2 so it is not relitigated | §2, §3, §4, §5, §8, §12 |
| F25 | **≥ 4 layers decreed** — the exposed pad requires "a dedicated copper ground layer *within* the PCB", so there is no compliant 2-layer build. A **floor, not a ceiling**; 6 stays live pending routing | §6.3 / Block E |
| F27 | **TMP461-class replaces TMP102**, remote channel to the DSP's thermal diode on pins 63/64 | §5, §9 |

**v1.7 - 2026-08-16.** V-04, V-06 closed; §7.2 gains a precondition satisfied by construction.

| Finding | Change | Section |
|---|---|---|
| V-04 | ADC side closed: **MCLK = 512fs** (DCKS low), so 24.576 MHz is exactly 512fs at 48 kHz on both converter families. **§7.2 gains step 5a-pre**: MCLK must be running before `PDN` release — satisfied by rail ordering, verified at bring-up | §7.2 |
| V-06 | OPA1656 swing **(V−)+0.25 … (V+)−0.25** → ±13.25 V vs the 6.36 V peak 4.5 V<sub>rms</sub> needs: **6.4 dB**, quoted at a *harder* load than §12's. The [HARD] output level is now derivation end-to-end | §6.2, §12 |
| F50/F51 | ADC input bias must be **ratiometric, 0.512 × AVDD** — a fixed reference fails against AVDD tolerance at both ends. And the correct network **depends on the part's date code** | §6.1 |

**v1.6 - 2026-08-16.** V-17 closed; F46 decreed — a rail deleted.

| Finding | Change | Section |
|---|---|---|
| V-17 | AK5574 `AVDD+VREFH1/2` **64 mA max**, AK4458 `AVDD` **41 mA max** each → **+5V_A = 146 mA**. LMK1C1104 40 mA max. **+6V2_A = 186 mA identified against 250 mA assumed** — the assumption becomes a derivation | §7.1 |
| F46 | **+3V3_A DELETED.** Vestigial twice over: its founding tenant was erased by V-09/V-04, its second tenant evicted by F33. Tombstone at note 14; §9 monitor set amended to VBATT / +13V5 / −13V5 / **+5V_A** | §7.1, §9 |

**v1.5 - 2026-08-16.** V-28, V-29 and V-23 closed. The power sheet's open list is empty.

| Finding | Change | Section |
|---|---|---|
| V-28 | HM3 successor read (Vishay doc 98647). `SM8S24AHM3` **electrically identical** to the part already analysed, so §12 stands unchanged. BOM line settles to the **unidirectional** part | §7.1, §12 |
| V-29 | **Multi-pulse closed BY ANALYSIS**, using §12's own v0.1 escape clause. Per-pulse ΔT<sub>J</sub> = 28.5 °C; 0.67 % duty against an 8 W steady-state rating gives 13× recovery headroom, so the 10-pulse case reduces to the per-pulse case | §12 |
| V-23 | **AP2127 V<sub>REF</sub> = 0.8 V ±2 %.** +3V6_BT divider 34.8 k / 10 k → **3.584 V**, inside `BAT_IN`'s 3.2–4.2 V with the full tolerance stack. **F36 closes** — the PROVISIONAL LT3045 comes off the sheet | §7.1 |

**v1.4 - 2026-08-16.** F42 closed; F44 raised. Input protection is now a bounded, evidenced claim.

| Finding | Change | Section |
|---|---|---|
| F42 | **TVS is SM8S24AHM3-class in DO-218AB, not SMBJ24A** — 6600 W with a molded heatsink, AEC-Q101, same 24 V standoff / 26.7 V breakdown / 38.9 V clamp, so **every derivation keyed to 38.9 V carries over unchanged**. Load-dump capability written into §12 **as a table**, not as an assumption. Reverse battery documented as a **fuse-clearing event**, seamless recovery rejected on a thermal result | §7.1, §12 |
| F44 | **Three premises corrected against the datasheet.** The SM8S10A–43A family is **NRND** (successor AHM3); it is **unidirectional only**, so no `SM8S24CA` exists; and the 6600 W / 5200 W pair is the two **waveform** ratings, not uni-vs-bi. The `H` suffix is the **AEC-Q101** grade and is load-bearing under §7.0 | §7.1 |

**v1.3 - 2026-08-16.** F39 decreed — the ±13V5_A topology, the last §11 delegated decision on
the power sheet. V-26 decreed. Two new pre-rails enter §7.1.

| Finding | Change | Section |
|---|---|---|
| F39 | **±13V5_A topology settled: SEPIC → +15V5_A from VBATT_PROT; inverting buck-boost → −15V5_A from +15V5_A; LT3045 / LT3094 post-regulators to ±13V5_A.** Two new pre-rails, **+15V5_A** and **−15V5_A**, added to the §7.1 table. **The cascade is forced, not preferred** — an IBB stresses its regulator at V<sub>IN</sub> + \|V<sub>OUT</sub>\|, which exceeds the regulator's absolute maximum on a battery-facing rail the moment the TVS conducts. f<sub>SW</sub> = 2.2 MHz on both stages | §7.1, new notes 11–13 |
| V-26 | **Spread spectrum OFF on the SEPIC**, `DITHOFF` fitted as a stuffing pair. The AM-band clearance now rests on the specified f<sub>SW</sub> floor (1980 kHz, 15.8 % above the band) rather than on a dither deviation the datasheet never states. **This does not change §7.5** — SS stays on for the bucks, whose PNs specify it | §7.5 note |
| — | **Fail order promoted to a safety property** *(operator, F39(b))*: −15V5_A cannot outlive its own source, so the analog rails collapse in the only safe order **by construction** | §7.4 |

**v1.2 - 2026-08-16.** F34 resolved; V-22 closed.

| Finding | Change | Section |
|---|---|---|
| F34 | PVDD LDO enable gated from the **+3V3_D buck's `PG` pin**, not a divider off the raw rail - a loose EN threshold against a ramping rail is a race, not a guarantee. Pull-down for fail-safe-off. Note restated at **part level**: every ADAU1466 supply pin carries an ordering relationship to IOVDD | S7.1 note 10 |
| V-22 | Power/regulator/reset section read **end-to-end**. No third ordering constraint. Recorded: `AVDD` and `PVDD` are **mandatory even when unused**; RESET wants an external kOhm-class pull-down; RAM is not cleared by reset | S7.1, BRINGUP |

**v1.1 - 2026-08-16.** F33 closed, F34 raised.

| Finding | Change | Section |
|---|---|---|
| F33 | **`+3V3_PLL`** — dedicated small LDO from +6V2_A for the DSP's PLL supply. Both cheap fixes rejected with reasons recorded, so they are not re-proposed | §7.1 note 9 |
| F34 | **[HARD]: `IOVDD` must never come up after `PVDD`.** The PVDD LDO's **enable** is gated from +3V3_D — the shared ancestor is a logic signal, never a current path, so F33's isolation survives | §7.1 note 10 |
| V-21 | PVDD current settled at **15 mA max**, sizing the LDO at ~44 mW | §7.1 |

**v1.0 — 2026-08-16.** F30, F31, F32 dispositioned; `BRINGUP.md` created.

| Finding | Change | Section |
|---|---|---|
| F30 | Config phase reordered so the **12.5 ms I2C bus-quiet window costs zero wall-clock** — absorbed under the SPI program load, which is bus-independent and longer anyway | §7.2 |
| F31 | BM83 moved off +5V_D to a dedicated **`+3V6_BT`** LDO feeding `BAT_IN` directly; `ADAP_IN` rejected as the charger path | §7.1 note 8 |
| F32 | Host-mode config flash as a **documented bring-up step**, config binary committed to the repo | `BRINGUP.md` §2 |

**v0.9 — 2026-08-16.** Detail dispositions following F26.

| Change | Section |
|---|---|
| **The S/PDIF AC coupling cap carries a [HARD] annotation on the schematic** — required by datasheet, looks optional by topology, therefore a deletion candidate for anyone who has not read p.74 | §8 |
| Transformer specified: **1:1 pulse, PE-65612 / PT-class**, sourced on the connector/magnetics list | §8 |
| Consumer-not-AES3 caveat annotated so it is not later misread as "pro sources will not work" — it is a level/impedance matter, and the transformer front end handles AES3 *better* than most consumer inputs | §8 |
| **§12 SPDIF criterion split into two tiers** — register polls as the fast construction-check, plus one end-to-end tone pass. Lock is not audio | §12 |
| `SPDIF_LOSS_OF_LOCK` given a **runtime** consumer: the input-switching debounce signal, exposed through the control API from day one | §5 |
| Spare-port note updated: **four** spare serial ports, a full TDM8 in and out uncommitted | §4 |

Unchanged and still open at v0.9: F4 (impedance targets), F12, F13, F21 (accepted, lands at
capture).

---

## 1. System Overview

Single-board automotive DSP processor:

- 4× analog inputs (line-level and speaker-level capable, differential)
- 12× analog outputs (differential-buffered single-ended, 4–5 Vrms capability)
- SPDIF input (coax), optional SPDIF output
- Bluetooth A2DP audio sink (aptX-HD/AAC) via BM83
- Control plane: BLE GATT + WiFi HTTP/WebSocket via ESP32-S3
- 12 V automotive power with remote turn-on, signal-sense turn-on, sequenced muting

```
                     ┌─────────────────────────────────────────────┐
  4x HI/LO analog ──▶│ INA1650 diff RX ──▶ AK5574 ADC ──TDM4──▶    │
  SPDIF coax ───────▶│ AK4118A ──I2S──▶ (via ASRC)                 │
                     │                    ADAU1466                  │
  BT A2DP ══════════▶│ BM83 ──I2S──▶ (via ASRC)   SigmaDSP core    │
       ║             │                                              │
       ║ UART        │        TDM8 x2 ──▶ 2x AK4458 DAC            │
       ▼             │                      │                       │
   ESP32-S3 ◀──SPI──▶│◀── slave boot / safeload                    │
   BLE + WiFi        │                      ▼                       │
   control plane     │        OPA1656 buffers ──▶ 12x RCA out      │
                     └─────────────────────────────────────────────┘
```

---

## 2. Bill of Materials — Major Components

| Function | Part | Package notes | Rationale |
|---|---|---|---|
| DSP | ADI ADAU1466 — **72-lead LFCSP `CP-72-6`, 10 × 10 mm, 5.3 mm exposed pad** *(v0.5, F17 — this is the only package offered; the LQFP/WLCSP hand-rework preference was not available and is deleted)* | 3.3 V IOVDD, 1.2 V core | 8 stereo hardware ASRCs, 4+4 TDM serial ports, slave-boot over SPI |
| MCU | ESP32-S3-WROOM-1 (N8R2 or better) | Module, certified | BLE 5 + WiFi control plane, USB-OTG, SPI master to DSP |
| BT audio | Microchip BM83SM1 module | Certified module | A2DP sink, aptX/aptX-HD/AAC, I2S out, transparent UART data channel |
| ADC | AKM AK5574 | 4ch, 121 dB, TDM | Single-chip 4ch differential input |
| DAC | 2× AKM AK4458 | 8ch each, 115 dB, TDM8 | 6+6 channel split (see §4) |
| ~~SPDIF RX~~ | ~~AKM AK4118A~~ | **DELETED v0.8 (F26)** | superseded by the ADAU1466's integrated S/PDIF receiver |
| ~~SPDIF TX~~ | ~~WM8804~~ | **DELETED v0.8 (F26)** | superseded by the ADAU1466's integrated S/PDIF transmitter |
| Diff line RX | **2× INA1650** *(v0.2)* | 2ch/pkg → 4 channels for 4 diff inputs | High CMRR speaker/line-level front end |
| Output buffers | **OPA1656** *(v0.2 — OPA1612 alternate dropped)* | 2ch/pkg, 12 pkgs min | Diff-to-SE conversion + reconstruction filter. JFET input; high Zin relaxes the filter network. Filter values computed against OPA1656 only |
| Master clock | 24.576 MHz XO, **duty tighter than 45/55 (e.g. 48/52), −20…+70 °C as a base spec** *(v1.8)* | 3.3 V CMOS | Single clock master, see §3. ~~low-jitter~~ — **jitter is not a selection criterion** |
| CAN PHY (optional) | NXP TJA1051T-Q1 | DNP stuffing option | Future head-unit / SWC integration |
| EEPROM | 25AA1024 SPI EEPROM | DNP option | Self-boot fallback if MCU absent |

**[VERIFY]** AKM part availability/lifecycle status at time of capture; PCM1865 (ADC) and
PCM1690 (DAC, AEC-Q100) are the approved TI substitutes if AKM lead times are bad.
Substitution changes TDM formats — flag if exercised.

### Why the external S/PDIF receiver existed, and why it left *(v0.8, F26 — recorded so a future revision does not relitigate it)*

The AK4118A was specified before it was established that the ADAU1466 carries an **integrated
S/PDIF receiver and transmitter** (pins 4 and 5). Its stated rationale was an 8-input mux —
"spare inputs allow future optical".

That rationale did not survive scrutiny. **The mux only ever rode free.** While an external
receiver was being bought anyway, its extra inputs cost nothing; standing alone they had to
justify the whole part, and they cannot — a **TORX-class optical module outputs logic-level
S/PDIF directly**, so a future optical input is one 3.3 V receiver module plus a 2:1 mux or a
stuffing-option jumper into the same RX pin. The expansion path survives at roughly a tenth of the
cost, on the day it is actually wanted.

What the deletion recovered: a part, a serial input port, board area, **I2C address 0x13**, and
the whole verification tail that had not yet been spent — symbol, footprint, an eyeball slot in
the DL-14 set, control-port bring-up, and its share of the datasheet table reads.

**If a future revision wants multiplexed digital inputs, that is the reason to reopen this — not
"the DSP receiver looked marginal."** It is not: 18 kHz to 192 kHz lock range, fully digital
clock recovery, ASRC-coupled on-die.

---

## 3. Clock Architecture [HARD]

Single clock domain, one master, ASRCs isolate everything foreign.

- Master: 24.576 MHz XO → ADAU1466 MCLK input. ADAU1466 PLL configured for fs = 48 kHz core rate.
- **Master oscillator specification *(v1.8, operator decree — supersedes “low-jitter XO”)*.**
  The master oscillator **shall be specified for duty cycle such that, with the fanout buffer in
  the path, the converters' 45–55 % requirement is met** — requiring a source specified **tighter
  than 45/55, e.g. 48/52**. It **shall be rated over −20 °C to +70 °C as a BASE SPECIFICATION, not
  as an order-code option.** **Jitter is not a selection criterion**; the budget is cleared by any
  commodity part.
  > *Rationale, recorded so the clause is not re-litigated:* the jitter budget is **7.09 ps RMS at
  > 20 kHz for 121 dB**, and any commodity part clears it by **~140×**. What binds is **duty cycle
  > and temperature range**, neither of which the previous wording named — so the requirement as
  > written **was satisfiable by a part that fails the real one**.
- ADAU1466 is clock master on the **synchronous** serial ports. It generates BCLK/LRCLK for:
  AK5574 (slave), both AK4458 (slave), BM83 I2S port (BM83 configured as I2S slave).
  *(v0.2 — AK4118A removed from this list, see below.)*
- **S/PDIF is entirely on-die** *(v0.8, F26 — supersedes the v0.2 AK4118A arrangement)*. The
  ADAU1466's integrated receiver takes the coax stream on `SPDIFIN` (pin 4) and, per the
  datasheet, *"because the S/PDIF input data is most likely asynchronous to the DSP core, it must
  be routed through an ASRC."* Clock recovery is **completely digital**.
  **The recovered clock never leaves the die**, which satisfies the original §3 intent more
  completely than the external arrangement did — there is no serial port in clock-consumer mode,
  no external recovered-clock net, and nothing for the system clock tree to be contaminated by.
  Lock range **18 kHz to 192 kHz**, covering every rate in §12 with wide margin.
  *(Historical note: v0.2 corrected a v0.1 error that had the AK4118A slaved to our BCLK. That
  correction was right, and F26 has now removed the part it applied to. The principle it
  established — **ASRC in the path, no exceptions** — is unchanged and still governs the BM83.)*
- BM83 I2S also routes through an ASRC even though it's slaved — BT audio arrives at the source's
  rate regardless of our BCLK. **[VERIFY]** BM83 I2S slave mode + our clocking scheme against the
  BM83 datasheet; if BM83 must be I2S master in the chosen firmware config, land it on its own DSP
  input port as clock consumer of that port only, still through ASRC. Either way: ASRC in the path,
  no exceptions.
- DAC/ADC MCLK: distribute from the XO through a low-additive-jitter fanout buffer
  (e.g., LMK1C110x class) rather than daisy-chaining. **[VERIFY]** AK5574/AK4458 MCLK ratio
  requirements at 48 kHz TDM. *(v0.6: AK4458 accepts 512fs at 48 kHz — our 24.576 MHz XO exactly.)*
- *(v0.7)* **The fanout buffer runs from its own LDO, `+3V3_CLK`** (§7.1 note 7). Its supply noise
  converts directly into jitter on every converter at once, so it does not share a rail with the
  converters' signal-dependent AVDD current. **The rail exists for this tree; do not repurpose it.**
- No spread-spectrum anywhere in the audio clock tree. SS is fine on the ESP32 side; keep it off
  this net.

---

## 4. Serial Audio / TDM Map [HARD]

fs = 48 kHz system-wide. 32-bit slots.

**Audio interface format *(v1.8, operator decree)*.** The three **converter** links — `SDATA_IN0`
(AK5574), `SDATA_OUT0` and `SDATA_OUT1` (AK4458 ×2) — use **32-bit MSB-justified format with LRCK
RISING edge.**

**`SDATA_IN1` (BM83) is EXCLUDED from this clause.** The BM83 is **16-/24-bit I2S** and can meet
**neither** the word length nor the justification; its format is set in the **Config Tool binary**
and is governed separately.

> **The exclusion is not optional.** Without it, implementing this clause literally sets that port
> to a format its peer cannot produce.


| DSP Port | Direction | Peer | Format | Channels |
|---|---|---|---|---|
| SDATA_IN0 | in | AK5574 | TDM4, 32-bit slots | 4 (analog in 1–4) |
| SDATA_IN1 | in | BM83 | I2S stereo | 2 (BT L/R) → ASRC |
| SDATA_IN2 | in | **— spare —** *(v0.8, F26)* | | header/testpoints only. SPDIF is now **on-die**: `SPDIFIN` pin 4 → internal ASRC, no serial port consumed |
| SDATA_IN3 | in | — spare — | | header/testpoints only |
| SDATA_OUT0 | out | AK4458 #1 | TDM8 | ch 1–6 used, 7–8 reserved |
| SDATA_OUT1 | out | AK4458 #2 | TDM8 | ch 7–12 used (slots 1–6), 7–8 reserved |
| SDATA_OUT2 | out | **— spare —** *(v0.8, F26)* | | digital out is now **on-die**: `SPDIFOUT` pin 5, fed directly from the core at core rate, **costs zero serial ports** |
| SDATA_OUT3 | out | — spare — | | header/testpoints only |

- *(v0.9)* **Four spare ports now, not two** — F26 returned SDATA_IN2 and SDATA_OUT2 to the pool
  alongside IN3/OUT3. All four go to 0.1" test headers with ground pins between signals. A
  comfortable position: a full TDM8 in and out remain uncommitted for expansion or bring-up.
- 6+6 DAC split (rather than 8+4) keeps per-chip output loading symmetric and leaves 2 spare
  channels on each DAC for rework flexibility.

---

## 5. Control Plane

ESP32-S3 is the single owner of all device state.

| Bus | Master | Peers | Notes |
|---|---|---|---|
| SPI0 (ESP32) | ESP32-S3 | ADAU1466 slave port | Slave boot at power-up; runtime parameter writes via safeload mechanism. Target ≥10 MHz SCLK. **[VERIFY]** 1466 slave-port max SCLK. |
| UART1 | ESP32-S3 | BM83 | Command/control + transparent data channel (legacy SPP tunnel if ever needed) |
| I2C0 | ESP32-S3 | AK5574, 2× AK4458, **TMP461-class remote-diode temp sensor** *(v0.8, F27)*, **ADS1015-class rail-monitor ADC** *(v0.3)* — ~~AK4118A~~ deleted *(v0.8, F26)* | 400 kHz. **[VERIFY]** each AKM part's control-port mode strapping (some are I2C/SPI selectable — strap consistently to I2C). |
| GPIO/ADC | ESP32-S3 | signal-sense comparators (×4), remote-in sense, rail dividers, mute relay/FET driver, remote-out high-side driver, BM83 MFB/reset, DSP reset | See sequencing §7 |

Firmware responsibilities (out of scope for PCB, listed so pin budget is right): BLE GATT
NUS-style control service, WiFi HTTP/WS API, OTA, DSP program storage in ESP32 flash, param
persistence.

**Firmware contract** *(v0.6 — items the hardware design depends on being honoured)*:

1. **Boot preamble** — §7.2 step 3a. Configure PLL (0xF000-0xF003), poll `PLL_LOCK` (0xF004
   Bit 0) with a 15 ms timeout, *then* load the program. Timeout = distinct fault code.
2. **Safeload** — `num_SafeLoad_Lower` / `num_SafeLoad_Upper`, 1-5 parameters per transaction,
   page-split addressing. Output routing at `SOUT_SOURCEx`, 0xF180-0xF197.
3. **I2C0 bus map** — fixed addresses per `STATE.md` §9. **The AKM prefix 0x10-0x13 is full**;
   any future AKM part requires splitting the bus onto the S3's second I2C controller.
4. **S/PDIF registers** *(v0.9)*. `SPDIF_LOCK_DET` 0xF600 and `ASRC_LOCK` 0xF580 for the §12
   tier-(a) sweep. **`SPDIF_LOSS_OF_LOCK` 0xF605 needs a *runtime* consumer, not just a test
   hook** — it is the input-switching debounce signal, and it should be exposed through the BLE/WS
   control API **from day one** rather than retrofitted once the need is discovered on a bench.
   `SPDIF_RESTART` 0xF604 auto-resumes the receiver. Channel-status / user-data / validity /
   parity blocks at 0xF610-0xF68B if source metadata is ever wanted.
5. **Do not mix digital-filter modes between the two AK4458s** *(F15)*. Both are slaved to the
   same BCLK/LRCLK pair, so they are sample-aligned and group-delay-matched **by construction** —
   provided their filter settings match. Cross-DAC alignment is therefore one register write away
   from being wrong, and it is a firmware invariant, not something an acceptance test should be
   asked to catch.

**Pin budget note:** the above consumes roughly 20–24 ESP32-S3 GPIOs. WROOM-1 exposes enough, but
do the explicit pin map before capture and reserve USB D+/D− (GPIO19/20) — do not assign them
elsewhere. USB-C connector (device role, ESD-protected) to the S3 native USB for
flashing/debug/console.

---

## 6. Analog Design

### 6.1 Input front end (×4)

- Differential input, RCA + strip-terminal speaker-level entry.
- Attenuation ladder ahead of INA1650: two software-readable ranges minimum — line (≤2 Vrms) and
  speaker-level (target ≤ 30 Vrms full-scale). Range switching via relay or analog switch under
  MCU control; do not use jumpers.
- *(v0.2, F8)* **The divider sits ahead of the switch element** so the switch never sees more than
  attenuated signal — 30 Vrms is ~42 V peak, beyond common analog switches. A relay satisfies this
  trivially; an analog switch only with the divider in front of it.
- *(v0.2, F9)* **Attenuator resistors are 0.1 % matched or better** — a BOM requirement, not a
  preference. The §12 CMRR ≥ 60 dB criterion is set by leg-to-leg matching in this ladder, not by
  the INA1650, which has far more rejection than the network in front of it.
- INA1650 output → AK5574 differential input with the datasheet-recommended antialias RC.
- Signal-sense: precision rectifier + comparator per input pair (or one on a summed node —
  designer's choice) into ESP32 GPIO for auto turn-on. Threshold settable by resistor divider;
  ~10 mVrms nominal.
- Input impedance ≥ 20 kΩ line mode.

### 6.2 Output stage (×12)

- AK4458 differential outputs → OPA1656 diff-to-SE + 2nd-order reconstruction filter → RCA.
- **4.5 Vrms minimum output before clip into 10 kΩ [HARD]** — this drives the ±12–15 V analog rail
  requirement.
- Output muting: FET or relay shunt mute at each RCA, single mute rail driven by MCU.
  ~~Relay preferred for zero distortion contribution; FET acceptable if THD contribution < DAC
  floor.~~ *(v0.3 — superseded by §6.4; the burden of proof is reversed.)*
- Output impedance ≤ 100 Ω.

### 6.4 Mute topology — series–shunt *(v0.4)*

**Series–shunt semiconductor mute. Two devices, each fail-safe in its own polarity, splitting the
two requirements that could not be met by one.**

Fail-safe polarity is a property of the **topology**, not of the device class:

- **Series element — Form A photoMOS** (TLP3475-class), LED driven = pass. Unpowered the LED
  dies, the MOSFETs open, and an open series path *is* mute. Enhancement-mode is correct here;
  the v0.3 exclusion applied only to the shunt case.
  Ron 1–2 Ω against a ≥10 kΩ load is nothing, and photoMOS on-resistance is genuinely resistive —
  the floating photovoltaic gate drive keeps Vgs constant as the signal moves, which is why these
  parts live in ATE signal paths. Off, it delivers 60+ dB of isolation, the same as a relay
  contact, without a coil.
- **Shunt element — depletion-mode FET pair, back-to-back source-to-source**, after the series
  device, gate biased off from a −13V5_A-derived rail. Rail collapse returns Vgs to 0 and it
  conducts. The back-to-back requirement is not a refinement: a single MOSFET shunting a bipolar
  signal conducts through its body diode on one half-cycle and becomes a rectifier.

**Why this dissolves the v0.3 conflict.** The shunt's only remaining job is to kill the series
device's off-state Coff leakage — tens of pF feeding a node that is being actively shorted. Ron of
100–500 Ω is ample for that, which permits a small-die part, which means small Coff, which is
exactly what the pass-state THD budget wanted. Depth and linearity stop competing because they are
no longer asked of the same device.

**Failure behaviour is the product of two independent mechanisms.** Rails collapse → LED dies →
series opens. Independently, the −13V5-derived bias dies → shunt closes. Neither depends on the
MCU, on the other, or on anything remaining powered.

**Continuous cost, stated honestly:** the series photoMOS is energised-to-pass, so ~2–5 mA of LED
drive per channel × 12 ≈ **60 mA on +5V_D, held for the operating life of the unit** (~0.3 W).
That is an order of magnitude better than the 0.4–0.5 A and watt-plus of relay coils, but it is
not zero and it belongs in the +5V_D budget as a line item, not as a rounding error.

**Series device voltage rating** must cover the full output swing (±6.4 V peak at 4.5 Vrms) plus
whatever the rails do on collapse.

---

*Superseded v0.3 text, retained for the record:* **semiconductor shunt mute is the default; a
relay must justify itself.** That framing stands — a relay is still not the answer — but the
reasoning below over-generalised the enhancement-mode exclusion from the shunt case to the whole
device space, and §6.4 above is the correction.

- **Latching relays: prohibited.** A latching relay holds its state through a rail collapse, so a
  unit that loses power while unmuted stays unmuted through the entire decay. That is the worst
  available configuration and it is the one a latching part naturally produces.
- **Non-latching relays: permitted only wired energised-to-unmute** (de-energised = shunted).
  Fail-safe, but it holds ~12 coils × 30–40 mA for the operating life of the unit — ~0.4–0.5 A
  continuous on +5V_D and better than a watt of coil heat, permanently, to buy a THD improvement
  that sits below the DAC noise floor. If this option is taken, the +5V_D budget grows by 0.5 A
  and the LM61460-Q1 is re-checked against total load.
*(The v0.3 single-device analysis — that `Ron × Coff` is roughly constant, so mute depth bought
with a shunt costs off-capacitance and therefore THD — was correct **for a shunt-only design** and
is what motivated the split. It no longer constrains the part choice.)*

### 6.3 Grounding/planes (guidance, layout-delegated)

Single ground plane, partitioned analog/digital by placement not splits, star-connect chassis at
the RCA ground field through an RC network. Standard practice; flag deviations.

---

## 7. Power Architecture & Sequencing

### 7.0 Environment and component grade *(v0.2, F5)*

**This is not an AEC-Q board.** It is an enthusiast/aftermarket unit, not OEM automotive.

- **Operating range: −20 °C to +70 °C.** Industrial-grade components acceptable throughout the
  signal path.
- **AEC-Q100 is required only where parts face the battery/harness directly** — input protection,
  the bucks, CAN PHY, remote-out driver. Load dump and transients are physics, not certification
  theatre; the qualification requirement follows the exposure, not the product category.
- The PCM1690 note in §2 was a supply-driven substitution option, **not** a signal that the
  converter chain needs automotive grade. The AKM converters and the OPA1656 are industrial parts
  and that is correct for this design.

### 7.1 Rails

*Re-emitted as a unit at v0.5 (F18, F19, F22 and the V-01 datasheet pass). Supersedes the v0.1
table entirely — do not merge it with the original.*

| Rail | Source | Loads | Budget |
|---|---|---|---|
| **VBATT_PROT** | **5 A fuse + SM8S24 TVS (`AHM3` vs `CAHM3` pending V-28) + reverse P-FET + damped LC** *(v1.4, F42/F45)* — ~~SMBJ24A~~ | everything below | ISO 7637-2 **[HARD]**, bounded per §12 |
| **+5V_D** | **LM61460-Q1 buck from VBATT_PROT** | USB, **+3V6_BT LDO** — ~~BM83~~ moved *(v1.0, F31)* | modest — see note 1 |
| **+3V6_BT** *(v1.0, F31; part settled v1.5)* | **AP2127K-ADJ from +5V_D**, divider-set — V<sub>REF</sub> 0.8 V ±2 %, 34.8 k / 10 k → **3.584 V** | BM83SM1 `BAT_IN` **only** | ~140 mW at 100 mA — see note 8 |
| **+3V3_D** | **LM61460-Q1 buck from VBATT_PROT** *(v0.5 — "or LDO" struck)* | ESP32-S3, DSP IOVDD, converter digital sides, +1V2_CORE buck input | **2 A continuous design point** |
| **+1V2_CORE** | **dedicated buck from +3V3_D** (TPS62823-class, ≥750 mA) *(v0.5 — was "LDO from 3V3")* | ADAU1466 DVDD only | 220 mA typ, **495 mA max** |
| **+15V5_A** *(v1.3, F39)* | **SEPIC from VBATT_PROT**, LM5156-Q1 + external FET, 2.2 MHz, dither **off** | +13V5_A LDO **and** the −15V5_A stage — see note 11 | ~544 mA, ≈ 8.5 W |
| **−15V5_A** *(v1.3, F39)* | **inverting buck-boost from +15V5_A** (LM61460-Q1 reconfigured per SNVA856), 2.2 MHz | −13V5_A LDO only | ~250 mA |
| **±13V5_A** | ~~SEPIC/flyback or dual-boost~~ → **LT3045 (+) / LT3094 (−) from ±15V5_A** *(v1.3, F39)* | op-amp stages | **200 mA cont., 250 mA peak, per rail** |
| **+6V2_A** *(v0.6, F24)* | **small Q1-rated buck from VBATT_PROT**, spread-spectrum permitted | pre-regulator for the analog LDOs only | sized at V-17 |
| **+5V_A** | **LT3045 from +6V2_A** *(v0.6)* | AK5574 + both AK4458 `AVDD` | **146 mA max** (V-17) |
| ~~**+3V3_A**~~ | **DELETED v1.6, F46** — see the tombstone below | — | — |
| **+3V3_CLK** *(v0.7)* | **dedicated LT3045 from +6V2_A** | **MCLK fanout buffer only** — see §3 | small; sized with V-17 |
| **+3V3_PLL** *(v1.1, F33)* | **dedicated small LDO from +6V2_A** (MIC5504 / TPS7A02 class) — **enable-gated by +3V3_D, see note 10** | ADAU1466 `PVDD` (pin 15) **only** | **15 mA max** (V-21) → ~44 mW |

**Note 1 — two bucks from the battery, not a cascade.** +3V3_D is taken directly from VBATT_PROT
rather than from +5V_D. This avoids compounding conversion loss at the largest step, stops an
ESP32-S3 WiFi TX burst from sagging the BM83/USB domain, and keeps both parts battery-facing and
therefore AEC-Q100 per §7.0. Using the **same LM61460-Q1 twice** gives one qualification, one
layout block drawn twice, and one datasheet.

**Note 2 — the 2 A floor on +3V3_D is a decree, not a calculation.** The DSP core alone pulls up
to 495 mA (through the +1V2_CORE buck), the ESP32-S3 bursts several hundred mA on WiFi TX, and the
DSP's own IOVDD is 53 mA, plus BM83 and the converter digital sides. **Peaks coincide by Murphy,
not by schedule.** Size for 2 A continuous.

**Note 3 — why +1V2_CORE is a buck and not the on-chip regulator.** The ADAU1466 provides a
regulator *controller* driving an external PNP (`VDRIVE`, pin 3). That path dissipates ~1 W at
maximum program and drags in a supply-ordering constraint — DVDD must follow AVDD/IOVDD/PVDD —
that entangles with the [HARD] §7.2 sequence. A dedicated buck dissolves both. **This is a 1.2 V
digital core; it has no seat at the §3 noise table.** The on-chip controller and `VDRIVE` go
unused and **no PNP footprint is fitted, not even DNP.** Spread-spectrum is permitted on this
stage per §7.5 — it is a power stage, not the audio clock tree.

**Note 4 — +6V2_A is a pre-regulator, and it exists because the arithmetic killed the
alternative** *(v0.6, F24)*. Feeding the +5V_A LT3045 from ±13V5_A burns (13.5 − 5) × I: at the
150–200 mA the converter AVDDs plausibly draw, that is **1.3–1.7 W in a part chosen for its noise
floor, not its thermals** — and it loads the bipolar converter with current that never needed to
be bipolar. Deriving +5V_A from +5V_D is simply impossible; an LDO has no headroom there. A small
buck at 6.2 V gives the LT3045s **1.2 V of headroom, keeping dissipation in the 200 mW class**,
and the LT3045's PSRR at buck switching frequencies is precisely the job it was hired for. This is
the standard pre-regulator shape.

**Note 6 — the analog LDOs run in parallel from +6V2_A, not cascaded, and the clock buffer gets
its own.** Cascading (+6V2 → +5V_A → +3V3_CLK) would multiply PSRR, but it puts the **converters'
signal-dependent AVDD current upstream of the clock buffer's supply** — a modulation path that
does not need to exist. Parallel LDOs decouple them.

**Note 14 — tombstone: why +3V3_A existed, and why it does not** *(v1.6, F46)*. The rail was
written in v0.1 when "+5V_A / +3V3_A → ADC/DAC analog supplies" was set down against *assumed*
converter supply domains. **V-09/V-04 then established that all three converters run `AVDD` at
5 V**, and their 3.3 V domain is `TVDD` — digital, and already assigned to +3V3_D by note 1. That
erased its founding tenant. It got a second life housing the **clock fanout** when F22 moved the
LMK1C1104 off the digital rail, and **F33's escalation evicted that tenant too** when the fanout
earned its own `+3V3_CLK` from +6V2_A. **Nobody re-ran the occupancy check after the move-out, so
an LT3045 has been regulating for an empty room since v0.6.** V-17's enumeration is the first thing
that walked every load since then.

*Reading (c) — repurposing it for converter `TVDD` — was considered and rejected, recorded so it
is not re-had.* TVDD noise perturbs digital *thresholds*, on lines that latch data rather than
convert it; the sampling instant on these parts is set by MCLK, which already rides the board's
cleanest supply. And the interface levels are driven from the DSP's `IOVDD` on +3V3_D regardless,
so a clean receiver supply under a noisy driver's signal buys threshold margin against noise that
arrives *on the signal* — which is not the mechanism note 9 describes.
**Reopen condition:** if bench EMI shows the converters' digital domains want isolation, the
datasheet-standard answer is a **local ferrite plus bypass per TVDD pin** — two passives, below
rail architecture. Unverified concern, not disproven (M12).

**What the deletion freed:** one LT3045 and its 33.2 kΩ R<sub>SET</sub>, one testpoint, ~100 mW,
and **one ADS1015 channel — reassigned to +5V_A**, which was never monitored and is the most
diagnostic single analog voltage on the board: it feeds all three converters' `AVDD` directly, so
a sagging +5V_A explains more field symptoms than the empty rail ever could.

**Note 11 — the ±13V5_A cascade is forced by an absolute maximum, not chosen for elegance**
*(v1.3, F39)*. An inverting buck-boost stresses its regulator at **V<sub>IN</sub> +
|V<sub>OUT</sub>|**. Sited on VBATT_PROT, that is ≥ 26.7 + 15.5 = **42.2 V against the
LM61460-Q1's 42 V absolute maximum** — and it holds without knowing the clamp voltage, because
any TVS with a standoff above 24 V breaks down above 26.5 V. **The negative stage therefore
cannot sit on the battery rail at all.** Fed from the regulated +15V5_A it sees a fixed 31 V, at
the ideal 0.5 duty. The mirror argument excludes a plain boost on the positive rail: TI states
that a boost passes its input through the high-side diode when V<sub>OUT</sub> ≤ V<sub>IN</sub>,
which would land a clamped load dump on a 20 V LDO input. **Do not "simplify" either stage back
onto VBATT_PROT.** The honest cost is that the SEPIC carries both rails — ≈ 8.5 W, ~1.65 A input
at crank — where independent stages would be half that each.

**Note 12 — f<sub>SW</sub> = 2.2 MHz on both stages, on three independent legs** *(v1.3, F39)*.
**(a)** The LT3045's PSRR has a **notch at 500 kHz–1 MHz and recovers by 2 MHz** — 77 / 72 / 70 /
84 dB at 100 kHz / 500 kHz / 1 MHz / 2 MHz with 2 V of headroom. The part is *better* at 2.2 MHz
than at half that; this is what excluded the four-switch buck-boost, whose range tops out at
600 kHz, squarely in the notch. **(b)** The dither triangle runs at 0.156 × f<sub>SW</sub> =
343 kHz; at a 100 kHz f<sub>SW</sub> it would sit at 15.6 kHz, *inside the audio band*.
**(c)** Nothing exists below the fundamental, so no harmonic falls in the AM band — a 440 kHz
choice would put its 2nd and 3rd squarely in it.

**Note 13 — the two analog rails are not symmetric, and the budget says so** *(v1.3, F39)*. The
LT3094 has **its own** PSRR shape: it peaks at 100 kHz where the LT3045 peaks at 2 MHz, and
**degrades as headroom grows past ~2 V**, the opposite behaviour. Against the [HARD] 50
µV<sub>RMS</sub>: **+13V5_A ≈ 2.0 µV<sub>RMS</sub> (28 dB margin), −13V5_A ≈ 4.5 µV<sub>RMS</sub>
(21 dB)**. Both clear comfortably, and the budget is carried by the LDOs' **audio-band** PSRR
(110 dB / ≥93 dB), not by f<sub>SW</sub> — which is why the unspecified light-load pulse-skip
behaviour (V-27) cannot break it. The ~1.9 V headroom target is a **PSRR specification, not a
dropout one**: dropout is 260 mV and 235 mV respectively, so the design carries ~8× dropout on
purpose.

**Note 9 — the PLL supply is a victim *and* an aggressor, so it gets its own LDO** *(v1.1, F33)*.
`PVDD` feeds the PLL that generates BCLK/LRCLK for every converter on the board, so supply noise
on it becomes jitter everywhere at once — the F22 argument. But it is **not** tapped from
`+3V3_CLK`: the fanout buffer is a pure victim, while **the PLL's charge pump and VCO draw
switching current**, and on a shared LDO those transients appear across the regulator's output
impedance and modulate the fanout's supply. Tapping +3V3_CLK would put the noisiest clock-domain
device on the rail that exists to be the quietest.

Nor is it a ferrite or RC off +3V3_D. **The contamination is low-frequency by nature** — WiFi TX
bursts droop the rail at envelope rates of hundreds of Hz to low kHz, where a ferrite does nothing
and an RC large enough to help would burn headroom out of a ±10 % window. **An LDO's PSRR is
strongest exactly where a ferrite is weakest**, and feeding it from +6V2_A removes the shared
upstream path entirely: the WiFi bursts and the PLL no longer have a common ancestor below the
battery input. At 15 mA (V-21) with 2.9 V of headroom this is ~44 mW — any competent small LDO,
not a reference-grade part.

**Note 10 — `IOVDD` must never come up after `PVDD`, and the fix is the enable, not the supply
path** **[HARD]** *(v1.1, F34)*. The ADAU1466 states: *"IOVDD, which is the reference for the ESD
protection diodes that are situated inside the input and output pins, must be applied first to
avoid stressing these diodes. PVDD, AVDD, and DVDD can then be supplied in any order."*

Note 9 puts `PVDD` on a **different branch of the power tree** from `IOVDD` (+3V3_D), so nothing
otherwise guarantees their relative order — if the +3V6/+6V2 branch wins the race, **PVDD precedes
IOVDD and stresses the ESD diodes on every power-up.**

**Resolution: gate the PVDD LDO's enable from the +3V3_D buck's `PG` (power-good) pin** — *not*
from the raw rail through a divider. **A divider into an LDO enable turns the guarantee back into
a race, just a slower one:** EN thresholds are specified loosely (often "somewhere in 0.4–1.2 V"),
and against a ramping rail that is not a sequencing guarantee. The LM61460 has `PG`, which asserts
at a defined threshold with defined brownout and hiccup behaviour — **PG-to-EN makes the order a
designed property with a datasheet behind both ends.**

- **Pull-down on the EN net**, so the PVDD LDO defaults **off** when `PG` is high-Z or unpowered.
  This is the fail-safe-polarity rule from §6.4 applied to a rail enable. **[VERIFY]** whether the
  LM61460's `PG` is open-drain (likely) and size the pull-up/pull-down pair accordingly.
- **The shared ancestor becomes a logic signal, never a current path.** Note 9's noise isolation
  survives intact. *Sequencing and noise isolation are separable concerns, and are separated here
  deliberately* — recorded verbatim so a future "simplification" does not tie PVDD back to +3V3_D
  on the grounds that they are related anyway.

**This constraint is a property of the part, not of these two rails.** **Every ADAU1466 supply pin
carries an ordering relationship to `IOVDD`: none of `AVDD`, `DVDD` or `PVDD` may precede it.**
Today `AVDD` shares +3V3_D (simultaneous) and `DVDD` comes from the +1V2_CORE buck fed from
+3V3_D (necessarily later), so both are safe by construction. **Consult this note before adding,
moving, or re-parenting any rail that feeds any ADAU1466 supply domain** — not merely before
touching these two.

Related, and easy to optimise away by mistake *(T1-61)*: **`AVDD` must be supplied even though the
auxiliary ADCs are unused**, and **`PVDD` must be supplied even if the PLL were unused.** Neither
is droppable.

**Note 8 — the BM83 gets its own 3.6 V rail, and `ADAP_IN` is a trap door** *(v1.0, F31)*.
`BAT_IN` is specified 3.2–4.2 V, so **+5V_D was never legal** and a nominal 3.3 V is not a fix
either — 3.3 V −5 % = 3.135 V, below the minimum. **`ADAP_IN` is not the answer:** it is the input
to the module's **Li-ion charger**, designed assuming a battery hangs on `BAT_IN` to absorb charge
current and set the voltage. Battery-less operation through the charger path is the kind of thing
that works on the bench and then **brown-outs on Bluetooth TX peaks**, when the charger's current
limit meets a load transient it was never designed to source.

An LDO at 3.6 V from +5V_D burns (5 − 3.6) × 0.1 ≈ **140 mW** — thermally trivial — and **an LDO's
transient response suits a radio better than a small buck's** anyway. Two **[VERIFY]** items ride
along: **(a)** the module's real peak current from the electrical tables, so the LDO is not sized
on folklore; **(b)** confirmation the datasheet blesses supplying `BAT_IN` directly with no
battery present. **If it requires the charger path for battery-less designs, escalate** — that
section gets read together, not worked around.

**Note 7 — the MCLK fanout buffer has its own LDO: `+3V3_CLK`** *(v0.7, approved)*. A third
LT3045 from +6V2_A, feeding **only** the fanout buffer. It is the one device whose supply noise
converts directly into jitter on **every converter simultaneously**; sharing an LDO with the
converters' AVDDs would create a signal-correlated modulation path into the [HARD] §3 clock tree.
This is note 6's parallel-not-cascaded reasoning applied one level down, for the price of one part
and a few cm².

**Note 5 — the MCLK fanout buffer moves to a clean rail.** The LMK1C110x is a 1.8/2.5/3.3 V part
and was never a 5 V load, so the v0.1 placement on +5V_D was wrong on its face (F22). More
importantly it is the most jitter-critical device in the clock tree (§3 **[HARD]**), and its
7.5 fs additive jitter figure is specified on a clean supply. **Put it on +3V3_CLK** *(v1.6 — F33 gave the fanout its own rail; this line said +3V3_A, which F46 deleted)*, **not the +3V3_D
switcher.**

- All battery-facing regulators AEC-Q100.
- Load-dump: design to survive ISO 7637-2 pulses at the input **[HARD]**.

### 7.2 Turn-on sequence [HARD]

1. Remote-in asserted (or signal-sense) → protected rails enable
2. Digital rails up → ESP32 boots
3. ESP32 releases DSP reset
3a. *(v0.5, F20)* **ESP32 configures the DSP PLL** — 0xF000 `PLL_CTRL0`, 0xF001 `PLL_CTRL1`,
    0xF002 `PLL_CLK_SRC`, 0xF003 `PLL_ENABLE` — **then polls `PLL_LOCK` (0xF004, Bit 0) until set,
    with a 15 ms timeout**, before any program write.
    **Why this step exists:** while the PLL is locking, the DSP's SPI and I2C slave control ports
    are *inactive and every write fails*. Worst case is 10.666 ms at 48 kHz, typically ~3.5 ms.
    Firmware that releases reset and begins the slave boot immediately has its writes silently
    discarded — and it presents as an SPI wiring fault.
    **Timeout is a distinct fault code, not a retry loop.** A PLL that will not lock means the XO
    or its supply is broken, and no amount of retried writes repairs that.
4. ESP32 slave-boots the program over SPI, verifies readback
5. **Converter config phase, reordered so the wait costs nothing** *(v1.0, F30)*:
   - **5a-pre.** **MCLK MUST ALREADY BE RUNNING** *(v1.7, V-04)*. The AK5574's datasheet:
     *"After exiting reset (PDN pin L→H) upon power-up, the AK5574 is in power-down state
     **until MCLK is input**."* **Fourth member of the F20/F30 family** — a [HARD] sequence step
     whose precondition was not written down.
     **SATISFIED BY CONSTRUCTION, NOT BY A STEP.** The clock tree runs from +3V3_CLK off
     +6V2_A, which is up before the MCU finishes booting, and the fanout's `1G` straps high per
     its F21 disposition — so **the clocks free-run from analog-rails-up and no firmware
     ordering can get this wrong.** A step that *can* be misordered was deliberately not
     created. **Verify at bring-up** rather than sequence it: `BRINGUP.md` checks MCLK at the
     ADC pin before the first PDN release.
     *What would break it:* gating the fanout from an MCU GPIO — see the clock sheet, where
     that proposal will arrive.
   - **5a.** Release the AK5574 `PDN` **first, at the top of the phase.**
   - **5b.** **Hold the entire I2C0 bus quiet for ≥12.5 ms** — the max of the AK5574's 10 ms
     register-write lockout and its 583/fs ≈ 12.1 ms initialisation at 48 kHz.
     **Why bus-wide and not just the AK5574:** during this window the part may emit instantaneous
     pulses on its digital pins, and AKM directs that *"data transmission with a device on the same
     3-wire serial/I2C bus should be avoided in this period."* Traffic to the AK4458s, ADS1015 or
     the temp sensor can be corrupted by a device that is not being addressed.
     **A bus-noise edge that looks like a START is the same hazard the AK5574 documents against
     itself in 3-wire mode — here it is on the other foot.**
   - **5c.** **The wait is free if the firmware interleaves.** The DSP program load over SPI
     (step 4) is bus-independent and takes longer than 12.5 ms anyway; run the quiet window
     underneath it. By the time slave-boot readback verifies, I2C0 is legal again. **Wall-clock
     cost zero; the cost of *not* knowing this is a day of "why does the second DAC sometimes lose
     its filter config."**
   - **5d.** Then configure ADC and DACs in one pass, DACs held in soft-mute.
5. Analog rails confirmed in-window (rail monitor) → output mute released, DAC soft-unmute ramp
6. Remote-out asserted after configurable delay (default 500 ms post-unmute)

### 7.3 Turn-off sequence [HARD]

1. Remote-in drop detected → remote-out released immediately (amps mute first)
2. Hard mute engaged
3. State persisted, DACs soft-muted
4. Rails allowed to fall

**No audible pop at either transition is an acceptance criterion, not a nice-to-have.**

---

### 7.4 Mute is the zero-energy state [HARD] *(v0.3)*

**The muted state must require no energy to hold.** §7.3 describes the orderly shutdown, but that
is not the only path rails collapse by: ignition crank sag, a blown fuse, a harness fault, a
pulled connector. Those paths involve no MCU participation at all. If holding mute costs energy,
every one of them ends in whatever the dying DACs and op-amps produce, reaching the amplifiers
unattenuated.

Therefore: **de-energised = muted**, by construction, for whatever element is chosen. The
sequencing in §7.2/§7.3 is how the *orderly* path is made quiet; §7.4 is how the disorderly path
is made quiet. Both are required, and only §7.4 survives a fault.

This was implicit in v0.1's "no audible pop is an acceptance criterion, not a nice-to-have" and is
now explicit because it turned out to decide the mute topology outright (§6.4).

**The analog rails fail in a safe order by construction** *(v1.3, F39)*. This is the same
principle as the paragraph above, applied to the supply instead of the mute element, and it was
a by-product of the topology rather than a goal of it — which is why it is written down here
rather than left in the power section.

The hazard is a **partial** rail failure, not a total one. The shunt mute element is held *off*
by a bias derived from −13V5_A, so a state in which **+13V5_A dies while −13V5_A survives** is
actively dangerous: the op-amps have one rail, their outputs slam to it, and the mute is being
held open by the rail that is still alive. A total collapse is safe; this specific half-collapse
is not.

Two independent battery-fed converters can produce that state and sit in it indefinitely.
**The cascade cannot**: −15V5_A is derived from +15V5_A, so the negative rail has no source of
energy once the positive one is gone. The dangerous combination is not made unlikely, it is made
**unreachable** — the transient case during discharge is bounded by capacitor decay and is the
same class as any orderly power-down.

*Generalisation worth carrying to other boards:* **where a protective element is biased from one
rail and the thing it protects runs from another, the rails must be ordered by construction, not
by sequencing firmware.** Firmware is not present for the disorderly paths §7.4 exists to cover.

**How much depth, and for how long** *(v0.4)*. The requirement is bounded, not indefinite, because
**remote-out is itself fail-safe by construction** — §7.3 line 1 is an energised high-side driver
that de-energises the instant rails sag, before anything else on the board notices. Downstream
amplifiers mute on remote loss within their own turn-off time. So the mute only has to suppress
the dying DAC below audibility for the window between **our** rails sagging and **the amp's**
remote-mute engaging — typically tens to a couple of hundred ms.

The source in that window is not full-scale programme material; it is whatever a brown-out-
resetting DAC emits, usually well under −20 dBFS equivalent. **V-16 must therefore model the whole
stack — DAC residual × mute attenuation × amp gain × amp mute latency** — using a pessimistic
latency, since that number belongs to someone else's amplifier and varies by model.

Note this is a different question from §12's "< 10 mV transient at outputs", which is measured at
**our** outputs and so does not involve amp gain at all. The 10 mV figure is a measurable proxy;
the stack above is the actual requirement. Keep both — the proxy is what gets scoped on the bench,
and the stack is what says whether the proxy was set correctly.

### 7.5 EMC posture *(v0.3, F6)*

**Design to FCC Part 15 Class B practices. No formal chamber testing for v1. CISPR 25 is out of
scope** — that is OEM territory, and this design took the industrial fork at §7.0.

The BM83SM1 and ESP32-S3-WROOM-1 carry their own modular RF certifications, which is a large part
of why they were selected; the board inherits that and must not compromise it (§8 keepouts).

Practical consequences for layout and capture:

- **Spread-spectrum stays enabled on the bucks.** §3's prohibition is on the *audio clock tree*,
  not on the power stages. These are different nets and the distinction is deliberate.
- **Input LC filtering does double duty** — ISO 7637-2 transient survival (§7.1) and conducted
  emissions.
- **The RCA ground-field RC to chassis (§6.3) is the emissions relief valve.** Treat it as an EMC
  component, not only a ground-loop measure.

---

## 8. Connectors & External IO

- 4× RCA in + speaker-level strip terminal (shared front end, §6.1)
- 12× RCA out
- SPDIF coax RCA in, transformer-coupled, **direct to `SPDIFIN` (pin 4)** *(v0.8, F26)*:
  RCA → 75 Ω termination → **1:1 pulse transformer (PE-65612 / PT-class — part number belongs on
  the connector/magnetics list, not left as an unsourced symbol)** → **AC coupling capacitor** →
  pin 4. Optional coax out from `SPDIFOUT` (pin 5) as a stuffing option; no external transceiver
  either way.
  - **The AC coupling capacitor is required by the ADAU1466 datasheet [HARD]** *(v0.9)*. It must
    carry that annotation on the schematic, not merely exist. **A component that is
    required-by-datasheet but looks optional-by-topology is exactly what a future "simplification"
    deletes** — the transformer already provides DC isolation, so the cap reads as redundant to
    anyone who has not read p.74.
  - Receiver input is a comparator centred at IOVDD/2 needing **≥200 mV p-p**; transformer-coupled
    consumer coax clears this with wide margin. Logged as margin, no action.
  - *Note for a future reader:* the consumer-not-AES3 caveat is about **specification compliance,
    not compatibility**. AES3 and S/PDIF share biphase-mark framing; the difference is level and
    impedance (AES3: 2–7 V into 110 Ω balanced). A transformer front end handles pro sources
    **better** than most consumer inputs would. **Do not let the caveat later be read as "pro
    sources will not work."**
- Power: keyed automotive connector — BATT, GND, REM-IN, REM-OUT minimum
- USB-C (ESP32-S3 native USB): debug/flash/console
- BT antennas: BM83SM1 onboard antenna — enforce module keepout **[HARD]**; ESP32-S3-WROOM-1
  onboard antenna with its keepout **[HARD]**. Separate the two antennas as far as board geometry
  allows; both radios are 2.4 GHz and will coexist but shouldn't be stacked.
- Test headers: spare TDM ports (§4), UART consoles (ESP32 + BM83), I2C, resets

---

## 9. Monitoring & Diagnostics

- ~~Rail voltage dividers → ESP32 ADC~~ *(v0.3, F16)* — **rail voltage dividers → ADS1015-class
  4-channel I2C ADC on I2C0**, covering VBATT, +13V5, −13V5 and **+5V_A** *(v1.6, F46 — was 3V3_A, a rail that no longer exists)*. The ESP32-S3's own ADC is
  the module's known weak organ, nonlinear and noisy, and §7.2 step 5 gates output unmute on this
  reading. The dividers themselves are unchanged; only the converter behind them moves.
  −13V5 is brought into range by a divider referenced to a positive rail rather than to ground —
  one resistor network, no op-amp, provided the reference is chosen correctly. Moving these four
  channels off the SoC also returns GPIO to the §5 pin budget, which helps F13.
- **TMP461-class remote-diode temp sensor on I2C** *(v0.8, F27 — replaces TMP102)*. Local channel
  near the output stage as before, **plus its remote channel wired to the ADAU1466's thermal diode
  on pins 63/64 (`THD_M`/`THD_P`)**. The DSP junction temperature is the thing §9's thermal
  protection exists to guard, and a local-only sensor measures the air near it instead.
  **[VERIFY]** the chosen variant's address straps against the `STATE.md` §9 bus map — the 0x48
  range already holds the ADS1015, and two parts have already default-collided there once
- All resets and mute states MCU-readable
- One status RGB LED, MCU-driven

---

## 10. Net Naming Conventions

- Audio serial: `TDM_IN0_BCLK/LRCLK/DATA`, `TDM_OUT0_*`, etc. per §4 port numbers
- Clocks: `MCLK_XO`, `MCLK_ADC`, `MCLK_DAC1`, `MCLK_DAC2`
- Control: `SPI_DSP_*`, `I2C0_SDA/SCL`, `UART_BM83_TX/RX`
- Analog channels: `AIN1_P/N` … `AIN4_P/N`, `AOUT1` … `AOUT12` — channel numbers match the TDM slot
  map in §4, no remapping between schematic and slot assignment **[HARD]**
- *(v0.2, F10)* To state the mapping unambiguously: the [HARD] rule means **schematic net names
  match system channel numbers**. Slot assignment within each DAC is defined by §4 and by this
  line: **AOUT1–6 occupy AK4458 #1 TDM slots 1–6; AOUT7–12 occupy AK4458 #2 TDM slots 1–6.**
  So AOUT7 is device #2, slot 1 — the net is still named `AOUT7`, never `AOUT1`.
- Rails exactly as named in §7.1

---

## 11. Open Items / Decisions Delegated to Designer

- AKM vs TI converter final selection pending lead-time check (§2)
- BM83 I2S master/slave final config (§3 **[VERIFY]**)
- Relay vs FET output mute (§6.2) — designer's call with THD justification
- SEPIC vs dual-boost topology for ±13V5_A — designer's call, noise budget: < 50 µVrms
  20 Hz–20 kHz at the op-amp rails after LDO/filtering
- Board form factor / enclosure — not yet specified; assume ≤ 200 × 140 mm unless told otherwise

---

## 12. Acceptance Criteria (v1 board)

- [ ] All 12 outputs: ≥ 4.5 Vrms before clip, THD+N ≤ 0.003 % @ 1 kHz, 2 Vrms
- [ ] *(v0.4)* All 12 outputs: **CCIF twin-tone IMD ≤ 0.003 %** — 19 kHz + 20 kHz at 2 Vrms,
      difference product measured at 1 kHz. **This is the criterion that actually exercises the
      mute shunt's nonlinear off-capacitance.** 1 kHz THD is blind to it because the mechanism is
      negligible at 1 kHz; a 20 kHz THD test would be blind to it too, because its harmonics land
      at 40/60 kHz, outside the measurement band. The twin tone puts the product **in band**,
      where it cannot be forgiven. Added alongside the 1 kHz line, not replacing it
- [ ] Output noise floor ≤ −105 dBV A-weighted, muted
- [ ] No audible pop on power-up/down (scope-verified < 10 mV transient at outputs)
- [ ] BT A2DP stream glitch-free ≥ 1 hr (ASRC path validation)
- [ ] SPDIF lock across 32/44.1/48/96 kHz sources — **two tiers** *(v0.9)*:
      - **(a)** `SPDIF_LOCK_DET` 0xF600 and `ASRC_LOCK` 0xF580 poll clean at every rate. Fast
        construction-check; makes the bench sweep quick.
      - **(b)** **One end-to-end pass** — tone in via coax, level verified at an output.
      **(a) does not replace (b).** The registers prove *lock*, not *audio*: a receiver locked but
      routed to the wrong ASRC slot polls perfectly while delivering silence. The polls make the
      sweep fast; they do not remove the one listen. Receiver lock range is 18 kHz–192 kHz.
- [ ] Slave-boot + safeload parameter writes verified over SPI at target clock
- [ ] Survives ISO 7637-2 test pulses (or documented protection analysis if untested)
- [ ] **Load-dump capability is a BOUNDED CLAIM, stated by the table rather than assumed**
      *(v1.4, F42)*. ISO 7637-2 pulse 5 for a 14 V powertrain is **U<sub>S</sub> = 65–87 V,
      R<sub>i</sub> = 0.5–4 Ω, t<sub>d</sub> = 400 ms** (Vishay 88490 Table 1) — the commonly
      quoted 35 V is the *suppressed* level, not the pulse. With the SM8S24A-class clamp and its
      63.5 mΩ dynamic resistance, against P(400 ms) = (175 − T<sub>mount</sub>)/0.30 from the
      part's transient thermal impedance:

      | Condition | I | V_clamp | P | Verdict |
      |---|---|---|---|---|
      | Suppressed, U<sub>S</sub>\* 35 V, R<sub>i</sub> 2 Ω | 3.3 A | 28.3 V | 95 W | **passes, 3–5×** |
      | Unsuppressed, 79 V, R<sub>i</sub> 4 Ω | 12.5 A | 28.9 V | 362 W | passes cold, **marginal hot** |
      | Unsuppressed, 79 V, R<sub>i</sub> 2 Ω | 24.7 A | 29.7 V | 732 W | **exceeded** |
      | Unsuppressed, 87 V, R<sub>i</sub> 0.5 Ω | 105 A | 34.7 V | 3631 W | **exceeded 7–12×** |

      **Multi-pulse (ISO 16750-2) closed by analysis — V-29** *(v1.5)*. The vendor publishes no
      multi-pulse curve for this part, so this closure uses **§12's own escape clause, written at
      v0.1: "or documented protection analysis if untested."** The assumptions are ours, tagged as
      such. **Per pulse**, the suppressed row is 95 W × 400 ms into R<sub>θJM</sub> ≈ 0.30 °C/W →
      **ΔT<sub>J</sub> = 28.5 °C**, i.e. T<sub>J</sub> = 53.5 °C from a 25 °C mount and 113.5 °C
      from 85 °C, against a 175 °C limit. **Between pulses**, 10 pulses at 1-minute intervals is a
      **0.67 % duty cycle → 0.63 W average against the part's 8 W steady-state rating, 13×
      headroom**, so the junction returns to baseline and heating does not accumulate. **The
      10-pulse case therefore reduces to the per-pulse case, which passes with 60 °C of margin.**
      *Assumptions carried:* R<sub>θJM</sub> read off the transient-impedance curve at 0.4 s, and
      a mount temperature that depends on the copper poured under the tab — see (ii).

      **Two caveats travel with this table and must not be dropped from it:**
      **(i) the multi-pulse result above is ANALYSIS, not a vendor curve.** ISO **16750-2** superseded the load-dump test with
      **10 pulses in 10 minutes**, and repeated clamping measurably degrades capability. The 3–5×
      margin on the suppressed row is where that has to come from — likely sufficient, not yet
      evidenced (**V-29**). **(ii) The numbers assume the recommended pad.** Vishay ties these
      capability figures to *"the recommended pad size as listed in the datasheet"*; the DO-218AB
      land is **15.30 × 10.70 mm** with the **anode tab poured into ground**. **Shrinking that pad
      at layout makes this criterion false** — it is an electrical input, not an outline.

      **Therefore: this board is specified for vehicles with central load-dump suppression.**
      It is not rated for unsuppressed pulse 5 except at the high-R<sub>i</sub> end. This is a
      scope statement with evidence behind it, and it must appear in the G7 note and in any
      installation documentation — **an unstated environmental limit is the same defect as an
      unstated fuse.**
- [ ] **Reverse battery is a fuse-clearing event, by design, and is documented as such**
      *(v1.4, F42)*. The series FET protects everything downstream, but the TVS sits ahead of it
      and forward-conducts on reverse, clearing F1. Seamless recovery was evaluated and
      **rejected on a thermal result, not on cost**: moving the TVS behind the FET routes the
      full clamp current through it — 48 A for 400 ms at U<sub>S</sub> 79 V / R<sub>i</sub> 1 Ω,
      ~117 W, ~176 °C rise — which destroys the FET. Acceptance is that the board is **undamaged**
      after a reverse-polarity connection, not that it keeps running through one.
- [ ] All four analog inputs pass CMRR ≥ 60 dB @ 1 kHz in speaker-level mode
