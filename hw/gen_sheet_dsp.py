# Generates 02_dsp.kicad_sch -- the ADAU1466 and its clock tree.
#
# Net names follow REQUIREMENTS.md section 10 [HARD]. Every pin gets an explicit
# disposition per F28: a net label, a rail, or an explicit no-connect. Nothing floats
# by accident and nothing is left unannotated.
import os, re, uuid

HW = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HW, "lib", "ODSP12.kicad_sym")
DEST = os.path.join(HW, "02_dsp.kicad_sch")
NS = uuid.UUID("0d5f1a00-0000-4000-8000-0000000000ff")
SHEET_UUID = str(uuid.uuid5(NS, "sheet:02_dsp.kicad_sch"))   # this file's own uuid
# The instance path is built from the SHEET SYMBOL's uuid in the root sheet, which is a
# different object from the child file's uuid. Getting these confused yields a schematic
# that parses cleanly, passes ERC, and contains no components -- silent, not loud.
SHEET_SYM_UUID = str(uuid.uuid5(NS, "inst:02_dsp.kicad_sch"))
ROOT_UUID = "0d5f1a00-0000-4000-8000-000000000001"
VER = "20260306"

def u(tag): return str(uuid.uuid5(NS, "dsp:" + tag))

# ---- pull the ADAU1466 definition out of the library ----
src = open(LIB, encoding="utf-8").read()
start = src.index('\t(symbol "ADAU1466"')
depth, i = 0, start
while True:
    if src[i] == "(": depth += 1
    elif src[i] == ")":
        depth -= 1
        if depth == 0: break
    i += 1
# Only the PARENT symbol carries the LIB:NAME prefix. Sub-symbols keep the bare name --
# verified against share/kicad/demos/cm5_minima, where "CM5IO:C" contains "C_0_1", not
# "CM5IO:C_0_1". Prefixing the children too yields a file that parses, passes ERC, exports
# a PDF and contains no components: every check says fine except the one that matters.
adau = src[start:i + 1].replace('(symbol "ADAU1466"', '(symbol "ODSP12:ADAU1466"', 1)

# ---- recover pin geometry using the same math the symbol generator used ----
import importlib.util
spec = importlib.util.spec_from_file_location("gs", os.path.join(HW, "lib", "gen_symbols.py"))
gs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gs)          # re-runs assertions; a failure here stops the sheet
PINS = gs.ADAU1466

def geometry(unit):
    """-> {pin_number: (x, y)} in symbol coords, matching gen_symbols.unit_block."""
    pins = [p for p in PINS if p[3] == unit]
    half = (len(pins) + 1) // 2
    left, right = pins[:half], pins[half:]
    rows = max(len(left), len(right))
    w, top = 63.5, (rows + 1) * 2.54 / 2
    out = {}
    for i, (num, *_rest) in enumerate(left):
        out[num] = (-w / 2 - 5.08, top - 2.54 * (i + 1))
    for i, (num, *_rest) in enumerate(right):
        out[num] = (w / 2 + 5.08, top - 2.54 * (i + 1))
    return out

# ---- net assignment: every pin, explicitly ----
GND = "GND"
NETS = {}
for n in (1, 17, 19, 25, 36, 37, 54, 55, 72, 6, 14, "EP"): NETS[n] = GND
for n in (2, 18, 38, 56): NETS[n] = "+3V3_D"
for n in (20, 35, 53, 71): NETS[n] = "+1V2_CORE"
NETS[7] = "+3V3_D"          # AVDD, auxiliary ADC supply, 3.3 V +/-10%
NETS[15] = "+3V3_PLL"       # PVDD -- see F33; deliberately its own net, resolved on the power sheet
NETS[16] = "PLLFILT"        # loop filter network, local to this sheet
NETS[3] = GND               # VDRIVE -> GND, DVDD fed externally (T1-41)
# serial ports, section 4 [HARD] naming
NETS.update({59: "TDM_IN0_DATA", 57: "TDM_IN0_BCLK", 58: "TDM_IN0_LRCLK"})
NETS.update({62: "TDM_IN1_DATA", 60: "TDM_IN1_BCLK", 61: "TDM_IN1_LRCLK"})
NETS.update({67: "TDM_IN2_DATA", 65: "TDM_IN2_BCLK", 66: "TDM_IN2_LRCLK"})
NETS.update({70: "TDM_IN3_DATA", 68: "TDM_IN3_BCLK", 69: "TDM_IN3_LRCLK"})
NETS.update({41: "TDM_OUT0_DATA", 40: "TDM_OUT0_BCLK", 39: "TDM_OUT0_LRCLK"})
NETS.update({44: "TDM_OUT1_DATA", 43: "TDM_OUT1_BCLK", 42: "TDM_OUT1_LRCLK"})
NETS.update({49: "TDM_OUT2_DATA", 48: "TDM_OUT2_BCLK", 47: "TDM_OUT2_LRCLK"})
NETS.update({52: "TDM_OUT3_DATA", 51: "TDM_OUT3_BCLK", 50: "TDM_OUT3_LRCLK"})
NETS.update({21: "MCLK_DSP", 23: "CLKOUT_DSP", 24: "DSP_RESET_N", 34: "DSP_SELFBOOT"})
NETS.update({33: "SPI_DSP_SS_N", 31: "SPI_DSP_SCLK", 32: "SPI_DSP_MOSI", 30: "SPI_DSP_MISO"})
NETS.update({4: "SPDIF_RX_IN", 5: "SPDIF_TX_OUT"})
NETS.update({63: "DSP_THD_M", 64: "DSP_THD_P"})
# explicit no-connects, each justified
NC = {
    22: "XTALOUT - external XO used, not a crystal",
    26: "SS_M - SPI master port unused (self-boot protocol select, SELFBOOT is low)",
    27: "MOSI_M - SPI master port unused",
    28: "SCL_M - I2C/SPI master port unused",
    29: "SDA_M - I2C/SPI master port unused",
    45: "MP6 - unused multipurpose I/O",
    46: "MP7 - unused multipurpose I/O",
    8: "AUXADC0 unused", 9: "AUXADC1 unused", 10: "AUXADC2 unused",
    11: "AUXADC3 unused", 12: "AUXADC4 unused", 13: "AUXADC5 unused",
}

allpins = {p[0] for p in PINS}
covered = set(NETS) | set(NC)
missing = allpins - covered
assert not missing, f"pins with no disposition (violates F28): {sorted(missing, key=str)}"
print(f"  disposition check: {len(NETS)} nets + {len(NC)} no-connects = {len(covered)} / {len(allpins)} pins")

# Origins snapped to the 1.27 mm grid. Pin offsets are multiples of 1.27 by construction,
# so an on-grid origin keeps every endpoint on grid -- KiCad flags off-grid endpoints because
# they are the classic cause of a connection that looks made and is not.
GRID = 1.27
def snap(v): return round(v / GRID) * GRID
UNIT_POS = {1: (snap(60.0), snap(60.0)), 2: (snap(190.0), snap(60.0)), 3: (snap(320.0), snap(60.0))}
REF = "U1"

def sym_instance(unit):
    px, py = UNIT_POS[unit]
    pins = [p for p in PINS if p[3] == unit]
    out = ['\t(symbol', '\t\t(lib_id "ODSP12:ADAU1466")',
           f'\t\t(at {px} {py} 0)', f'\t\t(unit {unit})',
           '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)', '\t\t(dnp no)',
           '\t\t(fields_autoplaced yes)', f'\t\t(uuid "{u(f"inst{unit}")}")',
           f'\t\t(property "Reference" "{REF}" (at {px} {py - 5} 0) (effects (font (size 1.27 1.27))))',
           f'\t\t(property "Value" "ADAU1466WBCPZ300" (at {px} {py - 2.5} 0) (effects (font (size 1.27 1.27))))']
    for num, *_ in pins:
        out.append(f'\t\t(pin "{num}" (uuid "{u(f"p{unit}_{num}")}"))')
    out += ['\t\t(instances', '\t\t\t(project "ODSP12-MB"',
            f'\t\t\t\t(path "/{ROOT_UUID}/{SHEET_SYM_UUID}" (reference "{REF}") (unit {unit}))',
            '\t\t\t)', '\t\t)', '\t)']
    return "\n".join(out)

def labels(unit):
    px, py = UNIT_POS[unit]
    geo = geometry(unit)
    out = []
    for num, name, etype, uu in [p for p in PINS if p[3] == unit]:
        sx, sy = geo[num]
        x, y = snap(px + sx), snap(py - sy)    # schematic Y is inverted vs symbol Y
        left = sx < 0
        if num in NC:
            out += [f'\t(no_connect (at {x} {y}) (uuid "{u(f"nc{num}")}"))']
        else:
            just = "right" if left else "left"
            rot = 180 if left else 0
            out += [f'\t(global_label "{NETS[num]}"',
                    f'\t\t(shape bidirectional)', f'\t\t(at {x} {y} {rot})',
                    f'\t\t(fields_autoplaced yes)',
                    f'\t\t(effects (font (size 1.27 1.27)) (justify {just}))',
                    f'\t\t(uuid "{u(f"lbl{unit}_{num}")}")', '\t)']
    return "\n".join(out)

# ---- stock Device:R, embedded for the RESET pull-down ----
STOCK = r"C:/Program Files/KiCad/10.0/share/kicad/symbols/Device.kicad_sym"
_s = open(STOCK, encoding="utf-8").read()
_i = _s.index('\t(symbol "R"\n'); _d = 0
for _j in range(_i, len(_s)):
    if _s[_j] == "(": _d += 1
    elif _s[_j] == ")":
        _d -= 1
        if _d == 0: break
res_def = _s[_i:_j + 1].replace('(symbol "R"', '(symbol "Device:R"', 1)   # parent only (see ledger)

RPOS = (snap(408.0), snap(120.0))

def reset_pulldown():
    px, py = RPOS
    out = ['\t(symbol', '\t\t(lib_id "Device:R")', f'\t\t(at {px} {py} 0)', '\t\t(unit 1)',
           '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)', '\t\t(dnp no)',
           f'\t\t(uuid "{u("rst_r")}")',
           f'\t\t(property "Reference" "R1" (at {px + 3.5} {py - 1.3} 0) (effects (font (size 1.27 1.27)) (justify left)))',
           f'\t\t(property "Value" "10k" (at {px + 3.5} {py + 1.3} 0) (effects (font (size 1.27 1.27)) (justify left)))',
           '\t\t(instances', '\t\t\t(project "ODSP12-MB"',
           f'\t\t\t\t(path "/{ROOT_UUID}/{SHEET_SYM_UUID}" (reference "R1") (unit 1))',
           '\t\t\t)', '\t\t)', '\t)']
    # Device:R pins sit at (0, +/-3.81) in symbol coords
    for sy, net, rot, just in ((3.81, "DSP_RESET_N", 90, "left"), (-3.81, GND, 270, "left")):
        x, y = snap(px), snap(py - sy)
        out += [f'\t(global_label "{net}"', '\t\t(shape bidirectional)', f'\t\t(at {x} {y} {rot})',
                '\t\t(fields_autoplaced yes)',
                f'\t\t(effects (font (size 1.27 1.27)) (justify {just}))',
                f'\t\t(uuid "{u("rstlbl" + net)}")', '\t)']
    return "\n".join(out)

# ---- sheet notes: defences placed where the mistake would be made (F28 principle) ----
NOTES = [
    (150.0, 34.0,
     "AVDD (pin 7) and PVDD (pin 15) are REQUIRED even though AUXADC0-5 are unused and\\n"
     "even if the PLL were unused -- ADAU1466 Rev.C p.33, V-22. Do not drop either rail.\\n"
     "The six AUXADC no-connects below make 'drop AVDD' look like a free optimisation. It is not."),
    (150.0, 46.0,
     "R1 holds RESET low if its driver is absent or high-Z (Rev.C p.34), backing up the\\n"
     "internal pull-down. Fail-safe polarity: unpowered = held in reset."),
    (150.0, 54.0,
     "Every pin on this sheet has an explicit disposition -- net label or no-connect (F28).\\n"
     "Unused-pin policy is PER PART, sourced from that part's own datasheet. No board-wide default."),
]

def notes():
    out = []
    for i, (x, y, txt) in enumerate(NOTES):
        out += [f'\t(text "{txt}"', f'\t\t(exclude_from_sim no)', f'\t\t(at {snap(x)} {snap(y)} 0)',
                '\t\t(effects (font (size 1.27 1.27)) (justify left top))',
                f'\t\t(uuid "{u(f"note{i}")}")', '\t)']
    return "\n".join(out)

body = "\n".join([sym_instance(un) for un in (1, 2, 3)] + [labels(un) for un in (1, 2, 3)]
                 + [reset_pulldown(), notes()])

sch = f'''(kicad_sch
\t(version {VER})
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{SHEET_UUID}")
\t(paper "A3")
\t(title_block
\t\t(title "ODSP-12 :: DSP and Clock Tree")
\t\t(date "2026-08-16")
\t\t(rev "A")
\t\t(comment 1 "ODSP12-MB-A")
\t\t(comment 2 "Every pin has an explicit disposition -- net or no-connect (F28)")
\t)
\t(lib_symbols
{adau}
{res_def}
\t)
{body}
\t(embedded_fonts no)
)
'''
open(DEST, "w", encoding="utf-8", newline="\n").write(sch)
print("wrote", DEST)
