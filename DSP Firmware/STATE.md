# STATE.md — ODSP-12 **firmware** working state

**Scope: `DSP Design/DSP Firmware/` only.** This is the firmware agent's ledger. It is *not* the
hardware `STATE.md` one level up — that file is reserved for the hardware agent and is **not read
and not written by this agent, by operator decree (2026-08-22).**

Governed by `../CLAUDE.md` (project constitution: §0 UNSET rule, §5 evidence tiers, §10 working
under compaction). Requirements source is **`../REQUIREMENTS.md` v1.8**. Both are read directly,
never from a summary — including never from a bus message.

---

## 0. LIVE STATUS — rewritten every step, never appended to

**Position:** bus leg 1 complete. Protocol agreed, hw's I2C table verified against the artefact,
five findings raised (`FW-001`…`FW-005`). Both blocking UNSETs decreed by the operator. **No
firmware code exists yet and none should — the toolchain is not installed.**

**Single next action:** **verify the ADAU1466 register addresses against `../datasheets/adau1462-1466.pdf`
(Rev. C)** — safeload `num_SafeLoad_Lower`/`_Upper`, `SOUT_SOURCEx` `0xF180`–`0xF197`, PLL
`0xF000`–`0xF004`, S/PDIF `0xF580`/`0xF600`/`0xF604`/`0xF605`. **Every one of them is currently T2,
carried on hw's word.** Then write the boot-sequence specification with its **three distinct timing
windows written as three** (see §3a).

**Sits with the operator:** the **ESP-IDF version pin** — "pinned" was decreed, the pin was not
stated. Not blocking; ask at the point it matters. **Do not infer 5.x.**

**Blocked and deliberately not started:** §7.3 power-down step order — hw reports F97 gates
F99/F98/F100/F105 and that F99 may reorder the steps. hw has committed to sending a message when
F97 and F99 resolve. **§7.2 power-up is NOT blocked and is proceeding.**

**Armed:** persistent monitor polling `agent comms/inbox/` every 15 s, one notification per new
file. Armed 2026-08-22. **Session-scoped — re-arm after any session end.** Without it an inbox
message is invisible.

**Bus ledger — shared monotonic sequence across BOTH folders:**

| seq | dir | file | topic | status |
|---|---|---|---|---|
| 001 | hw → fw | `001-…-hw-channel-protocol-and-what-shapes-firmware.md` | protocol; I2C map; six forces shaping firmware | **read, answered by 002** |
| 002 | fw → hw | `002-…-fw-protocol-confirmed-and-akm-boot-defaults.md` | protocol confirmed; Q2/Q3 decrees; I2C table verified; FW-001…005 | **sent, awaiting reply** |

**Next sequence number: 003, whichever direction it travels.**

**Open asks outstanding on hw (from 002 §7):** concurrence on FW-002/FW-003 · FW-004 write-order
consequence · AK5574 `03H` default row · FW-005 benign or not.

---

## 1. The channel — protocol SET

**`DSP Firmware/agent comms/`** — created 2026-08-22. `inbox/` we read, `outbox/` we write.

**Protocol decreed by hw in seq 001 and adopted in full (T1):**

- **Filename** `NNN-YYYY-MM-DD-<from>-<slug>.md`, `<from>` ∈ {`hw`,`fw`}.
- **`NNN` is ONE sequence shared across BOTH folders.** A shared monotonic counter makes a dropped
  message visible as a gap; per-folder numbering hides a loss because each side's own count still
  looks complete.
- **Header block** every message: `from` · `to` · `seq` · `date` · `re` · `tier`.
- **Append, never edit.** A correction is a **new** message citing the `seq` it corrects.
- **Findings: ours are `FW-###`.** hw's are `F###` and currently reach **F111**. No collision.
- **Four conduct rules, both directions:** no state document crosses the bus (**facts from one may,
  by fact and with method — that is rule 1's second sentence**) · state the method, not just the
  value · unanswered items stay named · one message per completed leg.
- **Both sides' claims are T2 on arrival.** Validate before agreeing *and* before dismissing.

**Distinct from `../CLAUDE.md` §9's adversary bus** (at 092 on its own counter). Two channels, two
counters, no interaction.

---

## 2. T1 register — what is established, and how

| # | Fact | Method |
|---|---|---|
| **T1-F01** | `DSP Firmware/` was empty at session start | `ls`, 2026-08-22 |
| **T1-F02** | `../REQUIREMENTS.md` is at **v1.8**, dated 2026-08-21; two [HARD] amendments (§3 oscillator, §4 audio format) | read doc-status line + revision history directly |
| **T1-F03** | §4 audio-format amendment text matches hw's quote **verbatim**, incl. *"The exclusion is not optional"* | read §4 body directly |
| **T1-F04** | **TOOLCHAIN: ESP-IDF, bare, pinned version.** Not Arduino, not PlatformIO | **operator decree 2026-08-22** |
| **T1-F05** | **No ESP-IDF on this machine; `IDF_PATH` unset.** PlatformIO *is* present (`espressif32@6.5.0`, `framework-arduinoespressif32@3.20014.231204` = Arduino core 2.0.14 / IDF 4.4.x), but ships **only `toolchain-riscv32-esp` — no Xtensa toolchain. The S3 has never been built for here** | probed the machine directly |
| **T1-F06** | **No SigmaStudio project exists yet.** Firmware builds against the ADAU1466 datasheet behind a **defined loader interface**; the blob is fitted later | **operator decree 2026-08-22** |
| **T1-F07** | I2C0 device straps, all six devices — see §3b. Refs `U40`/`U51`/`U52`/`U43`/`U11`/`U12` | `kicad-cli sch export netlist --format kicadsexpr`, state-machine pass over `(nets` |
| **T1-F08** | **AK5574 is in I²C control mode by strap**: `U40` pin 42 (`I2C`) → `+3V3_D`, pin 41 (`PSN`) → `GND` = Table 22 "I2C Bus" | netlist + AK5574 p.56 Table 22 |
| **T1-F09** | **AK5574 `MSN` (pin 24) → `GND` = SLAVE.** MSN is the **one** mode input no register overrides | netlist + AK5574 p.31, p.56 |
| **T1-F10** | Schematic's cited datasheet revisions (`015016764-E-03`, `014011794-E-02`) **match the PDFs read** | netlist properties vs PDF footers |
| **T1-F11** | AK4458 register space: `00H`–`14H` writable, Note 35 bars `15H`–`1FH` | AK4458 p.74, page image |

**Datasheet revisions used:** AK5574 `015016764-E-03` (2022/02) · AK4458 `014011794-E-02` (2017/07).
**Method for every register value below: PDF page rendered and read as a page image, never recalled.**

---

## 3. The boot problem — what firmware must actually do

### 3a. THREE distinct timing windows. They are NOT the same window and must not be merged.

| # | Window | Bus | Cause | Tier |
|---|---|---|---|---|
| **W1** | **PLL lock ≤ 15 ms** — configure `0xF000`–`0xF003`, poll `PLL_LOCK` `0xF004` bit 0. **Timeout is a distinct fault code, not a retry loop** | SPI0 | ADAU1466 control port dead until lock | REQUIREMENTS §5 item 1 — **T1 as a requirement**, register addresses **T2** pending datasheet |
| **W2** | **ADC wake-up ~12.5 ms** after `PDN` release (16384 internal-osc cycles, max 10 ms; init 583/fs = 12.1 ms @48 kHz). **Do not transact with ANY device on I2C0 during it** — not the DACs, expander, rail monitor or temp sensor | I2C0 | AK5574 may emit pulses on shared pins | **T2, from hw seq 001 §4.4.** Not re-derived. Consequence accepted |
| **W3** | **Reset-around-format-change.** Changing CKS/TDM/DIF **requires the ADC be in reset** (`RSTN`=0 or `PW4-1`=`0H`), and *"a stable clock must be supplied after releasing the reset"* | I2C0 | AK5574 p.31 | **T1** |

### 3b. I2C0 map — verified against the netlist, not taken on trust

| Device | Ref | Addr | Straps as found |
|---|---|---|---|
| AK5574 ADC | **U40** | **0x10** | pin 32 → `GND`, pin 34 → `GND` |
| AK4458 #1 (AOUT1–6) | **U51** | **0x11** | pin 12 → `GND`, pin 15 → `+3V3_D` |
| AK4458 #2 (AOUT7–12) | **U52** | **0x12** | pin 12 → `+3V3_D`, pin 15 → `GND` |
| PCF8574T expander | **U43** | **0x20** | A2,A1,A0 → `GND` |
| ADS1015 rail monitor | **U11** | **0x48** | ADDR → `GND` |
| TMP461 temp | **U12** | **0x49** | A0 → `+3V3_D`, A1 → `GND` |

All on `I2C0_SDA` / `I2C0_SCL`. `0x13` free but **the AKM prefix is full at four** (T2, hw).
**Scope limit: strap wiring is T1; strap→address decode for ADS1015 and TMP461 is T2 from hw** —
their pins go where hw said, but I have not read TI's address tables.

**hw's F26 two-DACs-at-0x11 defect is fixed in the copper, not only in the notes** — U51 and U52
carry opposite strap pairs. Checked specifically because the symptom would present as a firmware
bug ("DAC #2 ignores its filter configuration").

### 3c. Power-on defaults — what is wrong before firmware touches anything

| Part | Register | Default | Against the design? |
|---|---|---|---|
| **AK4458** | `00H` D0 `RSTN` | **`0` = Reset** | **YES — boots HELD IN RESET.** Firmware must write 1 |
| **AK4458** | `00H` D3:D1 `DIF2-0` | **`110` = Mode 6, 32-bit MSB justified** | **No — but conditional. See FW-004** |
| **AK4458** | `0AH` D7:D6 `TDM1-0` | `00` "Normal" | **YES** — §4 [HARD] requires TDM8. **T2, default row not read** |
| **AK4458** | `01H` D0 `SMUTE` | `0` = not muted | No. Analog mute covers the window by construction |
| **AK5574** | `01H` D0 `RSTN` | **`1` = Normal Operation** | **Boots RUNNING — the OPPOSITE of the DAC** |
| **AK5574** | `02H` D3:D2 `DIF1-0` | **`00` → Table 8 row 0 = 24-bit MSB, non-TDM** | **YES — wrong word length AND wrong multiplex mode** |
| **AK5574** | `03H` D6:D5 `TDM1-0` | `0` presumed | **T2 — default row not read.** Asked hw |

---

## 4. Decisions log

| # | Decision | Why | What reopens it |
|---|---|---|---|
| FD-01 | Firmware state lives in **this** file; the hardware `STATE.md` is never opened by this agent | Operator decree 2026-08-22. Two agents writing one ledger is a lost-update race | Operator says otherwise |
| FD-02 | `agent comms/{inbox,outbox}/` under `DSP Firmware/`, separate from the adversary `bus/` | Operator instruction; keeps the two channels' counters from colliding | Operator says otherwise |
| FD-03 | Inbox watch is a **polling monitor (15 s)**, not a filesystem-event watch | Windows host, no `inotifywait`. 15 s is far below any plausible message cadence | A native watcher becomes available |
| FD-04 | **Verify hw's claims against the artefact before agreeing**, not only before dismissing | hw decreed the symmetry in seq 001 §1 and it immediately paid: their §4.2 argument was one-legged, and the AK5574's wrong defaults were absent | Never — this is the channel's point |
| FD-05 | Netlist exported to the **scratchpad**, never into `../hw/` | Read-only posture toward the hardware artefact. Nothing in the project tree was written | Never |

---

## 5. Open items

| # | Question | Blocks | State |
|---|---|---|---|
| Q1 | I2C0 address table | I2C driver | **CLOSED** — received seq 001, verified against netlist. See §3b |
| Q2 | ESP32-S3 toolchain | repo layout, build system | **CLOSED — ESP-IDF, bare (T1-F04)** |
| **Q2a** | **The exact ESP-IDF version pin** | pinning the build, CI | **OPEN, ⬜ UNSET.** "Pinned" was decreed; the pin was not stated. **Do not infer 5.x.** Ask at the point it matters |
| Q3 | DSP program binary ownership | loader design | **CLOSED — no SigmaStudio project exists yet (T1-F06).** Loader interface first, blob later |
| Q4 | Bus message format | every message | **CLOSED** — see §1 |
| **Q5** | **ADAU1466 register addresses** — safeload, `SOUT_SOURCEx`, PLL, S/PDIF | any DSP driver code | **OPEN. All T2, carried on hw's word.** Next action. **Rule 2 binds on hw's numbers too** |

---

## 6. Findings register

| # | Finding | Verdict | Tier |
|---|---|---|---|
| **FW-001** | hw §4.2 — AK5574 ignores its mode straps in serial control mode, so the [HARD] audio format exists **only** as a firmware register write | **CONFIRMED, and strengthened.** hw's argument rested on one sentence ("pins ignored"); that does not by itself establish firmware *can* set the format. Supplied the second leg: `02H` D3:D2 `DIF1-0` exists and defaults `00` (p.62). Plus structural corroboration — **CKS3-0 are multiplexed onto the I²C pins themselves** (31 `SDA/CKS0`, 33 `SCL/CKS2`, 32 `CAD0_I2C/CKS1`, 34 `CAD1/CKS3`), so the strap is **physically impossible** in I²C mode. Plus the precondition made T1 (T1-F08) | **T1** |
| **FW-002** | **The AK5574 boots wrong on BOTH counts** — `DIF1-0`=`00` → Table 8 row 0 = **24-bit MSB, non-TDM**, against §4 [HARD] 32-bit MSB and the TDM8 map. **Absent from hw's §4.3**, which covered only the DAC | **RAISED** — gap in hw's list, not an objection. Same silent-until-audio-fails signature | **T1** (the `03H` TDM default row is T2) |
| **FW-003** | **The two AKM parts' `RSTN` defaults are OPPOSITE** — AK4458 `0` (held in reset), AK5574 `1` (running) — **and the required motions are opposed**: p.31 requires the ADC be driven *into* reset to change CKS/TDM/DIF, while the DAC must be brought *out*. A firmware author generalising "AKM parts boot in reset" gets the ADC wrong, silently. Establishes **W3** as a third timing window | **RAISED** | **T1** |
| **FW-004** | **Qualifier on hw §4.3.** The AK4458's format default is **not** wrong: `DIF2-0` = `110` = Mode 6, 32-bit MSB — what §4 asks for. But the datasheet warns *"Format varies in TDM1 and TDM0."* **The trap is a default that is right BEFORE the TDM write and may not be after it** → DIF must be re-verified **after** setting TDM. **A readback that sees `110` passes in both the correct and incorrect case** — a check that cannot fail | **RAISED** — refinement, changes write **order** | **T1** |
| **FW-005** | `kicad-cli sch export netlist` warns *"schematic has annotation errors"* on every run. **Investigated before reporting: 0 refdes ending in `?`, 0 duplicate refdes.** Cause not reproduced | **RAISED, hw's domain.** T1 that the warning was emitted; **no tier on any cause.** May be benign | **T1 (emission only)** |

**Not verified this leg, named per bus rule 3:** BM83 `SDATA_IN1` exclusion (decreed, not
corroborated) · F70's AK5574 Table 9 row 26 / AK4458 Table 13 Mode 12 self-consistency (**T2**,
will read both before writing either) · §4.4's 583/fs derivation (**T2**, consequence accepted) ·
all ADAU1466 register addresses (**T2** — Q5) · §7.3 step order (**blocked on hw's F97/F99**).

---

## 7. Mistakes ledger

| # | Wrong belief | Correction | The tell that would have caught it sooner |
|---|---|---|---|
| **FM-01** | Bootstrapped `STATE.md` citing `REQUIREMENTS.md` **§5 v0.6** and **v0.9**, and treated those as current | Document is **v1.8**; two [HARD] amendments landed 2026-08-21, one of which (§4 audio format) is a firmware register setting | **The version was sitting in the doc-status line on line 7 and in the revision history at line 21. I read §5's body and never read the header.** `../CLAUDE.md` §3 says cite by section *and* version — I cited a version I had not checked. **Read the header before the section.** Caught by hw, not by me |

---

## 8. Method notes carried forward

- **A check that cannot fail is not a check that passed** (hw's F109: footprint properties written
  to library symbols instead of instances — 0 of 536 exported, and every content check passed
  because none checked the address). **FW-004 is the same shape in firmware and was found by
  looking for it.**
- **Two correct facts never brought into contact** is this project's recorded failure mode
  (`../CLAUDE.md` §0b). FW-003 is exactly that: both RSTN defaults were individually documented and
  correct; the defect only appears when they are read side by side.
- **Rule 2 binds on the other agent's numbers too.** hw's register addresses are T2 until read.
