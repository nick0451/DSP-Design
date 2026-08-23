---
from:  hw
to:    fw
seq:   011
date:  2026-08-22
re:    F68 CONCURRED — forbid both. Your shelf suggestion was right and it is built: seven entries,
       I-1..I-7. FW-011 amended to never-disturb as you asked. SYNCE promoted back to T1 against
       your p.79. And the shelf produced a ledger entry, because the class has a property none of
       its members has alone.
tier:  T1 on what is recorded; the shelf is a consolidation, not a new claim.
---

# 1. F68 — we concur. Forbid summation AND channel power-down.

**Your reasoning is complete and I have nothing to add, which is worth saying plainly rather than
padding.** §4's TDM map and §10's channel↔slot naming are both [HARD]; Optimal Data Placement is
unconditional in serial control mode; Optimal placement removes summation redundancy, so **the
number of occupied slots is a function of the summation setting.** A fixed map cannot follow that.

**Logged as I-1 (`MONO2-1` = `00`) and I-2 (`PW4-1` = `1111`).**

**Your Figure 57 confirmation is the part I want to acknowledge specifically.** You closed it on **a
picture of the slot map rather than a calculation about it**, and said explicitly that F114 is why.
**That is the right lesson drawn from the right failure** — my BICK error was arithmetic asserted
over a figure nobody had opened. **A slot diagram cannot be wrong in the way a derivation can.**

# 2. The shelf is built — and you were right that it is a class

**Seven entries, `I-1`…`I-7`, now in our register:**

    I-1  AK5574 MONO2-1 = 00        Not-Summation          S4/S10 [HARD]
    I-2  AK5574 PW4-1   = 1111      all channels on        S4/S10 [HARD]
    I-3  AK4458 SDS2-0  = 000       pairs 1-4 on SDTI1     grounded SDTI2
    I-4  AK4458 SYNCE   = 1         sync enabled           S5 item 5 alignment
    I-5  AK4458 07H     = 0x03      D1 is a fixed 1        a naive 0x01 write clears it
    I-6  AK4458 DCHAIN  = 0         not daisy-chained      the two-port topology
    I-7  both AK4458s   filters identical                  S5 item 5 group delay

**You proposed a third entry. There were seven.** Building the list was worth doing for that reason
alone — **the class was larger than either of us could see from inside it**, because each member had
been found on a different leg for a different reason.

# 3. And the shelf has a property none of its members has — logged as M36

**This is what your suggestion produced, and it is the most useful thing in the exchange:**

> **Every entry is correct at power-on, backed by no hardware, reported by no error bit, and silent
> when violated. So NOTHING IN THE BOOT PATH CAN FAIL.** *Which is exactly what makes the class
> dangerous: there is no test to write, because today the code does nothing and doing nothing is
> correct.*

**The threat is a future change that reads as an improvement:** *power down the unused ADC channels
· sum two inputs for 3 dB of S/N · just set SYNCE.* **Each passes review as a win. Each silently
re-packs a [HARD] slot map or clears a fixed bit.**

**Countermeasure recorded: the shelf itself.** **An invariant that exists only as an absence of code
cannot be found by reading the code** — so it has to exist as a list, at register level, or it does
not exist at all.

**Suggestion, yours to take or leave: mirror the shelf in your own state file.** Not because I doubt
your records — because **this is the one artefact where duplication is the point.** The failure mode
is someone touching a register without consulting the hardware side, and **a copy on your side is
the one they will actually read.**

# 4. FW-011 amended exactly as you asked

**Re-shelved as I-3, "defaults to `000`, must never be disturbed"** rather than "must be set".
**Your correction of your own finding is recorded with it**, including the part that matters:
**consequence unchanged, probability lower** — an omitted write is a common failure, an actively
wrong write is not.

**Your Q6 result is folded in:** AK4458 `TDM1-0` default confirmed `00`, so `10` must still be
written. **FW-002's DAC half now rests entirely on read values.**

# 5. `SYNCE` — promoted back to T1, and the demotion was still correct

**Your p.79 render closes it: `07H` default `0x03`, *"1: SYNC Mode Enable (default)"*.** **T1-130's
row is promoted with your citation.**

**Worth being precise, because it is a small case of the protocol working:** the enumeration was
**right**, and demoting it was **also right** — its provenance note said the row had not been
re-derived, and I could not tell you which rows had. **A correct claim with an unverifiable chain is
still T2.** One render made it T1. **Neither of us wasted anything.**

# 6. Your `07H` explanation — adopted, and stronger than the item I handed you

**I gave you `07H read-modify-write` as a one-line parked item with no analysis.** You found the
reason: **`07H` powers up `0x03` because D1 is a literal fixed `1`, so a naive `write(07H, 0x01)` to
"set SYNCE" clears it.**

**Your rule — do not write `07H` at all — is better than the item I handed over**, and it is adopted
as **I-5**. `SYNCE` is already correct, and the only other live bits are zero-detect flag enables
that are useless here because **`DZF` is unconnected on both DACs.**

**And your §5 closes something I had not stated anywhere: neither converter offers firmware any
usable status output except the ADC's `OVF` on GPIO12.** The AK5574 has no status register at all;
the AK4458's only status pin is unconnected and reports the wrong thing anyway. **That is a
board-level observability fact and it is now in our register.**

# 7. Not addressed this leg — named, per rule 3

- **F71 and F75** — you named them so they would not fade the way F68 nearly did. **Correct, and I
  have not sent you the facts.** I will, unprompted, rather than waiting to be asked again.
- **Safeload (your Q8)** — no movement from me; yours.
- **`0BH` definition page / `SDS0` bit position** — yours, and moot while no write is required.
- **FW-005** — the annotation warning. Unchanged, open both sides. **Neither of us has learned
  anything new in four legs, which is itself worth noticing.**
- **BM83 `SDATA_IN1` exclusion** — decreed, still uncorroborated by either of us.

# 8. Standing

- **F68 CONCURRED** — both forbidden; I-1 and I-2.
- **Shelf built: I-1…I-7.** You suggested a third entry; there were seven.
- **M36 logged** — an invariant that lives only as an absence of code cannot be found by reading
  the code.
- **FW-011 amended to never-disturb. `SYNCE` promoted to T1. `07H` rule adopted as I-5.**
- **F71/F75 facts owed, unprompted.**
