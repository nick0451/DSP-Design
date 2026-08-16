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
    "ODSP12:LM5156-Q1":  (PROJ_LIB, "LM5156-Q1"),
    "ODSP12:LMK1C1104":  (PROJ_LIB, "LMK1C1104"),
    "ODSP12:LT3094":     (PROJ_LIB, "LT3094"),
    "Transistor_FET:Q_NMOS_DGS":       (STOCK_DIR + "/Transistor_FET.kicad_sym", "Q_NMOS_DGS"),
    "Transistor_FET:Q_PMOS_DGS":       (STOCK_DIR + "/Transistor_FET.kicad_sym", "Q_PMOS_DGS"),
    "Device:Fuse":                     (STOCK_DIR + "/Device.kicad_sym", "Fuse"),
    "Device:D_TVS":                    (STOCK_DIR + "/Device.kicad_sym", "D_TVS"),
    "Device:D_Zener":                  (STOCK_DIR + "/Device.kicad_sym", "D_Zener"),
    "Device:D_Schottky":               (STOCK_DIR + "/Device.kicad_sym", "D_Schottky"),
    "Device:L_Coupled":                (STOCK_DIR + "/Device.kicad_sym", "L_Coupled"),
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
        "10": sw, "14": f"{ref}_CBOOT", "13": f"{ref}_RBOOT", "4": fbnet,
        "5": pgnet, "6": rt, "7": ennet})

# LT3045xDD actual map, read as name+number PAIRS from one regex match rather than two
# zipped lists (see ledger -- the zipped version silently permuted every name):
#   1 IN  2 IN  3 EN/UV  4 PG  5 ILIM  6 PGFB  7 SET  8 GND  9 OUTS  10 OUT  11 GND
def lt3045(ref, x, y, vin, vout, en=None, pg=None, pgfb=None):
    # ILIM (5) -> GND, the datasheet's own "not needed" disposition. See F40: this pin was
    # previously carrying a 20k placeholder, and the scale factor is 150mA*kOhm / R_ILIM, so
    # 20k programmed a 7.5 mA limit on rails that must deliver 15-200 mA. The datasheet gives
    # the worked example directly -- "a 1k resistor programs 150mA". Tied to GND the pin can
    # never reach its 300 mV threshold and the internal limit governs, which is what we want
    # while V-17 (AKM AVDD currents) is still open: do not program a limit against an unknown load.
    return (ref, "Regulator_Linear:LT3045xDD", x, y, "LT3045EDD", {
        # PGFB (6) -> OUT is the datasheet's own disposition when fast start-up is unused
        # ("tie PGFB to IN or to OUT for output voltages above 300mV"), and it explicitly
        # DISABLES power good. The five housekeeping LDOs take that; U15 gets a real divider
        # because F39 asked for +/-13V5_A to have a sequencing hook it did not have before.
        "1": vin, "2": vin, "3": en or vin, "4": pg or f"{ref}_PG", "5": GND,
        "6": pgfb or vout, "7": f"{ref}_SET", "8": GND, "11": GND,
        "9": vout, "10": vout})

# LT3094 pin map -- ADI Rev. B p.15, verified. NOT a mirror of the LT3045 beside it:
#   1,2 IN  3 EN/UV  4 PG  5 PGFB  6 ILIM  7 VIOC  8 SET  9 GND  10 OUTS  11,12 OUT  EP=IN
def lt3094(ref, x, y, vin, vout, en, pgfb, pg):
    return (ref, "ODSP12:LT3094", x, y, "LT3094EDD", {
        "1": vin, "2": vin, "EP": vin,          # EP IS IN. Not a typo, not a copy of the LT3045.
        "3": en, "4": pg, "5": pgfb, "6": GND,  # ILIM -> GND, same reasoning as F40 above
        "7": None,                              # VIOC unused -> datasheet says FLOAT it (F28)
        "8": f"{ref}_SET", "9": GND, "10": vout, "11": vout, "12": vout})

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
    # ---------------- F39: the +/-13V5_A block ----------------
    # SEPIC -> +15V5_A.  LM5156-Q1 pin map: 1 BIAS 2 VCC 3 GATE 4 GND 5 CS 6 COMP
    #                    7 DITHOFF 8 FB 9 SS 10 RT 11 PGOOD 12 UVLO/SYNC/EN  EP=GND
    # DITHOFF is driven through a stuffing pair, not strapped: V-26 decree is dither OFF.
    ("U13", "ODSP12:LM5156-Q1", 40, 560, "LM5156QDSSRQ1", {
        "1": "VBATT_PROT", "2": "U13_VCC", "3": "U13_GATE", "4": GND, "EP": GND,
        "5": "U13_CS", "6": "U13_COMP", "7": "DITHOFF_U13", "8": "FB_15V5_A",
        "9": "U13_SS", "10": "RT_U13", "11": "PG_15V5_A", "12": "UVLO_U13"}),
    # Inverting buck-boost -> -15V5_A, per SNVA856: a BUCK with its ground pin tied to the
    # negative rail. Every "GND" pin below is therefore -15V5_A, and the part's regulated
    # output node is SYSTEM ground. This is the whole trick; misreading it inverts the block.
    ("U14", "ODSP12:LM61460-Q1", 150, 560, "LM61460AQRJRRQ1", {
        "8": "+15V5_A", "12": "+15V5_A",
        "3": "-15V5_A", "9": "-15V5_A", "11": "-15V5_A",
        "1": "-15V5_A",          # BIAS: datasheet -- "if output voltage is above 12 V,
                                 # connect this pin to ground." Ours is 15.4 V. Also keeps
                                 # BIAS off a node 0.6 V from its 16 V abs max.
        "2": "U14_VCC", "10": "SW_N15V5", "14": "U14_CBOOT", "13": "U14_RBOOT",
        "4": "FB_N15V5_A", "6": "RT_U14", "7": "EN_N15V5",
        "5": None}),             # PGOOD referenced to -15V5_A: a +3V3_D pull-up would sit
                                 # 18.8 V above the pin's own ground against a 20 V abs max.
                                 # The negative rail's power-good comes from U16 instead,
                                 # which is system-referenced and needs no level shifter.
    lt3045("U15", 260, 560, "+15V5_A", "+13V5_A", en="EN_13V5P", pg="PG_13V5P",
           pgfb="PGFB_13V5P"),
    lt3094("U16", 370, 560, "-15V5_A", "-13V5_A", en="EN_13V5N",
           pgfb="PGFB_13V5N", pg="PG_13V5N"),
]
# PG_3V3_D is the open-drain pull-down onto the same node
PLACE.append(("R4", "Device:R", 400, 200, "0R", {"1": "PG_3V3_D", "2": "EN_3V3_PLL"}))

TESTPOINTS = ["VBATT_PROT", "+5V_D", "+3V3_D", "+6V2_A", "+1V2_CORE", "+5V_A",
              "+3V3_A", "+3V3_CLK", "+3V3_PLL", "+3V6_BT",
              "+15V5_A", "-15V5_A", "+13V5_A", "-13V5_A"]

# ---------------------------------------------------------------- passive pass
# Reference voltages read from datasheets, not assumed (M2):
#   LM61460-Q1  VREF = 1.0 V   -> Vout = 1.0 * (1 + Rt/Rb)      [SNVSB70F]
#   LT3045      ISET = 100 uA  -> Vout = 100uA * Rset, +/-1%    [LT3045 Rev D]
#   TPS62823    VREF = ?       -> V-24, datasheet not in archive
#   AP2127K-ADJ VFB  = ?       -> V-23, datasheet not in archive
LM_VREF = 1.0
SRC["Device:C"] = (STOCK_DIR + "/Device.kicad_sym", "C")
SRC["Device:L"] = (STOCK_DIR + "/Device.kicad_sym", "L")
for _lid in ("Device:C", "Device:L"):
    _b, _p = extract(*SRC[_lid])
    DEFS[_lid] = _b.replace(f'(symbol "{_lid.split(":")[1]}"', f'(symbol "{_lid}"', 1)
    PINGEO[_lid] = {q[0]: (q[1], q[2]) for q in _p}

E96 = [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150,
       154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232,
       237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309, 316, 324, 332, 340, 348, 357,
       365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549,
       562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732, 750, 768, 787, 806, 825, 845,
       866, 887, 909, 931, 953, 976]

def e96(target_ohms):
    """Nearest E96 value, returned as (ohms, printable)."""
    import math
    best = None
    for dec in range(-1, 7):
        for m in E96:
            v = m * (10 ** dec) / 10.0
            if best is None or abs(math.log(v / target_ohms)) < abs(math.log(best / target_ohms)):
                best = v
    if best >= 1e6:   txt = f"{best/1e6:g}M"
    elif best >= 1e3: txt = f"{best/1e3:g}k"
    else:             txt = f"{best:g}R"
    return best, txt

def lm_divider(vout):
    """Top/bottom for Vout = VREF*(1+Rt/Rb). Rb anchored near 10k for noise/leakage balance."""
    rb, rb_txt = e96(10000.0)
    rt, rt_txt = e96(rb * (vout / LM_VREF - 1.0))
    return (rt, rt_txt), (rb, rb_txt), LM_VREF * (1 + rt / rb)

def lt_set(vout):
    r, txt = e96(vout / 100e-6)
    return (r, txt), r * 100e-6

_pcount = [0]
def passive(kind, x, y, val, na, nb):
    _pcount[0] += 1
    ref = {"C": "C", "L": "L", "R": "R"}[kind] + str(100 + _pcount[0])
    libid = {"C": "Device:C", "L": "Device:L", "R": "Device:R"}[kind]
    return (ref, libid, x, y, val, {"1": na, "2": nb})

PASSIVES = []
# --- three LM61460 bucks: L, Cin, Cout, boot network, RT, VCC/BIAS bypass, FB divider ---
for ref, vout, vin, bx, by in (("U2", 5.0, "VBATT_PROT", 40, 250),
                               ("U3", 3.3, "VBATT_PROT", 40, 290),
                               ("U4", 6.2, "VBATT_PROT", 40, 330)):
    rail = {"U2": "+5V_D", "U3": "+3V3_D", "U4": "+6V2_A"}[ref]
    (rt, rt_t), (rb, rb_t), vact = lm_divider(vout)
    PASSIVES += [
        passive("L", bx,      by, "10uH",  f"SW_{rail[1:]}" if False else f"SW_{rail.strip('+')}", rail),
        passive("C", bx + 20, by, "10uF",  vin, GND),
        passive("C", bx + 40, by, "22uF",  rail, GND),
        passive("C", bx + 60, by, "100nF", f"SW_{rail.strip('+')}", f"{ref}_CBOOT"),
        passive("R", bx + 80, by, "0R",    f"{ref}_CBOOT", f"{ref}_RBOOT"),
        passive("R", bx + 100, by, "5.76k", f"RT_{ref}", GND),   # 2.2 MHz typ -- DATASHEET POINT, see note
        passive("C", bx + 120, by, "1uF",  f"{ref}_VCC", GND),
        passive("R", bx + 140, by, rt_t,   rail, f"FB_{rail.strip('+')}"),
        passive("R", bx + 160, by, rb_t,   f"FB_{rail.strip('+')}", GND),
    ]
# --- TPS62823: L, Cin, Cout; FB divider deferred to V-24 ---
PASSIVES += [
    passive("L", 40, 370, "1uH",   "SW_1V2", "+1V2_CORE"),
    passive("C", 60, 370, "10uF",  "+3V3_D", GND),
    passive("C", 80, 370, "22uF",  "+1V2_CORE", GND),
    passive("R", 100, 370, "100k", "+1V2_CORE", "FB_1V2"),   # VFB=0.6V (V-24): Rt=Rb -> 1.2 V
    passive("R", 120, 370, "100k", "FB_1V2", GND),
]
# --- five LT3045: Cin, Cout, Rset, Cset, Rilim ---
for ref, vout, vin, rail, py in (("U6", 5.0, "+6V2_A", "+5V_A", 410),
                                 ("U7", 3.3, "+6V2_A", "+3V3_A", 430),
                                 ("U8", 3.3, "+6V2_A", "+3V3_CLK", 450),
                                 ("U9", 3.3, "+6V2_A", "+3V3_PLL", 470),
                                 ("U10", 3.6, "+5V_D", "+3V6_BT", 490)):
    (rs, rs_t), vact = lt_set(vout)
    PASSIVES += [
        passive("C", 40,  py, "10uF",  vin, GND),
        passive("C", 60,  py, "22uF",  rail, GND),
        passive("R", 80,  py, rs_t,    f"{ref}_SET", GND),
        passive("C", 100, py, "4.7uF", f"{ref}_SET", GND),
        # (F40) the 20k ILIM resistor that used to sit here is GONE, not re-valued.
        # ILIM now ties straight to GND at the symbol. See the lt3045() comment.
    ]

# ---------------------------------------------------------------- F39: +/-13V5_A block
# Divider maths uses the SAME helper and the SAME reference as the bucks above: the
# LM5156-Q1's FB reference is 1.000 V +/-1% (T1-75), identical to the LM61460's, so the
# SEPIC and the IBB take an identical divider. One value pair, drawn twice.
(RT15, RT15_T), (RB15, RB15_T), V15 = lm_divider(15.5)
# LDO setpoints: Vout = 100 uA * RSET on BOTH parts (same SET architecture, +/-1% on ISET).
# 13.5 V / 100 uA = 135 kOhm exactly -- and 135k IS NOT AN E96 VALUE (E96 goes 133, 137).
# It exists in E192, so it is specified as 135k 0.1%. The 0.1% buys the VALUE, not accuracy:
# ISET's own +/-1% dominates the stack either way. A cost pass that "normalises" this to 1%
# will find the value does not exist -- which is why the reason is written on the sheet.
RSET_135K = "135k 0.1%"
PASSIVES += [
    # --- SEPIC power stage (U13). Vin -> L1a -> A; Q1 A->CS; Rs CS->GND;
    #     Cs A->B; L1b B->GND; D1 B->+15V5_A.  L1a/L1b are ONE coupled part.
    passive("C", 40,  600, "10uF/50V",  "VBATT_PROT", GND),
    ("Q1", "Transistor_FET:Q_NMOS_DGS", 100, 600, "80V N-FET (F38)",
        {"1": "SEPIC_A", "2": "U13_GATE", "3": "U13_CS"}),
    passive("R", 130, 600, "25m",       "U13_CS", GND),        # Rs: 100 mV / 25 m = 4 A peak limit
    passive("C", 160, 600, "4.7uF/50V", "SEPIC_A", "SEPIC_B"), # Cs -- carries full ripple RMS
    ("D1", "Device:D_Schottky", 190, 600, "60V 3A Schottky (F38)",
        {"1": "SEPIC_B", "2": "+15V5_A"}),
    passive("C", 220, 600, "22uF/25V",  "+15V5_A", GND),
    passive("R", 250, 600, "9.09k",     "RT_U13", GND),        # 2200 kHz typ, T1-75 datasheet point
    passive("C", 280, 600, "1uF",       "U13_VCC", GND),
    passive("C", 310, 600, "22nF",      "U13_SS", GND),
    passive("R", 340, 600, RT15_T,      "+15V5_A", "FB_15V5_A"),
    passive("R", 370, 600, RB15_T,      "FB_15V5_A", GND),
    passive("R", 400, 600, "100k",      "PG_15V5_A", "+3V3_D"),  # PGOOD is open-drain
    # DITHOFF stuffing pair (V-26 decree): populated leg to VCC = dither OFF.
    passive("R", 430, 600, "10k",       "DITHOFF_U13", "U13_VCC"),
    passive("R", 460, 600, "10k DNP",   "DITHOFF_U13", GND),
    # UVLO divider on VBATT_PROT: sets the SEPIC's start threshold (12 V system).
    passive("R", 490, 600, "100k",      "VBATT_PROT", "UVLO_U13"),
    passive("R", 520, 600, "13.7k",     "UVLO_U13", GND),
    # --- IBB (U14). Note the caps that span the FULL 31 V, not 15.5 V. ---
    passive("C", 40,  640, "10uF/50V",  "+15V5_A", "-15V5_A"),   # Cin spans Vin to IC ground
    passive("C", 70,  640, "22uF/50V",  GND, "-15V5_A"),         # Cout: system GND to -15V5_A
    passive("C", 100, 640, "100nF",     "SW_N15V5", "U14_CBOOT"),
    passive("R", 130, 640, "0R",        "U14_CBOOT", "U14_RBOOT"),
    passive("R", 160, 640, "5.76k",     "RT_U14", "-15V5_A"),    # 2.2 MHz, V-25 analysis carries over
    passive("C", 190, 640, "1uF",       "U14_VCC", "-15V5_A"),
    passive("R", 220, 640, RT15_T,      GND, "FB_N15V5_A"),      # "output" node IS system ground
    passive("R", 250, 640, RB15_T,      "FB_N15V5_A", "-15V5_A"),
    passive("R", 280, 640, "100k",      "+15V5_A", "EN_N15V5"),  # self-enable from its own input
    passive("R", 310, 640, "13.7k",     "EN_N15V5", "-15V5_A"),
    # --- post-regulators ---
    passive("C", 40,  680, "10uF/25V",  "+15V5_A", GND),
    passive("C", 70,  680, "22uF/25V",  "+13V5_A", GND),
    passive("R", 100, 680, RSET_135K,   "U15_SET", GND),
    passive("C", 130, 680, "4.7uF",     "U15_SET", GND),         # 0.8 uVrms needs C_SET = 4.7 uF
    passive("R", 160, 680, "107k",      "+15V5_A", "EN_13V5P"),
    passive("R", 190, 680, "10k",       "EN_13V5P", GND),
    passive("R", 220, 680, "100k",      "PG_13V5P", "+3V3_D"),
    passive("C", 40,  720, "10uF/25V",  "-15V5_A", GND),
    passive("C", 70,  720, "22uF/25V",  "-13V5_A", GND),
    passive("R", 100, 720, RSET_135K,   "U16_SET", GND),
    passive("C", 130, 720, "4.7uF",     "U16_SET", GND),
    passive("R", 160, 720, "105k",      "-15V5_A", "EN_13V5N"),  # EN/UV is bidirectional: turns
    passive("R", 190, 720, "10k",       "EN_13V5N", GND),        # on at 1.26 V BELOW ground
    passive("R", 220, 720, "392k",      "-13V5_A", "PGFB_13V5N"),
    passive("R", 250, 720, "10k",       "PGFB_13V5N", GND),
    passive("R", 280, 720, "100k",      "PG_13V5N", "+3V3_D"),
    passive("R", 310, 720, "412k",      "+13V5_A", "PGFB_13V5P"),
    passive("R", 340, 720, "10k",       "PGFB_13V5P", GND),
]
# ---------------------------------------------------------------- VBATT_PROT front end
# Order, connector outward to board inward:
#   VBATT_IN -> F1 fuse -> D2 TVS (to GND) -> Q2 reverse P-FET -> L2 + C damped -> VBATT_PROT
#
# Q2 orientation is NOT arbitrary and is the half people get wrong: DRAIN to the battery,
# SOURCE to the load. A P-channel's body diode runs drain->source, so this way it is forward
# in normal flow and BLOCKS on reverse battery. Wired the other way round (source to battery)
# the part still works forwards -- and in reverse the body diode conducts happily from the
# load side back to the battery, which is the entire failure the FET was fitted to prevent.
PASSIVES += [
    ("F1", "Device:Fuse", 40, 780, "5A", {"1": "VBATT_IN", "2": "VBATT_FUSED"}),
    # D2 is drawn with the ZENER symbol (K/A), NOT Device:D_TVS. That symbol's pins are named
    # A1/A2 -- it models a BIDIRECTIONAL TVS, and the SMBJ24A is unidirectional ('A' suffix;
    # 'CA' is the bidirectional member). A polarity-blind symbol on a polarity-critical part
    # gives assembly a coin-flip, and a unidirectional TVS fitted backwards across a 12 V
    # battery is a DEAD SHORT, not a degraded clamp. K to the battery, A to GND.
    ("D2", "Device:D_Zener", 80, 780, "SMBJ24A uni (see F42)", {"1": "VBATT_FUSED", "2": GND}),
    ("Q2", "Transistor_FET:Q_PMOS_DGS", 120, 780, "60V P-FET (F38)",
        {"1": "VBATT_FUSED", "2": "VBATT_GATE", "3": "VBATT_REV"}),
    ("D3", "Device:D_Zener", 160, 780, "15V", {"1": "VBATT_GATE", "2": "VBATT_REV"}),
    passive("R", 200, 780, "100k",   "VBATT_GATE", GND),
    passive("L", 240, 780, "4.7uH 5A PROVISIONAL", "VBATT_REV", "VBATT_PROT"),
    passive("C", 280, 780, "22uF/50V", "VBATT_PROT", GND),
    # Damping branch -- NOT optional, and not a bulk cap. See NOTE6.
    passive("R", 320, 780, "0.68R",  "VBATT_PROT", "VBATT_DAMP"),
    passive("C", 360, 780, "47uF/50V", "VBATT_DAMP", GND),
]

# The SEPIC's coupled inductor: ONE part, two windings. Placed as a single L_Coupled so the
# BOM cannot count it twice and so the coupling is visible on the sheet rather than implied
# by two adjacent inductors that happen to share a value.
PLACE.append(("L1", "Device:L_Coupled", 70, 600, "10uH coupled, Isat >= 4A (F38)",
              {"1": "VBATT_PROT", "2": "SEPIC_A", "3": "SEPIC_B", "4": GND}))
# IBB inductor: SW to SYSTEM ground, because system ground is this converter's output node.
PASSIVES.append(passive("L", 340, 640, "10uH PROVISIONAL", "SW_N15V5", GND))
PLACE += PASSIVES

# Every global label this sheet emits, keyed by (x, y). Connectivity here is BY LABEL at a
# pin endpoint, so two labels sharing a coordinate is a short -- and a silent one: it passes
# the F28 pin-coverage assertions, passes the symbol assertions, and only shows up if someone
# reads the netlist. It happened: growing TESTPOINTS from 10 to 14 pushed a third row onto the
# U2 passive row and shorted +5V_D/+15V5_A, GND/+13V5_A and U2_CBOOT/-15V5_A at once.
# A completeness check sees omission, never collision (M6) -- so this is the collision check.
LABELS = {}
def emit_label(net, lx, ly, rot, just, uid):
    prev = LABELS.get((lx, ly))
    assert prev is None or prev == net, (
        f"LABEL COLLISION at ({lx}, {ly}): '{prev}' and '{net}' would be shorted. "
        f"Two nets cannot share a coordinate on a label-connected sheet.")
    LABELS[(lx, ly)] = net
    return [f'\t(global_label "{net}"', '\t\t(shape bidirectional)',
            f'\t\t(at {lx} {ly} {rot})', '\t\t(fields_autoplaced yes)',
            f'\t\t(effects (font (size 1.27 1.27)) (justify {just}))',
            f'\t\t(uuid "{uid}")', '\t)']

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
        out += emit_label(nets[num], lx, ly, rot, just, u("l" + ref + num))
    return "\n".join(out)

NOTE = (
    "PG->EN DIVIDER ARITHMETIC (F34) -- check before any BOM cost-pass normalises these values.\\n"
    "PGOOD on U3 is OPEN-DRAIN (T1-64). Three constraints on two resistors:\\n"
    "  1. PG released (+3V3_D up): EN_3V3_PLL = 3V3 * R3/(R2+R3) must exceed the LDO's V_IH.\\n"
    "  2. PG asserted low (fault): EN must sit below V_IL.\\n"
    "  3. +3V3_D absent / PG high-Z: R3 must dominate so EN defaults LOW -- fail-safe off.\\n"
    "Values above are PLACEHOLDERS. [VERIFY] the chosen LDO's EN threshold table, then solve.\\n"
    "Do not substitute standard values without re-checking all three inequalities.\n"
    "\n"
    "FB DIVIDER TOLERANCE NOTE -- the Err figures in STATE.md are E96-SNAP ONLY. The full\n"
    "stack is snap + resistor tol (both legs) + reference tol. All rails here have wide\n"
    "windows and clear comfortably; a future tight-window rail reusing this format does not\n"
    "inherit that luck.\n"
    "+1V2_CORE is the highest-impedance divider on the board: 100k/100k, R_thev = 50k, and\n"
    "TPS62823 FB leakage is 10 nA typ / 50 nA max -> 50k * 50nA = 2.5 mV worst case against a\n"
    "1.2 V rail with +/-5% window (60 mV). Leakage * R_thev << window, by ~24x. Term shown\n"
    "because the convention is to make the whole inequality visible, not only the tight ones."
)
NOTE2 = (
    "SCOPE: this pass places active devices, dispositions every pin, and defines the\\n"
    "sequencing and monitor nets. Inductors, bulk/bypass caps and feedback dividers are the\\n"
    "next pass -- FB/SW/CBOOT/SET/ILIM pins carry named nets, not no-connects, so nothing\\n"
    "is left undispositioned in the meantime (F28)."
)

NOTE3 = (
    "+/-13V5_A BLOCK (F39, decreed 2026-08-16). Read this before changing any value here.\\n"
    "\\n"
    "WHY THE CASCADE IS FORCED, not preferred:\\n"
    "  An inverting buck-boost stresses its regulator at VIN + |VOUT| (SNVA856 s4.1). On\\n"
    "  VBATT_PROT that is >= 26.7 + 15.5 = 42.2 V the instant the TVS conducts at all,\\n"
    "  against the LM61460-Q1's 42 V ABSOLUTE MAX. True for ANY 12 V-system TVS, because a\\n"
    "  standoff above 24 V breaks down above 26.5 V. Fed from +15V5_A it sees a fixed 31 V.\\n"
    "  DO NOT 'simplify' U14 by moving its input to the battery.\\n"
    "  A plain boost on the positive rail is excluded for the mirror reason: TI states that\\n"
    "  boost converters pass the input straight through the high-side diode when VOUT <= VIN\\n"
    "  (SNVSBI7B s9.3.8), which would put a clamped load dump on a 20 V LDO input.\\n"
    "\\n"
    "WHY f_sw = 2.2 MHz on BOTH stages -- three independent legs:\\n"
    "  1. LT3045 PSRR has a NOTCH at 500 kHz-1 MHz and RECOVERS by 2 MHz: at 2 V headroom\\n"
    "     it reads 77 / 72 / 70 / 84 dB at 100k / 500k / 1M / 2M (Rev. D curve G45).\\n"
    "     The part is BETTER at 2.2 MHz than at half that. This is why LM5175-Q1 (4-switch\\n"
    "     buck-boost, nicer magnetics) was rejected -- it tops out at 600 kHz, in the notch.\\n"
    "  2. LM5156-Q1 dither triangle runs at 0.156 x f_sw = 343 kHz. At a 100 kHz f_sw it\\n"
    "     would land at 15.6 kHz -- INSIDE the audio band.\\n"
    "  3. Nothing below the fundamental, so no harmonic falls in the AM band. A 440 kHz\\n"
    "     choice would put its 2nd and 3rd harmonics squarely in it.\\n"
    "\\n"
    "NOISE BUDGET vs the [HARD] 50 uVrms, 20 Hz-20 kHz. The two rails are NOT symmetric:\\n"
    "  LT3094's PSRR curve is its own (G47), not the LT3045's. At 2 V headroom it reads\\n"
    "  76 / 66 / 72 / 72 dB -- it PEAKS at 100 kHz, where the LT3045 peaks at 2 MHz, and it\\n"
    "  DECLINES as headroom grows past ~2 V, which is the opposite behaviour. So:\\n"
    "     +13V5_A : 0.8 (LDO) + 1.8 (50 mVpp ripple thru 80 dB) + 0.35 -> RSS 2.0 uVrms\\n"
    "     -13V5_A : 0.8 (LDO) + 4.4 (50 mVpp ripple thru 72 dB) + 0.20 -> RSS 4.5 uVrms\\n"
    "  Margin 28 dB and 21 dB. The budget is carried by the LDOs' AUDIO-BAND PSRR\\n"
    "  (LT3045 110 dB / LT3094 >=93 dB at 20 kHz), NOT by f_sw -- which is why V-27's\\n"
    "  unspecified pulse-skip onset cannot break it. Headroom target 1.9-2.0 V is a PSRR\\n"
    "  specification, NOT a dropout one: dropout is 260 mV (LT3045) / 235 mV (LT3094).\\n"
    "\\n"
    "RSET = 135k ON BOTH RAILS: 13.5 V / 100 uA. 135k IS NOT AN E96 VALUE -- E96 runs\\n"
    "  133, 137. It is E192, hence 0.1%. The 0.1% buys the VALUE, not the accuracy; ISET's\\n"
    "  own +/-1% dominates. Normalising this to 'a 1% part' finds no such part exists.\\n"
    "\\n"
    "U16 EXPOSED PAD IS **IN**, NOT GND. U15 beside it has EP = GND. Same vendor, adjacent\\n"
    "  part numbers, sold as a matched +/- pair, same SET architecture -- and DIFFERENT lead\\n"
    "  counts with OPPOSITE pad nets (LT3045 DD = DFN-10, EP=GND; LT3094 DD = DFN-12, EP=IN).\\n"
    "  Mirroring the positive channel to lay out the negative one shorts IN to GND.\\n"
    "\\n"
    "U14 IS A BUCK WIRED AS AN INVERTER (SNVA856). Its GND pins sit at -15V5_A and its\\n"
    "  regulated output node is SYSTEM GROUND. Its input caps therefore span the full 31 V,\\n"
    "  not 15.5 V -- 50 V parts, and the DC-bias derating trap applies with force here.\\n"
    "  BIAS -> -15V5_A is the datasheet's instruction for outputs above 12 V, not a shortcut."
)
NOTE4 = (
    "F40 -- CORRECTION APPLIED THIS PASS, recorded because the value looked plausible.\\n"
    "Every LT3045 on this sheet carried R_ILIM = 20k. The LT3045 scale factor is\\n"
    "150mA*kOhm / R_ILIM, and the datasheet gives the worked example outright: '1k programs\\n"
    "150 mA'. So 20k programmed a 7.5 mA CURRENT LIMIT on rails budgeted 15-200 mA --\\n"
    "including +3V6_BT feeding a radio at ~100 mA. All five would have current-limited.\\n"
    "ILIM now ties to GND, which is the datasheet's own disposition when the programmable\\n"
    "limit is unused, and leaves the internal limit governing. Deliberately NOT programmed:\\n"
    "V-17 (AKM AVDD currents) is still open, and a limit set against an unknown load is the\\n"
    "same mistake with a better-looking number.\\n"
    "\\n"
    "STILL PROVISIONAL ON THIS SHEET -- inductor values. The 10uH figures are placeholders\\n"
    "from the first pass, not derivations; at 2.2 MHz a 5 V/6 A buck wants ~1-2.2 uH. They\\n"
    "are marked PROVISIONAL and belong to the queued saturation-current pass, which must set\\n"
    "them from ripple AND from Isat at low line -- not from RMS heating."
)

NOTE5 = (
    "HEADROOM ON +/-15V5_A IS A JOINT OPTIMUM SERVING TWO CURVES WITH OPPOSITE SLOPES.\\n"
    "Do not re-tune the intermediates as if this were a free parameter.\\n"
    "  LT3045  (+13V5_A): PSRR COLLAPSES below ~1 V headroom -- 84 dB at 2 V, 62 dB at 1 V,\\n"
    "                     off a cliff below that. It wants MORE headroom.\\n"
    "  LT3094  (-13V5_A): PSRR PLATEAUS at ~1.5 V and then DECLINES as headroom grows --\\n"
    "                     73 dB at 1.5 V, 72 dB at 2.0 V, 70.5 at 2.5 V, 68 at 4 V.\\n"
    "                     It wants LESS headroom.\\n"
    "~1.9-2.0 V is where both are near their best. MOVING IT HELPS ONE REGULATOR AND HURTS\\n"
    "THE OTHER, in opposite directions, which is not a trade anyone re-derives by accident.\\n"
    "Raising it also costs dissipation on both (2 V x 250 mA = 500 mW each). Sources:\\n"
    "LT3045 Rev. D curve G45, LT3094 Rev. B curve G47 -- read independently, not inherited."
)
NOTE6 = (
    "VBATT_PROT FRONT END -- the five claims, written out so they can be checked, not re-derived.\\n"
    "\\n"
    "1. FUSE. F1 = 5 A, BOARD-MOUNTED. Board draw ~20 W; at 9 V crank that is 2.2 A, so 5 A\\n"
    "   carries >2x margin without nuisance-blowing on inrush. ADDITIONAL REQUIREMENT ON THE\\n"
    "   INSTALL, and it belongs in the manual, not in someone's head: upstream harness fuse\\n"
    "   <= 15 A, for selectivity -- ours must clear first. An assumed fuse is an unstated\\n"
    "   requirement wearing someone else's part.\\n"
    "\\n"
    "2. TVS ARITHMETIC -- AND IT DOES NOT CLOSE. SEE F42, THIS IS AN ESCALATION.\\n"
    "   SMBJ24A: standoff 24 V, breakdown 26.7-29.5 V, clamp 38.9 V @ 15.4 A, 600 W/10-1000us.\\n"
    "   STANDOFF AXIS -- fine. 24 V clears 16 V max operating and a 24 V jump start; that is\\n"
    "     evidently what the 24 V choice was sized for.\\n"
    "   ENERGY AXIS -- FAILS. A suppressed load dump (ISO 16750-2, Us* = 35 V, td = 400 ms,\\n"
    "     Ri = 0.5-4 ohm) sits ABOVE the 26.7 V breakdown, so the TVS conducts for the whole\\n"
    "     400 ms. At Ri = 2 ohm holding ~31 V: I = (35-31)/2 = 2 A, P = 62 W, E = 24.8 J.\\n"
    "     At Ri = 0.5 ohm: I = 8 A, P = 250 W, E = 100 J. Against 600 W for 1 ms = 0.6 J,\\n"
    "     that is 40x to 165x over. THE PART IS DESTROYED, and the fuse clears afterwards.\\n"
    "   So the design as drawn implicitly claims 'no load dump reaches this input'. That is\\n"
    "   a SCOPE STATEMENT and it has not been made. Ladder in F42; footprint is DO-214AB (SMC)\\n"
    "   so the more capable part stuffs without a respin.\\n"
    "\\n"
    "3. REVERSE STRATEGY -- SERIES FET, SEAMLESS, not a crowbar. Q2 blocks; nothing conducts;\\n"
    "   the unit resumes when polarity is corrected, with no fuse to replace. This is why the\\n"
    "   TVS sits on the BATTERY side of Q2: on the load side it would be unbiased in reverse\\n"
    "   and protect nothing. Q2 stress, both polarities:\\n"
    "     V_DS reverse  = battery reversed, worst case 24 V jump start reversed -> 24 V\\n"
    "     V_DS forward  = ~0, Q2 is ON; the TVS holds the node, Q2 merely conducts the surge\\n"
    "     -> 60 V part, >2x on the governing case.\\n"
    "   GATE is the fragile pin, not the channel. Source can reach the 38.9 V clamp while the\\n"
    "   gate is pulled to GND, i.e. V_GS = -38.9 V against a +/-20 V rating -> GATE DESTROYED.\\n"
    "   D3 (15 V) clamps V_GS; R (100k) limits the zener current: (38.9-15)/100k = 239 uA.\\n"
    "   D3 IS NOT OPTIONAL AND IS NOT A 'PROTECTION EXTRA' -- without it the FET dies on the\\n"
    "   first transient it was fitted to survive.\\n"
    "\\n"
    "4. LC DAMPING vs THE CONVERTERS' NEGATIVE INCREMENTAL RESISTANCE (Middlebrook).\\n"
    "   Three bucks and a SEPIC are CONSTANT-POWER loads: draw rises as the rail falls, which\\n"
    "   is a negative incremental resistance and will happily ring an undamped input filter.\\n"
    "     Load ~20 W. At 9 V crank:  R_neg = -V^2/P = -81/20 = -4.05 ohm  <-- the limit\\n"
    "     L = 4.7 uH, C = 22 uF nominal -> ~10 uF EFFECTIVE at 14 V (DC-bias derating; use the\\n"
    "       derated figure here, the nominal one is not the capacitor you have)\\n"
    "     Z0 = sqrt(L/C) = sqrt(4.7u/10u) = 0.686 ohm ; f0 = 23.2 kHz\\n"
    "   UNDAMPED, with ~10 mohm ESR:  Q = Z0/ESR = 68  ->  |Zout|peak = Q*Z0 = 47 ohm\\n"
    "       47 ohm  >>  4.05 ohm   ->  CRITERION VIOLATED BY ~21 dB. This oscillates.\\n"
    "   DAMPED, Rd = 0.68 ohm (= Z0) with Cd = 47 uF (>= 4x C, blocks DC so Rd burns nothing):\\n"
    "       Q ~ 1  ->  |Zout|peak ~ 0.69 ohm  <<  4.05 ohm   ->  5.9x, 15.4 dB margin  OK\\n"
    "   Rd AND Cd ARE A PAIR. Deleting Rd as 'a resistor doing nothing' restores the 47 ohm\\n"
    "   peak. Replacing Cd with a plain bulk cap puts Rd across DC and burns it.\\n"
    "   The alternator-whine filter and the stability network are THE SAME TWO COMPONENTS.\\n"
    "\\n"
    "5. CLAMP -> SWITCH-STRESS CHAIN, recorded as a consequence-check so a TVS change re-fires it\\n"
    "   (M7). The SEPIC's FET rating was derived FROM this clamp, not chosen independently:\\n"
    "       V_clamp(TVS) 38.9 V  +  V_out(SEPIC) 15.5 V  =  54.4 V switch stress  -> 80 V FET\\n"
    "   IF THE TVS PN CHANGES, THIS NUMBER CHANGES AND Q1's RATING MUST BE RE-CHECKED.\\n"
    "   An SMCJ36A (clamp 58.1 V) would put the SEPIC switch at 73.6 V and a 80 V FET at 92%\\n"
    "   of rating -- i.e. the F42 decision reaches Q1, which is on the other side of the sheet."
)

body = [place(*p) for p in PLACE]
# Testpoints live in their own column clear of every device row, not tucked between them.
# The previous layout interleaved them with the passive rows, which is what made the
# collision above possible in the first place.
for i, r in enumerate(TESTPOINTS):
    x, y = snap(700), snap(40 + i * 12)
    body.append("\n".join(emit_label(r, x, y, 0, "left", u("tp" + r))))
for i, (nx, ny, txt) in enumerate([(150.0, 200.0, NOTE), (150.0, 250.0, NOTE2),
                                   (560.0, 560.0, NOTE3), (560.0, 700.0, NOTE4),
                                   (560.0, 760.0, NOTE5), (40.0, 820.0, NOTE6)]):
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
