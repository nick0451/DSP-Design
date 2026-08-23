# Generates 02_dsp.kicad_sch -- the ADAU1466 and its clock tree.
#
# Net names follow REQUIREMENTS.md section 10 [HARD]. Every pin gets an explicit
# disposition per F28: a net label, a rail, or an explicit no-connect. Nothing floats
# by accident and nothing is left unannotated.
import os, re, uuid, math

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
# F109: U1 is emitted by this hand-rolled block, NOT by place(), so the generic
# FPMAP patch did not reach it -- the same defect one level down. Parsed from the
# same block the symbol comes from, so there is one source of truth, not two.
_m = re.search(r'\(property "Footprint" "([^"]*)"', adau)
assert _m and _m.group(1), "ADAU1466 symbol carries no footprint"
ADAU_FP = _m.group(1)

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
NETS.update({21: "MCLK_DSP", 24: "DSP_RESET_N", 34: "DSP_SELFBOOT"})
NETS.update({33: "SPI_DSP_SS_N", 31: "SPI_DSP_SCLK", 32: "SPI_DSP_MOSI", 30: "SPI_DSP_MISO"})
NETS.update({4: "SPDIF_RX_IN", 5: "SPDIF_TX_OUT"})
NETS.update({63: "DSP_THD_M", 64: "DSP_THD_P"})
# explicit no-connects, each justified
NC = {
    22: "XTALOUT - external XO used, not a crystal",
    23: ("CLKOUT - DELIBERATELY UNUSED. This is the pin a future engineer reaches for to feed a "
         "converter's MCLK, and doing so is EXACTLY the daisy chain S3 [HARD] forbids: the "
         "converters take MCLK from the fanout buffer, never from the DSP. See the clock note."),
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
           f'\t\t(property "Value" "ADAU1466WBCPZ300" (at {px} {py - 2.5} 0) (effects (font (size 1.27 1.27))))'
           f'\t\t(property "Footprint" "{ADAU_FP}" (at {px} {py} 0) (effects (font (size 1.27 1.27)) (hide yes)))']
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


# ======================================================================================
# THE S3 [HARD] CLOCK TREE.  XO -> fanout -> four converters, point to point.
# ======================================================================================
PROJ = os.path.join(HW, "lib", "ODSP12.kicad_sym")
STOCKD = r"C:/Program Files/KiCad/10.0/share/kicad/symbols"

def extract(path, name):
    t = open(path, encoding="utf-8").read()
    m = re.search(r'\t\(symbol "' + re.escape(name) + r'"\n', t)
    if not m: raise KeyError(name)
    i = m.start(); d = 0
    for j in range(i, len(t)):
        if t[j] == "(": d += 1
        elif t[j] == ")":
            d -= 1
            if d == 0: break
    blk = t[i:j + 1]
    pins = []
    for mm in re.finditer(r'\(pin\s+\w+\s+\w+[\s\S]{0,400}?\(number "([^"]+)"', blk):
        at = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', mm.group(0))
        if at: pins.append((mm.group(1), float(at.group(1)), float(at.group(2))))
    assert pins, f"{name}: zero pins"
    return blk, pins

CSRC = {"ODSP12:XO_LVCMOS": (PROJ, "XO_LVCMOS"),
        "ODSP12:LMK1C1104": (PROJ, "LMK1C1104"),
        "Device:C": (STOCKD + "/Device.kicad_sym", "C")}
CDEFS, CGEO = {}, {}
for libid, (path, nm) in CSRC.items():
    blk, pins = extract(path, nm)
    base = libid.split(":")[1]
    blk = blk.replace(f'(symbol "{nm}_', f'(symbol "{base}_')
    CDEFS[libid] = blk.replace(f'(symbol "{nm}"', f'(symbol "{libid}"', 1)
    CGEO[libid] = {p[0]: (p[1], p[2]) for p in pins}

# F109: the footprint must land on the INSTANCE, not only in the library symbol.
# The netlist exporter reads instance properties; before this, 536 of 536 exported none.
FPMAP = {}
for _lid, _blk in CDEFS.items():
    _m = re.search(r'\(property "Footprint" "([^"]*)"', _blk)
    FPMAP[_lid] = _m.group(1) if _m else ""
CGEO["Device:R"] = {"1": (0.0, 3.81), "2": (0.0, -3.81)}

CLABELS = {}
def cemit(net, lx, ly, rot, just, uid):
    prev = CLABELS.get((lx, ly))
    assert prev is None or prev == net, (
        f"LABEL COLLISION at ({lx}, {ly}): '{prev}' and '{net}' would be shorted.")
    CLABELS[(lx, ly)] = net
    return [f'\t(global_label "{net}"', '\t\t(shape bidirectional)',
            f'\t\t(at {lx} {ly} {rot})', '\t\t(fields_autoplaced yes)',
            f'\t\t(effects (font (size 1.27 1.27)) (justify {just}))',
            f'\t\t(uuid "{uid}")', '\t)']

CPLACE = []
def cplace(ref, libid, x, y, val, nets):
    x, y = snap(x), snap(y)
    geo = CGEO[libid]
    missing = set(geo) - set(nets)
    assert not missing, f"{ref}: pins with no disposition (F28): {sorted(missing)}"
    assert not (set(nets) - set(geo)), f"{ref}: nets on non-existent pins"
    out = ['\t(symbol', f'\t\t(lib_id "{libid}")', f'\t\t(at {x} {y} 0)', '\t\t(unit 1)',
           '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)', '\t\t(dnp no)',
           f'\t\t(uuid "{u("ci" + ref)}")',
           f'\t\t(property "Reference" "{ref}" (at {x} {y - 12} 0) (effects (font (size 1.27 1.27))))',
           f'\t\t(property "Value" "{val}" (at {x} {y - 9} 0) (effects (font (size 1.27 1.27))))',
           f'\t\t(property "Footprint" "{FPMAP.get(libid, "")}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))' ,
           '\t\t(instances', '\t\t\t(project "ODSP12-MB"',
           f'\t\t\t\t(path "/{ROOT_UUID}/{SHEET_SYM_UUID}" (reference "{ref}") (unit 1))',
           '\t\t\t)', '\t\t)', '\t)']
    for num, (sx, sy) in geo.items():
        lx, ly = snap(x + sx), snap(y - sy)
        if nets[num] is None:
            out.append(f'\t(no_connect (at {lx} {ly}) (uuid "{u("cnc" + ref + num)}"))')
            continue
        out += cemit(nets[num], lx, ly, 180 if sx < 0 else 0,
                     "right" if sx < 0 else "left", u("cl" + ref + num))
    CPLACE.append("\n".join(out))

CLKR = "+3V3_CLK"
FANOUT = [("3", "MCLK_DSP", "R50"), ("8", "MCLK_ADC", "R51"),
          ("5", "MCLK_DAC_A", "R52"), ("7", "MCLK_DAC_B", "R53")]

# --- PLL loop filter (PLLFILT, pin 16) ------------------------------------------------
# ADI Figure 16 "PLL Filter", Rev. C p.30, RENDERED 200 dpi -- adopted VERBATIM, not designed.
# The datasheet does not invite a loop-filter design: it gives one network and a tolerance
# rule, and our operating point IS its stated design centre. Same reasoning as the library
# policy's "vendor footprint verbatim where one exists".
#
# TOPOLOGY, and the part a from-memory design gets wrong: THE FILTER RETURNS TO PVDD, NOT
# TO GROUND. Two parallel paths between PVDD (pin 15) and PLLFILT (pin 16):
#     PVDD --150pF-- PLLFILT           (direct shunt)
#     PVDD --5.6nF-- MID --4.3k-- PLLFILT
#
# Table on the same page confirms our operating point is ADI's NOMINAL, not an extrapolation:
#     MCLK 24.576 MHz -> predivider 8 -> PLL input 3.072 MHz -> feedback x96 -> 294.912 MHz
# and the text says the recommended filter is FOR "a nominal 3.072 MHz PLL input and a
# 294.912 MHz system clock output" -- exactly us -- adding "this filter works for the full
# frequency range of the PLL".
PLL_MID = "PLL_LF_MID"
cplace("C61", "Device:C", 430, 200, "150p C0G 5%", {"1": "+3V3_PLL", "2": "PLLFILT"})
cplace("C60", "Device:C", 460, 185, "5n6 C0G 5%", {"1": "+3V3_PLL", "2": PLL_MID})
cplace("R60", "Device:R", 490, 200, "4k3 1%", {"1": PLL_MID, "2": "PLLFILT"})

cplace("Y1", "ODSP12:XO_LVCMOS", 60, 200, "PLACEHOLDER F56 -- 24.576 MHz",
       {"1": "XO_OE", "2": GND, "3": "CLK_24M576", "4": CLKR})
cplace("R54", "Device:R", 30, 200, "1k", {"1": CLKR, "2": "XO_OE"})
cplace("C50", "Device:C", 30, 225, "100n", {"1": CLKR, "2": GND})

cplace("U50", "ODSP12:LMK1C1104", 200, 200, "LMK1C1104PWR",
       {"1": "CLK_24M576", "2": "CLK_1G", "6": CLKR, "4": GND,
        **{p: f"U50_Y{i}" for i, (p, _n, _r) in enumerate(FANOUT)}})
cplace("R55", "Device:R", 150, 170, "10k", {"1": CLKR, "2": "CLK_1G"})
cplace("C51", "Device:C", 255, 235, "100n", {"1": CLKR, "2": GND})
cplace("C52", "Device:C", 285, 235, "1u", {"1": CLKR, "2": GND})
for i, (_p, net, ref) in enumerate(FANOUT):
    cplace(ref, "Device:R", 320, 175 + i * 18, "0R", {"1": f"U50_Y{i}", "2": net})

# ---- sheet notes: defences placed where the mistake would be made (F28 principle) ----

# ---- clock-tree notes: the seven published criteria, in copper and in writing ----
PLLNOTE = (
    "PLL LOOP FILTER -- ADOPTED VERBATIM FROM ADI FIGURE 16, NOT DESIGNED. AND THE ONE\n"
    "THING A FROM-MEMORY DESIGN GETS WRONG: IT RETURNS TO PVDD, NOT TO GROUND.\n"
    "\n"
    "  Source: ADAU1462/ADAU1466 Rev. C p.30, Figure 16 'PLL Filter', RENDERED 200 dpi.\n"
    "\n"
    "      PVDD (15) --+---- 5n6 ----+                 C60  5n6  C0G 5%\n"
    "                  |             |                 C61  150p C0G 5%\n"
    "                150p          4k3                 R60  4k3  1%\n"
    "                  |             |\n"
    "   PLLFILT (16) --+-------------+\n"
    "\n"
    "  WHY VERBATIM RATHER THAN DERIVED: the datasheet does not invite a loop-filter\n"
    "  design. It gives ONE network plus a tolerance rule, and OUR OPERATING POINT IS ITS\n"
    "  STATED DESIGN CENTRE -- not an extrapolation from it. Same page, same table:\n"
    "     MCLK 24.576 MHz -> predivider 8 -> PLL input 3.072 MHz -> x96 -> 294.912 MHz\n"
    "  and the text specifies the filter FOR 'a nominal 3.072 MHz PLL input and a 294.912\n"
    "  MHz system clock output', adding 'this filter works for the full frequency range of\n"
    "  the PLL'. Deriving our own would be replacing a characterised network with an\n"
    "  uncharacterised one to no end. (Library policy's 'vendor part verbatim', applied to\n"
    "  a circuit instead of a footprint.)\n"
    "\n"
    "  TOLERANCE IS A SPECIFICATION HERE, NOT A PREFERENCE. Verbatim: 'Because the centre\n"
    "  frequency and bandwidth of the loop filter is determined by the values of the\n"
    "  included components, use high accuracy (low tolerance) components. Components that\n"
    "  are valued within 10% of the recommended component values and with a 15% OR LOWER\n"
    "  TOLERANCE are suitable.' So: 5% C0G on both caps and 1% on the resistor clear it\n"
    "  with room. C0G RATHER THAN X7R IS THE POINT -- X7R's voltage coefficient would move\n"
    "  the loop bandwidth with the PLLFILT bias, which is exactly the parameter the\n"
    "  sentence above says is set by these values. A 10% X7R part meets the tolerance\n"
    "  number on paper and misses its intent.\n"
    "\n"
    "  PLLFILT BIAS is internally generated, 'typically between 1.65 V and 2.10 V' (p.30).\n"
    "  Against PVDD = +3V3_PLL that is ~1.2-1.65 V across the network. No stress, and it is\n"
    "  why a 16 V C0G part is ample.\n"
    "\n"
    "  *** LAYOUT CONSTRAINT, ADI p.197, VERBATIM -- THIS IS A BLOCK D/E INPUT: ***\n"
    "  'To minimize jitter, connect the single resistor and two capacitors in the PLL\n"
    "   filter to the PLLFILT and PVDD pins with SHORT TRACES.'\n"
    "  Three parts, both pins, short. It is the only placement instruction ADI gives for\n"
    "  this network and it is a jitter argument, so it outranks tidiness.\n"
    "\n"
    "  NOTE PVDD IS ITS OWN NET (+3V3_PLL, F33) AND IS RESOLVED ON THE POWER SHEET. The\n"
    "  filter's PVDD end must land on THAT rail, not on a convenient +3V3_D -- the whole\n"
    "  point of the separate net is that the PLL's supply reference is not the digital one.\n"
)

CLKNOTE1 = (
    "S3 [HARD] CLOCK TREE -- ONE XO, ONE FANOUT, FOUR POINT-TO-POINT LINKS. NO DAISY CHAIN.\n"
    "\n"
    "  Y1  24.576 MHz LVCMOS  ->  U50 LMK1C1104  ->  Y0  MCLK_DSP    (U1  pin 21)\n"
    "                                                Y1  MCLK_ADC    (U40 pin 16)\n"
    "                                                Y2  MCLK_DAC_A  (U51 pin 1)\n"
    "                                                Y3  MCLK_DAC_B  (U52 pin 1)\n"
    "\n"
    "FOUR OUTPUTS, FOUR LOADS, 1:1 -- AND THAT IS A CHANGE. Both AK4458s previously shared one\n"
    "MCLK_DAC net, which left the fourth fanout output unused and forked a clock trace into two\n"
    "loads. A fork is an impedance discontinuity and a reflection. It is not literally a daisy\n"
    "chain, but the buffer exists precisely so that no converter's clock depends on another's\n"
    "stub, and there was no reason to spend that. Split into MCLK_DAC_A / MCLK_DAC_B.\n"
    "\n"
    "24.576 MHz = 512 fs at 48 kHz, which is what lets ONE oscillator serve every converter:\n"
    "  AK5574 512fs (V-04)   AK4458 512fs or 768fs at 30-54 kHz (T1-26)   ADAU1466 PLL input\n"
    "\n"
    "MCLK INPUT REQUIREMENTS, VERIFIED AGAINST THE PART HARDEST TO SATISFY (Rev.C p.29):\n"
    "  f_MCLK  2.375 .. 36 MHz          -> 24.576 MHz sits mid-range\n"
    "  DUTY -- AND THE BINDING NUMBER IS THE CONVERTER'S, NOT THE DSP's. The ADAU1466 asks\\n"
    "  only 25..75 % (p.29). THE AK5574 ASKS 45..55 % (dCLK, S11 Switching Characteristics\\n"
    "  p.19, figure read) -- 2.5x tighter, and a real specification some oscillators miss\\n"
    "  where 25..75 % is cleared by every LVCMOS part ever made. CITE THE CONVERTER.\\n"
    "  AND THE BUDGET DOES NOT CLOSE BY ITSELF: the LMK1C1104 specifies output duty 45..55 %\\n"
    "  but ONLY for a 50 % input -- its duty transfer for a non-50 % input is not\\n"
    "  characterised at all. XO 45..55 -> buffer 45..55 -> converter needs 45..55 puts every\\n"
    "  element at the same limit with NOTHING allocated to the buffer. SO THE XO IS SPECIFIED\\n"
    "  TIGHTER THAN ITS LOAD: 48..52 %, leaving the buffer 3 % each side. Many parts hold\\n"
    "  +/-2 %; it costs nothing and turns an unallocated term into a stated one.\\n"
    "  ALL FOUR LOADS SEE THE BUFFER, not the XO, so there is ONE duty requirement here and\\n"
    "  it is the converters' 45..55 % measured at the buffer output.\\n"
    "  Pin 21 accepts a clock DIRECTLY; XTALOUT (22) is a no-connect because we drive the pin\n"
    "  rather than hang a crystal on it.\n"
    "\n"
    "+3V3_CLK IS ITS OWN RAIL AND THAT IS F33's REASON, NOT A CONVENIENCE: the clock tree is the\n"
    "one place where supply noise becomes PHASE noise, and phase noise at the converters is not\n"
    "removable downstream by any filter, digital or analog."
)

CLKNOTE2 = (
    "TWO ENABLE PINS, BOTH DRAWN, BOTH FAIL-SAFE TOWARD KEEPING THE CLOCK RUNNING.\n"
    "\n"
    "R55 10k PULLS 1G UP TO +3V3_CLK, AND IT IS A FITTED PART, NOT A DISPOSITION (F21).\n"
    "T1-68: the LMK1C1104's 1G carries an INTERNAL 300 kOhm PULL-DOWN and 'switches the outputs\n"
    "into a low state when 1G is low'. So a floating 1G does not degrade the clock tree --\n"
    "IT TURNS THE WHOLE THING OFF, and no MCLK reaches any converter on the board. A DNP here\n"
    "is a dead board, which is why the resistor is drawn rather than noted. 10k against the\n"
    "internal 300k holds 1G at 0.968 x VDD.\n"
    "\n"
    "1G IS DELIBERATELY *NOT* ON A GPIO -- see CLKNOTE3. Gating this pin from the MCU is the\n"
    "power-saving idea that breaks the sequencing precondition, and the way to make sure it\n"
    "gets considered rather than assumed is to make it require a schematic edit.\n"
    "\n"
    "R54 1k HOLDS THE XO's PIN 1 HIGH. The part is not pinned (F56) and pin 1 is OE, ST or NC\n"
    "depending on the variant that arrives. High is the enabled state for OE and for ST, and it\n"
    "is harmless on an NC variant -- so ONE resistor is correct for every candidate, and the\n"
    "position exists so the level can be moved without cutting a track.\n"
    "\n"
    "SOURCE TERMINATION AT EVERY OUTPUT -- R50..R53, FITTED, CURRENTLY 0R.\n"
    "  LMK1C1104 R_OUT = 50 Ohm typ at VDD = 3.3 V (SNAS791D, table read). Source termination\n"
    "  wants   R_series = Z0 - R_OUT\n"
    "  so THE VALUE CANNOT BE FINALISED HERE: Z0 depends on the stackup and the stackup is\n"
    "  UNSET (Block D/E). Per S0 the step that depends on it does not run -- but the step that\n"
    "  does not depend on it does, so the POSITION is fitted at 0R and the change is a value\n"
    "  rather than a respin. HANDED TO BLOCK E EXPLICITLY:\n"
    "    * state Z0 for the four MCLK traces, then set R50-R53 = Z0 - 50 Ohm\n"
    "    * LENGTH MATCHING IS NOT REQUIRED. These are four independent point-to-point MCLK\n"
    "      links, not a bus; nothing compares their arrival times. What matters is that each\n"
    "      is short, direct, and over an unbroken reference plane.\n"
    "      BUT BOUND THE ABSOLUTE LENGTH, WHICH IS THE CONSTRAINT THAT DOES BITE: source\\n"
    "      termination assumes an unterminated high-impedance far end, and at 0.35 ns edges\\n"
    "      the transmission-line regime starts near 50-60 mm. KEEP EACH LINK UNDER ~50 mm.\\n"
    "      Why matching is pointless: the buffer's own output-output skew is 25 ps typ /\\n"
    "      50 ps max, MORE THAN ~8 mm OF TRACE -- matching tighter than the part's own skew\\n"
    "      does not even reach the dominant term. AK5574 S12 also states outright that MCLK\\n"
    "      must be synchronised with BICK/LRCK 'but the phase is not important'.\\n"
    "    * the fanout's own output-output skew is 25 ps typ / 50 ps max -- orders below\n"
    "      anything a 48 kHz system can resolve, so skew is not the budget item. JITTER is."
    "\\n"
    "JITTER: THE SPEC IS UNQUOTABLE AT OUR OPERATING POINT, SO THE BUDGET IS WRITTEN INSTEAD\\n"
    "AND THE SPEC STOPS MATTERING -- the same move that closed V-26.\\n"
    "  Jitter-limited SNR:  SNR = -20 log10( 2.pi . f_sig . t_j )\\n"
    "  At f_sig = 20 kHz:   121 dB needs t_j <= 7.09 ps RMS       112 dB needs 20 ps\\n"
    "  LMK1C1104 additive jitter 8 fs typ / 20 fs max -- 355x BELOW the 121 dB budget. Its\\n"
    "  test conditions do not match us (f_IN 156.25 MHz; slew 2 V/ns against a 0.1 V/ns\\n"
    "  minimum; integration 12 kHz-20 MHz, which exceeds half our carrier). Degrade it 10x\\n"
    "  for slew and it is still 35x below, and it adds in QUADRATURE with the oscillator.\\n"
    "  CONSEQUENCE WORTH MORE THAN THE NUMBER: a commodity 24.576 MHz XO at ~1 ps clears\\n"
    "  7.09 ps by 7x. JITTER IS NOT THIS OSCILLATOR'S BINDING CRITERION -- duty and\\n"
    "  frequency stability over -20..+70 degC are. S3 [HARD] does say LOW-JITTER XO, so\\n"
    "  relaxing that is the OPERATOR'S call, not a design economy to be taken quietly.\\n"
    "  'DROP THE LMK AND FAN OUT FROM CLKOUT' IS NOT AVAILABLE -- AND HERE IS THE\n"
    "  ARITHMETIC, NOT JUST THE VERDICT. A verdict invites challenge; a verdict with its\n"
    "  arithmetic attached answers the challenge in advance (adversary 010).\n"
    "    ADAU1466 CLKOUT jitter = 12 typ / 106 ps max, CYCLE-TO-CYCLE RMS (Table 6, p.9).\n"
    "    Budget = 7.09 ps RMS for 121 dB at 20 kHz.   106 / 7.09 = 15x OVER, ON THE RAW\n"
    "    FIGURE, BEFORE any metric conversion is attempted at all.\n"
    "    Cycle-to-cycle RMS is NOT aperture jitter and the two DO NOT INTERCONVERT -- but\n"
    "    no c2c-to-aperture relationship is favourable enough to recover 15x, let alone\n"
    "    the four orders of magnitude against the buffer. THE GAP SURVIVES THE CAVEAT.\n"
)

CLKNOTE4 = (
    "BCLK IS TWO NET CLASSES, NOT ONE. FW-010, F70.\n"
    "  TDM_IN0_BCLK   (AK5574)      128 fs =  6.144 MHz   TDM128, Table 9 row 26\n"
    "  TDM_OUT0_BCLK  (AK4458 #1)   256 fs = 12.288 MHz   TDM256, Table 13 Mode 18\n"
    "  TDM_OUT1_BCLK  (AK4458 #2)   256 fs = 12.288 MHz   TDM256, Table 13 Mode 18\n"
    "Same MCLK, same LRCK, same format -- DIFFERENT BICK, by a factor of two. Our register\n"
    "carried 'both 128 fs' until 2026-08-22; it was wrong for the DAC half and no termination\n"
    "or routing decision had yet been taken against it. Do not treat these three as one class.\n"
    "\n"
    "AND THE EDGE RATE ON THE TWO FAST NETS IS A FIRMWARE REGISTER, NOT A RESISTOR. FW-013.\n"
    "There is NO series termination anywhere on these nets. The only edge-rate control is\n"
    "ADAU1466 0xF784-0xF787 BCLK_OUTx_PIN (BCLK_OUT_SLEW / BCLK_OUT_DRIVE, reset 0x0018, RW).\n"
    "So if layout gives these long runs, slew is a knob firmware can turn -- and if firmware\n"
    "leaves the reset defaults and nobody records that this was a choice, it is a SILENT one.\n"
    "A signal-integrity parameter owned by software is unusual; it is written here so the\n"
    "layout engineer meets it at the net rather than in a boot log.\n"
)

CLKNOTE3 = (
    "NO SPREAD SPECTRUM ON THIS SHEET. EVER. S3 [HARD], RESTATED IN COPPER BECAUSE THIS IS\n"
    "WHERE THE FIX WOULD BE PROPOSED.\n"
    "The bucks on 01_power DO use spread spectrum and that is correct and decreed. If an EMI\n"
    "problem appears at 24.576 MHz or a harmonic, the tempting fix is to dither this clock.\n"
    "That converts a narrow spur into MODULATED JITTER at the converters -- broadband noise in\n"
    "the audio band, removable by nothing downstream. The prohibition covers the AUDIO CLOCK\n"
    "TREE ONLY; it is not a general EMC posture, and the two must not be conflated in either\n"
    "direction.\n"
    "\n"
    "RAILS-UP-BEFORE-PDN IS A PROPERTY OF THIS TREE, STATED HERE BECAUSE THIS IS WHERE THE\n"
    "PROPOSAL THAT BREAKS IT WOULD ARRIVE.\n"
    "ADAU1466 Rev.C p.24: 'the crystal oscillator circuit must provide a stable master clock to\n"
    "the XTALIN/MCLK pin by the time the PVDD supply reaches its nominal level.' READ THE\n"
    "CONDITION WITH IT: that sentence is written for the CRYSTAL case and we drive the pin\n"
    "externally, so it is the vendor's statement of intent rather than a spec that literally\n"
    "binds our configuration. The same page adds that the pin is gated internally until the\n"
    "DVDD POR and the PVDD-to-DVDD level shifter initialise, and that boot needs eight MCLK\n"
    "cycles. S7.2 step 5a-pre separately requires MCLK running before PDN release.\n"
    "\n"
    "SATISFIED BY CONSTRUCTION, WHICH IS THE ONLY REASON IT IS NOT A SEQUENCING STEP: the tree\n"
    "runs from +3V3_CLK, up with the analog rails, before the MCU boots and long before any PDN\n"
    "is released -- and both enables are hard-tied. There is no ordering firmware can get wrong,\n"
    "because there is no ordering firmware controls.\n"
    "\n"
    "  THE PROPOSAL THAT BREAKS IT: 'gate the fanout from a GPIO to save power in standby.'\n"
    "  It moves MCLK from a rail-timed guarantee to a firmware-timed one, at the pin whose\n"
    "  failure mode is SILENCE rather than degradation. If it is ever wanted, S7.2 gains a real\n"
    "  step and BRINGUP gains a real test. It is not a resistor change.\n"
    "\n"
    "VERIFIED AT BRING-UP RATHER THAN TRUSTED: scope MCLK AT THE ADC PIN, not at the buffer,\n"
    "and confirm it is running before PDN rises. BRINGUP.md S4 carries the line."
)

NOTES = [
    (150.0, 34.0,
     "AVDD (pin 7) and PVDD (pin 15) are REQUIRED even though AUXADC0-5 are unused and\n"
     "even if the PLL were unused -- ADAU1466 Rev.C p.33, V-22. Do not drop either rail.\n"
     "The six AUXADC no-connects below make 'drop AVDD' look like a free optimisation. It is not."),
    (150.0, 46.0,
     "R1 holds RESET low if its driver is absent or high-Z (Rev.C p.34), backing up the\n"
     "internal pull-down. Fail-safe polarity: unpowered = held in reset."),
    (150.0, 54.0,
     "Every pin on this sheet has an explicit disposition -- net label or no-connect (F28).\n"
     "Unused-pin policy is PER PART, sourced from that part's own datasheet. No board-wide default."),
    (150.0, 62.0, CLKNOTE1),
    (150.0, 70.0, CLKNOTE2),
    (150.0, 78.0, CLKNOTE3),
    (150.0, 86.0, PLLNOTE),
    (150.0, 94.0, CLKNOTE4),
]

# C2: OVERFLOW AND OVERLAP ARE DIFFERENT FAILURES OF THE SAME FAMILY, AND A CHECK FOR ONE IS
# SILENT ON THE OTHER. 06_analog_in's page-extent assert passed while NOTE5 grew straight through
# NOTE6 -- two boxes can overlap perfectly while their union still fits the frame. So notes are
# STACKED by measured height (construction) and then CHECKED for intersection (verification),
# because M3 is two clauses and the second one is the half that gets skipped.
ESC = chr(92) + "n"
def note_extent(txt):
    lines = txt.split(ESC)
    return max(len(l) for l in lines) * 0.85, len(lines) * 1.9
def stack_notes(items, gap=6.0):
    out, y = [], None
    for x, y0, t in items:
        t = t.replace(chr(10), ESC)
        y = y0 if y is None else max(y, y0)
        w, h = note_extent(t)
        out.append((x, y, t, w, h)); y += h + gap
    return out
# ADVERSARY 038: THIS CHECK USED TO BE INLINE, AND THAT IS WHY IT WENT TWELVE LEGS WITHOUT A
# NEGATIVE TEST. I had claimed it was untestable -- 'I would have to defeat the stacker to test
# the checker' -- which was wrong, and my own F78 guard disproved it the same morning: you do
# not defeat the producer, you HAND THE CHECKER FABRICATED DATA. It could not be handed anything
# while it was welded to the stacker's output, so the fix was to move the seam, not to write a
# cleverer test.
#
#   A GUARD THAT CAN ONLY BE TESTED BY BREAKING ITS PRODUCER HAS BEEN WRITTEN AT THE WRONG LAYER.
#
# Signature is now (list of boxes) -> ok, so it takes DATA rather than generator state.
def assert_no_note_overlap(boxes, tag=""):
    for _a in range(len(boxes)):
        for _b in range(_a + 1, len(boxes)):
            ax, ay, aw, ah = boxes[_a][0], boxes[_a][1], boxes[_a][3], boxes[_a][4]
            bx, by, bw, bh = boxes[_b][0], boxes[_b][1], boxes[_b][3], boxes[_b][4]
            if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah:
                raise AssertionError(
                    f"NOTE BOX OVERLAP{tag}: note {_a} at ({ax:.0f},{ay:.0f}) {aw:.0f}x{ah:.0f} "
                    f"intersects note {_b} at ({bx:.0f},{by:.0f}). Two notes can overlap while "
                    f"the PAGE still fits, which is why the page-extent assert does not see this.")
    return len(boxes)

# M9 NEGATIVE TEST, at last. Two fabricated boxes that must intersect, and the same two pulled
# apart -- no stacker involved in either direction, which was the whole point.
_ov_bad  = [(0.0, 0.0, "a", 50.0, 20.0), (10.0, 10.0, "b", 50.0, 20.0)]   # must FAIL
_ov_good = [(0.0, 0.0, "a", 50.0, 20.0), (0.0, 21.0, "b", 50.0, 20.0)]    # must PASS
try:
    assert_no_note_overlap(_ov_bad, " [NEGATIVE TEST]")
    raise SystemExit("OVERLAP GUARD IS DEFECTIVE: it passed two boxes that plainly intersect (M9).")
except AssertionError:
    pass
assert_no_note_overlap(_ov_good, " [POSITIVE CONTROL]")
print("  overlap guard: negative test FIRED, positive control PASSED (M9 satisfied)")

NOTES = stack_notes(NOTES)
assert_no_note_overlap(NOTES)
NOTES = [(x, y, t) for x, y, t, _w, _h in NOTES]

def notes():
    out = []
    for i, (x, y, txt) in enumerate(NOTES):
        out += [f'\t(text "{txt}"', f'\t\t(exclude_from_sim no)', f'\t\t(at {snap(x)} {snap(y)} 0)',
                '\t\t(effects (font (size 1.27 1.27)) (justify left top))',
                f'\t\t(uuid "{u(f"note{i}")}")', '\t)']
    return "\n".join(out)

body = "\n".join([sym_instance(un) for un in (1, 2, 3)] + [labels(un) for un in (1, 2, 3)]
                 + CPLACE + [reset_pulldown(), notes()])

# The page is DERIVED from content and asserted (F53); note boxes are separately checked for
# intersection above (C2). Overflow and overlap are different failures of the same family.
_X = [lx for lx, _ in CLABELS] + [420.0]
_Y = [ly for _, ly in CLABELS] + [260.0]
for _x, _y, _t in NOTES:
    _w, _h = note_extent(_t); _X.append(_x + _w); _Y.append(_y + _h)
PAPER_W = math.ceil((max(_X) + 25) / 10) * 10
PAPER_H = math.ceil((max(_Y) + 25) / 10) * 10
assert PAPER_W <= 1200 and PAPER_H <= 1200, f"page {PAPER_W} x {PAPER_H} mm exceeds the limit"

sch = f'''(kicad_sch
\t(version {VER})
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{SHEET_UUID}")
\t(paper "User" {PAPER_W:.1f} {PAPER_H:.1f})
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
{chr(10).join(CDEFS.values())}
\t)
{body}
\t(embedded_fonts no)
)
'''
open(DEST, "w", encoding="utf-8", newline="\n").write(sch)
print("wrote", DEST)
print(f"  clock tree: {len(CPLACE)} devices, {len(CLABELS)} labels, no collisions")
print(f"  page {PAPER_W:.0f} x {PAPER_H:.0f} mm, derived and asserted; note boxes checked for overlap")
