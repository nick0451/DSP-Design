# Datasheet register — ODSP-12

Local archive: [`datasheets/`](datasheets/) — **not tracked in git** (see `.gitignore`); this
register is the tracked artefact. Hashes are SHA256 truncated to 16 hex chars, which is for
detecting corruption and mix-ups, not for cryptographic purposes.

**Every PDF below was verified after download** — page count and first-page text checked against
the expected part. A HTTP 200 and a `.pdf` extension prove nothing; see the ledger entry in
`STATE.md` §5, which exists because one "successful" download was an HTML page for an unrelated
optocoupler.

Retrieved 2026-08-15.

---

## Held

| Part | File | Pages | SHA256/16 | Source |
|---|---|---|---|---|
| **AK4458** 8ch DAC | `AK4458_AKM.pdf` | 90 | `1D837FF1E7301B22` | akm-semi.com (official) |
| **AK5574** 4ch ADC | `AK5574_AKM.pdf` | 70 | `E75632374D354625` | akm.com CDN (official) |
| **AK4118A** SPDIF xcvr | `AK4118A_AKM.pdf` | 56 | `A71CCB7BAC763546` | akm.com CDN (official) |
| **INA1650** diff line RX | `INA1650_TI.pdf` | 42 | `D2BF4591DB74CA5C` | ti.com (official) |
| **OPA1656** op-amp | `OPA1656_TI.pdf` | 42 | `4243B58E553E6F27` | ti.com (official) |
| **LM61460-Q1** buck | `LM61460-Q1_TI.pdf` | 58 | `019278702073B81C` | ti.com (official) |
| **LMK1C1104** clock fanout | `LMK1C1104_TI.pdf` | 27 | `4403CE872CF97948` | ti.com (official) |
| **ADS1015** rail-monitor ADC | `ADS1015_TI.pdf` | 50 | `A5CB3720275767B1` | ti.com (official) |
| **TMP102** temp sensor | `TMP102_TI.pdf` | 33 | `C9DA6620EF95F75C` | ti.com (official) |
| **BM83** BT audio module | `BM83_Microchip.pdf` | 76 | `C24F40D28C04C64D` | microchip.com DS70005402 (official) |
| **ESP32-S3-WROOM-1** | `ESP32-S3-WROOM-1_Espressif.pdf` | 53 | `27D71971DA07C280` | espressif.com (official) |
| **25AA1024** EEPROM *(DNP)* | `25AA1024_Microchip.pdf` | 32 | `3262F74248BF2698` | microchip.com (official) |
| **ADAU1462/ADAU1466** DSP | `adau1462-1466.pdf` | 202 | `C473F6316A5D3F95` | analog.com **Rev. C** — operator-supplied |
| **LT3045** LDO | `LT3045.pdf` | 32 | `9132E595759A58A0` | analog.com **Rev. D** — operator-supplied |
| **TPS62823** buck | `TPS62823_TI.pdf` | 32 | *(see repo)* | ti.com **Rev. C** — closes V-24 |
| **LM5156-Q1** boost/SEPIC ctrl | `LM5156-Q1_TI.pdf` | 50 | `D04AD7C9CC97EA5D` | ti.com SNVSBI7B **Rev. B** — ±13V5_A SEPIC |
| **LM5155-Q1** boost/SEPIC ctrl | `LM5155-Q1_TI.pdf` | 51 | `4E9C3E37EE320EBA` | ti.com SNVSAY4F **Rev. F** — *held for the elimination* |
| **LM5157-Q1** integrated-switch | `LM5157-Q1_TI.pdf` | 48 | `28B681FF944763E5` | ti.com SNVSBK8B **Rev. B** — *held for the elimination* |
| **LM5175-Q1** 4-switch buck-boost | `LM5175-Q1_TI.pdf` | 38 | `7F53B15F7B5D0F8D` | ti.com — *held for the elimination* |
| **TPS55340-Q1** boost/SEPIC | `TPS55340-Q1_TI.pdf` | 40 | `1C9A8605568C0ED3` | ti.com **Rev. C** — *held for the elimination* |
| **SNVA856** *(app note)* | `SNVA856_TI_InvertingBuckBoost.pdf` | 20 | `806345F00EA5D4BD` | ti.com **Rev. B** — "Working With Inverting Buck-Boost Converters" |
| **LT3094** neg. LDO | `LT3094.pdf` | 34 | `C82438CA3359A588` | analog.com **Rev. B** — operator-supplied 2026-08-16 |
| **SM8S10A–43A** TVS *(NRND)* | `sm8s.pdf` | 6 | `A627B4D5C5CD6D17` | vishay.com doc 88387 **Rev. 06-Feb-2026** — operator-supplied |
| **TVS for automotive** *(app note)* | `tvs.pdf` | 4 | `4A8C122BEFD46EBC` | vishay.com doc 88490 — carries the ISO 7637-2 pulse-5 test table |
| **Load dump: old vs new ISO** *(article)* | `49748.pdf` | 5 | `028F83CE47A98FF4` | vishay.com doc 49748, EDN reprint — **an article, not a specification** |
| **SM8S10AHM3–85AHM3** TVS | `SM8S_AHM3_Vishay.pdf` | 6 | `A9B581CFDF743398` | vishay.com **doc 98647, rev. 14-Oct-2025** — the successor. **Closes V-28** |
| **AP2127** LDO | `AP2127_Diodes.pdf` | 24 | `D48C96AC985D348A` | diodes.com — **closes V-23 and F36** |
| **USBLC6-2** ESD array | `usblc6-2.pdf` | 20 | `BC30154F310CD631` | st.com Doc ID 11265 — operator-supplied. **Closes V-30** |

All twenty-four are manufacturer-published documents, not aggregator copies — but note the last
row is an **EDN article reprinted by Vishay**, which is context, not a specification, and must not
be cited as one.

**`sm8s.pdf` has no text layer at all** — `pdftotext` returns nothing. It was read entirely by
rendering, which is the M2 method anyway; recorded because a text-extraction pipeline over this
archive will silently skip it rather than fail.

**The SM8S10A–43A document is marked NOT FOR NEW DESIGNS** (successors SM8S10AHM3–SM8S85AHM3).
It is held because every figure currently on the power sheet is read from it, and those figures
inherit a re-verification against the AHM3 datasheet, which is **not held** — see F44.

**Four of these are held for their eliminations, not their selections.** LM5155-Q1, LM5157-Q1,
LM5175-Q1 and TPS55340-Q1 were each excluded from the ±13V5_A block by a number in their own
datasheet (F39). A discarded candidate's datasheet is the evidence that the discard was reasoned;
without it the exclusion decays into "we picked the other one." Keep them.

**SNVA856 is an application note, not a datasheet, and it is load-bearing anyway.** None of the
five wide-V<sub>IN</sub> switching datasheets above documents an inverting configuration. The
negative rail is drawn from SNVA856's schematics, not from first principles — CLAUDE.md §8 rule 9
applies to topology exactly as it applies to pin numbers.

## Missing

| Part | Why it matters | Status |
|---|---|---|
| ~~**SMBJ24A** TVS~~ | ~~ISO 7637-2 input protection~~ | **Superseded — the part is gone from the design.** F42: a 600 W SMB misses the load-dump energy by 40–165×. Replaced by the SM8S24A class |
| ~~**SM8S24AHM3**~~ | ~~successor datasheet~~ | **HELD — fetched 2026-08-16, doc 98647. V-28 closed** |
| **SM8S24CAHM3** *(bidirectional)* | **Optional improvement, not a blocker (F45).** Would restore seamless reverse and retire the F43 polarity hazard. Doc 98647 covers the **unidirectional** series only, so a CA series lives under a different doc number — **unverified, not disproven** (M12) | Open. Same land pattern either way, so the swap is a value change rather than a respin |
| **PNP pass transistor** | **New requirement** — the ADAU1466's internal regulator drives an external PNP (T1-21). Dissipates ~1 W at max program | Part not selected; needed only if F18 goes the internal-regulator way |
| **24.576 MHz XO** | T1-D03 clock master | Part not finalised (SiT8208 vs CCHD-575 class) — fetch once chosen |
| **TLP3475** photoMOS | **V-14**, mute series element | Candidate only; fetch with the part decision |
| Depletion FET | **V-15**, mute shunt | Part not selected |
| **WM8804**, **TJA1051T-Q1** | DNP on v1 | Deferred deliberately — no capture dependency |

**analog.com remains unreachable from this environment** (T1-15) — it refused every automated
fetch path tried, while a browser session worked first time, so it reads as bot/UA filtering
rather than a routing failure. **Any further ADI part will need the same manual step.**

**vishay.com IS reachable — an earlier claim to the contrary is RETRACTED** (T1-92). It was
generalised from one failed fetch of `docs/88361/smbj.pdf`, and it became a reason to ask the
operator for files that could have been fetched here. **Use the shortlink form
`https://www.vishay.com/doc?NNNNN`**, which resolves server-side to the current revision.
**And when a datasheet cross-references others, extract its embedded `/URI` hyperlinks** — that is
how doc 98647 was located, since the NRND banner text is not itself a link.

---

## Closed from the archive on retrieval

| V | Finding | Evidence |
|---|---|---|
| **V-11** | **INA1650 is dual-channel** — confirms T1-D27 (2 packages for 4 differential inputs) and closes F2 against the manufacturer document rather than operator confirmation | `INA1650_TI.pdf` p.1: *"The dual-channel INA1650 and single-channel [INA1651]"* |
| **V-05** | **AK4458 full-scale output = 2.8 Vpp differential** at (VREFH − VREFL) = 5 V, stated per DAC channel | `AK4458_AKM.pdf`: *"AOUT (typ.@0dB) = (AOUT+) − (AOUT−) = 2.8 Vpp × (VREFH1 − VREFL1)/5"* |

V-05 confirms T2-05 exactly: 2.8 Vpp differential is 0.99 Vrms, so reaching the 4.5 Vrms [HARD]
output needs **4.55× = 13.2 dB** of gain in the diff-to-SE stage. The estimate that raised the
noise-budget concern was right, and the concern stands — that gain multiplies DAC-referred noise
by the same 4.55× against the −105 dBV criterion.

**Also noted:** `INA1651` is the single-channel sibling. Not needed at 4 inputs, but it is the
part to reach for if a channel count ever goes odd.

### V-01 pass — ADAU1466 Rev. C, 2026-08-15

One opening of the document per DL-22, covering V-01, V-07, V-08, V-13 and the firmware contract.
Full results at `STATE.md` T1-16…T1-25. Headlines:

| | |
|---|---|
| Package | **72-lead LFCSP `CP-72-6` only** — no LQFP, no WLCSP. Confirms F17 |
| Ports / ASRC | 4 in, 4 out; up to 8 stereo ASRCs, 1:8 to 7.75:1, 139 dB DR — §2/§4 correct |
| Per-port master/slave | **Yes** — `SERIAL_BYTE_x_0` LRCLK_MODE/BCLK_MODE. **F1 confirmed** |
| SPI SCLK | 20 MHz max — 2x the target |
| Core | 1.2 V ±5%, **220 mA typ / 495 mA max** → F19 |
| 1.2 V regulator | Controller + **external PNP** on `VDRIVE` pin 3, to 800 mA → F18 |
| PLL lock | ≤10.666 ms; **control port inactive throughout** → F20 |
| SELFBOOT | Pin 34, 250 kOhm internal pull-up → F21 |

The pass produced **four new findings**, three of which touch the [HARD] power and sequencing
sections. That ratio is the argument for reading datasheets before capture rather than during it.

---

## Tooling

**poppler 25.07.0** installed via winget (`oschwartz10612.Poppler`), user scope, added to user
PATH:

```
C:\Users\nick\AppData\Local\Microsoft\WinGet\Packages\
  oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin
```

Provides `pdftotext` (spec extraction), `pdfinfo` (verification), and `pdftoppm` — the last is
what the footprint-verification pass of DL-14 needs to rasterise a land-pattern drawing.

**Note:** a freshly spawned shell may not inherit the updated user PATH. Invoke by full path when
a bare `pdftotext` fails rather than concluding the install is broken.
