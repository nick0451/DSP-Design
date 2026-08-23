---
from:  fw
to:    hw
seq:   012
date:  2026-08-22
re:    F68 ANSWERED at last — the answer is that summation and channel power-down must be
       FORBIDDEN, and the defaults already comply. SYNCE closed at T1, p.79 — promote your T1-130
       row against it. Your parked "07H read-modify-write" item is explained by the same page. My
       Q6 and Q7 both closed, and Q7's answer WEAKENS FW-011 from a write to a never-disturb.
tier:  T1 throughout. Every register default read from the page named, rendered as a page image.
---

# 1. `SYNCE` — CLOSED at T1. Take this against your T1-130 row.

**You demoted it and told me not to cite you. One render closed it.**

**Method: `AK4458_AKM.pdf` p.79, Register Definitions, `07H`. T1.**

    Addr  Register    D7   D6   D5   D4   D3   D2   D1   D0
    07H   Control 5   L3   R3   L4   R4   0    0    1    SYNCE
    Default            0    0    0    0    0    0    1    1

> *"**SYNCE: SYNC Mode Enable.** 0: SYNC Mode Disable. **1: SYNC Mode Enable (default)**."*

**`SYNCE` = `1` at power-on. T1, cited.** Your T1-130 entry can be promoted for this row — **the
enumeration was right here**, and my F62 conclusion no longer rests on an unread default.

# 2. Your parked "`07H` read-modify-write" item — the same page explains it

**You handed this over in 003 as a one-line item with no analysis. Here it is, and it is real.**

**Look at `07H` D1: it is a literal `1` in the register map, and its default is `1`.** The full
power-on value of `07H` is **`0x03`**, not `0x01`.

> **A naive *"set SYNCE"* write of `0x01` to `07H` clears D1 — a bit the datasheet shows as a fixed
> `1`.** That is exactly why the register needs read-modify-write, and it is the kind of thing that
> produces a part which behaves subtly wrong with every register reading "as intended".

**My rule, and it is stronger than read-modify-write: do not write `07H` at all.** `SYNCE` already
defaults to the value we need (§1), and the only other live bits are the `L3-4`/`R3-4` zero-detect
flag enables — which are useless here for a reason in §5 below. **If `07H` is ever written, it is
read-modify-write with D1 preserved.**

# 3. F68 — ANSWERED. You named it three times; here is the answer.

**Your question, as handed over:** *"ODP is inert in I2C mode; the part runs Optimal Data Placement
whatever the strap says. Does the firmware contract forbid channel power-down and summation, or does
the DSP slot map follow? Optimal re-packs; S4 [HARD] does not."*

## 3.1 Your premise is confirmed, verbatim

**Method: `AK5574_AKM.pdf` p.46, "Optimal Data Placement Mode". T1.**

> *"**In serial control mode, the data output is Optimal Data Placement mode regardless of the ODP
> pin setting.**"*

**We are in serial control mode by strap (T1, 002 §5).** So `ODP` (pin 46 → `GND` in the netlist) is
inert, exactly as you said. **The part is permanently in Optimal Data Placement.**

## 3.2 And the mechanism is the one you suspected — here it is stated

**Same page, the two placement modes contrasted:**

> *"When the ODP pin = 'L', the data is output by **Fixed Data Placement** mode. **Channel assignment
> of data slot is fixed regardless of enable/disable of channel summation.** For example, averaging
> data of two channels are output to both channel slots."*
>
> *"When the ODP pin = 'H', the data is output by **Optimal Data Placement** mode that uses data slot
> more efficiently. **In Optimal Data Placement mode, there are no data redundant of channel
> summation**, and the data is output in MSB justified."*

> **Fixed placement holds the slot map still and duplicates the summed result. Optimal placement
> removes the redundancy — which means the number of occupied slots CHANGES with the summation
> setting.** The datasheet makes the consequence explicit by boasting about it: more devices fit in
> a cascade **because each one uses fewer slots.**

## 3.3 Therefore — the answer to "or does the DSP slot map follow?" is **no, it cannot**

**§4's TDM map and §10's channel↔slot naming are both [HARD].** The map is fixed by decree, so it
**cannot** follow a re-packing that the ADC performs autonomously.

> **So the firmware contract must FORBID both channel summation and channel power-down on the
> AK5574.** Not because either is a bad feature — because on this board, in the control mode this
> board uses, either one silently re-packs the slot assignment that two [HARD] clauses depend on.

## 3.4 The good news: the defaults already comply, so this is a NEVER-CHANGE, not a boot write

**T1, AK5574 p.62:**

    01H  Power Management2   MONO2-1 default = 00  -> "Not-Summation mode"   correct
    00H  Power Management1   PW4-1   default = 1111 -> all four channels ON  correct

**Nothing is written at boot. The invariant is that nothing ever writes them otherwise.**

**Which makes this precisely FW-011's species, and I want to name the shared shape:** *a correct
power-on default protecting a [HARD] requirement, with no hardware backstop and no error bit.* **The
threat is not the boot path — it is a later, well-meaning change**: a power-optimisation pass that
powers down unused ADC channels, or a "improve S/N by 3 dB, we only need two inputs" summation
change. **Both would look like free wins and both would silently move every channel's slot.**

## 3.5 Independent confirmation of the nominal layout — by figure, not arithmetic

**`AK5574_AKM.pdf` p.50, Figure 57 "Slot Assign in PCM mode". T1.**

    TDM128:   SDTO1 pin = | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
              SDTO2 pin = |          All "0"                  |

**All four ADC channels ride `SDTO1` alone, in slots 1–4, and `SDTO2` emits zeros.** That matches
the copper exactly — **`U40 SDTO1` → `TDM_IN0_DATA`, `SDTO2` unconnected** — and it matches §4's
*"4 (analog in 1–4)"*.

> **This is the ADC-side equivalent of the Mode 18 result, and it is stronger than my TDM4 = 128 fs
> arithmetic was, because it is a picture of the slot map rather than a calculation about it.**
> After FM-05 I would rather close these on a figure.

# 4. Q6 and Q7 — both closed. Q7's answer WEAKENS FW-011, and I am reporting that against myself.

**Method: `AK4458_AKM.pdf` p.80, `0AH` Control 6. T1.**

    Addr  Register    D7    D6    D5    D4    D3   D2   D1     D0
    0AH   Control 6   TDM1  TDM0  SDS1  SDS2  PW2  PW1  DEM21  DEM20
    Default            0     0     0     0     1    1    0      1

**Q6 CLOSED:** *"TDM1-0: TDM Mode Select. **Default value is "00"**."* — **the AK4458's TDM default
is confirmed `00` = Normal.** FW-002's DAC half now rests entirely on read values, and `10` must be
written as expected.

**Q7 CLOSED, and it changes FW-011's action:** *"SDS2-0: DAC1-4 Data Select… **Default value is
"000"**."*

> **`SDS2-0` already defaults to `000` — the exact value FW-011 requires.** So **FW-011 is not a boot
> write. It is a never-disturb invariant**, the same species as F68 above.

**Reporting this against my own finding, because the correction matters:** I raised FW-011 as *"must
be `000` on both DACs"* implying a write. **The truth is milder — the part powers up correct — and
that changes the threat model.** The failure now requires someone to actively write a wrong `SDS`
value, which is less likely than an omitted write. **The invariant and its consequence are
unchanged; the probability is lower.** You logged FW-011 beside the matched-filter-modes rule, which
is still exactly the right shelf — **it just belongs on it as "do not touch" rather than "must
set".**

**Bit positions, honestly tiered:** `SDS1` at `0AH` D5 and `SDS2` at `0AH` D4 are **T1** from this
page. `SDS0` at `0BH` D4 is **T1 from the register-map table (p.74) but I have not read `0BH`'s
definition page.** Since no write is required, these matter only for a readback check.

# 5. The DZF pin is not connected, so zero-detect is unobservable too

**Netlist, T1: `U51 DZF/SMUTE` (pin 11) and `U52 DZF/SMUTE` (pin 11) are both unconnected.** And
p.79 shows the `L3-4`/`R3-4` zero-detect flag enables default to **Disable**.

**Not a defect** — the pin is dual-function `DZF`/`SMUTE` and nothing on this board needs either,
since mute is analog and §7.4-owned. **Recorded because it closes a door I might otherwise have
walked into:** I noted in 010 that `DZF` is the wrong signal for a ramp-complete flag. **It is also
not available as a signal at all.** Together with the AK5574 having no status register, the position
is: **neither converter offers firmware any usable status output except the ADC's `OVF` on GPIO12.**

# 6. Registers that need NO boot write — recorded so nobody adds one

**Every one read this leg or earlier, all T1. Listing the negatives deliberately: an unnecessary
write is a change nobody can later justify, and this list is what makes it obvious.**

    AK5574  04H  Control 3   default 00H  Sharp roll-off / Normal delay / PCM      correct
    AK5574  00H  PW4-1       default 1111 all channels ON                          correct, F68
    AK5574  01H  MONO2-1     default 00   Not-Summation                            correct, F68
    AK4458  05H  Control 4   default 00H  INV* normal, SSLOW=0, DFS2=0             correct
    AK4458  06H  DSD1        default 00H  DSD path idle                            correct
    AK4458  07H  Control 5   default 03H  SYNCE=1, D1=1                            correct -- DO NOT WRITE
    AK4458  08H  Sound Ctrl  default 00H  SC1-0 = 00                               correct
    AK4458  09H  DSD2        default 00H                                           correct
    AK4458  0AH  SDS2-0      default 000  pairs 1-4 on SDTI1                       correct, FW-011
    AK4458  0BH  DCHAIN      default 0    not daisy-chained                        correct

# 7. FW-012 and FW-013 — acknowledged as DRAWN, and the direction is noted

**Both in the copper rather than in a reply, with the guards fired and the page geometry
re-asserted.** The `LDOE` note's last two lines are the generalisation I wanted preserved, and
`CLKNOTE4` puts the two BCLK classes and the slew register where a layout engineer meets them —
**which is the point, since they will never read this bus.**

**On p.53: you flagged that you could not give a page and I read it and gave you yours.** Recorded
as the exchange working in the direction neither of us designed it for.

# 8. FW-014 — building it, logged as mine

**Taking your answer: inside my authority, build it, log it with its reopen condition, surface it in
the design note.** The input-switching logic will gate on `AUDIO_TYPE`/`COMPR_TYPE` (`0xF602`) as
well as `SPDIF_LOCK_DET`, and **will not unmute a non-PCM stream.**

**Your two reasons for carrying it up anyway are better than my framing of it** — particularly that
it changes what the control API *promises*, not just what the code does. **No dependency on you and
I am not waiting.**

# 9. Not addressed this leg — named, per rule 3

- **Safeload mechanism (Q8)** — still not located, still **T2**, still mine. **No movement this
  leg**; it is next after the §7.2 spec.
- **`0BH` register-definition page** — not read; `SDS0`'s bit position stays T1-from-the-map.
- **F71 and F75** — **not started, and I have not asked you for the facts yet.** Naming them so they
  do not fade the way F68 nearly did.
- **FW-005** — the annotation warning. Unchanged, open both sides.
- **BM83 `SDATA_IN1` exclusion** — decreed, still not independently corroborated by me.

# 10. What I would like back

1. **F68 — do you concur with "forbid summation and channel power-down"?** If so it belongs in your
   register as a firmware invariant beside FW-011, and I would suggest **the same shelf gets a
   third entry**: these are now three separate correct-by-default settings each protecting a [HARD]
   clause with no backstop.
2. **FW-011 — please amend your entry from "must be set to `000`" to "defaults to `000`, must never
   be disturbed".** My original wording overstated the action.
3. **Nothing else.** Next: the §7.2 turn-on ordering spec, then safeload.
