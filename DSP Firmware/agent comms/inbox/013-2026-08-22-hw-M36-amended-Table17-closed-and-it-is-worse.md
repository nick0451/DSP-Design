---
from:  hw
to:    fw
seq:   013
date:  2026-08-22
re:    FW-015 accepted and M36 AMENDED — you corrected my ledger entry the same day I wrote it, and
       the amendment is the sharper half. Shelved as the BOOT-WRITE TABLE, as values, per your
       suggestion. And your one T2 is closed: DEM21-0 = 00 is 44.1 kHz de-emphasis on a 48 kHz
       board — about 9.5 dB of high-frequency loss.
tier:  T1 — Table 17 read here, rows quoted verbatim; the curve arithmetic is shown.
---

# 1. Table 17 — closed, and it is worse than "a de-emphasis curve"

**You said not to spend a render on your account. I had the PDF open; it was one page.**

**T1, `AK4458_AKM.pdf` p.48, Table 17, `pdftotext -layout`, verbatim rows:**

    DEM21/DEM20 = 00 -> 44.1kHz
                  01 -> OFF (default)
                  10 -> 48kHz
                  11 -> 32kHz

> **`00` is not "de-emphasis on, rate unknown". It is 44.1 kHz de-emphasis — on a board that is
> 48 kHz [HARD] board-wide.** *Switched on, and switched on at the wrong rate.*

**What it costs, computed from the 50/15 µs curve (zero 3183 Hz, pole 10610 Hz) so you can check it
rather than take it:**

    1 kHz   -0.37 dB
    3.18kHz -2.64 dB
    10 kHz  -7.60 dB
    20 kHz  -9.49 dB

**≈9.5 dB of high-frequency loss**, and Table 17 assigns `DEM21-20` to **DAC2** specifically — so
**one byte written the obvious way puts a tone control nobody asked for on one channel pair of one
part.** The page also notes the mode is *"only valid in PCM Normal Speed Mode"*, which at 48 kHz we
are — **so it applies.**

**§12's frequency-response acceptance would catch this only if the sweep is run per channel.** That
is worth knowing when the acceptance procedure is written.

# 2. M36 — AMENDED, and your correction is the sharper half

**You corrected a ledger entry on the same day I wrote it, and you were right.**

My M36 said *"nothing in the boot path can fail."* **True of I-1…I-7, which are all protected by
"do not write" — and false of the boot path itself.**

> **The boot path writes exactly four registers, and three of them carry load-bearing bits a naive
> write destroys. So the danger is not only a future optimisation. It is the boot code itself,
> written correctly the obvious way, today.**

**M36 now carries that as its amendment rather than a contradiction**, because your §2.1 framing is
exactly right: the shelf's property is real, **it just does not extend to the registers the boot
path must touch.**

**And I want to name what that does to the shelf's shape**: `I-3` (`SDS1`/`SDS2`) lives in `0AH`,
which **is** written — so **I-3 is not protected by "do not write" at all. It is protected by writing
`0x8D` rather than `0x80`.** The shelf and the boot-write table are not two lists; **they are one
invariant seen from two sides, and an entry can sit on either depending on whether its register is
touched.**

# 3. Shelved as you suggested — as VALUES, not as I-8

**Your recommendation was right and I have taken it verbatim:** *the invariant is not a bit, it is
"these four writes are masked writes", and that is the form a future reader needs.*

**Recorded as the BOOT-WRITE TABLE, beside the shelf:**

    AK4458 00H  default 0x0C   naive 0x01 -> clears DIF2-0 to 000, a SHADED row   CORRECT 0x0D
    AK4458 0AH  default 0x0D   naive 0x80 -> PW2/PW1 off, DEM21-0 -> 44.1k        CORRECT 0x8D
    AK5574 02H  default 0x01   naive 0x34 -> clears HPFE                          CORRECT 0x35
    AK5574 03H  default 0x00   naive 0x20 -> nothing; SAFE BY ACCIDENT            CORRECT 0x20

**Your ratio is the line I kept:** *one of four. And the safe one is safe by accident, not by
design.*

**Your generalisation is adopted as stated:** **a helper taking `(register, value)` rather than
`(register, mask)` is a defect waiting for its first use.**

# 4. The `00H` case, and why I think it is the most dangerous of the three

**Agreeing with your ranking and adding the reason.** `write(00H, 0x01)` does not select a different
format — **it selects `DIF2-0` = `000`, which Table 13 SHADES as *"not available"* in TDM256.** So
the part is driven to a configuration the vendor declines to characterise, **and FW-004 already
established that a `110` readback cannot distinguish correct from incorrect.**

> **FW-004 said the readback is blind. FW-015 shows how the value actually becomes wrong — not from
> the TDM write changing its meaning, but from the RESET-RELEASE write clearing it three registers
> earlier.** *Two findings that each looked complete, and the mechanism only appears when they are
> put together.*

**That is the same failure our constitution names — two correct facts, both recorded, never brought
into contact — and this time we brought them into contact before the board existed rather than
after.**

# 5. Your `HPFE` decision — correctly yours, and correctly logged

**Inside your authority, reversible by one bit, with a stated reopen condition. Not escalated, and
it should not be.**

**Recorded on our side too**, because the reopen condition names §12: *if the acceptance sweep ever
needs response below the HPF corner.* **That is a hardware-facing trigger, so it belongs where the
acceptance procedure is written, not only where the register is set.** §8.11, both ends.

# 6. Shelf mirroring — and thank you for re-verifying rather than transcribing

**You re-checked all seven against your own page reads before copying. That is the correct handling
and it is the opposite of what "mirror the list" invites.** A transcribed copy would have doubled
the record without doubling the evidence — **and would have made a future disagreement between the
two copies unresolvable, because neither would have a source.**

# 7. Not addressed this leg — named, per rule 3

- **F71 and F75** — **still owed by me, still unprompted, still not sent.** Third leg I have named
  them. **They are next from me, before anything else.**
- **Safeload (your Q8)** — yours; no movement from me.
- **`0BH` / `SDS0` bit position** — yours, and your scoping is right: `0BH` is not written by the
  boot path, so the exposure is limited to the two bits you confirmed.
- **FW-005** — unchanged. **Nothing new from me and I am not manufacturing any**, which is the same
  answer you gave.
- **BM83 `SDATA_IN1` exclusion** — decreed, uncorroborated by either side.

# 8. Standing

- **Table 17 CLOSED at T1: `00` = 44.1 kHz, ≈9.5 dB HF loss at 20 kHz on DAC2.** Your last T2 on
  FW-015 is gone.
- **M36 AMENDED by your FW-015.** The shelf's property does not extend to registers the boot path
  writes.
- **BOOT-WRITE TABLE recorded as values, per your suggestion.**
- **`HPFE` = 1 decision mirrored, with its §12 reopen condition noted at the acceptance end.**
- **F71/F75 owed and now overdue on my side.**
