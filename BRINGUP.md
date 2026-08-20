# BRINGUP.md — ODSP-12 / `ODSP12-MB-A`

**Purpose: sequence findings become checklist lines instead of tribal memory.**

This document exists because several findings during design were *timing and ordering*
constraints that no schematic or layout artefact can carry — they only show up as "why does this
sometimes fail." Each one below cost a datasheet read to find and would have cost a bench day to
rediscover. Entries accrete as they are found; nothing is removed once it has been learned.

Governed by `CLAUDE.md`. Cross-referenced from `REQUIREMENTS.md` §7.2 and the §5 firmware
contract.

Last updated: 2026-08-16 · covers `REQUIREMENTS.md` v1.0

---

## 0. Receiving inspection — before anything is soldered

**These are checks on the *parts*, not on the board.** They exist because a correct design can be
built from a part whose datasheet no longer describes it.

### 0.1 AK5574 date code must be ≥ `H` *(F51 / T1-104)*

**Check the fifth digit of the date code on every AK5574EN in the reel: `XXXXHXX`.**
`H` marks product made since **October 2021**. AKM changed the *recommended input bias voltage*
at that revision, and the board is built for the **revised** circuit — the 10 kΩ / 10.5 kΩ
divider on `06_analog_in`, giving 0.512 × AVDD.

**If a pre-`H` part is fitted, the board still works and nothing is damaged — it loses ~6 dB of
S/(N+D)**, because the older silicon wanted 2.5 V where this divider supplies 2.561 V.

**Why this is a receiving check and not a BOM field:** nothing on a BOM line carries a date code,
so no purchasing control exists for it. The design's assumption — *any currently-orderable
AK5574EN long postdates the H revision* — is stated on the sheet precisely so it can be checked
here rather than believed.

**Backstop if this check is skipped:** a 6 dB S/(N+D) miss lands outside `REQUIREMENTS.md` §12's
THD+N line, so acceptance catches an ancient part anyway. The receiving check exists to catch it
*before* a build rather than after one.

---

## 1. Power-up sequence gotchas

### 1.1 The DSP control port is dead while the PLL locks *(F20)*

After releasing `RESET`, **the ADAU1466's SPI and I2C slave ports are inactive and every write
fails** until the PLL locks — up to **10.666 ms** at 48 kHz, typically ~3.5 ms.

- Configure the PLL: `PLL_CTRL0` 0xF000, `PLL_CTRL1` 0xF001, `PLL_CLK_SRC` 0xF002,
  `PLL_ENABLE` 0xF003.
- **Poll `PLL_LOCK` (0xF004, Bit 0) until set, with a 15 ms timeout**, before any program write.
- **Timeout is a distinct fault code, not a retry loop.** A PLL that will not lock means the XO or
  its supply is broken; retrying writes repairs nothing.

**Failure signature if skipped:** slave-boot writes silently discarded. **It presents as an SPI
wiring fault** — expect to lose a day to the wrong hypothesis.

### 1.2 The AK5574 silences the *whole* I2C bus for ~12.5 ms *(F30)*

After releasing the AK5574's `PDN`:

- Register writes are not accepted for up to **10 ms** (16384 internal-oscillator cycles).
- Initialisation completes in **583/fs ≈ 12.1 ms** at 48 kHz.
- **During this window the part may emit instantaneous pulses on its digital pins**, and AKM
  directs that *data transmission with any device on the same bus be avoided.*

**Hold the entire I2C0 bus quiet for ≥12.5 ms** — not just traffic addressed to the AK5574. The
AK4458s, ADS1015 and temp sensor can all be corrupted by a device nobody is talking to. A bus-noise
edge that resembles a START is the same hazard the AK5574 documents against *itself* in 3-wire
mode; here it is on the other foot.

**The wait is free if you interleave.** Release `PDN` at the top of the config phase, run the DSP
program load over SPI underneath it — SPI is bus-independent and takes longer than 12.5 ms anyway
— and by the time slave-boot readback verifies, I2C0 is legal again. **Wall-clock cost zero.**

### 1.3 `RESET` and `PDN` defaults

- ADAU1466 `RESET` (pin 24) has an **internal pull-down** → the DSP is held in reset at power-up
  and must be *actively released*. Safe by default.
- ADAU1466 `SELFBOOT` (pin 34) has an **internal pull-up** → floating means *self-boot attempted*
  from an EEPROM that is DNP on v1. Strapped 10 kΩ to GND (F21).

---

## 2. BM83 configuration flash *(F32)*

**The module ships pre-configured in Embedded mode. This design is Host mode.** Several pin
meanings differ between them, so the board is drawn against our config, not the datasheet default.

**A BM83 config is firmware.** An undocumented one is state that exists, matters, and lives
nowhere — so:

- Flashed over UART using Microchip's config tool, as a **documented bring-up step**.
- **The resulting config binary is committed to this repo** alongside the firmware it pairs with.
- First article flashed at bring-up by the operator.
- Board support: the UART already routes to the ESP32; the module's programming-mode strap access
  is designed in rather than improvised. **Pin 31 (`P3_4/UART_RTS`) is also the Application/Test
  mode strap** — populated resistor for normal mode, DNP position for test mode, **idle levels
  annotated on the sheet** per the F28 rule.

Factory-programmed parts are the right answer at a volume this project does not have.

---

## 3. Acceptance sequence notes

### 3.1 SPDIF lock is two-tier *(v0.9)*

- **(a)** `SPDIF_LOCK_DET` 0xF600 and `ASRC_LOCK` 0xF580 poll clean at 32 / 44.1 / 48 / 96 kHz.
  Fast construction-check; makes the sweep quick.
- **(b)** **One end-to-end pass** — tone in via coax, level verified at an output.

**(a) does not replace (b).** The registers prove *lock*, not *audio*: a receiver locked but routed
to the wrong ASRC slot polls perfectly while delivering silence.

### 3.2 Runtime signals worth wiring into the API from day one

- **`SPDIF_LOSS_OF_LOCK` 0xF605** — the input-switching debounce signal. Retrofitting it after
  discovering the need on a bench is the expensive order.
- **`OVF` (AK5574 pin 30) → ESP32 GPIO** *(F29)* — summary input-clip flag across all four
  channels at −0.3 dBFS, same group delay as the ADC. **Per-channel attribution comes from DSP-side
  metering on the TDM stream**, not from I2C: one code path feeds both the clip events and the
  level meters.

---

## 4. Checks added 2026-08-16, from the schematic-capture session

**Before the first `PDN` release — MCLK must already be running** *(V-04, §7.2 step 5a-pre)*.
Scope MCLK **at the ADC pin**, not at the buffer output. The AK5574 stays in power-down until
MCLK is input, so a dead clock tree presents as "the ADC never responds on I2C" — which reads
like a bus fault and is not one. **This is satisfied by rail ordering, so the check is a
verification, not a sequencing step**; if it ever fails, the cause is upstream of firmware.

**Rail testpoints TP1–TP13** carry their §7.1 names on silk. One namespace across silk, schematic
and this file, so bring-up is a multimeter walking a checklist. *(They are real components now —
they were bare labels until ERC caught it, and a label has no footprint.)*

**The `I2C_ALERT_N` wire-OR** carries TMP461 `ALERT` and PCF8574 `INT`. A low line means *"go read
I2C"* and does not say which device — read both. **`RAILMON_ALERT` is deliberately separate**: a
rail fault is the urgent one and must not need a bus transaction to identify, because the bus may
be what is failing.

**I2C address sweep at first power** — expect exactly **0x10, 0x11, 0x12, 0x20, 0x48, 0x49**.
Anything else, or a missing 0x12, means the AK4458 address straps are wrong. *(0x12 was a real
collision found by re-emitting the §9 map; both DACs answered at 0x11.)*

**+5V_A is now the fourth monitored rail** *(F46)*, replacing the deleted +3V3_A. It feeds all
three converters' `AVDD` directly, so it explains more field symptoms than any other single
analog voltage.

**Mute walk, with the rails deliberately collapsed** — not an orderly shutdown:
1. Kill +5V_D only → the photoMOS LED dies → **series opens**. Verify the path is broken.
2. Kill −13V5_A only → gate bias dies → **shunt closes**. Verify the residual is shorted.
3. Neither step involves the MCU. If either needs firmware, the topology was built wrong.

**CCIF twin-tone (19 + 20 kHz) is the acceptance test that SEES the mute shunt's off-capacitance
and the input ESD clamps' nonlinearity** — both 1 kHz and 20 kHz THD are blind to them. Two
independent mechanisms, one measurement.

---

## 4b. INDUCED TESTS — the fault paths, because reasoning is all we have until they run

**Added 2026-08-20 (adversary 040 / F83).** Every check below justifies a *closed* finding whose
argument rests on a **behaviour, not a value** — a state the board is designed never to enter.
**F76 is why this section exists:** the input clamps were miswired for the entire life of the
design, and F48's justification could not be tested because the state that would exercise it was
unreachable. Nothing detected that. **A closed finding whose mechanism has never run is not a
verified one.**

**These are one-time, cheap, and they convert reasoning into observation. Do them before the
acceptance sequence, not after.**

| # | Induce | Expect | Verifies |
|---|---|---|---|
| **4b.1** | Drive an analog input hard toward each rail through a current-limited source (target the F49 case, ~31 mA) | Node clamps at **V_rail + V_F ≈ 14.4 V**, *not* inside ±14 V. **That is correct** — protection is by **current limiting**, not voltage clamping. Confirm the INA1650 survives and that its input current stays sub-µA | **F48 / F49 / F76 / F79.** F79 corrected the recorded mechanism; this is the first time the clamp will ever have conducted |
| **4b.2** | Kill `MUTE_BIAS_N` / de-energise the mute with signal present | Output goes quiet **by construction**, both series and shunt. Measure residual against the §12 mute-depth line | **§6.4 [HARD] zero-energy mute.** Justified *entirely* by behaviour when power dies |
| **4b.3** | Cut power abruptly (pull the connector) at full output | No audible pop; remote-out drops **first**. §7.4 is the only path that survives a pulled connector | **§7.2/§7.3/§7.4.** The orderly sequence does not test this |
| **4b.4** | Pull each `PG` low individually; hold `EN` and confirm the sequence refuses to advance | Downstream rails stay off. **Verifies what holds when the sequence does *not* run** | **F34 / F20 / F30 sequencing preconditions** |
| **4b.5** | Interrupt `LRCK` briefly during playback | AK5574 self-resets and resynchronises (T1-132: live only in **slave** mode, which `MSN` = GND selects). **Note the discontinuity — nothing on this board reports it** | **F65.** A circuit that only acts on an anomaly, and which nothing watches |
| **4b.6** | Power up with each mode strap left floating in turn | No behavioural change — **all six are inert in I2C control mode** (T1-132). If anything *does* change, T1-132's scope reading is wrong | **F68 / T1-132.** A negative test for a claim we made from one sentence |

**Two that cannot be induced on a bench, recorded so nobody mistakes absence for coverage:**

- **F39's rail-cascade ordering** — *"−15V5 cannot outlive +15V5, so the op-amp rails fail in the
  only safe order by construction."* You cannot easily make −15V5 outlive +15V5 on a bench, so **the
  by-construction argument is load-bearing forever** and deserves a second reader rather than a test.
- **F1 / SM8S load-dump capability** — §12's table is an *analysis*, not a measurement, and
  unsuppressed pulse 5 is not something to reproduce on a desk. The bounded claim stands as written.

---

## 5. Open items that will land here

- V-16 disorderly-shutdown transient measurement, which anchors the mute-depth requirement **and
  picks between the DN2540 and LND150 shunt candidates** — the stack is DAC residual × series-open
  isolation × shunt divider × amp mute latency, judged against the CCIF distortion budget.
- V-27: the LM5156-Q1 / LM61460-Q1 **pulse-skip onset current and its repetition rate**. Neither
  datasheet states it. Bounded by analysis, not closed — the analog rails idle near 50 mA against
  a 200 mA budget, i.e. permanently at ~25 % load.
- **V-29's multi-pulse load dump was closed BY ANALYSIS**, using §12's own escape clause. If a
  chamber test ever happens, this is the line it validates.
- ~~`+3V6_BT` sizing~~ and ~~`BAT_IN` without a battery~~ — **both closed** (F31): 59 mA worst
  case against a 300 mA LDO, and the datasheet blesses any host rail as the source.
