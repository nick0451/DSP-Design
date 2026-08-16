# Generates 01_power.kicad_sch -- ten rails, sequencing as nets, testpoints as one namespace.
#
# SCOPE OF THIS PASS: active devices, every pin dispositioned, sequencing/monitor nets, the
# PG->EN divider with its arithmetic, and a testpoint per rail. Passive networks (inductors,
# bulk/bypass caps, feedback dividers) are the NEXT pass -- same convention the DSP sheet
# follows. Feedback pins carry a named net rather than a no-connect so nothing is undispositioned.
import os, re, uuid

HW = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HW, "01_power.kicad_sch")
NS = uuid.UUID("0d5f1a00-0000-4000-8000-0000000000ff")
SHEET_UUID = str(uuid.uuid5(NS, "sheet:01_power.kicad_sch"))
SHEET_SYM_UUID = str(uuid.uuid5(NS, "inst:01_power.kicad_sch"))
ROOT_UUID = "0d5f1a00-0000-4000-8000-000000000001"
VER = "20260306"
GRID = 1.27
def snap(v): return round(v / GRID) * GRID
def u(t): return str(uuid.uuid5(NS, "pwr:" + t))

STOCK_DIR = r"C:/Program Files/KiCad/10.0/share/kicad/symbols"
PROJ_LIB = os.path.join(HW, "lib", "ODSP12.kicad_sym")

def extract(path, name):
    """Return (definition_text, [(pin_number, x, y, angle), ...]) for one symbol."""
    s = open(path, encoding="utf-8").read()
    m = re.search(r'\t\(symbol "' + re.escape(name) + r'"\n', s)
    if not m: raise KeyError(name)
    i = m.start(); d = 0
    for j in range(i, len(s)):
        if s[j] == "(": d += 1
        elif s[j] == ")":
            d -= 1
            if d == 0: break
    blk = s[i:j + 1]
    # Tolerate both layouts: KiCad's multi-line pin blocks and this project's compact
    # single-line form. The earlier regex required a newline the project generator never
    # emits, so it matched nothing -- and an EMPTY pin map made the F28 completeness
    # assertion pass vacuously. See the ledger: an assertion over an empty set is not a check.
    pins = []
    for m in re.finditer(r'\(pin\s+\w+\s+\w+[\s\S]{0,400}?\(number "([^"]+)"', blk):
        seg = m.group(0)
        at = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', seg)
        if at:
            pins.append((m.group(1), float(at.group(1)), float(at.group(2)), int(at.group(3))))
    assert pins, f"{name}: extracted ZERO pins -- regex/format mismatch, not an empty part"
    return blk, pins

# lib alias -> (file, symbol name in that file)
SRC = {
    "ODSP12:LM61460-Q1": (PROJ_LIB, "LM61460-Q1"),
    "ODSP12:LMK1C1104":  (PROJ_LIB, "LMK1C1104"),
    "Regulator_Switching:TPS62823DLC": (STOCK_DIR + "/Regulator_Switching.kicad_sym", "TPS62823DLC"),
    "Regulator_Linear:LT3045xDD":      (STOCK_DIR + "/Regulator_Linear.kicad_sym", "LT3045xDD"),
    "Analog_ADC:ADS1015IDGS":          (STOCK_DIR + "/Analog_ADC.kicad_sym", "ADS1015IDGS"),
    "Sensor_Temperature:TMP461xxRUN":  (STOCK_DIR + "/Sensor_Temperature.kicad_sym", "TMP461xxRUN"),
    "Device:R":                        (STOCK_DIR + "/Device.kicad_sym", "R"),
}
DEFS, PINGEO = {}, {}
for libid, (path, nm) in SRC.items():
    blk, pins = extract(path, nm)
    DEFS[libid] = blk.replace(f'(symbol "{nm}"', f'(symbol "{libid}"', 1)   # parent only
    PINGEO[libid] = {p[0]: (p[1], p[2]) for p in pins}

GND = "GND"
# ---- placements: (ref, lib_id, x, y, value, {pin: net}) ----
# LM61460-Q1 pins: 1 BIAS 2 VCC 3 AGND 4 FB 5 PGOOD 6 RT 7 EN/SYNC 8 VIN1 9 PGND1
#                  10 SW 11 PGND2 12 VIN2 13 RBOOT 14 CBOOT
def buck(ref, x, y, vin, vout, fbnet, pgnet, ennet, sw, rt):
    return (ref, "ODSP12:LM61460-Q1", x, y, "LM61460AQRJRRQ1", {
        "8": vin, "12": vin, "1": vout, "2": f"{ref}_VCC", "3": GND, "9": GND, "11": GND,
        "10": sw, "14": f"{ref}_CBOOT", "13": f"{ref}_CBOOT", "4": fbnet,
        "5": pgnet, "6": rt, "7": ennet})

# LT3045xDD actual map, read as name+number PAIRS from one regex match rather than two
# zipped lists (see ledger -- the zipped version silently permuted every name):
#   1 IN  2 IN  3 EN/UV  4 PG  5 ILIM  6 PGFB  7 SET  8 GND  9 OUTS  10 OUT  11 GND
def lt3045(ref, x, y, vin, vout, en=None):
    return (ref, "Regulator_Linear:LT3045xDD", x, y, "LT3045EDD", {
        "1": vin, "2": vin, "3": en or vin, "4": f"{ref}_PG", "5": f"{ref}_ILIM",
        "6": f"{ref}_PGFB", "7": f"{ref}_SET", "8": GND, "11": GND,
        "9": vout, "10": vout})

PLACE = [
    buck("U2", 40, 40, "VBATT_PROT", "+5V_D",  "FB_5V_D",  "PG_5V_D",  "VBATT_PROT", "SW_5V_D",  "RT_U2"),
    buck("U3", 40, 100, "VBATT_PROT", "+3V3_D", "FB_3V3_D", "PG_3V3_D", "VBATT_PROT", "SW_3V3_D", "RT_U3"),
    buck("U4", 40, 160, "VBATT_PROT", "+6V2_A", "FB_6V2_A", "PG_6V2_A", "VBATT_PROT", "SW_6V2_A", "RT_U4"),
    # +1V2_CORE: TPS62823 actual map -- 1 EN  2 FB  3 AGND  5 PGND  6 SW  7 VIN  8 PG
    ("U5", "Regulator_Switching:TPS62823DLC", 150, 40, "TPS62823DLC", {
        "7": "+3V3_D", "1": "+3V3_D", "2": "FB_1V2", "3": GND, "5": GND,
        "6": "SW_1V2", "8": "PG_1V2", "4": None}),
    lt3045("U6", 150, 100, "+6V2_A", "+5V_A"),
    lt3045("U7", 150, 160, "+6V2_A", "+3V3_A"),
    lt3045("U8", 260, 40,  "+6V2_A", "+3V3_CLK"),
    # +3V3_PLL -- F33/F34. EN gated from PG_3V3_D via the R2/R3/R4 network.
    lt3045("U9", 260, 100, "+6V2_A", "+3V3_PLL", en="EN_3V3_PLL"),
    # +3V6_BT -- F36: MIC5504 is fixed-voltage with no 3.6 V option, so an adjustable part
    # stands in provisionally. Flagged, not silently substituted.
    lt3045("U10", 260, 160, "+5V_D", "+3V6_BT"),
    # Rail monitor: ADS1015  1 ADDR 2 ALERT/RDY 3 GND 4 AIN0 5 AIN1 6 AIN2 7 AIN3 8 VDD 9 SDA 10 SCL
    ("U11", "Analog_ADC:ADS1015IDGS", 370, 40, "ADS1015IDGS", {
        "8": "+3V3_D", "3": GND, "1": GND, "9": "I2C0_SDA", "10": "I2C0_SCL",
        "2": "RAILMON_ALERT", "4": "MON_VBATT", "5": "MON_P13V5", "6": "MON_N13V5",
        "7": "MON_3V3_A"}),
    # TMP461  1 V+ 2 D+ 3 D- 4 THERM 5 A0 6 GND 7 ALERT/THERM2 8 SDA 9 SCL 10 A1
    ("U12", "Sensor_Temperature:TMP461xxRUN", 370, 120, "TMP461-Q1", {
        "1": "+3V3_D", "6": GND, "2": "DSP_THD_P", "3": "DSP_THD_M",
        "8": "I2C0_SDA", "9": "I2C0_SCL", "5": "+3V3_D", "10": GND,
        "4": "TEMP_THERM_N", "7": "TEMP_ALERT_N"}),
    # PG -> EN divider (F34). PGOOD is open-drain (T1-64): R2 pulls up, R3 holds EN low
    # when PG is high-Z or +3V3_D is absent.
    ("R2", "Device:R", 340, 200, "100k", {"1": "+3V3_D", "2": "EN_3V3_PLL"}),
    ("R3", "Device:R", 370, 200, "100k", {"1": "EN_3V3_PLL", "2": GND}),
]
# PG_3V3_D is the open-drain pull-down onto the same node
PLACE.append(("R4", "Device:R", 400, 200, "0R", {"1": "PG_3V3_D", "2": "EN_3V3_PLL"}))

TESTPOINTS = ["VBATT_PROT", "+5V_D", "+3V3_D", "+6V2_A", "+1V2_CORE", "+5V_A",
              "+3V3_A", "+3V3_CLK", "+3V3_PLL", "+3V6_BT"]

def place(ref, libid, x, y, val, nets):
    x, y = snap(x), snap(y)
    geo = PINGEO[libid]
    assert geo, f"{ref}: no pin geometry for {libid} -- would place a symbol with no connections"
    missing = set(geo) - set(nets)
    extra = set(nets) - set(geo)
    assert not missing, f"{ref}: pins with no disposition (F28): {sorted(missing)}"
    assert not extra, f"{ref}: nets assigned to non-existent pins {sorted(extra)} -- stale pin map"
    out = ['\t(symbol', f'\t\t(lib_id "{libid}")', f'\t\t(at {x} {y} 0)', '\t\t(unit 1)',
           '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)', '\t\t(dnp no)',
           f'\t\t(uuid "{u("i" + ref)}")',
           f'\t\t(property "Reference" "{ref}" (at {x} {y - 22} 0) (effects (font (size 1.27 1.27))))',
           f'\t\t(property "Value" "{val}" (at {x} {y - 19} 0) (effects (font (size 1.27 1.27))))',
           '\t\t(instances', '\t\t\t(project "ODSP12-MB"',
           f'\t\t\t\t(path "/{ROOT_UUID}/{SHEET_SYM_UUID}" (reference "{ref}") (unit 1))',
           '\t\t\t)', '\t\t)', '\t)']
    for num, (sx, sy) in geo.items():
        lx, ly = snap(x + sx), snap(y - sy)
        if nets[num] is None:                      # explicit no-connect, per F28
            out.append(f'\t(no_connect (at {lx} {ly}) (uuid "{u("nc" + ref + num)}"))')
            continue
        rot = 180 if sx < 0 else 0
        just = "right" if sx < 0 else "left"
        out += [f'\t(global_label "{nets[num]}"', '\t\t(shape bidirectional)',
                f'\t\t(at {lx} {ly} {rot})', '\t\t(fields_autoplaced yes)',
                f'\t\t(effects (font (size 1.27 1.27)) (justify {just}))',
                f'\t\t(uuid "{u("l" + ref + num)}")', '\t)']
    return "\n".join(out)

NOTE = (
    "PG->EN DIVIDER ARITHMETIC (F34) -- check before any BOM cost-pass normalises these values.\\n"
    "PGOOD on U3 is OPEN-DRAIN (T1-64). Three constraints on two resistors:\\n"
    "  1. PG released (+3V3_D up): EN_3V3_PLL = 3V3 * R3/(R2+R3) must exceed the LDO's V_IH.\\n"
    "  2. PG asserted low (fault): EN must sit below V_IL.\\n"
    "  3. +3V3_D absent / PG high-Z: R3 must dominate so EN defaults LOW -- fail-safe off.\\n"
    "Values above are PLACEHOLDERS. [VERIFY] the chosen LDO's EN threshold table, then solve.\\n"
    "Do not substitute standard values without re-checking all three inequalities."
)
NOTE2 = (
    "SCOPE: this pass places active devices, dispositions every pin, and defines the\\n"
    "sequencing and monitor nets. Inductors, bulk/bypass caps and feedback dividers are the\\n"
    "next pass -- FB/SW/CBOOT/SET/ILIM pins carry named nets, not no-connects, so nothing\\n"
    "is left undispositioned in the meantime (F28)."
)

body = [place(*p) for p in PLACE]
for i, r in enumerate(TESTPOINTS):
    x, y = snap(40 + (i % 5) * 60), snap(230 + (i // 5) * 12)
    body.append(f'\t(global_label "{r}"\n\t\t(shape bidirectional)\n\t\t(at {x} {y} 0)\n'
                f'\t\t(fields_autoplaced yes)\n'
                f'\t\t(effects (font (size 1.27 1.27)) (justify left))\n'
                f'\t\t(uuid "{u("tp" + r)}")\n\t)')
for i, (nx, ny, txt) in enumerate([(150.0, 200.0, NOTE), (150.0, 250.0, NOTE2)]):
    body.append(f'\t(text "{txt}"\n\t\t(exclude_from_sim no)\n\t\t(at {snap(nx)} {snap(ny)} 0)\n'
                f'\t\t(effects (font (size 1.27 1.27)) (justify left top))\n'
                f'\t\t(uuid "{u(f"n{i}")}")\n\t)')

sch = f'''(kicad_sch
\t(version {VER})
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{SHEET_UUID}")
\t(paper "A3")
\t(title_block
\t\t(title "ODSP-12 :: Power and Sequencing")
\t\t(date "2026-08-16")
\t\t(rev "A")
\t\t(comment 1 "ODSP12-MB-A")
\t\t(comment 2 "Ten rails. Sequencing as nets. Testpoint names match silk and BRINGUP.md.")
\t)
\t(lib_symbols
{chr(10).join(DEFS.values())}
\t)
{chr(10).join(body)}
\t(embedded_fonts no)
)
'''
open(DEST, "w", encoding="utf-8", newline="\n").write(sch)
print(f"wrote {DEST}")
print(f"  {len(PLACE)} devices placed, all pins dispositioned")
print(f"  {len(TESTPOINTS)} rail testpoints")
