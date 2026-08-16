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

All fourteen are manufacturer-published documents, not aggregator copies.

## Missing

| Part | Why it matters | Status |
|---|---|---|
| **SMBJ24A** TVS | ISO 7637-2 input protection | Not yet fetched; generic part, many vendors, low risk |
| **PNP pass transistor** | **New requirement** — the ADAU1466's internal regulator drives an external PNP (T1-21). Dissipates ~1 W at max program | Part not selected; needed only if F18 goes the internal-regulator way |
| **24.576 MHz XO** | T1-D03 clock master | Part not finalised (SiT8208 vs CCHD-575 class) — fetch once chosen |
| **TLP3475** photoMOS | **V-14**, mute series element | Candidate only; fetch with the part decision |
| Depletion FET | **V-15**, mute shunt | Part not selected |
| **WM8804**, **TJA1051T-Q1** | DNP on v1 | Deferred deliberately — no capture dependency |

**analog.com remains unreachable from this environment** (T1-15) — it refused every automated
fetch path tried, while a browser session worked first time, so it reads as bot/UA filtering
rather than a routing failure. **Any further ADI part will need the same manual step.**

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
