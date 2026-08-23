# STATE.md — ODSP-12 **firmware** working state

**Scope: `DSP Design/DSP Firmware/` only.** This is the firmware agent's ledger. It is *not* the
hardware `STATE.md` one level up — that file is reserved for the hardware agent and is **not read
and not written by this agent, by operator decree (2026-08-22).**

Governed by `../CLAUDE.md`. Requirements source is **`../REQUIREMENTS.md` v1.8**. Both read
directly, never from a summary — including never from a bus message.

---

## 0. LIVE STATUS — rewritten every step, never appended to

**Position:** three bus legs complete. **§7.3 power-down order is DECREED and implementable.**
Nine findings raised (`FW-001`…`FW-009`), all concurred or open with hw. **No firmware code exists
yet — the toolchain is not installed.**

**Single next action:** **verify the ADAU1466 register addresses against
`../datasheets/adau1462-1466.pdf` (Rev. C)** — safeload `num_SafeLoad_Lower`/`_Upper`,
`SOUT_SOURCEx` `0xF180`–`0xF197`, PLL `0xF000`–`0xF004`, S/PDIF `0xF580`/`0xF600`/`0xF604`/`0xF605`.
**All T2, carried on hw's word, and hw has confirmed they have not verified them either.** Then
§7.2 turn-on ordering, then the power-down handler.

**Sits with the operator:** the **ESP-IDF version pin** (Q2a). Not blocking; ask when it matters.
**Do not infer 5.x.**

**Sits with hw:** FW-009 numbering rule · FW-006 the two BICK rows · FW-008 whether the `ATS1-0`
trade attaches to an open escalation · FW-007 register entry. hw owes **the §4.4 citations** (and
had owed the `03H` row — **I closed that myself, see T1-F12**).

**Armed:** persistent monitor polling `agent comms/inbox/` every 15 s. **Session-scoped — re-arm
after any session end.**

**Bus ledger — see §1 for the numbering DEFECT:**

| seq | dir | file | topic | status |
|---|---|---|---|---|
| 001 | hw → fw | `…hw-channel-protocol-and-what-shapes-firmware` | protocol; I2C map; six forces | read, answered by 002 |
| 002 | fw → hw | `…fw-protocol-confirmed-and-akm-boot-defaults` | protocol confirmed; Q2/Q3 decrees; I2C table verified; FW-001…005 | **answered by 003** |
| 003 | hw → fw | `…hw-F97-closed-F99-answered-shutdown-order-changes` | F97 closed (§12 two limits); F99 answered; concurs FW-002/3/4; 7 items handed over | read, answered by 006 |
| 004 | hw → fw | `…hw-shutdown-order-decreed-implement-it` | **§7.3 steps 2/3 SWAPPED by decree.** §7.4 untouched | read, answered by 006 |
| ~~004~~ | fw → hw | *withdrawn* | **COLLIDED with hw's 004** (mine 20:52:00.000, theirs 20:51:38.814 — theirs stands). Renamed to 006, content unchanged, rename disclosed in 006 §0 | superseded |
| **005** | — | — | **RESERVED, not dropped** — hw's owed message | reserved |
| 006 | fw → hw | `…fw-seq-collision-correction-to-002-and-the-ramp-figure` | FW-009 collision; §7.3 ack + no ramp-complete bit; corrects 002; closes `03H`; FW-006/7/8 | **sent, awaiting reply** |

---

## 1. The channel — protocol SET, with one defect open

Protocol per hw seq 001, adopted in full (T1): `NNN-YYYY-MM-DD-<from>-<slug>.md` · header block
(`from`/`to`/`seq`/`date`/`re`/`tier`) · **append, never edit** — a correction is a new message
citing the seq it corrects · findings `FW-###` (hw uses `F###`, now past F111) · `CLAUDE.md` §5
tiers · four conduct rules: no state document crosses (**facts from one may, by fact and with
method**) · state the method not just the value · unanswered items stay named · one message per leg.
**Both sides' claims are T2 on arrival.**

⚠ **The shared counter has no allocation authority — see FW-009.** Both sides take `max(seen)+1`
and can collide, which happened on leg 3. **A gap is loud; a collision is silent.** Even/odd
banding proposed to hw; **until hw rules, keep `max(seen)+1` and disclose any collision.**

Distinct from `../CLAUDE.md` §9's adversary bus (own counter, past 092). Two channels, no
interaction.

---

## 2. T1 register

| # | Fact | Method |
|---|---|---|
| **T1-F02** | `../REQUIREMENTS.md` is **v1.8** (2026-08-21); two [HARD] amendments — §3 oscillator, §4 audio format | read doc-status + revision history |
| **T1-F03** | §4 amendment text matches hw's quote verbatim incl. *"The exclusion is not optional"* | read §4 |
| **T1-F04** | **TOOLCHAIN: ESP-IDF, bare, pinned version** | **operator decree 2026-08-22** |
| **T1-F05** | **No ESP-IDF on this machine**, `IDF_PATH` unset. PlatformIO present (`espressif32@6.5.0`, Arduino core 2.0.14) but **only `toolchain-riscv32-esp` — no Xtensa. The S3 has never been built for here** | probed directly |
| **T1-F06** | **No SigmaStudio project exists yet.** Loader interface first, blob later | **operator decree 2026-08-22** |
| **T1-F07** | I2C0 straps, all six devices — §3b | `kicad-cli sch export netlist`, awk over `(nets` |
| **T1-F08** | **AK5574 in I²C control mode by strap**: `U40` pin 42 → `+3V3_D`, pin 41 → `GND` = Table 22 "I2C Bus" | netlist + p.56 |
| **T1-F09** | **`MSN` (pin 24) → `GND` = SLAVE.** The one mode input **no register overrides** | netlist + p.31/p.56 |
| **T1-F10** | Schematic's cited datasheet revs match the PDFs read | netlist properties vs PDF footers |
| **T1-F11** | AK4458 register space `00H`–`14H`; Note 35 bars `15H`–`1FH` | AK4458 p.74 |
| **T1-F12** | **AK5574 `03H` default = all zeros → `TDM1-0` = `00` = Normal.** Modes are named by BICK ratio: Normal/TDM128/TDM256/TDM512 | **AK5574 p.63** — closed myself; hw had owed it |
| **T1-F13** | **AK5574 `04H` default `00H`** → Sharp roll-off, Normal delay, PCM. **All three already correct — no boot write needed** | AK5574 p.63 |
| **T1-F14** | **Table 5: `CKS3-0`=`0000` (default) = 128 fs / Quad Speed / 108–216 kHz; `0110` = 512 fs / Normal / 8–54 kHz.** With MSN=L, 512 fs @48 kHz = **24.576 MHz** = our XO | AK5574 p.33, corroborated by Table 2 p.32 |
| **T1-F15** | **§4 port map: `SDATA_IN0` = TDM4; `SDATA_OUT0/1` = TDM8**, 32-bit slots | read §4 table directly |
| **T1-F16** | **No ramp-complete status bit on the AK4458.** `DZF` is input-data zero-detect over **8192 LRCK = 170.7 ms**, a different and slower event | AK4458 p.61 note (4) |
| **T1-F17** | **§7.3 steps 2 and 3 SWAPPED**: remote-out → DACs soft-muted → hard mute into silence → rails fall. **§7.4 unchanged and not firmware's** | **operator decree via hw 004** |

**Datasheet revisions:** AK5574 `015016764-E-03` (2022/02) · AK4458 `014011794-E-02` (2017/07).
**Every register value below was read from the page named, rendered as a page image, never recalled.**

---

## 3. The boot problem

### 3a. THREE distinct timing windows — do not merge. hw has adopted this framing.

| # | Window | Bus | Cause | Tier |
|---|---|---|---|---|
| **W1** | **PLL lock ≤ 15 ms** — `0xF000`–`0xF003`, poll `PLL_LOCK` `0xF004` bit 0. **Timeout = distinct fault code, not a retry loop** | SPI0 | ADAU1466 control port dead until lock | requirement **T1**; addresses **T2** |
| **W2** | **ADC wake-up ~12.5 ms** after `PDN` release. **Do not transact with ANY device on I2C0** | I2C0 | AK5574 may pulse shared pins | **T2 from hw**, citation owed in their next |
| **W3** | **Reset-around-format-change** — changing CKS/TDM/DIF requires the ADC in reset (`RSTN`=0 or `PW4-1`=`0H`); *"a stable clock must be supplied after releasing the reset"* | I2C0 | AK5574 p.31 | **T1** |

### 3b. I2C0 map — verified against the netlist

| Device | Ref | Addr | Straps as found |
|---|---|---|---|
| AK5574 | **U40** | **0x10** | pin 32 → `GND`, pin 34 → `GND` |
| AK4458 #1 (AOUT1–6) | **U51** | **0x11** | pin 12 → `GND`, pin 15 → `+3V3_D` |
| AK4458 #2 (AOUT7–12) | **U52** | **0x12** | pin 12 → `+3V3_D`, pin 15 → `GND` |
| PCF8574T | **U43** | **0x20** | A2,A1,A0 → `GND` |
| ADS1015 | **U11** | **0x48** | ADDR → `GND` |
| TMP461 | **U12** | **0x49** | A0 → `+3V3_D`, A1 → `GND` |

All on `I2C0_SDA`/`I2C0_SCL`. **Strap wiring T1; strap→address decode for ADS1015/TMP461 is T2 from
hw.** hw's F26 two-DACs-at-0x11 defect **is fixed in the copper**, checked specifically.

### 3c. Power-on defaults — what is wrong before firmware touches anything

**AK5574 — wrong on THREE counts, all in `02H`/`03H`, every `PDN` cycle** (Note 26, p.62):

| Field | Reg | Default | Required |
|---|---|---|---|
| `CKS3-0` | `02H` D6:D3 | `0000` = **128 fs / Quad Speed / 108–216 kHz** | `0110` = 512 fs / Normal |
| `DIF1-0` | `02H` D2:D1 | `00` = **24-bit MSB** | 32-bit MSB |
| `TDM1-0` | `03H` D6:D5 | `00` = **Normal (non-TDM)** | **TDM128 (= TDM4)** |
| `RSTN` | `01H` D0 | **`1` = running** | — **opposite of the DAC** |

**AK4458:**

| Field | Reg | Default | Against the design? |
|---|---|---|---|
| `RSTN` | `00H` D0 | **`0` = Reset** | **YES — boots HELD IN RESET** |
| `DIF2-0` | `00H` D3:D1 | `110` = Mode 6, 32-bit MSB | **No — but conditional, see FW-004** |
| `TDM1-0` | `0AH` D7:D6 | `00` "Normal" | **YES** — needs TDM8. *Default row not read — T2* |
| `SMUTE` | `01H` D0 | `0` = not muted | No — analog mute covers it |
| `ATT7-0` | `0AH`–`11H` | **`FFH` = +0 dB on every PDN** | **DAC boots at FULL VOLUME** |
| `ATS1-0` | `0BH` D7:D6 | `00` = 4080/fs = **85.0 ms** | Selectable — see FW-008 |

### 3d. Power-down handler — DECREED, implementable (T1-F17)

    1. remote-in drop  ->  remote-out released immediately
    2. state persisted, DACs SOFT-MUTED
    3. hard mute engaged, into digital silence      <- must NOT start until 2 COMPLETES
    4. rails allowed to fall

**Step 2 must complete before step 3.** **No status bit exists (T1-F16) → elapsed-time wait is
forced**, which makes the ramp figure load-bearing on a [HARD] step — and the datasheet gives two
(FW-007). Implementation:

    ramp_ms = ATT_STEPS[ATS] / fs      ATT_STEPS = {4080, 2040, 510, 255}
    wait    = ramp_ms x margin         unconditional, before releasing MUTE_EN

**No hard-coded `85`.** Default `ATS`=`00` → 85.0 ms, on FW-007's safe-direction argument.
**§7.4 is hardware's; firmware must not be in the rail-collapse path at all.**

### 3e. Power-up facts held for §7.2 ordering (next design work)

- **DAC boots full volume, not muted** — nothing digital backstops a boot-path bug.
- **~104 µs window (5/fs) after reset release where volume writes are INSTANT, no ramp** — usable
  to slam to mute at boot; miss it and the same write ramps 85 ms.

---

## 4. Decisions log

| # | Decision | Why | Reopens |
|---|---|---|---|
| FD-01 | Firmware state in **this** file; hardware `STATE.md` never opened | Operator decree; lost-update race | Operator |
| FD-02 | `agent comms/` under `DSP Firmware/`, separate from the adversary bus | Operator instruction; counter collision | Operator |
| FD-03 | Inbox watch = polling monitor (15 s) | Windows, no `inotifywait` | Native watcher |
| FD-04 | **Verify hw's claims against the artefact before agreeing**, not only before dismissing | hw decreed the symmetry; it paid immediately | Never |
| FD-05 | Netlist exported to **scratchpad**, never into `../hw/` | Read-only posture toward the hardware artefact | Never |
| FD-06 | **Take `ATS1-0` = `00` (85.0 ms) and wait it in full**, parameterised | FW-007 safe direction: waiting long is imperceptible, waiting short defeats the §7.3 swap | An operator ruling on shutdown latency |
| FD-07 | **Leave `005` unused rather than reuse it** | It is hw's owed message; a reserved number disclosed beats a reused one | hw's FW-009 ruling |

---

## 5. Open items

| # | Question | State |
|---|---|---|
| Q1 | I2C0 address table | **CLOSED** — received, verified against netlist |
| Q2 | Toolchain | **CLOSED — ESP-IDF bare (T1-F04)** |
| **Q2a** | **Exact ESP-IDF version pin** | **OPEN, ⬜ UNSET.** Do not infer 5.x |
| Q3 | DSP binary ownership | **CLOSED — none exists yet (T1-F06)** |
| Q4 | Bus message format | **CLOSED** — §1 |
| **Q5** | **ADAU1466 register addresses** | **OPEN, all T2. hw confirms they have not verified them either.** Next action |
| **Q6** | **AK4458 `0AH` TDM default row** | **OPEN, T2** — not yet read |

---

## 6. Findings register

| # | Finding | Verdict | Tier |
|---|---|---|---|
| **FW-001** | hw §4.2 — AK5574 ignores mode straps in serial control mode; the [HARD] format exists **only** as a firmware register write | **CONFIRMED and strengthened.** hw's argument was one-legged; supplied the second leg (`02H` `DIF1-0` exists, defaults `00`). Structural corroboration: **CKS3-0 are multiplexed onto the I²C pins**, so the strap is physically impossible in I²C mode. Precondition made T1 (T1-F08) | **T1** |
| **FW-002** | **The AK5574 boots wrong — now THREE counts** (`CKS3-0`, `DIF1-0`, `TDM1-0`), every PDN cycle. Absent from hw's §4.3 | **CONCURRED by hw**, logged as ours. Folds in hw's **F66**. `TDM1-0` promoted T2→T1 (T1-F12) | **T1** |
| **FW-003** | **`RSTN` defaults are OPPOSITE** (AK4458 `0` held in reset, AK5574 `1` running) **and the required motions are opposed** — the ADC must be driven *into* reset to change format. Establishes **W3** | **CONCURRED**; hw adopted the three-window framing | **T1** |
| **FW-004** | The AK4458's format default is **right before the TDM write and may not be after it** → DIF must be re-verified **after** TDM. **A readback seeing `110` passes in both the correct and incorrect case** | **CONCURRED**, write-order consequence accepted, does not touch the schematic. **hw correctly corrected my attribution — see FM-02** | **T1** |
| **FW-005** | `kicad-cli` warns *"schematic has annotation errors"*; 0 `?` refdes, 0 duplicates found | **INDEPENDENTLY CONFIRMED by hw** (562/562 unique `(refdes,unit)`, 0 path mismatches). **Cause unknown both sides, logged open** | T1 (emission only) |
| **FW-006** | **hw's F70 BICK figures cannot both be 128 fs.** TDM4 = 128 fs ✔ but TDM8 × 32-bit = **256 fs = 12.288 MHz**. Likely a transmission compression of two rows | **RAISED, question.** Neither Table 9 nor Table 13 read — arithmetic on hw's summary | **T2** |
| **FW-007** | **The ramp is stated two ways in one datasheet** — p.49 `4080/fs` (**85.0 ms**, self-checking against its own 92.5 ms @44.1 kHz) vs p.61 note (1) *"4080 LRCK cycles (1020/fs)"* (**21.25 ms**), contradicting itself in one parenthesis. **Taking 85.0 ms** on corroboration **and** safe direction | **RAISED.** Made load-bearing by T1-F16/T1-F17 | **T1** |
| **FW-008** | **The 85 ms is not a property of the part** — `ATS1-0` selects 4080/2040/510/255 per fs (85.0/42.5/10.6/5.3 ms), and the time is proportional to `ATT_DATA`. **A faster ramp trades against §12(ii)'s weighted-peak limit**, which is exactly the criterion that sees step size | **RAISED while F99's package was still open.** Not mine to decide | **T1** |
| **FW-009** | **The shared sequence counter has no allocation authority.** Both sides take `max(seen)+1`; on leg 3 both took `004`. **A gap is loud, a collision is SILENT** — both folders look internally consistent and two messages share one identity. Proposed **even/odd banding** (prevention, not resolution) | **RAISED.** hw's protocol, hw's call | **T1 (it happened)** |

**Not verified, named per rule 3:** BM83 `SDATA_IN1` exclusion (decreed, not corroborated) ·
F70's Table 9 / Table 13 rows (**T2** — FW-006) · §4.4's 583/fs derivation (**T2**, consequence
accepted) · **all ADAU1466 register addresses (T2 — Q5)** · AK4458 `0AH` default (**T2** — Q6) ·
hw's parked F62/F65/F68/F71/F75 and the `07H` read-modify-write item (**not started**).

---

## 7. Mistakes ledger

| # | Wrong belief | Correction | The tell |
|---|---|---|---|
| **FM-01** | Cited `REQUIREMENTS.md` §5 as **v0.6**/**v0.9** and treated it as current | Document is **v1.8**; two [HARD] amendments landed 2026-08-21, one a firmware register setting | **The version was on line 7 and line 21. I read §5's body and never read the header.** Caught by hw |
| **FM-02** | Attributed to hw a claim they did not make — read their §4.3 second item as *"the format half"* when they had written `TDM1-0` | Their two items were `RSTN` and `TDM1-0`; they never claimed `DIF2-0` was wrong. **My substance stood; the attribution did not** | **Quote the other side's list verbatim before characterising it.** Caught by hw |
| **FM-03** | Wrote in seq 002 that §4 requires **TDM8** on the ADC link | §4's port table says **`SDATA_IN0` = TDM4**; TDM8 is the two DAC links. Substance of FW-002 unaffected — the target mode named was wrong | **I read §4's amendment paragraph and skipped the port table three lines below it — the same prose-over-table failure as FM-01, twice in two messages.** Caught by me, on re-reading §4 for FW-006 |
| **FM-04** | Wrote an outbox file into `DSP Design/agent comms/` — **outside my scope**, creating a stray folder in the hardware agent's tree | Removed immediately; nothing of theirs was touched; correct file written under `DSP Firmware/agent comms/` | **Absolute paths for anything outside the immediate working file.** Caught by me, same turn |

---

## 8. Method notes carried forward

- **A check that cannot fail is not a check that passed** (hw's F109). **FW-004 is that shape in
  firmware; FW-009 is that shape in the protocol itself** — the collision replaced a loud failure
  with a silent one.
- **Two correct facts never brought into contact** (`../CLAUDE.md` §0b). **FW-003** is exactly
  that; so is **FW-007**, where two pages of one datasheet each look fine alone.
- **Rule 2 binds on the other agent's numbers too.** hw's register addresses stay T2 until read —
  hw has explicitly agreed.
- **A convenience number can be promoted into a load-bearing one by a decision elsewhere.** The
  85 ms was a costing figure in F99; the §7.3 swap made it decide whether the hard mute opens into
  silence. **Record shared margins at both ends.**
