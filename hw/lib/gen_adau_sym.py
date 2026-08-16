# ADAU1466 symbol generator.
# SOURCE OF TRUTH: adau1462-1466.pdf Rev. C, Table 18 "Pin Function Descriptions"
# (pp. 18-21), cross-checked against Figure 11 "Pin Configuration" (p. 18).
# METHOD (STATE.md M2): figure-level render at 170 dpi + read, BOTH sources,
# agreement required. Not text-extracted -- see the T1-28 retraction.
import os

VER = "20251024"   # verified from share/kicad/symbols/Device.kicad_sym

# (pin, name, electrical type, unit)
# unit 1 = Power/Ground, 2 = Serial Audio Ports, 3 = Control/Clock/Aux
PINS = [
    # ---- Unit 1: power, ground, regulator, PLL ----
    (1,  "DGND",   "power_in", 1), (17, "DGND",   "power_in", 1),
    (19, "DGND",   "power_in", 1), (25, "DGND",   "power_in", 1),
    (36, "DGND",   "power_in", 1), (37, "DGND",   "power_in", 1),
    (54, "DGND",   "power_in", 1), (55, "DGND",   "power_in", 1),
    (72, "DGND",   "power_in", 1),
    (6,  "AGND",   "power_in", 1), (14, "PGND",   "power_in", 1),
    (2,  "IOVDD",  "power_in", 1), (18, "IOVDD",  "power_in", 1),
    (38, "IOVDD",  "power_in", 1), (56, "IOVDD",  "power_in", 1),
    (20, "DVDD",   "power_in", 1), (35, "DVDD",   "power_in", 1),
    (53, "DVDD",   "power_in", 1), (71, "DVDD",   "power_in", 1),
    (7,  "AVDD",   "power_in", 1), (15, "PVDD",   "power_in", 1),
    (16, "PLLFILT", "passive",  1),
    (3,  "VDRIVE", "output",   1),      # -> GND when DVDD fed externally (F18)
    ("EP", "EP",   "power_in", 1),      # exposed pad; see F25

    # ---- Unit 2: serial audio ports ----
    (59, "SDATA_IN0",      "input",         2),
    (57, "BCLK_IN0",       "bidirectional", 2),
    (58, "LRCLK_IN0/MP10", "bidirectional", 2),
    (62, "SDATA_IN1",      "input",         2),
    (60, "BCLK_IN1",       "bidirectional", 2),
    (61, "LRCLK_IN1/MP11", "bidirectional", 2),
    (67, "SDATA_IN2",      "input",         2),
    (65, "BCLK_IN2",       "bidirectional", 2),
    (66, "LRCLK_IN2/MP12", "bidirectional", 2),
    (70, "SDATA_IN3",      "input",         2),
    (68, "BCLK_IN3",       "bidirectional", 2),
    (69, "LRCLK_IN3/MP13", "bidirectional", 2),
    (41, "SDATA_OUT0",     "output",        2),
    (40, "BCLK_OUT0",      "bidirectional", 2),
    (39, "LRCLK_OUT0/MP4", "bidirectional", 2),
    (44, "SDATA_OUT1",     "output",        2),
    (43, "BCLK_OUT1",      "bidirectional", 2),
    (42, "LRCLK_OUT1/MP5", "bidirectional", 2),
    (49, "SDATA_OUT2",     "output",        2),
    (48, "BCLK_OUT2",      "bidirectional", 2),
    (47, "LRCLK_OUT2/MP8", "bidirectional", 2),
    (52, "SDATA_OUT3",     "output",        2),
    (51, "BCLK_OUT3",      "bidirectional", 2),
    (50, "LRCLK_OUT3/MP9", "bidirectional", 2),
    (45, "MP6",            "bidirectional", 2),
    (46, "MP7",            "bidirectional", 2),

    # ---- Unit 3: control, clock, aux, SPDIF, thermal ----
    (21, "XTALIN/MCLK",      "input",         3),
    (22, "XTALOUT",          "output",        3),
    (23, "CLKOUT",           "output",        3),
    (24, "~{RESET}",         "input",         3),
    (34, "SELFBOOT",         "input",         3),
    (33, "~{SS}/ADDR0",      "input",         3),
    (31, "SCLK/SCL",         "input",         3),
    (32, "MOSI/ADDR1",       "input",         3),
    (30, "MISO/SDA",         "bidirectional", 3),
    (26, "SS_M/MP0",         "bidirectional", 3),
    (27, "MOSI_M/MP1",       "bidirectional", 3),
    (28, "SCL_M/SCLK_M/MP2", "bidirectional", 3),
    (29, "SDA_M/MISO_M/MP3", "bidirectional", 3),
    (4,  "SPDIFIN",          "input",         3),
    (5,  "SPDIFOUT",         "output",        3),
    (63, "THD_M",            "passive",       3),
    (64, "THD_P",            "passive",       3),
    (8,  "AUXADC0", "input", 3), (9,  "AUXADC1", "input", 3),
    (10, "AUXADC2", "input", 3), (11, "AUXADC3", "input", 3),
    (12, "AUXADC4", "input", 3), (13, "AUXADC5", "input", 3),
]

# ---- assertions: the safety net that makes generation trustworthy ----
nums = [p[0] for p in PINS]
assert len(nums) == len(set(nums)), "duplicate pin number"
expected = set(range(1, 73)) | {"EP"}
assert set(nums) == expected, f"pin set mismatch: missing {expected - set(nums)}, extra {set(nums) - expected}"
assert len(PINS) == 73, f"expected 73 entries, got {len(PINS)}"
print(f"assertions OK: {len(PINS)} pins, 1..72 + EP, each exactly once")

UNIT_NAMES = {1: "Power", 2: "Serial Audio", 3: "Control"}

def esc(s):
    return s.replace('"', '\\"')

def unit_block(unit):
    pins = [p for p in PINS if p[3] == unit]
    half = (len(pins) + 1) // 2
    left, right = pins[:half], pins[half:]
    rows = max(len(left), len(right))
    h = (rows + 1) * 2.54
    w = 63.5
    top = h / 2
    out = []
    out.append(f'\t\t(symbol "ADAU1466_{unit}_0"')
    out.append(f'\t\t\t(rectangle (start {-w/2} {top}) (end {w/2} {-top})')
    out.append('\t\t\t\t(stroke (width 0.254) (type default))')
    out.append('\t\t\t\t(fill (type background))')
    out.append('\t\t\t)')
    out.append('\t\t)')
    out.append(f'\t\t(symbol "ADAU1466_{unit}_1"')
    for i, (num, name, etype, _) in enumerate(left):
        y = top - 2.54 * (i + 1)
        out.append(f'\t\t\t(pin {etype} line (at {-w/2 - 5.08} {y} 0) (length 5.08)')
        out.append(f'\t\t\t\t(name "{esc(name)}" (effects (font (size 1.27 1.27))))')
        out.append(f'\t\t\t\t(number "{num}" (effects (font (size 1.27 1.27))))')
        out.append('\t\t\t)')
    for i, (num, name, etype, _) in enumerate(right):
        y = top - 2.54 * (i + 1)
        out.append(f'\t\t\t(pin {etype} line (at {w/2 + 5.08} {y} 180) (length 5.08)')
        out.append(f'\t\t\t\t(name "{esc(name)}" (effects (font (size 1.27 1.27))))')
        out.append(f'\t\t\t\t(number "{num}" (effects (font (size 1.27 1.27))))')
        out.append('\t\t\t)')
    out.append('\t\t)')
    return "\n".join(out)

props = [
    ("Reference", "U", 0, 0),
    ("Value", "ADAU1466WBCPZ300", 0, -2.54),
    ("Footprint", "ODSP12:ADI_LFCSP-72_10x10mm_P0.5mm_EP5.3x5.3mm", 0, -5.08),
    ("Datasheet", "adau1462-1466.pdf Rev. C", 0, -7.62),
    ("Description", "SigmaDSP 32-bit audio processor, 72-LFCSP", 0, -10.16),
    ("MFR", "Analog Devices", 0, -12.7),
    ("MPN", "ADAU1466WBCPZ300", 0, -15.24),
]

lines = [
    "(kicad_symbol_lib",
    f'\t(version {VER})',
    '\t(generator "odsp12-symgen")',
    '\t(generator_version "10.0")',
    '\t(symbol "ADAU1466"',
    '\t\t(pin_names (offset 0.254))',
    '\t\t(exclude_from_sim no)',
    '\t\t(in_bom yes)',
    '\t\t(on_board yes)',
]
for i, (k, v, x, y) in enumerate(props):
    hide = "" if k in ("Reference", "Value") else "\n\t\t\t\t(hide yes)"
    lines.append(f'\t\t(property "{k}" "{esc(v)}"')
    lines.append(f'\t\t\t(at {x} {y} 0)')
    lines.append(f'\t\t\t(effects (font (size 1.27 1.27)){hide})')
    lines.append('\t\t)')
for u in (1, 2, 3):
    lines.append(unit_block(u))
lines.append('\t\t(embedded_fonts no)')
lines.append('\t)')
lines.append(")")

dest = r"c:\Users\nick\Documents\Claude Project\DSP Design\hw\lib\ODSP12.kicad_sym"
os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")
print("wrote", dest)
for u in (1, 2, 3):
    print(f"  unit {u} ({UNIT_NAMES[u]}): {len([p for p in PINS if p[3]==u])} pins")
