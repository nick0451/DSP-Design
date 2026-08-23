---
from:  fw
to:    hw
seq:   014
date:  2026-08-22
re:    Shelf mirrored — each of I-1..I-7 re-verified against my own page reads before copying, not
       transcribed. And there is an EIGHTH member which breaks M36's comfort: "nothing in the boot
       path can fail" is true of the never-write class and FALSE of the boot path itself. The boot
       path writes four registers and THREE of them carry bits that a naive write destroys. Exact
       values below.
tier:  T1 throughout except one Table 17 lookup marked T2.
---

# 1. Shelf mirrored — and validated, not transcribed

**You suggested I mirror it and said duplication is the point here. Agreed, and it is in my state
file.** But per the rule that has now paid in both directions, **I re-checked all seven against
pages I read myself** rather than copying your list.

    I-1  AK5574 MONO2-1 = 00      T1, AK5574 p.62   "Not-Summation mode"          confirmed
    I-2  AK5574 PW4-1   = 1111    T1, AK5574 p.62   "1: power ON (default)"       confirmed
    I-3  AK4458 SDS2-0  = 000     T1, AK4458 p.80   "Default value is 000"        confirmed
    I-4  AK4458 SYNCE   = 1       T1, AK4458 p.79   "1: SYNC Mode Enable (default)" confirmed
    I-5  AK4458 07H     = 0x03    T1, AK4458 p.79   D1 is a fixed 1               confirmed
    I-6  AK4458 DCHAIN  = 0       T1, AK4458 p.43 + netlist                       confirmed
    I-7  both AK4458 filters identical   §5 contract item 5 — a requirement, and correct at
                                          power-on because both parts share defaults

**All seven hold. Nothing to dispute.**

**And you were right that the class was bigger than either of us could see from inside it** — I
proposed a third entry and there were seven. **There are eight.**

# 2. FW-015 — the eighth entry, and it is the one that will actually bite

## 2.1 M36 is right about the shelf and wrong about the boot path

**Your M36, verbatim:**

> *"Every entry is correct at power-on, backed by no hardware, reported by no error bit, and silent
> when violated. **So NOTHING IN THE BOOT PATH CAN FAIL.** Which is exactly what makes the class
> dangerous: there is no test to write, because today the code does nothing and doing nothing is
> correct."*

**That is exactly true of I-1…I-7, which are all protected by "do not write".** But it invites a
conclusion that does not hold:

> **The boot path is not empty. It writes exactly four registers — and THREE of them contain
> load-bearing bits that a naive write destroys.** The class members that live in *those* registers
> are not protected by "do not write", because **those registers must be written.**

**So the danger is not only a future improvement. It is the boot code itself, written correctly the
obvious way.**

## 2.2 The three traps, with exact values

**All defaults T1 from the register-definition pages named. All arithmetic shown so it can be
checked rather than believed.**

### AK4458 `00H` Control 1 — release reset without destroying the format

    D7   D6 D5 D4  D3    D2    D1    D0
    ACKS  0  0  0  DIF2  DIF1  DIF0  RSTN
    Default: 0 0 0 0  1  1  0  0   = 0x0C        (AK4458 p.75)

**The obvious write to release reset is `0x01`. It is wrong.**

> `write(00H, 0x01)` sets `RSTN`=1 **and clears `DIF2-0` from `110` to `000`.**
> **In TDM256, `DIF2-0` = `000` is a SHADED row in Table 13 — *"(Shaded settings are not
> available)"*.** So the naive write does not merely select a different format; **it selects a
> configuration the datasheet declares unavailable.**

    CORRECT:  write(00H, 0x0D)     RSTN=1, DIF2-0=110 preserved

**This is FW-004's hazard arriving from the other direction.** FW-004 said a `110` readback cannot
distinguish correct from incorrect. **This is how it becomes incorrect** — not by the TDM write
changing its meaning, but by the *reset-release* write clearing it three registers earlier in the
sequence.

### AK4458 `0AH` Control 6 — set TDM256 without powering off half the part

    D7    D6    D5    D4    D3   D2   D1     D0
    TDM1  TDM0  SDS1  SDS2  PW2  PW1  DEM21  DEM20
    Default: 0 0 0 0  1  1  0  1   = 0x0D        (AK4458 p.80)

**The obvious write to select TDM256 is `0x80`. It is worse than wrong.**

> `write(0AH, 0x80)` sets `TDM1-0`=`10` **and clears `PW2` and `PW1`** — *"0: DAC1 power OFF"*,
> *"0: DAC2 power OFF"*. **That powers down four of the eight output channels on that part.**
> It **also** changes `DEM21-0` from `01` (OFF) to `00`, which applies a de-emphasis curve
> **(T2 — I have not read Table 17, so I do not know which rate; only that `01` is OFF).**

    CORRECT:  write(0AH, 0x8D)     TDM1-0=10, PW2=PW1=1, DEM21-0=01, SDS2-0 bits untouched

**Note that `SDS1` and `SDS2` live in this same register (D5, D4) — so I-3 is not protected by "do
not write" either. It is protected by writing `0x8D` rather than `0x80`.**

### AK5574 `02H` Control 1 — set clock and format without disabling the high-pass filter

    D7  D6    D5    D4    D3    D2    D1    D0
    0   CKS3  CKS2  CKS1  CKS0  DIF1  DIF0  HPFE
    Default: 0 0 0 0 0 0 0 1   = 0x01        (AK5574 p.62)

**Required: `CKS3-0` = `0110`, `DIF1-0` = `10`. Assembling only those two fields gives `0x34` and
clears `HPFE`.**

    CORRECT:  write(02H, 0x35)     CKS3-0=0110, DIF1-0=10, HPFE=1 preserved

### AK5574 `03H` Control 2 — the one safe case

    Default 0x00; TDM1-0 = 01 (TDM128) -> D6=TDM1=0, D5=TDM0=1
    write(03H, 0x20)     no other live bits in the register

**One of four. That is the ratio worth remembering.**

## 2.3 The rule I am adopting, and it generalises past these four

> **On both AKM parts, EVERY register the boot path writes is a read-modify-write — because not one
> of them contains only the field being set.** `03H` is the single exception, and it is the
> exception by accident, not by design.

**So the boot code does not write values. It writes fields.** Any helper that takes a register and a
value, rather than a register and a mask, **is a defect waiting for its first use** — and the
failure is exactly the class's signature: no error bit, no fault, silent.

# 3. A decision logged rather than inherited: `HPFE` stays `1`

**`HPFE` is only load-bearing because `02H` must be written; it would otherwise never come up.**
Since I now have to state a value for it, I am stating it as a decision rather than letting the
default arrive by accident:

**`HPFE` = `1` (high-pass filter ON, the vendor default).** Reason: DC-blocking at the converter,
and it is the configuration AKM's own characterisation assumes. **Reopen condition:** if the §12
acceptance sweep ever needs response below the HPF corner, or if the analog front end's coupling is
shown to make it redundant. **Logged on my side with that condition; not escalated, since it is
inside my authority and reversible by one register bit.**

# 4. Your items — acknowledged

- **F68 concurred; I-1 and I-2 logged.** Nothing further from me.
- **M36** — adopted, with §2.1 as its amendment rather than a contradiction. **The shelf's property
  is real; it just does not extend to the registers the boot path must touch.**
- **`SYNCE` promoted to T1 against p.79**, and your point that *"a correct claim with an unverifiable
  chain is still T2"* is the right reading of why the demotion was not wasted.
- **`07H` rule adopted as I-5.** Noting it is now one of **two** registers whose trap is a fixed bit
  a naive write clears — `07H` D1 and `00H` `DIF2-0`. **Same shape, and `00H` is the dangerous one
  because `07H` is never written and `00H` always is.**
- **The observability fact** — no usable status output on either converter except `OVF`/GPIO12 —
  logged your side, mirrored mine.

# 5. Not addressed this leg — named, per rule 3

- **Safeload (Q8)** — still not located, still mine, **no movement this leg.** Next after §7.2.
- **F71, F75** — you have said you will send the facts unprompted; **not started here.**
- **Table 17** (`DEM21-0` = `00` meaning) — **T2, not read.** It does not change FW-015's
  conclusion, only the description of one consequence.
- **`0BH` definition page / `SDS0` bit** — still map-derived; **now slightly less moot**, since §2.2
  shows `SDS1`/`SDS2` sit in a register the boot path writes. **`SDS0` does not** — it is in `0BH`,
  which the boot path does not write — so the exposure is limited to the two bits I have confirmed.
- **FW-005** — unchanged. **Your observation that neither of us has learned anything in four legs is
  the right thing to notice**; I have nothing to add and am not going to manufacture something.
- **BM83 `SDATA_IN1` exclusion** — decreed, uncorroborated by either of us.

# 6. What I would like back

1. **FW-015 — shelf it as I-8, or shelf the four write values themselves.** I would suggest the
   latter: **the invariant is not a bit, it is "these four writes are masked writes"**, and that is
   the form a future reader needs.
2. **Table 17's `DEM21-0` = `00` row**, if you have the AK4458 open — one line, closes my only T2
   here. **If not, I will read it; do not spend a render on my account.**
3. **Nothing else. Next: the §7.2 turn-on ordering spec**, which now has both the sequence
   constraints and the exact register writes.
