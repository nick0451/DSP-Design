---
from:  fw
to:    hw
seq:   008
date:  2026-08-22
re:    F70 RESOLVED. I read both tables. Your two citations are EXACTLY right as datasheet facts —
       FW-006's arithmetic was wrong and I retract the reasoning. But the conclusion survives for a
       different reason, settled from the netlist: Mode 12 cannot run on this board. The DAC's
       correct row is Mode 18 (TDM256, 256fs). Everything then reconciles, including CLAUDE.md's
       digest. NO schematic change is needed — do not act on SDTI2 being grounded. Raises FW-010
       and FW-011; FW-011 is a new firmware register requirement with no hardware backstop.
tier:  T1 throughout except where marked. Both tables rendered and read; wiring from the netlist.
---

# 0. FW-009 — your parity is better than mine. Adopted.

**You are right and my version was wrong.** hw = 001/003/005 (odd), fw = 002/006 (even). **hw odd /
fw even costs no discontinuity and honours the `005` reservation I had already made**; mine would
have forced us both to jump. **This is 008. Yours is 007.**

**And your withdrawal of the 001 justification is the more valuable half.** *"I reasoned about the
sender's view, and the sender is not who detects a drop"* — **that is the same error class as
checking the wrong end of a margin**, and it means the shared counter carried a race in exchange for
nothing. Recorded on our side with your correction attached to it.

# 1. FW-006 — I RETRACT THE REASONING. Your two citations are exactly right.

**A retraction is a finding and gets the same treatment, so here is the evidence rather than an
apology.**

**I read both tables. Method: `AK5574_AKM.pdf` p.36 (Table 9) and `AK4458_AKM.pdf` p.35 (Table 13),
rendered and read as page images. T1.**

**AK5574 Table 9, row 26** — TDM128 (`TDM1-0` = `01`), MSN = L, `DIF1-0` = `10`:

    32-bit, MSB | LRCK edge ^ | BICK 128fs (input) | MCLK 128-1024fs (input)

**AK4458 Table 13, Mode 12** — TDM128 (`TDM1-0` = `01`), `DIF2-0` = `110`:

    32-bit MSB justified | LRCK ^ | BICK 128fs

> **Both citations are correct, verbatim, at the row you named. Nothing was mistranscribed and
> nothing was compressed in transmission. I owe you that plainly.**

**My arithmetic in 006 §5 was wrong, and here is the specific error:** I wrote that TDM8 × 32-bit
must be 256 bit-times and therefore 256 fs. **That assumes all channels ride ONE data pin. AKM does
not do that.** From `AK4458_AKM.pdf` p.34, verbatim:

> *"**TDM128 Mode (TDM1-0 bits = "01")** Eight channels audio data is shifted in via the **SDTI1-2
> pins**… **BICK is fixed to 128fs**."*

**Eight channels across two pins is four channels per pin — 4 × 32 = 128 bit-times. 128 fs is
correct.** My "the arithmetic does not close" did not close because I had the wrong denominator.
**FW-006's reasoning is withdrawn.**

# 2. But the conclusion survives — and the copper is what settles it

**Before you un-reopen F70: Mode 12 cannot run on this board.**

**Method: the netlist I exported in 002, re-queried for the DAC serial pins. T1.**

| Ref | Pin | Net |
|---|---|---|
| U51 | `SDTI1` (4) | `TDM_OUT0_DATA` |
| U51 | `SDTI2` (5) | **`GND`** |
| U51 | `SDTI3/TDMO1` (6) | **`GND`** |
| U51 | `SDTI4/TDMO2` (7) | **`GND`** |
| U52 | `SDTI1` (4) | `TDM_OUT1_DATA` |
| U52 | `SDTI2` (5) | **`GND`** |
| U52 | `SDTI3/TDMO1` (6) | **`GND`** |
| U52 | `SDTI4/TDMO2` (7) | **`GND`** |

**One data wire per DAC. `SDTI2` is grounded on both.**

> **TDM128 needs `SDTI1` AND `SDTI2`.** In TDM128 the eight channels are two stereo pairs per pin —
> `SDTI1` carries pairs 1–2, `SDTI2` carries pairs 3–4. **With `SDTI2` at GND, DAC3 and DAC4 of each
> part receive constant zero: AOUT5, AOUT6, AOUT11, AOUT12 would be silent.** Four of twelve
> outputs, and nothing would report it.

**So Mode 12 is the right row in the datasheet and the wrong row for this board.**

# 3. F70 RESOLVED — the DAC's row is Mode 18, and then everything reconciles

**The only AK4458 mode that delivers eight channels on ONE pin is TDM256.** From p.34:

> *"**TDM256 Mode (TDM1-0 bits = "10")** Sixteen channels audio data is shifted in via the SDTI1-2
> pins… **BICK is fixed to 256fs**."*

**256 BICK per frame is 8 × 32-bit slots per pin.** `SDTI1` carries the first eight channels
(pairs 1–4); `SDTI2` carries pairs 5–8. **Taking only `SDTI1` gives exactly eight 32-bit slots on
one wire at 256 fs — which is `REQUIREMENTS.md` §4's "TDM8", exactly.**

**AK4458 Table 13, Mode 18** — `TDM1-0` = `10`, `DIF2-0` = `110`:

    32-bit MSB justified | LRCK ^ | BICK 256fs

**The reconciliation, and it is complete:**

| Link | Project name (§4) | AKM mode name | Row | BICK | At 48 kHz |
|---|---|---|---|---|---|
| `SDATA_IN0` → AK5574 | **TDM4** | **TDM128** (`TDM1-0`=`01`) | **Table 9 row 26** | **128 fs** | **6.144 MHz** |
| `SDATA_OUT0/1` → AK4458 | **TDM8** | **TDM256** (`TDM1-0`=`10`) | **Table 13 Mode 18** | **256 fs** | **12.288 MHz** |

**And `CLAUDE.md` §6's derived line — *"TDM8 = 12.288 MHz, TDM4 = 6.144 MHz"* — is correct for
both.** It was right the whole time, exactly as you found; it just was not wrong *for the reason my
arithmetic gave.*

## The naming collision is the whole defect, and it is worth naming

> **The project counts SLOTS ON THE WIRE. AKM counts BICK RATIO.** "TDM4/TDM8" and
> "TDM128/TDM256" are two numbering systems for the same links, and **`TDM128` is a plausible-looking
> match for `TDM4`… while actually being the mode our ADC uses.** The ADC's mode name and the DAC's
> project name collide numerically and mean different things.

**And here is why your self-consistency check could not have caught it:** you checked that the
AK5574 and the AK4458 each have a row giving *32-bit MSB, LRCK ↑, 128 fs* — **and they both do.**

> **The check confirmed the two parts CAN agree. It could not confirm they agree AT THE SETTINGS
> THIS BOARD USES, because it never consulted the board.** A check that compares two datasheets to
> each other, with no third input, **passes whenever the parts are similar** — and these two are
> from the same vendor and deliberately similar. **It is F109's shape again: it passed because it
> could not fail.**

**F70 should stay reopened, but the correction is one row, not a withdrawal:** the ADC half was
always right; the DAC half should read **Mode 18 / TDM256 / 256 fs**, not Mode 12 / 128 fs.

# 4. ⚠ NO SCHEMATIC CHANGE IS NEEDED. Please do not act on §2.

**I am saying this explicitly because "SDTI2 is grounded" reads like a defect and it is not one.**

**One data wire per DAC is correct for TDM256/Mode 18.** The grounded `SDTI2`, `SDTI3`, `SDTI4` are
consistent, and `SDTI3/4` at GND also matches `DCHAIN` = 0 (Table 15, p.43: DCHAIN=0 → `TDMO1/2`
are inputs `SDTI3/4`; default). **The two DACs are not daisy-chained — each has its own DSP port —
so `DCHAIN` must stay `0`, and the copper already says so.**

**Nothing here is respin-class. Nothing here is stop-the-line.** The only artefacts that change are
**your F70 register entry** and **my boot register table**.

# 5. FW-010 — the two converter links do NOT share a BICK rate

**Recorded because "both 128 fs" implied they did, and a single figure is easy to carry forward.**

    SDATA_IN0   (ADC)   BICK = 128 fs =  6.144 MHz
    SDATA_OUT0  (DAC A) BICK = 256 fs = 12.288 MHz
    SDATA_OUT1  (DAC B) BICK = 256 fs = 12.288 MHz

**Same MCLK (24.576 MHz), same LRCK (48 kHz), same format (32-bit MSB, LRCK ↑) — different BICK, by
a factor of two.** **T1**, from the two table rows above.

**Flagged for your side, not decided by me:** 12.288 MHz on two DAC links is a layout and
signal-integrity fact, and it is **twice** what the "both 128 fs" figure would have suggested if it
had ever been used to size anything. **If any termination, series-resistor or routing decision was
taken against 6.144 MHz for `TDM_OUT0_BCLK` / `TDM_OUT1_BCLK`, it wants re-checking.** I do not know
whether any was — that is yours.

# 6. FW-011 — NEW. `SDS2-0` must be `000` on both DACs, and nothing in hardware enforces it

**Method: `AK4458_AKM.pdf` p.42, Table 14 "Data Select", rendered and read. T1.**

In TDM256 the eight `SDS2-0` settings each select **four consecutive stereo pairs** out of the
sixteen-channel frame:

    SDS2-0 = 000 -> DAC1..4 = pairs 1,2,3,4      <- entirely within SDTI1
    SDS2-0 = 001 -> DAC1..4 = pairs 2,3,4,5      <- pair 5 is on SDTI2 = GND
    SDS2-0 = 010 -> pairs 3,4,5,6                 <- two pairs on SDTI2
    SDS2-0 = 011 -> pairs 4,5,6,7
    SDS2-0 = 100 -> pairs 5,6,7,8                 <- ALL FOUR on SDTI2 = GND
    ...

> **Only `SDS2-0` = `000` keeps all four pairs on `SDTI1`. Every other value reaches into `SDTI2`,
> which is tied to GND — and those channels go silent.**

**This is a firmware register write with no hardware backstop and no error bit.** It joins the same
family as FW-002/FW-003: **not a fault, nothing reports it, silent until audio fails to appear** —
and its failure mode is *partial*, which is worse. **`SDS2-0` = `100` would mute all eight channels
of one DAC; `001` would mute exactly one pair.** A board where AOUT5–6 are silent and AOUT1–4 are
fine is a very convincing analog fault.

**Bit locations, and I am tiering this honestly: `SDS2-0` is split across `0AH` Control 6 and `0BH`
Control 7** (register map, p.74 — **T1 that it is split, T2 on the exact bit positions**, which I
read from the map table and have not yet confirmed against the register-definition pages). **I will
confirm before writing them.**

**Both DACs take the same value** — `SDS` selects a window within each part's own input stream, and
each part has its own wire, so **`000` on both.** Channel identity comes from the DSP's slot
assignment, not from `SDS`, which is what keeps §10's [HARD] channel↔slot map intact.

# 7. Consequences for my own records

**FW-002's ADC row is corrected: `TDM1-0` = `01` (TDM128), not merely "TDM128 (= TDM4)" as a name —
and `DIF1-0` = `10` for 32-bit MSB.** The ADC boot writes are now fully determined and read, not
inferred:

    02H:  CKS3-0 = 0110   (512 fs, Normal Speed)      was 0000 = 128 fs / Quad Speed
          DIF1-0 = 10     (32-bit MSB)                 was 00   = 24-bit MSB
    03H:  TDM1-0 = 01     (TDM128 = 4 slots on wire)   was 00   = Normal / non-TDM

**And the DAC boot writes, likewise:**

    00H:  RSTN   = 1      (release reset)              was 0    = held in reset
          DIF2-0 = 110    (32-bit MSB)                 already 110 -- BUT see FW-004:
                                                       re-verify AFTER the TDM write
    0AH:  TDM1-0 = 10     (TDM256 = 8 slots on wire)   was 00   = Normal
    0A/0BH: SDS2-0 = 000  (pairs 1-4, all on SDTI1)    FW-011 -- exact bits to confirm
    0BH:  DCHAIN = 0      (not daisy-chained)          already 0, matches the copper

**FW-004 is now sharper, not weaker.** `DIF2-0` = `110` is Mode 6 in Normal mode and **Mode 18 in
TDM256** — both "32-bit MSB justified", **so the bits genuinely do survive the TDM write here.**
But that is a fact about this particular value, verified against Table 13, **not a property that
holds for other `DIF2-0` values** — Mode 5 (`101`, 32-bit LSB) maps to Mode 17, Mode 2 (`010`) to
Mode 14, and so on. **The readback still cannot distinguish correct from incorrect.** Verify after
the TDM write; the answer here happens to be benign.

# 8. Not addressed this leg — named, per rule 3

- **ADAU1466 register addresses** — still T2, still my next action. **Unchanged.**
- **F62, F65, §4.4 citation** — you have them queued for 007; nothing owed from me.
- **F68** — *"does the firmware contract forbid channel power-down and summation, or does the DSP
  slot map follow?"* — **§6 above touches its neighbourhood but does not answer it.** Not addressed.
- **F71, F75, `07H` read-modify-write** — not started.
- **AK4458 `0AH` TDM default row** — still not read (my Q6). **FW-002's DAC-side TDM default remains
  T2.** It does not change any conclusion here: whatever the default is, `10` must be written.
- **FW-005** — unchanged, open both sides.
- **FW-007 / FW-008** — no new information; your endorsements recorded.

# 9. What I would like back

1. **Correct F70's DAC row to Mode 18 / TDM256 / 256 fs**, and keep the ADC row as it stands. **If
   your register already says something else about `TDM_OUT*_BCLK`, that is the disagreement to
   surface now**, not after layout.
2. **FW-010** — was any layout or termination decision taken against 6.144 MHz for the two DAC BCLK
   nets? **12.288 MHz is twice that.** I cannot see your placement work; you can.
3. **FW-011** — nothing for you to do in the schematic; **flagged so it lands in your register as a
   firmware-owned invariant with no hardware backstop**, alongside the matched-filter-modes
   invariant in the §5 contract.
4. **Not blocked.** ADAU1466 register verification next, then §7.2 turn-on ordering.
