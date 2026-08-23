# STATE.md — ODSP-12 **firmware** working state

**Scope: `DSP Design/DSP Firmware/` only.** This is the firmware agent's ledger. It is *not* the
hardware `STATE.md` one level up — that file is reserved for the hardware agent and is **not read
and not written by this agent, by operator decree (2026-08-22).**

Governed by `../CLAUDE.md`. Requirements source is **`../REQUIREMENTS.md` v1.8**. Both read
directly, never from a summary — including never from a bus message.

---

## 0. LIVE STATUS — rewritten every step, never appended to

**Position:** four bus legs complete. **§7.3 power-down order DECREED. F70 RESOLVED — both audio
format tables now read at T1, and the ADC/DAC boot register writes are fully determined.** Eleven
findings raised (`FW-001`…`FW-011`). **No firmware code exists yet — the toolchain is not
installed.**

**Single next action:** **verify the ADAU1466 register addresses against
`../datasheets/adau1462-1466.pdf` (Rev. C)** — safeload `num_SafeLoad_Lower`/`_Upper`,
`SOUT_SOURCEx` `0xF180`–`0xF197`, PLL `0xF000`–`0xF004`, S/PDIF `0xF580`/`0xF600`/`0xF604`/`0xF605`.
**All T2; hw has confirmed they never verified them either — they came from requirements prose, not
a datasheet.** Then §7.2 turn-on ordering, then the power-down handler.

**Sits with the operator:** ESP-IDF version pin (Q2a). Not blocking.

**Sits with hw:** correct F70's DAC row to Mode 18 · FW-010 (were any layout decisions taken
against 6.144 MHz for the DAC BCLK nets, which are actually 12.288 MHz) · FW-011 logged as a
firmware invariant · FW-005 open both sides. **hw owes: F62, F65, §4.4 citation — all in their
007.**

**Armed:** persistent monitor polling `agent comms/inbox/` every 15 s. **Session-scoped — re-arm
after any session end.**

---

## 1. The channel

Protocol per hw seq 001: `NNN-YYYY-MM-DD-<from>-<slug>.md` · header block · **append, never edit** ·
findings `FW-###` vs hw's `F###` · `CLAUDE.md` §5 tiers · four conduct rules (no state document
crosses — **facts may, by fact and with method** · state the method · unanswered items stay named ·
one message per leg). **Both sides' claims are T2 on arrival.**

**NUMBERING — amended by hw seq 005 after FW-009: `hw` takes ODD, `fw` takes EVEN.** The shared
`max(seen)+1` counter had no allocator and collided on leg 3. hw's parity assignment fits the
existing history with no discontinuity (hw 001/003/005, fw 002/006). **hw also withdrew their
original 001 justification for the shared counter as wrong** — per-folder numbering does *not* hide
a drop, because the *receiver* sees the gap, and they had reasoned about the sender's view.

**Bus ledger:**

| seq | dir | topic | status |
|---|---|---|---|
| 001 | hw → fw | protocol; I2C map; six forces shaping firmware | answered by 002 |
| 002 | fw → hw | protocol confirmed; Q2/Q3 decrees; I2C table verified; FW-001…005 | answered by 003 |
| 003 | hw → fw | F97 closed (§12 two limits); F99 answered; concurs FW-002/3/4; 7 items handed over | answered by 006 |
| ~~004~~ | hw → fw | **§7.3 steps 2/3 SWAPPED by decree.** §7.4 untouched | answered by 006 |
| ~~004~~ | fw → hw | **COLLIDED** (mine 20:52:00.000 vs theirs 20:51:38.814 — theirs stands). Renamed to 006, content unchanged, disclosed in 006 §0 | superseded |
| 005 | hw → fw | FW-009 adopted, parity swapped; **F70 REOPENED**; FW-007/008 logged | answered by 008 |
| 006 | fw → hw | FW-009; §7.3 ack + no ramp-status-bit; corrects 002; closes `03H`; FW-006/7/8 | answered by 005 |
| 007 | hw → fw | *pending* — owes F62, F65, §4.4 citation | awaited |
| 008 | fw → hw | **F70 resolved**, FW-006 reasoning retracted, Mode 18 identified; FW-010, FW-011 | **sent** |

---

## 2. T1 register

| # | Fact | Method |
|---|---|---|
| **T1-F02** | `../REQUIREMENTS.md` is **v1.8**; §3 oscillator + §4 audio-format [HARD] amendments | read doc-status + revision history |
| **T1-F04** | **TOOLCHAIN: ESP-IDF, bare, pinned version** | **operator decree** |
| **T1-F05** | **No ESP-IDF here**, `IDF_PATH` unset. PlatformIO present but **no Xtensa toolchain — the S3 has never been built for on this machine** | probed directly |
| **T1-F06** | **No SigmaStudio project exists yet.** Loader interface first, blob later | **operator decree** |
| **T1-F07** | I2C0 straps, all six devices — §3b | netlist export + awk |
| **T1-F08** | **AK5574 in I²C control mode by strap** (pin 42 → `+3V3_D`, pin 41 → `GND`) | netlist + p.56 Table 22 |
| **T1-F09** | **`MSN` → `GND` = SLAVE.** The one mode input **no register overrides** | netlist + p.31/p.56 |
| **T1-F11** | AK4458 registers `00H`–`14H`; Note 35 bars `15H`–`1FH` | AK4458 p.74 |
| **T1-F12** | AK5574 `03H` default all zeros → `TDM1-0` = `00` = Normal | AK5574 p.63 |
| **T1-F13** | AK5574 `04H` default `00H` → Sharp roll-off, Normal delay, PCM. **No boot write needed** | AK5574 p.63 |
| **T1-F14** | Table 5: `CKS3-0`=`0000` = 128 fs/Quad/108–216 kHz; **`0110` = 512 fs/Normal**, = 24.576 MHz at 48 kHz | AK5574 p.33 + Table 2 p.32 |
| **T1-F15** | §4 port map: `SDATA_IN0` = TDM4; `SDATA_OUT0/1` = TDM8, 32-bit slots | read §4 table |
| **T1-F16** | **No ramp-complete status bit on the AK4458.** `DZF` is input-zero detect over 8192 LRCK = 170.7 ms | AK4458 p.61 note (4) |
| **T1-F17** | **§7.3 steps 2/3 SWAPPED**; §7.4 unchanged and not firmware's | **operator decree via hw 004** |
| **T1-F18** | **AK5574 Table 9 row 26** — TDM128 (`TDM1-0`=`01`), MSN=L, `DIF1-0`=`10` → **32-bit MSB, LRCK ↑, BICK 128 fs**, MCLK 128–1024 fs, all inputs | AK5574 p.36 |
| **T1-F19** | **AK4458 Table 13** — Mode 12 = TDM128/`DIF2-0`=`110` → 32-bit MSB, ↑, **128 fs**. **Mode 18 = TDM256/`110` → 32-bit MSB, ↑, 256 fs** | AK4458 p.35 |
| **T1-F20** | **AK4458 pin/mode requirements** (p.34): Normal = 8 ch via SDTI1-4 · **TDM128 = 8 ch via SDTI1-2, BICK 128 fs** · **TDM256 = 16 ch via SDTI1-2, BICK 256 fs** · TDM512 = 16 ch via SDTI1, 512 fs | AK4458 p.34 |
| **T1-F21** | **Both DACs wire `SDTI1` only — `SDTI2`, `SDTI3`, `SDTI4` are tied to `GND`** on U51 and U52 | netlist |
| **T1-F22** | **Table 14 Data Select**: in TDM256, `SDS2-0` picks 4 consecutive stereo pairs of 8; **only `000` = pairs 1–4, entirely on `SDTI1`** | AK4458 p.42 |
| **T1-F23** | `DCHAIN` = 0 (default) → `TDMO1/2` are inputs `SDTI3/4`. **Not daisy-chained; the copper agrees** | AK4458 p.43 Table 15 + netlist |

**Datasheet revisions:** AK5574 `015016764-E-03` · AK4458 `014011794-E-02`. **Every register value
was read from the page named, rendered as a page image, never recalled.**

---

## 3. The boot problem

### 3a. THREE distinct timing windows — do not merge. hw has adopted the framing.

| # | Window | Bus | Tier |
|---|---|---|---|
| **W1** | **PLL lock ≤ 15 ms** — poll `PLL_LOCK`; **timeout = distinct fault code, not a retry loop** | SPI0 | requirement T1; addresses **T2** |
| **W2** | **ADC wake-up ~12.5 ms** after `PDN` release — **do not transact with ANY device on I2C0** | I2C0 | **T2**, citation owed in hw 007 |
| **W3** | **Reset-around-format-change** — ADC must be in reset to change CKS/TDM/DIF; stable clock after release | I2C0 | **T1** |

### 3b. I2C0 map — verified against the netlist

`U40` AK5574 **0x10** · `U51` AK4458#1 **0x11** · `U52` AK4458#2 **0x12** · `U43` PCF8574T **0x20** ·
`U11` ADS1015 **0x48** · `U12` TMP461 **0x49**. All on `I2C0_SDA`/`I2C0_SCL`.
**Strap wiring T1; strap→address decode for ADS1015/TMP461 is T2 from hw.** hw's F26
two-DACs-at-0x11 defect **is fixed in the copper**.

### 3c. The serial links — RESOLVED (F70)

**The project counts SLOTS ON THE WIRE; AKM counts BICK RATIO. That collision is what put a wrong
mode in hw's ledger.**

| Link | §4 name | AKM mode | Row | BICK @48 kHz |
|---|---|---|---|---|
| `SDATA_IN0` → AK5574 | TDM4 | **TDM128** (`01`) | Table 9 row 26 | **128 fs = 6.144 MHz** |
| `SDATA_OUT0/1` → AK4458 | TDM8 | **TDM256** (`10`) | Table 13 **Mode 18** | **256 fs = 12.288 MHz** |

**The two converter links do NOT share a BICK rate (FW-010).** Same MCLK, same LRCK, same format —
BICK differs by 2×. `CLAUDE.md` §6's derived line (TDM8 = 12.288, TDM4 = 6.144) is correct for both.

### 3d. Boot register writes — fully determined, all read

**AK5574** (wrong on three counts, every `PDN` cycle — Note 26):

    02H:  CKS3-0 = 0110    512 fs / Normal Speed      was 0000 = 128 fs / Quad Speed
          DIF1-0 = 10      32-bit MSB                  was 00   = 24-bit MSB
    03H:  TDM1-0 = 01      TDM128 = 4 slots on wire    was 00   = Normal / non-TDM
    04H:  no write needed  Sharp / Normal delay / PCM  already correct (T1-F13)
    RSTN (01H D0) defaults to 1 = RUNNING -- opposite of the DAC (FW-003)

**AK4458** (both parts):

    00H:  RSTN   = 1       release reset               was 0 = HELD IN RESET
          DIF2-0 = 110     32-bit MSB                  already 110 -- re-verify AFTER the TDM write
    0AH:  TDM1-0 = 10      TDM256 = 8 slots on wire    was 00 = Normal  (default row T2, Q6)
    0A/0BH: SDS2-0 = 000   pairs 1-4, all on SDTI1     FW-011 -- exact bit positions T2
    0BH:  DCHAIN = 0       not daisy-chained           already 0, matches copper
    ATT7-0 boots FFH = 0 dB (full volume); SMUTE boots 0 (unmuted)

### 3e. Power-down handler — DECREED (T1-F17)

    1. remote-in drop -> remote-out released immediately
    2. state persisted, DACs SOFT-MUTED
    3. hard mute engaged, into digital silence   <- must NOT start until 2 COMPLETES
    4. rails allowed to fall

**No status bit exists (T1-F16) → elapsed-time wait forced**, which makes the ramp figure
load-bearing on a [HARD] step — and the datasheet gives two (FW-007).

    ramp_ms = ATT_STEPS[ATS] / fs      ATT_STEPS = {4080, 2040, 510, 255}
    wait    = ramp_ms x margin         unconditional, before releasing MUTE_EN

**No hard-coded `85`.** Default `ATS`=`00` → 85.0 ms (FD-06). **§7.4 is hardware's; firmware must
not be in the rail-collapse path at all.**

### 3f. Power-up facts held for §7.2 ordering (next design work)

- **DAC boots full volume, unmuted** — nothing digital backstops a boot-path bug.
- **~104 µs window (5/fs) after reset release where volume writes are INSTANT, no ramp.**

---

## 4. Decisions log

| # | Decision | Why | Reopens |
|---|---|---|---|
| FD-01 | Firmware state in **this** file; hardware `STATE.md` never opened | Operator decree; lost-update race | Operator |
| FD-02 | `agent comms/` under `DSP Firmware/` | Operator instruction | Operator |
| FD-03 | Inbox watch = polling monitor (15 s) | Windows, no `inotifywait` | Native watcher |
| FD-04 | **Verify hw's claims against the artefact before agreeing**, not only before dismissing | hw decreed the symmetry; it has now paid in both directions | Never |
| FD-05 | Netlist exported to **scratchpad**, never into `../hw/` | Read-only posture toward the hardware artefact | Never |
| FD-06 | `ATS1-0` = `00` (85.0 ms), waited in full, parameterised | FW-007 safe direction | Operator ruling on shutdown latency |
| FD-07 | Leave `005` unused rather than reuse it | hw's owed message; disclosed reservation beats reuse | — resolved by hw's parity rule |
| FD-08 | **fw takes EVEN sequence numbers** | hw decree seq 005; fits history with no discontinuity | hw |

---

## 5. Open items

| # | Question | State |
|---|---|---|
| Q2a | **Exact ESP-IDF version pin** | **OPEN, ⬜ UNSET.** Do not infer 5.x |
| **Q5** | **ADAU1466 register addresses** | **OPEN, all T2.** hw confirms they never verified them — they came from requirements prose. **Next action** |
| **Q6** | **AK4458 `0AH` TDM default row** | **OPEN, T2.** Does not change any conclusion — `10` must be written regardless |
| **Q7** | **`SDS2-0` exact bit positions** in `0AH`/`0BH` | **OPEN, T2** — read from the register map table, not yet from the definition pages |

Closed: Q1 (I2C map, verified) · Q2 (ESP-IDF, decreed) · Q3 (no SigmaStudio project) · Q4 (protocol).

---

## 6. Findings register

| # | Finding | Verdict | Tier |
|---|---|---|---|
| **FW-001** | AK5574 ignores mode straps in serial control mode; the [HARD] format exists **only** as a firmware register write | **CONFIRMED and strengthened** — supplied the missing second leg; structural corroboration (CKS3-0 multiplexed onto the I²C pins, so the strap is physically impossible) | **T1** |
| **FW-002** | **AK5574 boots wrong on THREE counts** (`CKS3-0`, `DIF1-0`, `TDM1-0`), every PDN cycle | **CONCURRED by hw**, folds in hw's F66. Target values now all read (§3d) | **T1** |
| **FW-003** | **`RSTN` defaults OPPOSITE** and required motions opposed; establishes **W3** | **CONCURRED**; hw adopted the three-window framing | **T1** |
| **FW-004** | AK4458 format default is **right before the TDM write and may not be after it**; a readback seeing `110` passes in both correct and incorrect cases | **CONCURRED.** Now sharper: `110` **does** survive here (Mode 6 → Mode 18, both 32-bit MSB, verified against Table 13) — **a fact about this value, not a property of the field** | **T1** |
| **FW-005** | `kicad-cli` "annotation errors" warning; cause not reproduced by either side | **INDEPENDENTLY CONFIRMED by hw** (562/562 unique refdes/unit, 0 path mismatches). **Open both sides** | T1 (emission only) |
| **FW-006** | *"hw's F70 BICK figures cannot both be 128 fs"* | **REASONING RETRACTED — my arithmetic assumed one data pin; AKM spreads channels across SDTI1-2, so TDM128 really is 8 ch at 128 fs. hw's Mode 12 and row 26 citations are both EXACTLY right.** **Conclusion survives for a different reason** — see FW-010 | reasoning **withdrawn** |
| **FW-010** | **The two converter links do NOT share a BICK rate.** ADC = 128 fs (6.144 MHz); **DAC = 256 fs (12.288 MHz), because `SDTI2` is grounded (T1-F21) so only TDM256/Mode 18 delivers 8 channels on one wire.** F70's DAC row should read Mode 18, not Mode 12 | **RAISED.** Resolves F70. **No schematic change needed — one wire per DAC is correct for Mode 18** | **T1** |
| **FW-011** | **`SDS2-0` must be `000` on both DACs.** In TDM256 it selects 4 consecutive pairs of 8; every value but `000` reaches into `SDTI2` = GND → silent channels. **Firmware register write, no hardware backstop, no error bit, and the failure is PARTIAL** (`001` mutes one pair; `100` mutes all eight) | **RAISED** | **T1** (bit positions T2 — Q7) |
| **FW-007** | **Ramp stated two ways in one datasheet** — p.49 `4080/fs` (85.0 ms, self-checking) vs p.61 *"4080 LRCK cycles (1020/fs)"* (21.25 ms). **Taking 85.0 ms** | **LOGGED by hw.** hw notes the safe-direction argument is the one that survives the contradiction being resolved either way | **T1** |
| **FW-008** | **The 85 ms is not a property of the part** — `ATS1-0` selects 16:1, and time scales with `ATT_DATA`. Faster ramp trades against §12(ii) | **ENDORSED by hw**, going to the operator as a correction of their framing, **not** a reopening of the §7.3 decree | **T1** |
| **FW-009** | **The shared sequence counter had no allocation authority** — both sides took `004`. **A gap is loud; a collision is SILENT** | **ADOPTED** with parity inverted (hw odd / fw even). **hw withdrew their original justification as wrong** | **T1** |

**Not verified, named per rule 3:** BM83 `SDATA_IN1` exclusion (decreed, not corroborated) ·
**all ADAU1466 register addresses (T2 — Q5)** · AK4458 `0AH` default (T2 — Q6) · `SDS2-0` bit
positions (T2 — Q7) · §4.4's 583/fs derivation (T2, owed in hw 007) · hw's F62/F65/F68/F71/F75 and
the `07H` read-modify-write item (**not started**; F68 neighbours FW-011 but is not answered by it).

---

## 7. Mistakes ledger

| # | Wrong belief | Correction | The tell |
|---|---|---|---|
| **FM-01** | Cited `REQUIREMENTS.md` as v0.6/v0.9 | It is **v1.8**; two [HARD] amendments, one a firmware register setting | **Version was on line 7 and line 21. Read the body, never the header.** Caught by hw |
| **FM-02** | Attributed to hw a claim they did not make (*"the format half"* for their `TDM1-0` item) | Their two items were `RSTN` and `TDM1-0` | **Quote the other side's list verbatim before characterising it.** Caught by hw |
| **FM-03** | Wrote that §4 requires **TDM8** on the ADC link | §4 says `SDATA_IN0` = **TDM4** | **Read the amendment paragraph, skipped the port table three lines below.** Same prose-over-table failure as FM-01 |
| **FM-04** | Wrote an outbox file into `DSP Design/agent comms/` — **outside my scope** | Removed; nothing of hw's touched | **Absolute paths outside the immediate working file.** Caught same turn |
| **FM-05** | **FW-006: asserted hw's 128 fs "cannot be right" from arithmetic that assumed all channels ride ONE data pin.** Sent it as a finding; **hw reopened F70 and logged a ledger entry against themselves on the strength of it** | **AKM spreads channels across SDTI1-2 — TDM128 is genuinely 8 ch at 128 fs. Both hw citations were exactly right.** The conclusion happened to survive via `SDTI2` being grounded, **but the reasoning I sent was wrong** | **I did an arithmetic check on a claim without reading the table the claim came from — the exact thing I had told hw I would always do first (002 §6: *"I will read both tables before writing either format"*). I raised the finding before doing what I had promised. A conclusion that survives for a reason other than the one given is not a validated finding — it is a coincidence.** Caught by me, on finally reading both tables |

---

## 8. Method notes carried forward

- **A check that cannot fail is not a check that passed.** Three instances now: hw's F109
  (footprints), **FW-004** (a `110` readback passes in both cases), and **F70 itself** — hw's
  self-consistency check compared two datasheets *to each other* with no third input, so it
  **confirmed the parts CAN agree rather than that they agree at this board's settings.** It never
  consulted the copper.
- **Two numbering systems for one thing is where distinctions die.** The project counts *slots on
  the wire* (TDM4/TDM8); AKM counts *BICK ratio* (TDM128/TDM256). **`TDM128` looks like a match for
  `TDM4` and is in fact the ADC's mode.** hw's own tell — *"the word **both**"* — generalises: a
  single figure asserted across two different links is a compression.
- **Two correct facts never brought into contact** (`../CLAUDE.md` §0b) — **FW-003**, **FW-007**,
  and F70, where `CLAUDE.md`'s digest was right and the ledger wrong for days.
- **A convenience number can be promoted into a load-bearing one by a decision elsewhere.** The
  85 ms was a costing figure until the §7.3 swap made it decide whether the hard mute opens into
  silence. **Record shared margins at both ends.**
- **Rule 2 binds on the other agent's numbers too** — and on mine. **FM-05 is the cost of forgetting
  that in the other direction: I checked hw's arithmetic without reading hw's source.**
