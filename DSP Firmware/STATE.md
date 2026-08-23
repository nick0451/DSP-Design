# STATE.md — ODSP-12 **firmware** working state

**Scope: `DSP Design/DSP Firmware/` only.** This is the firmware agent's ledger. It is *not* the
hardware `STATE.md` one level up — that file is reserved for the hardware agent and is **not read
and not written by this agent, by operator decree (2026-08-22).**

Governed by `../CLAUDE.md`. Requirements source is **`../REQUIREMENTS.md` v1.8**. Both read
directly, never from a summary — including never from a bus message.

---

## 0. LIVE STATUS — rewritten every step, never appended to

**Position:** eight bus legs complete. **[`BOOT.md`](BOOT.md) is written — the §7.2/§7.3
specification, and the first real artefact on this side.** All converter and DSP registers verified;
F62/F65/F68 answered; invariant shelf I-1…I-7 plus the boot-write table. Sixteen findings
(`FW-001`…`FW-016`). **No firmware code exists yet — the toolchain is not installed and the version
pin is ⬜ UNSET; I am not writing code against an unpinned toolchain.**

**Single next action:** **close FW-016's T2** — confirm from the ADAU1466 serial-port and
clock-generator sections that the serial ports can be started **before** the DSP core runs. If they
cannot, `BOOT.md` step 3b must move after the program load and §7.2 5c's interleaving argument needs
re-examining. **Then Q8 (safeload).**

**Sits with the operator:** ESP-IDF version pin (Q2a). Not blocking.

**Sits with hw:** shelf FW-015 as I-8 (**suggested: shelf the four write VALUES, since the invariant
is "these are masked writes", which is the form a future reader needs**) · Table 17's `DEM21-0`=`00`
row if convenient · **F71/F75 facts, which hw will send unprompted** · FW-005 open both sides,
**nothing new learned in four legs**.

**Armed:** persistent monitor polling `agent comms/inbox/` every 15 s. **Session-scoped — re-arm
after any session end.**

---

## 1. The channel

Protocol per hw seq 001: `NNN-YYYY-MM-DD-<from>-<slug>.md` · header block · **append, never edit** ·
findings `FW-###` vs hw's `F###` · `CLAUDE.md` §5 tiers · four conduct rules (no state document
crosses — **facts may, by fact and with method** · state the method · unanswered items stay named ·
one message per leg). **Both sides' claims are T2 on arrival.**

**NUMBERING (amended by hw seq 005 after FW-009): `hw` takes ODD, `fw` takes EVEN.** The shared
`max(seen)+1` counter had no allocator and collided on leg 3. **hw also withdrew their original 001
justification as wrong** — per-folder numbering does not hide a drop, because the *receiver* sees
the gap; they had reasoned about the sender's view.

| seq | dir | topic | status |
|---|---|---|---|
| 001 | hw → fw | protocol; I2C map; six forces | answered by 002 |
| 002 | fw → hw | protocol confirmed; Q2/Q3 decrees; I2C table verified; FW-001…005 | answered by 003 |
| 003 | hw → fw | F97 closed; F99 answered; concurs FW-002/3/4; 7 items handed over | answered by 006 |
| ~~004~~ | hw → fw | **§7.3 steps 2/3 SWAPPED by decree** | answered by 006 |
| ~~004~~ | fw → hw | **COLLIDED** — renamed to 006, disclosed in 006 §0 | superseded |
| 005 | hw → fw | FW-009 adopted, parity swapped; F70 reopened; FW-007/008 logged | answered by 008 |
| 006 | fw → hw | FW-009; §7.3 ack; corrects 002; closes `03H`; FW-006/7/8 | answered by 005 |
| 007 | hw → fw | F70 corrected to Mode 18; FW-010 answered; FW-011 logged; **M35**; F62/F65/§4.4 delivered | answered by 010 |
| 008 | fw → hw | **F70 resolved**, FW-006 reasoning retracted, Mode 18 identified; FW-010, FW-011 | answered by 007 |
| 009 | hw → fw | **FW-012/FW-013 DRAWN in the schematic**; `SYNCE` demoted to T2; FW-014 is mine to build | answered by 012 |
| 010 | fw → hw | **ADAU1466 addresses verified**; §4.4 page = p.53; FW-012/013/014; F62/F65 answered | answered by 009 |
| 011 | hw → fw | **F68 CONCURRED**; shelf built I-1…I-7; **M36**; FW-011 amended; `SYNCE` promoted | answered by 014 |
| 012 | fw → hw | **F68 answered**; `SYNCE` closed T1; hw's `07H` item explained; Q6/Q7 closed; FW-011 amended down | answered by 011 |
| 013 | hw → fw | **Table 17 closed** (`00` = 44.1 kHz de-emph, ~9.5 dB HF loss on DAC2); **M36 amended by FW-015**; boot-write table shelved as values | answered by 016 |
| 014 | fw → hw | Shelf mirrored + validated; **FW-015 — the boot path's three masked writes**; `HPFE` decision | answered by 013 |
| 016 | fw → hw | **`BOOT.md` written**; **FW-016 — a fifth F20 in §7.2 step 5a**; Table 17 label inversion | **sent** |

**My next: 018.**

---

## 2. T1 register

| # | Fact | Method |
|---|---|---|
| **T1-F02** | `../REQUIREMENTS.md` is **v1.8**; §3 oscillator + §4 audio-format [HARD] amendments | read directly |
| **T1-F04** | **TOOLCHAIN: ESP-IDF, bare, pinned version** | **operator decree** |
| **T1-F05** | **No ESP-IDF here**; PlatformIO present but **no Xtensa toolchain — the S3 has never been built for on this machine** | probed directly |
| **T1-F06** | **No SigmaStudio project exists yet.** Loader interface first, blob later | **operator decree** |
| **T1-F07** | I2C0 straps, all six devices — §3b | netlist + awk |
| **T1-F08** | **AK5574 in I²C control mode by strap** (`I2C`=H, `PSN`=L) | netlist + p.56 Table 22 |
| **T1-F09** | **`MSN` → `GND` = SLAVE**; the one mode input no register overrides | netlist + p.31/p.56 |
| **T1-F12** | AK5574 `03H` default `00` → `TDM1-0` = Normal | AK5574 p.63 |
| **T1-F13** | AK5574 `04H` default `00H` — Sharp/Normal/PCM, **no boot write needed** | AK5574 p.63 |
| **T1-F14** | Table 5: `CKS3-0` default `0000` = 128 fs/Quad; **`0110` = 512 fs/Normal** = 24.576 MHz @48 kHz | AK5574 p.33 + p.32 |
| **T1-F15** | §4 port map: `SDATA_IN0` = TDM4; `SDATA_OUT0/1` = TDM8 | read §4 table |
| **T1-F16** | **No ramp-complete status bit on the AK4458**; `DZF` = input-zero over 8192 LRCK = 170.7 ms | AK4458 p.61 |
| **T1-F17** | **§7.3 steps 2/3 SWAPPED**; §7.4 unchanged, not firmware's | **operator decree** |
| **T1-F18** | **AK5574 Table 9 row 26** — TDM128, `DIF1-0`=`10` → 32-bit MSB, LRCK ↑, **128 fs** | AK5574 p.36 |
| **T1-F19** | **AK4458 Table 13** — Mode 12 = TDM128/128 fs; **Mode 18 = TDM256/256 fs**, both 32-bit MSB ↑ | AK4458 p.35 |
| **T1-F20** | AK4458 mode/pin needs: TDM128 = 8 ch via SDTI1-2; **TDM256 = 16 ch via SDTI1-2**; TDM512 = 16 ch via SDTI1 | AK4458 p.34 |
| **T1-F21** | **Both DACs wire `SDTI1` only — `SDTI2/3/4` tied to `GND`** | netlist (**hw confirmed independently from `gen_sheet_dac.py:206`**) |
| **T1-F22** | **Table 14**: in TDM256 `SDS2-0` picks 4 consecutive pairs of 8; **only `000` stays on `SDTI1`** | AK4458 p.42 |
| **T1-F23** | `DCHAIN`=0 default → `TDMO1/2` are inputs `SDTI3/4`. **Not daisy-chained; copper agrees** | AK4458 p.43 |
| **T1-F24** | **ADAU1466 Rev. C: every §5-contract address confirmed** — §3g | `adau1462-1466.pdf` pp. 92–96, 98 |
| **T1-F25** | **AK5574 wake-up citation is p.53.** 583/fs = **12.15 ms**; instantaneous pulse bound **max 1 µs** | AK5574 p.53 |
| **T1-F26** | **The 16384-cycle / 10 ms window is case (b), selected by `LDOE`=H + `PSN`=L. `LDOE`=L would give 1 ms max.** Board straps `LDOE` (45) → `+3V3_D` | AK5574 p.53 note (2) + netlist |
| **T1-F27** | **Slave mode: internal PDN is released by inputting MCLK, BICK and LRCK** after `PDN`→H. **The DSP's serial port must clock before the ADC leaves power-down** | AK5574 p.53 |
| **T1-F28** | **Firmware owns all three converter `PDN` lines and reads `OVF`**: `ADC_PDN_N`→GPIO9, `DAC1_PDN_N`→GPIO10, `DAC2_PDN_N`→GPIO11, `ADC_OVF`→GPIO12, all on U20 (ESP32-S3) | netlist |
| **T1-F29** | **AK4458 sync: bound is 3/256fs = 244.1 ns @48 kHz**, triggered by `RSTN`=0 **or** 8192 all-zero samples with `SYNCE`=1 | AK4458 p.67 |
| **T1-F30** | **The AK5574 has no status register** — space is `00H`–`07H`, all control. **No flag reports a phase resynchronization** | AK5574 p.62 |

| **T1-F31** | **AK4458 `07H` D0 `SYNCE` default = `1`** — *"SYNC Mode Enable (default)"*. Closes hw's demoted T2 | AK4458 p.79 |
| **T1-F32** | **AK4458 `07H` D1 is a fixed `1`; the register's power-on value is `0x03`, not `0x01`.** A naive `write(07H,0x01)` clears it — **this is why hw's parked "`07H` read-modify-write" item exists** | AK4458 p.79 + p.74 |
| **T1-F33** | **"In serial control mode, the data output is Optimal Data Placement mode regardless of the ODP pin setting."** Fixed placement holds the slot map **regardless of summation**; **Optimal removes the redundancy, so the occupied-slot count MOVES with summation** | AK5574 p.46 |
| **T1-F34** | **Figure 57: in TDM128, `SDTO1` carries Slots 1–4 and `SDTO2` emits all "0"** — matches the copper (`SDTO2` unconnected) and §4's 4 channels. **A picture of the slot map, not a calculation about it** | AK5574 p.50 |
| **T1-F35** | **AK4458 `0AH`: `TDM1-0` default `00` (Q6 closed); `SDS2-0` default `000` (Q7 closed)** — `SDS` already holds the FW-011 value | AK4458 p.80 |
| **T1-F36** | **`DZF/SMUTE` (pin 11) is UNCONNECTED on both DACs**, and its enable bits default disabled. **Neither converter offers any usable status output except the ADC's `OVF` on GPIO12** | netlist + AK4458 p.79 |

**Datasheet revisions:** AK5574 `015016764-E-03` · AK4458 `014011794-E-02` · ADAU1462/1466 **Rev. C**.
**Every register value was read from the page named, rendered as a page image, never recalled.**

---

## 3. The boot problem

### 3a. THREE distinct timing windows — do not merge. hw has adopted the framing.

| # | Window | Bus | Tier |
|---|---|---|---|
| **W1** | **PLL lock ≤ 15 ms** — poll `0xF004` bit 0; **timeout = distinct fault code, not a retry loop** | SPI0 | **T1** (addresses now verified) |
| **W2** | **ADC wake-up** — 16384 internal-osc cycles, **max 10 ms**; SDTO valid at 583/fs = 12.15 ms. **Do not transact with ANY device on I2C0.** **Duration is set by the `LDOE` strap (FW-012)** | I2C0 | **T1** |
| **W3** | **Reset-around-format-change** — ADC must be in reset to change CKS/TDM/DIF; stable clock after release | I2C0 | **T1** |

### 3b. I2C0 map — verified against the netlist

`U40` AK5574 **0x10** · `U51` AK4458#1 **0x11** · `U52` AK4458#2 **0x12** · `U43` PCF8574T **0x20** ·
`U11` ADS1015 **0x48** · `U12` TMP461 **0x49**. All on `I2C0_SDA`/`I2C0_SCL`.
**Strap wiring T1; strap→address decode for ADS1015/TMP461 is T2 from hw.**

### 3c. The serial links — RESOLVED (F70)

**The project counts SLOTS ON THE WIRE; AKM counts BICK RATIO. That collision is what put a wrong
mode in hw's ledger.**

| Link | §4 name | AKM mode | Row | BICK @48 kHz |
|---|---|---|---|---|
| `SDATA_IN0` → AK5574 | TDM4 | **TDM128** (`01`) | Table 9 row 26 | **128 fs = 6.144 MHz** |
| `SDATA_OUT0/1` → AK4458 | TDM8 | **TDM256** (`10`) | Table 13 **Mode 18** | **256 fs = 12.288 MHz** |

**The two converter links do NOT share a BICK rate (FW-010).** hw confirms **no series termination
exists on any BCLK net** and layout has not started — nothing was sized against the wrong figure.
**Edge rate on those nets is a firmware register (FW-013).**

### 3d. Boot register writes — fully determined, all read

**AK5574** (wrong on three counts, every `PDN` cycle — Note 26):

    02H:  CKS3-0 = 0110    512 fs / Normal Speed      was 0000 = 128 fs / Quad Speed
          DIF1-0 = 10      32-bit MSB                  was 00   = 24-bit MSB
    03H:  TDM1-0 = 01      TDM128 = 4 slots on wire    was 00   = Normal / non-TDM
    04H:  no write needed                              already correct (T1-F13)
    RSTN (01H D0) defaults to 1 = RUNNING -- opposite of the DAC (FW-003)

**AK4458** (both parts):

    00H:  RSTN   = 1       release reset               was 0 = HELD IN RESET
          DIF2-0 = 110     32-bit MSB                  already 110 -- re-verify AFTER the TDM write
    0AH:  TDM1-0 = 10      TDM256 = 8 slots on wire    was 00 = Normal  (T1, p.80)
    ATT7-0 boots FFH = 0 dB (full volume); SMUTE boots 0 (unmuted)

### 3d-i. THE INVARIANT SHELF — mirrored from hw's register, each entry re-verified against my own page reads

**hw asked me to mirror it because *"this is the one artefact where duplication is the point"* — the
failure mode is someone touching a register without consulting the hardware side, and a copy here is
the one they will read. I validated all seven rather than transcribing them; all hold.**

    I-1  AK5574 MONO2-1 = 00      Not-Summation           S4/S10 [HARD]   p.62
    I-2  AK5574 PW4-1   = 1111    all channels on         S4/S10 [HARD]   p.62
    I-3  AK4458 SDS2-0  = 000     pairs 1-4 on SDTI1      grounded SDTI2  p.80
    I-4  AK4458 SYNCE   = 1       sync enabled            S5 item 5       p.79
    I-5  AK4458 07H     = 0x03    D1 is a fixed 1         naive 0x01 clears it   p.79
    I-6  AK4458 DCHAIN  = 0       not daisy-chained       two-port topology
    I-7  both AK4458s   filters identical                 S5 item 5 group delay

**hw's M36:** every entry is correct at power-on, backed by no hardware, reported by no error bit,
silent when violated — **so there is no test to write, because today the code does nothing and doing
nothing is correct.** An invariant that exists only as an absence of code cannot be found by reading
the code, so it must exist as a list or not at all.

### 3d-ii. I-8 / FW-015 — M36's framing does NOT extend to the boot path

> **The boot path writes four registers and THREE carry load-bearing bits a naive write destroys.**
> I-1…I-7 are protected by "do not write". These are not — **these registers must be written.**

    AK4458 00H  default 0x0C   naive 0x01 to release reset CLEARS DIF2-0 110 -> 000,
                               which Table 13 SHADES as "not available" in TDM256
                               CORRECT:  write(00H, 0x0D)
    AK4458 0AH  default 0x0D   naive 0x80 to set TDM256 CLEARS PW2/PW1 -> powers OFF DAC1+DAC2
                               (four of eight channels) and moves DEM21-0 01(OFF) -> 00 (T2)
                               CORRECT:  write(0AH, 0x8D)     -- also where SDS1/SDS2 live, so I-3
                                                                 is protected by THIS write, not by
                                                                 "do not write"
    AK5574 02H  default 0x01   assembling only CKS3-0=0110 and DIF1-0=10 gives 0x34 and clears HPFE
                               CORRECT:  write(02H, 0x35)
    AK5574 03H  default 0x00   TDM1-0=01 -> write(03H, 0x20)   the ONLY register with no other
                                                                live bits. One of four.

**THE RULE: on both AKM parts, every register the boot path writes is a read-modify-write, because
not one of them contains only the field being set.** The boot code writes **fields, not values** —
any helper taking `(register, value)` rather than `(register, mask, value)` is a defect waiting for
its first use, and the failure is the class signature: no fault, no error bit, silent.

**Registers needing NO boot write** (all T1): AK5574 `04H` · AK4458 `05H`, `06H`, `07H`, `08H`,
`09H`, `0BH`. **Recorded as negatives deliberately — an unnecessary write is a change nobody can
later justify.**

**ADAU1466:** `0xF690` `SPDIF_TX_EN` must be written — **the on-die S/PDIF transmitter is disabled
at reset**, and F26 made S/PDIF TX on-die.

### 3e. Power-down handler — DECREED (T1-F17)

    1. remote-in drop -> remote-out released immediately
    2. state persisted, DACs SOFT-MUTED
    3. hard mute engaged, into digital silence   <- must NOT start until 2 COMPLETES
    4. rails allowed to fall

**No status bit exists (T1-F16) → elapsed-time wait forced**, making the ramp figure load-bearing on
a [HARD] step — and the datasheet gives two (FW-007).

    ramp_ms = ATT_STEPS[ATS] / fs      ATT_STEPS = {4080, 2040, 510, 255}
    wait    = ramp_ms x margin         unconditional, before releasing MUTE_EN

**No hard-coded `85`.** Default `ATS`=`00` → 85.0 ms (FD-06). **§7.4 is hardware's; firmware must
not be in the rail-collapse path at all.**

### 3f. Power-up facts held for the §7.2 spec — NEXT ACTION

- **`PDN` must be held L >150 ns after AVDD and TVDD are up** (p.53 note 1).
- **The ADC will not leave power-down until MCLK/BICK/LRCK are present (T1-F27)** — the DSP's serial
  port clocks first, then `ADC_PDN_N` releases.
- **Firmware owns `ADC_PDN_N`/`DAC1_PDN_N`/`DAC2_PDN_N` on GPIO9/10/11 (T1-F28)** — the ordering is
  implementable.
- **DAC boots full volume, unmuted** — nothing digital backstops a boot-path bug.
- **~104 µs window (5/fs) after reset release where volume writes are INSTANT, no ramp.**
- **Both DACs sync on `RSTN`=0, which is their power-on default** — no common trigger needed (F62).

### 3g. ADAU1466 control registers — VERIFIED against Rev. C (T1-F24)

    0xF000 PLL_CTRL0      RW   PLL_FBDIVIDER, reset 0x0060
    0xF001 PLL_CTRL1      RW   PLL_DIV
    0xF002 PLL_CLK_SRC    RW   CLKSRC
    0xF003 PLL_ENABLE     RW   PLL_ENABLE
    0xF004 PLL_LOCK       R    PLL_LOCK at BIT 0            <- W1's poll target
    0xF180-0xF197 SOUT_SOURCEx  RW  SOUT_ASRC_SELECT / SOUT_SOURCE
    0xF580 ASRC_LOCK      R    ASRC0L..ASRC7L
    0xF600 SPDIF_LOCK_DET R    LOCK at bit 0
    0xF604 SPDIF_RESTART  RW   RESTART_AUDIO
    0xF605 SPDIF_LOSS_OF_LOCK R  LOSS_OF_LOCK               <- needs a RUNTIME consumer
    0xF610-0xF68B  SPDIF_RX CS/UD/VB/PB blocks  R           <- range ends exactly at 0xF68B

**Not in the contract but needed:** `0xF690` `SPDIF_TX_EN` (TX disabled at reset) · `0xF402`
`START_CORE` / `0xF403` `KILL_CORE` / `0xF404` `START_ADDRESS` / `0xF405` `CORE_STATUS` (R) ·
`0xF602` `SPDIF_RX_DECODE` (`AUDIO_TYPE`/`COMPR_TYPE` — FW-014) · `0xF784`/`0xF794` pin drive and
slew (FW-013) · `0xF200`–`0xF21D` `SERIAL_BYTE_x_0/1` (`WORD_LEN`, `DATA_FMT`, `LRCLK_POL`,
`TDM_MODE` — the DSP side of §4's format decree).

---

## 4. Decisions log

| # | Decision | Why | Reopens |
|---|---|---|---|
| FD-01 | Firmware state in **this** file; hardware `STATE.md` never opened | Operator decree; lost-update race | Operator |
| FD-02 | `agent comms/` under `DSP Firmware/` | Operator instruction | Operator |
| FD-03 | Inbox watch = polling monitor (15 s) | Windows, no `inotifywait` | Native watcher |
| FD-04 | **Verify hw's claims against the artefact before agreeing**, not only before dismissing | Has now paid in both directions | Never |
| FD-05 | Netlist exported to **scratchpad**, never into `../hw/` | Read-only posture | Never |
| FD-06 | `ATS1-0` = `00` (85.0 ms), waited in full, parameterised | FW-007 safe direction | Operator ruling |
| FD-08 | **fw takes EVEN sequence numbers** | hw decree seq 005 | hw |
| FD-09 | **No polling loop for a condition that has no observable** (F65) | A guard that cannot see its target is FW-004's shape — a check that cannot fail | A status bit appearing, which it will not |
| FD-10 | **Conservative reading where the AK5574 datasheet gates one event two ways** — require clocks running **AND** ≥10 ms before I2C0 traffic | Satisfies both sentences; vendor ambiguity is not resolved by picking | A vendor clarification |
| FD-11 | **`HPFE` = `1`** (ADC high-pass filter ON, the vendor default) | Only load-bearing because `02H` must be written at all (FW-015). **Stated as a decision rather than inherited by accident**: DC-blocking at the converter, and the configuration AKM's own characterisation assumes | §12's sweep needing response below the HPF corner, or the front end's coupling shown to make it redundant |
| FD-12 | **The boot code writes FIELDS, not values** — every register access is `(register, mask, value)` | FW-015: three of the four boot registers carry bits a naive whole-register write destroys, silently | Never |

---

## 5. Open items

| # | Question | State |
|---|---|---|
| Q2a | **Exact ESP-IDF version pin** | **OPEN, ⬜ UNSET.** Do not infer 5.x |
| **Q8** | **Safeload mechanism** — `num_SafeLoad_Lower`/`_Upper` have **no addresses in the contract**, so nothing was falsifiable. Not in the `0xF000`–`0xF7FF` block; lives in parameter RAM (datasheet p.89) | **OPEN, mine to close. The only open datasheet item left** |

**Closed:** Q1 (I2C map) · Q2 (ESP-IDF) · Q3 (no SigmaStudio project) · Q4 (protocol) ·
**Q5 (ADAU1466 addresses, §3g)** · **Q6 (AK4458 `0AH` `TDM1-0` default `00`, p.80)** ·
**Q7 (`SDS2-0` default `000`; `SDS1`/`SDS2` bits T1 at `0AH` D5/D4, `SDS0` at `0BH` D4 from the map
table)** · **Q9 (`SYNCE` default `1`, p.79)**.

---

## 6. Findings register

| # | Finding | Verdict |
|---|---|---|
| **FW-001** | AK5574 ignores mode straps in serial control mode; the [HARD] format exists **only** as a firmware register write | **CONFIRMED, strengthened** — supplied the missing second leg; CKS3-0 are multiplexed onto the I²C pins, so the strap is physically impossible |
| **FW-002** | **AK5574 boots wrong on THREE counts** (`CKS3-0`, `DIF1-0`, `TDM1-0`), every PDN cycle | **CONCURRED**; folds in hw's F66; all target values now read |
| **FW-003** | **`RSTN` defaults OPPOSITE** and required motions opposed; establishes **W3** | **CONCURRED**; hw adopted the three-window framing |
| **FW-004** | AK4458 format default is right **before** the TDM write and may not be after; a `110` readback passes in both cases | **CONCURRED.** `110` does survive here (Mode 6 → Mode 18) — a fact about this value, **not a property of the field** |
| **FW-005** | `kicad-cli` "annotation errors" warning; cause not reproduced by either side | **CONFIRMED independently by hw.** Open both sides |
| **FW-006** | *"hw's F70 BICK figures cannot both be 128 fs"* | **REASONING RETRACTED** (assumed one data pin). **hw validated the retraction against their own generator before accepting it.** Conclusion survives via FW-010 |
| **FW-007** | **Ramp stated two ways in one datasheet** — 85.0 ms (p.49, self-checking) vs 21.25 ms (p.61). **Taking 85.0** | **LOGGED by hw**, who note the safe-direction argument survives either resolution |
| **FW-008** | **The 85 ms is not a property of the part** — `ATS1-0` selects 16:1; time scales with `ATT_DATA` | **ENDORSED**; going to the operator as a correction of hw's framing, not a reopening |
| **FW-009** | **The shared sequence counter had no allocation authority.** A gap is loud; **a collision is silent** | **ADOPTED**, parity inverted. **hw withdrew their original justification as wrong** |
| **FW-010** | **The two converter links do NOT share a BICK rate** — ADC 128 fs, **DAC 256 fs**, because `SDTI2` is grounded so only Mode 18 works | **ANSWERED: nothing was ever sized against 6.144 MHz; no series termination exists; layout not started.** F70 corrected |
| **FW-011** | **`SDS2-0` must be `000` on both DACs** — any other value reaches the grounded `SDTI2`. **No hardware backstop, no error bit, and the failure is PARTIAL** | **LOGGED by hw.** ⚠ **AMENDED DOWN BY ME (seq 012): `SDS2-0` already DEFAULTS to `000` (T1-F35), so this is a never-disturb invariant, not a boot write.** My original wording overstated the action; the invariant and consequence are unchanged, the probability is lower. hw asked to amend their entry |
| **FW-012** | **W2's 10 ms is set by the `LDOE` STRAP, not the part** — `LDOE`=H+`PSN`=L is case (b), 16384 cycles/10 ms; **`LDOE`=L would be 1 ms.** A strap chosen for a *power* reason silently owns a *boot-timing* property | **RAISED** — back-reference requested at sheet 06 |
| **FW-013** | **Edge rate on the two 12.288 MHz DAC BCLK nets is a FIRMWARE register** (`0xF784`/`0xF794`), because no series termination exists. **Leaving the defaults is a silent decision** | **RAISED** |
| **FW-014** | **`0xF602` `SPDIF_RX_DECODE` reports `AUDIO_TYPE`/`COMPR_TYPE`.** S/PDIF can carry a compressed bitstream; **routed to the DACs as PCM that is full-scale noise into twelve channels, while `SPDIF_LOCK_DET` reads perfectly healthy.** Lock ≠ safe to unmute | **MINE TO BUILD** (hw: inside my authority, closed-book). hw is carrying it to the operator as information, not a gate — it changes what the control API *promises*, and the failure is a speaker/hearing-safety event. **Not waiting** |
| **FW-016** | **§7.2 step 5a has an unwritten precondition — a FIFTH member of the F20/F30 family, inside the step that family was written to protect.** 5b's window is `max(10 ms, 583/fs)`, and **`583/fs` is a count of LRCK periods**: if LRCK is not running when `PDN` is released, the term does not start. **5a-pre covers MCLK only, and MCLK free-runs by construction — `BICK`/`LRCK` come from the ADAU1466 serial port and no strap can make them free-run.** p.53 requires *"MCLK, BICK and LRCK"* | **RAISED, [HARD]-sequence — hw's to escalate, not mine to amend.** `BOOT.md` adds step 3b conservatively. **Suggested §7.2 wording offered, not decided** | **T1** (one T2: whether the DSP serial ports can start before the core) |
| **FW-015** | **M36's "nothing in the boot path can fail" does not extend to the boot path itself.** It writes four registers; **three carry bits a naive write destroys**: `00H` `0x01` clears `DIF2-0` to a Table-13 *unavailable* setting · `0AH` `0x80` **powers off DAC1+DAC2** and moves de-emphasis · `02H` `0x34` clears `HPFE`. Correct: `0x0D`, `0x8D`, `0x35`, `0x20` | **RAISED.** Yields **FD-12**: the boot code writes fields, not values | **T1** (one Table 17 consequence T2) |

**Answered questions handed over by hw:** **F62** — no common sync trigger needed; `RSTN`=0 is
itself a trigger and is the power-on default, alignment referenced to the shared clocks, bound
3/256fs = **244.1 ns** (sources hw's figure); §5 item 5's "by construction" claim **holds**.
**F65** — cannot be observed: no status register on the AK5574, and `OVF`/GPIO12 reports overflow,
not resynchronization. **F66** folded into FW-002.
**F68** *(named by hw three times before either side addressed it)* — **ANSWERED: the firmware
contract must FORBID channel summation and channel power-down on the AK5574.** In serial control
mode the part is permanently in Optimal Data Placement (T1-F33), which removes summation redundancy
and therefore **moves the occupied-slot count**; §4's TDM map and §10's channel↔slot naming are both
[HARD] and cannot follow. **Defaults already comply**, so it is a never-change invariant.
**hw's `07H` read-modify-write item** — explained by T1-F32.

**On F68 nearly fading:** it survived only because bus rule 3 forced it to be named each leg.
**Silence and omission are indistinguishable to the reader** — the rule is what kept a real
invariant from being lost. Same now applies to F71/F75, which I have named without starting.

**Not verified, per rule 3:** BM83 `SDATA_IN1` exclusion (decreed) · safeload addresses (Q8) ·
`SYNCE` default (Q9, T2 from hw) · AK4458 `0AH` default (Q6) · `SDS2-0` bit positions (Q7) ·
**F68 — still unaddressed by either side** · F71, F75, `07H` read-modify-write (not started).

---

## 7. Mistakes ledger

| # | Wrong belief | Correction | The tell |
|---|---|---|---|
| **FM-01** | Cited `REQUIREMENTS.md` as v0.6/v0.9 | It is **v1.8** | **Version was on line 7 and line 21; I read the body, never the header.** Caught by hw |
| **FM-02** | Attributed to hw a claim they did not make | Their items were `RSTN` and `TDM1-0`, not format | **Quote the other side's list verbatim before characterising it.** Caught by hw |
| **FM-03** | Wrote that §4 requires **TDM8** on the ADC link | §4 says `SDATA_IN0` = **TDM4** | **Read the amendment paragraph, skipped the port table three lines below** — same prose-over-table failure as FM-01 |
| **FM-04** | Wrote an outbox file **outside my scope**, into `DSP Design/agent comms/` | Removed; nothing of hw's touched | **Absolute paths outside the immediate working file** |
| **FM-05** | **FW-006: asserted hw's 128 fs "cannot be right" from arithmetic assuming ONE data pin.** hw reopened F70 and logged against themselves on it | AKM spreads channels across SDTI1-2; **both hw citations were exactly right** | **I ran an arithmetic check on a claim without reading the table it came from — after telling hw I would read both tables first. A conclusion that survives for a reason other than the one given is not validated, it is lucky.** Caught by me |
| **FM-06** | Worked the boot sequence for six legs from hw's §4.4 summary and the §5 contract, **without reading `REQUIREMENTS.md` §7.2 itself** | §7.2 carries step 5a-pre, the interleaving argument, and the whole F20/F30 family framing — **and reading it immediately produced FW-016** | **Third instance of the same failure: FM-01 (read §5's body, not the header), FM-03 (read §4's prose, not the port table three lines below), now this. Normative text sat unread while I worked from a summary of it — the exact thing `../CLAUDE.md` §3 classes as advisory-only.** **Read the section before specifying against it.** Caught by me, but late |

---

## 8. Method notes carried forward

- **A check that cannot fail is not a check that passed.** Four instances now: hw's F109
  (footprints), **FW-004** (a `110` readback), **FW-009** (message numbering), and F70 — where hw's
  self-consistency check compared two datasheets *to each other* with no third input. **hw's M35:
  a compatibility check needs THREE inputs — both datasheets AND the artefact.** FD-09 applies the
  same rule forward: do not write a guard for a condition with no observable.
- **Two numbering systems for one thing is where distinctions die.** Slots-on-the-wire vs BICK
  ratio; hw's tell — *"the word **both**"* — generalises to any single figure asserted across two
  links.
- **Two correct facts never brought into contact** (`../CLAUDE.md` §0b) — FW-003, FW-007, F70. On
  F70 hw found the bad figure had **three** correct copies elsewhere in the repo and one wrong copy
  in the most-read block. **A majority of correct copies helps nothing if nothing compares them.**
- **A value owned for one reason can be load-bearing for another.** FW-012 (`LDOE` chosen for power,
  owns boot timing) and the 85 ms (a costing figure until the §7.3 swap). **Record at both ends.**
- **Rule 2 binds on the other agent's numbers, and on mine.** The ADAU1466 addresses came from
  requirements prose and turned out correct — **the verdict is recorded, not just the doubt.**
