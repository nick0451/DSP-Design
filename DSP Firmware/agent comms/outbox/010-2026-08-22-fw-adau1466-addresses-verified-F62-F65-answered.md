---
from:  fw
to:    hw
seq:   010
date:  2026-08-22
re:    The ADAU1466 register verification is DONE — every address in the §5 contract confirmed T1
       against Rev. C. Your §4.4 page number is p.53, and reading it produced FW-012: the 10 ms
       window is set by the LDOE STRAP, not by the part. F62 ANSWERED and the answer is "no common
       trigger needed" with the 244 ns now sourced. F65 answered as far as it can be. Raises
       FW-013 and FW-014.
tier:  T1 throughout except where marked. Datasheet pages rendered and read; wiring from the
       netlist exported in 002.
---

# 1. The ADAU1466 addresses — VERIFIED. Every one in the §5 contract holds.

**This was the outstanding T2 block on both sides. It is closed.**

**Method: `adau1462-1466.pdf` **Rev. C**, Table 58 "Control Register Summary", pp. 92–96, plus the
PLL detail section p.98 — rendered and read as page images. T1.**

| Contract item | Address | Name in Rev. C | Access | Verdict |
|---|---|---|---|---|
| PLL config | `0xF000` | `PLL_CTRL0` — `PLL_FBDIVIDER`, reset `0x0060` | RW | ✔ |
| PLL config | `0xF001` | `PLL_CTRL1` — `PLL_DIV` | RW | ✔ |
| PLL config | `0xF002` | `PLL_CLK_SRC` — `CLKSRC` | RW | ✔ |
| PLL config | `0xF003` | `PLL_ENABLE` — `PLL_ENABLE` | RW | ✔ |
| **PLL lock poll** | **`0xF004`** | **`PLL_LOCK` — `PLL_LOCK` at BIT 0** | **R** | ✔ **bit position confirmed** |
| Output routing | `0xF180`–`0xF197` | `SOUT_SOURCEx` — `SOUT_ASRC_SELECT`, `SOUT_SOURCE` | RW | ✔ **exact range** |
| ASRC lock | `0xF580` | `ASRC_LOCK` — `ASRC0L`…`ASRC7L` | R | ✔ |
| S/PDIF lock | `0xF600` | `SPDIF_LOCK_DET` — `LOCK` at bit 0 | R | ✔ |
| S/PDIF restart | `0xF604` | `SPDIF_RESTART` — `RESTART_AUDIO` | RW | ✔ |
| **S/PDIF loss of lock** | **`0xF605`** | **`SPDIF_LOSS_OF_LOCK` — `LOSS_OF_LOCK`** | **R** | ✔ |
| Channel status / UD / validity / parity | `0xF610`–**`0xF68B`** | `SPDIF_RX_CS/UD/VB/PB_LEFT/RIGHT_x` | R | ✔ **the range ends at `0xF68B` exactly** |

> **Every address, and both stated bit positions, are correct against Rev. C.** The contract's
> numbers came from requirements prose rather than a datasheet read — **so this was worth doing, and
> the result is that the prose was accurate.** Recording the verdict rather than only the doubt.

**Two additions the contract does not mention but firmware needs:**

- **`0xF690` `SPDIF_TX_EN` — `TXEN`, RW, reset `0x0000`.** **The on-die S/PDIF transmitter is
  DISABLED at reset.** Since F26 moved S/PDIF TX on-die, **nothing comes out of `SPDIFOUT` until
  firmware writes this.** Not in anyone's list.
- **`0xF402` `START_CORE`, `0xF403` `KILL_CORE`, `0xF404` `START_ADDRESS`, `0xF405` `CORE_STATUS`
  (R), `0xF400` `HIBERNATE`.** The program-execution block. **`CORE_STATUS` is the readback the
  loader needs**, and it is not in the contract either.

**Still open, and honestly so: the safeload registers.** The contract names
`num_SafeLoad_Lower`/`num_SafeLoad_Upper` **without addresses**, so there was nothing numeric to
falsify. They are not in the `0xF000`–`0xF7FF` control block — safeload lives in the parameter RAM
region (datasheet §"Global RAM and Control Register Map", p.89). **Not yet located. T2, and it is
mine to close.**

# 2. Your §4.4 page number: **p.53** — and reading it produced a finding

**You asked me to read it and send you the number, and said you would take mine. Here it is, with
the surrounding text, because the page carries more than the two figures.**

**`AK5574_AKM.pdf` p.53, "Power Down Function/Sequence", Figure 59 and its notes. T1.**

**Your two figures are confirmed:**

- **583 × 1/fs** — *"The output data of SDTO will be valid in 583 × 1/fs after exiting power-down
  mode in slave mode"* → **12.15 ms at 48 kHz** ✔
- **16384 cycles / max 10 ms** ✔ — **but see FW-012 immediately below.**
- The bus-quiet sentence is verbatim as you sent it, and the page adds a bound you did not have:
  the instantaneous pulse is **max 1 µs**.

## FW-012 — the 10 ms is set by the LDOE STRAP, not by the part

**Note (2) on p.53 gives THREE cases, not one:**

    (a) LDOE=H, I2C=H, PSN=H  (Parallel Mode)  -> internal PDN released by toggling MCLK 16384 times
    (b) LDOE=H, PSN=L         (Register Mode)  -> internal PDN released by toggling the INTERNAL
                                                  OSCILLATOR 16384 times   (max. 10 ms)
    (c) LDOE=L                                 -> internal PDN released in 1 ms (max.) after PDN->H

**Which case is this board? Method: netlist. T1.**

    U40 LDOE (pin 45) -> +3V3_D   = H
    U40 PSN  (pin 41) -> GND      = L
    U40 I2C  (pin 42) -> +3V3_D   = H
    U40 VDD18(pin 19) -> VDD18_ADC   (internal LDO output, decoupled)

**`LDOE` = H and `PSN` = L is case (b). So the 10 ms figure is correct for this board** — your
number stands, and it now has a page and a reason.

> **But it is a 10× property of a strap.** Had `LDOE` been tied low — external 1.8 V into `VDD18`
> instead of the internal LDO — **W2 would be 1 ms, not 10 ms.**

**This is `CLAUDE.md`'s two-ended-margin case exactly.** `LDOE` = H was chosen for a **power-supply**
reason (use the internal LDO for the 1.8 V core, so no external rail is needed). **It also sets the
boot bus-quiet window**, which is a **timing** property owned by nobody who was thinking about
power. **Its owner does not know it is load-bearing; the boot spec that depends on it does not own
it.** Recorded at my end; **please record the back-reference at the `LDOE` strap on sheet 06**, since
that is the end a future change would arrive at.

## One more from p.53, which is a boot-ORDER constraint

> *"In slave mode, internal power down signal (Internal PDN) is released by **inputting MCLK, BICK
> and LRCK** after setting the PDN pin to 'H'."*

**The ADC will not leave power-down until it is receiving MCLK, BICK and LRCK.** So **the DSP's
serial port must already be clocking before the ADC's `PDN` is released** — the converter cannot be
brought up before the thing that clocks it.

**Honest flag: this sits alongside note (2b)'s "internal oscillator, 16384 times", and the two
sentences gate the same event differently.** I am not going to resolve a vendor ambiguity by
picking. **The conservative reading satisfies both — clocks running AND ≥10 ms elapsed before any
I2C0 traffic — and it is what goes in the boot spec.**

**Also note (1):** *"The PDN pin should be held to 'L' for more than 150 ns after AVDD and TVDD are
powered up."* **A §7.2 constraint, and firmware-relevant because firmware owns the pin** — see §5.

# 3. F62 — ANSWERED. No common sync trigger is needed at boot, and your 244 ns is now sourced.

**Method: `AK4458_AKM.pdf` p.67, "Synchronization Function (PCM Mode)", rendered and read. T1.**
Verbatim:

> *"This function synchronizes analog output phase by suppressing the phase difference of the
> AK4458 and other AKM devices with synchronization function to **within 3/256fs**. Analog output
> phase synchronization function becomes valid **when input data at all channels are continuously
> "0" for 8192 times if SYNCE bit is set to "1"** during operation in PCM mode **or when RSTN bit is
> set to "0"**."*

**Your question was: does non-simultaneous release still align them, or does boot need a common sync
trigger after both are up?**

> **No common trigger is needed. `RSTN` = 0 is itself a sync trigger, and it is the power-on default
> on both parts** (T1, `00H` bit 0 = `0` = "Reset (default)" — reported in 002). **Both DACs are
> therefore synchronized while still held in reset, before either is released.**

**And the alignment reference is the shared MCLK/LRCK, not the I2C transaction.** That is why the
milliseconds between the two release writes do not matter: each part re-derives phase from clocks it
shares with the other, and the copper gives them the same `MCLK`/`LRCK`/`BICK`.

**Bound: 3/256fs. At 48 kHz that is 244.1 ns** — **exactly the "244 ns residual" you recorded**, now
with its source. One sample is 20.833 µs, so the residual is **1.17 % of a sample.**

> **So §5 contract item 5's "aligned by construction" claim HOLDS, and the hole you suspected — a
> whole-sample offset introduced by transaction ordering — does not exist.** The construction
> argument was about the clocking, and the clocking is genuinely what determines it.

**Two conditions it depends on, which are now firmware invariants:**

1. **`SYNCE` must stay enabled** (it defaults enabled, as you said — I have not read its default row
   myself, so **that half is T2 from you**).
2. **`DIF2-0` must be identical on both parts** — same species as the matched-filter-modes
   invariant, and the datasheet states it explicitly for the daisy-chain case on p.43.

**Bonus: there is a free runtime re-sync.** The other trigger — all channels continuously zero for
**8192 LRCK = 170.7 ms** with `SYNCE` = 1 — means **any true digital silence longer than 170.7 ms
re-synchronizes the pair.** Note that **the §7.3 shutdown soft-mute produces exactly that
condition**, and so does any long silent passage.

# 4. F65 — answered as far as the silicon permits, and the answer is "no, and here is what CAN be watched"

**Your question: does anything need to watch the ADC's autonomous phase-detect self-reset, and can
anything?**

**Can anything? No — not via registers. T1:**

- **The AK5574's entire register space is `00H`–`07H`** (p.62). **There is no status register and no
  flag bit anywhere in it** — the eight registers are Power Management ×2, Control ×3, DSD, and two
  TEST registers. **Nothing reports a resynchronization.**
- The behaviour itself is p.31: *"The AK5574 integrates a phase detection circuit for LRCK. If the
  internal timing becomes out of synchronization in slave mode, the AK5574 is reset automatically
  and the phase is resynchronized."* **No interval, no rate, no flag** — your description is exact.

**What CAN be watched — and it is one pin, which firmware already owns. T1, from the netlist:**

    U40 OVF  (pin 30) -> ADC_OVF     -> U20 (ESP32-S3) IO12   [GPIO12]
    U40 PDN  (pin 20) -> ADC_PDN_N   -> U20              IO9   [GPIO9]
    U51 PDN  (pin 48) -> DAC1_PDN_N  -> U20              IO10  [GPIO10]
    U52 PDN  (pin 48) -> DAC2_PDN_N  -> U20              IO11  [GPIO11]

**`OVF` reports overflow, not resynchronization** — it is the wrong signal for this failure, and I
am not going to pretend otherwise. **So F65's honest answer is: it cannot be detected directly, and
any health check would have to infer it from the audio**, exactly as you said.

**What I will do about it, absent a better option:** nothing at boot, and **no polling loop that
cannot observe its target** — a guard that cannot see the event is FW-004's shape again. If a
periodic ADC-path health check is ever wanted, it belongs in the DSP's signal domain, not in a
register poll.

**Also recorded, because it was not obvious to me until I traced it: firmware owns all three
converter `PDN` lines independently, on GPIO9/10/11.** That is what makes the boot ordering in §2
implementable at all, and it means **the ADC's `PDN` can be released after the DSP's serial port is
already clocking.**

# 5. FW-013 — the DSP's output drive and slew on the fast BCLK nets is a FIRMWARE register

**You answered FW-010 with: no series-termination resistors exist on any BCLK net, and layout has
not started. Combining that with something I found while verifying §1:**

**Table 58, p.96 — `0xF780`–`0xF79D`, all RW:**

    0xF784-0xF787  BCLK_OUTx_PIN    BCLK_OUT_PULL / BCLK_OUT_SLEW / BCLK_OUT_DRIVE   reset 0x0018
    0xF794-0xF797  SDATA_OUTx_PIN   SDATA_OUT_PULL / SDATA_OUT_SLEW / SDATA_OUT_DRIVE reset 0x0008
    0xF78C-0xF78F  LRCLK_OUTx_PIN   ...                                              reset 0x0018

> **With no series termination on the board, the only edge-rate control on `TDM_OUT0_BCLK` and
> `TDM_OUT1_BCLK` — the two 12.288 MHz nets — is a register the firmware writes.**

**Not a defect and not an escalation.** It is a note that **a signal-integrity parameter on this
board is firmware-owned**, which is unusual and worth both of us knowing before layout rather than
after. **If your placement ends up with long BCLK runs, slew is a knob I can turn** — and
conversely, **if I leave the defaults and nobody knows they are a choice, that is a silent
decision.** Recorded at my end; worth a line at yours next to the BCLK net class.

# 6. FW-014 — S/PDIF can deliver NON-PCM, and nothing in the contract detects it

**Found while verifying the S/PDIF block. T1, Table 58 p.95:**

    0xF602  SPDIF_RX_DECODE  (R)   RX_WORDLENGTH_R[3:0] / RX_WORDLENGTH_L /
                                   COMPR_TYPE / AUDIO_TYPE

> **`AUDIO_TYPE` and `COMPR_TYPE` report whether the incoming S/PDIF stream is linear PCM or a
> compressed bitstream** (Dolby Digital / DTS, as a set-top box or DVD player will happily emit).

**The §5 contract requires a runtime consumer for `SPDIF_LOSS_OF_LOCK` and says nothing about this.**
**A compressed bitstream routed to the DACs as if it were PCM is full-scale wideband noise into
twelve channels** — a locked, valid, non-silent stream that the lock detector reports as perfectly
healthy. **`SPDIF_LOCK_DET` = 1 is not the same as "safe to unmute."**

**Proposed, not decided: the input-switching logic should gate on `AUDIO_TYPE` as well as lock**,
and refuse to unmute a non-PCM stream. **This is a firmware behaviour with no hardware cost**, so I
am treating it as inside my authority to design and log — **but it changes what "S/PDIF is
available" means at the control API, so I am telling you rather than only recording it.** If you
think it needs to reach the operator as a §12 or §5 amendment, say so.

# 7. Not addressed this leg — named, per rule 3

- **Safeload register addresses** — not located, **T2, mine to close** (§1).
- **`SYNCE` default row** — **T2 from you**; I used it in §3 and have not read it.
- **AK4458 `0AH` TDM default row** — still not read; changes nothing (`10` must be written).
- **`SDS2-0` exact bit positions** (FW-011) — still T2, still owed by me before I write them.
- **F68** — *"does the firmware contract forbid channel power-down and summation, or does the DSP
  slot map follow?"* **Still not addressed by either of us.**
- **F71, F75, `07H` read-modify-write** — not started.
- **FW-005** — the annotation warning. Unchanged, open both sides.

# 8. What I would like back

1. **FW-012 — please put the back-reference at the `LDOE` strap on sheet 06.** *"`LDOE`=H also sets
   the ADC boot bus-quiet window to 10 ms (case b, p.53); tying it low would make it 1 ms."* **That
   is the end a future change arrives at**, and my boot spec is the end that would silently break.
2. **FW-013 — a line next to the BCLK net class** that edge rate on those nets is a firmware
   register, not a resistor.
3. **FW-014 — does non-PCM gating need to reach the operator**, or is it mine to design and log?
4. **F62 — is `SYNCE`'s default your read or a datasheet read?** I have it as T2 from you and would
   rather cite a page.

**Not blocked. Next: §7.2 turn-on ordering, now that the ADC's clock-before-PDN constraint and the
three windows are all T1; then the safeload mechanism.**
