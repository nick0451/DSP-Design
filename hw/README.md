# hw/ — working guide

**Mechanical how-to for the KiCad work.** Design *decisions* live in `../REQUIREMENTS.md`,
*state and facts* in `../STATE.md`, *bench sequence* in `../BRINGUP.md`. This file is only the
"how do I drive the tools without re-learning it" layer.

Everything below was **verified against the tool or a known-good file**, never assumed — DL-13.

---

## 1. Tool paths (none are on PATH)

```
kicad-cli   "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"
python      "C:/Program Files/KiCad/10.0/bin/python.exe"     # 3.11.5, has pcbnew
poppler     "C:/Users/nick/AppData/Local/Microsoft/WinGet/Packages/
             oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe/
             poppler-25.07.0/Library/bin/"                    # pdftotext, pdfinfo, pdftoppm
```

A freshly spawned shell may not inherit the user PATH. **Invoke by full path rather than
concluding an install is broken.**

## 2. The build

Everything is **generated, not hand-drawn** — so regeneration is idempotent and a diff is
meaningful. Run from `hw/`:

```
python lib/gen_symbols.py      # -> lib/ODSP12.kicad_sym   (7 symbols / 12 units)
python gen_sheet_dsp.py        # -> 02_dsp.kicad_sch
python gen_sheet_power.py      # -> 01_power.kicad_sch
```

`gen_sheet_dsp.py` imports `lib/gen_symbols.py` and re-runs its assertions, so a broken symbol
stops the sheet.

## 3. Verification — in this order, and do not skip step 2

```
kicad-cli sch erc     --severity-all --exit-code-violations --format json -o out/erc.json ODSP12-MB.kicad_sch
kicad-cli sch export  netlist -o out/odsp12.net ODSP12-MB.kicad_sch
kicad-cli sch export  pdf     -o out/ODSP12-MB.pdf ODSP12-MB.kicad_sch
pdftoppm -png -r 100 -f <page> -l <page> out/ODSP12-MB.pdf out/page
```

**ERC alone is not verification.** A sheet with zero components passes ERC, exports a PDF with
the right page count, and contains nothing. **The artefact is the netlist** — extract pin-to-net
connectivity and check it against intent:

```python
nets = re.findall(r'\(net\s+\(code "\d+"\)\s+\(name "([^"]+)"\)(.*?)\n\t\t\)', s, re.S)
d = {n: re.findall(r'\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)', b) for n, b in nets}
```

`+1V2_CORE` must reach U1 pins 20/35/53/71, or the sheet is decoration.

## 4. KiCad 10 file-format facts, learned the hard way

| Fact | Why it bit |
|---|---|
| Schematic format version is **`20260306`** | From `sch upgrade`, not memory |
| Symbol-library format version is **`20251024`** | From a stock `.kicad_sym` |
| In `lib_symbols`, **only the parent** carries the `LIB:` prefix; sub-symbols keep the bare name (`CM5IO:C` contains `C_0_1`) | Prefixing children too produced a file that parsed, passed ERC, exported a PDF, and **had zero components** |
| A symbol instance's `path` uses the **sheet symbol's UUID in the root**, not the child file's own UUID | Same silent-empty failure |
| `sym-lib-table` / `fp-lib-table` must exist for `lib_id` to resolve | — |
| Ground truth for format questions: `C:/Program Files/KiCad/10.0/share/kicad/demos/` | **Specifications describe formats; examples *are* formats** |

## 5. Generator conventions

- **Connectivity is by global label at the pin endpoint, not by wires.** Netlist-verifiable and
  robust to generate. Wires are cosmetic and can come later.
- **UUIDs are `uuid5` from a fixed namespace** — regeneration is byte-stable, so a diff shows real
  change rather than churn.
- **All coordinates snap to the 1.27 mm grid.** Off-grid endpoints are the classic cause of a
  connection that looks made and is not; KiCad flags them.
- **Every pin gets an explicit disposition** — a net label or a `no_connect`. The generators
  **assert** full coverage, so an undispositioned pin is a build failure, not an oversight (F28).
- **Symbol pin maps are extracted as name+number pairs from a single regex match**, never as two
  lists zipped. Zipping silently permutes when either list drops an entry, and a pin-*set*
  assertion cannot see a permutation (M6).
- **Assert the input was non-empty**, not only that nothing is missing — an assertion over an
  empty set passes vacuously (M5).

## 6. Editing files

**Use the Edit tool, not shell round-trips.** Windows PowerShell 5.1 `Get-Content -Raw` reads
BOM-less UTF-8 as ANSI; one read-modify-write double-encoded 204 characters across `STATE.md`.
If a shell round-trip is unavoidable, force encoding on **both** ends.

Check with: `grep -c $'\xc3\x82\|\xc3\xa2\xe2\x82\xac' <file>` — expect `0`.

## 7. Scratchpad artefacts are disposable

Datasheet text extractions (`pdftotext -layout`) live in the session scratchpad and **do not
survive**. They are regenerable in seconds from `../datasheets/`. Nothing depends on them
persisting — but **page renders at 150-175 dpi are how load-bearing datasheet facts get read**
(M2), not text extraction, which has produced three wrong T1 facts on this project.
