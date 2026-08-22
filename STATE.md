# STATE.md — ODSP-12 · `ODSP12-MB-A` rev A

Working scope, tiered fact base, open unknowns, findings, and the anti-drift ledger.
Governed by `CLAUDE.md` §5. **Read at session start. Update as work happens.**

Tiers: **T1** source of truth (verified) · **T2** highly probable (actionable, tagged) ·
**T3** likely (branchable, check quickly) · **T4** speculation (never drives work).

Last updated: 2026-08-16

---

## 0. Where we are

### ⏱ LIVE STATUS — 2026-08-21. **Rewrite this block, do not append to it.**

**★ ROLE: REVIEW primary, drawing secondary — `CLAUDE.md` §0b.**

**★ `REQUIREMENTS.md` IS NOW v1.8.** Two **[HARD] amendments**, the operator's act, **sent directly
rather than through the review bus** — which is the route §9 requires and the reason the relayed
versions were refused on 2026-08-18. **§4** now fixes the three converter links at **32-bit
MSB-justified, LRCK rising**, with **`SDATA_IN1` (BM83) explicitly excluded**. **§3** replaces
*“low-jitter XO”* with **duty tighter than 45/55 and −20…+70 °C as a base spec; jitter is not a
selection criterion.**

**F70 CLOSED and the decree VERIFIED SELF-CONSISTENT — no copper moves.** AK5574 Table 9 row 26 and
AK4458 Table 13 Mode 12 both give **32-bit MSB, LRCK ↑, BICK 128fs**. The strap set in F69 on the
default-matching argument lands on the decreed value, so **019's guard resolved as intended: it
agreed, nothing moved.** **F56 already closed on SiT1605, which satisfies §3 as amended.**

**Position:** ten sheets · **ERC 68, UP FROM 26, AND THE RISE IS THE GOOD NEWS** · **81 of 536
components now carry a footprint; that number was ZERO this morning** · G0-L untouched.

**★ F109 — THE FOOTPRINT PASS FOUND ITS OWN PREREQUISITE BEFORE DRAWING ANYTHING.** No placed
symbol carried a `Footprint` property: `gen_symbols.py` wrote it into the **library symbol**, the
sheet generators emitted instances with **only Reference and Value**, and the netlist exporter reads
**instances**. **0 of 536 footprints exported.** *Update PCB from Schematic* would have placed
nothing and **G1 parity was not failing — it was unmeasurable.** **Fixed and verified by tool output:
0 → 81.** The **42 new ERC violations name the nine footprints that must now be drawn** — before the
fix ERC could not raise them, so **the 26 was silence, not health.**

**★ THE FOOTPRINT WORK QUEUE IS NOW TOOL-GENERATED, not a list I wrote:**

    12x  ODSP12:TBD_V15                    <- V-15 placeholder, BLOCKED on F100/V-16
    12x  ODSP12:Toshiba_VSON4_11-2D1A      <- TLP3475, unblocked
     6x  ODSP12:AKM_LQFP-48_7x7mm_P0.5mm   <- AK5574 + AK4458   RESPIN SET
     4x  ODSP12:TI_VQFN-HR-14_RJR
     3x  ODSP12:ADI_LFCSP-72_..._EP5.3x5.3 <- ADAU1466          RESPIN SET
     2x  ODSP12:Microchip_BM83SM1_Module   <- vendor verbatim    RESPIN SET
     1x  ODSP12:TI_WSON-12_3x2mm_DSS
     1x  ODSP12:ADI_DFN-12-1EP_3x3mm_P0.45mm_EP_IS_IN
     1x  Oscillator:...SG210_4pin_3.2x2.5mm <- F111, NAME IS WRONG

**Five guards** (F91/F93/F109) built and negative-tested before the first footprint exists; **G5
fires on the live board.**

**★ THE 455 REMAINING ARE NOT DRAWABLE AND THAT IS CORRECT.** R 237 · C 162 · J 22 · TP 13 · L 7 ·
D 6 · Q 4 · SW 2 · F 1 · T 1 — **every one needs a package size, which follows from fab capability,
⬜ UNSET Block E.** They stay empty and now stay **visibly** empty.

**THE NEXT ACTION, one line:** **footprints for the pinned parts** — run every one through
`hw/lib/fp_guards.py`.

**⛔ STILL BLOCKED: the mute shunt cannot be drawn** — **F61 + V-16 must be decided TOGETHER** (F89:
no footprint straddles DN2540 and LND150; F90: the pin count changes 3 → 8 with the answer).

### 🔴 WITH THE OPERATOR

### ⚠⚠ SEVEN DECISIONS ARRIVED **VIA THE BUS**, RELAYED BY THE REVIEWER — 2026-08-18, msg 028

**Recorded as T2-RELAYED, not as T1 by decree, and that is deliberate.** `CLAUDE.md` §5 makes an
operator statement *evidence, not truth*; this one has **an extra hop** and arrived through the one
channel §9 explicitly places outside the authority order. **Two of the seven are [HARD] amendments,
which §9 says review cannot make** — the reviewer is not claiming to; they are relaying. But the
protocol's guard exists for exactly this shape.

**✅✅ THE TWO [HARD] ITEMS ARE NOW SETTLED — SUPERSEDED BY DIRECT DECREE, 2026-08-22.** The
operator issued **§4 (audio interface format)** and **§3 (oscillator duty + temperature)** as
`REQUIREMENTS.md` **v1.8**, **sent directly rather than through review** — which is exactly the route
§9 requires, and the reason the relayed versions were held. **The guard worked and cost nothing: the
relay was never actioned as a decree, and the direct decree arrived four days later saying the same
thing.** **Do not re-ask for these.**

**✅ THE FIRMWARE-CONTRACT AGENT NOW EXISTS** (`DSP Firmware/`, stood up 2026-08-22). **So F62 · F65 ·
F66 · F71 · F75 · `07H` read-modify-write · DFS-boot-only have an owner** — **ours to hand over the
bus, not to escalate.** Channel-2 msg 001 sent; **the boot-register items are queued for 003.**

**→ STILL NEEDED FROM THE OPERATOR: nothing from this table.** The five non-[HARD] rows below were
actioned where harmless and stay marked where load-bearing.

| Item | Relayed decision | Handling |
|---|---|---|
| **F70** | **MSB-justified** — *“no planned revision would benefit from I2S”* | ✅ **Confirms `DIF1-0 = 10`.** No change. Harmless to action |
| **§4 amendment** | **APPROVED** — *“this was just poor documentation on my end”* | ⚠ **[HARD] amendment. Needs direct confirmation before `REQUIREMENTS.md` is touched** — and §4 of our own constitution forbids us editing it to resolve a finding regardless |
| **§3 rewording** | **APPROVED** — name duty + temperature; source an XO tighter than 45/55 % | ⚠ **[HARD] amendment. Same treatment.** The *sourcing* half is actionable now |
| **F73** | **Leave the defaults** — declined added complexity | ✅ No change. The 437.5 µs trade is declined, not overlooked |
| **F58(a)** ✅*verified* | Add the separation criterion, **four-channel figure beside the one-channel test figure** | ✅ Actionable in §12 |
| **F58(b)** | **Not a board requirement — a calibration step.** DSP trim owns channel gain | ✅ Removes it from §12 |
| **F63 / BAV99** | Pin a manufacturer **and justify it**; Diotec was availability-driven and *“weak”* | → Assigned to the reviewer; delivered in 029, see below |

**A FIRMWARE-CONTRACT AGENT is being stood up (relayed: “tomorrow”)** to own boot decisions with the
operator directly. **So F62 · F65 · F66 · F71 · F75 · `07H` read-modify-write · DFS-boot-only get a
home.** Until it exists, **neither we nor the reviewer should be inventing the boot sequence** —
record required writes as findings and let that agent assemble them. *This also resolves the
weakness we named in 021: there is no firmware contract document, and now there will be an owner.*

### Still ours, still open

| # | Decision |
|---|---|
| ~~**Convention 4 clause**~~ | ✅ **DONE 2026-08-20 by operator instruction — but NOT as an amendment, because THE THING TO BE AMENDED DOES NOT EXIST.** Installed instead as **`CLAUDE.md` §8 rule 11**, a new rule anchored to **M7** (which is real). **See F86 — both citations in the proposal were phantom and I had propagated one into THIS FILE.** The substance survives on its own evidence (`R_IN`, the INA1650 500 kΩ); the provenance did not |
| **F88** | **`REQUIREMENTS.md` carries the stale TVS package too, and §4 forbids us fixing it.** §12's load-dump caveat reads *“the **DO-218AB** land is 15.30 × 10.70 mm … shrinking that pad at layout makes this criterion false — it is an electrical input, not an outline”*, plus the F42 change-log row. **The pinned `SM8S24AHM3` is DO-218AC** (T1-91). **Nothing physical is wrong** — the land is identical — **but that sentence is what tells a layout engineer the pad is a rating, and it names the wrong package while doing it** |
| **Bus numbering** | **First finding-number collision in 48 messages** — we both allocated **F86** in the same hour. Theirs renumbered to F87 because the register lives here. **The protocol has no rule.** Proposed for your call: *findings allocated by the design side*, or *the reviewer prefixes its own (`R-12`) until adopted* |
| **Block E** | **Two back-references the new §8.11 now requires, both from the reviewer:** Block E registers the SM8S pad size but **carries no mount-temperature requirement**, while V-29's load-dump survival is computed against one (its 8 W benchmark is *“on infinite heatsink at 25 °C”*). Same for **R<sub>ΘJA</sub>'s “2 oz.” condition against an UNSET copper weight** |
| **F39** *(reopened by F84)* | **Its recorded reason does not reach the op-amps.** The SEPIC topology orders **±15V5**; the op-amps run on **±13V5**, behind an LT3045 and an LT3094 — dissimilar parts, independent dropout. **Two things needed and neither is ours:** the recorded reason replaced, and the ±13V5 propagation step given an argument. **Not inducible** — the argument is all there will ever be |
| **F77** *(rule offered)* | The reviewer proposes deciding it as a **boundary, not a diode**: *“qualification follows **bounded fault energy**, not proximity to the connector — a part that can see unbounded harness energy is input protection; a part behind an element that bounds the fault current to a computed value is signal path.”* **On that line the clamps are signal path**, since F49 already computed the injected current at **31.2 mA**. Not adopted — it is a scope reading of a decree, so it is yours |
| **F77** | **§7.0 names *input protection* as one of four places AEC-Q100 IS required.** The BAV99/BAV199 clamps **are** input protection. **Scope question:** does that mean the TVS + series R at the connector, or does it reach the **rail clamps behind the 1 kΩ**? Decides whether `BAV199-Q`'s qualification is *required* or a *bonus* — and applies to every part on the input side |
| **Respin set** | **`CLAUDE.md` §7's “five the operator personally eyeballs” was stale twice (F92).** Corrected for fact to **four** — ADAU1466 **LFCSP** · AK5574 · AK4458 · BM83SM1 keepout. **What the fifth should be is yours**, since which footprints get eyeballed is a decree. *SM8S suggested — its land has a stated electrical consequence (§12/G3) — but not decided* |
| **AK4458 exposed pad** | **A defaulted choice worth 20 °C (F93).** Grounded = −40…+105 °C; open = −40…+85 °C. **Both clear the −20…+70 decree** (by 35 and 15 °C), so nothing is broken — **but no one has chosen.** *Grounding is obviously better, and “obviously better” is how a default gets installed as a decision without anyone deciding.* **No guard can hold this**: the constraint is that the net choice and the temperature rating agree, and they live in different documents |
| **⛔ F108 — §6.4 ASSERTS TWO MECHANISMS AND ONE HAS AN UNSTATED LATENCY** | *(Re-sized after the reviewer caught a safe-direction error and after re-reading §6.4 — the earlier ‘arrives too late to do anything’ over-claimed.)* **Hold-up, model v3: ±13V5_A survives 3.96–16.87 ms** (32 µF upstream through 1.74 V of headroom, then **both caps in parallel** once the LT3045's pass element is in dropout at ~0.52 Ω). **Margin 2–19× — and now a MEASUREMENT, `BRINGUP.md` 4b.7, because the number has been corrected twice in the same direction (M31).** The shunt's bias decays with **τ = 50 ms**, so it **begins conducting at 33–75 ms** — **4–42× after the rails are gone**, while the series relay opens in **≤ 0.4 ms**. **§6.4 explicitly assigns the shunt to this case:** *“Failure behaviour is the product of two independent mechanisms. Rails collapse → LED dies → series opens. **Independently, the −13V5-derived bias dies → shunt closes.**”* **So during the collapse window the ‘two independent mechanisms’ are ONE.** *§6.4 also gives the shunt a STEADY-STATE job (killing `C_off` leakage), which the latency does not touch — the finding bites only on the collapse-window claim.* **The question: does the two-mechanism assertion stand, given that one of them has a latency nowhere stated?** |
| **⛔⛔ STOP-THE-LINE — READ BEFORE DECREEING F61** | **The “no feasible value” in my last escalation is a property of OPTION C, not of the board.** The ~850 Ω THD floor exists **only because a resistor is permanent**; a switched FET is off in normal operation, so **no drive penalty, no THD floor, no crossing.** **And V-16 is not mooted by option C — it decides it:** **DN2540 25 Ω max → 0.40 mV, passes §12 by 27.9 dB** (47 Ω hot → 0.76 mV, +22.4 dB); **LND150 1 kΩ max → 14.73 mV, FAILS by 3.4 dB.** *Option C's real gains still stand — it deletes the bias network and deletes a NONLINEAR element (the `C_off` §12's CCIF criterion exists to catch).* **But §6.4's own “100–500 Ω is ample” is what sent everyone hunting in the hundreds — the DN2540 is 25 Ω, an order of magnitude better than the decree's illustrative range** |
| **F105 — ONE LINE SETTLES IT FOR THE WHOLE BOARD** | **Is §7.0's +70 °C the EXTERNAL environment or the INTERNAL ambient at the part?** §7.0 does not say — searched, and it contains no statement of ambient/external/internal/enclosure beyond the range itself. **A sealed enclosure runs hotter inside than out, so EVERY hot-end margin on this board is measured against whichever one it means** — the TLP3475's 15 °C (F103), the SM8S mount temperature, the AK4458 exposed-pad 20 °C, the DN2540's 1.1 %/°C. *Effectively a §0 UNSET: a value nothing may depend on, that a great deal already does.* **Raised once rather than twelve times** |
| **F103 — ASK THIS ONE FIRST, IT NEEDS NO INTERPRETATION** | **The TLP3475's RECOMMENDED operating range is −20…+85 °C; its ABSOLUTE MAXIMUM is −40…+110.** §7's note: recommended is what is *“necessary to obtain the intended performance”*. **Against §7.0's decreed −20…+70: the cold end MEETS EXACTLY, ZERO MARGIN; the hot end has 15 °C.** *Not a failure — a zero-margin finding, F55's shape at the other end of the scale.* **And every figure we use (`C_OFF` 20 pF, `R_ON` 1.5 Ω, `t_OFF` 400 µs) is at `T_a` = 25 °C, so there is no characterised behaviour AT the floor.** Twelve parts. **The question: is that acceptable in the signal path?** |
| **⚠⚠⚠ THREE ITEMS — THE ORDER IS NOW LOAD-BEARING** | **F97 FIRST, and it IS the sizing.** §12's *“scope-verified < 10 mV transient”* omits **bandwidth, peak-vs-RMS, and source condition** — and the source condition **alone** moves the answer from *“shunt ≤ 657 Ω”* to *“≤ 16 kΩ”* to *“no shunt needed at all”*. **A criterion whose answer ranges from ‘delete the part’ to ‘no feasible part exists’ is not a criterion.** ⚠ **Justify each of the three words from AUDIBILITY and write them down BEFORE any value is on the table** — the edit is being drafted by people who now know which values pass under which reading, and **a criterion edited after seeing which value passes is not a criterion.** → **F99 SECOND — does §7.3's step order stand?** Hard mute at step 2, DAC soft-mute at step 3. **Soft-mute first in the ORDERLY path and the relay opens into silence, Event A vanishes, and no resistor is needed at all.** §7.4's order is right for a collapsing rail, so this is a **branch in a [HARD] sequence** — F20/F30/F34 territory. → **F98 LAST — size only if a part is still needed.** Under the worst-case reading **pop ≤ 657 Ω and THD ≥ ~850 Ω CROSS: no feasible value.** *My earlier “~1 kΩ, two axes meet” is WITHDRAWN* |
| **⚠⚠ F95 — DECIDE THIS BEFORE THE SIZING** | **No mute-depth acceptance figure exists in dB.** §12 has a **noise floor** (−105 dBV muted) and a **transient proxy** (< 10 mV); §7.4 says **V-16 must model the stack** and **V-16 is open**. **And §7.4 reframes the question:** the mute *“only has to suppress the **dying DAC** … usually well under −20 dBFS”* during power-down — **so it is a TRANSIENT requirement, and every number we traded prices STEADY-STATE full-scale feedthrough.** Against the 10 mV proxy: a −20 dBFS dying source needs **−33.2 dB**, so **10 kΩ (−38.1) already clears with 5 dB spare and 500 Ω is ~25 dB of overkill**. *Full scale would need −53.2 dB — but §7.4 says that is not the case.* **The decision is WHICH QUESTION THE MUTE ANSWERS; the resistor value is downstream of it** |
| **⚠ F94 — CORRECTION: I GAVE YOU A WRONG NUMBER FIRST** | **My *“option C costs ~20 dB”* was an artefact of costing the reviewer's `[mine, arguable]` 10 kΩ sizing as though it were option C's definition.** **Corrected: the shunt sits on `MUTED`, before the 10 Ω build-out, so its source impedance is `R_ON` = 1.5 Ω.** **At 500 Ω — §6.4's own figure — option C matches the FET's mute depth (**−58.4 dB**) for **0.026 dB** of output level, stays **+0.106 dB above the §6.2 [HARD] floor**, and draws **13.5 mA peak against the OPA1656's 100 mA (7.4× inside)**. **So the real cost of option C is the one §6.4 already states — losing the second independent fail-safe mechanism.** **§6.4's two-independent-mechanism language is in THREE places**, so the amendment is larger than a part swap. **One axis unverified: THD into a permanent 476 Ω vs the 10 kΩ §12 specifies** |
| **F61 + V-16 TOGETHER** | **These now land on the SAME milestone and neither can be deferred past the footprint pass (F89).** **F61 decides HOW MANY** (24 singles vs a dual vs revisit) · **V-16 decides WHICH** (DN2540 vs LND150) — and **F89 shows the two parts are NOT pin-compatible in either shared package**, so no footprint can straddle them. **Plus F90: if singles win, each pair puts a drain TAB at the muted output node**, and `MUTE_DEPFET` needs **8 pins, not 3** |
| **F61** | Mute shunt: **24 singles**, a dual depletion FET in one package, or revisit DN2540. §6.4 [HARD] wants a **pair**; LND150 is a **single**, so honest BOM = **24 FETs, not 12** — and `07/08_dac` need restructuring for (a). **Stopped before the restructure per stop-before-a-block** |
| **F63** | **Reviewer recommends `BAV99-AQ` (Diotec), AEC-Q101 *qualified*.** The real finding is that **the pinned part has no suffix at all** — industrial grade on an automotive board. **The conflict: the low-leakage `BAV199` is not offered in the qualified suffix**, so qualified-and-low-leakage needs a different vendor (a datasheet request, not a read) |
| **F60 / V-15** | LND150 has **no numbered pin table**; DN2540 does, but is Supertex-vintage vs Microchip — **pin ordering does not transfer by assumption**. Becomes **irreversible at LAYOUT, not purchase** |
| **F68** | `ODP` and five siblings inert — **annotations fixed**; the open half is whether firmware may ever power down a channel or enable summation (Optimal re-packs; §4 [HARD] does not) |

**Datasheets still wanted:** XO tighter than 45/55 % over −20…+70 °C · range-switch relay · remote-out
P-FET · *(new)* a **qualified low-leakage BAV99-class** part from Nexperia/onsemi/Vishay, if the
F63 conflict is to be resolved rather than accepted.

| # | Decision |
|---|---|
| **F58(a)** | §12 channel-separation criterion. Proposed ≥ 70 dB @ 1 kHz one-channel-driven **with the four-coherent figure recorded beside it** (−85.7 vs −73.7 dB) |
| **F58(b)** | Inter-channel gain matching: a **board** criterion or a **calibration** one? Per C4 it is trimmable in the DSP, so it may not belong in §12 at all |
| **F62** *(reframed)* | **`SYNCE` DEFAULTS TO ENABLED** — the item is *do not disable it, and give it a valid trigger*. **Real question:** both DACs arm at power-up (`RSTN`=0) but are released by **two I2C transactions ms apart** with LRCK running. **Does non-simultaneous release still align them, or does boot need a common sync trigger after both are up?** |
| **F73** | **A GROUP-DELAY DECISION WITH A PRICE, not a family mismatch.** Both default to *Sharp roll-off*; they differ only on delay — ADC **Normal**, DAC **Short**. **Matching the DAC to the ADC costs 437.5 µs of added output latency** (558.3 vs 120.8 µs), against a BT path already carrying A/V-sync exposure. The ADC's own `SD`/`SLOW` is the other half and is decided in the same breath. *First live case where M25's precondition fails* |
| **F72** | **BM83 link is excluded TWICE** — `16-Bit/24-Bit I2S` only, so neither §4's 32-bit nor F70's justification applies. Its matched pair lives in **Config Tool binary + SigmaStudio**, different artefacts and a different owner |
| **F68** | `ODP` is **inert in I2C mode** — the part runs Optimal Data Placement whatever the strap says. **Does the firmware contract forbid channel power-down and summation, or does the DSP slot map follow?** Optimal re-packs; §4 [HARD] does not |
| **F62** | `SYNCE` in the boot sequence — the RSTN path. Plus the 244 ns residual as a product property |
| **F66** | **Boot sequence must write `02H CKS3-0 = 0110` then a channel reset.** The ADC powers up at 128fs/Quad Speed/108–216 kHz against our 512fs/48 kHz, **every PDN cycle** (Note 26), and in I2C mode there are **no CKS pins to strap** |
| **F65** | AK5574's LRCK phase-detect **self-resets autonomously** in slave mode — unbounded, unobservable, no status bit. Does anything need to watch for it? |
| **C1** | **Third route found by adversary 014 and I think it closes the item — close it by making the number irrelevant, the V-26/DITHOFF move.** FS margin is **3.9 %**; worst excursion from the 25 °C test condition over a −20…+70 °C decree is **45 °C**. → **breakeven tempco = 867 ppm/°C** (recomputed here). The FS stack survives unless full scale drifts faster than that. Their T2 judgement, *explicitly not from a datasheet*: the temperature-dependent term in `0.56 × (VREFH − VREFL)` is the **0.56**, a switched-cap **ratio**, and like-capacitor ratios on one die run single-digit to tens of ppm/°C — **17–87× inside**. **Put 867 ppm/°C on the sheet, not the opinion of it**: if the operator disagrees with the tempco judgement the inequality still stands and only its conclusion moves. **ONE ADDITION OF OURS:** that argument covers **AKM's** term only. **`VREFH − VREFL` is a BOARD-supplied voltage and its tempco is OURS**, not in C1's scope and not covered by the ratio argument — a separate, smaller, and *tractable* item |
| **F56** | **The escalation is a REWORDING, not a relaxation — reframed by adversary 010 and they are right.** §3 **[HARD]** says *low-jitter XO*. **Jitter clears by 140×**; what actually binds is **duty (45–55 % at the converters, which no held candidate meets with the buffer in between)** and **temperature range (−20 °C vs ASDMB's 0 °C default order code)**. **A [HARD] naming the wrong parameter is satisfiable by a part that FAILS the real requirement** — someone buys a 50 fs oscillator specified 40/60 % at 0–70 °C and has honoured the decree exactly. So the ask is *“this [HARD] names jitter and should name duty and temperature range”*, which is an **amendment with history preserved**, not an economy taken quietly. Still needs an XO tighter than 45/55 % |
| **F63** | BAV99 manufacturer must be pinned on the BOM (`bav99.pdf` is Diotec; cloned PN) |
| **V-10** | AKM vs TI converters |

**DATASHEETS WANTED — ranked, 2026-08-17.** *The operator gathers these on request and asks to be
bugged — never build a workaround around a missing document.*

| # | Part | Blocks | Why this one, specifically |
|---|---|---|---|
| **1** | **24.576 MHz XO, duty specified tighter than 45/55 %** over **−20…+70 °C** | **F56** | Both held candidates sit *exactly* on the AK5574's 45–55 % limit with **nothing allocated to the LMK buffer** — ASDMB *45/55 @ ½ Vdd*, CCHD-575 *45/55 % Max @ 50 % Vdd* (both text-read 2026-08-17). A compliant 45 % part arrives at the converter **below** its minimum. ±2 % parts exist. Jitter does **not** discriminate (7.09 ps budget); **duty and temperature range do** |
| **2** | **Range-switch relay** | K1–K4 on `06_analog_in` | Drawn on the **stock `Relay:FINDER-30.22` symbol** with the value string *"2-pole signal relay, 5 V coil"* — a placeholder that is not even the right relay class. Needs: **coil current** (→ +5V_D budget §7.1 and the ULN2003A sink), **2 × Form A**, contact material/rating at ±42 V signal, and a footprint |
| **3** | **Remote-out P-FET (Q91)** + its NPN (Q90) | `08_io` | Value string is literally **`60V P-FET`**. Faces **VBATT_PROT** → §7.0 wants **AEC-Q101**. Needs V_DS above the TVS clamp, V_GS abs max vs the 15 V D90 zener, R_DS(on) at the remote load |
| **4** | **F38 power discretes:** SEPIC switch **Q1** *(`80V N-FET`)*, **D1** *(`60V 3A Schottky`)*, reverse-polarity **Q2** *(`60V P-FET`)*, and the SEPIC **coupled inductor** | `04_power` | Same shape as #3 — generic value strings on stock symbols, all **battery-facing**, so all AEC-Q101. Not blocking capture; **blocking BOM freeze and footprints** |
| **5** | **Dual depletion FET in one package** — *only if F61 goes that way* | F61 / V-15 | §6.4 **[HARD]** wants a back-to-back **pair**; LND150 is a single, so the alternative is 24 singles. **Ask only after F61 is decided** — see the F60 update, DN2540 may already answer both |
| **6** | **SM8S24CAHM3** (bidirectional TVS) | F45 | *Optional improvement, not a blocker.* Doc 98647 is the unidirectional series only; a CA series would live under a different doc number — **unverified, not disproven** |
| **7** | **PNP pass transistor** | F18 | **Conditional** — needed only if the ADAU1466 goes the internal-regulator route |

**NOT wanted, and worth stating so they are not re-fetched:** **OPA2320** and **OPA2365** are both
**held** — F52 needs a *figure read of a held document*, not a document. **DN2540** is held and
carries the numbered pin tables LND150 lacks (F60). **TLP3475**, **tmp461**, **LT3094**, **usblc6-2**
and **SM8S_AHM3** are all in `datasheets/`.

### 📮 BUS LEDGER — **TWO CHANNELS NOW.** Check this before writing to either.

**⚠ Two counterparties, two independent sequences. Do not cross them.**

#### Channel 1 — adversary review (`CLAUDE.md` §9)

Path in `CLAUDE.md` §9. **One shared sequence across both folders.**

| Sent by us (`inbox/`) | Received (`outbox/`) |
|---|---|
| 002 … 086, **088** | 001 … 085, **087** |

**✅ NOTHING OWED.** 090 and 092 sent 2026-08-22. **F108 CLOSED BOTH SIDES.** 091 corrected my 47 µF
availability argument — wrong current *and* wrong test; conclusion unchanged. **M32 logged.**

#### Channel 2 — FIRMWARE AGENT (opened 2026-08-22 by operator instruction)

**Path: `DSP Firmware/agent comms/`.** `inbox/` = **we write** · `outbox/` = **we read**.

**🔔 WATCH ARMED 2026-08-22 on `outbox/`** (15 s poll, persistent, task `bpaezst3f`) —
alongside the channel-1 watch on the adversary `outbox/`. **BOTH ARE SESSION-SCOPED: re-arm them at
session start.** §10 makes the repo the memory, but a monitor lives only in the session, and **an
unread message is indistinguishable from no message.**
**Separate shared sequence, starting at 001. Unrelated to channel 1's 092.**

| Sent by us (`inbox/`) | Received (`outbox/`) |
|---|---|
| **001** | — |

**⛔ `DSP Firmware/STATE.md` IS NOT OURS.** Operator decree 2026-08-22: that ledger belongs to the
firmware agent. **We do not write it.** Reading it to avoid duplicating their work is fine; editing
it is not. **Equally, they may not read ours** — which is why their Q1 (the I2C0 address table) had
to arrive over the bus, and why anything else they need from §9 must too.

**001 sent 2026-08-22** — defined the channel protocol (their Q4), answered **Q1** with the full
I2C0 map and its method, and **declined Q2/Q3 as ⬜ UNSET and the operator's to state.**

**⚠ OWED TO THEM, and promised in writing:** *"I will send you a message the moment F97 and F99
resolve."* **They are holding §7.3 power-down sequencing unimplemented on my say-so.** Under bus
rule 3 they cannot distinguish *still open* from *resolved and he forgot* — **so this is a debt, not
a courtesy.**

**Told them, so it is not re-derived:** v1.8's §4 amendment is a firmware register write; **T1-132**
— the AK5574 in serial control mode ignores every strap pin but `MSN`, so the [HARD] audio format
exists **only** as a firmware register write; **T1-130** — AK4458 boots `RSTN`=0 and `TDM1-0`=Normal
against §4; **T1-55** — the ADC's wake-up blocks the **whole I2C0 bus** for ~10 ms, not just itself.

**⚠ `DSP Firmware/` is UNTRACKED in git** (`git status` → `?? "DSP Firmware/"`). Not ours to commit;
flagged to the operator because an untracked folder is one `git clean` from gone.
*When the failure mode is omission from a sum of positive terms, same-direction is FORCED and carries
no information.* **Closure is ENUMERATION** — which I then ran: **`VBATT_PROT` holds 10 + 22 = 32 µF,
not the 220–1000 µF their bounding table assumed, so their predicted term 4 adds 0.2–1.6 ms and
F108 v3 STANDS — by a complete count rather than a fourth model.** 4b.7 gains **ch3 = `VBATT_PROT`**.
*Earlier:* 086 · 084 · 082 · 080 · 078 · 076 · 074 · 072 · 070 · 068 · 066 · 064 · 062 · 058 · 056 · 054 · 052 · 050 · 048 · 046 · 043 · 041 · 039 · 037 · 035 · 032 · 030 · 027 · 025 · 023 · 021 · 019 · 017 · 015 · 013 · 011 · 009., covering 007 and 008 together, with the rule-3
unaddressed list named explicitly (C1-narrowed, F58a/b, the AK5574 SYNCE counterpart, `PLLFILT`,
BAV99, and the F53 A3 sweep — flagged to them because sheets they have already read may have been
**clipped on export**).

**We asked them for 010:** *(1)* OPA2320 **C_L-vs-phase-margin at 100 pF** with the 10 Ω isolation
credited, *(2)* OPA2365 **noise density at 1 kHz** plus its **charge-pump switching spec**. We said
we would read (1) **independently as well** — two figure reads of one curve, where a *disagreement*
is itself the finding. **(2) is the more decision-relevant**, because T1-118's ranking rests on a
two-point *fit* with an 11 % margin, and a measured 1 kHz density either promotes it or breaks it.

**Protocol note raised in 009:** their ADAU1466 citation is *Table 6, p.9*, ours is *Rev. C, p.29* —
**numbers agree exactly**, so it is a **revision difference, not a conflict.** Cite revision with
page from here.

### 🧠 CONTEXT DISCIPLINE — this project is designed to be compacted, repeatedly

**Everything load-bearing is in files. Context is scratch space; drop it freely.**

1. **Never read a whole generator.** `grep -n` for an anchor line, then edit **by line index**.
   The note strings hold a literal `
`, so string-matching them from a heredoc fails on escaping —
   use `chr(92)` or line indices. This cost several rounds before it was written down.
2. **Generators print their own load-bearing numbers.** Run one and read stdout rather than
   re-deriving (**M22** — prose numbers get read back from the module, never recalled).
3. **Datasheets: locate with `pdftotext`, confirm with `pdftoppm` render.** Never promote a
   load-bearing number on an extraction (**M2**), and state which of values / structure / conditions /
   citation the read covered (**M20**).
4. **Verification is three commands**, not a re-read: ERC count · netlist walk · M17 refdes audit.
5. **A finding is not done until it is in §7.** If it only exists in a chat reply, it is lost.

### RESUME HERE — read order after a context compaction

Everything needed is **in the repo**; nothing load-bearing lives only in conversation.

| # | File | What it gives you |
|---|---|---|
| 1 | `CLAUDE.md` | The constitution. §0 UNSET, §4 channel policy, §5 tiers, §8 working rules, **§10 compaction contract** |
| 2 | **`STATE.md` §0** (here) | Position, next action, session boundary |
| 3 | `STATE.md` §5 | **The ledger. Read M1–M31a before any datasheet or file work. M19 governs review-agent findings** |
| 4 | `REQUIREMENTS.md` **v1.7** | The authority. Cite by section **and** version |
| 5 | `hw/README.md` | Tool paths, build/verify commands, KiCad-10 format traps |
| 6 | `STATE.md` §7 / §8 / §9 | Findings (F1–F63), [VERIFY] (V-01…V-30), I2C bus map |
| 7 | `BRINGUP.md` | Bench checklist — **§0 is receiving inspection**, §4 is capture-session additions |
| 8 | `DATASHEETS.md` | 27 documents held in `datasheets/` (untracked); this is the register |

**Git is the memory of record.** Commit messages carry the *reasoning*; `git log` is a usable
narrative of why things are as they are.

**THE FIVE HABITS that account for almost everything this session caught.** Every one of them
found a real defect in committed work:

1. **Render the datasheet page; never trust extracted text.** Figure-level reads produced T1-71
   (the PSRR notch), T1-103 (AKM's bias divider) and every pin map. Text extraction produced
   three *wrong* T1 facts earlier in the project.
2. **Verify the artefact, not the receipt.** ERC on an empty sheet is clean; a 200 response can
   be the wrong PDF; `file` said 10 pages where `pdfinfo` said 51. **Check the netlist.**
   **F53 is this habit's own failure and the sharpest example of it:** *"PDF export renders 10
   pages"* was recorded as proof, and a page **count** was read as a content check. The export had
   been clipping every sheet's notes for four sessions. **A count is a receipt. Open the page.**
3. **Run the recorded constraints against the artefact.** The `RT` error, the ILIM error and the
   4.479 V<sub>rms</sub> gain miss were all caught by a *consequence* contradicting a written
   requirement — never by re-deriving anything.
4. **Criteria before the block.** The operator publishes acceptance criteria *before* the work
   starts. Three times this session they caught committed or staged work (F40's ILIM, F41's
   collision, F48's abs-max). It works because the criteria arrive before the momentum does.
5. **Stop before a block, never partway through.** Used three times, correctly each time.

**A REVIEW AGENT IS IN THE LOOP as of 2026-08-16.** Its findings are **T2 on arrival** and are
validated against the artefact before they are accepted *or* dismissed — **M19**, read it before
answering one. It may request context and will reason from what it has; where it has less than the
repo does, its assumptions are the first thing to check, not its conclusion.

**Closing rituals — run BOTH at every sheet close:**
- **M6a:** one end-to-end walk of every control/I2C net, driver to receiver. *Coverage assertions
  see omission; only a trace sees misassignment.* (Caught the PCF8574 SDA/INT swap.)
- **M17:** hierarchy-wide refdes audit. *Generated sheets bypass the annotator.* (Caught `Q1`
  being both the SEPIC FET and a mute shunt — which would have detonated at assembly.)

**Phase:** **Capture begun** (2026-08-15). Architecture specified at `REQUIREMENTS.md` v0.7,
governance closed, tooling verified. Mechanical and fabrication still unspecified — layout remains
blocked, capture does not.

**Board state:** KiCad project `hw/ODSP12-MB.kicad_pro` exists with a **10-page hierarchy**
(index + 9 sheets), all empty of components. **ERC: 0 violations.** PDF export renders 10 pages,
which is the proof KiCad *traverses* the hierarchy rather than merely parsing the root. Nothing
placed, nothing routed.

**`03_control.kicad_sch` is drawn** (page 4, 2026-08-16). 28 devices — ESP32-S3-WROOM-1-N8R2,
USB-C receptacle, USBLC6-2SC6 ESD array, reset/boot switches, status LED, and the strapping,
bulk, divider and pull-up networks. **100 global labels, no collisions** (the F41 guard ran).
**Cross-sheet integration is live**: `I2C0_SDA/SCL` now joins the ESP to the ADS1015 and TMP461,
and `PG_5V_D`/`PG_6V2_A`/`PG_1V2` join the bucks' open-drain PGOOD pins to their sense GPIOs.
**ERC 78 → 77**, and `pin_not_driven` fell 15 → 11 as the controller terminated four nets.

**`04_bluetooth.kicad_sch` is drawn** (page 5, 2026-08-16). 10 devices, all 50 module pins
dispositioned across two units. **Cross-sheet integration verified in the netlist against the
[HARD] §4 map**: `TDM_IN1_BCLK/LRCLK/DATA` join DSP pins 60/61/62 to module pins 3/2/4.
**ERC 77 → 70.**

**Drawing it found two of my own wiring errors and one gap in 03_control** — the ESP was on the
*module* side of both series resistors (so the domain-crossing protection was bypassed), and
BM83 reset reached no GPIO at all. Both fixed; IO47/IO48 took the two new nets once T1-102
showed footnote c does not apply to the N8R2.

**`06_analog_in.kicad_sch` is drawn** (page 7, 2026-08-16). **66 device instances, 232 labels, no
collisions.** 4 differential channels → 2× INA1650 → AK5574, with dual-range attenuators, 2-pole
range relays, a PCF8574 expander and a ULN2003A coil driver. **ERC 70 → 81**, all of it new
undrawn-counterpart labels. `+3V3_A` is gone from the netlist (F46).

**The gain plan caught two errors that a parts-list approach would have shipped:**
- **The INA1650's 500 kΩ input resistors are *part of* the divider, not a load on it.** The first
  pass ignored them and put **speaker mode at 100.9 % of full scale — clipping at the stated
  ceiling.** R<sub>top</sub> dropped 100 k → 10 k (loading 20 % → 2 %, and the CMRR budget
  improves in the same move) and both ranges now target 95 % FS. Final: **line 95.3 %, speaker
  94.0 %, Z<sub>in,diff</sub> = 38 kΩ** against the ≥ 20 kΩ decree.
- **The PCF8574's `SDA` and `INT` were swapped, and the F28 assertion passed anyway.** Coverage
  proves every pin has a net, never that it is the *right* net — **M6, stated before it was
  checked and then demonstrated within the hour.** Caught by reading the parent symbol's map.

**Two more of the extends-alias family** (PCF8574T, ULN2003A) — fifth and sixth instances, now
handled **generically** in `extract()` rather than per part, and both built as project symbols
because the rename otherwise produces a `lib_symbol_mismatch`. **`VDD18` was typed `power_in`**
on the AK5574 while T1 already recorded it as an internal-LDO *output*; retyped `power_out`,
which is what cleared the last `power_pin_not_driven`.

**ALL TEN SHEETS ARE DRAWN** (2026-08-16). `05_spdif` and `09_io` closed the set; **ERC is 41 and
the number is now ABSOLUTE** — no violation is waiting on an undrawn counterpart. It is a punch
list:

| Class | n | What it actually is |
|---|---|---|
| `isolated_pin_label` | 28 | **Real gaps + genuine spares.** Gaps: `U13_COMP` (the SEPIC's compensation network is not drawn), the four `MON_*` rail-monitor dividers (§9 requires them), `MCLK_DSP`/`MCLK_ADC`/`CLKOUT_DSP` (**the 24.576 MHz XO and the LMK1C1104 fanout are not placed**). Spares by design: the four unused TDM ports, `U6/U8/U9_PG` (PG disabled by the PGFB→OUT disposition — should become no-connects), `TP_SPDIF_TX`, `TEMP_THERM_N` |
| `pin_not_driven` | 13 | The same gaps seen from the pin side: ADS1015 `AIN0-3`, DSP `XTALIN/MCLK`, both converters' `MCLK`. Plus `AIN{n}_N` on the ADC — **the INA1650 is single-ended-out, so the ADC's N inputs need a reference, which is not yet drawn** |

**The biggest single omission is the clock tree**: §3's [HARD] XO → fanout → converters exists as
net names on `02_dsp` and as nothing else. That is the next block, and it is the one place where
the [HARD] section with the most consequences has the least copper.

**Sheet plan** — mirrors the architecture, not the BOM, so that a [HARD] section maps to one sheet:

| Page | File | Contents |
|---|---|---|
| 1 | `ODSP12-MB.kicad_sch` | Index |
| 2 | `01_power.kicad_sch` | §7 rails, sequencing, monitor. **9 rails incl. +6V2_A and +3V3_CLK** |
| 3 | `02_dsp.kicad_sch` | ADAU1466, XO, MCLK fanout, PLL — the [HARD] §3 tree in one place |
| 4 | `03_control.kicad_sch` | ESP32-S3, USB-C, I2C0, GPIO |
| 5 | `04_bluetooth.kicad_sch` | BM83SM1 |
| 6 | `05_spdif.kicad_sch` | AK4118A, transformer-coupled coax, WM8804 DNP |
| 7 | `06_analog_in.kicad_sch` | 4× front end → AK5574 |
| 8 | `07_dac_a.kicad_sch` | AK4458 #1 + AOUT1-6 |
| 9 | `08_dac_b.kicad_sch` | AK4458 #2 + AOUT7-12 |
| 10 | `09_io.kicad_sch` | RCA field, power connector, test headers |

The 6+6 output split gets **two sheets rather than one instantiated twice** — §10's [HARD]
no-remapping rule wants the channel numbers written literally, not derived from an instance path.

**Tool-verified format facts:** native schematic version is **20260306** (from `sch upgrade`, not
memory — DL-13). Sheet UUIDs are `uuid5` from a fixed namespace, so regeneration is stable rather
than randomised.

**Gate status:** G0-S **open, and now blocked only on datasheets** — Blocks A–C and F closed
except Q2 (channel policy) and Q4 (board name/PN/rev), neither of which blocks drawing.
The §8 [VERIFY] checklist is the gate: **13 of 16 open, every one a datasheet read.**
G0-L **open** — blocked on Blocks D and E, unchanged.

**Symbol library** — `hw/lib/ODSP12.kicad_sym`. First symbol done:

| Symbol | Pins | Verification | Status |
|---|---|---|---|
| `ADAU1466` | 72 + EP, 3 units (Power / Serial Audio / Control) | Table 18 rendered pp.18-21 **and** Figure 11, independently read, 100% agreement (T1-37) | Ready for eyeball |
| `AK5574` | 48, 2 units (Analog / Digital) | Pin Functions pp.5-6 rendered and read (T1-47) | Ready for eyeball |
| `AK4458` | 48, 2 units (Analog / Digital) | Pin Functions pp.8-9 rendered and read (T1-47) | Ready for eyeball |
| `BM83SM1` | 50, 2 units (Power+Audio / Host+GPIO) | Table 2-2 pp.13-15 rendered and read (T1-56). **Names are the Host-mode function**; config-dependent pins carry `*` so the sheet shows which meanings depend on the flashed config (F32) | Ready for eyeball |

All four generated by `hw/lib/gen_symbols.py`, which **asserts every pin number appears exactly
once and that the set is exactly 1..N (+EP)** — the generator refuses to emit an incomplete symbol.
`kicad-cli sym upgrade` reports no change needed; all **9 units** export to SVG.
**The DL-14 eyeball set is complete — all four parts ready, reviewable as a batch.**

**Still open on the BM83:** V-12's keepout dimensions. Pages 54-55 are rendered but **not yet
read** — the antenna keepout, no-ground-under-antenna zone and mounting clearances come off the
mechanical drawing together, and they belong with the footprint rather than the symbol.

**Layer count: ≥ 4, decreed** (F25) — a floor from the silicon, not a routing estimate. 6 stays
live. This is the first Block E slot to close, and it closed from a datasheet rather than a fab
conversation.

**First sheet drawn: `02_dsp.kicad_sch`** (page 3). ADAU1466 as U1A/U1B/U1C, **all 73 pins
dispositioned — 60 nets + 13 explicit no-connects**, generator-asserted so an undispositioned pin
is a build failure rather than an oversight (F28 made mechanical). Net names per §10 [HARD].

**Verified by netlist, not by ERC** — see the ledger entry. `+1V2_CORE` reaches pins 20/35/53/71;
`GND` reaches all 13 ground-class pins including `VDRIVE` (T1-41) and the exposed pad; 54 nets
total.

**ERC is not clean, and should not be yet:** 38 `isolated_pin_label`, 11 `pin_not_driven`,
4 `power_pin_not_driven` — every one of them a label or pin whose counterpart lives on a sheet not
drawn yet. They retire as sheets fill. **G1b is not met and is not claimed.** Off-grid endpoints
were found and fixed; that one *was* a real defect.

**`01_power.kicad_sch` is drawn** (page 2). 14 devices — 3× LM61460-Q1, TPS62823, 5× LT3045,
ADS1015, TMP461, and the R2/R3/R4 PG→EN network — **every pin dispositioned**, 10 rail testpoints,
and the F34 divider arithmetic written on the sheet where a BOM cost-pass will trip over it.

**Cross-sheet integration is live and netlist-verified:** `+3V3_PLL` joins U9's output to the DSP's
`PVDD`; `DSP_THD_P`/`_M` join the TMP461's remote channel to the DSP's thermal diode;
`PG_3V3_D` → R4 → `EN_3V3_PLL` → U9 `EN/UV` is the complete F34 chain.

**Passive pass done — 69 devices, and ERC fell 118 → 82** as predicted: the rails are now *driven*
through their inductors, with feedback dividers closing each loop.

**Divider values computed from datasheet references, not assumed** (M2) and snapped to E96 —
LM61460 `VREF = 1.0 V`, LT3045 `ISET = 100 µA ±1 %`:

| Rail | Network | Actual | Err |
|---|---|---|---|
| +5V_D | Rt 40.2k / Rb 10k | 5.020 V | +0.40 % |
| +3V3_D | Rt 23.2k / Rb 10k | 3.320 V | +0.61 % |
| +6V2_A | Rt 52.3k / Rb 10k | 6.230 V | +0.48 % |
| +5V_A | Rset 49.9k | 4.990 V | −0.20 % |
| +3V3_A / _CLK / _PLL | Rset 33.2k | 3.320 V | +0.61 % |
| +3V6_BT | Rset 35.7k | 3.570 V | −0.83 % |

**Err column is E96-snap error only** — the full stack is snap + resistor ±1 % on both legs +
reference tolerance. Every rail here has a wide window and clears comfortably, but **the caveat
travels with the format** so a future tight-window rail reusing this table inherits it. +3V6_BT at
−0.83 % is the loosest fit and still holds ~28 % of its window as margin; it is recomputed for the
AP2127K-ADJ under V-23 anyway, where the FB reference tolerance joins the stack.

**Closed since:** **V-24** — TPS62823 `VFB = 0.6 V`, so +1V2_CORE takes equal legs, 100k/100k,
exactly 1.2 V; datasheet fetched into the archive (32 pp, Rev. C). **V-25** — LM61460 spread
deviation is **±2 %**, so at 2.2 MHz typ the worst-case instantaneous fundamental is
1.98 × 0.98 = **1.94 MHz, clear of the AM band's 1710 kHz top.** `RT = 5.76 kΩ` is **decided**,
and it is a datasheet point rather than an interpolation.

**Deliberate non-action, logged so it is not re-proposed:** the two battery-side bucks could be
synchronised via `EN/SYNC` to a common clock to avoid beat products. **Do not.** Beyond the pin and
net cost, the datasheet is explicit that *"a valid synchronization signal overrides spread
spectrum, turning it off"* — **syncing would disable the very mechanism that decorrelates them**,
and the beat between two spread carriers is itself spread. The non-action is now supported by the
part's own behaviour, not only by economy.

**±13V5_A is drawn** (F39, decreed and built 2026-08-16). Four devices — **U13** LM5156-Q1 SEPIC
→ +15V5_A, **U14** LM61460-Q1 as an inverting buck-boost → −15V5_A, **U15** LT3045 → +13V5_A,
**U16** LT3094 → −13V5_A — plus their passives. **116 devices on the sheet, every pin
dispositioned.** Two new symbols built from datasheet pin tables (LM5156-Q1, LT3094), library now
**9 symbols / 14 units**. Rail count 10 → 12; testpoints 10 → 14.

**Two defects found and fixed during the draw, both in already-committed work:**
- **F40** — every LT3045 carried `R_ILIM = 20 kΩ`, which programs a **7.5 mA** limit against
  rails budgeted 15–200 mA. All five analog rails would have current-limited into collapse.
- **F41** — growing the testpoint grid silently **shorted three net pairs** by landing global
  labels on identical coordinates. Every assertion passed; only the netlist showed it.

Both are now guarded: ILIM ties to GND per the datasheet, and a **`LABEL COLLISION` assertion**
(negative-tested) makes the second class a build failure rather than a discovery.

**VBATT_PROT is drawn** — F1 5 A fuse → D2 TVS → Q2 reverse P-FET (drain to battery, source to
load, so the body diode is forward in normal flow and blocks on reverse) → damped LC → VBATT_PROT.
**125 devices on the sheet.** All five published criteria are answered *on the sheet*, including
the Middlebrook inequality with values: undamped, the filter's peak output impedance is **47 Ω
against a −4.05 Ω load — violated by 21 dB**; with R<sub>d</sub> = 0.68 Ω and C<sub>d</sub> =
47 µF it is **0.69 Ω, a 15.4 dB margin**. **One criterion does not close: F42, escalated** — the
SMBJ24A misses the load-dump energy by 40–165×, and the board currently makes that scope claim
silently.

**THE POWER SHEET'S OPEN LIST IS EMPTY.** The three mechanical items ran 2026-08-16:

- **PWR_FLAG pass** — 9 flags on the nets whose source is a passive (every switcher rail formed
  after an inductor or diode, plus GND and the battery input). **`power_pin_not_driven` 8 → 0.**
  Flags were placed *only* where no active source exists; the LDO rails already carry a
  `power_out`, and flagging those would suppress a check still doing work. It surfaced one real
  modelling defect: `VDRIVE` was typed `output` while the datasheet directs grounding it, so an
  Output met the GND flag's Power output. **Retyped `passive`** — a pin the datasheet tells you
  to tie to a rail is a terminated node, not a driver. **`pin_to_pin` 1 → 0**, without an ERC
  exclusion, which §4 forbids anyway.
- **Saturation / DC-bias sweep** — every inductor **derived, snapped to E12, then re-derived at
  the snapped value**, because the ripple a 2.2 µH part gives is not the ripple a 1.98 µH
  calculation asked for. Emitting the raw number would have been **the 135 kΩ defect in another
  component class.** Results: +5V_D 10 µH · +3V3_D 1.8 µH · +6V2_A 15 µH · +1V2_CORE 2.2 µH ·
  IBB 15 µH · SEPIC 10 µH coupled. `Isat` quoted at 1.6× peak *operating* current with the gap
  to the converter's ~7 A fault limit **named as a choice, not left as an oversight**. The
  ceramic rule — rated ≥ 2× working, effective capacitance where a number is load-bearing — is
  on the sheet with its two live cases.
- **V-23 closed** — AP2127 **V<sub>REF</sub> = 0.8 V ±2 %**; 34.8 k / 10 k → **3.584 V**, inside
  `BAT_IN`'s 3.2–4.2 V across the full stack, with the datasheet-recommended feed-forward cap.
  **F36 closes with it**: the PROVISIONAL LT3045 is off the sheet and U10 is an AP2127K-ADJ.

**Still open on this sheet:** nothing. Remaining traps — **inductor saturation current** (the spec that matters, not RMS
heating; the 10 µH values on this sheet are **placeholders marked PROVISIONAL**, not derivations)
and **ceramic DC-bias derating** (sheet values must be *effective* capacitance at working voltage,
and the IBB's input caps span the full 31 V). **ERC 87**, in four enumerated classes:
50 `isolated_pin_label`, 15 `pin_not_driven`, 14 `label_dangling` — all counterparts on undrawn
sheets — plus **8 `power_pin_not_driven`, which are a real class needing a PWR_FLAG pass** before
G1b can close. **G1b remains unmet and unclaimed.**

### Open items at the boundary — the complete list

**Operator-owned (nothing else is):** none. Q2 and Q4 closed; no ⬜ UNSET remains in the
governance layer.

**Next action, prepared and waiting:** the **±13V5_A topology proposal** (assistant brings it,
operator dispositions against the four published criteria below).

**Open [VERIFY]s:** V-04 (AK5574 MCLK ratios, ADC side) · V-06 (OPA1656 output swing) ·
V-12 (BM83/WROOM-1 keepout *dimensions* — pages rendered, not yet read; belongs with footprints) ·
V-14/V-15/V-16 (mute part Ron/Coff + disorderly-transient measurement) · V-17 (AKM AVDD currents,
sizes +6V2_A) · V-18 (ADAU1466 core ripple tolerance) · V-23 (AP2127K-ADJ FB reference).

**Open findings:** F4 (impedance targets — layout) · F12 (output-stage gain vs noise budget) ·
F13 (ESP32-S3 GPIO map against the **module** datasheet, three specific checks logged) ·
F15 (MCLK/LRCK phase coherence) · **F37** (pin the SS-enabled LM61460 PN) ·
**F38** (the eight-line PN-pinning sweep, run once at first BOM emission).

**Undrawn:** sheets 03–09 (control, BT, SPDIF, analog in, both DAC/output sheets, IO) ·
±13V5_A and VBATT_PROT blocks on 01_power · all footprints · the whole PCB.

**Gates:** G0-S closed except datasheet residue · **G1b unmet and unclaimed** (ERC 80) ·
G0-L still blocked on Blocks D/E (mechanical + fab), which remain the largest unknown on the
project — **layer count has a floor of 4 (F25) but no outline, no stackup, no fab house.**

### Session boundary — deliberate, 2026-08-16 (fourth). READ THIS FIRST.

**ALL TEN SHEETS ARE DRAWN. ERC = 41 and the number is ABSOLUTE** — no violation waits on an
undrawn counterpart. Nothing is half-wired; every stop this session was taken *before* a block.

**F50's COPPER IS DRAWN (2026-08-16, fifth pass). ERC 41 → 33.** `06_analog_in` is now 158
instances / 440 labels. Executing the criteria changed the block's shape and turned up two
findings — **F52** (the amplifier's gate rules out both named candidates) and **F53** (every sheet
has been declaring a page smaller than its content, so the PDF export has been clipping every
on-sheet note since the first sheet). See §7.

### Review pass 1 — dispositioned 2026-08-16. **9 raised, 7 accepted, 1 refuted, 1 partly each.**

Per **M19**, each was validated against the artefact before being accepted *or* dismissed.
The reviewer stated their method (no renderer; `pdftotext -layout` only) and flagged their own
table reads as weak — **that self-scoping was correct and it is what made A4 cheap to confirm.**

| # | Claim | Verdict | What it cost / bought |
|---|---|---|---|
| V1 | OPA1656 exclusion confirmed | **Confirmed** | Reproduces exactly; still holds after F54 shrank the swing (478 → **453 mV**) |
| V2 | Swing cross-checks to 95.3 % FS | **Confirmed** | Independent path, same number |
| A1 | F53's blast radius unscoped — which closed checks ate a bad export? | **ACCEPTED, and it was the right question** | Enumeration run (§5, M21). **Result: nothing load-bearing.** Every net walk used the netlist, every [VERIFY] a vendor PDF, ERC/DRC JSON. The footprint eyeball wasn't done *badly* — **it has never been done, because no footprint exists** |
| A2 | The ±50 mV window is a **DC** spec; the writeup converted it to an instantaneous-CM limit | **ACCEPTED — the sharpest finding of the pass** | An inference was stated in the register of a datasheet limit, to justify a topology change and two part exclusions. Rationale re-led with T1-106 (parse-independent); the window demoted to corroboration **with the caveat attached**. **No copper changed** |
| A3 | The noise budget predates the drawn topology | **REFUTED on the core claim, accepted on two riders** | N<sub>res</sub> contains R<sub>A</sub>‖R<sub>B</sub> and the op-amp factor is (NG<sub>N</sub>²+1) = 3.25 — **exactly two legs; a single buffer would be 1.0.** The budget is native to what was drawn. Their divider figures (10 k/100 k) were speculative; actual is 2 k → 1 kΩ. **I<sub>B</sub> *is* already a stated gate** — they inferred otherwise from my under-reported chat summary, which is A5's fault, not theirs. **But their 112 dB point lands:** I compared a *noise* number to an *S/(N+D)* number. T1-109 fixes it — the noise number is DR **121 typ / 117 min** |
| A4 | FS is 2.7 Vpp **min**; 95.3 % was computed against typ | **CONFIRMED at figure level → F54, copper changed** | They asked for figure-level confirmation before action; I have the renderer, they don't. Confirmed, **and the same render produced T1-109 and T1-110** — two facts neither of us had |
| A5 | Three of five published criteria unreported | **ACCEPTED** | All five were *met on the sheet*; three were absent from my narrative. Accounted for below |
| A6 | General form: values extract, topology doesn't | **ACCEPTED → M20** | Sweep run: **14 of 23 figure-cited T1s carry no structural language**, and it flagged a real open gap (T1-31 / V-12) on first application |
| A7 | Crosstalk transfer function missing; single-supply premise misplaced | **ACCEPTED, and it found a number error** | Prose said −37 dB; the sheet computes **−33.7 dB**. Their decomposition of the gap (4 channels + leg asymmetry) was exactly right. Closed form now on-sheet |

**A5's accounting — all five criteria, including the ones satisfied without incident:**

| # | Criterion | Where it landed | Reported before? |
|---|---|---|---|
| 1 | Ratio-tolerance inequality | NOTE6 — −1.99 %/+1.91 % window, 1 % clears 2.04×, 0.1 % clears 20.4× | Yes |
| 2 | Coupling corner, cold-derated | **NOTE7** — 0.796 Hz / 0.723 Hz, **deliberately mismatched legs** because corner mismatch converts to *common mode*, which the ADC rejects; worst-case cold **1.33 Hz**; group delay 0.40 ms with channel-to-channel spread the thing that matters. **The topology change did move where the DC break sits** — there are now *two* breaks, and matching them is the criterion's real content | **No** |
| 3 | Part pick | → **F52**, four-leg gate | Yes |
| 4 | 10 Ω stability annotation | **NOTE8 gate 4** — the 10 Ω is the isolation resistor and **leg P is a unity-gain follower**, the least stable configuration into a capacitive load. "Do not improve this filter" is written on the sheet | **No** |
| 5 | F49-form clamp inequality on +5V_A | **NOTE9** — 31.2 mA injected vs 146 mA quiescent, clears **4.7×**; plus **no clamp at the ADC pins**, because same-rail-by-construction makes AVDD+0.3 unviolatable | **No** |

**THE NEXT ACTION, unambiguous and in this order:**

**(1) The clock tree** — six criteria plus the rails-up-before-PDN statement, all recorded below.

**(2) Sweep the ERC punch list** — three tiers, below. **F53's paper fix rides along here**: eight
generators still declare A3, the change is ~12 identical lines each, and the pattern is already
proven on `06_analog_in`.

**(3) F52 needs one datasheet** — any single-supply dual op-amp meeting the four-leg gate. This is
the only thing on the sheet that is not committable.

---

**DONE, kept for the argument — F50's copper.** The *disposition* was closed
(T1-103, AKM Figure 76); what the copper added:
   - AC-couple the INA1650 output into a **single-supply +5V_A stage** whose non-inverting input
     sits on a **ratiometric bias: 10 kΩ / 10.5 kΩ from AVDD = 0.51220 × AVDD**, decoupled
     10 µF ∥ 0.1 µF. **Unbuffered is correct** — it feeds an op-amp input, so T1-67 never engages.
   - **Unity gain**, not AKM's −14.5 dB: our 0.94 V<sub>rms</sub> is already at level.
   - **Not an OPA1656.** Single-supply CMOS — OPA2320 / TLV9002 class, sized for the job.
   - ADC pins take AKM's own network: **10 Ω series + 100 pF to ground each, 15 nF differential**
     (film for the 15 nF and 1 nF per the figure's footnote).
   - **F49's clamp inequality repeats on the ADC side** — abs max is AVDD + 0.3 V, and a clamped
     INA input at unity still sends ±13 V toward it. Series R + clamp, inequality on-sheet.
   - **F51 decision due here:** DNP position across the 10.5 kΩ leg so the board builds for
     either date-code revision.

**FIVE DELIBERATE DEPARTURES FROM THAT PLAN, each argued on the sheet — kept side by side with it
because the plan was right about the *inputs* and wrong about the *shape*, and that distinction is
the useful one:**

| Planned | Built | Why |
|---|---|---|
| One unity buffer per channel | **Two amplifiers, differential** | AKM's window constrains the **common mode**; single-ended drive moves it 13.3× the window's width (F50c) |
| "Unity gain" | **Unity *differential* gain**, ±0.5 per leg | Same thing, once the source is single-ended — but it costs a noise-gain of 1.5 on the inverting leg, and that is what makes F52's gate tight |
| Bias feeds the stage | Bias feeds **high-impedance inputs only**; R<sub>BP</sub> = 10 MΩ | A resistor returning to a shared divider injects signal current — −37 dB of crosstalk at the obvious value |
| Film per the figure's footnote | **C0G** at 100 p / 620 p / 15 n | Strictly better than film on every axis that matters here, and available in 0603/0805. A departure *upward* from a vendor note |
| Clamp at the ADC pins | **Clamps at the op-amp inputs; none at the ADC** | The stage runs on the *same* `+5V_A` that feeds AVDD, so no sequencing skew can violate AVDD + 0.3 V. Clamping there would buy nothing and cost voltage-variable capacitance where the CCIF criterion is listening |
| DNP across the 10.5 kΩ leg | **No DNP** | See F51 — the hedge is against parts discontinued in 2021, and it degrades a precision ratio node |

**(2) Then the clock tree** — criteria below, all seven.

**(3) Then sweep the ERC punch list** — three tiers, in this order:
   - **Design work:** `U13_COMP` (SEPIC compensation network is not drawn), the four `MON_*`
     rail-monitor dividers (§9 requires them).
   - **Transcription:** `CLKOUT_DSP` termination.
   - **F28 dispositions only:** the four unused TDM ports, `U6/U8/U9_PG` (PG is disabled by the
     PGFB→OUT disposition — these should become explicit no-connects), `TP_SPDIF_TX`,
     `TEMP_THERM_N`, `SIGNAL_SENSE`, `DSP_SELFBOOT`, `PLLFILT`.

**G1b is NOT claimable and no date is named.** F50 is design work, the clock tree is absent, and
41 is a punch list, not zero. **G0-S is otherwise closed.** **G0-L is untouched — Blocks D and E
remain the largest unknown on the project: no outline, no stackup, no fab house.** Layer count
still has only its floor of 4 (F25), and Block E has gained three thermal claims (the SM8S pad,
the SEPIC magnetics, the 1466's via array) plus one *electrical* one — §12's load-dump table is
conditional on the TVS land pattern being honoured.

**What this session did:** F39 decreed and drawn (±13V5_A), then sheets 01, 03, 04, 05, 06, 07,
08, 09 drawn. **Twelve findings raised (F40–F51), ten [VERIFY]s closed** (V-03, V-04, V-06, V-17,
V-23, V-26, V-27 bounded, V-28, V-29 by analysis, V-30). **Nine ledger rules added (M9–M17).**
REQUIREMENTS v1.2 → **v1.7**. Library 7 → **16 symbols**. Datasheets 15 → **27**.

**The corrections that mattered most, so they are not re-made:**
- **F40** — every LT3045 was programmed to a **7.5 mA** current limit. All five analog rails
  would have collapsed.
- **F41** — the testpoint grid silently **shorted three net pairs**; every assertion passed.
- **F48** — the relay fail-direction trade violated the INA1650's **abs-max by 5 V**.
- **F50** — the ADC bias was **2.51 V outside its window**; a fixed reference cannot fix it.
- **Testpoints were labels, not components** — they would never have reached copper.
- **Both AK4458s answered at 0x11**, found by re-emitting §9 as a gate.

### Clock tree — criteria published 2026-08-16, block NOT started

The [HARD] §3 section with the most downstream consequence and the least copper. **Criteria, so
they survive the compaction:**

1. **XO PN pinned with the jitter spec that justified §3** — the "CCHD-575 class" placeholder
   becomes an orderable line with phase-noise/jitter numbers stated, **output format and level
   verified against the ADAU1466's MCLK input requirements** (the last unread corner of V-01's
   document), F38 one-line why attached.
2. **The `1G` pull-up is DRAWN, not just dispositioned** — T1-68's "floating disables the whole
   fanout and no MCLK reaches any converter" lands as a **fitted resistor** with its idle level
   on-sheet (F21).
3. **Source termination at every fanout output** — series R at the driver per the LMK1C1104's
   guidance, values stated, **length-matching and impedance handed to Block E as a routing
   input** rather than left implicit.
4. **`+3V3_CLK` arrives with its reason** — one-line cross-reference to F33, per the convention
   set when the rail was decreed.
5. **V-04's ADC side is CLOSED** (T1-103/T1-104) — 512fs confirmed, so this criterion is already
   satisfied; the read that closed it also produced F50 and F51.
6. **No spread-spectrum touches this sheet — restated in copper**, because that is where a future
   EMI fix would be proposed (M15's placement logic).
7. **NEW, inherited from V-04:** the tree's **rails-up-before-PDN** property gets stated on the
   clock sheet itself, since that sheet is where a future *"gate the fanout from the MCU for
   power savings"* proposal would arrive — and that proposal would break §7.2's precondition.

### Session boundary — deliberate, 2026-08-16 (third): stopped BEFORE 06_analog_in

**V-17 is closed and the analog anchors are staged, but the sheet is not started.** This is the
same stop-before-a-block rule that governed `01_power`: `06_analog_in` is the largest analog block
on the board and four of its eight published criteria need real derivation, not transcription.
Starting it at the end of a long pass and finishing it in the next one is exactly the half-wired
state the convention exists to prevent. **Nothing is partially drawn.**

**Everything the sheet needs is now T1 and on the record:**

| Anchor | Value | Source |
|---|---|---|
| AK5574 full scale | **0.56 × (VREFH−VREFL) = 2.80 Vpp diff = 0.99 Vrms** at AVDD 5 V | AK5574 Note 10 |
| INA1650 | **gain 1 V/V**, 500 kΩ input resistors | SBOS818B |
| Line range | 2 Vrms → **÷2.02, −6.1 dB** | §6.1 ceiling |
| Speaker range | 30 Vrms → **÷30.3, −29.6 dB** | §6.1 ceiling |
| +5V_A | **146 mA max** | V-17 |
| +6V2_A | **186 mA identified** vs 250 mA assumed | V-17 |

**Three things the anchors already decided, before any drawing:**
1. **The INA1650 has no gain to give** (1 V/V), so the attenuator does *all* the range work in
   both modes. There is no "share it between stages" option to consider.
2. **The INA1650's CMRR is trimmed against its own 500 kΩ internal resistors.** External source
   impedance from the attenuator lands in series with them and unbalances the trim — so F9's
   matching requirement is not only about the divider's own ratio, it is about **what the
   attenuator does to the receiver's CMRR**. That materially strengthens the criterion-4
   argument for an integrated array over discrete 0.1 % singles.
3. **Criterion 2 looks pre-decided by the arithmetic:** at 30 Vrms the node sees ±42 V, and an
   analog switch would need rails containing that swing. ±13V5_A does not. Unless the switch
   sits *after* a fixed first-stage attenuation, F8's "or it's a relay" is where this lands —
   and that is the derivation to write on the sheet rather than assert.

**Open and owed to the operator: F46** — `+3V3_A` has no identified load, and reading (c) would
be a real design difference rather than bookkeeping. It is escalate-class (rail architecture) and
it wants a decision before the analog sheets commit to supplies.

### Session boundary — deliberate, 2026-08-16 (second)

**Stopped before the ±13V5_A disposition, not partway through it.** `01_power` is drawn to the
passive pass and ERC sits at **80, falling for enumerated reasons**. Nothing is half-wired.

**The next move is a single delegated decision**, prepared and waiting: **±13V5_A topology
(SEPIC vs dual-boost)**, carrying its "designer's call" tag since v0.1. The operator has stated
the disposition criteria **in advance**, so the proposal is built against them rather than
defended after:

| # | Criterion |
|---|---|
| **a** | **<50 µVrms, 20 Hz–20 kHz** at the op-amp rails after LDO/filtering — with the LDO's **actual PSRR curve at the topology's switching frequency** doing the work. **The proposal must state f_sw**, because PSRR at 100 kHz and at 2 MHz differ by decades |
| **b** | **Asymmetric load reality** — the op-amp rails draw class-A-ish quiescent plus signal current, so **regulation under imbalance** matters more than total capacity |
| **c** | **Magnetics honesty** — SEPIC's coupled inductor vs dual-boost's two inductors plus an inverting stage is where the real BOM difference lives |
| **d** | **F38 applied at birth** — whatever controller is proposed, **PN pinned with options stated** |

*"If the proposal survives those four, it's decreed on arrival."*

Queued behind it: **VBATT_PROT** (ISO 7637-2 front end — reverse-FET, TVS, LC, with the gate
zener and standoff-vs-clamp arithmetic getting the on-sheet-inequality treatment, because load
dump is where nominally-fine boards die), **V-23** (AP2127K-ADJ divider), and the two remaining
traps — **inductor saturation current** and **ceramic DC-bias derating** — which land *with* those
blocks, not after them.

### Earlier session boundary — read this before reconstructing anything

**`01_power.kicad_sch` is deliberately undrawn.** It is **not** stopped partway through: the file
is the empty stub `gen_hier.py` created, no components were placed, and nothing is half-wired.
The stop was chosen, not hit.

~~**The first move is symbols, not the sheet**~~ — **done 2026-08-16.** `LM61460-Q1`,
`LMK1C1104` and `INA1650` are built and verified; the library now holds **7 symbols / 12 units**,
and **no part on the power sheet is missing a symbol.** F34's open [VERIFY] closed in the same
pass (T1-64: `PGOOD` is open-drain).

**The next move is `01_power` itself**, built to the three conventions below. Nothing else blocks
it: topology settled through F34, all ten rails sourced and budgeted, PG-to-EN resolved,
sequencing-as-nets on file. **F35 is an open observation, not a blocker** — it affects the clock
sheet, not this one.

**01_power's design is settled, and F34 gated it** — it changes the sheet's enable topology, so it was raised
before drawing rather than after. Three conventions are set for that sheet: **(1)** every rail
gets a testpoint with its §7.1 name silkscreened — one namespace across silk, schematic and
`BRINGUP.md`, so bring-up is a multimeter walking a checklist; **(2)** sequencing signals are
**nets, not annotations** — enables, rail-monitor dividers into the ADS1015, PDN/reset lines all
originate or terminate here, so §7.2/§7.3 and the sheet can be checked against each other
mechanically; **(3)** footprints for the +3V6_BT and +3V3_PLL LDOs accommodate the likely
alternates (SOT-23-5 / SOT-89 class) while their [VERIFY]s are open — free now, a respin later.

**Next action:** three findings await operator disposition, two of them respin- or [HARD]-class:
**F30** (AK5574 wake-up silences the whole I2C bus — §7.2 amendment), **F31** (BM83 supply rail:
`BAT_IN` is 3.2-4.2 V, not 5 V, and 3.3 V −5 % is below its minimum), **F32** (module ships in
Embedded mode; who flashes Host mode, and when). Then V-12 keepouts + footprints, then the first
sheet.

**Two confirmations folded in:** the output-stage **13.2 dB gain is now derived from verified
endpoints at both ends** — AK4458 full-scale measured 2.8 Vpp at AVDD 5 V (T1-11/T1-49) and the
4.5 Vrms [HARD] requirement — rather than assumed at either. And `VDD18` on both AKM parts is an
**internal-LDO output, not a supply input**: it wants an explicit *do-not-load* label per F28,
because a node with a capacitor and a voltage on it looks exactly like a rail to whoever probes it
next — V-04 ADC side + F15 phase
coherence, V-06 output swing, V-12 keepout dimensions via `pdftoppm`, V-17 (analog AVDD currents,
to size +6V2_A), and F13's module-datasheet pass. **One item is escalated and awaiting the
operator:** a third LT3045 dedicated to the MCLK fanout buffer (§7.1 note 6) — not fitted until
approved, per the new `CLAUDE.md` §4 rail-architecture rule.

**Governance is closed.** Q2 and Q4 both settled; no ⬜ UNSET remains in the constitution's
decision layer. The open set is purely technical.

**Zero-slack note for a future ODSP-16:** a third AK4458 has no address to live at — the
0b00100 prefix is full at four devices. I2C1 comes out of reserve at that point, not before.

**Datasheets:** 14 held and verified (`DATASHEETS.md`). ADAU1466 Rev. C and LT3045 Rev. D supplied
by the operator 2026-08-15; analog.com remains unreachable from here for anything further.

**Layout-blocked list gained an entry:** the ADAU1466's **5.3 mm exposed-pad via array** is now a
Block E stackup input (F17). Logged here so it is not rediscovered at fab-quote time. Its paste
aperture wants **windowed openings rather than one flood** and is called out in the DL-14
verification pass.

**Baseline safety copy:** none — nothing to copy yet. The first board file that lands here gets a
copy with its SHA256 recorded in this section **before** any edit.

**Standing risks:**

| Risk | Status |
|---|---|
| ~~Directory not under version control~~ | **Closed** — git initialised 2026-08-15, T1-D38 / DL-15 |
| No baseline copy exists yet | Open — vacuous until files arrive, then immediate. Note git now covers *history*, which is not the same thing as a pre-batch-edit restore point |
| `REQUIREMENTS.md` is v0.4 and still a baseline | Open — cite by section **and** version; a v0.5 supersedes and does not merge silently |
| KiCad 10 postdates the assistant's training | Open, permanent — CLI and `pcbnew` API are T2 from memory, T1 only from `--help`/`dir()`. See ledger |
| 4 findings open (§7): F4, F12, F13, F15 | Open |
| Mute topology decided (series–shunt, DL-19); parts not yet chosen | Open — V-14/V-15. Much lower risk than at v0.3: two lax requirements on two cheap parts rather than one constrained optimisation |
| **Only the operator can close Q2** (channel policy) | Open — owed next round. Does not block drawing |
| **F17 — ADAU1466 may have no LQFP option** | Open, T2 — if it is LFCSP-only, §2's hand-rework rationale fails and a thermal-via requirement enters the stackup. Settles at V-01 |
| analog.com unreachable (T1-15) | Open — needs a manual download; blocks V-01 and therefore the first sheet |

---

## 1. T1 — Source of truth

Each entry names **how it was verified**. Nothing enters on reasoning alone.

| ID | Fact | Verified by |
|---|---|---|
| T1-01 | Project directory contained no files before this document set | directory listing, 2026-08-15 |
| T1-02 | The directory is not a git repository | environment report + `git rev-parse`, 2026-08-15 |
| T1-03 | Constitution derives from the template at `C:\Users\nick\.claude\templates\pcb-project\` | both template files read in full, 2026-08-15 |
| T1-04 | `REQUIREMENTS.md` reproduces the operator's v0.1 text with formatting normalised only; v0.2 changes are each traceable to an operator disposition in its revision history | transcribed and re-read, 2026-08-15 |
| T1-05 | KiCad **10.0.5** installed at `C:\Program Files\KiCad\10.0\` | `kicad-cli --version`, 2026-08-15 |
| T1-06 | `kicad-cli.exe` is at `...\10.0\bin\` and is **not on PATH** | `Get-Command kicad-cli` → not found; direct invocation at full path succeeded |
| T1-07 | Bundled Python 3.11.5 at `...\10.0\bin\python.exe`; `pcbnew` 10.0.5 imports | `python.exe -c "import pcbnew; pcbnew.GetBuildVersion()"` |
| T1-08 | `pcb drc` and `sch erc` both support `--severity-exclusions`, `--exit-code-violations`, `--format json`; `pcb drc` also `--schematic-parity` | `kicad-cli pcb drc --help`, `sch erc --help` |
| T1-09 | Stock libraries present: 224 symbol, 155 footprint, 105 3D-model | directory count under `share\kicad\` |
| T1-10 | **AK4118A has no internal SRC** — PLL clock recovery only; rate conversion was never on that die | Operator confirmation, 2026-08-15. Closes V-02 and is the basis of the F1 disposition |
| T1-11 | **AK4458 full-scale output = 2.8 Vpp differential** at (VREFH−VREFL) = 5 V, per DAC channel | `AK4458_AKM.pdf` (90 pp, official AKM), 2026-08-15. Closes V-05 |
| T1-12 | **INA1650 is dual-channel**; INA1651 is the single-channel sibling | `INA1650_TI.pdf` p.1 (official TI), 2026-08-15. Closes V-11 and re-grounds T1-D27 on the manufacturer document |
| T1-13 | 12 manufacturer datasheets held locally in `datasheets/`, each verified by page count and first-page content after download; register in `DATASHEETS.md` | Retrieval + `pdfinfo`/`pdftotext` verification, 2026-08-15 |
| T1-14 | poppler 25.07.0 installed (winget, user scope), on user PATH; provides `pdftotext`, `pdfinfo`, `pdftoppm` | `winget install`, binaries exercised on the archive, 2026-08-15 |
| T1-26 | **AK4458 MCLK ratio at 48 kHz: 512fs or 768fs** (30-54 kHz band). Our 24.576 MHz XO is exactly **512fs at 48 kHz** — compatible. "In PCM mode, master clock is divided automatically by fs rate auto detection" | `AK4458_AKM.pdf`. Closes V-04 for the DAC side |
| T1-27 | **All four AKM parts select I2C vs 3-wire serial by pin strap.** AK4458: I2C mode requires `I2C` pin = H **and `PS` pin = L** (PS = H gives *parallel* mode). AK5574: `I2C` pin = H selects I2C (L selects 3-wire). AK4118A: `IIC` pin = H selects I2C | The three AKM datasheets. **Closes V-09** |
| ~~T1-28~~ | ~~AK4118A has C1 fixed at 0, leaving two addresses~~ — **WRONG, RETRACTED 2026-08-15.** That clause belongs to the AK4118A's **4-wire serial mode (IIC pin = "L")**, not I2C. Superseded by T1-32 | Retracted after a figure-level read; see ledger |
| T1-32 | **All three AKM families share one 7-bit slave-address space: `0b00100` + CAD1 + CAD0 = 0x10, 0x11, 0x12, 0x13.** Identical for AK5574, AK4458 and AK4118A in I2C mode; each device can be strapped to any of the four | Rendered figure reads: AK4458 Fig. 73 (p.70), AK5574 Fig. 63 (p.57), AK4118A Fig. 38 (p.38) + §(2)-1-4 verbatim. **Closes F23** |
| T1-33 | **AK5574 3-wire serial has a drive-conflict hazard:** "The I2C interface block continues to run, even when the 3-wire serial interface is selected." A CDTI(SDA) H→L while CCLK(SCL) is H reads as a START; if the following bits match the slave address the I2C block drives ACK onto the shared pin, conflicting with the 3-wire input, and "the data cannot be reliably written". Mitigation: change CDTI only on the CCLK falling edge | `AK5574_AKM.pdf` p.57. **Independent support for rejecting the SPI escape hatch** |
| T1-29 | **OPA1656 quiescent current = 3.9 mA per channel**, 100 mA output drive | `OPA1656_TI.pdf`. Confirms the ~96 mA figure in the T1-D30 rail budget (24 × 3.9 = 93.6 mA) |
| T1-30 | **LMK1C110x supply is 3.3 V / 2.5 V / 1.8 V — it is not a 5 V part.** Additive jitter 7.5 fs typ specified at VDD = 3.3 V | `LMK1C1104_TI.pdf`. Drives F22 |
| T1-31 | **Both modules mandate an antenna keepout.** BM83: "Figure 7-4. Recommended Keep-out Area for PCB Antenna" — "No copper, No component" and no ground plane under the antenna on the host PCB. ESP32-S3-WROOM-1 has an antenna keepout zone; **the -1U variant does not, because it uses an external antenna** | `BM83_Microchip.pdf`, `ESP32-S3-WROOM-1_Espressif.pdf`. **V-12 partially closed** — existence and mandate confirmed; exact dimensions live in figures and need a `pdftoppm` render |
| T1-16 | **ADAU1462/ADAU1466 ship in ONE package: 72-lead LFCSP, `CP-72-6`, 10 x 10 mm, 5.3 mm exposed pad.** The ordering guide lists six orderable models and every one is LFCSP. **There is no LQFP and no WLCSP.** Temp range -40 C to +105 C | `adau1462-1466.pdf` Rev. C p.202 ordering guide + p.1 features. **Closes V-01 (package), confirms F17** |
| T1-17 | **4 serial input ports, 4 serial output ports.** Up to **8 stereo ASRCs**, ratio 1:8 to 7.75:1, 139 dB dynamic range, THD+N -120 dB, I/O sample rate 6-192 kHz | Rev. C p.1 features + spec tables. Closes V-01 (ports/ASRC); `REQUIREMENTS.md` §2/§4 confirmed correct |
| T1-18 | **Serial ports are independently master/slave, per port.** `SERIAL_BYTE_x_0` at 0xF200 / 0xF204 / 0xF208 / 0xF20C (SDATA_IN0…IN3), Bit 9 `LRCLK_MODE`, Bit 8 `BCLK_MODE`. Pin descriptions state per port that "Serial Input Port *n* is a master or slave" | Rev. C register map + pin table. **Closes V-13 — the F1 disposition is confirmed against the document** |
| T1-19 | **SPI slave-port max SCLK = 20 MHz**, read and write (`fSCLKWRITE`, `fSCLKREAD`) | Rev. C timing specs. **Closes V-07** — the 10 MHz target has 2x margin |
| T1-20 | **DVDD = 1.2 V ±5% (1.14-1.26 V). ADAU1466 core current: 213 mA minimal program, 220 mA typical, 233 mA typ / 495 mA max for maximum program.** The typical figure is measured with 16-channel I/O, 10-band EQ per channel, all ASRCs active. IOVDD current 53 mA at 3.3 V with all serial ports as clock masters | Rev. C Tables 2/3. **Closes V-08** |
| T1-21 | **The on-chip 1.2 V regulator is a controller, not a self-contained LDO** — pin 3 `VDRIVE` is a "PNP Bipolar Junction Transistor-Base Drive Bias Pin for the Digital Supply Regulator"; DVDD is derived from IOVDD "in combination with an external pass transistor", up to an 800 mA load | Rev. C pin table + regulator spec |
| T1-22 | **Supply sequence depends on the DVDD method.** Internal regulator: DVDD comes up **after** AVDD, IOVDD and PVDD. DVDD supplied directly: **"no special sequence is required"** | Rev. C power supplies section |
| T1-23 | **The control port is dead while the PLL locks.** "While the PLL is attempting to lock, the I2C slave and SPI slave control ports are inactive… all attempts to write to the control port fail." Max lock 10.666 ms at 48 kHz (3.072 MHz post-prescaler); typically ~3.5 ms. Poll `PLL_LOCK` at 0xF004 Bit 0 | Rev. C power-up / PLL section |
| T1-24 | **Firmware contract, first pass:** PLL registers 0xF000 `PLL_CTRL0`, 0xF001 `PLL_CTRL1`, 0xF002 `PLL_CLK_SRC`, 0xF003 `PLL_ENABLE`, 0xF004 `PLL_LOCK`. Output routing `SOUT_SOURCEx` at 0xF180-0xF197. Software safeload via `num_SafeLoad_Lower` / `num_SafeLoad_Upper`, 1-5 parameters per transaction, page-split addressing | Rev. C register map + Software Safeload section |
| ~~T1-25~~ | ~~SELFBOOT pin 34: floating -> SPI self-boot, 10 kOhm pull-down -> I2C self-boot~~ — **PARTIALLY WRONG, corrected 2026-08-16.** The protocol-select behaviour belongs to **pin 26**, not pin 34. Superseded by T1-34/T1-35 | Text-extraction error across table rows; caught by the figure-level read |
| T1-34 | **Pin 34 `SELFBOOT`: internal pull-up.** Logic high (IOVDD) initiates self boot on the **next rising edge of `RESET`**; tied to ground = no self boot. May be strapped directly or through a >=1.0 kOhm resistor | Table 18 p.20, rendered. **F21's disposition is confirmed** — floating means high means self-boot from a DNP EEPROM |
| T1-35 | **Pin 26 `SS_M/MP0` selects the self-boot *protocol*** — internal 250 kOhm pull-up; when SELFBOOT is high at the RESET rising edge, **floating = SPI, 10 kOhm pull-down to DGND = I2C**. Irrelevant while SELFBOOT is grounded, but it is a second strap that must be deliberate if self-boot is ever stuffed | Table 18 p.19, rendered |
| T1-36 | **Pin 24 `RESET` is active low with an internal pull-DOWN** — the part is held in reset by default at power-up and must be *actively released*. Triggers on high->low, exits on low->high | Table 18 p.19. Confirms the §7.2 step-3 model is safe by default |
| T1-37 | **Complete ADAU1466 pin map verified: all 72 pins + exposed pad.** Table 18 (pp. 18-21, normative per T1-D45) rendered at 170 dpi and read, cross-checked against Figure 11 (p.18). **100% agreement, zero discrepancies** | Figure-level render of four pages + independent diagram read. This is the M2 method record for the symbol |
| T1-38 | **Exposed pad is ground and thermally mandatory:** soldered to a copper square of equivalent size, "**identical copper squares must exist on all layers** of the board, connected by vias, and they must be connected to a **dedicated copper ground layer within the PCB**" | Table 18 p.21 + Figure 11 note. Drives **F25** |
| T1-39 | **The ADAU1466 has an integrated S/PDIF receiver AND transmitter** — pin 4 `SPDIFIN` ("Input to the Integrated Sony/Philips Digital Interconnect Format Receiver"), pin 5 `SPDIFOUT`. Both internally biased to IOVDD/2 | Table 18 p.18. Drives **F26** |
| T1-40 | **Pins 63/64 `THD_M`/`THD_P` are a thermal diode**, intended for "the D- / D+ pin of an external temperature sensor IC" — a *remote-diode* sensor, not a local one | Table 18 p.21. Drives **F27** |
| T1-68 | **LMK1C1104 `1G` has an internal 300 kOhm pull-DOWN and "switches the outputs into a low state when 1G is low"** — so **left floating, the entire clock fanout is disabled** and no MCLK reaches any converter. Must be actively pulled/driven high. **`Y3` unused: "Unused outputs can be left floating"** — the datasheet's own guidance | TI SNAS791D pp.3, 7. Textbook F21: floating is a state someone chose, and here it chose *off*. Failure presents as "the converters don't work" |
| T1-69 | **MIC5504 is fixed-output only** — 1.2 / 1.8 / 2.5 / 2.8 / 3.3 V, **no 3.6 V variant** | Stock `Regulator_Linear.kicad_sym` enumeration. Drives **F36** |
| T1-70 | **Stock symbol pin maps, read as name+number pairs from single matches:** `TPS62823DLC` 8 pins (4 = `NC`); `LT3045xDD` **11** pins (2 = second `IN`, 11 = second `GND`); `ADS1015IDGS` 10; `TMP461xxRUN` 10 | Direct extraction. **Supersedes an earlier zipped-regex map that was permuted** — see ledger |
| T1-64 | **LM61460-Q1 `PGOOD` (pin 5) is open-drain** — *"Pull this pin up to a suitable voltage supply through a current limiting resistor. High = power OK, low = fault. PGOOD goes low when EN = low, VIN > 1 V."* | TI SNVSB70F Table 7-1 p.4, rendered. **Closes F34's open [VERIFY]** |
| T1-65 | **LM61460-Q1 pins that must not float: `FB` (4), `RT` (6), `EN/SYNC` (7).** `RT` additionally must not be grounded — it needs 5.76-66.5 kOhm to set 200-2200 kHz. `VCC` (2) is an internal-LDO output: **"do not connect to any external loads"** | Same table. F28 dispositions required for all four |
| T1-66 | **LMK1C1104 is 8-pin TSSOP with FOUR outputs** — `Y0` (3), `Y1` (8), `Y2` (5), `Y3` (7); `CLKIN` (1), `1G` output-enable (2), `VDD` (6), `GND` (4) | TI SNAS791D Figure 6-4 p.3. Drives **F35** |
| T1-67 | **INA1650 is 14-pin TSSOP**; `REF A` (12) and `REF B` (9) **"must be driven from a low impedance"** — not left to a divider. `VMID_IN` (11) takes a noise-reduction capacitor; `VMID_OUT` (10) is the buffered supply-divider output | TI SBOS818B p.3, rendered |
| T1-61 | **V-22, end-to-end read of Power Supplies / Voltage Regulator / Hardware Reset (pp.33-34). No third ordering constraint exists** — IOVDD-first (T1-59) is the only one. But **two mandatory-supply rules** that are easy to optimise away: **`AVDD` "must be supplied even if the auxiliary ADCs are not in use"** and **`PVDD` "must be supplied even if the PLL is not in use"**. Table 23 externally-supplied: IOVDD **yes**, DVDD **optional**, AVDD **yes**, PVDD **yes** | Rev. C pp.33-34, rendered. **Closes V-22** — the section is now read exhaustively, not sampled |
| T1-62 | **`VDRIVE` grounded still draws ~100 µA from IOVDD**, and the internal regulator has **no control registers**. ADI also states *"do not use the regulator to provide a voltage supply to external ICs"* — not applicable here, DVDD is external | Rev. C p.33. Completes T1-41 |
| T1-63 | **`RESET` wants an external pull-down of several kΩ** *"to guarantee that the device is held in reset in the event that the reset supervisory [circuit fails]"* — in addition to the internal pull-down (T1-36). Also: **RAM is not guaranteed cleared by a reset; the DSP program must clear it manually** | Rev. C p.34. Second half is a firmware-contract item |
| T1-58 | **ADAU1466 `PVDD` current: 8.3 / 10.1 / 12.9 mA (25 °C), 15 mA max over temperature.** PVDD range 2.97-3.63 V; absolute max 0-4.0 V | Rev. C Tables 2/3. **Closes V-21** — settles the F33 LDO as a small part, ~44 mW |
| T1-59 | **ADAU1466 supply ordering [HARD]:** all power pins may be applied simultaneously; if not, **`IOVDD` must be first** because it references the internal ESD protection diodes. `AVDD`, `DVDD`, `PVDD` may follow in any order but **must not precede IOVDD** | Rev. C Power-Up Sequence, p.24. Drives **F34** |
| T1-60 | **Stock KiCad 10 already carries LT3045, TPS62823, MIC5504, ADS1015, TMP461, OPA1656 and ESP32-S3-WROOM-1.** Absent and needing project symbols: LM61460-Q1, LMK1C1104, INA1650 | `grep` over `share/kicad/symbols`. **DL-14's stock-first rule pays off** — 7 of 10 power-sheet parts need no symbol work |
| T1-54 | **AK5574 `OVF` is a summary flag, not per-channel.** "The OVF pin outputs 'H' if **one of AIN1-4** channel overflows (**more than -0.3 dBFS**)… returns to 'L' when overflows are resolved. The OVF output has the **same group delay as the ADC**." No per-channel overflow register found in the overflow sections | AK5574 pp.51 + notes. Shapes the F29 disposition |
| T1-55 | **AK5574 wake-up blocks the whole I2C bus, not just itself.** After `PDN` release the internal PDN clears only after 16384 internal-oscillator cycles (**max 10 ms**); register writes are unavailable until then. **"During this period, digital output and digital in/output pins may output an instantaneous pulse… therefore, referring the output of digital pins and data transmission with a device on the same 3-wire serial/I2C bus as the AK5574 should be avoided in this period to prevent system errors."** Initialisation completes in 583/fs (12.1 ms at 48 kHz) | AK5574 timing notes, rendered. Drives **F30** |
| T1-56 | **BM83SM1 has 50 pins.** `BAT_IN` (23) is the main supply at **3.2-4.2 V**; `ADAP_IN` (22) is a **5 V** adapter/charger input, "otherwise it can be left floating". `SYS_PWR` (24) and `VDD_IO` (25) are **internal-use, do-not-connect** (SYS_PWR may feed LED1/LED2 only). I2S: `MCLK1` (5) is **output-only**; `SCLK1` (3) and `RFS1` (2) are I/O, so the module can be I2S master or slave | BM83 Table 2-2, pp.13-15, rendered. Drives **F31** |
| T1-57 | **The BM83 ships pre-configured in Embedded mode**, and pin functions are config-dependent: *"The BM83 module is pre-configured with Embedded mode… The GPIOs mentioned in the preceding table can be configured using the Config Tool or the SDK."* Pin 49 shows the split explicitly — external codec reset (Embedded) vs `UART_TX_IND` host wake (Host). Pin 31 `P3_4/UART_RTS` is additionally a **system configuration pin (Application vs Test mode)** | BM83 p.15 note + Table 2-2. Drives **F32** |
| T1-47 | **AK5574 and AK4458 pin maps verified, 48 pins each.** AK5574 "Pin Functions" pp.5-6; AK4458 pp.8-9 | Figure-level render at 175 dpi and read. M2 method record for both symbols |
| T1-48 | **Neither AKM part needs a 1.8 V rail.** Both have `LDOE`: **H = internal LDO enabled**, and `VDD18` then becomes an output/stabilisation node (AK4458: 1.0 uF to DVSS; AK5574: stabilisation cap). AK5574 TVDD is 1.7-1.98 V when LDOE=L but **3.0-3.6 V when LDOE=H** | AK5574 p.5 pin 17/19/45; AK4458 p.9 pin 44/47 + Note 4. **Confirms §7.1 needs no 1.8 V entry** |
| T1-49 | **Supply rails: AK5574 AVDD 4.75-5.25 V; AK4458 AVDD 3.0-5.5 V; both TVDD 3.0-3.6 V.** AK4458 VREFH/VREFL are per channel-pair and tie to AVDD/AVSS | AK5574 p.5; AK4458 p.9. **At AVDD = 5 V the T1-11 full-scale formula gives exactly 2.8 Vpp** — the 13.2 dB gain figure stands |
| T1-50 | **I2C-mode straps, complete:** AK5574 `I2C` (42) = H **and `PSN` (41) = L**; AK4458 `I2C` (17) = H **and `PS` (16) = L**. On both, the second pin high selects **parallel** mode. Addresses: AK5574 `CAD0_I2C` (32) / `CAD1` (34); AK4458 `CAD0_I2C` (15) / `CAD1` (12) | Both pin tables, rendered. **Refines T1-27** — the AK5574's PSN requirement was not previously recorded |
| T1-51 | **AK5574 `MSN` (24) is a hardware master/slave select**, and `TEST` (15) has a 100 kOhm internal pull-down. `PDN` (20): L = reset/power-down. AK4458 `PDN` (48): L = power-down, registers reset to default | Both pin tables |
| T1-52 | **AK4458 "Handling of Unused Pin" is explicit and counter-intuitive:** unused analog outputs (`AOUTL/Rn P/N`) **must be OPEN**; `DZF` must be open; unused `SDTI1-4`, `DSDR3`, `DSDL4`, `DSDR4` **must be connected to DVSS** | AK4458 p.9. **Directly binding on this design** — T1-D08 reserves slots 7-8 on each DAC, so the AOUT4 pairs are unused and **must be left open, not grounded** |
| T1-53 | **AK5574 pin 30 `OVF` is an analog-input overflow flag output** | AK5574 p.5. Drives **F29** |
| T1-42 | **ADAU1466 S/PDIF receiver lock range: 18 kHz to 192 kHz.** Clock recovery is "completely digital". Ports designed to meet AES/EBU jitter of 0.25 UI p-p at ≥8 kHz and 10 UI p-p below 200 Hz | `adau1462-1466.pdf` pp. 74-75, rendered. Closes V-19 condition 1 |
| T1-43 | **Integrated S/PDIF RX is ASRC-coupled on-die:** "because the S/PDIF input data is most likely asynchronous to the DSP core, **it must be routed through an ASRC**". No serial port and no external recovered-clock net involved. 16 ASRC channels in 8 stereo sets; we need 2 | p.74, rendered. Closes V-19 condition 2 |
| T1-44 | **Pins 4/5 are dedicated `SPDIFIN`/`SPDIFOUT`** with no alternate/multipurpose functions and no current assignment — no conflict. RX input is a comparator centred at IOVDD/2 requiring **≥200 mV p-p**, accepting TTL or bipolar, and **requiring an AC coupling capacitor on the pin** | Table 18 + p.74. Closes V-19 condition 3 |
| T1-45 | **Integrated S/PDIF TX outputs two channels directly from the core at core rate** and **consumes no serial output port**; non-audio bits copyable from the RX or programmed. Auxiliary Output Mode (metadata onto TDM8) exists but is optional and unused. Interface meets **consumer** S/PDIF, **not AES3 professional** | p.75, rendered. Retires the WM8804 stuffing option |
| T1-46 | **S/PDIF status registers:** `SPDIF_LOCK_DET` 0xF600, `SPDIF_RX_CTRL` 0xF601, `SPDIF_RESTART` 0xF604, `SPDIF_LOSS_OF_LOCK` 0xF605, plus channel-status / user-data / validity / parity blocks 0xF610-0xF68B. `ASRC_LOCK` 0xF580, `ASRC_MUTE` 0xF581, per-ASRC ratio 0xF582-0xF589 | p.74-75. Makes §12's SPDIF-lock criterion a register poll (M3) |
| T1-41 | **Pin 3 `VDRIVE` disposition is explicit:** "If an external supply is provided directly to DVDD, **connect the VDRIVE pin to ground**." Recommended PNP, if ever used, is ON Semi NSS1C300ET4G | Table 18 p.18. **Closes the F18 loose end** — VDRIVE goes to GND, not left floating |
| T1-15 | **analog.com is unreachable from this environment** — ADAU1466 and LT3045 PDFs and the HTML product page all timed out via `Invoke-WebRequest`, `curl` and `WebFetch`; Verical 403 | Four independent fetch attempts, 2026-08-15 |
| T1-71 | **LT3045 PSRR vs input-to-output differential, the criterion-(a) number.** At **2 V headroom: 100 kHz ≈ 77 dB, 500 kHz ≈ 72 dB, 1 MHz ≈ 70 dB, 2 MHz ≈ 84 dB.** At 1.5 V: 74 / 63 / 62 / 84 dB. **The curve has a notch at 500 kHz–1 MHz and recovers by 2 MHz** — the part is *better* at 2 MHz than at half that. Below ~1 V headroom every curve collapses | Curve G45 p.10 cropped to 400 dpi and read, `LT3045.pdf` Rev. D. Conditions on the figure: I<sub>L</sub> = 500 mA, R<sub>SET</sub> 30.1k, C<sub>OUT</sub> 10 µF, C<sub>SET</sub> 0.47 µF |
| T1-72 | **LT3045 audio-band PSRR and noise.** G41: with C<sub>SET</sub> = 4.7 µF, PSRR ≈ 98 dB at 10 Hz, peaks ~117 dB near 200 Hz, ~110 dB at 1 kHz, still ≈ 80 dB at 200 kHz. G46/G48: **integrated output noise is 0.8 µV<sub>RMS</sub> (10 Hz–100 kHz), flat across 0–500 mA load and flat across output voltage to 15 V** | Curves G41 p.9, G46/G48 p.10, rendered at 175 dpi |
| T1-73 | **LT3045's output side is a 16 V part.** Abs max **OUT, OUTS and SET pins = −0.3 V / 16 V**; electricals specified over **0 V < V<sub>OUT</sub> < 15 V**. IN pin ±22 V. Dropout **260 mV typ at 500 mA**. θ<sub>JA</sub> = 33 °C/W (DFN-12) | `LT3045.pdf` Rev. D abs-max block + electrical table. **At 13.5 V this is the closest to a ceiling any LT3045 on this board runs** — the other five sit at 3.3–5 V |
| T1-74 | **LM61460-Q1 abs max V<sub>IN</sub> = 42 V; recommended operating 3–36 V.** Also abs max: BIAS 16 V, FB 16 V, PGOOD 20 V, PGND-to-AGND ±0.3 V DC. Output range for the adjustable version **1 V to 0.95 × V<sub>IN</sub>**; f<sub>SW</sub> 200–2200 kHz | `LM61460-Q1_TI.pdf` §8.1/§8.3. **Decides F39** — an inverting buck-boost stresses the IC at V<sub>IN</sub> + \|V<sub>OUT</sub>\|, so this rail cannot sit on VBATT_PROT |
| T1-75 | **LM5156-Q1: 3.5–60 V operating, 65 V abs max, AEC-Q100 grade 1, WSON-12 3×2 mm, external FET.** V<sub>REF</sub> = **1.000 V ±1 %** — the same reference as the LM61460, so the divider helper is reused unchanged. RT = 9.09 kΩ → **2200 kHz (1980 min / 2420 max)**; RT = 220 kΩ → 100 kHz. t<sub>ON(MIN)</sub> = 50 ns at 2.2 MHz; D<sub>MAX</sub> = 80 % min / 85 % typ | `LM5156-Q1_TI.pdf` SNVSBI7B Rev. B, features + electrical table |
| T1-76 | **LM5156-Q1 dual random spread spectrum: triangular modulation runs at 0.156 × f<sub>SW</sub>**, and *"the frequency of the triangular modulation is further modulated randomly **to reduce the likelihood of any audible tones**."* Selectable live via `DITHOFF` — grounded enables dither, tied to VCC disables it | §9.3.5 + Figure 9-10. **The deviation percentage is not specified anywhere in the datasheet** — see V-26 |
| T1-77 | **TI states the boost pass-through problem in its own words:** *"Boost converters have a natural pass-through path from the supply to the load through the high-side power diode (D1). Because of this path and the minimum on-time limitation of the device, boost converters cannot provide current limit protection when the output voltage is close to or less than the input supply voltage."* | `LM5156-Q1_TI.pdf` §9.3.8. **This is the citation under F39's rejection of a plain boost** — not our inference |
| T1-78 | **The eliminated candidates, each by a number in its own datasheet.** LM5155-Q1: 45 V operating / 50 V transient. LM5157-Q1: **integrated 50 V** switch. TPS55340-Q1: 2.9–38 V in, **40 V** switch, f<sub>SW</sub> to 2.5 MHz. LM5175-Q1 (4-switch buck-boost, one plain inductor): **operating frequency range 100–600 kHz, full stop** | The four datasheets, now held. LM5175's range lands squarely in T1-71's PSRR notch |
| T1-103 | **AK5574 Figure 76, "Input Buffer Example 1" — AKM's own recommended circuit, read at figure level, and it settles F50's shape.** Structure: input buffer on **±15 V** (NJM5534) → **68 µF AC COUPLING** → a **single-supply +5 V second stage** whose non-inverting input sits on a **Bias node**, gain 620/3300 = **−14.5 dB** → **10 Ω series + 100 pF to ground at each ADC pin**, plus **15 nF differential across the pair**. Film capacitors specified for the 15 nF and 1 nF. Stated performance: DR 121 dB, S/(N+D) 112 dB at 48 kHz | `AK5574_AKM.pdf` p.67, rendered. **The bias divider is 10 kΩ / 10.5 kΩ from VA — i.e. 0.51220 × AVDD, dead centre of the 0.502–0.522 window — and it is UNBUFFERED, decoupled with 10 µF ∥ 0.1 µF** |
| T1-124 | **OPA2320 stability is NOT a table value.** `PM Phase margin, V_S = 5 V, **C_L = 50 pF: 47°**` and `C_L Capacitive load drive: **"See Typical Characteristics"**`. **Our load is 100 pF — 2× the characterised condition** — before the 10 Ω isolation resistor is credited, and 47° at half the load is already modest. Also `THD+N 0.0005 % at G = 1, 4 V_PP, 10 kHz, R_L = 10 kΩ`, and `0.0011 % at R_L = 600 Ω` | TI SBOS513F, table read (adversary 008, verified independently). **G = 1 is exactly leg P's configuration**, so the THD+N figure is directly applicable rather than inferred — but its **R_L = 10 kΩ is not our load**: the AK5574 presents 3.0/3.6/4.2 kΩ (T1-115), and interpolating the two stated loads lands near **0.0007 % (−103 dB)**, still 12.5 dB inside §12's −90.5 dB line |
| T1-136 | **SiT1605 closes F56's duty blocker, and the temperature axis — which the reviewer did not check — clears too.** **Table 1, p.2, rendered 210 dpi:** **Duty Cycle `DC` min 48 / max 52 %, condition “All Vdd levels”** — a guaranteed base-table limit, **not an order-code option and not a typ**. Also: Tr/Tf 2.3 ns max · **`Z_in` pull-down min 2 MΩ on pin 1 (OE or /ST or NC)** · **`T_start` 0.5 typ / 0.7 ms max** · **`PSNS` 0.8 ps/mV** at 50 mV pk-pk on 3.3 V · RMS phase jitter **0.45 typ / 0.700 ps max** (12 kHz–20 MHz). **Operating temperature −40…+85 °C, Industrial — and it is the ONLY temperature option in the ordering table**, so there is no ASDMB-style wrong-default trap. 24.576 MHz is on the supported-frequency list | **Rendered, and the temperature/frequency axes checked HERE because 034 verified only the duty number.** F56 has **two** criteria and the last candidate died on the second one. **All three now clear:** duty 48/52 against the AK5574's 45–55 · −40…+85 covering the −20…+70 decree at both ends · 24.576 MHz available. **Jitter is 10× inside the 7.09 ps budget on the max figure alone**, so §3's *low-jitter XO* wording is satisfied as written and F56's close does not depend on the pending rewording |
| T1-135 | **ADAU1466 PLL loop filter, and our operating point is ADI's stated DESIGN CENTRE, not an extrapolation from it.** **Figure 16 “PLL Filter”, Rev. C p.30, rendered 200 dpi:** two parallel paths between **PVDD (pin 15)** and **PLLFILT (pin 16)** — **150 pF direct**, and **5.6 nF in series with 4.3 kΩ**. **IT RETURNS TO PVDD, NOT TO GROUND.** Same page's table: **MCLK 24.576 MHz → predivider 8 → PLL input 3.072 MHz → feedback ×96 → 294.912 MHz**; the text specifies the filter *“for a nominal 3.072 MHz PLL input and a 294.912 MHz system clock output”* — **exactly our numbers** — and adds *“this filter works for the full frequency range of the PLL.”* **Tolerance is specified:** *“valued within 10 % of the recommended component values and with a **15 % or lower tolerance**”*. **PLLFILT bias is internally generated, “typically between 1.65 V and 2.10 V”.** **Layout, p.197 verbatim:** *“To minimize jitter, connect the single resistor and two capacitors in the PLL filter to the PLLFILT and PVDD pins with **short traces**.”* | **Rendered, not extracted — the layout figure's extraction interleaved the four values into an unreadable run.** **Drawn 2026-08-20 as C60/C61/R60 on `02_dsp`.** ADI gives **one** network plus a tolerance rule, so this is a **verbatim adoption**, not a design — the library policy's *“vendor part verbatim where one exists”* applied to a circuit rather than a footprint. **The p.197 sentence is a Block D/E input** and it is a *jitter* argument, so it outranks tidiness at placement time |
| T1-134 | **DN2540 ships ONLY in three-lead packages — `3-lead TO-92 · 3-lead SOT-89 · 3-lead TO-220` (DS20006717, package list).** All single devices, so **the “revisit DN2540” escape from F61 does not exist** and the shunt is 24 packages regardless of which depletion FET wins | **Adversary 031, verified here.** **Its real value is record hygiene: V-16 and F61 have been travelling together and are INDEPENDENT.** DN2540-vs-LND150 is a choice about R<sub>DS(on)</sub>, C<sub>oss</sub> and the transient window; *how many packages the shunt needs* is settled by §6.4's pair requirement and is identical either way. **Separated in the record** |
| T1-133 | **BAV99 is three parts and four qualification suffixes in ONE datasheet, and the spread inside the family dwarfs the vendor question.** Diotec, 2025-11-18: **`-C` commercial · no suffix INDUSTRIAL · `-Q` AEC-Q101 *compliant* · `-AQ` AEC-Q101 *qualified*.** `BAV99` 85 V, I_R **30 nA @ 25 °C → 30 µA @ 150 °C** (1000×); **`BAV199` 5 nA → 80 nA** (16×); `BAV99L` 100 V. **The low-leakage part is NOT offered in the qualified suffix** | **Adversary 029. THE PINNED PART HAS NO SUFFIX — it is the INDUSTRIAL grade on a board where every other suffixed part is `-Q1`.** Not a specification failure; a **consistency** failure that surfaces at qualification review rather than bring-up. **Their node-impedance inference CONFIRMED WITH A CORRECTION IN THE SAFE DIRECTION:** they assumed ~10 kΩ from `Rtop`; the input clamps actually sit on the divider node at **Rtop ∥ Rbot = 4.58 kΩ**, so the 105 °C offset is **~11 mV, not ~25 mV**. And the level-shift clamps (`D409+`) sit at the op-amp **inverting node — a virtual earth**, where feedback absorbs the leakage and it appears only as I_leak × R_F ≈ **2.5 mV** referred to the output. **Their conclusion holds with roughly 2× more margin than they claimed** |
| T1-132 | **ONE SENTENCE GOVERNS EVERY MODE STRAP ON THE AK5574, and it moots two legs of strap work.** §“Operation Mode Control”, **p.56, verbatim:** *“Operation modes of the AK5574 are set by pins or registers. In parallel mode, the operation mode is set by pin and register settings are invalid … **In serial control mode, register settings are prioritized so that all pin settings except the MSN pin setting are ignored.**”* We run I2C — **serial control mode** | **Adversary 028; verified verbatim here.** **`DIF0`/`DIF1` ON PINS 37/38 ARE NOT READ BY THE PART.** So **F67's `00`→`11` and F69's `11`→`10` were BOTH FUNCTIONALLY INERT** — the line that changed twice, that triggered my working-rule-7 watch, and that I was told not to swing at a third time, **was never being read.** **`MSN` is the sole honoured pin, and it is the load-bearing one** — it selects slave mode, which is the mode in which F65's self-reset circuit exists at all. *Over-broad phrasing flagged, not resolved:* taken literally *“all”* would include `PDN` and `LDOE`, which cannot be true (`LDOE` has no register equivalent, `PDN` is the hardware reset); the safe reading scopes it to **operation-mode pins that have register equivalents**. Our `LDOE`/`PDN` dispositions stand either way |
| T1-131 | **AK4458 `FIR2-0` is RAIL-COUPLED, and `07H` carries a reserved `1` the datasheet never states a rule for.** *(a)* **p.50 verbatim:** *“This FIR filter attenuates out of band noise and may reduce degradation of the analog characteristics caused by a switching regulator, etc. **Best performance should be achieved by clean linear regulated AVDD/VREF power supplies and the default setting of the FIR2-0 bits. These conditions are included in the Analog Characteristics specs.**”* — so **the 115 dB we budget against is specified under TWO conditions at once**: a linear AVDD/VREF *and* `FIR2-0 = 000`. *(b)* **`07H` default byte is `0x03`, not `0x01`** — D1 is a fixed `1` alongside `SYNCE` at D0. *(c)* `SMUTE` default `0` confirmed | **Adversary 026; the p.50 quote and the missing-rule count verified here.** **(b)'s consequence lands on a write we will make: `SYNCE` lives in `07H`, so a blind `0x01` to ‘set SYNCE’ CLEARS D1.** And the sibling trap is in the DOCUMENTATION, not the silicon: **AK5574 Note 25 says *“The bits indicated as ‘0’ must contain a ‘0’ value”*; the AK4458 says nothing of the kind — `grep -c “bits indicated as”` returns **0** on the AK4458 and 1 on the AK5574.** So `D1 = 1` is documented as a *default* and nowhere as a *requirement*. **Rule for the firmware contract: read-modify-write `07H`, stated as a rule rather than left as an inference from a `1` in a bit-map cell.** *(c)* closes a constraint we had ASSERTED — the category this exchange keeps catching |
| T1-130 | **AK4458 register space CLOSED: 23 fields, bound by Note 35 (`“Data must not be written into addresses from 15H to 1FH”`) → writable `00H`–`14H`, 21 registers.** *2 defects* — **`RSTN` = `0` (boots held in reset)** and **`TDM1-0` = `00` Normal, against §4 [HARD] TDM8**. *2 pending* — `DIF2-0` (F70), filter group (F73). *11 correct* — `ACKS`, `DFS`, `DEM`, `ATT`=`FF` 0 dB, `INV`, `MONO`, `SELLR`, `PW`, `SDS`, `SYNCE`=`1`, `DP`. *5 inherited-not-chosen* — `SC1-0`, `ATS1-0`, **`FIR2-0`**, `DZFB`+zero-detect. *2 inert* (DSD, gated `DP=0`). *2 not read* — `SMUTE` default, `07H` D1's fixed `1` | **Adversary 024, keyed on fields per M26a. T2 on arrival; Table 16 and the group-delay arithmetic verified independently here, the remaining rows not yet re-derived.** **THE HEADLINE NUMBER FOR THE FIRMWARE CONTRACT: 11 of 23 fields are SPLIT across registers — over half — so *any constraint on this part that names one register is more likely wrong than right.* `FIR2-0` wants a second look: filter-adjacent, defaults `000`, and ABSENT FROM TABLE 31** — the same combination that hid `TDM1-0` |
| T1-129 | **AK4458 Table 31 “Function List”, p.73 — AKM ships a VENDOR-AUTHORED, FIELD-KEYED enumeration with the split registers named explicitly. It is the best KEY available and a FATAL completeness source.** 14 functions, each with plain-language default and address: `ATT7-0` **03-04H + 0F-14H** · `DIF2-0` **00H, default “32-bit MSB justified”** · `DEM3-0` **01H+0AH+0EH** · `SELLR1-4` **02H+05H+0DH** · `INVL/R1-4` **05H+0CH** · `MONO` **02H+0DH** · `SDS1/2` **0A-0BH** · **`SYNCE` 07H, default `Enable`** · plus PCM/DSD availability columns | **Rendered 190 dpi, PDF p.73** (*and the extraction's `- 72 -` footer belongs to the PREVIOUS page — **M23 caught in real time**; I rendered p.72 first and got I2C timing diagrams*). **THE DECISIVE PROPERTY IS WHAT IT OMITS: `TDM1-0` IS NOT IN IT. Nor `RSTN`, `ACKS`, `DFS`, `SC1-0`, `ATS1-0`, `DSDF`, `FIR`, `SSLOW`.** It is a *function* list, 14 entries against a **21-register** writable space — **and BOTH DAC-side defects found so far (`TDM1-0` wrong at `00`, `RSTN` booting held in reset) are ABSENT from it.** Using it as the enumeration yields a confident, complete-looking sweep that misses exactly the two things that are wrong |
| T1-128 | **AK5574 register space CLOSED, and the AK5574's own HPF corner.** *(a)* **Writable space is `00H`–`05H`, six registers** — Note 24: *“Data must not be written into addresses from ‘06H’ to ‘1FH’.”* That finite bound is what makes a completeness claim available at all. **N = 14 fields**, defaults verified: `03H` all-zero (TDM1-0 = 00), `04H` all-zero (DP/SD/SLOW = 0), `05H` all-zero (DCKS/PMOD/DCKB/DSDSEL = 0). *(b)* **Digital HPF corner is fixed 1.0 Hz at fs = 48 kHz** (Normal Speed): *“The cut-off frequency of the high-pass filter is fixed 1.0 Hz…”*, and it is *ignored* in OCT/HEX/DSD. *(c)* **AK4458 `SD` default = `1` = Short delay filter**, against the AK5574's `SD = 0` Normal Delay + `SLOW = 0` Sharp Roll-off | **Rendered 185 dpi p.63; text verbatim p.55-ish for the HPF; AK4458 p.75 text verbatim.** Independently reproduces adversary 020's sweep table exactly. **(b) converts `HPFE = 1` from inherited to CHOSEN**: 1.0 Hz is decades below anything audible and it cancels ADC DC offset ahead of DSP gain — a decision input that did not exist before |
| T1-127 | **AK4458 ACKS/DFS chain, resolved end to end — and the DEFAULTS ARE CORRECT, which is a read result and not an assumption.** *(a)* **`ACKS` = 0 = Manual is live for us.** The *“ACKS mode is enabled and fixed internally”* sentence adversary 018 found is scoped to **PARALLEL mode** (*“In parallel mode, the clock setting mode is always in auto setting mode…”*, p.68) — **we run serial/I2C, so the bit governs.** *(b)* **Table 2: `DFS2-0` = `000` = Normal Speed, 8 kHz–54 kHz (default).** 48 kHz is Normal Speed → **default correct.** *(c)* **Table 4 confirms 48.0 kHz @ 512fs = 24.5760 MHz** is a valid Manual-mode combination. *(d)* **The DR/S/N table, p.32 — and it settles ACKS on merit:** `ACKS 0` → **115 dB at 256/384/512/768fs**; `ACKS 1` → **112 dB at 256/384fs**, 115 dB at 512/768fs; prose: *“DR and S/N will degrade by approximately 3 dB”* | **Rendered 185 dpi p.31 (Tables 2/3/4); text read verbatim pp.30–32, doc 014011794-E-02.** **ACKS = 0 is UNCONDITIONALLY 115 dB while ACKS = 1 conditions the DR on the clock ratio** — so Manual is the right setting **for a reason**, not merely because it is the default. Both would give 115 dB at our 512fs, but Manual is robust to the ratio changing and Auto is not |
| T1-126 | **AK5574 CLOCK MODE POWERS UP WRONG FOR THIS BOARD, and it takes two figure reads to see it.** *(a)* **Register 02H `Control 1` default = `0 0 0 0 0 0 0 1`** — CKS3–0 = **0000**, DIF1–0 = 00, HPFE = 1. *(b)* **Table 5 `Clock Mode`, row CKS3–0 = 0000 with MSN = L: MCLK = 128fs, Quad Speed, 108 kHz < fs ≤ 216 kHz.** We supply **48 kHz LRCK and 24.576 MHz MCLK = 512fs, MSN = L (slave)** — so the default is wrong **twice over**: wrong ratio (128fs vs 512fs) *and* fs outside the mode's declared range. **The mode we need is CKS3–0 = `0110`** (L,H,H,L) → 512fs, Normal Speed, 8 kHz ≤ fs ≤ 54 kHz — i.e. **02H = 0x31** with default DIF/HPFE. **Note 26: “When the PDN pin is set to ‘L’, all registers are initialized to their default values”** — so *every* PDN cycle returns to the mismatched state | **Rendered 200 dpi, PDF pp.33 and 62** (doc 015016764-E-03, 2022/02). **Both reads were necessary and neither alone is sufficient:** the register default is meaningless without Table 5's decode, and Table 5 is meaningless without knowing where the bits start. **Extraction was actively misleading on both** — Table 5's rows interleave and 02H's default row scrambles. *Column alignment cross-checked against HPFE:* the prose says “HPF ON **(default)**” and D0 = 1 in the rendered table, which anchors the bit order independently |
| T1-125 | **`OPA2320S` is NOT the same package as `OPA2320`.** The shutdown section is headed *OPA2320S only* and the pin table gives **`SHDN A` = pin 5, `SHDN B` = pin 6** — which on a standard dual SOIC-8 are `+IN_B` and `−IN_B` | TI SBOS513F pin tables. **F52's standing claim that "every candidate ships on the standard dual SOIC-8" holds for the base part and FAILS for the S suffix**, so the placeholder's "footprint is T1" was only ever T1 for a PN not yet pinned. **The S suffix is exactly what a purchasing substitution reaches for** — F37/F38's suffix axis, third instance |
| T1-123 | **AK4458 Analog Output Phase Synchronization, verbatim:** *"This function synchronizes analog output phase by suppressing the phase difference of the AK4458 and other AKM devices with synchronization function to within **3/256fs**. Analog output phase synchronization function becomes valid when input data at all channels are continuously '0' for **8192 times** if **SYNCE** bit is set to '1' during operation in PCM mode, **or when RSTN bit is set to '0'**."* | p.67, rendered 200 dpi (adversary 007, their text read confirmed at figure level). **3/256 fs at 48 kHz = 244 ns.** Without SYNCE the datasheet bounds inter-device output phase **not at all** — see F62 |
| T1-122 | **AK5574 §11 Switching Characteristics, Master Clock Timing: f<sub>CLK</sub> 2.048–49.152 MHz, **d<sub>CLK</sub> duty cycle 45–55 %**. LRCK duty likewise 45–55 % | p.19, rendered 200 dpi. **This supersedes the ADAU1466's 25–75 % as the binding duty specification — the converter is 2.5× tighter**, and 25–75 % is cleared by every LVCMOS oscillator made while 45–55 % is a real spec some miss. F56's gate cited the wrong part |
| T2-20 | **LND150 SOT-23 (`LND150K1-G`) pin map, DERIVED from two figures rather than read from a table: 1 = GATE, 2 = DRAIN, 3 = SOURCE.** Page 5's package outline Top View numbers the leads — **1 near-edge left, 2 near-edge right, 3 alone on the far edge**. Page 1's pin-configuration photograph names them — the two near-edge leads are GATE (left) and DRAIN (right), with SOURCE alone at the rear. Both views are from above, so no mirroring applies | **T2 AND DELIBERATELY NOT T1.** The two figures are independent and consistent, which is stronger than either alone — but `CLAUDE.md` §7 requires a **pin-function table**, and this document has none (F60). One half of the derivation is a **photograph**, which is precisely what that rule distrusts. **Needs one independent confirmation before layout** — a distributor CAD model or Microchip's product page — because a wrong pin number is a respin ERC cannot catch |
| T1-121 | **TLP3475 pin assignment, figure level: 1 = Anode, 2 = Cathode, 3 = Drain, 4 = Drain.** The internal schematic shows the two photo-MOSFETs **source-to-source with the common node internal**, so both output pins are drains and the switch is inherently bidirectional. Also: **1-Form-A, normally open**; isolation **500 V<sub>rms</sub> min**; ON-state current 300 mA max; ERT 40 ps typ | §4 Packaging and Pin Assignment, rendered 200 dpi. **1-Form-A normally-open is §6.4 [HARD]'s fail-safe polarity satisfied by the part's own construction**, and the internal source-to-source pair is the same arrangement §6.4 demands of the *shunt* — the series element gets it for free |
| T1-120 | **LND150 (Supertex/Microchip), N-channel DEPLETION-mode DMOS:** BV<sub>DSX</sub>/BV<sub>DGX</sub> **500 V**, R<sub>DS(ON)</sub> **1.0 kΩ max**, I<sub>DSS</sub> **1.0 mA min**, V<sub>GS</sub> abs max **±20 V**, operating/storage **−55…+150 °C**. Packages: **SOT-23** (`LND150K1-G`), TO-92, **SOT-89** (`LND150N8-G`). Gate is ESD-protected | Supplied 2026-08-17, text read. **Note the I<sub>DSS</sub> discrepancy against the operator's verbal figure of "30 mA" — the datasheet says 1.0 mA MIN.** Ordinary transcription slip most likely, but it is the kind that matters: the shunt's conduction budget depends on it. **Pin numbering still needs a figure-level read** — three packages, three pinouts |
| T1-119 | **TLP3475 (Toshiba) Form-A photorelay, VSON4:** OFF-state output voltage **50 V min** · R<sub>ON</sub> **1.0 Ω typ / 1.5 Ω max** · **C<sub>OFF</sub> 12 pF typ / 20 pF max** (V = 0, f = 100 MHz) · I<sub>OFF</sub> 1 nA max at 50 V · trigger LED current **3 mA max** · recommended I<sub>F</sub> 5/7.5/20 mA, abs max 30 mA · **recommended operating temperature −20…+85 °C** | Supplied 2026-08-17, text read. **C<sub>OFF</sub> is V-14's whole point** — it is the nonlinear off-capacitance §12's CCIF twin-tone criterion exists to catch. **And the −20 °C low end sits EXACTLY on the §6 decree with zero margin**, the same shape as F55. **Pin numbering needs a figure-level read** before the symbol is trusted |
| T1-118 | **OPA2320 beats OPA2365 in the audio band, and the headline numbers say the opposite.** OPA2320 table states e<sub>n</sub> **8.5 nV/√Hz at 1 kHz and 7 at 10 kHz** — both given, no figure read needed → 1/f corner **≈ 470 Hz**. OPA2365's corner is **≈ 7.4 kHz** (T1-116). Integrated 20 Hz–20 kHz: **OPA2320 1.068 µV<sub>RMS</sub>** vs **OPA2365 1.197 µV<sub>RMS</sub>**. VCM rail-to-rail on both; OPA2320 I<sub>B</sub> ±0.9 pA max at 25 °C but **±50 pA max over −40…+85 °C** → 0.5 mV across R<sub>BP</sub>, still 100× inside the bias window | TI SBOS513F table read. **OPA2365 quotes 4.5 nV/√Hz and OPA2320 quotes 7 — and the part with the better headline is worse in-band, because the quoted frequencies differ (100 kHz vs 10 kHz) and the corners differ 15×.** This is F59's point made concrete |
| T1-117 | **NDK NZ2520SD operating temperature range = −10 to +60 °C** (overall tolerance ±20 ppm; symmetry 45–55 %; CMOS; 2.5×2.0 mm; the family's frequency table covers 20 ≤ F < 30 MHz at 4.5 mA on 3.3 V, so 24.576 MHz exists). Application line reads *"For wireless LAN"* | Datasheet supplied 2026-08-17, text read. **FAILS the §6 decree of −20…+70 °C AT BOTH ENDS** — see F56 |
| T1-116 | **OPA2365: VCM = (V−)−0.1 to (V+)+0.1 V** (true rail-to-rail input, CMRR 100 dB min over that whole range at −40…+125 °C) · **I<sub>B</sub> ±0.2 pA typ / ±10 pA max** · supply **2.2–5.5 V** · specified **−40…+125 °C** · GBW 50 MHz. **Noise: the table gives ONLY 4.5 nV/√Hz at f = 100 kHz** and 5 µV<sub>PP</sub> over 0.1–10 Hz — **no 1 kHz figure exists** | TI datasheet supplied 2026-08-17; VCM/I<sub>B</sub> table read, **noise read from Figure 7-14 at 200 dpi**. The curve runs ~110 nV/√Hz at 10 Hz, ~35 at 100 Hz, **~12–14 at 1 kHz**, ~6 at 10 kHz, 4.5 at 100 kHz — **a 1/f corner near 6–9 kHz.** Everything except noise clears F52's gate outright |
| T1-115 | **AK5574 p.9, figure read:** **Interchannel Isolation 110 dB min / 120 typ**, and its condition is stated in the parameter name — ***(AIN1⇔AIN2, AIN3⇔AIN4)***, i.e. **within a pair, not across all four**. **Interchannel Gain Mismatch: — / 0 typ / 0.5 dB MAX.** PSRR 60 dB typ. AVDD+VREFH1/2 current 49 typ / 64 max mA | Rendered 200 dpi. **The gain-mismatch figure is what demotes the resistor-tolerance gain argument (C4): the converter's own 0.5 dB max is ~4× our 0.13 dB at 1 % parts.** The isolation figure's *pairing condition* is a third instance of M20's conditions clause — the number is not "110 dB between any two channels" |
| T1-114 | **LMK1C1104 at VDD = 3.3 V: R<sub>OUT</sub> = 50 Ω typ**; output-output skew 25 ps typ / 50 ps max; part-to-part skew 250 ps; propagation delay 1.5/2 ns; **additive jitter 8 fs typ / 20 fs max** | TI SNAS791D, table. **Read the jitter figure's CONDITIONS with it (M10):** it is specified at **f<sub>IN</sub> = 156.25 MHz, 2 V/ns input slew, 12 kHz–20 MHz integration** — none of which is our operating point at 24.576 MHz. T1-30 recorded "7.5 fs"; the table says 8/20. **Neither number is quotable bare**, and the tree's jitter claim rests on the XO (F56), not on the buffer |
| T1-113 | **ADAU1466 MCLK input, Rev. C p.29:** f<sub>MCLK</sub> **2.375–36 MHz**, t<sub>MCLK</sub> 27.8–421 ns, **duty cycle 25–75 %**, high/low width 0.25–0.75 × t<sub>MCLK</sub>. Pin 21 accepts a clock **directly**; pin 22 XTALOUT is for a crystal we do not fit. p.24: *"the crystal oscillator circuit must provide a stable master clock to the XTALIN/MCLK pin by the time the PVDD supply reaches its nominal level"*, the pin is gated internally until the DVDD POR and PVDD→DVDD level shifter initialise, and boot consumes **eight MCLK cycles** | **CITATION CORRECTED 2026-08-17 (adversary 010, verified independently): the duty spec is on p.9, Table 6 — NOT p.29.** Whole-document audit: `“MCLK duty cycle”` occurs **exactly once in 202 pages**, PDF p.9, whose own footer reads *Rev. C | Page 9 of 202* (so PDF page = printed page, no offset). p.24 is INITIALIZATION/Power-Up Sequence; p.29 is Example PLL Settings, Table 20. **The VALUES were right and are unchanged; the CITATION was wrong.** **The duty-cycle window is the real XO selection constraint and a jitter-only spec does not cover it.** **And the PVDD sentence is conditioned on "when a crystal is in use"** — we drive the pin externally, so it is the vendor's statement of intent rather than a spec binding our configuration. Recorded with its condition rather than quoted bare |
| T1-112 | **AK5574 Absolute Maximum Ratings, p.8:** `IIN` (any pin except supplies) **10 mA max**; `VINA` −0.3 to **AVDD+0.3 V**. **And the ambient rating is CONDITIONAL ON THE BACK TAB:** **−40…+105 °C when the back tab is connected to VSS, −40…+70 °C when the back tab is open** | p.8, `pdftotext -layout`. **The IIN figure is what makes NOTE9's no-clamp deletion defensible against a stated limit rather than against an absent quantity** (adversary 004). **The tab condition is a finding in its own right — see F55** |
| T1-111 | **The AK5574's full-scale spread IS part-to-part, and one word settles it.** Recommended Operating Conditions gives **VREFH1-2 = 4.75 / 5.0 / 5.25 V**, and **Note 9** carries the scaling formula: ***"Vin (typ, @ 0dB) = ±2.8 × {(VREFH) − (VREFL)} / 5 [V]."*** | p.8, **rendered 200 dpi**, corroborated against the p.9 table (T1-109). **Citation corrected from "Note 11" (adversary 004, confirmed at figure level):** p.8's notes run 6–9 and stop; the formula is Note 9's continuation. The *table row* does read "Voltage Reference (Note 11)", but Note 11 is on p.9 and is the PSRR note — a forward reference that does not resolve on its own page. **The first read took the row's marker for the note's number**, which is M20's shape again: a citation is a third separate read from values and structure. **The discriminator is the word `typ` INSIDE the formula:** a formula that yields the *typ* value cannot also be what generates the min/max columns. So Note 11 tells you how the typ **scales with VREFH**, while the ±2.7/2.8/2.9 column is the **spread across parts at a given VREFH** — evaluated at the table's own stated condition, AVDD = 5.0 V. Note 8 independently caps VREFH at AVDD + 0.1 V, so 5.25 V is not even reachable under that condition and cannot be the source of the 2.9 max. **The two effects stack:** ±3.6 % part spread × the +5V_A rail's own ~±1 % → worst-case FS = **2.673 Vpp = 0.9450 V<sub>rms</sub>**. Against the pre-F54 design point of 0.9433 that is **99.8 % — at clip.** F54 was right and, if anything, under-corrected; the new point sits at **96.1 %** |
| T1-109 | **AK5574 Analog Characteristics, read at figure level 2026-08-16 — the columns matter and two of them were being quoted wrong.** **Input Voltage ±2.7 / 2.8 / 2.9 Vpp** min/typ/max (→ F54). **S/(N+D)** at fs = 48 kHz, −1 dBFS: **min 100, typ 112 dB**. **Dynamic Range (−60 dBFS A-wtd) and S/N (A-wtd), Not-Sum mode: min 117, typ 121 dB** | p.9, rendered at 200 dpi. **The 112 dB figure is measured at −1 dBFS and INCLUDES DISTORTION** — setting a noise budget against it compares a noise number to a noise-plus-distortion one, which is what `06_analog_in`'s first pass did. **The noise number is DR/(S/N): 121 typ, 117 min.** Correct framing: the front end's 111.8 dB SNR sits **~5 dB above the converter's own min floor**, so **the attenuator and INA1650 set this path's noise and the ADC is nowhere near the limit** |
| T1-110 | **AK5574 analog input resistance = 3.0 / 3.6 / 4.2 kΩ** min/typ/max (doubled in DSD 64fs mode) | Same table. The switched-cap input's equivalent resistance. **Not a defect for our drive** — the 10 Ω series against 3.6 kΩ is −0.024 dB, and the noise is inside the ADC's own specified DR — but it is a real load and it is now on the record rather than assumed to be infinite |
| T1-105 | **AK5574 full scale is 2.8 Vpp DIFFERENTIAL, and Note 10 says so in as many words:** *"This value is (AINnP)−(AINnN) that the ADC output becomes full-scale (n=1-4). Vin = 0.56 × (VREFHm−VREFLm) [Vpp]."* Spec table: 2.7 / **2.8** / 2.9 Vpp | p.9, rendered. **Checked because Figure 76 labels "2.8 Vpp" beside *each* ADC pin, which would imply 5.6 Vpp differential and put `06_analog_in`'s whole gain plan 6 dB out.** It reconciles: 14.9 Vpp differential in, ÷2 per leg, ×0.1879, ×2 back to differential = 2.80 Vpp. The figure's annotation is loose; Note 10 is normative. **The anchor holds and the gain plan is unchanged** |
| T1-106 | **Figure 76 drives BOTH ADC pins, antiphase, from two INVERTING stages** — one per leg of an already-differential source, each with `Bias` on its **non-inverting** input. So **AKM's bias node carries no signal current at all**, which is the property that lets it be an unbuffered divider | p.67, rendered at 200 dpi. **This is the structural fact the recorded T1-103 did not carry**, and it decides the AIN_N gap: the ADC is driven differentially, not single-ended |
| T1-107 | **OPA1656 VCM range is (V−) to (V+) − 2.25 V.** On a +5 V single supply that is **0 to 2.75 V**. Rail-to-rail *output* to 250 mV; supply 4.5–36 V; e<sub>n</sub> **4.3 nV/√Hz at 1 kHz** (2.9 at 10 kHz); I<sub>B</sub> 10 pA | TI SBOS901C, spec table. **This is the number behind the operator's "not an OPA1656" rider** — it clears the 2.561 V bias point by 189 mV but **fails the +5V_A follower's signal peak of 3.228 V by 478 mV** |
| T1-108 | **INA1650 output voltage noise = 1.56 µV<sub>RMS</sub>, 20 Hz–20 kHz, C<sub>MID</sub> = 1 µF** → 11.0 nV/√Hz flat-equivalent | TI SBOS818B spec table. **The front-end noise anchor.** With the attenuator's 4.72 kΩ per-leg Thévenin (12.5 nV/√Hz differential) the receiver output is **16.6 nV/√Hz → 112.1 dB SNR**, within a decibel of the AK5574's own 112 dB S/(N+D) — so neither dominates, and the level-shift stage's budget is tight by arithmetic rather than by preference |
| T1-104 | **The 2.5 V bias is the OLD circuit and it costs ~6 dB.** *"For products with Date Code XXXXHXX, AKM recommends Figure 76 as the revised circuit example, which adjusts the optimal input bias voltage… In case the original circuit example is used featuring input bias voltage of 2.5 V (Typ.), S/(N+D) performance will be degrade ~6 dB."* The 10.5 kΩ leg **is** the revision | Same page. **This is an F38/date-code axis nobody had considered: the correct bias depends on when the part was manufactured** |
| T1-99 | **F31 CLOSES on the datasheet's own words.** Pin 23 `BAT_IN`: *"Power supply input; voltage range: 3.2V to 4.2V. **Source can either be a Li-ion battery or any other power rail on the host board.**"* A direct rail feed with no battery and no charger path is **blessed, not tolerated**. `ADAP_IN` (22) is the 5 V charger input and its own description permits floating | BM83 DS70005402G Table 2-2 p.13 + §5.1 |
| T1-100 | **BM83 current, Table 9-12:** A2DP 12.05 mA (iOS) / 12.32 mA (Android) · SCO/eSCO 14.1 mA · **continuous TX 59 mA worst (modulation off, PL0)** · continuous RX 49 mA · standby 2.81 µA. Charger draws 3–4.5 mA and is unused | §9. **Against the AP2127's 300 mA: 5× margin**, and the LDO dissipates 84 mW. §7.1's 100 mA estimate was conservative by ~1.7× — left in place, but recorded so a cost pass cannot "discover" the headroom |
| T1-101 | **Host-mode interface is FOUR wires, not three** (Figure 6-8 §6.6): MCU `UART_TX`→`UART_RXD`, `UART_RX`←`UART_TXD`, **`BT_WAKE_UP`→`MFB`**, and **`MCU_WAKE_UP`←`P0_0`**. *"An external MCU can control the BM83 module over the UART interface and wake up the module with the MFB and P0_0 pins"* | §6.6. **Drawing this sheet is what revealed 03_control was one net short** — `P0_0` had no GPIO |
| T1-102 | **ESP32-S3-WROOM-1 footnote c is R16V-ONLY:** *"For modules embedded with ESP32-S3R16V, as the VDD_SPI voltage … is set to 1.8 V, the working voltage for GPIO47 and GPIO48 is also 1.8 V."* On the **N8R2 these are ordinary 3.3 V GPIOs** | Datasheet p.12 footnote c. **Same variant-conditional shape as footnote b** — two footnotes, both reservations that apply to variants we are not buying, both reasons the PN is pinned. IO48 now carries `BM83_TX_IND`, IO47 `BM83_RST_N_MCU` |
| T1-98 | **V-30 CLOSED — USBLC6-2SC6 SOT-23-6 pin map confirmed against ST's own document:** `1 = I/O1 · 2 = GND · 3 = I/O2 · 4 = I/O2 · 5 = VBUS · 6 = I/O1`. Pins 1/6 and 3/4 are one node each; GND and VBUS are the only orientation-bearing pins | `usblc6-2.pdf` (ST Doc ID 11265) p.1 pin diagram. **The KiCad parent symbol's map was right** — T2 → T1 with no change to the drawn sheet |
| T1-93 | **TPS62823 f<sub>SW</sub> = 2.2 MHz typ**, and *"as the load current decreases, the converter enters PSM, reducing the switching frequency."* | `TPS62823_TI.pdf` Rev. C §8.5 + §9.3. Aligns +1V2_CORE with the other four stages, **and the PSM note is a named instance of V-27's pulse-skip class — this part documents that it skips, where the LM5156/LM61460 only say they can** |
| T1-94 | **ESP32-S3-WROOM-1 module pin table, all 41 pins extracted** — 1/40 GND, 2 3V3, 3 EN, 41 EPAD(GND), and IO4/5/6/7/15/16/17/18/8/19/20/3/46/9/10/11/12/13/14/21/47/48/45/0/35/36/37/38/39/40/41/42/RXD0(44)/TXD0(43)/2/1 on pins 4–39. **The stock `RF_Module:ESP32-S3-WROOM-1` symbol is self-contained (no extends), 41 pins, and matches** — its pins 13/14 are named `USB_D-`/`USB_D+`, i.e. the [HARD] reservation is pre-encoded | Datasheet Table 3 pp.10–12, parsed as rows and spot-checked against the symbol. Five rows needed a second pass (line-wrapped) — **recovered rather than assumed**, which is the whole point of counting them |
| T1-95 | **F13(a) CLOSES: IO35/36/37 are free on the N8R2.** *"For modules with Octal SPI PSRAM, i.e. modules embedded with ESP32-S3R8 or ESP32-S3R16V, pins IO35, IO36 and IO37 are connected to the Octal SPI PSRAM and are not available for other uses."* **N8R2 is quad PSRAM**, so the reservation does not apply | Datasheet p.12 footnote b. **This is the F38 pinned-PN rule with teeth** — three power-good sense lines now sit on those pins, so an R8/R16V substitution shorts them into the PSRAM bus |
| T1-96 | **Strapping-pin defaults, Table 4-1:** GPIO0 **weak pull-up (1)** · GPIO3 **FLOATING (no default)** · GPIO45 weak pull-down (0) · GPIO46 weak pull-down (0). Strapping set: **GPIO0, GPIO3, GPIO45, GPIO46**; latched at reset and unchangeable until power-down | Datasheet §4 + Table 4-1. **GPIO3 is the one with no internal default at all**, so it is the one that cannot be left to chance |
| T1-97 | **AP2127 adjustable: V<sub>REF</sub> = 0.8 V, min 0.784 / max 0.816 (±2 %)**, V<sub>OUT</sub> = V<sub>REF</sub>(1 + R1/R2), 300 mA, and a feed-forward cap is datasheet-recommended for noise and stability. Ordering code: **`K` = SOT-23-5, `ADJ` = adjustable** | `AP2127_Diodes.pdf` §Adjustable Operation + electrical table. **Closes V-23 and F36** |
| T1-90 | **V-28 CLOSED — `SM8S24AHM3` is electrically IDENTICAL to the NRND `SM8S24A` on every figure this design uses.** V<sub>WM</sub> 24.0 V · V<sub>BR</sub> 26.7/28.1/29.5 V · I<sub>PPM</sub> **170 A** · V<sub>C</sub> **38.9 V** · α<sub>T</sub> 0.087 %/°C · R<sub>θJA</sub> 55, R<sub>θJM</sub> 0.35 °C/W · P<sub>D</sub> 8 W · I<sub>FSM</sub> 700 A. Family now runs to **85 V** standoff. **`P_PPM` 6600 W (10/1000 µs) and 5200 W (10/10 000 µs) are BOTH listed for the same UNIDIRECTIONAL part** | Vishay **doc 98647, rev. 14-Oct-2025**, pp.1–2 rendered. **Settles the three-way reading: the two-waveform interpretation is correct and the uni-vs-bi one is wrong.** The distributor's 43 V/153 A is not reproducible from the table — **43 V is the *standoff* of SM8S43AHM3**, a mis-mapped field |
| T1-91 | **Package designation changed DO-218AB → DO-218AC, and the land pattern did NOT change.** Mounting pad **15.30 × 10.70 mm** (main 9.80 × 10.70, lead 2.15 × 2.60, gap 3.35), body 13.3–13.7 × 8.3–8.7 mm, height 4.7–5.0 mm — the same drawing. AC adds a **0.10 mm nominal standoff** dimension. Heatsink is still the **anode** | Doc 98647 p.5 rendered, compared against doc 88387 p.5. **No footprint rework**, and the Block E pad note stands unchanged |
| T1-92 | **vishay.com IS reachable from this environment.** The shortlink form `https://www.vishay.com/doc?NNNNN` resolves server-side to the current revision and returns a PDF. It also **returned a different, newer file for doc 88387 than the held copy** — same content, but with a text layer the held copy lacks | Direct fetch, HTTP 200, `application/pdf`, final URL `docs/88387/sm8s.pdf`. **Retracts the standing "vishay.com refused this environment" claim** — see the ledger entry |
| T1-86 | **SM8S24A confirmed at figure level — and it promotes the three-distributor T2 to T1.** V<sub>WM</sub> **24.0 V** · V<sub>BR</sub> **26.7 / 28.1 / 29.5 V** at I<sub>T</sub> = 5 mA · V<sub>C</sub> **38.9 V at I<sub>PPM</sub> = 170 A** · leakage 10 µA at 25 °C but **150 µA at T<sub>J</sub> = 175 °C** · α<sub>T</sub> **0.087 %/°C**. Package **DO-218AC** *(corrected 2026-08-20, F87 — was DO-218AB, the SUPERSEDED doc 88387's designation)*, P<sub>PPM</sub> **6600 W (10/1000 µs) / 5200 W (10/10 000 µs)**, P<sub>D</sub> 8 W on infinite heatsink, I<sub>FSM</sub> **700 A** (8.3 ms), T<sub>J</sub> max 175 °C, AEC-Q101, **unidirectional only**, **heatsink tab is the ANODE**. R<sub>θJA</sub> 55 °C/W, **R<sub>θJM</sub> 0.35 °C/W** | `sm8s.pdf` (Vishay 88387, rev. 06-Feb-2026) pp.1–2, **rendered** — the file has no text layer at all, so this is a figure-level read by necessity as well as by policy |
| T1-87 | **The derived number that actually governs: dynamic resistance r<sub>d</sub> = (V<sub>C</sub> − V<sub>BR,nom</sub>)/I<sub>PPM</sub> = (38.9 − 28.1)/170 = 63.5 mΩ.** At the currents this circuit sees, the clamp is **28.9 V at 12 A, 29.7 V at 25 A, 31.1 V at 48 A** (25 °C), rising to **34.2 V at 48 A / 150 °C** once V<sub>BR</sub> is scaled by α<sub>T</sub>. The 38.9 V headline is the clamp at a current this design never reaches | Derived from T1-86. **Drives M10** — quoting 38.9 V outside its test condition and adding tempco gives 44 V and condemns a sound design |
| T1-88 | **ISO 7637-2 pulse 5 for 14 V powertrains, from the vendor's own table:** V<sub>TOTAL</sub> **78.5–100.5 V**, U<sub>S</sub> **65–87 V**, V<sub>A</sub> 13.5 V, **R<sub>i</sub> 0.5–4.0 Ω**, **t<sub>d</sub> 400 ms**, 1 cycle. JASO A-1 alongside it at 70–88 V / 0.8–1.0 Ω / 200 ms | `tvs.pdf` (Vishay 88490) Table 1. **Corrects the working assumption**: the 35 V figure used earlier is the *suppressed* level, not pulse 5 itself |
| T1-89 | **DO-218AC land pattern — IDENTICAL to AB's, which is why the label error was harmless (T1-91): 15.30 × 10.70 mm overall** — main pad 9.80 × 10.70 mm, lead pad 2.15 × 2.60 mm, gap 3.35 mm. Body 13.3–13.7 × 8.3–8.7 mm, height **5.0 mm max**, IPC-7351. **Does not stuff on an SMC land** | `sm8s.pdf` p.5, rendered. **Block E input** — and since the tab is the anode (ground), R<sub>θJM</sub> = 0.35 °C/W is only as good as the copper poured under it |
| T1-80 | **LT3094 confirmed against its own document, and it is NOT the LT3045 mirrored.** −20 V / 500 mA, dropout 235 mV, output range 0 to −19.5 V, 0.8 µV<sub>RMS</sub> (10 Hz–100 kHz), SET sinks 100 µA ±1 %. Pin map **1,2 IN · 3 EN/UV · 4 PG · 5 PGFB · 6 ILIM · 7 VIOC · 8 SET · 9 GND · 10 OUTS · 11,12 OUT · EP 13 = IN**. **The exposed pad is IN, where the LT3045's is GND**, and `DD` is DFN-**12** here against DFN-**10** on the LT3045 | Rev. B Pin Functions p.15 **and** the Pin Configuration diagram p.3, read independently — 100 % agreement (M2). Diagram caption states *"EXPOSED PAD (PIN 13) IS IN"* outright |
| T1-81 | **LT3094's PSRR curve is its own shape, not the LT3045's.** At 2 V headroom: **76 / 66 / 72 / 72 dB** at 100 kHz / 500 kHz / 1 MHz / 2 MHz — it **peaks at 100 kHz** where the LT3045 peaks at 2 MHz, and **declines as headroom grows beyond ~2 V**, the opposite of the LT3045. Audio band (G46, V<sub>OUT</sub> ≤ −1.5 V): ~112 dB peak near 30 Hz, ~107 dB to 1 kHz, **≥ 93 dB at 20 kHz** | Curves G47 and G46 p.12, cropped to 400 dpi and read. **The operator's instruction not to inherit G45 was correct** — inheriting it would have overstated the negative rail by ~12 dB at 2.2 MHz |
| T1-82 | **LT3045 current-limit programming: `Current Limit = 150 mA·kΩ / R_ILIM`**, with the datasheet's own worked example — *"a 1kΩ resistor programs the current limit to 150mA and a 2kΩ resistor programs 75mA."* ILIM threshold 300 mV; the pin sources current 1:500 to output current. **"If the programmable current limit functionality is not needed, tie ILIM to GND."** LT3094's equivalent scale is **3.75 A·kΩ** — a 25× different constant on the sibling part | Rev. D Applications Information p.19 + p.15. **Drives F40** |
| T1-83 | **LT3045 `PGFB` unused disposition:** *"If fast start-up capability is not used, tie PGFB to IN or to OUT for output voltages above 300mV. **Note that doing so also disables power good functionality.**"* So PGFB→OUT is datasheet-sanctioned and knowingly gives up PG | Rev. D p.19. The five housekeeping LDOs take this; U15 gets a real divider instead |
| T1-84 | **LM5156-Q1 pin map, 12-pin WSON (DSS):** 1 BIAS · 2 VCC · 3 GATE · 4 GND · 5 CS · 6 COMP · 7 DITHOFF · 8 FB · 9 SS · 10 RT · 11 PGOOD · 12 UVLO/SYNC/EN · EP. **EP "must be connected to GND"** — electrical, not thermal-only. **Pin 12 "must not be left floating."** DITHOFF polarity: **VCC disables** dither, **GND enables** it | Table 7-1 p.4 cross-checked against Figure 7-1, same page — 100 % agreement (M2) |
| T1-85 | **LM61460-Q1 `BIAS` has an explicit high-output-voltage rule:** *"Input to internal LDO. Connect to output voltage point to improve efficiency… **If output voltage is above 12 V, connect this pin to ground.**"* Below 3.1 V on BIAS, VIN powers the internal LDO directly | SNVSB70F Table 7-1 p.4 + §9.3.6. **Settles the IBB's BIAS disposition from the document** rather than from the 16 V abs-max argument alone |
| T1-79 | **TI's documented inverting buck-boost is a reconfigured *buck*, not a boost** — SNVA856 "Working With Inverting Buck-Boost Converters", 20 pp. Carries §4.1 voltage stress, §5 component selection, and **§7.1/§7.2/§7.3 level shifters for enable, sync and power-good** — the three practical problems a negative-referenced controller creates. Worked examples use LMR33640 and LMR14020 | `SNVA856_TI_InvertingBuckBoost.pdf` Rev. B, contents + §2. **None of the five switching datasheets held documents an inverting configuration** |

**Twenty-one datasheets now held and read to varying depth** (`DATASHEETS.md`). `CLAUDE.md` §5's
*a part number is not a datasheet* still governs every parameter not in this table. T1-10 remains
the one fact resting on operator confirmation rather than a document — worth the 60-second
re-check next time the AK4118A file is open, since the whole F1 disposition stood on it.

### T1 by decree — requirements

Binding because `REQUIREMENTS.md` is the authority, not because the underlying state has been
independently confirmed. Section references are to `REQUIREMENTS.md` **v0.1**.

| ID | Requirement | Src | Tag |
|---|---|---|---|
| T1-D01 | Single-board automotive DSP: 4 diff analog in, 12 buffered SE out, coax SPDIF in, BT A2DP sink, BLE+WiFi control, 12 V automotive power | §1 | |
| T1-D02 | fs = 48 kHz system-wide, 32-bit slots | §4 | HARD |
| T1-D03 | Single 24.576 MHz low-jitter XO is the master clock; ADAU1466 PLL to 48 kHz core | §3 | HARD |
| T1-D04 | ADC/DAC MCLK distributed via low-additive-jitter fanout buffer, **not** daisy-chained | §3 | HARD |
| T1-D05 | No spread-spectrum anywhere in the audio clock tree | §3 | HARD |
| T1-D06 | BM83 and SPDIF paths both traverse an on-chip ASRC — "no exceptions" | §3 | HARD |
| T1-D07 | TDM/port map exactly per the §4 table; spare IN3/OUT3 to 0.1" headers with interleaved grounds | §4 | HARD |
| T1-D08 | DAC split is 6+6 across two AK4458; slots 7–8 reserved on each | §4 | HARD |
| T1-D09 | ESP32-S3 is sole owner of all device state; SPI slave-boot + safeload to DSP, ≥10 MHz target | §5 | |
| T1-D10 | GPIO19/20 reserved for USB D± — not assignable elsewhere; USB-C device role, ESD-protected | §5 | |
| T1-D11 | Input ranges: line ≤2 Vrms, speaker ≤30 Vrms FS; MCU-controlled relay or analog switch; **never jumpers**; Zin ≥ 20 kΩ line | §6.1 | |
| T1-D12 | Signal-sense per input (or summed node), ~10 mVrms threshold, resistor-settable | §6.1 | |
| T1-D13 | ≥ 4.5 Vrms before clip into 10 kΩ on all 12 outputs; Zout ≤ 100 Ω | §6.2 | HARD |
| T1-D14 | Shunt mute at each RCA on a single MCU-driven mute rail; relay preferred, FET acceptable only if THD contribution < DAC floor | §6.2 | |
| T1-D15 | Single ground plane; analog/digital partitioned **by placement, not splits**; chassis star-connect at RCA ground field via RC network; deviations flagged | §6.3 | |
| T1-D16 | Rail set and names exactly per §7.1; all battery-facing regulators AEC-Q100 | §7.1 | |
| T1-D17 | ±13V5_A noise budget < 50 µVrms, 20 Hz–20 kHz, at the op-amp rails after LDO/filtering | §11 | |
| T1-D18 | ISO 7637-2 survival at the input | §7.1 | HARD |
| T1-D19 | Turn-on sequence §7.2 and turn-off sequence §7.3, in order; no audible pop is acceptance | §7.2/7.3 | HARD |
| T1-D20 | BM83SM1 and ESP32-S3-WROOM-1 antenna keepouts enforced; the two 2.4 GHz antennas separated as far as geometry allows, not stacked | §8 | HARD |
| T1-D21 | Net naming per §10; analog channel numbers match §4 TDM slots with no remapping | §10 | HARD |
| T1-D22 | WM8804, TJA1051T-Q1, 25AA1024 are DNP on v1 | §2 | |
| T1-D23 | AKM→TI substitution (PCM1865/PCM1690) is pre-approved but changes TDM formats and must be flagged if exercised | §2 | |
| T1-D24 | Board envelope ≤ 200 × 140 mm assumed until told otherwise | §11 | |
| T1-D25 | Post-fab acceptance criteria per §12 (8 items) | §12 | |
| T1-D26 | **AK4118A is clock master on SDATA_IN2**; DSP port is clock consumer of that link only; ASRC does the rate conversion; recovered clock terminates at the ASRC boundary | §3 v0.2 | HARD |
| T1-D27 | **2×** INA1650, not 4 — 4 diff inputs = 4 channels at 2 ch/pkg | §2 v0.2 | |
| T1-D28 | **Not an AEC-Q board.** Operating range −20 °C…+70 °C; industrial grade acceptable throughout the signal path; AEC-Q100 only where parts face the battery/harness directly — input protection, bucks, CAN PHY, remote-out driver | §7.0 v0.2 | |
| T1-D29 | **OPA1656**, decided. OPA1612 alternate dropped; filter values computed against OPA1656 only | §2/§6.2 v0.2 | |
| T1-D30 | ±13V5_A: **200 mA continuous, 250 mA peak, per rail** | §7.1 v0.2 | |
| T1-D31 | Input attenuator: divider **ahead of** the switch element; resistors **0.1 % matched or better** as a BOM requirement | §6.1 v0.2 | |
| T1-D32 | AOUT1–6 = AK4458 #1 slots 1–6; AOUT7–12 = AK4458 #2 slots 1–6. Net names follow the **system** channel number, never the per-device slot | §10 v0.2 | HARD |
| T1-D33 | EDA tool is **KiCad** | Operator instruction, 2026-08-15 | |
| T1-D34 | **Mute is the zero-energy state.** De-energised = muted by construction. §7.2/§7.3 cover the orderly path; §7.4 is the only thing that survives crank sag, blown fuse or pulled connector | §7.4 v0.3 | HARD |
| T1-D35 | Latching relays **prohibited**. Non-latching relays permitted only energised-to-unmute, and if chosen the +5V_D budget grows ~0.5 A and the LM61460-Q1 is re-checked. Semiconductor shunt is the default and a relay must justify itself | §6.4 v0.3 | |
| T1-D36 | Rail monitoring via **ADS1015-class 4-ch I2C ADC on I2C0** — VBATT, +13V5, −13V5, 3V3_A. Not the ESP32-S3 ADC. §9 dividers unchanged; −13V5 referenced to a positive rail | §5/§9 v0.3 | |
| T1-D37 | **FCC Part 15 Class B design practices; no chamber test for v1; CISPR 25 out of scope.** Spread-spectrum **stays enabled on the bucks** — §3's prohibition is on the audio clock tree only | §7.5 v0.3 | |
| T1-D38 | Version control is **git**, library **in-repo** not a submodule | Operator, 2026-08-15 | |
| T1-D39 | Footprint sourcing: vendor-published verbatim → IPC-generated → hand-built as last resort. Verification is an adversarial rasterise-over-datasheet pass logged per part; operator personally checks ADAU1466, AK5574, AK4458, AK4118A, BM83SM1 | Operator, 2026-08-15 | |
| T1-D40 | **Series–shunt mute.** Series = Form A photoMOS (TLP3475-class), energised-to-pass, open when unpowered. Shunt = depletion-mode FET pair, back-to-back source-to-source, biased off from −13V5_A, conducting when unpowered. Both fail safe independently; failed-state depth is the product | §6.4 v0.4 | HARD |
| T1-D41 | Mute continuous cost: ~60 mA on +5V_D (12 × 2–5 mA photoMOS LED drive), ~0.3 W, held for the operating life. A **line item in the +5V_D budget**, not a rounding error | §6.4 v0.4 | |
| T1-D42 | **CCIF twin-tone IMD ≤ 0.003 %** — 19 kHz + 20 kHz at 2 Vrms, product at 1 kHz. Added alongside the existing 1 kHz THD criterion, not replacing it | §12 v0.4 | |
| T1-D43 | Mute depth requirement is **bounded by the amp's remote-mute latency**, not indefinite — remote-out is fail-safe and drops before anything else notices. V-16 models DAC residual × mute attenuation × amp gain × amp mute latency, with a pessimistic latency | §7.4 v0.4 | |
| T1-D44 | Board is **ODSP-12**, PN `ODSP12-MB-A`, revision scheme A/B/C… for fab revisions with the running change log in git | Operator, 2026-08-15 | |
| T1-D45 | Symbol pin maps verified against the datasheet's **pin-function table**, not the package drawing — vendors have shipped datasheets where the two disagree and the table is normative | Operator, 2026-08-15 | |

---

## 2. T2 — Highly probable (actionable, still tagged)

Derived by calculation or strong inference from T1-D. Actionable; still tagged; downstream work
inherits the tag.

| ID | Claim | What promotes it |
|---|---|---|
| T2-01 | BCLK rates at 48 kHz / 32-bit slots: **TDM8 = 12.288 MHz**, **TDM4 = 6.144 MHz**, **I2S stereo = 3.072 MHz**. MCLK = 24.576 MHz = **512 fs**. | Arithmetic from T1-D02/D03 — solid; confirm each peer accepts these ratios (§8 V-04) |
| T2-02 | No parallel memory bus exists anywhere on this board — ADAU1466 uses internal RAM, ESP32-S3-WROOM-1 has flash/PSRAM inside the module. **The usual dominant layer-count driver is absent.** | BOM read; confirm no external DSP program memory beyond the DNP EEPROM |
| T2-03 | Finest pitch is the ADAU1466 72-LQFP at **0.5 mm**, and there is **no BGA**, if the LQFP option is taken. WLCSP would change this materially. | Datasheet package drawing (§8 V-01) |
| T2-04 | Controlled impedance is required on exactly two things: **SPDIF coax at 75 Ω** and **USB D± at 90 Ω differential**. All TDM/I2S at ≤12.288 MHz is slow enough not to need it; both antennas are module-integrated so there is **no 50 Ω RF trace to route**. | Operator decree — currently a proposal, see F4 |
| T2-05 | Reaching 4.5 Vrms SE from an AK4458 differential output requires roughly **13 dB of gain** in the diff-to-SE stage (if FS is ~2.8 Vpp diff ≈ 1.0 Vrms). This sets the output-stage noise budget and the resistor values, and it multiplies DAC-referred noise by ~4.5×. | AK4458 FS output voltage from datasheet (§8 V-05) |
| T2-06 | ±13.5 V rails give OPA1656 roughly ±12 V of usable swing into 10 kΩ, i.e. ~8.5 Vrms capability against a 4.5 Vrms requirement — **comfortable headroom**, ~5.5 dB. | OPA1656 output swing spec (§8 V-06) |
| T2-07 | ESP32-S3 pin budget drops to **~21 GPIO** after T1-D36 moves rail sensing to I2C: SPI 4, UART 2, I2C 2, signal-sense 4 (comparator outputs, digital), remote-in 1, mute 1, remote-out 1, BM83 MFB+reset 2, DSP reset 1, LED 1, USB 2. Was 22–24 with three ADC channels on the SoC. | The explicit pin map, which §5 requires before capture — not yet done |
| ~~T2-12~~ | ~~`Ron × Coff` constrains a single shunt device, so depth and linearity compete~~ | **Retired by topology, not disproved.** The analysis was correct *for a shunt-only design* and is what motivated the split into series–shunt (T1-D40). It no longer constrains the part choice, because no single device is now asked for both |
| T2-13 | Off-state distortion from a shunt's nonlinear capacitance is negligible at 1 kHz and rises ~20 dB/decade. **1 kHz THD cannot see it; 20 kHz THD cannot either**, because the harmonics land at 40/60 kHz outside the band. Only an in-band distortion *product* catches it. | Resolved into T1-D42 (CCIF twin-tone). Retained here because the reasoning, not just the criterion, is what transfers |
| T2-14 | A **single** MOSFET shunting a bipolar audio signal conducts through its body diode on one half-cycle. Discretes must be **back-to-back, source-to-source**. | Standard device physics — high confidence, but it goes in the schematic as a reviewed detail, not an assumption. Survives the v0.4 topology change unchanged |
| T2-15 | Series photoMOS off-isolation alone is frequency-dependent — a few pF of Coff against a 10 kΩ load gives roughly 70 dB at 1 kHz falling to ~45 dB at 20 kHz. **This is exactly the leakage the shunt exists to kill**, and it is why the shunt's Ron requirement is lax (100–500 Ω against a ~MΩ leakage source impedance still buys ~70 dB). | V-14/V-15 with real part numbers. The point that matters is the *ratio*, and it is comfortable by two orders of magnitude |
| ~~T2-08~~ | CMRR ≥ 60 dB is set by attenuator resistor matching, implying 0.1 % or better | **Promoted → T1-D31.** Decreed as a BOM requirement 2026-08-15. A tolerance analysis before the BOM freezes is still worth doing — 0.1 % is the estimate that generated the decree, not a measured margin |
| T2-11 | **RCA-class jack count is 17 populated, 18 positions**: 4 line in + 12 out + 1 SPDIF coax in, plus 1 DNP SPDIF out. Differential inputs are tip-vs-shield on a single jack, so 4 inputs = 4 jacks, not 8. | Confirmed against `REQUIREMENTS.md` §8 by the operator, 2026-08-15, after the assistant stated 28 in error. See ledger |
| T2-09 | The ADAU1466's PLL locks to the same 24.576 MHz XO that feeds the converters' MCLK, so LRCLK and MCLK are frequency-coherent by construction. Phase/jitter relationship is not thereby guaranteed. | AKM MCLK/LRCK synchronisation requirement in TDM slave mode (§8 V-04) |
| T2-10 | Schematic capture can proceed on the §4/§5/§6/§7 architecture **without** any Block D/E answer. Only footprint assignment and layout depend on mechanical and fab data. | — structural, acted on in `CLAUDE.md` §2 (G0-S / G0-L split) |

---

## 3. T3 — Likely / moderate confidence

Branchable, but check the root before the branch gets expensive.

| ID | Theory | Check |
|---|---|---|
| ~~T3-01~~ | ~~The EDA tool is KiCad~~ | **Closed, and it was right — which is the trap.** Operator decreed KiCad (T1-D33) and the install verified at T1-05…T1-09. A correct guess held at T3 cost nothing; the same guess acted on would have been indistinguishable from luck. Note it did not predict **version 10**, which is the part that actually matters (see ledger) |
| T3-02 | This board wants **6 layers** (sig / GND / pwr / pwr / GND / sig or similar), not 4: mixed-signal with a mandated single unsplit ground plane, seven rails, ±13.5 V analog distribution, two 2.4 GHz modules, and switching regulators — even without a memory bus. | Q22. **Not acted on.** Layer count is a fab and cost decision, and T2-02 cuts the other way. |
| ~~T3-03~~ | ~~"4× INA1650" is a channel count in a package column~~ | **Confirmed by operator → T1-D27.** 2× INA1650 |

---

## 4. Open unknowns — remaining intake

Rows are **BLOCKING** unless marked. Closed rows are struck and promoted to §1.

### Block A — Engagement and role

| ID | Question | Why it matters | Status |
|---|---|---|---|
| ~~Q1~~ | ~~What is being delivered?~~ | | **Closed** → schematic capture then layout, greenfield. `CLAUDE.md` §1 |
| ~~Q2~~ | ~~Channel policy~~ | | **Closed 2026-08-15** → closed-book by default, batched escalation, stop-the-line exception. Written into `CLAUDE.md` §4. Settled **by observation** — the project had been running it for five rounds |
| ~~Q3~~ | ~~Version control?~~ | | **Closed** → git, initialised 2026-08-15, library in-repo. T1-D38 / DL-15 |
| ~~Q4~~ | ~~Board name/PN/revision~~ | | **Closed** → **ODSP-12**, PN `ODSP12-MB-A`, rev A/B/C… per fab revision, change log in git. T1-D44 |
| Q5 | Is the process visible to the client as well as the result? | Changes how much reasoning is written for an outside reader | Non-blocking |

### Block B — Tooling · *gates: G0-S, and therefore capture*

| ID | Question | Why it matters | Status |
|---|---|---|---|
| ~~Q6~~ | ~~EDA tool, version, install path~~ | | **Closed** → KiCad 10.0.5, T1-D33 / T1-05 |
| ~~Q7~~ | ~~CLI on PATH?~~ | | **Closed** → no. Full path always, T1-06 |
| ~~Q8~~ | ~~Bundled Python path~~ | | **Closed** → T1-07 |
| ~~Q10~~ | ~~Units: mm or mil?~~ | | **Closed** → mm, decided and logged DL-09 |
| Q9 | Autorouter in play? Which, and what runtime? | Changes routing strategy and which ledger entries apply | BLOCKING (layout) |
| ~~Q30~~ | ~~Footprint library verification~~ | | **Closed** → T1-D39, DL-14 |

### Block C — Electrical

| ID | Question | Why it matters | Status |
|---|---|---|---|
| ~~Q12–Q18~~ | | | **Closed** by `REQUIREMENTS.md` §1–§10 → T1-D01…D25 |
| ~~Q29~~ | ~~INA1650 quantity~~ | | **Closed** → 2×, T1-D27 |
| ~~Q33~~ | ~~OPA1656 or OPA1612~~ | | **Closed** → OPA1656, T1-D29 |
| ~~Q31~~ | ~~±13V5_A current budget~~ | | **Closed** → 200 mA cont / 250 mA peak, T1-D30. *Mute-rail budget still open below* |
| ~~Q32~~ | ~~Rail monitor: distinct device or ESP32 ADC?~~ | | **Closed** → ADS1015-class on I2C0, T1-D36 |
| ~~Q38~~ | ~~Mute rail budget~~ | | **Closed in principle** → T1-D34/D35 make it a GPIO-class load with no §7.1 entry beyond a line item, *conditional on* the semiconductor shunt surviving V-14/V-15. If a relay is justified instead, +5V_D grows ~0.5 A and the LM61460-Q1 is re-checked |

### Block D — Mechanical · *gates: G0-L, and therefore all layout*

| ID | Question | Why it matters | Status |
|---|---|---|---|
| Q19 | Board outline and dimensions, or the DXF/STEP that defines them | ≤200×140 mm is an *envelope*, not an outline. Hardest constraint; changing it after placement invalidates the layout | BLOCKING (layout) |
| Q20 | Mounting holes, keepouts, enclosure interference | Placement anchors, not adjustments | BLOCKING (layout) |
| Q21 | Component height limits, top and bottom | Silently violated otherwise, discovered at assembly | BLOCKING (layout) |
| Q34 | Connector part numbers — RCA jacks (16 of them), automotive power connector, speaker-level strip terminal | 28 RCA-class jacks dominate the board edges and the area budget. Footprints are needed before any placement | BLOCKING (layout) |

### Block E — Stackup and fabrication · *gates: G0-L, G2, G3, G4*

**The TVS land pattern is an ELECTRICAL rating input, not an outline** *(2026-08-16, F42)*. Vishay
states the load-dump capability figures are *"based on normal room temperature **with the
recommended pad size as listed in the datasheet**, but the actual capability varies by PCB type,
pad size, and temperature conditions"* (doc 49748). So **§12's whole verdict column is conditional
on the layout honouring the recommended pad** — **DO-218AC** *(F87)*, land **15.30 × 10.70 mm**, tab is the
**anode**, so it pours into the ground plane. R<sub>θJM</sub> = 0.35 °C/W is junction-to-*mount*
and is only as good as the copper under it. **This is the first case on the project where a
layout choice moves a number in the acceptance criteria**, which is a different class from
"placement affects performance" — shrink this pad at layout and §12 becomes false.

**New input, logged 2026-08-16 (F39):** the SEPIC's **FET, Schottky and coupled inductor are now
the board's dominant heat sources** — ≈ 8.5 W through that stage, ~1.65 A input at crank. Copper
allocation there is a **stackup input**, alongside the ADAU1466's 5.3 mm exposed-pad via array.
Two thermal claims on the layer count now, from opposite ends of the board.

| ID | Question | Why it matters | Status |
|---|---|---|---|
| Q22 | Layer count and intended stackup | G3. T3-02 is a guess and is not acted on | BLOCKING (layout) |
| Q23 | Fab house and capability limits: min trace/space, min drill, annular ring, allowed via types | These *are* the design rules | BLOCKING (layout) |
| Q24 | Copper weight and surface finish | Affects trace width for the ±13V5 and battery rails, and fine-pitch assembly | BLOCKING (layout) |
| Q25 | Source of the shipped design rules and DRC severities | G2 requires a baseline that exists before work starts | BLOCKING (layout) |
| Q35 | Confirm or replace the proposed impedance targets: 75 Ω SPDIF coax, 90 Ω USB differential | F4. Feeds directly into the stackup | BLOCKING (layout) |

### Block F — Assembly, thermal, EMC

| ID | Question | Why it matters | Status |
|---|---|---|---|
| Q26 | Single- or double-sided assembly | Drives silkscreen, courtyards, fiducials, and whether the 12 mute relays can go on the bottom | BLOCKING (layout) |
| Q27 | Thermal: airflow, hot parts, expected dissipation | Automotive enclosure, ±13.5 V switcher, 24 op-amps and possibly 12 relay coils in a sealed box | BLOCKING (layout) |
| ~~Q36~~ | ~~Operating temperature range and AEC-Q grade~~ | | **Closed** → −20…+70 °C, not an AEC-Q board, T1-D28 |
| ~~Q37~~ | ~~Emissions target~~ | | **Closed** → FCC Part 15 Class B practices, no chamber for v1, CISPR 25 out of scope. T1-D37 |

---

## 5. Anti-drift ledger

**Permanent.** Entries are never deleted once corrected — the point is that a corrected belief
cannot quietly return.

Format: the wrong belief → the correction → **the tell** that catches it.

### Method rules — promoted from specific entries because they generalise

**M5 — "Nothing is missing" needs "and there were N things."** A check passes **vacuously** when
its input is empty. Every completeness assertion needs a companion assertion that the input was
non-empty **and plausibly sized against an independent expectation**. Four instances now: ERC on
an empty sheet, `file` reporting 10 pages, HTTP 200 on the wrong PDF, and a pin-set assertion over
an empty pin map. Stating the rule is what stops the fifth from needing to be caught by luck.

**M7a — The convention caught its own author.** The FB leakage term was first stated
conversationally as **"5 µV"**; 100 nA × 50 kΩ is **5 mV** — off by three orders of magnitude, by
the operator, in the same round that specified the convention. **The conclusion survived** (the
window is wide either way) **and the derivation under it was broken** — M1a's exact shape, this
time on the operator's side rather than the assistant's.
*What caught it:* the convention **required the inequality to be written on the sheet**, and
**written arithmetic gets checked in a way conversational arithmetic does not.** The sheet now
carries the correct figure: 50 nA × 50 kΩ = **2.5 mV against a 60 mV window, 24× margin**.
*Why it belongs beside M7:* consequences are cheaper to check than derivations **and they check
both parties.** A method whose whole claim is that written constraints catch what confidence
misses is only evidenced when it catches the people who wrote it. It now has that evidence from
both sides of the desk, in the same session — the `RT` error and this one.

**The "vishay.com is unreachable" claim was wrong, and it shaped two rounds of asks.** *(caught
2026-08-16.)* It came from **one** failed fetch — `docs/88361/smbj.pdf`, which returned HTML —
and was generalised to the host, then repeated in `DATASHEETS.md` and in two escalations as a
reason the operator had to fetch things manually. The shortlink `vishay.com/doc?88387` returns a
PDF, HTTP 200, first try. **A single failed request is evidence about that request, not about the
host** — the same shape as M1 (confidence attaches to the method) and the same shape as the grep
errors, one observation promoted to a general rule. *The tell:* a negative claim about
infrastructure should name what was tried and stay scoped to it, and it costs one retry to check
before it becomes an ask on someone else's time.
*Technique worth keeping, since it is what actually found the successor:* **PDF hyperlinks are
extractable** — `/URI (...)` entries, including inside compressed streams — so a datasheet that
cross-references other documents hands you their doc numbers directly. That is how doc **98647**
was located after the NRND banner text turned out not to be a link.

**M14 — A multi-unit symbol placed as one instance strands the other units' labels.** They sit
at coordinates no pin occupies: **attached to nothing, present in the netlist, and invisible as an
error** — every completeness check passes because every pin *was* dispositioned. The countermeasure
is structural: recompute per-unit geometry with **the symbol generator's own math**, then assert
that the units **reconstruct the full pin set** and **do not overlap**. *Why it earns a rule now:*
the next sheets are full of multi-unit parts — every op-amp package on the output stage is two
units plus power — so this stops being a BM83 anecdote and becomes the default hazard. M6's blind
spot in a third layer, after the zipped pin map and the label collision.

**M13a — Variant-conditional footnotes are a confirmed pattern, not a curiosity.** The
ESP32-S3-WROOM-1 carries **two** footnotes that reserve pins **by module suffix**: (b) IO35/36/37
belong to the PSRAM on R8/R16V, (c) IO47/48 run at 1.8 V on R16V. Both are false for the N8R2, so
five GPIOs are available that a careless read would have written off — and **two of them now carry
nets** (`BM83_TX_IND`, `BM83_RST_N_MCU`). The pinned PN therefore guards two nets it did not exist
to guard. *The rule:* on any part with variant suffixes, **read the footnotes as pinout conditions
and resolve each against the ordered variant**, because they cut both ways — reserving pins you
planned to use, and freeing pins you wrote off.

**M13 — A PDF's cross-reference graph is machine-readable navigation, not decoration.**
Embedded `/URI` entries — including inside compressed streams — turn "hunt the successor
document" into a parse. Doc **98647** was found this way after the NRND banner's *text* turned
out not to be a link while the "Related Documents" icon was. **This pays on every vendor whose
site search is worse than their own documents, which is most of them**, and it is strictly better
than guessing doc numbers or trusting a distributor's link. *Companion to M11:* when a document
points at a successor, the pointer is usually **in** the file, so the redirect boundary M11 warns
about is normally crossable without leaving the archive.

**M22 — PROSE IS WHERE THE ARITHMETIC IS UNPROTECTED. Numbers in a report must be READ BACK from the module that computes them, never recalled from the model that motivated them.** *(Adversary 004, diagnosing a pattern rather than an instance — accepted.)* The bias-node crosstalk figure has now been wrong **twice in prose and never once in the generator**: first −37 dB (the expression missing its noise-gain factor), then a decomposition that overstated by exactly the ÷2 term. Both times the sheet was right. **M7a's protection — written arithmetic gets checked — does not reach a paraphrase of the arithmetic**, and a paraphrase is what a report is. The generator prints its own load-bearing numbers; the report copies them. **The tell is a number that appears in a message but nowhere in a program's output.**

**M23 — A CITATION IS A FIFTH KIND OF READ, AND IT IS THE ONE THAT FAILS SILENTLY. Values, structure, conditions, and *the page they came from* are four independent reads; a wrong page corrupts nothing today and everything on re-verification.** *(Predicted in our own 003 as the fifth read; first instance in the wild caught by adversary 010 — against **me**.)* T1-113 recorded the ADAU1466 MCLK duty window as **Rev. C p.29**. The values were right. The page was wrong: a whole-document audit shows `"MCLK duty cycle"` occurs **exactly once in 202 pages, on p.9, Table 6** — and p.9's own footer reads *Rev. C | Page 9 of 202*, so there is not even a PDF-vs-printed offset to blame. p.29 is **Example PLL Settings, Table 20** — real, MCLK-adjacent, and carrying no duty spec at all, which is exactly why the error survived: *a plausible neighbour is more durable than a wrong one.*

**What makes this class dangerous is that it is invisible until someone else reads the same document.** The number was correct, so no downstream calculation broke, no assertion fired, and no review of the *value* would ever have caught it. It surfaced only when a second reader cited a different page for the same fact — at which point **I diagnosed it as a revision difference between two copies of the document.** There is one copy, in a shared folder, 202 pages, Rev. C, one timestamp. **My diagnosis invented a document that does not exist to explain an error I had made**, and it was a *comfortable* explanation: "different revisions" blames the archive and asks nothing of me, where "my citation is wrong" asks for a re-read. That the comfortable diagnosis arrived first is the part to distrust.

**The countermeasure is the audit, not the re-read:** when two readers cite different pages for the same fact, **grep the whole document for the parameter name and count the hits** before theorising. One hit ends the argument in seconds. **The tell is a citation defended by a story about the document rather than by an occurrence in it.**

**M24 — THE NETLIST AND THE ANNOTATION FAIL IN OPPOSITE DIRECTIONS, AND NEITHER SIDE IS CHECKABLE BY THE TOOL THAT CATCHES THE OTHER.** *(Adversary 016, pairing F41 with F67 — their formulation, which was better than mine.)* **F41 was names right, coordinates wrong**: three nets merged because the geometry disagreed with the labels. **F67 was coordinates right, names wrong**: the strap sat on exactly the pin its comment named, and the comment's *claim* about that pin was false. Same underlying failure from opposite ends. **ERC reads the netlist and cannot see the annotation; review reads the annotation and cannot see the netlist.**

**The specific F67 shape is worth naming on its own, because it is invisible by construction:** the comment read *"TDM0/TDM1 → TDM4, 32-bit"*. TDM1-0 **was** correct. But **TDM1-0 sets the multiplex mode and DIF1-0 sets the word length** — the "32-bit" claim was written beside the pair that does not control it. **A comment asserting a fact about a pin it is not attached to passes review, because the pins it names check out.** The reviewer verifies TDM, finds it right, and moves on.

**Countermeasure: an annotation must name the pin that ENFORCES its claim, not a neighbour that shares the topic.** Where one comment covers several straps, each claim gets its own pin list. **The tell is a comment whose subject and whose evidence are different pins.**

**M25 — “LET THE RESET DEFAULT BE THE OPERATING VALUE” IS A TIEBREAKER WITH A PRECONDITION, NOT A DECISION PROCEDURE. It only decides when the parts' defaults AGREE on the free parameter.** *(Mine, from F69; the precondition is adversary 018's correction and it is the half that keeps it honest.)* The principle is sound and it is §7.4's zero-energy logic applied to configuration — **PDN restores defaults, so where a requirement is silent, choosing the default as the operating value makes every restore benign instead of a fault.** It also shrinks the boot-write set, which is F66's own criterion.

**But look at why it worked here.** AK5574 defaults to 24-bit **MSB**; AK4458 to 32-bit **MSB**. They **agree on justification** — the free parameter — and differ only on word length, which §4 [HARD] already settles. **Had one defaulted to I2S, the principle would have produced no answer at all**, and the danger is that it would still have *looked* applicable.

**A worse failure is available and it is the one to watch for: the principle silently picking whichever part you happened to read first.** With disagreeing defaults there is no “the default” to adopt, only two of them.

**And it does not outrank a real deciding input.** In F69 the genuinely free variable was the DSP — SigmaStudio port configuration is **authored, not defaulted, so it has no reset state to inherit** — which means it should be decided first and the converters derived from it. Deriving the converters from converter defaults was, as 018 put it, *a choice about the DSP dressed as a discovery from the converters.* **Check the precondition holds AND that no authored input outranks it, before reaching for this.**

**F72n — negative result, recorded so it is not rediscovered as a problem.** AK4458 pp.43 and 45: *“DIF2-0 bits setting of both first AK4458 and the second AK4458 must be the same.”* **It does not bind us.** Both instances sit inside the **daisy-chain** examples — TDM512 (Figure 38) and TDM256 (Figure 42) — where the second AK4458 receives shifted data and re-emits via `TDMO1`. Our two DACs sit on **independent DSP output ports with no cascade**, so there is no “first” and “second” in AKM's sense. **We satisfy it incidentally anyway, both being `110` — which is exactly the condition under which a constraint gets mistaken for a validated one.** A reader who sees *two AK4458s* plus that sentence has two available wrong conclusions: that it binds, or that the design ought to be cascaded.

**M26 — A COMPLETENESS SWEEP MUST BE KEYED ON FIELDS, NOT REGISTERS, BECAUSE A FIELD CAN BE SPLIT ACROSS NON-ADJACENT REGISTERS AND ONLY A CROSS-REFERENCE SENTENCE REVEALS IT.** *(Adversary 020, from `DFS2-0`.)* The AK4458's sampling-speed field lives in **two places**: `01H` holds `DFS1-0` and **`05H` holds `DFS2`**, each definition disclosing the other only in prose — *“See also register address 05H for DFS2”* / *“See also register address 01H for DFS1-0.”*

**The obvious method fails silently.** Walk the register map, list the defaults, compare each against intent — and you have checked **two-thirds of that field**. A firmware author who writes `01H` to set sampling speed and never touches `05H` has written part of a field and **nothing tells them.** No tool sees it: the register map looks complete, every register has been visited, and the field's own name appears in both places without either being obviously partial.

**So the sweep's unit of work is the FIELD, carrying a mapping to *(register, bits)* that is allowed to be PLURAL.** The cross-reference sentence is the only artefact in the document that reveals the plurality, which means **the sweep is a prose read as much as a table read** — M20's four-kinds-of-read applied to enumeration.

**Two corollaries worth having.** *(a)* **“Correct at default” is not “decided”** — a sweep reporting *“N wrong, M fine”* conceals every field that is right by accident, and F73 is one that turned out not to be right at all once both ends were compared. The honest output has **four** buckets: wrong · inherited-not-chosen · inert · correct-and-intended. *(b)* **A completeness claim needs a stated bound on the space** — here Note 24's *“do not write 06H–14H”* is what makes N = 14 a closed count rather than a tally. **Without a bound you have a tally wearing a completeness claim's clothes.**

**M26a — THE METHOD CORRECTION, AND IT TOOK THREE TRIES. Key the sweep on field-name SUFFIXES GROUPED BY BASE NAME across the whole register map. Not on cross-references (a courtesy extended once), and not on the vendor's own function list (which omits the defects).** *(Adversary 022 supplied the middle correction against my advice; the third is T1-129, ours.)*

| Key | Finds | Verdict |
|---|---|---|
| **Cross-reference sentences** — *my advice in 021* | **1 of 8** split fields on the AK4458 | **Wrong.** AKM wrote *“See also register address…”* for `DFS` and for nothing else. Seven splits carry no cross-reference at all |
| **Field-name suffixes grouped by base name** — *theirs* | **8 of 8** | **Correct, mechanical, needs no vendor goodwill.** `INVL1/INVR1/…/INVL4` → `INV`; `SELLR1..4` → `SELLR`; `DEM11..DEM40` → `DEM` |
| **Table 31 “Function List”** — *vendor-authored, ours* | 14 functions, **splits named explicitly** | **Best KEY, fatal as a SOURCE.** Omits `TDM1-0` and `RSTN` — *both* known AK4458 defects |

**The trap in the third row is the one to remember.** Table 31 looks exactly like the artefact this whole exercise was trying to construct: field-keyed, defaults in plain language, multi-register addresses spelled out, even PCM/DSD availability so the *inert* bucket fills itself. **And it silently omits both defects.** A sweep built on it would be complete-looking, vendor-sourced, and wrong — which is strictly more dangerous than having no list.

**So use Table 31 to LEARN THE SPLITS and the register map to ENUMERATE.** Never the reverse. **And verify the splits AGAINST the map, because — adversary 024 — the splits key itself contains an incomplete split: Table 31 gives the filter group as `01-02H`, but the filter is `SD` (01H) + `SLOW` (02H) + **`SSLOW` (05H)**. It names two of three registers.** A sweep trusting Table 31 for splits would have written `SD` and `SLOW` and left `SSLOW` at default — **a three-register field written across two.** The rule survives its own test only because the map, not the table, is the enumeration source.

**Table 31 fails THREE distinct ways, worth separating because only the first is obvious:** *(1)* **it omits fields** — `TDM1-0` and `RSTN`, both defects; *(2)* **its register lists can be incomplete** — the filter group above; *(3)* **its default column collapses multi-bit fields into single-axis labels** — “Sharp roll-off filter” for a state that is actually *Short delay Sharp roll-off*, naming the roll-off axis and dropping the delay axis. **(3) is what produced F74, my own false finding.**

**M32 — A STEADY-STATE TEST DOES NOT ANSWER A TRANSIENT QUESTION, AND IT MOST OFTEN GETS THE RIGHT ANSWER ANYWAY — WHICH IS WHY THE SHAPE SURVIVES REVIEW AFTER REVIEW.** *(Adversary 091. **Fourth instance this week**, and the first one where nothing was at stake, which is where they could finally point at it.)* **The instance:** I justified the 47 µF damping cap being fully available with *“0.68 Ω drops 32 mV at our discharge currents.”* **Two errors.** (1) **Wrong current** — 32 mV/0.68 Ω = 47 mA is the *analog rail quiescent*; `VBATT_PROT` carries the whole board's input current, **128 mA–1.02 A, dropping 87–696 mV — 3–20× what I stated.** (2) **Wrong test entirely** — the question is transient, and the answer is **τ = 0.68 Ω × 47 µF = 32 µs against a 0.5–4.1 ms event: the cap TRACKS `VBATT_PROT` and is available regardless of current.** **My conclusion was right and neither number in my reason was.** **Prior instances, same shape:** 067→069 · F94's 20 kHz column · R-66's arrival time. > **The diagnostic: if the reason cites a VOLTAGE or a CURRENT for a question about WHEN or HOW FAST, it is the wrong test — a transient question is answered by a time constant.** **And the reviewer's meta-point is the more valuable half:** *the shape survived into a place where nothing was at stake, which is where you can see it clearly — a number that mattered would have had both of us checking it.* **So low-stakes justifications are where a habitual error is VISIBLE, not where it is harmless.**

**M31a — THE DIRECTION TEST IS VOID WHEN THE FAILURE MODE IS *OMISSION FROM A SUM OF POSITIVE TERMS*: there, same-direction is FORCED BY THE ARITHMETIC and carries no information. Closure comes from ENUMERATION, not from more terms.** *(Adversary 087, refuting my own addition to M31 within a day of my making it.)* I had written *“alternating = converging, same-direction = being unpacked.”* **Forgetting stored energy can only ever shorten a hold-up** — so the direction of F108's corrections was settled before either of us looked, and **the test would fire identically on a model one term from done and one four terms from done.** **M31 keeps its force only where corrections CAN go either way** — a divider ratio, a tolerance stack, anything with a subtraction in it.

**What closes such a model is M5's shape: an INDEPENDENT EXPECTATION, and here it is mechanical** — *every capacitance in the energy path from the input connector to the op-amp supply pins.* **That is a netlist query, not an analysis**, so the model closes by construction instead of by nobody thinking of a fourth term.

**RUN — AND THEN THE COUNT ITSELF FAILED AT ITS BOUNDARY, WHICH IS THE ONLY PLACE A COUNT CAN FAIL AND EXACTLY WHERE THEY LOOKED.** They asked one question about my ‘complete’ enumeration: *“is there any capacitance BEFORE `VBATT_PROT`?”*, noting that **an enumeration's only failure mode is its boundary — the count inside is checkable, but where the boundary was drawn is a judgement, and it is the one part of the method that thinking harder cannot verify.** **There was.** `VBATT_PROT` —[**0.68 Ω**]— `VBATT_DAMP` —[**47 µF/50 V**]— GND, the damping leg of the input LC. **0.68 Ω drops 32 mV at our currents, so it is fully available** — and it is **larger than the 32 µF I did count.** **Corrected: 79 µF, E = 6.10 mJ → 0.5–4.1 ms**, and their stress-grid worst case scales 2.47× to **5.04 ms — 15 % of the gap, not 6 %.** **F108 v3 still stands, and the conclusion never depended on it — but my claim that the count was COMPLETE was wrong, and the error was at the boundary rather than in the arithmetic.** *Original claim:* **RUN, and it settled the fourth term the same hour it was raised.** They predicted term 4 — *input bulk sustains the upstream converter to its UVLO, and **energy crosses a switching stage, not charge**, so ½CV² on the far side of that boundary had never been counted* — and bounded it at **1.4–51 ms on assumed input bulk of 220–1000 µF**, explicitly declining to compute a v4 from imagined inputs. **The enumeration gives the real number: `VBATT_PROT` carries 10 µF + 22 µF = 32 µF, and nothing larger exists anywhere in the path** (the only 100 µF on the board is `06_analog_in`'s NP audio coupling cap). **E = ½·32 µF·(13.8² − 6²) = 2.47 mJ → 0.2–1.6 ms.** **So term 4 adds under 2 ms and F108 v3 is NOT reversed** — known by a complete count rather than by a fourth model.

**M31 — WHEN A MODEL HAS BEEN CORRECTED TWICE IN THE SAME DIRECTION, STOP REFINING IT AND MEASURE THE THING. The tell is not that the number is wrong — it is that every correction so far has moved the same way, and the next unknown term probably does too.** *(Adversary 085, about a number of mine they had twice corrected and then declined to reopen.)* **F108's rail hold-up, three models in two days:**

| version | model | hold-up | margin |
|---|---|---|---|
| v1 | LDO **output** capacitance only | 1.53–6.52 ms | 5–45× |
| v2 | **+ upstream regulated phase** (an LDO holds until its INPUT hits dropout) | 1.80–7.71 ms | 4–42× |
| v3 | **+ both caps in parallel during dropout** (the pass element is ~0.52 Ω — a short) | 3.96–16.87 ms | **2–19×** |

**Two corrections, both omissions of STORED ENERGY, both in the direction that flattered the conclusion.** *“A third omission of the same kind closes the gap. I do not know of one — but I did not know of the last two either, and neither did you.”*

**This is M3 INVERTED: where construction cannot guarantee a property, MEASURE the property rather than refine the model.** A capture includes every term **by construction**, including the ones nobody has thought of — which is exactly the class that has been moving this number.

**Distinguish it from ordinary iteration:** a model corrected in *alternating* directions is converging. **A model corrected twice in the SAME direction is not converging — it is being unpacked**, and the remaining unknowns are drawn from the same population as the found ones. **Working rule 7's oscillating-error signal, with the sign attached.**

**Landed as `BRINGUP.md` 4b.7** — one single-shot capture, no fixture, takeable the first time the board powers down.

**M30 — A BACK-REFERENCE THAT PROTECTS ONE BOUND OF A TWO-BOUNDED PARAMETER TELLS THE NEXT READER THE PARAMETER HAS ONE BOUND. It is not merely incomplete — it ACTIVELY MISINFORMS, and it does so in the voice of the person who checked.** *(A failure mode OF §8.11 rather than a separate rule, so it belongs beside it. Mine, from F107; the generalisation is the reviewer's.)* **The instance:** F107 put a note at the mute bias capacitor saying *“shrinking this cap shortens a guarantee nobody else records”* — true, and written **one message after** installing the back-reference rule. **The cap has THREE jobs and the third wants it SMALLER:** filter the gate (large) · enforce break-before-make (large) · **let the fail-safe shunt ARRIVE (small, and with no stated requirement).** **“Do not shrink” gets obeyed by growing.**

**Why this is worse than an omission:** a reader who finds no note assumes nothing was checked and proceeds carefully. **A reader who finds a one-sided note assumes the parameter WAS checked and that the stated bound is the only one** — so the note converts caution into confidence in the wrong direction. **The rule that exists to make a coupling visible can hide the other half of it.**

**Countermeasure: a back-reference names every bound the value has, or says explicitly which bounds were not examined.** *“Do not change without re-running X”* is safe; *“do not shrink”* is not.

**M29 — REPETITION MANUFACTURES CONFIDENCE WITHOUT ADDING EVIDENCE, AND EACH REPETITION IS CHEAPER THAN THE FIRST. The tell is a claim you have said often and never re-derived.** *(Adversary 051, correcting a diagnosis of mine that was location-based.)* I had said the two errors that travelled furthest this week both lived in **standing sections**. **That is true of mine and false of theirs:**

| claim | repetitions | where |
|---|---|---|
| our `“7 generators still declare A3”` | ~12 | standing sections |
| their `convention 4` | 7 | **message bodies** |
| their `M7a` wording | 8 | **message bodies** |

**A mechanism aimed at standing sections catches ours and misses theirs; one aimed at REPETITION catches both.** Their description of the mechanism is the durable half: *the first mention was a passing aside; by the seventh it felt established — because it had been said often.* **That is M5 inverted — “I have said this many times” is a count over an empty set of checks.**

**AND THE COMPANION FINDING, which explains `convention 4` precisely: a reconstruction fails in TWO directions, for opposite reasons.** They had ranked *negative* claims (“it is not in there”) as highest-risk because a lossy copy drops content — **then both their negative claims about §12 were VERIFIED TRUE (F58), and the one that was phantom was POSITIVE.**

    NEGATIVE claim wrong  <-  the copy is LOSSY            (content dropped)
    POSITIVE claim wrong  <-  the copy is OVER-ORGANISED   (structure INVENTED)

**Their reconstruction has ELEVEN numbered conventions; this repo has THREE, and they are sheet-local to `01_power`.** That is not loss — it is **tidying**: a summariser imposing a schema the source never had, then numbering it. **Numbered structure is the most confident-looking thing a summary can produce and the least likely to be real, because numbering is exactly what a summariser adds.** *Watch what a summary has BUILT, not only what it has lost.*

**Partial countermeasure, and it was an accident:** an inline provenance tag — `[recon]`, `[yours, 023]` — at the point of use. **A tag travels with the claim; confidence travels with the claimant**, so the seventh repetition carries the same marker as the first. **It does nothing for a repeated NUMBER**, which is our A3 case, and that half is open on both sides.

**M28 — A CLOSED FINDING JUSTIFIED BY A *BEHAVIOUR* IS ONLY AS VERIFIED AS THAT STATE IS REACHABLE. Values are checkable by inspection; behaviours require the board to enter a state — and a state the design is built never to enter is one nothing will ever contradict.** *(Adversary 040, supplying the discriminator for a question I had raised without one.)* **F48 is the proof:** its justification was a behaviour (*the clamp holds the node inside ±14 V*), the state was *clamp conducting*, and **F76 made that state unreachable for the entire life of the design.** Nothing detected it — not ERC, not review, not the acceptance criteria — because **nothing ever asked the circuit to do the thing the finding claimed it did.**

**The sharpest subset is the sequencing-precondition family RUN BACKWARDS:** that family was written as a rule for new work — *ask what holds a state when the sequence never runs* — and it applies just as hard to findings already closed.

**Actionable by one question: can this state be entered deliberately?** **Yes → it belongs in `BRINGUP.md` as an INDUCED test**, which converts reasoning into observation for the price of one bench minute. **No → the reasoning is all there will ever be, and it deserves a second reader precisely because nothing will ever contradict it.**

**The tell: a closed finding whose evidence is an argument about a fault, and whose fault has never occurred.**

**M27 — A GUARD THAT CAN ONLY BE TESTED BY BREAKING ITS PRODUCER HAS BEEN WRITTEN AT THE WRONG LAYER. This is STRICTER THAN M9: M9 asks whether a guard *has been* fed a known defect; M27 asks whether it *CAN be*.** *(Adversary 038, from the F53 overlap guard I had been carrying untested for twelve legs.)* My stated reason was *“I would have to defeat the stacker to test the checker”* — **and it was wrong, disproved by my own F78 guard the same morning.** You do not defeat the producer; **you hand the checker fabricated data.** The overlap check could not be handed anything **only because it was inline**, welded to the stacker's output.

**If a checker's signature is `(data) → ok`, it is testable in isolation. If it is `(generator state) → ok`, it is not — and the fix is not a cleverer test, it is MOVING THE SEAM so the check takes data rather than context.**

**The admission criterion for any new assertion: can I hand this a known defect without running the thing that produces its input?** If no, refactor before writing it — otherwise it will still be untested ten legs later, **which is precisely the situation F53's overlap guard was in, and which F82 shows the page-extent guard is still in.**

**M26c — ENUMERATE ON THE AXIS THAT GENERALISES, AND LOOK FOR THE RULE IN THE SECTION NAMED AFTER THAT AXIS.** *(Adversary 031, sharpening our own search-order lesson into a predictive form.)* Our version was the observation: *“reading about the THING found the exception; reading about the MODE found the rule”* — p.46's `ODP` paragraph could only ever tell us about `ODP`, while p.56's control-mode section is where anything true of *all* pins has to live, because **that is the only section whose subject is the mode itself.** Their form is predictive: **the rule lives in the section named after the axis that VARIES, not the section named after the thing that varies WITH it.** *Same instruction as M26's field-vs-register point, arriving in a place neither of us expected it — fields not registers, modes not pins.*

**M26b — A SUMMARY TABLE IS NOT A NORMATIVE STATEMENT, AND TREATING IT AS ONE MANUFACTURES CONFLICTS THAT DO NOT EXIST.** *(From F74, retracted.)* I compared Table 31's partial label against the `SD` bit definition, called it a contradiction between two normative statements, and reached for **§5's conflicting-decrees rule — which does not apply, because a summary cell was never a decree.** §5's *“two conflicting [HARD] statements are a finding and a question”* draws its force from **both sides being authoritative.** A vendor function-list cell, a feature bullet, a block-diagram label (*“Very Low Ripple”*, F52) and a marketing summary are **derived views** — the same class §3 assigns to exported netlists: *never an override, and a disagreement with the source is a finding about the SUMMARY, not about the design.* **The tell is a ‘contradiction’ in which one side is a table cell carrying no units, no conditions and no bit values.**

**Two structural hazards found while doing it, both defeating ordinary reading order:** `SDS` is split **out of numeric order** — `SDS1`/`SDS2` in `0AH`, **`SDS0` in `0BH`** — so a reader who finds the higher-numbered members has no reason to suspect a lower-numbered one elsewhere. And the Sound Control channel bits **run backwards**: `07H` holds L3/R3/L4/R4 while `08H` holds L1/R1/L2/R2.

**And the corollary for CONSTRAINTS, not just for sweeps:** a constraint written as *“`INV`: non-inverted, all 12”* or *“de-emphasis: OFF”* is **unimplementable in one access and nothing says so** — `INV` spans `05H`+`0CH`, `DEM` spans `01H`+`0AH`+`0EH`, and `ATT` spans **eight** registers (`03-04H` + `0F-14H`). **Both would be ‘satisfied’ by a firmware author who wrote one register and stopped, and the verification would agree with them.** A constraint on a split field must name every register, or it is not checkable.

**M21 — A FIX RESTORES THE CHANNEL; IT DOES NOT RE-CLOSE WHAT FLOWED THROUGH IT WHILE IT WAS
BROKEN.** *(Review A1, 2026-08-16 — accepted, and the enumeration it demanded is below.)*
When a cheap indicator turns out to have been lying, the indicator is the small half of the
problem. The large half is **every conclusion that consumed it**, which is still carried as done.
F53 fixed the export; it did not re-validate anything that had been checked against an export.
**So the second question is mandatory and it is a short list: which closed items took the broken
artefact as their evidence?** Ask it *before* moving on, because if the answer is "nothing
load-bearing" it costs ten minutes, and if it is not, the cost only grows.

**F53's enumeration, run 2026-08-16 — result: nothing load-bearing flowed through it.**

| Closed item | Artefact it actually consumed | Affected? |
|---|---|---|
| DL-14 symbol eyeball set (4 parts) | **SVG export of the symbol library**, per-symbol — not a sheet PDF, so paper size never applied | No |
| Convention 6's five-part **footprint** eyeball | — | **Never performed at all.** `hw/lib/ODSP12.pretty` is empty; no `.kicad_mod` exists. It was not done badly, it has not been done |
| Every M6a driver-to-receiver walk | **`kicad-cli sch export netlist`** — recorded explicitly as *"verified by netlist, not by ERC"* | No |
| ERC / DRC results | JSON reports | No |
| Every [VERIFY] closure | **Vendor** PDFs rendered with `pdftoppm` — someone else's document, not our export | No |
| *"PDF export renders 10 pages, proof KiCad traverses the hierarchy"* | Our export | **The only one.** And its actual claim survives: a 10-page PDF does prove traversal into all nine child sheets. **Clipping cannot forge a page.** What failed was reading it as a *content* check, which is the tell, not the conclusion |

**Nothing was handed upward as a PDF**, and `out/` is git-ignored, so no exported sheet has ever
been review evidence. **The one thing this did cost is G7's on-sheet half** — the notes were absent
from the deliverable — and G7 was never claimed.

**M20 — A CLAIM THAT CARRIES A FIGURE'S NUMBERS IS NOT A READ OF THE FIGURE. Values extract;
TOPOLOGY DOES NOT.** *(Review A6, 2026-08-16 — accepted, and it generalises two of this project's
own failures.)* T1-103 recorded AKM Figure 76's every component value and **missed that the
circuit was differential** — which is the fact that decided the whole stage. F53 is the same shape
one stage later: the export carried the page *count* and lost the page *contents*. **A T1 promotion
sourced from a figure must state WHICH OF THE TWO it read** — values, structure, or both — because
"read at figure level" currently reads as if it certified both and certifies neither.
**Testable, not merely asserted:** it predicts other figure-sourced T1s carry numbers without
structure. **Sweep run 2026-08-16: of 108 T1 rows, 23 cite a figure and 14 carry no structural
language at all.** Most of those are pin-map or single-parameter reads where **there is no topology
to miss** — but *the citation format cannot distinguish "no structure present" from "structure not
read,"* and **that is the finding**, not the count. One is worth naming: **T1-31 cites BM83 Figure
7-4, "Recommended Keep-out Area for PCB Antenna," and records only that a keepout is mandated —
the geometry, which is the entire content of that figure, is still open as V-12.** The rule
predicted a real gap on its first application, which is the corroboration it needed.
*(The first number written here was "3 of 27", guessed before the sweep was run and corrected by
running it. Logged rather than quietly replaced — M19 binds the person applying it.)*

**Symmetric extension, contributed by the adversary against their own error (004):**
> **A note read without its table's conditions is as incomplete as a table read without its note.**
> Values, structure, and conditions are three separate reads; citing one does not evidence the others.

Their A4 retraction took p.9's Note 10 as an exact identity, concluded the min/max column could only be
the reference range, and never checked it against the reference's own spec one page earlier. **Fourth
instance of *the artefact was not what the check thought it was*** — T1-103, F53, the note-overlap below,
and this. **And a fifth read is now named: the CITATION.** T1-111 first cited "Note 11" because the table
*row* carries that marker while the note itself is Note 9 — p.8's notes run 6–9 and stop, and Note 11 is
on p.9 and is about PSRR.

**M19 — AN ADVERSARIAL REVIEWER'S FINDING IS EVIDENCE, NOT A VERDICT. The tier rules apply to it
completely unchanged.** *(Operator, 2026-08-16, on the arrival of a review agent.)*

A finding arrives at **T2 at best** and rises only on evidence — the file, the netlist, the
datasheet. Never on the reviewer's confidence, never on repetition, never because it was
uncomfortable to hear. `CLAUDE.md` §5 already names the failure mode: **a wrong number accepted
politely becomes a T1 that is not true.** A reviewer is a new inlet for exactly that, and an
adversarial one is *designed* to produce claims faster than they can be checked.

**Handle by direction, asymmetrically — the two directions are not equally informative:**
- **"This is wrong"** → reproduce it as a command against the artefact *before agreeing and
  before disagreeing*. Agreement is as expensive as dismissal when it is unearned.
- **"This is fine", or silence** → **closes nothing.** *Absence of a finding is not a passed
  check.* No gate closes on a reviewer's approval; §2's gates close on tool output or the
  operator's own glance, and that list has not changed.

**Check the finding's ASSUMPTIONS before its conclusion** — §5's upstream-first rule, which bites
harder here than anywhere, because a reviewer working from the artefact must **reconstruct intent**
and this board is unusually full of things that look wrong and are logged as deliberate: R<sub>BP</sub>
at 10 MΩ · R<sub>B</sub> returning to `GND` rather than `AGND_REF` · no clamps at the ADC pins ·
the relay's fail direction · `U6/U8/U9_PG` disabled by the PGFB→OUT disposition · testpoints in
their own column · `VDD18` typed `power_out`. **Each has a written reason. A finding that names one
is answered by citing the reason — but only after confirming the copper still matches it.**

**And that caveat is the more expensive half, because it has already happened here three times.**
"It is in the notes" does **not** mean the file agrees with the notes. F40 (every LT3045 programmed
to 7.5 mA), both AK4458s answering at 0x11, and testpoints that were labels rather than components
were all cases where the written intent was correct and **the artefact was not**. So: **a finding
against a documented decision is checked against the FILE, not against the document.** A reviewer
who cannot see the reason may still have found a real defect in the thing the reason describes.

**Two classes a reviewer cannot resolve, and must not be allowed to:**
- **⬜ UNSET slots.** An outside proposal to fill one is not a resolution — it is precisely the
  inference §0 forbids, arriving with more authority than usual because it is framed as a review.
- **[HARD] decrees.** A well-argued objection is an **escalation to the operator**, never an edit.

**Give them the source, not my summary.** `CLAUDE.md` §3 already classes my own digests as
advisory-only; that applies with more force when someone else will act on them. Answer context
requests with file and section so the reviewer reads the thing itself.

**Every finding lands in §7 with its verdict and the evidence — including the refuted ones.**
A refutation that is not written down gets re-raised, and the second time it is harder to argue
against because it now looks like independent confirmation.

**M18 — A DECLARED CONTAINER IS NOT A CHECKED ONE, AND EESCHEMA DRAWS OUTSIDE ITS OWN FRAME.**
Every sheet declared `(paper "A3")` — 420 × 297 mm — while seven of nine ran content to as much as
1050 × 884 mm. On screen nothing looked wrong, because the editor renders past the frame quite
happily. **The PDF export clips to the page**, so the exported schematic silently dropped the
AK5574, both INA1650s' surroundings, every decoupling network — **and all forty on-sheet notes,
which is to say every M7 inequality this project has written.** The convention that "the number
that makes this legal goes *on the sheet*" was defeated for four sessions by a one-line property
nobody checked. **The tell:** `STATE.md` recorded *"PDF export renders 10 pages, which is the
proof KiCad traverses the hierarchy"* — a page **count** was read as if it were a content check.
That is habit 2 ("verify the artefact, not the receipt") failing on the very artefact cited as
proof. **Countermeasure, and it is not a bigger constant:** the generator **derives** the page from
its own content extent and **asserts** the fit, so a sheet can never again outgrow its paper
silently. Generalised: *when a format declares a container — page, buffer, envelope, budget — the
declaration is an assertion to be run, not a fact to be trusted.*

**M17 — Reference-designator uniqueness is an unstated assumption that every downstream
artefact relies on, and generated sheets bypass the annotator that normally enforces it.**
`Q1` was both the SEPIC FET and a mute shunt; `K1` was both a range relay and a mute photoMOS.
**It would have survived every electrical check and detonated at assembly** — a BOM with two `Q1`
rows is resolved by whoever is loading the pick-and-place, silently and in their favour. ERC does
not check it, the netlist does not care, and the schematic looks correct on every sheet
individually. **Countermeasure: a hierarchy-wide refdes audit as a closing ritual**, beside M6a's
end-to-end net walk. 438 instance refs, zero duplicates, and the check takes one command.

**M16 — Stock symbols carry vetted GEOMETRY, not vetted electrical TYPES.** DL-14's stock-first
ordering was a *drawing* economy and it never certified pin types. Four instances now prove the
stock library's types are drawn from idiom rather than from pin-function tables: `D_TVS`
(bidirectional symbol for a unidirectional part), `ADS1015` `ALERT/RDY` typed `Output` where the
datasheet says open-drain, and — on this project's *own* symbols — `VDRIVE` and both AKM `VDD18`
pins typed `power_in` when they are outputs. **Rule: every stock symbol's pin types get checked
against the pin-function table at adoption, to the same standard as a project symbol.** Cheap,
because it is once per part, and the failures are silent — a mis-typed pin either hides a real
conflict or invents a false one, and both cost more than the check.
*Corollary that keeps recurring:* **type a pin for how the datasheet says to USE it.** A pin the
datasheet tells you to tie to a rail is a terminated node, not a driver; an alternate function you
do not use should not set the type.

**M6a — The closing ritual: one end-to-end walk per sheet, on the control and I2C nets.**
Coverage assertions see omission; **only a trace from one end to the other sees misassignment**,
and the PCF8574's swapped SDA/INT proved it inside an hour of M6 being cited. So it becomes a
*closing* step rather than a debugging response: at sheet close, walk every control/I2C net from
its driver to its receiver — the same rail-to-pin trace that caught F41, applied to signal nets.
**Cheap exactly once per sheet, and it is the only check class that sees a net wired to the wrong
correct-looking pin.**

**M15 — Synchronising the wire does not synchronise the stream.** Slaving the BM83's I2S port to
our clocks makes the *interface* synchronous; the A2DP stream remains asynchronous by nature, and
§3's ASRC is what absorbs the difference. **The predictable "simplification" — delete the ASRC,
the port is slaved now — is F1's error on a different path**, and it is most likely to be proposed
precisely when the board works, because that is when the ASRC looks redundant. Generalised:
**a clock relationship at the connector says nothing about the rate relationship at the source.**
Written as a sentence on the sheet, not only here, because that is where the proposal will arrive.

**M12 — An elimination carries its evidence and its scope, exactly like a promotion.** *(operator,
2026-08-16.)* The project already tagged every T1 with how it was verified; **eliminations had no
such discipline**, and F44(b) is what that costs — "ruled out" entered the record as a bare verdict
and survived because nothing prompted a re-read of its basis. **Every "ruled out" now travels with
(a) the evidence that ruled it out and (b) the scope that evidence covers**, so it is re-openable by
a scope check rather than by luck or by a second party happening to hold different data.
*The held-for-elimination datasheet practice was half of this* — the document was kept, but the
*claim* was not tagged, and the claim is what gets consulted. **Concretely:** a wrongly-eliminated
option is worse than a wrong number, because a number gets re-derived when something downstream
disagrees with it, while an eliminated option is simply never revisited — nothing downstream
depends on it, so nothing can contradict it.
*It paid immediately:* the very next round, `SM8S24AHM3`'s own datasheet also says
*"Unidirectional"*, so a bidirectional member remains **unverified rather than disproven** — a
distinction M12 forces and the old habit would have collapsed in whichever direction was convenient.

**M11 — A superseded document is authoritative about the past, not about its redirect target.**
`sm8s.pdf` says *"available in unidirectional polarity only"*, and that sentence is **true of the
SM8S10A–43A family it describes**. It was carried forward as a fact about the **AHM3 successors**,
where it is false — a parallel **SM8S10CA–85CA** bidirectional series exists. **An NRND datasheet
is structurally incapable of describing what its replacement added**, so its scope statements
expire at the redirect boundary while its numbers do not.
*The tell — and it is the same one as T1-28 and M1a:* **a claim inherits the scope of the heading
it was read under**, and here the heading was the document itself. When a document names a
successor, every "only", "never" and "not available" in it is scoped to the old family and must be
re-read against the new one before it can be used to eliminate an option.
*Cost of the miss:* it eliminated a design route (bidirectional TVS ahead of Q2) that is in fact
available — the most expensive kind of error, because a wrongly-eliminated option is never
revisited. Caught only because the operator held distributor evidence from the successor family.

**M10 — A worst-case number quoted outside its test condition is not conservative, it is wrong.**
**Generalised: conservatism is a property of an *analysis*, not of a number — a number is only
conservative at its stated conditions.** Transplanted elsewhere it is simply a different number,
and its error has whatever sign the transplant gives it. **Safe-direction errors are the dangerous
ones**, because they survive review by looking like prudence: the 44 V phantom would have sat in
the document forever as margin nobody audited, and the part change it justified would never have
been questioned. *Practical form:* when a figure is doing work, write its test condition beside it
— and when it crosses into a new analysis, re-derive at the new operating point rather than
carrying the endpoint.
The SM8S24A's 38.9 V clamp is specified **at I<sub>PPM</sub> = 170 A**. Carried into an analysis
where the real current is 12–48 A, and then scaled by the breakdown tempco, it says 44 V and
condemns a design whose actual worst case is **34.2 V**. The fix is structural: **datasheet
maxima come with test conditions, and the condition travels with the number or the number does
not travel.** Where a part gives a slope — here r<sub>d</sub> = (V<sub>C</sub> −
V<sub>BR</sub>)/I<sub>PPM</sub> = 63.5 mΩ — use the slope at the operating point, not the endpoint.
*Why it belongs beside M7:* both are about running numbers against reality rather than reciting
them, and this one bites in the **safe** direction, which is worse — an over-conservative wrong
number gets rewarded with a part change nobody questions.

**M9 — A guard that has never fired is itself unverified.** You do not know an assertion checks
what you think it checks until you have fed it a known failure. The F41 collision guard was made
to fire on a synthetic duplicate *before* its green was believed — mutation testing in miniature,
and the enforcement clause M5 and M6 were missing. **The vacuous-completeness family has five
instances precisely because the guards that would have caught them were assumed to work.**
*Applies to:* every new assertion, every new lint, every new check-script. Show it a defect it
must catch, watch it fail, then trust its pass. The cost is one throwaway test; the alternative is
a green light that means nothing and is believed for months.

**M8 — Near-symmetric parts are more dangerous than unrelated ones, because the mistake is
*productive*.** The LT3045 and LT3094 are sold as a matched ± pair, share the SET architecture,
the 100 µA reference, the 0.8 µV<sub>RMS</sub> figure and the `DD` package suffix — and differ in
**lead count (10 vs 12), exposed-pad net (GND vs IN), pin order (ILIM/PGFB/SET vs PGFB/ILIM/VIOC)
and current-limit scale constant (150 mA·kΩ vs 3.75 A·kΩ, a 25× difference)**. Every one of those
is invisible if the negative channel is drawn by mirroring the positive one, and mirroring is
exactly what a symmetric supply invites. *The tell:* when two parts are marketed as a pair, look
for what the marketing flattens — **verify the sibling independently, at figure level, and never
by diff against the one you already read.** Recorded as a rule because the same shape recurs
wherever a vendor ships an inverting/complementary/mirror variant.

**M7 — A design rationale is also a test, and consequences are cheaper to check than
derivations.** Every constraint written down is a check that can be **executed against the
artefact** — and executing them is not the same as having written them. The `RT` error was caught
**not** by re-deriving the RT-to-frequency relation, but because a **consequence** of the value
(fundamental lands at 360 kHz) contradicted a **recorded requirement** (stay above the AM band).
*Why this compounds:* the document is now full of consequences. **It gets more protective as it
grows, not merely longer** — provided the constraints are periodically run against the artefact
rather than only consulted when someone remembers them.

**M6 — Ask of any passing check: "what failure would this not have caught?"** A check is only
sensitive to the failure modes it was designed around. **Completeness checks see omission, never
misassignment** — a pin-set assertion cannot see a permutation, so a symbol with every net wrong
and nothing missing passes it cleanly. **The general shape of the bug is extracting correlated
fields in separate passes and zipping them**; it recurs in every scraping context, not just
symbols. The countermeasure is structural: extract correlated fields **as pairs from a single
match**, so a dropped entry loses one whole record instead of shifting every record after it —
and verify the pairs against a figure-level read, not the sets.

**M1 — Confidence attaches to the method, not the claim.** When a method is known-ragged, *every*
claim it produced inherits the raggedness, **including the ones later verification happens to
bless.** The T1-28 retraction and the `00100`-prefix suspicion came from one careless grep in one
pass; one was false and one was true, and nothing in the output distinguished them. The response
to a broken claim is therefore to **re-derive everything the method touched with the better
method**, not just the claim that broke.

**M1a — the third instance, logged because it proves the rule was needed.** T1-25 said pin 34
`SELFBOOT` selects the self-boot *protocol* by float-vs-pulldown. It does not — **pin 26**
(`SS_M/MP0`) does, and pin 34 merely enables self boot. Same failure as T1-28: a grep crossing
table rows, attributing one row's sentence to another's mnemonic. It was caught by exactly the
method M1 and M2 prescribe, one round after they were written. **F21's disposition survived
unchanged** — pin 34's internal pull-up still means an unstuffed strap boots from an absent
EEPROM — so the conclusion was right for a wrong stated reason, which is its own hazard: a correct
conclusion is not evidence that the reasoning under it was sound.

**M2 — A T1 promotion records the method that produced it.** Provenance is part of the fact, so a
later reader can see "ragged grep" in the citation and discount accordingly. `STATE.md` §1's
"Verified by" column is that field; it is not decoration. Load-bearing claims get a figure-level
read *before* T1 status, not after something downstream breaks.

**M3 — Guarantee by construction, then test that the construction holds.** Acceptance tests are
for what design cannot guarantee. Anything guaranteeable by construction should be, and then
checked cheaply — the F15 cross-DAC alignment rule is one register comparison at boot, not a
bench measurement. Cheaper, and it fails loudly instead of subtly.

**M4 — A decree can be right for reasons its author did not know.** §5's "strap consistently to
I2C" was written for control-plane coherence; it also happened to dodge the AK5574's
I2C-block-active-during-3-wire drive-conflict hazard (T1-33), which neither party knew about when
the decree was written. **Route around a decree and you may be discarding reasons nobody has
articulated yet.** This is why the escalation ladder exists rather than a judgement call.

### Caught on this project

**"28 RCA-class jacks will dominate your board edges"** — assistant, 2026-08-15
*Correction:* **17 populated, 18 positions.** 4 line in + 12 out = 16 RCA, +1 SPDIF coax in,
+1 DNP SPDIF out. The error was pure arithmetic: `STATE.md` Q34 already read "RCA jacks (16 of
them)" — a subtotal containing the outputs — and the 12 outputs were then added to it a second
time in chat.
*The tell:* **the same count existing in two places with two values, where the larger one was
never written as its addends.** A total is an assertion; a sum is checkable. Any count that
steers a decision gets written as `4 + 12 + 1 + 1`, in the document, not as `28` in prose.
*Second tell, and the more useful one:* the operator's first hypothesis was interesting — that
differential inputs were being counted as jack pairs — and the truth was boring. `CLAUDE.md` §5
says to check ordinary human error before building an exotic theory when *operator* data looks
anomalous. **The rule is symmetric.** When the assistant's number is challenged, the first
candidate is a slipped digit or a double-count, not a subtle modelling difference.
*Standing:* the underlying point survived at 18 — connectors still dominate the board edge, and
board-mount vs. flying-lead RCA is still an early decision (Q34). **A conclusion that survives its
own broken evidence is not thereby vindicated;** it was re-derived, and the re-derivation is what
it now rests on.

**"A grep hit is a fact about the part"** — assistant, 2026-08-15, retracting T1-28
*Correction:* it is a fact about **one line**, and a line in a multi-mode datasheet is scoped to
whichever mode's section it sits in. "Chip address (1bit, C1 is fixed to 0)" was pulled from the
AK4118A and filed as its I2C addressing. It is the **4-wire serial mode** description, twelve
lines under a heading the grep never showed. In I2C the part has full CAD1/CAD0 like its
siblings. **A wrong T1 sat in the fact base for one round**, and it was load-bearing — F23's whole
"the address space may be too narrow" framing was built on it.
*The tell:* **a spec extracted from a datasheet that documents more than one interface mode.**
AKM, TI and ADI parts routinely describe I2C, SPI and parallel control in adjacent sections using
the same vocabulary. Before a control-interface fact becomes T1, confirm the **section heading it
lives under**, not just the sentence — `grep -B` to the nearest heading, or render the page.
*Second-order:* the earlier `00100`-prefix suspicion came from the same ragged grep and happened
to be **right**, which is worse, not better — one careless method produced one true and one false
belief in the same pass, and nothing in the output distinguished them. This is why
`CLAUDE.md` §5 says a claim rises a tier on evidence, never on having been useful.

**"An unconnected pin is an undefined pin"** — 2026-08-15, from F21
*Correction:* `SELFBOOT` floating is not undefined — a 250 kΩ internal pull-up makes it a
**chosen** state, and the state it chooses is *boot over SPI from an EEPROM that is DNP on v1*.
An unpopulated strap would have silently selected a boot path to a part that is not on the board.
*The tell:* **floating is a state someone chose. Find out who and why before trusting it.** Every
strap, mode and configuration pin gets its idle level read out of the pin table and stated in the
schematic — an unfitted resistor is a decision, not an absence.

**"A PowerShell round-trip through a text file is lossless"** — assistant, 2026-08-15
*Correction:* Windows PowerShell 5.1 `Get-Content -Raw` reads a UTF-8 file **without a BOM using
the system ANSI codepage**. Every multibyte character becomes separate CP1252 characters, and
`Set-Content -Encoding utf8` then writes that mojibake back as valid UTF-8. One
read-modify-write **double-encoded 204 characters across the whole file** — and it silently
"succeeded". Recovery was `git checkout` plus re-applying the edits through the Edit tool.
*The tell:* **any read-modify-write of a text file through PowerShell 5.1.** Use the Edit tool for
file edits; reserve the shell for running programs, which is what `CLAUDE.md` §7 already implies
and this made concrete. If a shell round-trip is truly unavoidable, force encoding on **both**
ends — and a blanket reverse is not a fix once new correctly-encoded text has been mixed in.
*Why it was cheap:* the damage was one commit deep, so `git checkout` cost only re-work. That is
DL-15 earning its keep on the same day it was made — and an argument for committing before any
bulk edit, not only after.

**"The revision history protects the document"** — assistant, 2026-08-16
*Correction:* it protects everything **except itself**. `REQUIREMENTS.md` carried F30–F34 while its
header still read v0.9 and the v1.0/v1.1 rows did not exist — the mechanism that exists to stop a
version being merged silently had itself merged silently. **The integrity check that guards
everything else has no guard of its own**, and the only thing standing behind it is commit
discipline: the version bump belongs in the same commit as the content it describes, never as a
follow-up.
*The tell:* content edits and the version header living in **different edits**. If a change is
worth a revision row, the row goes in before the content does, not after.

**"A plausible-looking component value is in the right ballpark"** — assistant, 2026-08-16
*Correction:* I placed **`RT = 36.5 kΩ` as "a ~2.1 MHz starting point."** The LM61460's RT-to-
frequency relation is **inverse**: 5.76 kΩ → 2.2 MHz, 33.2 kΩ → 0.4 MHz, 66.5 kΩ → 0.2 MHz.
36.5 kΩ gives roughly **360 kHz — inside the AM broadcast band**, on a **car audio** board whose
antenna is feet away. Off by ~6×, in the one direction that matters.
*The tell:* **a value stated with a frequency next to it that was never derived from the
datasheet's own table.** "Starting point" is not a tier — it is an untagged T4 wearing a number,
and `CLAUDE.md` §5 says speculation never enters a document untagged.
*What caught it:* being asked to **apply the reasoning to the number**. The operator's AM-band
argument existed already; running it against the placed value is what exposed the error. **A
design rationale is also a test** — every constraint written down is a check that can be executed
against the artefact, and executing them is not the same as having written them.
*Now:* `RT = 5.76 kΩ`, a **datasheet-specified point** (2.2 MHz typ, 1.98-2.42 MHz) rather than an
interpolation. Worst case under ±2 % spread: 1.98 × 0.98 = **1.94 MHz, still clear of 1710 kHz.**

**"The completeness assertion passed, so the part is fully connected"** — assistant, 2026-08-16
*Correction:* the F28 assertion is `set(pin_geometry) - set(assigned_nets)`. My pin-extraction
regex required a newline that **this project's own compact symbol format never emits**, so
`pin_geometry` came back **empty** for all three project symbols — and an empty set has nothing
missing. **The assertion passed vacuously and three LM61460-Q1 bucks were placed with every pin
unconnected**, which the netlist showed as 14 `unconnected-(U3-…)` stubs.
*The tell:* **an assertion over a set you did not also assert is non-empty is not a check.** Any
"nothing is missing" test needs a companion "and there was something to miss." Both guards are now
in: `assert pins` at extraction, `assert geo` at placement, plus `assert not extra` to catch a
stale pin map pointing at pins that do not exist.
*Family:* ERC on an empty sheet, `file` reporting 10 pages, HTTP 200 on the wrong PDF. **Fourth
instance of a check that answers the question it was asked while the thing it guards is absent.**

**"Zip the names and the numbers"** — assistant, 2026-08-16, caught before it shipped
*Correction:* I extracted stock-symbol pin names and pin numbers with **two independent regexes
and zipped the results.** Where either list dropped an entry — and both did, on `NC` pins and
duplicated `IN`/`GND` pads — every subsequent pair silently **shifted by one**. It produced a
complete-looking map in which the LT3045's `EN/UV` was pin 2 instead of 3, `PG` was 3 instead of
4, and so on down the part. Had the two lists happened to be the same length, **the pin-set
assertion would have passed and every net on the part would have been wrong.**
*The tell:* **pairing data from two separate passes over the same source.** Extract name and
number from **one match**, so a dropped entry loses the whole record rather than shifting the rest.
*Why it matters more than it looks:* a pin-set assertion checks **completeness, not correctness.**
It cannot see a permutation. This is the M1a shape — the check passed, the reasoning under it was
unsound — and the only reason it surfaced is that the lists were *unequal*.

**"The file parsed, so the file is right"** — assistant, 2026-08-16
*Correction:* the first `02_dsp.kicad_sch` **parsed cleanly, passed ERC with zero violations, and
exported as part of a 10-page PDF — while containing no components at all.** Every available check
said fine except the one that mattered. The cause was that `lib_symbols` sub-symbols had been
given the `LIB:` prefix that belongs only to the parent (`CM5IO:C` contains `C_0_1`, not
`CM5IO:C_0_1`), so KiCad silently discarded every instance.
*The tell:* **for a schematic, the artefact is the netlist, not the file.** ERC on an empty sheet
is vacuously clean; a PDF of an empty sheet still has the right page count. Verify by extracting
**pin-to-net connectivity** and checking it against intent — `+1V2_CORE` must reach pins
20/35/53/71, or the sheet is decoration.
*Family:* this is the same species as *"a download that returned 200 is the document I asked for"*
and the `file`-says-10-pages artefact. Three instances now of **a cheap indicator standing in for
the actual thing**. The rule that keeps earning: check the payload, not the receipt.
*What resolved it:* reading a real KiCad 10 schematic from `share/kicad/demos/` rather than
reasoning harder about the format — DL-13's "T1 only from the tool" applied to file format as
well as CLI flags.

**"A download that returned 200 is the document I asked for"** — assistant, 2026-08-15
*Correction:* an LCSC URL for the ADAU1466 returned **HTTP 200, a `.pdf` extension and a
plausible 47 KB** — and the content was an **HTML page for a Toshiba TLP185 optocoupler**, an
unrelated part from a different manufacturer. Had it been filed unchecked, the V-01 gate would
have shown as satisfied by a document that never mentions the part.
*The tell:* **verify the artefact, not the transfer.** Page count and first-page text against the
expected part number, every time, before a file is recorded as held. Transfer success is a fact
about the network; content correctness is a fact about the document, and only the second one is
what was wanted.
*Second instance, same class, same day:* `file` reported "10 page(s)" for every TI PDF — a
linearized-PDF artefact, not the truth. Both errors are a **metadata proxy trusted over content**.
When a cheap indicator and the actual thing can disagree, read the actual thing.

**"The zero-energy requirement excludes enhancement-mode devices"** — assistant, 2026-08-15
*Correction:* it excludes them **in a shunt**. In **series** the polarity inverts — unpowered, an
enhancement-mode device is open, and an open series path is mute. Form A photoMOS, ruled out one
sentence earlier, is the correct series element. The exclusion was a property of the **topology**
and was stated as a property of the **device class**, which closed a design space that was open,
and left a real depth-vs-capacitance conflict looking irreducible when it was only irreducible
*for a shunt*.
*The tell:* **a conclusion that names a component class rather than a configuration.** Fail-safe
polarity is topological. Any statement of the form "X devices are excluded" must be re-read as "X
devices are excluded *here*" and then tested in the other topology before the space is declared
closed.
*The sharper tell:* this happened **immediately after** correctly solving the shunt sub-case. The
frame that produced the sub-answer was carried forward without re-deriving. Solving a sub-case is
the moment of maximum risk for over-generalising from it — the reasoning is fresh, fluent and
still scoped to conditions that are no longer stated aloud.
*Cost if uncaught:* the design would have gone to capture with a single-device shunt, a
constrained part search that probably fails, and relays waiting as the fallback — carrying 0.5 A
and a watt of coil heat, forever, to solve a problem that two cheap parts solve better.

**"An acceptance criterion covers the failure mode it was written for"** — corollary, 2026-08-15
*Correction:* it covers the failure mode **at the stimulus and frequency it specifies**. §12's
1 kHz THD is blind to nonlinear off-capacitance because the mechanism is negligible at 1 kHz. The
obvious repair — test THD at 20 kHz — is *also* blind, because the harmonics land at 40/60 kHz,
outside the measurement band. Only a stimulus whose distortion **product** falls in band catches
it: CCIF 19 + 20 kHz, product at 1 kHz.
*The tell:* when a new failure mode is identified, ask **which existing criterion would catch it**
and at what stimulus. If the answer is "none, as written", the criterion needs amending — and
amending it means choosing the test, not moving the number. A number tightened at a frequency
where the mechanism is silent buys nothing and reads like diligence.

**"Mute is a state the MCU commands"** — implicit in v0.1 §7.2/§7.3, corrected 2026-08-15
*Correction:* the sequenced mute is the **orderly** path. Rails also collapse by crank sag, blown
fuse, harness fault and pulled connector, and none of those involve the MCU. **Mute must therefore
be the zero-energy state** (T1-D34), which decided the topology outright — it ruled out latching
relays entirely and every enhancement-mode device by construction, before THD was even considered.
*The tell:* **a requirement written as a sequence.** A sequence describes what happens when things
work. Ask what holds the requirement when the sequence never runs — and treat any answer of the
form "the controller sets it" as a gap, because the controller is powered by the thing that just
failed.

**"The EDA tool's CLI and Python API work the way I remember"**
*Correction:* the install is **KiCad 10.0.5**, which postdates this assistant's training. `pcbnew`
has broken API compatibility across major versions before, and CLI flags have moved. Everything
recalled about KiCad tooling is **T2 from memory and T1 only from `--help` or `dir()`.**
*The tell:* a version number higher than any release you can recall notes for. That is not a
detail — it is the whole basis of your confidence about the interface evaporating, silently.

### Pre-seeded from this project's own source document

**A [HARD] flag makes a requirement binding, so it must be right**
*Correction:* [HARD] is a statement about **authority**, not about correctness. `REQUIREMENTS.md`
§3 carries two [HARD] bullets that cannot both be built (F1). Binding and correct are independent
properties, and where they diverge the answer is a logged finding and a question — never a silent
choice between them.
*The tell:* two requirements that are each individually sensible but name the same interface from
opposite ends. Read every clock, bus, and power statement **from both peers' point of view**
before accepting it.

**The board envelope is the board outline**
*Correction:* "≤ 200 × 140 mm" (§11) is a **maximum**, offered as an assumption in the section
titled *Open Items*. It fixes no edge, no origin, no mounting hole and no connector position.
Placement against it would be placement against nothing.
*The tell:* a dimension that arrives with "assume" or "unless told otherwise" attached. That is
an unknown wearing a number.

### Carried forward from previous boards — read before starting

These recurred across a full board build and are not project-specific.

**Netclass track width is a minimum**
*Correction:* netclass widths are **defaults for newly drawn track**, not minima. The floor is the
board minimum. A 1.0 mm trace and 0.8 mm via cannot attach to a 0.25 mm pad on a 0.5 mm-pitch
package. Traces neck at the pad and widen in open copper.
*The tell:* a connection between two **adjacent pads of the same package** failing to route. That
is never topology; it is always width or clearance.
*Live risk here:* T2-03 puts a 0.5 mm-pitch LQFP on this board alongside a ±13.5 V rail that wants
wide copper.

**Via-in-pad is an electrical rule**
*Correction:* it is a **manufacturing** rule — solder wicks down the barrel during reflow — so it
applies **regardless of net**. Clearance checks correctly skip same-net copper, which lets a GND
via land happily on a GND pad. Nets are irrelevant to that check; test every pad.

**Pre-placing helper copper makes the router's job easier**
*Correction:* it makes it **impossible**. Plane stitching, fanout vias and escape stubs become
**fixed wiring** the router cannot move or rip up, and they sit exactly in the escape corridors.
Two independent routers plateaued at the identical completion percentage because of it.
*Correct order:* **route first, stitch the residue afterwards**, where the free space is known. The
same stitching code that caused 145 violations before routing caused zero after it.

**Critical nets can be routed last**
*Correction:* impedance-controlled pairs, crystal nets and RF feeds must be routed **first, on
empty copper**. Anything routed earlier takes the corridor they need, and carving it back out just
displaces the next net into it.
*Live risk here:* MCLK_XO and the four MCLK fanout branches, plus the SPDIF 75 Ω path, are the
first-routed nets on this board.

**Placement may fill the space in front of fine-pitch pads**
*Correction:* reserve an escape corridor in the **placement** stage. Without it the packer parks
decoupling caps where the differential pairs must escape, and the failure only surfaces during
routing.

**An obstacle model built from pads sees the whole board**
*Correction:* it must also read existing **tracks and vias**, or each pass is blind to the copper
the previous pass laid down. Symptom: violations between objects the tool itself created, always
at pass boundaries, never within a pass.

**Grid quantization is a rounding detail**
*Correction:* rounding to nearest lets an obstacle be modelled **smaller than it is**. Round
**outward** — floor the low edge, ceil the high edge, inflate discs by the cell diagonal — and use
`ceil` for dilation radii.
*The tell:* clearance violations whose actual value is just under the rule (0.1485 against 0.150).
Systematic near-misses are a model error, not luck.

**Geometry checks can ignore layers**
*Correction:* a bottom-layer trace obstructs nothing on the top layer. A layer-blind check will
confidently name an innocent object as the blocker.

**A bare `except: pass` around an API call is harmless**
*Correction:* if the call raises on *every* invocation, the fallback is not a fallback — it is the
only path. A silent fallback that fires 100 % of the time is indistinguishable from a working call.
If an except branch substitutes defaults, it must **count and report** how often it fires.

**Bool-returning API calls succeed**
*Correction:* several EDA scripting calls report failure as a **return value**, not an exception.
An import that silently returns `False` looks exactly like one that did nothing. **Check the
return value of every one.**

**A footprint needs only a reference, value, position and pads**
*Correction:* without a library id it exports to Specctra as `(component "")` and the returned
session can never be matched back — the import fails silently. Always set a proper FPID on
programmatically created footprints.

**More autorouter passes means a better result**
*Correction:* a good autorouter self-terminates on its own convergence criterion. Forcing 3× the
passes produced a *worse* result. When it stops improving, the limit is placement and topology,
not effort.

**"The search found nothing" is a fact about the board**
*Correction:* it is a fact about **the search**. A coarse lattice sampled six points under an
exposed pad, hit routed traces at every one, and reported no room for thermal vias — a fine scan
found fifteen.

---

## 6. Decision log

| ID | Date | Decision | Evidence tier | Reopens if |
|---|---|---|---|---|
| DL-01 | 2026-08-15 | Install the constitution before board details, with unknowns marked ⬜ UNSET rather than defaulted | Operator instruction | Operator asks for provisional defaults instead |
| DL-02 | 2026-08-15 | G0 (intake) gates G1–G7 | Reasoning from `CLAUDE.md` §5 | — |
| DL-03 | 2026-08-15 | Do not infer the EDA tool from the template's KiCad references; hold at T3-01 pending Q6 | `CLAUDE.md` §0 | Operator states the tool |
| DL-04 | 2026-08-15 | **G0 split into G0-S (schematic intake) and G0-L (layout intake).** Capture proceeds on the electrical architecture; layout waits for mechanical and fab | T2-10 | A mechanical or fab constraint arrives that changes part selection, not just placement |
| DL-05 | 2026-08-15 | `REQUIREMENTS.md` v0.1 committed to the repo verbatim as the §3 requirements authority; findings logged in §7 rather than corrected in place | `CLAUDE.md` §3 | — |
| DL-06 | 2026-08-15 | The five §11 delegated decisions run **closed book** — decide, justify against stated intent, log, surface in G7. Everything else holds pending Q2 | `REQUIREMENTS.md` §11 | Q2 answers "channel open" |
| DL-07 | 2026-08-15 | Impedance targets **proposed** as 75 Ω SPDIF / 90 Ω USB diff and recorded as T2-04, **not** entered as a constraint, pending Q35 | `CLAUDE.md` §0 | Operator decrees targets |
| DL-08 | 2026-08-15 | No datasheet parameter enters the schematic from memory; §8 checklist governs | `CLAUDE.md` §8 rule 9 | — |
| DL-09 | 2026-08-15 | **Units are mm.** Chosen, not assumed: KiCad is nm-internal and mm-native, every datasheet in this BOM is mm, and the only imperial dimension in the requirements is the 0.1" header pitch = exactly 2.54 mm, which lives inside a footprint | T1-05 + `REQUIREMENTS.md` §4/§11 | Operator prefers imperial, or a mechanical drawing arrives in inches |
| DL-10 | 2026-08-15 | **G2 proven by `--severity-exclusions` returning empty**, not by a baseline file diff — the CLI exposes it directly on both DRC and ERC | T1-08 | A KiCad update changes the flag's semantics |
| DL-11 | 2026-08-15 | Project-local KiCad symbol/footprint library is the default structure; stock libs used where they cover the part | T1-09 | Operator mandates a vendor library service |
| DL-12 | 2026-08-15 | `REQUIREMENTS.md` advanced to **v0.2** under operator disposition of F1/F2/F5/F7/F8/F9/F10/F14, with a revision history rather than silent edits | `CLAUDE.md` §4 | — |
| DL-13 | 2026-08-15 | KiCad 10 CLI/API treated as T2-from-memory, T1-only-from-`--help`; verified before scripting | Ledger, this session | — |
| DL-14 | 2026-08-15 | **Footprint policy:** vendor verbatim → IPC-generated → hand-built last. Adversarial rasterise-over-datasheet verification logged per part; operator personally checks the 5-part respin set | Operator proposal, adopted | A vendor pattern is found to disagree with its own datasheet — then the datasheet wins and the finding is logged |
| DL-15 | 2026-08-15 | **git initialised**; library in-repo, not a submodule; generated output untracked but delivered fab packages committed against a tag | Operator, T1-D38 | A second board shares the library — then reconsider the submodule |
| DL-16 | 2026-08-15 | `REQUIREMENTS.md` → **v0.3** under operator disposition of F6, F11, F16 and Q38 | `CLAUDE.md` §4 | — |
| DL-17 | 2026-08-15 | **Semiconductor shunt mute is the default**, relay must justify itself — decided by the §7.4 zero-energy requirement, **not** by THD. Depletion-mode/JFET topology; part deferred to V-14/V-15 | T1-D34/D35 | V-14/V-15 show no part meets both mute depth and off-capacitance — then energised-to-unmute relays return, with the +5V_D budget consequence |
| DL-18 | 2026-08-15 | Rail monitoring on an ADS1015-class I2C ADC rather than the SoC ADC — also returns ~3 GPIO to the F13 budget | T1-D36 | — |
| DL-19 | 2026-08-15 | **DL-17 superseded: series–shunt mute.** Enhancement-mode series photoMOS + depletion-mode shunt pair, each fail-safe in its own polarity. Relays now out on merit, not on burden of proof | T1-D40, operator correction of an assistant over-generalisation | V-14/V-15 show the series part cannot meet the voltage rating, or the shunt Coff fails T1-D42 |
| DL-20 | 2026-08-15 | **CCIF twin-tone IMD added to §12**, not substituted for the 1 kHz THD line — the failure mode needed a different *test*, not a tighter *number* | T1-D42, ledger corollary | — |
| DL-21 | 2026-08-15 | Board named **ODSP-12** / `ODSP12-MB-A`; fab revisions A/B/C with the change log in git rather than rev-suffix proliferation | T1-D44 | — |
| DL-22 | 2026-08-15 | V-01 expanded to a **single-pass ADAU1466 read** covering V-07, V-08, V-13 and the firmware contract (safeload register addresses, slave-boot header format) | Operator | — |

---

## 7. Findings register

### F112 ⛔⛔ STOP-THE-LINE — §7.0's +70 °C IS EXCEEDED BY SOAK BEFORE THE UNIT IS SWITCHED ON — 2026-08-22

**F105 asked which ambient +70 °C meant. The operator answered with the environment instead, and the
environment does not fit either reading.**

**T1, operator's direct observation of the actual deployment:** **110 °F (43.3 °C) outdoor ambient,
vehicle parked in an OPEN LOT, 8–10 hours, Oklahoma summer.**

**T2, vehicle-soak literature — recalled, NOT a datasheet, and this is the number that most wants
measuring:** a closed vehicle in sun plateaus at **+22 to +30 °C above outdoor ambient** within
60–90 minutes.

    outdoor 43.3 C  +22 C  ->  cabin air  65.3 C  (150 F)   typical
    outdoor 43.3 C  +28 C  ->  cabin air  71.3 C  (160 F)   conservative
    outdoor 43.3 C  +30 C  ->  cabin air  73.3 C  (164 F)   worst reported

**Then self-heating, once powered:** a 5–12 W board in a sealed enclosure adds **+10 to +20 °C** over
local ambient. **Worst realistic operating case is the driver returning after a 9-hour soak and
switching on into a 65–73 °C cabin.**

> **§7.0's +70 °C is exceeded by SOAK ALONE, with the unit OFF, on a typical day in the stated
> deployment. It is not a margin question. The decree does not describe the environment.**

**The industry has already answered this exact question.** **AEC-Q100 Grade 3 is −40…+85 °C and is
defined as the PASSENGER COMPARTMENT grade** — the +85 °C number exists *because* of the
parked-car-in-sun case. **Our decree sits 15 °C below the grade the industry created for our
application.**

## What this invalidates — four items, two of them CLOSED

| Part | Rating | At +85 °C internal |
|---|---|---|
| **AK5574**, back tab **OPEN** | **−40…+70 °C** (T1-112) | **FAILS** |
| **AK5574**, back tab **to VSS** | −40…+105 °C | 20 °C margin |
| **AK4458**, pad **open** | −40…+85 °C (F93) | **zero margin** |
| **AK4458**, pad **grounded** | −40…+105 °C | 20 °C margin |
| **TLP3475 ×12**, signal path | **+85 °C recommended** (F103) | **zero margin, and every parameter characterised at 25 °C only** |
| **SiT1605 XO** | **−40…+85 °C Industrial** (T1-136) | **zero margin — REOPENS F56, which closed on this part** |

**★ TWO EXPOSED-PAD DECISIONS ARE NO LONGER FREE CHOICES.** F93 recorded the AK4458 pad as *"a
defaulted choice worth 20 °C — both clear the −20…+70 decree."* **That sentence was true only under
the decree that just failed.** **Both AKM pads must be grounded**, and the AK5574's is the harder
case because **tab-open is −40…+70 °C, which fails even the CURRENT decree at zero margin.**

**★ AND THE GRADE POLICY NOW CONTRADICTS THE ENVIRONMENT.** §7.0 decrees *"Not an AEC-Q board.
Industrial grade throughout the signal path."* **Industrial grade tops out at +85 °C.** At an
+85 °C internal design point, **"industrial grade" has zero margin BY DEFINITION** — the policy and
the environment cannot both stand as written.

## Disposition — ESCALATED, not applied

**`CLAUDE.md` §4 puts environment changes in the escalate class and forbids us editing
`REQUIREMENTS.md` to resolve a finding.** Recommendation, for the operator's decree:

1. **Restate §7.0 as INTERNAL AMBIENT AT THE PART**, closing F105's original ambiguity in the same
   stroke.
2. **Set the operating design point at +85 °C internal**, matching AEC-Q100 Grade 3.
3. **Require signal-path and thermally-significant parts rated to +105 °C**, so the design point has
   real margin instead of zero. This is the clause that resolves the grade contradiction.
4. **Ground both AKM exposed pads.** Forced by (2), free to do, and it buys 20 °C on each.

**★ AND MEASURE IT, because the +22…+30 °C soak rise is the only T2 in the chain.** A logging
thermometer left in the car — **in the intended mounting location** — for one working day converts
the whole analysis to T1 for about $20. **`CLAUDE.md` §5: the operator's glance beats the clever
test, and here the operator owns the actual vehicle in the actual climate.** **Recorded as
`BRINGUP.md` 4b.8.**

**F105 is superseded by this finding** — it asked which of two readings was meant; the answer is
that **neither reading of +70 °C survives contact with the deployment.**

### F109 ⛔ NO PLACED SYMBOL CARRIES A FOOTPRINT — THE NETLIST EXPORTS **0 OF 536** — 2026-08-22

**Found while starting the footprint pass, before drawing anything. T1 — `kicad-cli` output, not
inspection.**

    kicad-cli sch export netlist --format kicadsexpr  ->  536 components, 0 with a footprint

**Root cause, and it is a split between two generators that are each individually correct:**

- `hw/lib/gen_symbols.py:397` writes `("Footprint", d["fp"], ...)` into the **library symbol
  definition** in `ODSP12.kicad_sym`. **Correct, and it is why every `grep` for a footprint string
  finds one.**
- `hw/gen_sheet_*.py` emit **placed instances carrying only `Reference` and `Value`** — verified on
  `U51` (AK4458VN) in `07_dac_a`, whose whole property list is those two.
- **The netlist exporter reads INSTANCE properties.** The library definition is not consulted, so
  every footprint string on the board is in a place that no downstream tool reads.

**Consequence:** *Update PCB from Schematic* would place **nothing**, and **G1 schematic-parity is
unreachable** — not failing, unreachable, because there would be no footprints to compare.

**Why this is the finding and not the fix:** *I was one command away from drawing footprints into
`ODSP12.pretty`.* **They would have been correct, and unreachable** — a full `.pretty` library, a
passing footprint-guard suite, and zero of them attached to a part. **`ODSP12.pretty` is empty
today, so nothing is lost; had I drawn first, the defect would have been hidden behind evidence of
progress.**

> **This is M28's shape at the tooling layer: a producer whose output is correct and whose
> DESTINATION is wrong. Every check on the value passes. Nothing checks the address.**

**The mechanism fix is ours** (emit the property on the instance, inherited from the library symbol)
**and is not blocked.** **The VALUES are split:** pinned parts' footprints follow from the package
and are unblocked; **the ~500 passives need a package size, which follows from fab capability —
⬜ UNSET, Block E.** Choosing 0603 as "typical practice" is precisely the §0 drift. **So the
footprint pass proceeds on pinned parts only, exactly as scoped.**

**FIXED AND VERIFIED THE SAME SESSION, by tool output at every step:**

    netlist footprints   0/536  ->  32/536 (dac only)  ->  80/536  ->  81/536
    ERC violations         26   ->  68

**The ERC RISE is the proof.** The 42 new violations are `footprint_link_issues` naming the nine
footprints that do not exist yet. **Before the fix ERC could not raise them — not because they were
absent, but because nothing was linked. The 26 was silence, not health.**

**The fix in two parts, because the second was the same defect one level down:**
1. `FPMAP` built from the extracted symbol block, emitted onto every instance by `place()` — seven
   generators. **80/536.**
2. **`U1`, the ADAU1466, was still bare** — it is emitted by a **hand-rolled block in
   `gen_sheet_dsp.py`, not by `place()`**, so the generic patch did not reach it. **The single most
   important part on the board, and the one the shared fix missed.** *A fix applied to the common
   path leaves the special case exactly where it was, and the special case is special because the
   part is important.* **81/536, ICs now 0 missing.**

**The remaining 455 are R (237), C (162), J (22), TP (13), L (7), D (6), Q (4), SW (2), F (1),
T (1).** **Every one needs a PACKAGE, which follows from fab capability — ⬜ UNSET, Block E.**
Choosing 0603 as "typical practice" is precisely the §0 drift, so they stay empty and now stay
*visibly* empty.

**Guard owed:** `fp_guards.py` has G1–G4 on footprint *content* and **nothing asserting a footprint
is REACHABLE from the netlist.** A **G5 — every non-power component in the exported netlist carries
a non-empty footprint** — is the check that would have failed loudly today. **M27: it belongs at the
netlist layer, not the generator layer, because the generator layer is where the bug was.**

### F110 ❌ REFUTED BY ITS OWN AUTHOR — THE `#FLG` EXPLANATION WAS WRONG — 2026-08-22

**Filed and refuted within the hour. Kept in full, because a refutation deleted is a finding that
gets re-raised looking like independent confirmation (`CLAUDE.md` §9).**

**Claimed:** `kicad-cli`'s *"schematic has annotation errors"* was caused by two `#FLG` symbols
carrying no number.

**Refuted:** **both bare `#FLG` references sit INSIDE the `lib_symbols` cache**, where `#FLG` is the
PWR_FLAG library symbol's normal default reference prefix. Verified by byte-offset containment
against the `lib_symbols` block in both files. **The generators emit correctly numbered flags**
(`#FLG00`…`#FLG08`, `#FLG20`). **There is no unannotated symbol.**

**The annotation warning's true cause is NOT IDENTIFIED.** Ruled out so far, each by a named test:

    duplicate (refdes, unit) pairs      562 pairs, 562 unique, ZERO duplicates
    refdes spanning >1 lib_id or sheet  ZERO
    references containing '?'           ZERO across all 10 files
    hierarchical instance paths         9 sheets, ZERO mismatches against the root

**Left OPEN and named rather than closed** — bus rule 3's principle applied to our own register:
*an unexplained warning recorded as explained is worse than one recorded as open.* **Severity ▫: it
does not block the footprint pass, and ERC runs.**

**This is the THIRD wrong test in one session** — duplicate-refdes, then `#FLG`, both producing
confident-looking answers. **M32 the same day it was logged, twice.** *The tell in both: I tested a
PROPERTY OF THE TEXT (“how many bare `#FLG` strings exist”) for a question about SEMANTICS (“is any
PLACED symbol unannotated”).*

### F111 ⚠ STOCK OSCILLATOR FOOTPRINT NAME IS WRONG — NAME **AND** BODY SIZE — 2026-08-22

`gen_symbols.py:335` specifies

    Oscillator:Oscillator_SMD_SeikoEpson_SG210_4pin_3.2x2.5mm      <- written
    Oscillator_SMD_SeikoEpson_SG210-4Pin_2.5x2.0mm                 <- what KiCad 10 actually ships

**Three differences, and only two are typography:** `_4pin_` vs `-4Pin_`, **and the body size is
`2.5 × 2.0 mm`, not `3.2 × 2.5 mm`.** The 3.2 × 2.5 body belongs to the **SG8002CE**, a different
part. **A name written from memory, carrying a dimension that is wrong for the named device.**

**It sits on the PLACEHOLDER F56 oscillator**, so no committed decision rests on it — **but the
mechanism is the finding: the wrong name was INVISIBLE until F109 was fixed.** With no footprint on
any instance, ERC had nothing to resolve and reported nothing. **One hour after the instances
carried footprints, ERC named it.**

> **F109's real cost was never the missing footprints. It was that EVERY footprint-name error on the
> board was unreportable — including ones on parts that are not placeholders.**

**Disposition:** name corrected when the F56 oscillator is chosen for real; the choice is the
operator's and the placeholder is honest. **Logged now so the correction is not lost with the
placeholder.**

## 9. I2C0 bus map

**Re-emitted complete, 2026-08-16, as the gate on `09_io`'s close** — named debt twice is a
ledger; three times is a pattern.

| Device | Addr | Strap | Sheet |
|---|---|---|---|
| **AK5574** ADC | **0x10** | `CAD1`=0 (pin 34→GND), `CAD0`=0 (pin 32→GND) | 06 |
| **AK4458 #1** (AOUT1–6) | **0x11** | `CAD1`=0 (pin 12→GND), `CAD0`=1 (pin 15→+3V3_D) | 07 |
| **AK4458 #2** (AOUT7–12) | **0x12** | `CAD1`=0, `CAD0`=1 — *see note* | 08 |
| ~~0x13~~ | — | **freed by F26** when the AK4118A was deleted | — |
| **PCF8574T** GPIO expander | **0x20** | `A2:A1:A0` = 0,0,0 (pins 3,2,1 → GND) | 06 |
| **ADS1015** rail monitor | **0x48** | `ADDR`→GND | 01 |
| **TMP461** temp | **0x49** | `A0`→+3V3_D, `A1`→GND | 01 |

**⛔ The re-emission found a defect, which is the argument for the ritual.** The generator hands
**both** AK4458s the same strap pair `(+3V3_D, GND)` — the `i2c_addr_strap` parameter differs
between the two `build()` calls, but only in the value I passed, and **I passed the same one
twice**. Device #2 therefore also strapped to **0x11**, which is an address collision: two DACs
answering together, presenting as "the second DAC ignores its filter config" — F30's symptom,
different cause. **Fixed:** #2 takes `CAD1`=1 (pin 12 → +3V3_D), `CAD0`=0 → **0x12**.

**Two structural facts worth keeping:** the `0b00100` prefix holds exactly four AKM devices, so a
future ODSP-16's third AK4458 has nowhere to live and I2C1 comes out of reserve at that point,
not before. And 0x20 sits clear of both the AKM block (0x10–0x13) and the monitor pair
(0x48/0x49), so the expander was free to add.

**Pull-ups: 2.2 kΩ on SDA and SCL, on `03_control`, ONCE.** A second pair at the far end is a
rise-time bug that measures fine on a bench and fails at temperature.

## 8. [VERIFY] checklist

`REQUIREMENTS.md` requires these confirmed against current datasheets **before capture**
(`CLAUDE.md` §3). Each is T2 at best until closed, and closing one is a T1 promotion **with a
citation** — part number, document revision, and section.

| ID | Item | Src | Status |
|---|---|---|---|
| V-28 | ~~The SM8S24 HM3 datasheet~~ | F42/F44/F45 | **CLOSED 2026-08-16 → T1-90/T1-91.** Found by extracting the PDF's own embedded hyperlinks (doc **98647**); the NRND banner text is not a link, but the "Related Documents" icon is. **Results: all four sub-questions answered and none of them moved a conclusion.** The successor is electrically identical, so §12's table stands as written; the **6600/5200 pair is two waveforms of one unidirectional part**, settling the three-way reading against the uni-vs-bi interpretation; the **43 V/153 A distributor figure is a mis-mapped field**; and the package changed **AB → AC with an identical land pattern**. *The pre-fired chain was never needed — which is the point of firing it.* |
| V-29 | ~~Multi-pulse derating~~ | F42 | **CLOSED BY ANALYSIS 2026-08-16**, using §12's own v0.1 escape clause — *"or documented protection analysis if untested"* — because Vishay publishes no multi-pulse curve for this part. **Per pulse:** 95 W × 400 ms × R<sub>θJM</sub> 0.30 °C/W = **ΔT<sub>J</sub> 28.5 °C** → 113.5 °C even from an 85 °C mount, against 175 °C. **Between pulses:** 0.67 % duty → **0.63 W average against an 8 W steady-state rating, 13× headroom**, so heating does not accumulate and the 10-pulse case reduces to the per-pulse case. **Assumptions are ours and tagged:** R<sub>θJM</sub> read off the transient curve at 0.4 s, and a mount temperature that depends on the Block E copper. *Original text below.* |
| ~~V-29-open~~ | | | **The gap, as located before closure.** The HM3 datasheet carries the same single-pulse figure set as its predecessor (Fig. 1 P<sub>PPM</sub> vs pulse width; Fig. 3 load-dump power for a **10 ms exponential**) and **publishes no M-suffix/S-suffix multi-pulse curves** — those appear in the EDN article for the *SM5S* family, not here. So ISO 16750-2's **10 pulses in 10 minutes** remains uncharacterised for this part. **Bound, not closed:** P<sub>D</sub> = 8 W steady-state sets the recovery rate between pulses, and at 1-minute intervals the junction fully recovers, so the binding case is per-pulse rather than cumulative heating — **but that is reasoning, not the vendor's curve.** Route: Vishay applications, or accept it as consumption of the suppressed row's 3–5× margin and say so in G7 |
| ~~V-29-orig~~ | | | **Open.** ISO **16750-2** superseded the load-dump test between the power sheet and full T1.** Read at figure level: **(1)** the **6600 W / 5200 W** pair, which now has **three competing readings and no T1** — mine-and-operator's-original (uni vs bi, supported by the distributor pattern of uni at 6.6 kW and bi at 5200 W), mine-second (two waveform ratings of one part, 10/1000 µs vs 10/10 000 µs, which is what the NRND table literally shows), and the possibility that **both are true at different levels** — family-wide polarity split *and* a waveform pair within each. **(2)** The clamp endpoints: held document says **38.9 V at 170 A**, an HM3-era distributor listing says **43 V at 153 A**. **(3)** The **M-suffix (multi-pulse, ISO 16750-2) vs S-suffix (single-pulse, ISO 7637-2)** capability curves. **(4)** The CA member's curves, which settle F45's direction decision. **Pre-fired, so the read cannot surprise us:** the consequence chain was run against *both* clamp endpoints — with 43 V/153 A, r<sub>d</sub> becomes 97 mΩ, Q1 sits at **73 %** of its 80 V rating (58 % on the realistic 48 A clamp), and **every §12 verdict row is unchanged** (93 / 364 / 739 / 3717 W against the same thresholds). **The pending read can refine numbers; it cannot move a conclusion.** That is criterion 5 and M7 doing exactly the job they were installed for |
| V-29 | **Multi-pulse derating: §12's table is a SINGLE-pulse analysis** | F42 | **Open.** ISO **16750-2** superseded the load-dump test with **10 pulses in 10 minutes**, and Vishay's own article states that *"10 continuous pulses affected the surge suppressing capability of the load dump TVS."* Our §12 rows compute one pulse. **The 3–5× margin on the suppressed row is the buffer this has to come out of**, and it is probably sufficient, but it is not yet evidenced. Settles from the HM3 M-suffix curves in the same read as V-28 |
| V-17 | ~~AVDD currents for AK5574 and AK4458~~ | §7.1 / F24 | **CLOSED 2026-08-16 from the datasheet maxima.** AK5574 `AVDD+VREFH1/2` **64 mA max** (49 typ); AK4458 `AVDD` **41 mA max** (31 typ) each. **+5V_A = 146 mA max.** LMK1C1104 on +3V3_CLK: **40 mA max**, and that is specified at f<sub>IN</sub> = 100 MHz where ours is 24.576 MHz, so it is conservative by a wide margin. **+6V2_A identified load = 186 mA against the 250 mA assumption already on the sheet — the assumption holds and is now a derivation.** The 15 µH / Isat ≥ 0.5 A inductor stands unchanged |
| V-26 | ~~LM5156-Q1 spread-spectrum deviation percentage~~ | F39 | **CLOSED by decree, 2026-08-16 — not by finding the number, but by removing the dependency.** `DITHOFF` is fitted as a stuffing pair with the **populated leg to VCC: dither OFF**. The fundamental then sits deterministically at 2.2 MHz with an RT-tolerance floor of 1980 kHz — **15.8 % above the AM band on specified numbers only**, where the dithered case rested on 4 % of margin against a parameter the datasheet declines to state (the F37 shape). The decorrelation argument is untouched: beat suppression needs only one party spread, and both LM61460s carry ±2 % SS on their pinned PNs. A DNP leg to GND re-enables dither if EMI measurement ever asks. **Second use this round of "close it by making the number irrelevant"** — see V-27 |
| ~~V-26-orig~~ | | | **Open — and the datasheet does not contain it.** T1-76 gives the modulation *frequency* (0.156 × f<sub>SW</sub>) but never the deviation. Bounded meanwhile: f<sub>SW</sub> min is 1980 kHz, so even ±10 % dither reaches only 1782 kHz — above the AM band's 1710 kHz top, **but by 4 %**, which is margin-by-luck rather than by design. `DITHOFF` is a one-resistor escape hatch either way. Source: TI E2E or the EVM report, not the datasheet |
| V-27 | **LM5156-Q1 / LM61460-Q1 pulse-skip onset current, and the repetition rate when skipping** | F39 | **Open — unspecified by both datasheets**, which mention light-load pulse skipping only in prose. Matters because the analog rails idle near 50 mA against a 200 mA budget, i.e. permanently at ~25 % load. **Bounded, not blocking:** even 100 mV<sub>PP</sub> of in-band skip artefact meets 0.35 µV<sub>RMS</sub> at the op-amp rail through T1-72's audio-band PSRR. Settles on the bench, not before capture |
| V-01 | ADAU1466 package, ports, ASRCs + V-07/V-08/V-13 + firmware contract, in one pass | §2 | **CLOSED 2026-08-15 → T1-16…T1-25.** Single pass as planned (DL-22). Confirmed F17 and produced F18/F19/F20/F21 |
| V-02 | AK4118A: confirm it has no internal SRC, and its output-port master/slave capability | §3 / F1 | **Closed** → T1-10, operator confirmation. Re-check on the datasheet when it is open for pinout anyway — F1's whole disposition rests on it |
| V-03 | BM83 I2S master/slave capability in the chosen firmware config | §3 | Open |
| V-04 | AK5574 and AK4458 MCLK ratio and MCLK/LRCK synchronisation requirements at 48 kHz TDM | §3 / F15 | **DAC side closed → T1-26** (512fs or 768fs at 48 kHz; our 24.576 MHz XO is exactly 512fs). **ADC side still open** — AK5574 ratio table needs a second look, and the F15 MCLK/LRCK phase-coherence question is unanswered for both |
| V-05 | AK4458 differential full-scale output voltage | §6.2 / F12 | **CLOSED → T1-11.** 2.8 Vpp differential at (VREFH−VREFL)=5 V. `AK4458_AKM.pdf`, see `DATASHEETS.md` |
| V-06 | OPA1656 output swing and quiescent current at ±13.5 V | §6.2 / F7 | **Iq closed → T1-29:** 3.9 mA/channel, confirming the 96 mA figure behind T1-D30. **Output swing still open** — it sits in a spec table that needs a targeted read, and it is what confirms the 4.5 Vrms [HARD] headroom claim in T2-06 |
| V-07 | ADAU1466 slave-port maximum SPI SCLK (target ≥10 MHz) | §5 | **CLOSED → T1-19.** 20 MHz read and write — 2x margin on the target |
| V-08 | ADAU1466 core voltage and current | §7.1 | **CLOSED → T1-20.** 1.2 V ±5%; 220 mA typical, **495 mA max**. Drove F18 and F19 |
| V-09 | AKM control-port mode strapping — each part, strapped consistently to I2C | §5 | **CLOSED → T1-27.** I2C/IIC pin = H on all three; **AK4458 additionally needs `PS` = L**, since PS = H selects *parallel* mode. But see **F23** — whether they can all *coexist* on one bus is a separate question the strapping answer exposed |
| V-10 | AKM part lifecycle and lead time; decide AKM vs TI (PCM1865 / PCM1690) | §2 / §11 | Open |
| V-11 | INA1650 channel count per package | §2 / F2 | **CLOSED → T1-12.** Dual-channel, confirmed against the TI datasheet, no longer resting on operator confirmation alone |
| V-13 | ADAU1466 per-port serial master/slave configurability | §3 v0.2 / F1 | **CLOSED → T1-18.** Per-port `SERIAL_BYTE_x_0` registers with `LRCLK_MODE` / `BCLK_MODE` bits, plus per-port pin-table wording. **The F1 disposition is confirmed against the document**, and the operator's T2 was correct. The fallback (dedicated ASRC pair) is not needed |
| V-14 | **Series photoMOS** (TLP3475-class): Ron, off-state Coff, voltage rating vs ±6.4 V peak plus rail-collapse excursion, LED drive current | §6.4 v0.4 | Open — **restated at v0.4.** No longer a constrained optimisation: Ron 1–2 Ω against ≥10 kΩ is inaudible and off-isolation is the easy half of the pair |
| V-15 | **Shunt depletion FET pair**: Ron (100–500 Ω is ample), off-state Coff **and its nonlinearity**, Vgs(off) against the −13V5-derived bias | §6.4 v0.4 | Open — **restated at v0.4.** Small-die part; Coff is now the only tight number and it is tight against T1-D42, not against mute depth |
| V-19 | ADAU1466 integrated S/PDIF receiver: lock range, clock/ASRC path, pin conflicts, and whether the TX covers the digital-out option | §2 / F26 | **CLOSED 2026-08-16 → T1-42…T1-45.** All three conditions passed; TX covers it too. Figure-level read of pp. 74-75 per M2 |
| V-20 | **TMP461-class variant address straps** against the §9 bus map — the 0x48 range already holds the ADS1015 | §9 v0.8 / F27 | Open — **folded into the F38 sweep** as line 7. Same deliverable: PN pinned with the one-line why against the bus map. Pick from the strap table, not from aesthetics |
| V-17 | **AVDD currents for AK5574 and AK4458** — sizes the +6V2_A buck and **all three** LT3045 stages | §7.1 v0.7 / F24 | Open. Read alongside V-04's ADC side, same tables. **Sizing note:** the +6V2_A budget is the sum of +5V_A, +3V3_A **and the newly approved +3V3_CLK fanout load** — the escalation changed this buck's budget on the same turn it was raised |
| V-18 | **ADAU1466 core-supply ripple tolerance** from the electrical table — designs the +1V2_CORE buck's output filter against a number rather than vibes | §7.1 v0.5 / F18 | Open — **new at v0.5**, rides with the F18 disposition |
| V-16 | Disorderly-path transient, modelled as the **full stack**: DAC brown-out residual × mute attenuation × amp gain × amp remote-mute latency | §7.4 v0.4 | Open — bench, first board. **Bounded, not indefinite:** remote-out is fail-safe and drops first, so the window is the amp's own mute latency (tens to ~200 ms), and the source is a resetting DAC well under −20 dBFS, not programme material. Use a pessimistic latency — it belongs to someone else's amplifier |
| V-12 | BM83SM1 and ESP32-S3-WROOM-1 antenna keepout dimensions and board-edge requirements | §8 | **Partially closed → T1-31.** Both mandates confirmed: BM83 needs no copper, no component **and no ground plane** under the antenna; WROOM-1 has a keepout zone. **Dimensions live in figures** and need a `pdftoppm` render — fold into the DL-14 footprint pass, where the operator already eyeballs the BM83 keepout. **Escape hatch noted:** the **-1U** variant has no keepout because it takes an external antenna — the answer if T1-D20's antenna-separation requirement fights the outline |
