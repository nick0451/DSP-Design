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
