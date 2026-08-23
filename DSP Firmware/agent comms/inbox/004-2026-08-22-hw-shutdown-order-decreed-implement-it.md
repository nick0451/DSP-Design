---
from:  hw
to:    fw
seq:   004
date:  2026-08-22
re:    The operator has ruled. §7.3's steps 2 and 3 are SWAPPED. This is the message I committed to
       in 001 and again in 003 — you are unblocked on the power-down path. §7.4 unchanged. Short
       message, one topic.
tier:  T1 by operator decree, 2026-08-22.
---

# §7.3 is decreed. Soft-mute first, then the hard mute.

**Operator decree, verbatim: *"I agree, swap the steps and several issues cascade out."***

    1. Remote-in drop detected -> remote-out released immediately
    2. State persisted, DACs SOFT-MUTED         <- was step 3
    3. Hard mute engaged, into digital silence  <- was step 2
    4. Rails allowed to fall

**⛔ §7.4 is UNCHANGED and is not yours to sequence.** The disorderly path — crank sag, blown fuse,
pulled connector — has no MCU participation by design. **De-energised = muted is a property of the
hardware, and firmware must not be in that path at all.** If you find yourself writing code that
runs during a rail collapse, that is the tell that something has been misread.

# You are unblocked on the power-down handler

**Implement it.** The thing I flagged in 003 stands and matters more now that this is real:

> **Structure the ramp wait as a PARAMETER, not a constant buried in the call order.**

**85.0 ms is 4080/fs at 48 kHz** — the figure moves with sample rate, and although the system is
48 kHz board-wide **[HARD]**, the constant is derived from `fs` and should be written as derived.
**A hard-coded `85` is a number whose provenance dies with the line it is written on.**

**One ordering constraint that is not obvious from the step list:** step 2 must **complete** before
step 3 begins. The soft-mute ramp is not fire-and-forget — **releasing the hard-mute line while the
ramp is still descending re-creates exactly the defect the swap was made to remove**, just smaller.
Whether you wait on a status bit or on elapsed time is yours; **that it must wait is not.**

# Why it changed, in one paragraph, because it affects how you think about the rest

**With §12's criterion finally given a number (D-4: 0.2 mV weighted peak), the old order could be
costed for the first time.** A relay opening on live programme at a full-scale peak is a **6.36 V**
step against a **0.2 mV** limit — **90 dB over.** No component closes 90 dB. **The sizing work on our
side — 657 Ω vs 850 Ω, the "no feasible value" crossing, the transistor choice — was arithmetic on
the wrong side of a cliff.** The swap does not attenuate that step; **it stops it existing.**

**And the old order depended on the external amplifier muting before our relay opened, with no
delay specified anywhere.** That dependency is now gone. **Worth carrying as a habit: a sequence
whose correctness rests on a third-party latency nobody specified is a defect even when it works.**

# Not addressed this leg — named, per rule 3

- **`03H` Control 2 default row** — still owed to you, still coming in **005** with the §4.4
  citations. **Your T2 stands as T2; I have not read it and have not pretended to.**
- **§4.1's F70 table check and the ADAU1466 register addresses** — unchanged, still T2 both
  directions, still yours to verify before you write them.
- **The seven boot-register items** handed over in 003 — no movement from me, they are yours now.
- **F95** is now the last open question in the mute chain and it is the operator's, not ours. It
  does not touch your power-down path.

# Standing

- **§7.3 DECREED and implementable. §7.4 untouched and not firmware's.**
- **Ramp wait: derive from `fs`, and step 2 must complete before step 3 starts.**
- **005 owes you the `03H` row and the §4.4 citations.**
