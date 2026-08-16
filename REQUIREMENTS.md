# ODSP-12 — System Architecture & Requirements

**Project:** ODSP-12 — open DSP, 12 out. Custom automotive DSP, 4 analog in / 12 analog out,
BT audio + wireless control
**Part number:** `ODSP12-MB-A` · **Revision scheme:** A/B/C… for fab revisions, running change
log in git rather than rev-suffix soup
**Doc status:** v0.7 — architecture baseline for schematic capture *(capture begun)*
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

Unchanged and still open at v0.7: F4 (impedance targets), F12, F13, F21 (accepted, lands at
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
| SPDIF RX | AKM AK4118A | 8-input mux | Coax input; spare inputs allow future optical |
| SPDIF TX (optional) | WM8804 | | Stuffing option only — DNP on v1 unless requested |
| Diff line RX | **2× INA1650** *(v0.2)* | 2ch/pkg → 4 channels for 4 diff inputs | High CMRR speaker/line-level front end |
| Output buffers | **OPA1656** *(v0.2 — OPA1612 alternate dropped)* | 2ch/pkg, 12 pkgs min | Diff-to-SE conversion + reconstruction filter. JFET input; high Zin relaxes the filter network. Filter values computed against OPA1656 only |
| Master clock | 24.576 MHz low-jitter XO (e.g., SiTime SiT8208 or Crystek CCHD-575 class) | 3.3 V CMOS | Single clock master, see §3 |
| CAN PHY (optional) | NXP TJA1051T-Q1 | DNP stuffing option | Future head-unit / SWC integration |
| EEPROM | 25AA1024 SPI EEPROM | DNP option | Self-boot fallback if MCU absent |

**[VERIFY]** AKM part availability/lifecycle status at time of capture; PCM1865 (ADC) and
PCM1690 (DAC, AEC-Q100) are the approved TI substitutes if AKM lead times are bad.
Substitution changes TDM formats — flag if exercised.

---

## 3. Clock Architecture [HARD]

Single clock domain, one master, ASRCs isolate everything foreign.

- Master: 24.576 MHz XO → ADAU1466 MCLK input. ADAU1466 PLL configured for fs = 48 kHz core rate.
- ADAU1466 is clock master on the **synchronous** serial ports. It generates BCLK/LRCLK for:
  AK5574 (slave), both AK4458 (slave), BM83 I2S port (BM83 configured as I2S slave).
  *(v0.2 — AK4118A removed from this list, see below.)*
- **AK4118A is clock master on SDATA_IN2** *(v0.2)*. It recovers the source rate with its internal
  PLL and has no internal SRC, so it cannot be slaved to our 48 kHz BCLK without slipping samples
  upstream of — and therefore invisibly to — the ASRC. ADAU1466 SDATA_IN2 is configured as a clock
  **consumer of that link only**; the ASRC performs the rate conversion.
- AK4118A recovered clock never touches the system clock tree. It terminates at the ASRC boundary
  on SDATA_IN2 and goes no further. *(Intent unchanged from v0.1; the configuration above is what
  actually achieves it.)*
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

| DSP Port | Direction | Peer | Format | Channels |
|---|---|---|---|---|
| SDATA_IN0 | in | AK5574 | TDM4, 32-bit slots | 4 (analog in 1–4) |
| SDATA_IN1 | in | BM83 | I2S stereo | 2 (BT L/R) → ASRC |
| SDATA_IN2 | in | AK4118A | I2S stereo | 2 (SPDIF L/R) → ASRC |
| SDATA_IN3 | in | — spare — | | header/testpoints only |
| SDATA_OUT0 | out | AK4458 #1 | TDM8 | ch 1–6 used, 7–8 reserved |
| SDATA_OUT1 | out | AK4458 #2 | TDM8 | ch 7–12 used (slots 1–6), 7–8 reserved |
| SDATA_OUT2 | out | WM8804 (DNP) | I2S stereo | digital out option |
| SDATA_OUT3 | out | — spare — | | header/testpoints only |

- Spare ports OUT3/IN3 to 0.1" test headers with ground pins between signals.
- 6+6 DAC split (rather than 8+4) keeps per-chip output loading symmetric and leaves 2 spare
  channels on each DAC for rework flexibility.

---

## 5. Control Plane

ESP32-S3 is the single owner of all device state.

| Bus | Master | Peers | Notes |
|---|---|---|---|
| SPI0 (ESP32) | ESP32-S3 | ADAU1466 slave port | Slave boot at power-up; runtime parameter writes via safeload mechanism. Target ≥10 MHz SCLK. **[VERIFY]** 1466 slave-port max SCLK. |
| UART1 | ESP32-S3 | BM83 | Command/control + transparent data channel (legacy SPP tunnel if ever needed) |
| I2C0 | ESP32-S3 | AK4118A, AK5574, 2× AK4458, temp sensor, **ADS1015-class rail-monitor ADC** *(v0.3)* | 400 kHz. **[VERIFY]** each AKM part's control-port mode strapping (some are I2C/SPI selectable — strap consistently to I2C). |
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
4. **Do not mix digital-filter modes between the two AK4458s** *(F15)*. Both are slaved to the
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
| **VBATT_PROT** | reverse-FET + TVS (SMBJ24A) + LC filter | everything below | ISO 7637-2 **[HARD]** |
| **+5V_D** | **LM61460-Q1 buck from VBATT_PROT** | BM83, USB | modest — see note 1 |
| **+3V3_D** | **LM61460-Q1 buck from VBATT_PROT** *(v0.5 — "or LDO" struck)* | ESP32-S3, DSP IOVDD, converter digital sides, +1V2_CORE buck input | **2 A continuous design point** |
| **+1V2_CORE** | **dedicated buck from +3V3_D** (TPS62823-class, ≥750 mA) *(v0.5 — was "LDO from 3V3")* | ADAU1466 DVDD only | 220 mA typ, **495 mA max** |
| **±13V5_A** | SEPIC/flyback or dual-boost | op-amp stages | **200 mA cont., 250 mA peak, per rail** |
| **+6V2_A** *(v0.6, F24)* | **small Q1-rated buck from VBATT_PROT**, spread-spectrum permitted | pre-regulator for the analog LDOs only | sized at V-17 |
| **+5V_A / +3V3_A** | **LT3045-class LDOs from +6V2_A** *(v0.6)* | ADC/DAC analog supplies | **1.2 V headroom → ~200 mW class** |
| **+3V3_CLK** *(v0.7)* | **dedicated LT3045 from +6V2_A** | **MCLK fanout buffer only** — see §3 | small; sized with V-17 |

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
its own.** Cascading (+6V2 → +5V_A → +3V3_A) would multiply PSRR, but it puts the **converters'
signal-dependent AVDD current upstream of the clock buffer's supply** — a modulation path that
does not need to exist. Parallel LDOs decouple them.

**Note 7 — the MCLK fanout buffer has its own LDO: `+3V3_CLK`** *(v0.7, approved)*. A third
LT3045 from +6V2_A, feeding **only** the fanout buffer. It is the one device whose supply noise
converts directly into jitter on **every converter simultaneously**; sharing an LDO with the
converters' AVDDs would create a signal-correlated modulation path into the [HARD] §3 clock tree.
This is note 6's parallel-not-cascaded reasoning applied one level down, for the price of one part
and a few cm².

**Note 5 — the MCLK fanout buffer moves to a clean rail.** The LMK1C110x is a 1.8/2.5/3.3 V part
and was never a 5 V load, so the v0.1 placement on +5V_D was wrong on its face (F22). More
importantly it is the most jitter-critical device in the clock tree (§3 **[HARD]**), and its
7.5 fs additive jitter figure is specified on a clean supply. **Put it on +3V3_A, not the +3V3_D
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
5. ESP32 configures ADC/DACs over I2C, DACs held in soft-mute
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
- SPDIF coax RCA in (transformer-coupled), optional out (DNP)
- Power: keyed automotive connector — BATT, GND, REM-IN, REM-OUT minimum
- USB-C (ESP32-S3 native USB): debug/flash/console
- BT antennas: BM83SM1 onboard antenna — enforce module keepout **[HARD]**; ESP32-S3-WROOM-1
  onboard antenna with its keepout **[HARD]**. Separate the two antennas as far as board geometry
  allows; both radios are 2.4 GHz and will coexist but shouldn't be stacked.
- Test headers: spare TDM ports (§4), UART consoles (ESP32 + BM83), I2C, resets

---

## 9. Monitoring & Diagnostics

- ~~Rail voltage dividers → ESP32 ADC~~ *(v0.3, F16)* — **rail voltage dividers → ADS1015-class
  4-channel I2C ADC on I2C0**, covering VBATT, +13V5, −13V5 and 3V3_A. The ESP32-S3's own ADC is
  the module's known weak organ, nonlinear and noisy, and §7.2 step 5 gates output unmute on this
  reading. The dividers themselves are unchanged; only the converter behind them moves.
  −13V5 is brought into range by a divider referenced to a positive rail rather than to ground —
  one resistor network, no op-amp, provided the reference is chosen correctly. Moving these four
  channels off the SoC also returns GPIO to the §5 pin budget, which helps F13.
- Board temp sensor on I2C (TMP102 class) near output stage
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
- [ ] SPDIF lock across 32/44.1/48/96 kHz sources (ASRC path validation)
- [ ] Slave-boot + safeload parameter writes verified over SPI at target clock
- [ ] Survives ISO 7637-2 test pulses (or documented protection analysis if untested)
- [ ] All four analog inputs pass CMRR ≥ 60 dB @ 1 kHz in speaker-level mode
