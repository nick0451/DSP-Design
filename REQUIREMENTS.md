# Car Audio DSP — System Architecture & Requirements

**Project:** Custom automotive DSP, 4 analog in / 12 analog out, BT audio + wireless control
**Doc status:** v0.3 — architecture baseline for schematic capture
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

Unchanged and still open at v0.3: F4 (impedance targets), F12, F13, F15.

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
| DSP | ADI ADAU1466 (WLCSP/LQFP — prefer 72-LQFP for hand-rework) | 3.3 V IOVDD, 1.2 V core | 8 stereo hardware ASRCs, 4+4 TDM serial ports, slave-boot over SPI |
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
  requirements at 48 kHz TDM.
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

### 6.4 Mute topology *(v0.3, Q38/F11)*

**Semiconductor shunt mute is the default. A relay must now justify itself, not the reverse.**
The §7.4 zero-energy requirement, not THD, is what decides this.

- **Latching relays: prohibited.** A latching relay holds its state through a rail collapse, so a
  unit that loses power while unmuted stays unmuted through the entire decay. That is the worst
  available configuration and it is the one a latching part naturally produces.
- **Non-latching relays: permitted only wired energised-to-unmute** (de-energised = shunted).
  Fail-safe, but it holds ~12 coils × 30–40 mA for the operating life of the unit — ~0.4–0.5 A
  continuous on +5V_D and better than a watt of coil heat, permanently, to buy a THD improvement
  that sits below the DAC noise floor. If this option is taken, the +5V_D budget grows by 0.5 A
  and the LM61460-Q1 is re-checked against total load.
- **Semiconductor shunt: the default.** Must satisfy §7.4 by construction, which rules out any
  enhancement-mode device that needs drive to conduct. **Depletion-mode MOSFET or JFET**, gate
  biased off from a mute rail derived from −13V5_A: the rail's own collapse returns Vgs to 0 and
  the device conducts. The negative rail dying *is* the mute signal.

**Two numbers decide the part, and neither is a preference:**

1. **Mute depth.** With the shunt after the output series resistor, attenuation is
   `Ron / (Ron + Rseries)`. Rseries is capped near 100 Ω by the §6.2 Zout limit, so 40 dB of mute
   needs `Ron ≈ 1 Ω` and 20 dB needs `Ron ≈ 11 Ω`. Relay contacts give >60 dB trivially;
   semiconductors do not.
2. **Off-state distortion.** The shunt's nonlinear off-capacitance loads the output. It is
   negligible at 1 kHz and rises 20 dB/decade, so the §12 criterion at 1 kHz is the easy case and
   20 kHz is the real one.

These two pull against each other — `Ron × Coff` is roughly constant within a device family, so
buying mute depth costs off-capacitance. **The part is not chosen until both numbers are read off
a datasheet** (V-14, V-15) and checked against the transient magnitude the disorderly path
actually produces.

**If discrete MOSFETs are used they must be back-to-back, source-to-source.** A single MOSFET
shunting a bipolar audio signal conducts through its body diode on one half-cycle and clamps it.
This is not a refinement; it is the difference between a mute circuit and a rectifier.

PhotoMOS is an acceptable semiconductor option and brings galvanic isolation of the drive, which
keeps the mute rail out of the analog ground — worth something given the §6.3 single-plane
mandate. It must still meet §7.4, which means a **normally-closed (Form B)** part; ordinary Form A
photoMOS is enhancement-mode and fails the requirement.

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

| Rail | Source | Loads |
|---|---|---|
| VBATT_PROT | reverse-FET + TVS (SMBJ24A) + LC filter | everything below |
| +5V_D | LM61460-Q1 buck | BM83, USB, fanout |
| +3V3_D | buck or LDO from 5V | ESP32-S3, DSP IOVDD, digital sides |
| +1V2_CORE | LDO from 3V3 | ADAU1466 core **[VERIFY]** core voltage/current from datasheet |
| ±13V5_A | SEPIC/flyback or dual-boost | op-amp stages. *(v0.2, F7)* **200 mA continuous, 250 mA peak, per rail.** Budget: 24 op-amp channels × ~4 mA ≈ 96 mA; 2× INA1650 ≈ 10 mA; signal delivery 12 ch × 4.5 Vrms into 10 kΩ ≈ 6 mA, call it 10 with margin |
| +5V_A / +3V3_A | LT3045-class ultra-low-noise LDOs | ADC/DAC analog supplies |

- All battery-facing regulators AEC-Q100.
- Load-dump: design to survive ISO 7637-2 pulses at the input **[HARD]**.

### 7.2 Turn-on sequence [HARD]

1. Remote-in asserted (or signal-sense) → protected rails enable
2. Digital rails up → ESP32 boots
3. ESP32 releases DSP reset, slave-boots program over SPI, verifies readback
4. ESP32 configures ADC/DACs over I2C, DACs held in soft-mute
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
- [ ] Output noise floor ≤ −105 dBV A-weighted, muted
- [ ] No audible pop on power-up/down (scope-verified < 10 mV transient at outputs)
- [ ] BT A2DP stream glitch-free ≥ 1 hr (ASRC path validation)
- [ ] SPDIF lock across 32/44.1/48/96 kHz sources (ASRC path validation)
- [ ] Slave-boot + safeload parameter writes verified over SPI at target clock
- [ ] Survives ISO 7637-2 test pulses (or documented protection analysis if untested)
- [ ] All four analog inputs pass CMRR ≥ 60 dB @ 1 kHz in speaker-level mode
