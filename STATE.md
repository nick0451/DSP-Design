# STATE.md — ODSP-12 · `ODSP12-MB-A` rev A

Working scope, tiered fact base, open unknowns, findings, and the anti-drift ledger.
Governed by `CLAUDE.md` §5. **Read at session start. Update as work happens.**

Tiers: **T1** source of truth (verified) · **T2** highly probable (actionable, tagged) ·
**T3** likely (branchable, check quickly) · **T4** speculation (never drives work).

Last updated: 2026-08-15

---

## 0. Where we are

**Phase:** **Capture begun** (2026-08-15). Architecture specified at `REQUIREMENTS.md` v0.7,
governance closed, tooling verified. Mechanical and fabrication still unspecified — layout remains
blocked, capture does not.

**Board state:** KiCad project `hw/ODSP12-MB.kicad_pro` exists with a **10-page hierarchy**
(index + 9 sheets), all empty of components. **ERC: 0 violations.** PDF export renders 10 pages,
which is the proof KiCad *traverses* the hierarchy rather than merely parsing the root. Nothing
placed, nothing routed.

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
| `ADAU1466` | 72 + EP, 3 units (Power / Serial Audio / Control) | Table 18 rendered pp.18-21 **and** Figure 11, independently read, 100% agreement (T1-37). Generator asserts pins 1..72+EP each appear exactly once. `kicad-cli sym upgrade` = no change needed; all 3 units render to SVG | **Ready for operator eyeball** (DL-14 five-part set) |

**Layer count: ≥ 4, decreed** (F25) — a floor from the silicon, not a routing estimate. 6 stays
live. This is the first Block E slot to close, and it closed from a datasheet rather than a fab
conversation.

**Next action:** the AKM symbols — now a **pair**, not a trio: `AK5574` and `AK4458`. The
AK4118A symbol will never be built. The DL-14 personal-eyeball set drops from five parts to
**four**: ADAU1466, AK5574, AK4458, BM83SM1. Residue unchanged, none of which gates the first
sheet — V-04 ADC side + F15 phase
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
| T1-42 | **ADAU1466 S/PDIF receiver lock range: 18 kHz to 192 kHz.** Clock recovery is "completely digital". Ports designed to meet AES/EBU jitter of 0.25 UI p-p at ≥8 kHz and 10 UI p-p below 200 Hz | `adau1462-1466.pdf` pp. 74-75, rendered. Closes V-19 condition 1 |
| T1-43 | **Integrated S/PDIF RX is ASRC-coupled on-die:** "because the S/PDIF input data is most likely asynchronous to the DSP core, **it must be routed through an ASRC**". No serial port and no external recovered-clock net involved. 16 ASRC channels in 8 stereo sets; we need 2 | p.74, rendered. Closes V-19 condition 2 |
| T1-44 | **Pins 4/5 are dedicated `SPDIFIN`/`SPDIFOUT`** with no alternate/multipurpose functions and no current assignment — no conflict. RX input is a comparator centred at IOVDD/2 requiring **≥200 mV p-p**, accepting TTL or bipolar, and **requiring an AC coupling capacitor on the pin** | Table 18 + p.74. Closes V-19 condition 3 |
| T1-45 | **Integrated S/PDIF TX outputs two channels directly from the core at core rate** and **consumes no serial output port**; non-audio bits copyable from the RX or programmed. Auxiliary Output Mode (metadata onto TDM8) exists but is optional and unused. Interface meets **consumer** S/PDIF, **not AES3 professional** | p.75, rendered. Retires the WM8804 stuffing option |
| T1-46 | **S/PDIF status registers:** `SPDIF_LOCK_DET` 0xF600, `SPDIF_RX_CTRL` 0xF601, `SPDIF_RESTART` 0xF604, `SPDIF_LOSS_OF_LOCK` 0xF605, plus channel-status / user-data / validity / parity blocks 0xF610-0xF68B. `ASRC_LOCK` 0xF580, `ASRC_MUTE` 0xF581, per-ASRC ratio 0xF582-0xF589 | p.74-75. Makes §12's SPDIF-lock criterion a register poll (M3) |
| T1-41 | **Pin 3 `VDRIVE` disposition is explicit:** "If an external supply is provided directly to DVDD, **connect the VDRIVE pin to ground**." Recommended PNP, if ever used, is ON Semi NSS1C300ET4G | Table 18 p.18. **Closes the F18 loose end** — VDRIVE goes to GND, not left floating |
| T1-15 | **analog.com is unreachable from this environment** — ADAU1466 and LT3045 PDFs and the HTML product page all timed out via `Invoke-WebRequest`, `curl` and `WebFetch`; Verical 403 | Four independent fetch attempts, 2026-08-15 |

**No datasheet has been read on this project yet.** Every part parameter below is therefore T2 or
lower. See `CLAUDE.md` §5: *a part number is not a datasheet.* T1-10 is the one exception and it
rests on operator confirmation rather than the document — worth the 60-second re-check when the
AK4118A datasheet is open anyway for pin assignment, since the whole F1 disposition stands on it.

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
| V-20 | **TMP461-class variant address straps** against the §9 bus map — the 0x48 range already holds the ADS1015 | §9 v0.8 / F27 | Open — **new at v0.8.** Pick the variant from its strap table, not from aesthetics |
| V-17 | **AVDD currents for AK5574 and AK4458** — sizes the +6V2_A buck and **all three** LT3045 stages | §7.1 v0.7 / F24 | Open. Read alongside V-04's ADC side, same tables. **Sizing note:** the +6V2_A budget is the sum of +5V_A, +3V3_A **and the newly approved +3V3_CLK fanout load** — the escalation changed this buck's budget on the same turn it was raised |
| V-18 | **ADAU1466 core-supply ripple tolerance** from the electrical table — designs the +1V2_CORE buck's output filter against a number rather than vibes | §7.1 v0.5 / F18 | Open — **new at v0.5**, rides with the F18 disposition |
| V-16 | Disorderly-path transient, modelled as the **full stack**: DAC brown-out residual × mute attenuation × amp gain × amp remote-mute latency | §7.4 v0.4 | Open — bench, first board. **Bounded, not indefinite:** remote-out is fail-safe and drops first, so the window is the amp's own mute latency (tens to ~200 ms), and the source is a resetting DAC well under −20 dBFS, not programme material. Use a pessimistic latency — it belongs to someone else's amplifier |
| V-12 | BM83SM1 and ESP32-S3-WROOM-1 antenna keepout dimensions and board-edge requirements | §8 | **Partially closed → T1-31.** Both mandates confirmed: BM83 needs no copper, no component **and no ground plane** under the antenna; WROOM-1 has a keepout zone. **Dimensions live in figures** and need a `pdftoppm` render — fold into the DL-14 footprint pass, where the operator already eyeballs the BM83 keepout. **Escape hatch noted:** the **-1U** variant has no keepout because it takes an external antenna — the answer if T1-D20's antenna-separation requirement fights the outline |
