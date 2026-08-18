# Generates 06_analog_in.kicad_sch -- 4 differential inputs, dual-range, into the AK5574.
#
# ANCHORS, all T1 before a line was drawn:
#   AK5574 full scale = 0.56 x (VREFH - VREFL) = 2.80 Vpp diff = 0.99 Vrms at AVDD 5 V
#   INA1650           = gain 1 V/V, 500 kOhm input resistors, CMRR trimmed against THOSE
#   line    <= 2 Vrms  -> -6.1 dB  (divide by 2.02)
#   speaker <= 30 Vrms -> -29.6 dB (divide by 30.3)
import os, re, uuid, math

HW = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HW, "06_analog_in.kicad_sch")
NS = uuid.UUID("0d5f1a00-0000-4000-8000-0000000000ff")
SHEET_UUID = str(uuid.uuid5(NS, "sheet:06_analog_in.kicad_sch"))
SHEET_SYM_UUID = str(uuid.uuid5(NS, "inst:06_analog_in.kicad_sch"))
ROOT_UUID = "0d5f1a00-0000-4000-8000-000000000001"
VER = "20260306"
GRID = 1.27
def snap(v): return round(v / GRID) * GRID
def u(t): return str(uuid.uuid5(NS, "ain:" + t))

STOCK = r"C:/Program Files/KiCad/10.0/share/kicad/symbols"
PROJ = os.path.join(HW, "lib", "ODSP12.kicad_sym")

def extract(path, name):
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
    pins = []
    for mm in re.finditer(r'\(pin\s+\w+\s+\w+[\s\S]{0,400}?\(number "([^"]+)"', blk):
        at = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', mm.group(0))
        if at: pins.append((mm.group(1), float(at.group(1)), float(at.group(2))))
    # FOURTH instance of the extends-alias trap (LT3094, AP2127K-ADJ, USBLC6-2SC6, and now
    # PCF8574T), so it is handled generically rather than patched per part: an alias carries no
    # pins of its own, and its geometry lives under the parent's basename. Follow the extends,
    # take the PARENT's block, and let the caller rename the children to the alias basename --
    # aliasing to the parent's lib_id instead would put the parent's PACKAGE in the BOM.
    if not pins:
        ext = re.search(r'\(extends "([^"]+)"', blk)
        assert ext, f"{name}: ZERO pins and no (extends ...) -- regex/format mismatch"
        pblk, pins = extract(path, ext.group(1))
        blk = pblk.replace(f'(symbol "{ext.group(1)}"', f'(symbol "{name}"', 1)
        blk = blk.replace(f'(symbol "{ext.group(1)}_', f'(symbol "{name}_')
    assert pins, f"{name}: extracted ZERO pins -- regex/format mismatch, not an empty part"
    return blk, pins

import importlib.util
_spec = importlib.util.spec_from_file_location("gs", os.path.join(HW, "lib", "gen_symbols.py"))
gs = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(gs)

def geometry(pinlist, unit):
    """Per-unit geometry, using gen_symbols.unit_block's own math (M14)."""
    pins = [q for q in pinlist if q[3] == unit]
    half = (len(pins) + 1) // 2
    left, right = pins[:half], pins[half:]
    rows = max(len(left), len(right))
    w, top = 63.5, (rows + 1) * 2.54 / 2
    out = {}
    for i, (num, *_r) in enumerate(left):  out[num] = (-w / 2 - 5.08, top - 2.54 * (i + 1))
    for i, (num, *_r) in enumerate(right): out[num] = (w / 2 + 5.08, top - 2.54 * (i + 1))
    return {str(k): v for k, v in out.items()}

SRC = {
    "ODSP12:AK5574":  (PROJ, "AK5574"),
    "ODSP12:INA1650": (PROJ, "INA1650"),
    "Device:R":       (STOCK + "/Device.kicad_sym", "R"),
    "Device:C":       (STOCK + "/Device.kicad_sym", "C"),
    "Diode:BAV99":    (STOCK + "/Diode.kicad_sym", "BAV99"),
    "Relay:FINDER-30.22": (STOCK + "/Relay.kicad_sym", "FINDER-30.22"),
    "ODSP12:PCF8574T": (PROJ, "PCF8574T"),
    "ODSP12:ULN2003A": (PROJ, "ULN2003A"),
    "ODSP12:OPAMP_ADCDRV": (PROJ, "OPAMP_ADCDRV"),
}
DEFS, PINGEO = {}, {}
for libid, (path, nm) in SRC.items():
    blk, pins = extract(path, nm)
    base = libid.split(":")[1]
    blk = blk.replace(f'(symbol "{nm}_', f'(symbol "{base}_')
    DEFS[libid] = blk.replace(f'(symbol "{nm}"', f'(symbol "{libid}"', 1)
    PINGEO[libid] = {p[0]: (p[1], p[2]) for p in pins}

GND = "GND"; NC = None

# ---------------------------------------------------------------- the gain plan, computed
FS_RMS   = 0.56 * 5.0 / (2 * math.sqrt(2))    # 0.99 Vrms differential -- the TYP column
# F54: full scale carries a TOLERANCE -- +/-2.7 / 2.8 / 2.9 Vpp, min/typ/max (T1-105, figure
# level). A part at the MIN end reaches full scale on a SMALLER input, i.e. IT CLIPS FIRST, so
# min is the dangerous end and min is what the attenuator is designed against. Targeting 95 % of
# TYP left only 1.2 % on a min part -- the "cheap insurance" the first pass claimed was, on the
# worst-case part, almost entirely absent. This is CLAUDE.md S7's outward-rounding rule applied
# to a CEILING instead of a floor: round toward the end that fails.
FS_MIN   = 2.7 / (2 * math.sqrt(2))
LINE_MAX, SPKR_MAX = 2.0, 30.0
E96 = [100,102,105,107,110,113,115,118,121,124,127,130,133,137,140,143,147,150,154,158,162,165,
       169,174,178,182,187,191,196,200,205,210,215,221,226,232,237,243,249,255,261,267,274,280,
       287,294,301,309,316,324,332,340,348,357,365,374,383,392,402,412,422,432,442,453,464,475,
       487,499,511,523,536,549,562,576,590,604,619,634,649,665,681,698,715,732,750,768,787,806,
       825,845,866,887,909,931,953,976]
def e96(target):
    best = None
    for dec in range(-1, 7):
        for m in E96:
            v = m * (10 ** dec) / 10.0
            if best is None or abs(math.log(v / target)) < abs(math.log(best / target)): best = v
    return best
def rtxt(r):
    return f"{r/1e6:g}M" if r >= 1e6 else (f"{r/1e3:g}k" if r >= 1e3 else f"{r:g}R")

# Divider per LEG (the input is differential, so each leg carries an identical network and the
# MATCHING between legs is what sets CMRR -- see NOTE2). Rtop fixed; line mode = Rbot alone,
# speaker mode = Rbot in parallel with Rspk, switched at the BOTTOM of the divider where the
# node is already attenuated.
# THE INA1650'S 500 kOhm INPUT RESISTORS ARE PART OF THIS DIVIDER, not a load hanging off it.
# They shunt Rbot, so a ratio computed without them is simply wrong -- at Rtop = 100k the error
# was ~9 %, which is how this got caught: the first pass put SPEAKER mode at 100.9 % of full
# scale, i.e. CLIPPING AT THE STATED CEILING. Two consequences, both taken:
#   * Rtop drops to 10k. Loading falls from ~20 % to ~2 %, AND the CMRR budget improves in the
#     same move, because NOTE2's tolerance is on imbalance relative to the 500k trim network.
#   * Both ranges target 95 % of full scale, not 100 %. The ceiling is a SOURCE ceiling; landing
#     exactly on FS leaves nothing for source tolerance, and 0.4 dB is cheap insurance.
RIN    = 500e3                                     # INA1650 internal input resistor, per leg
TARGET = 0.95 * FS_MIN                             # F54: against MIN, not typ
RTOP = e96(10e3)
def _ratio(rb):
    par = rb * RIN / (rb + RIN)
    return par / (RTOP + par)
def _solve(vin):
    want = TARGET / vin
    lo, hi = 1.0, 10e6
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if _ratio(mid) < want: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)
RBOT = e96(_solve(LINE_MAX))
_need_par = _solve(SPKR_MAX)                        # required Rbot||Rspk before RIN shunting
RSPK = e96(1.0 / (1.0 / _need_par - 1.0 / RBOT))
V_LINE = LINE_MAX * _ratio(RBOT)
V_SPKR = SPKR_MAX * _ratio(RBOT * RSPK / (RBOT + RSPK))
ZIN = 2 * (RTOP + RBOT * RIN / (RBOT + RIN)) / 1e3

CH = [1, 2, 3, 4]
PLACE = []

# --- AK5574, two units -----------------------------------------------------------------
G1, G2 = geometry(gs.AK5574, 1), geometry(gs.AK5574, 2)
assert set(G1) | set(G2) == set(PINGEO["ODSP12:AK5574"]), "AK5574 units do not reconstruct"
assert not (set(G1) & set(G2)), "AK5574 pin in two units"
ADC = {
    # analog: AIN pairs carry the S10 [HARD] names, channel n -> TDM slot n, NO remapping
    "47": "AIN1_P", "48": "AIN1_N", "5": "AIN2_P", "4": "AIN2_N",
    "8": "AIN3_P", "9": "AIN3_N", "14": "AIN4_P", "13": "AIN4_N",
    "3": "+5V_A", "2": GND, "10": "+5V_A", "11": GND,     # VREFH/VREFL = AVDD/AVSS
    "6": "+5V_A", "7": GND, "1": NC, "12": NC,
    # digital
    "16": "MCLK_ADC", "25": "TDM_IN0_BCLK", "26": "TDM_IN0_LRCLK", "27": GND,   # TDMIN unused
    "28": "TDM_IN0_DATA", "29": NC, "30": "ADC_OVF",
    "24": GND,            # MSN low = SLAVE. S3 [HARD]. THE ONLY MODE PIN THE PART READS (p.56).
    "20": "ADC_PDN_N", "15": GND,                          # TEST has an internal pull-down
    "31": "I2C0_SDA", "33": "I2C0_SCL", "32": GND, "34": GND,   # CAD1:CAD0 = 00 -> 0x10
    "41": GND,            # PSN low  } T1-50: I2C mode needs BOTH
    "42": "+3V3_D",       # I2C high }
    "21": GND, "22": GND, "23": GND,                       # PW0-2
    "35": GND, "36": GND, "37": GND, "38": "+3V3_D",     # ALL INERT in I2C mode -- see NOTE13
    "39": "+3V3_D", "40": GND,                             # INERT; consistent with TDM1-0=01
    "43": GND, "44": "+3V3_D",                             # INERT; consistent with DP=0, HPFE=1
    "45": "+3V3_D", "46": GND,                             # LDOE REAL (no reg equiv); ODP inert
    "17": "+3V3_D", "18": GND, "19": "VDD18_ADC",          # VDD18 is an LDO OUTPUT -- F28 note
}
PLACE.append(("U40", "ODSP12:AK5574", 520, 130, "AK5574EN", {k: v for k, v in ADC.items() if k in G1}, 1, G1))
PLACE.append(("U40", "ODSP12:AK5574", 520, 300, "AK5574EN", {k: v for k, v in ADC.items() if k in G2}, 2, G2))

# --- two INA1650, one per two channels -------------------------------------------------
INA = PINGEO["ODSP12:INA1650"]
for pkg, (ca, cb) in enumerate([(1, 2), (3, 4)], start=1):
    ref = f"U4{pkg}"
    PLACE.append((ref, "ODSP12:INA1650", 300, 100 + (pkg - 1) * 170, "INA1650PW", {
        "1": "+13V5_A", "14": "-13V5_A",
        # OUT_A / OUT_B now land on SE{n}, NOT on AIN{n}_P. The INA1650 is single-ended-out
        # and ground-referenced; the ADC needs differential about 0.512 x AVDD. F50's copper
        # -- the level-shift block below -- is what sits between them.
        "2": f"ATT{ca}_P", "4": f"ATT{ca}_N", "3": GND, "13": f"SE{ca}", "12": "AGND_REF",
        "7": f"ATT{cb}_P", "5": f"ATT{cb}_N", "6": GND, "8": f"SE{cb}", "9": "AGND_REF",
        "11": f"{ref}_VMIDIN", "10": f"{ref}_VMIDOUT"}, 1, INA))

_pc = [0]
def passive(kind, x, y, val, na, nb):
    _pc[0] += 1
    return (kind + str(400 + _pc[0]), {"C": "Device:C", "R": "Device:R"}[kind], x, y, val,
            {"1": na, "2": nb})

P = []
# --- per channel: protection, matched attenuator, range relay, antialias ---------------
for n in CH:
    ybase = 40 + (n - 1) * 60
    for li, leg in enumerate(("P", "N")):
        y = ybase + li * 22          # the two legs need distinct rows, or their labels collide
        i, a = f"IN{n}_{leg}", f"ATT{n}_{leg}"
        # Series protection ahead of everything. Sized for an AMPLIFIER FAULT, not normal
        # drive: a shorted output stage can park the full rail on this pin.
        P += [passive("R", 40, y, "1k/1W", i, f"PRT{n}_{leg}")]
        P += [passive("R", 70, y, rtxt(RTOP), f"PRT{n}_{leg}", a)]     # Rtop
        P += [passive("R", 100, y, rtxt(RBOT), a, GND)]                # Rbot: line mode
        P += [passive("R", 130, y, rtxt(RSPK), a, f"SPK{n}_{leg}")]    # + Rspk in speaker mode
        # RAIL CLAMP -- and it is NOT optional. See NOTE5: without it the speaker-in-line-mode
        # fault puts +/-19 V on a pin whose absolute maximum is +/-14 V. Series pair to the
        # +/-13V5_A rails, so the junctions sit ~12 V outside the +/-1.3 V signal swing and
        # their nonlinear capacitance never modulates it. This is ALSO the ESD element.
        PLACE.append((f"D{n}{leg}", "Diode:BAV99", 165, y, "BAV99",
                      {"1": "-13V5_A", "2": a, "3": "+13V5_A"}))
        # Antialias: single-pole per leg into the ADC, differential pole across the pair.
        P += [passive("C", 190, y, "1n", a, GND)]
    # Relay shorts BOTH legs' Rspk to ground together -- one part, two poles, so the two legs
    # switch identically. Matching matters more than count here (NOTE2).
    # 2-pole changeover: A1/A2 coil, 11/12/14 pole 1, 21/22/24 pole 2. Only the NORMALLY OPEN
    # contacts are used -- de-energised = LINE (Rspk floating), energised = SPEAKER. Both legs
    # switch on one armature, which is the point: two single-pole relays would have independent
    # contact resistance and imbalance Rspk between the legs (NOTE2).
    PLACE.append((f"K{n}", "Relay:FINDER-30.22", 160, ybase, "2-pole signal relay, 5 V coil", {
        "A1": "+5V_D", "A2": f"RLY{n}_DRV",
        "11": f"SPK{n}_P", "14": GND, "12": NC,
        "21": f"SPK{n}_N", "24": GND, "22": NC}))
    P += [passive("C", 220, ybase + 11, "470p", f"ATT{n}_P", f"ATT{n}_N")]      # differential pole

# --- range control: I2C GPIO expander --------------------------------------------------
EXP = PINGEO["ODSP12:PCF8574T"]
_ex = {"1": GND, "2": GND, "3": GND, "8": GND, "16": "+3V3_D",
       "4": "RLY1_SEL", "5": "RLY2_SEL", "6": "RLY3_SEL", "7": "RLY4_SEL",
       "9": "SIGNAL_SENSE", "10": NC, "11": NC, "12": NC,
       # 13 = INT, 15 = SDA. The first pass had these two SWAPPED, and the F28
       # coverage assertion passed anyway -- it proves every pin has a net, never
       # that the net is the right one (M6). Caught by reading the parent map.
       "13": "I2C_ALERT_N", "14": "I2C0_SCL", "15": "I2C0_SDA"}
PLACE.append(("U43", "ODSP12:PCF8574T", 300, 430, "PCF8574T",
              {p: _ex.get(p) for p in EXP}))
# Pull-up for the shared open-drain alert line. ONE pull-up for three wire-ORed
# sources; it lives here because this sheet added the third one.
P += [passive("R", 360, 430, "10k", "+3V3_D", "I2C_ALERT_N")]
# Coil driver. The PCF8574 sinks 25 mA per pin and far less across the package, against
# ~30 mA x 4 coils -- so it CANNOT drive these directly, and the ULN2003A is not an
# afterthought part: its internal freewheel diodes (COM, pin 9) are also the flyback path
# every relay coil needs. One part answers both problems; omitting it would leave inductive
# kick on the expander outputs, which is the failure that takes months to present.
_uln = {"1": "RLY1_SEL", "2": "RLY2_SEL", "3": "RLY3_SEL", "4": "RLY4_SEL",
        "5": NC, "6": NC, "7": NC, "8": GND, "9": "+5V_D",
        "10": NC, "11": NC, "12": NC,
        "13": "RLY4_DRV", "14": "RLY3_DRV", "15": "RLY2_DRV", "16": "RLY1_DRV"}
PLACE.append(("U44", "ODSP12:ULN2003A", 420, 470, "ULN2003A",
              {q: _uln.get(q) for q in PINGEO["ODSP12:ULN2003A"]}))

# --- AGND_REF: buffered mid-rail is NOT wanted here; see NOTE3 --------------------------
P += [passive("C", 400, 430, "100n", "AGND_REF", GND),
      passive("R", 430, 430, "0R",   "AGND_REF", GND)]
for pkg in (1, 2):
    P += [passive("C", 40 + pkg * 30, 400, "1uF", f"U4{pkg}_VMIDIN", GND),
          passive("R", 100 + pkg * 30, 400, "0R", f"U4{pkg}_VMIDIN", f"U4{pkg}_VMIDOUT")]
# --- AK5574 supply and VDD18 ------------------------------------------------------------
P += [passive("C", 460, 400, "10uF", "+5V_A", GND), passive("C", 490, 400, "100n", "+5V_A", GND),
      passive("C", 520, 400, "10uF", "+3V3_D", GND), passive("C", 550, 400, "100n", "+3V3_D", GND),
      passive("C", 580, 400, "1uF", "VDD18_ADC", GND)]

# ======================================================================================
# F50 COPPER -- the ADC level-shift stage. All arithmetic below, none of it typed.
# ======================================================================================
AVDD             = 5.0
BIAS_LO, BIAS_HI = 0.502, 0.522          # T1-103, AKM's own window, as a fraction of AVDD
RB_TOP, RB_BOT   = 10.0e3, 10.5e3        # T1-103, AKM Figure 76's own divider
BIAS_RATIO       = RB_BOT / (RB_TOP + RB_BOT)
BIAS_V           = BIAS_RATIO * AVDD
WIN_HI  = (BIAS_HI - BIAS_RATIO) / BIAS_RATIO
WIN_LO  = (BIAS_RATIO - BIAS_LO) / BIAS_RATIO
def ratio_err(t): return (1 - BIAS_RATIO) * 2 * t          # worst-case ratio error, +/-t each
WIN_HALFWIDTH = (BIAS_HI - BIAS_LO) / 2 * AVDD              # +/-50 mV, the CM window in volts

# Leg N -- inverting, gain -0.5.  Leg P -- passive /2 in the GROUND domain, then a follower.
# Signal gain SE -> (AINP - AINN) is exactly 1; each pin moves +/-half.
R_IN, R_F   = 2.00e3, 1.00e3
R_A = R_B   = 2.00e3
R_BP        = 10.0e6
C1, C2      = 100e-6, 22e-9
C_F         = 620e-12                     # leg N feedback pole
R_S, C_SS, C_D = 10.0, 100e-12, 15e-9     # T1-103, AKM's own ADC-pin network
R_ADC = (3.0e3, 3.6e3, 4.2e3)             # AK5574 input resistance, min/typ/max (p.9)
NG_N        = 1 + R_F / R_IN              # 1.5 -- the price of gain 0.5 from a 1x source
RA_PAR      = R_A * R_B / (R_A + R_B)

FC_N = 1 / (2 * math.pi * R_IN * C1)
FC_P = 1 / (2 * math.pi * (R_BP + RA_PAR) * C2)
def hpf_phase(fc, f): return math.degrees(math.atan(fc / f))
F_POLE = 1 / (2 * math.pi * R_F * C_F)                       # = 1/(2*pi*RA_PAR*C_F), matched
COLD_DERATE = 0.75                                            # -25 % at -20 degC, worst case
FC_N_COLD   = FC_N / (COLD_DERATE * 0.8)                      # x tolerance -20 % as well

# Noise, input-referred at SE. Differential gain is 1, so a leg's OUTPUT noise refers 1:1.
KT4 = 4 * 1.380649e-23 * 298.15
def eR(r): return math.sqrt(KT4 * r)
N_RES  = math.sqrt(KT4 * (R_F + R_F ** 2 / R_IN + RA_PAR))
def n_stage(en): return math.hypot(N_RES, math.sqrt(NG_N ** 2 + 1) * en)
INA_EN  = 1.56e-6 / math.sqrt(20e3 - 20)       # T1: SBOS818B, 1.56 uVrms 20 Hz-20 kHz
RS_LEG  = 1.0 / (1 / RTOP + 1 / RBOT + 1 / RIN)
FE_EN   = math.hypot(INA_EN, math.sqrt(2) * eR(RS_LEG))
def degr(en): return 20 * math.log10(math.hypot(FE_EN, n_stage(en)) / FE_EN)
def en_for(db):                                 # invert: largest en meeting a dB budget
    lo, hi = 1e-12, 1e-6
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if degr(mid) < db: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)
EN_GATE = en_for(2.0)
FE_SNR  = 20 * math.log10(V_LINE / (FE_EN * math.sqrt(20e3 - 20)))

# F49's inequality, restated on the +5 V side. The fault is NOTE3's OWN documented case:
# a relay/driver failure leaves speaker level in line mode, the INA1650 clips at its rail,
# and that rail arrives through R_IN (leg N) and R_A (leg P) at pins that live on +5V_A.
V_INA_RAIL = 13.5
I_CLAMP    = sum((V_INA_RAIL - AVDD - 0.7) / r for r in (R_IN, R_A))
I_INJ      = len(CH) * I_CLAMP
I_5VA      = 146e-3                             # V-17, T1
IQ_GATE    = (250e-3 - 186e-3) / (2 * len(CH))  # V-17 headroom on +6V2_A / 8 amplifiers

SE_PK  = V_LINE * math.sqrt(2)                  # single-ended peak at the INA1650 output
# --- F54's stack. TWO terms, and they MULTIPLY (T1-111). The device column is spread at a
# given reference; Note 9's formula scales the TYP with VREFH. VREFH1-2 are tied to +5V_A on
# this board, so the reference tolerance IS the rail tolerance -- named here because Note 8
# caps VREFH at AVDD+0.1 V, so it is not a free variable.
RAIL_TOL  = 0.01                                # +5V_A setpoint accuracy (LT3045 + Rset)
FS_WORST  = FS_MIN * (1 - RAIL_TOL)
# --- B2: leg-gain mismatch is a SECOND ratio node, distinct from the bias divider.
# leg N gain = R_F/R_IN  -> two parts at +/-t, worst-case ratio error +/-2t
# leg P gain = R_B/(R_A+R_B) -> a divider, error (1-ratio)*2t = +/-t
def cm_resid(t):  return 0.5 * (0.5 * 2 * t + 0.5 * t) * SE_PK   # CM residual, volts pk
def gain_err(t):  return 1.5 * t                                  # differential gain error
Z_BIAS = 1.0 / (1 / (RB_TOP * RB_BOT / (RB_TOP + RB_BOT)) + 2 * math.pi * 20 * 10e-6)
def xtalk_dB(rbp, n=None):
    """Bias-node crosstalk at 20 Hz. n = aggressor count: len(CH) COHERENT is the design worst case; n=1 is the conventional acceptance condition. They differ by 12.0 dB and must never be quoted apart (C3)."""
    return 20 * math.log10((len(CH) if n is None else n) * NG_N / 2 * Z_BIAS / rbp)

BIAS = "VBIAS_ADC"
P += [passive("R", 60, 505, rtxt(RB_TOP), "+5V_A", BIAS),
      passive("R", 90, 505, rtxt(RB_BOT), BIAS, GND),
      passive("C", 120, 505, "10uF",      BIAS, GND),
      passive("C", 150, 505, "100n",      BIAS, GND)]

for n in CH:
    yb = 540 + (n - 1) * 100
    se, nc = f"SE{n}", f"LS{n}_NC"
    ni, pi = f"LS{n}_NI", f"LS{n}_PI"
    no, po = f"LS{n}_NO", f"LS{n}_PO"
    half   = f"SE{n}_H"
    # leg N: AC-couple, invert at -0.5 about BIAS
    P += [passive("C", 60, yb, "100uF NP", se, nc),
          passive("R", 90, yb, rtxt(R_IN), nc, ni),
          passive("R", 120, yb, rtxt(R_F), ni, no),
          passive("C", 150, yb, "620p C0G", ni, no)]
    # leg P: passive /2 to GND -- NOT to AGND_REF, which is the INA1650's REF sense node and
    # must carry no signal current -- then AC-couple into a follower biased through R_BP.
    P += [passive("R", 60, yb + 14, rtxt(R_A), se, half),
          passive("R", 90, yb + 14, rtxt(R_B), half, GND),
          passive("C", 120, yb + 14, "620p C0G", half, GND),
          passive("C", 150, yb + 14, "22n film", half, pi),
          passive("R", 180, yb + 14, rtxt(R_BP), pi, BIAS)]
    # Clamps at the two op-amp inputs -- the ONLY nodes on this stage that a +/-13V5_A fault
    # can reach. Leg N's sits on a virtual earth, so it carries no signal and contributes no
    # nonlinear capacitance at all; leg P's sees signal but from a 1k source (NOTE7).
    PLACE.append((f"D{409 + n}", "Diode:BAV99", 215, yb, "BAV99", {"1": GND, "2": ni, "3": "+5V_A"}))
    PLACE.append((f"D{413 + n}", "Diode:BAV99", 215, yb + 14, "BAV99", {"1": GND, "2": pi, "3": "+5V_A"}))
    ref = f"U{44 + n}"
    OA1, OA2, OA3 = (geometry(gs.OPAMP_ADCDRV, i) for i in (1, 2, 3))
    assert set(OA1) | set(OA2) | set(OA3) == set(PINGEO["ODSP12:OPAMP_ADCDRV"]), "opamp units"
    PLACE.append((ref, "ODSP12:OPAMP_ADCDRV", 320, yb, "OPA2320AIDR",
                  {"1": no, "2": ni, "3": BIAS}, 1, OA1))
    PLACE.append((ref, "ODSP12:OPAMP_ADCDRV", 320, yb + 20, "OPA2320AIDR",
                  {"7": po, "6": po, "5": pi}, 2, OA2))
    PLACE.append((ref, "ODSP12:OPAMP_ADCDRV", 320, yb + 40, "OPA2320AIDR",
                  {"8": "+5V_A", "4": GND}, 3, OA3))
    P += [passive("C", 380, yb + 40, "100n", "+5V_A", GND)]
    # AKM's own ADC-pin network, values verbatim. C0G rather than the figure's "film" note:
    # at 100 pF / 620 pF / 15 nF, C0G is strictly better than film on every axis that matters
    # here (no piezoelectricity, no voltage coefficient, +/-30 ppm/degC) and is available in
    # 0603/0805. Departing UPWARD from a vendor note, with the reason stated.
    P += [passive("R", 400, yb, "10R", no, f"AIN{n}_N"),
          passive("C", 430, yb, "100p C0G", f"AIN{n}_N", GND),
          passive("R", 400, yb + 14, "10R", po, f"AIN{n}_P"),
          passive("C", 430, yb + 14, "100p C0G", f"AIN{n}_P", GND),
          passive("C", 460, yb + 7, "15n C0G", f"AIN{n}_P", f"AIN{n}_N")]

PLACE += P

LABELS = {}
def emit_label(net, lx, ly, rot, just, uid):
    prev = LABELS.get((lx, ly))
    assert prev is None or prev == net, (
        f"LABEL COLLISION at ({lx}, {ly}): '{prev}' and '{net}' would be shorted.")
    LABELS[(lx, ly)] = net
    return [f'\t(global_label "{net}"', '\t\t(shape bidirectional)',
            f'\t\t(at {lx} {ly} {rot})', '\t\t(fields_autoplaced yes)',
            f'\t\t(effects (font (size 1.27 1.27)) (justify {just}))',
            f'\t\t(uuid "{uid}")', '\t)']

def place(ref, libid, x, y, val, nets, unit=1, geo=None):
    x, y = snap(x), snap(y)
    geo = geo if geo is not None else PINGEO[libid]
    assert geo, f"{ref}: no pin geometry for {libid}"
    missing = set(geo) - set(nets)
    extra = set(nets) - set(PINGEO[libid])
    assert not missing, f"{ref}: pins with no disposition (F28): {sorted(missing)}"
    assert not extra, f"{ref}: nets on non-existent pins {sorted(extra)}"
    out = ['\t(symbol', f'\t\t(lib_id "{libid}")', f'\t\t(at {x} {y} 0)', f'\t\t(unit {unit})',
           '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)', '\t\t(dnp no)',
           f'\t\t(uuid "{u("i" + ref + str(unit))}")',
           f'\t\t(property "Reference" "{ref}" (at {x} {y - 22} 0) (effects (font (size 1.27 1.27))))',
           f'\t\t(property "Value" "{val}" (at {x} {y - 19} 0) (effects (font (size 1.27 1.27))))',
           '\t\t(instances', '\t\t\t(project "ODSP12-MB"',
           f'\t\t\t\t(path "/{ROOT_UUID}/{SHEET_SYM_UUID}" (reference "{ref}") (unit {unit}))',
           '\t\t\t)', '\t\t)', '\t)']
    for num, (sx, sy) in geo.items():
        lx, ly = snap(x + sx), snap(y - sy)
        if nets[num] is None:
            out.append(f'\t(no_connect (at {lx} {ly}) (uuid "{u("nc" + ref + str(unit) + num)}"))')
            continue
        rot = 180 if sx < 0 else 0
        just = "right" if sx < 0 else "left"
        out += emit_label(nets[num], lx, ly, rot, just, u("l" + ref + str(unit) + num))
    return "\n".join(out)

# ---------------------------------------------------------------- notes
cm_ceiling = lambda dr: 20 * math.log10(500e3 / dr)
NOTE1 = (
    "GAIN PLAN, WORKED FORWARD -- source ceiling to ADC full scale. A range change re-fires\\n"
    "this arithmetic; that is the point of writing it here rather than in a note file.\\n"
    "\\n"
    "  ADC full scale = 0.56 x (VREFH - VREFL) = 0.56 x 5 V = 2.80 Vpp diff = %.3f Vrms\\n"
    "  INA1650 gain   = 1 V/V EXACTLY -- there is no gain to share between stages, so the\\n"
    "                   attenuator does ALL the range work in BOTH modes.\\n"
    "\\n"
  "  FULL SCALE CARRIES A TOLERANCE AND THE MINIMUM GOVERNS (F54). The spec table reads\\n"
    "  +/-2.7 / 2.8 / 2.9 Vpp min/typ/max = %.4f / %.4f / %.4f Vrms differential. A part at\\n"
    "  the MIN end reaches full scale on a SMALLER input -- IT CLIPS FIRST -- so min is the\\n"
    "  dangerous end and min is the design point. Targeting 95%% of TYP would leave only 1.2%%\\n"
    "  on a min part, i.e. the 'cheap insurance' would be absent exactly where it is needed.\\n"
    "  This is CLAUDE.md S7's round-outward rule applied to a CEILING rather than a floor.\\n"
    "  Cost of the change: %.2f dB of signal, hence %.2f dB of SNR, on a path whose noise is\\n"
    "  set by the attenuator and the INA1650 anyway (NOTE8) -- and the ADC's own floor is\\n"
    "  ~%.0f dB below that, so it buys the margin back for nothing that matters.\\n"
    "\\n"
    "  Rtop = %s per leg, Rbot = %s per leg, Rspk = %s per leg (switched by K1-K4)\\n"
    "  LINE    (Rbot alone):        %.2f Vrms in -> %.3f Vrms  (%.1f%% of FS min, %.1f%% typ)\\n"
    "  SPEAKER (Rbot || Rspk):      %.1f Vrms in -> %.3f Vrms  (%.1f%% of FS min, %.1f%% typ)\\n"
    "  Zin, line mode, differential = 2 x (Rtop + Rbot) = %.0f kOhm  vs the >= 20 kOhm decree\\n"
    "\\n"
    "NOTE WHAT IS *NOT* HERE: no gain stage. That is a consequence, not an omission -- the\\n"
    "INA1650 is fixed at 1 V/V, so any topology that attenuated further would need one, and\\n"
    "every extra stage multiplies the attenuator's own noise before the ADC sees it."
) % (FS_RMS, FS_MIN, FS_RMS, 2.9 / (2 * math.sqrt(2)),
     20 * math.log10(FS_RMS / FS_MIN), 20 * math.log10(FS_RMS / FS_MIN), 117.0 - FE_SNR,
     rtxt(RTOP), rtxt(RBOT), rtxt(RSPK),
     LINE_MAX, V_LINE, 100 * V_LINE / FS_MIN, 100 * V_LINE / FS_RMS,
     SPKR_MAX, V_SPKR, 100 * V_SPKR / FS_MIN, 100 * V_SPKR / FS_RMS, ZIN)

NOTE2 = (
    "F9 AS AN INEQUALITY, NOT A PARTS PREFERENCE -- and the mechanism is NOT the divider ratio.\\n"
    "\\n"
    "The INA1650's CMRR is trimmed against its OWN internal 500 kOhm resistor network. Whatever\\n"
    "source impedance the attenuator presents lands IN SERIES with those internal resistors, so\\n"
    "it is the IMBALANCE between the P and N legs -- not the absolute value, not the ratio --\\n"
    "that detunes the trim. The ceiling is roughly:\\n"
    "        CMRR_limit  ~  20 x log10( 500 kOhm / dRs )\\n"
    "  dRs = 500 Ohm  -> %.0f dB      dRs = 50 Ohm -> %.0f dB      dRs = 5 Ohm -> %.0f dB\\n"
    "  S12 acceptance is CMRR >= 60 dB, so dRs must stay BELOW ~500 Ohm to clear it at all,\\n"
    "  and below ~50 Ohm to clear it with the margin an acceptance line deserves.\\n"
    "\\n"
    "Rtop is %s. 50 Ohm of imbalance on %s is 0.05 %% -- so DISCRETE 0.1 %% SINGLES DO NOT\\n"
    "COMFORTABLY CLEAR IT, and 1 %% parts miss it outright. THE ARRAY RECOMMENDATION FALLS OUT\\n"
    "OF THIS INEQUALITY rather than preceding it:\\n"
    "  * Use INTEGRATED RESISTOR ARRAYS for Rtop and Rbot -- P and N legs in ONE package.\\n"
    "  * The spec that matters is RATIO MATCHING and TRACKING, not absolute tolerance.\\n"
    "  * TEMPCO TRACKING is the half that discrete 0.1 %% parts cannot buy at any price: the\\n"
    "    decree is -20 to +70 degC, a 90 degC span, and two discrete parts with independent\\n"
    "    +/-25 ppm/degC drift 2250 ppm apart across it -- 0.225 %%, which is 4.5x the 0.05 %%\\n"
    "    budget above. CMRR measured at 25 degC on the bench would pass and then degrade in\\n"
    "    a hot car. An array's elements share a die and track.\\n"
    "  * K1-K4 are TWO-POLE relays switching both legs together for the same reason: two\\n"
    "    single-pole parts have independent contact resistance and would imbalance Rspk.\\n"
    "\\n"
    "This is why F8 put the divider AHEAD of the switch and why F9 is a BOM requirement."
) % (cm_ceiling(500), cm_ceiling(50), cm_ceiling(5), rtxt(RTOP), rtxt(RTOP))

NOTE3 = (
    "WHY THE RANGE ELEMENT IS A RELAY, DERIVED -- not asserted (Q2 convention).\\n"
    "\\n"
    "At the 30 Vrms speaker ceiling the INPUT NODE sees +/-42 V peak. Walk the options:\\n"
    "  * Analog switch AT THE INPUT: needs rails containing +/-42 V. The largest analog rail\\n"
    "    on this board is +/-13V5_A. IT DOES NOT CONTAIN THE SWING. Excluded by arithmetic,\\n"
    "    which is exactly the reasoning that made F8 say 'or use a relay'.\\n"
    "  * Analog switch AFTER a fixed first-stage attenuator: the switch then sees ~1 Vrms in\\n"
    "    NORMAL use -- but the misconfiguration case is not exotic, it is the DEFAULT user\\n"
    "    error: speaker level applied while the board still thinks it is in line mode. The\\n"
    "    node then sits at 30/2.02 = %.1f Vrms = +/-%.0f V peak, and the switch is across it.\\n"
    "    Survivable only by adding clamps that then load the signal.\\n"
    "  * RELAY in the bottom leg: contacts are indifferent to +/-42 V, add no distortion\\n"
    "    (S6.2's own preference), and the misconfiguration case is a non-event.\\n"
    "  -> RELAY. K1-K4, two Form A poles each, shorting Rspk to ground on BOTH legs together.\\n"
    "\\n"
    "FAIL DIRECTION IS DELIBERATE: de-energised = LINE (Rbot alone, less attenuation). The\\n"
    "opposite choice -- de-energised = speaker -- is the better FAIL-SAFE, since the safe state\\n"
    "is maximum attenuation, and it was rejected on power: line is the common install, so it\\n"
    "would energise four coils continuously in the ordinary case, ~120 mA on +5V_D forever.\\n"
    "THE CONSEQUENCE, STATED: a coil or driver failure in a speaker-level install presents as\\n"
    "%.1f Vrms into the INA1650, which CLIPS but does not damage it (500 kOhm inputs and the\\n"
    "1k/1W series parts limit the current). Audible distortion, not silence and not smoke.\\n"
    "REOPEN if a field failure makes that the wrong trade.\\n"
    "\\n"
    "REF A / REF B (12, 9) are tied to AGND_REF, a QUIET GROUND REFERENCE, through a 0R --\\n"
    "the banked disposition: 'must be driven from a low impedance, NOT left to a divider.'\\n"
    "A BUFFERED MID-RAIL IS DELIBERATELY *NOT* USED: the INA1650 runs on +/-13V5_A, so its\\n"
    "own mid-rail IS ground, and a buffer would only add a noise source and a failure mode\\n"
    "between the reference pin and the thing it references. VMID_OUT is tied back to VMID_IN\\n"
    "through 0R with a noise-reduction cap, which is the datasheet's own arrangement.\\n"
    "The 0R positions exist so a star point can be moved at layout WITHOUT a schematic edit."
) % (SPKR_MAX / (LINE_MAX / V_LINE), SPKR_MAX / (LINE_MAX / V_LINE) * math.sqrt(2),
     SPKR_MAX / (LINE_MAX / V_LINE))

NOTE4 = (
    "SIGNAL-SENSE, ESD, AND THE OUTSIDE WORLD.\\n"
    "\\n"
    "SIGNAL-SENSE MUST NOT CHATTER. S6.1 sets ~10 mVrms, resistor-settable. Music AT the\\n"
    "threshold is not a steady tone -- it crosses in and out on every phrase, so a bare\\n"
    "comparator would square-wave the remote-out logic and click the amplifiers on and off.\\n"
    "TWO things are therefore required and NEITHER is optional:\\n"
    "  * HYSTERESIS: assert at ~10 mVrms, release at ~5 mVrms (6 dB), so the release point is\\n"
    "    a different signal level, not a different sample of the same one.\\n"
    "  * ASYMMETRIC TIME CONSTANTS: attack ~50 ms (fast enough not to clip the first note),\\n"
    "    release ~20-30 s (long enough to ride a track gap, a quiet passage, or a fade).\\n"
    "    The release constant is the one that matters and it is LONG -- it is set by the\\n"
    "    longest musical silence the user will tolerate as 'still on', not by electronics.\\n"
    "  * THE SENSE PATH TAPS *AFTER* THE ATTENUATOR, at ATTn_*, so it inherits the range\\n"
    "    switching and can never see the 30 Vrms it is monitoring. Tapping the raw input --\\n"
    "    the obvious place -- would put +/-42 V on a comparator input.\\n"
    "  SIGNAL_SENSE lands on the expander (U43 P0 as an input), NOT a native GPIO, because\\n"
    "  03_control has none left. Detection latency over I2C is irrelevant at a 20 s release.\\n"
    "\\n"
    "SERIES PROTECTION IS SIZED FOR AN AMPLIFIER FAULT, NOT NORMAL DRIVE. The 1k/1W parts\\n"
    "ahead of every divider assume a shorted output stage parks a full rail on the pin: at\\n"
    "42 V across 1k that is 1.8 W momentarily and 42 mA into the network -- the resistor is\\n"
    "the fuse, and it is specified at 1 W so it survives long enough to be the thing that\\n"
    "fails safely rather than the INA1650.\\n"
    "\\n"
    "ESD MUST NOT BUY ITS PROTECTION WITH DISTORTION. Any diode across an audio node is a\\n"
    "voltage-variable capacitance in the signal path. Requirements for this position:\\n"
    "  * LOW capacitance (< 5 pF) and, more importantly, FLAT capacitance vs voltage.\\n"
    "  * BIASED OUTSIDE THE SIGNAL RANGE -- referenced to +/-13V5_A, not to ground, so the\\n"
    "    junctions never modulate across the audio swing. A ground-referenced clamp sits at\\n"
    "    its most nonlinear exactly where the signal lives.\\n"
    "  * S12's CCIF twin-tone criterion is the test that SEES this, and it is the same\\n"
    "    mechanism the mute shunt's off-capacitance was called out for -- second instance,\\n"
    "    same measurement.\\n"
    "  Part not yet pinned: this is an F38 line, and it wants manufacturer stated (F38a).\\n"
    "\\n"
    "RCA SHIELDS land on the S9 chassis star through the RC network, on 09_io -- NOT here,\\n"
    "and NOT to AGND_REF. Named so the two are not confused at layout."
)

NOTE5 = (
    "F50 COPPER -- AND WHY IT IS DIFFERENTIAL RATHER THAN THE UNITY BUFFER THAT WAS PLANNED.\\n"
    "\\n"
    "THE LOAD-BEARING REASON IS T1, FIGURE-LEVEL, AND DOES NOT DEPEND ON PARSING A SENTENCE:\\n"
    "AKM's own reference circuit for this exact part -- Figure 76 -- DRIVES BOTH ADC PINS\\n"
    "ANTIPHASE, from legs with Bias on their non-inverting inputs. Their published DR = 121 dB\\n"
    "and S/(N+D) = 112 dB are measured with that circuit. Departing from a converter vendor's\\n"
    "reference INPUT circuit is the class of decision that has cost this project before.\\n"
    "\\n"
    "BUT THIS IS NOT FIGURE 76'S TOPOLOGY, AND AN EARLIER DRAFT OF THIS NOTE WRONGLY SAID IT WAS.\\n"
    "Figure 76 does the single-ended-to-differential conversion UPSTREAM AND AT UNITY -- an\\n"
    "NJM5534 inverting 4.7k/4.7k stage on +/-15 V makes Vin-, a direct wire through JP2 makes\\n"
    "Vin+ -- and only then feeds TWO IDENTICAL inverting attenuators (3.3k in, 620R || 1n fb).\\n"
    "AKM's two Bias-referenced legs are MATCHED TO EACH OTHER. Ours are not: leg N is an ACTIVE\\n"
    "inverter at -0.5, leg P a PASSIVE /2 into a follower.\\n"
    "  WHY NOT COPY THEM EXACTLY: their upstream inverter needs the +/-rail domain, and ours is\\n"
    "  already spent -- the INA1650 IS our +/-13V5_A stage. Reproducing Figure 76 literally means\\n"
    "  a THIRD amplifier per channel (12 rather than 8) and one more stage of noise and\\n"
    "  distortion ahead of the split, to buy leg matching that NOTE11 shows we do not need.\\n"
    "  THE PROPERTY WE TRANSFERRED IS REAL -- Bias arriving only at high-impedance inputs, no\\n"
    "  signal current in the shared node. THE PROPERTY WE DID NOT is leg symmetry, and its\\n"
    "  consequence is quantified in NOTE11 rather than left as a resemblance claim.\\n"
    "\\n"
    "A SECOND, INDEPENDENT REASON: driving differentially HALVES the per-pin swing, to\\n"
    "%.3f..%.3f V instead of %.3f..%.3f V on a 5 V rail. That is what makes RAIL-TO-RAIL\\n"
    "OUTPUT UNNECESSARY and widens the candidate set for F52 considerably.\\n"
    "\\n"
    "CORROBORATION, AND IT IS DELIBERATELY NOT THE LEAD -- read the caveat with it. AKM writes:\\n"
    "'The S/(N+D) characteristics of the AK5574 varies depending on DC BIAS VOLTAGE of the\\n"
    "input signal. Set the DC BIAS VOLTAGE in a range from 0.502 x AVDD to 0.522 x AVDD for\\n"
    "OPTIMAL characteristics.' Note precisely what that sentence is and is not. It says DC bias,\\n"
    "twice, and it says optimal -- NOT abs-max, NOT guaranteed operation. Single-ended drive\\n"
    "keeps the DC bias compliant and modulates the INSTANTANEOUS common mode instead, by\\n"
    "%.0f mV peak against a window only +/-%.0f mV wide. IF S/(N+D) tracks the operating point\\n"
    "then a signal that moves the operating point modulates distortion -- which is the textbook\\n"
    "route to even-order products, and is why differential drive cancels them. THAT INFERENCE\\n"
    "IS OURS, NOT AKM's. It is T2, it corroborates, and NOTHING HERE RESTS ON IT: the vendor\\n"
    "built a differential drive for a part whose spec sentence mentions only DC bias, and the\\n"
    "swing argument above stands on its own. Stated this way so that the first reader who pulls\\n"
    "page 67 and sees 'DC bias voltage' does not conclude the constraint was misread and revert\\n"
    "to a unity buffer, taking the vendor-topology benefit with it.\\n"
    "\\n"
    "Either way the built circuit has the stronger property: the common mode sits at BIAS at\\n"
    "EVERY INSTANT, by construction, independent of signal level.\\n"
    "\\n"
    "The INA1650 is single-ended-out, so this stage must also convert. Per channel:\\n"
    "  LEG N  SE{n} -- C1 %s -- R_IN %s -> (-)in ; R_F %s || C_F 620p ; (+)in = VBIAS_ADC\\n"
    "         inverting, gain -0.5, output = BIAS - 0.5 x SE\\n"
    "  LEG P  SE{n} -- R_A %s -- SE{n}_H -- R_B %s -- GND      (passive /2, GROUND domain)\\n"
    "         SE{n}_H -- C2 %s -> follower(+) ; R_BP %s to VBIAS_ADC\\n"
    "         non-inverting, gain +0.5 of SE, output = BIAS + 0.5 x SE\\n"
    "  AINnP - AINnN = SE exactly. UNITY DIFFERENTIAL GAIN, which is what 'unity' has to mean\\n"
    "  here: %.3f Vrms single-ended in, %.3f Vrms differential at the ADC, %.1f %% of FS.\\n"
    "  Each pin moves only +/-%.0f mV about %.2f V -- %.2f to %.2f V on a 5 V rail.\\n"
    "\\n"
    "THREE PLACEMENT CHOICES THAT ARE NOT ARBITRARY:\\n"
    "  * R_B RETURNS TO GND, NOT TO AGND_REF. AGND_REF is the INA1650's REF SENSE node and\\n"
    "    must carry no current -- that is the whole content of T1-67. The /2 divider carries\\n"
    "    %.0f uA of audio per channel; putting that into AGND_REF would modulate the receiver's\\n"
    "    own reference with its own output. Same rule as F36: a sense node is not a return.\\n"
    "  * R_BP IS %s AND THAT IS THE POINT, NOT AN OVERSIZE -- WITH THE TRANSFER FUNCTION, since\\n"
    "    this is a 40 dB decision and a cost pass needs to trip over the arithmetic, not the\\n"
    "    conclusion. Anything returning to VBIAS_ADC injects signal current into a node shared\\n"
    "    by all four channels. Worst case is a correlated (mono) input on all four:\\n"
    "        i_tot   = N_ch x (SE/2) / R_BP                 leg P taps the /2 node\\n"
    "        Z_bias  = (RB_TOP||RB_BOT) || 1/(2.pi.f.C)  = %.0f || %.0f = %.0f Ohm at 20 Hz\\n"
    "        v_bias  = i_tot x Z_bias\\n"
    "      and v_bias reaches the VICTIM ASYMMETRICALLY, which is the half that is easy to miss:\\n"
    "      leg N's (+) input takes it at NOISE GAIN %.1f, while leg P's arrives through R_BP\\n"
    "      against a %s source and is divided by %.0e. So a COMMON-MODE disturbance on the bias\\n"
    "      node lands DIFFERENTIALLY at the ADC, and the ADC cannot reject it.\\n"
    "        crosstalk = (N_ch x NG_N / 2) x Z_bias / R_BP\\n"
    "      THE /2 IS NOT A FUDGE AND IT IS WORTH 6.0 dB, SO IT GETS NAMED: the INJECTING node is\\n"
    "      leg P's (+) input, which carries the /2-divided signal (%.0f mV pk), while the VICTIM's\\n"
    "      reference is its full differential swing (%.3f V pk). Exactly a factor of two. N_ch is\\n"
    "      COHERENT summing -- four channels driven by the same mono source, which is the worst\\n"
    "      case; audio crosstalk is conventionally specified with ONE channel driven, and that\\n"
    "      case is 12 dB quieter. Stated because coherent and uncorrelated summing differ by 6 dB\\n"
    "      and a reader cannot tell which was assumed from the constant alone.\\n"
    "      R_BP = %s  ->  %.1f dB        R_BP = 100k  ->  %.1f dB, which is audible\\n"
    "\\n"
    "      TWO CONDITIONS, AND THEY MUST NEVER BE QUOTED APART. The design was sized for FOUR\\n"
    "      COHERENT aggressors; the conventional acceptance measurement drives ONE channel.\\n"
    "      They differ by 20log10(4) = 12.0 dB:\\n"
    "         one channel driven   (what a bench test reports)      %.1f dB\\n"
    "         four coherent        (what the design was sized for)  %.1f dB\\n"
    "      Against a proposed S12 line of >= 70 dB that is %.1f dB of margin on the bench and\\n"
    "      only %.1f dB against the design case. THE BENCH NUMBER IS THE SAFE-DIRECTION ONE,\\n"
    "      so nobody audits it: the test passes comfortably and a later cost pass reads the\\n"
    "      comfort as spendable. M10 in its exact form -- which is why both numbers live here\\n"
    "      rather than the flattering one.\\n"
    "      FOR SCALE, the silicon: AK5574 interchannel isolation 110 dB min / 120 typ -- and\\n"
    "      note ITS condition too, specified AIN1<->AIN2 and AIN3<->AIN4, i.e. WITHIN a pair,\\n"
    "      not across all four. The shared bias node is the dominant term on either reading.\\n"
    "    The four channels together draw only %.2f uA at %s. AKM never meets any of this because\\n"
    "    BOTH their legs are inverting and their Bias node feeds only high-impedance (+) inputs.\\n"
    "    Our leg P is a follower, so the problem is ours and the fix has to be ours.\\n"
    "    NOTE THE COUPLING TO NOTE8: R_BP is also NOISELESS only because the /2 divider shunts\\n"
    "    it -- %s || %s = %.0f Ohm. Raise the divider and R_BP stops being free in BOTH budgets.\\n"
    "    AND R_BP HAS A THIRD REASON, WHICH IS THE COUPLING CAP IT BUYS. C2's corner is set\\n"
    "    against R_BP, not against the divider: %s gives %.2f Hz with a %s FILM part. At 100k the\\n"
    "    same corner needs ~2.2 uF -- an electrolytic or a large film part IN THE SIGNAL PATH,\\n"
    "    which is exactly what forced AKM's 68 uF. So this resistor buys crosstalk margin AND a\\n"
    "    small cheap low-distortion coupling cap. RECORDED AS THREE REASONS DELIBERATELY: a\\n"
    "    single-reason component is one cost pass away from being halved; a three-reason one is\\n"
    "    not, and the cost pass can see all three without re-deriving them.\\n"
    "  * THE TWO LEGS ARE PARALLEL, NOT CASCADED. Taking leg P as an inverter of leg N's\\n"
    "    output is one part cheaper and wrong: leg N's distortion would then appear at BOTH\\n"
    "    pins with opposite sign and DOUBLE differentially, where in parallel the two legs'\\n"
    "    distortions are uncorrelated and add in quadrature (x1.41, not x2).\\n"
    "\\n"
    "SUPERSEDES F50's FIRST FIX. Driving INA1650 REF A/B to ~2.56 V was the original answer;\\n"
    "it is single-ended drive by another name and falls to the same arithmetic. REF A/B stay\\n"
    "on AGND_REF, and NOTE3's disposition of them stands unchanged."
) % (BIAS_V - SE_PK / 2, BIAS_V + SE_PK / 2, BIAS_V - SE_PK, BIAS_V + SE_PK,
     SE_PK / 2 * 1e3, WIN_HALFWIDTH * 1e3,
     "100uF NP", rtxt(R_IN), rtxt(R_F), rtxt(R_A), rtxt(R_B), "22n film", rtxt(R_BP),
     V_LINE, V_LINE, 100 * V_LINE / FS_MIN, SE_PK / 2 * 1e3, BIAS_V,
     BIAS_V - SE_PK / 2, BIAS_V + SE_PK / 2,
     V_LINE / 2 / R_B * 1e6, rtxt(R_BP),
     RB_TOP * RB_BOT / (RB_TOP + RB_BOT), 1 / (2 * math.pi * 20 * 10e-6), Z_BIAS,
     NG_N, rtxt(RA_PAR), RA_PAR / R_BP,
     SE_PK / 2 * 1e3, SE_PK,
     rtxt(R_BP), xtalk_dB(R_BP), xtalk_dB(100e3),
     xtalk_dB(R_BP, 1), xtalk_dB(R_BP),
     (-70.0) - xtalk_dB(R_BP, 1), (-70.0) - xtalk_dB(R_BP),
     len(CH) * V_LINE / 2 / R_BP * 1e6, rtxt(R_BP),
     rtxt(R_BP), rtxt(RA_PAR), 1 / (1 / R_BP + 1 / RA_PAR),
     rtxt(R_BP), FC_P, "22n")

NOTE6 = (
    "THE BIAS DIVIDER IS A RATIO SPEC, AND THE E96-PLUS-TOLERANCE CONVENTION WAS BUILT FOR\\n"
    "ABSOLUTE ONES. So it is written here as the inequality it actually is.\\n"
    "\\n"
    "  %s / %s from +5V_A  ->  ratio = %.5f x AVDD = %.4f V, AKM's own value (T1-103)\\n"
    "  Window %.3f..%.3f x AVDD, expressed RELATIVE to that nominal:  -%.2f %% / +%.2f %%\\n"
    "  Worst-case ratio error from two independent +/-t parts = (1 - ratio) x 2t:\\n"
    "     t = 1 %%    ->  +/-%.3f %%   clears by %.1fx   -- LEGAL, and this is the fallback\\n"
    "     t = 0.1 %%  ->  +/-%.3f %%   clears by %.0fx   -- and F9 already puts 0.1 %% arrays\\n"
    "                                                       on this sheet, so it may be free\\n"
    "  RATIOMETRIC IS THE WHOLE POINT: a fixed 2.56 V reference lands at %.4f and %.4f x AVDD\\n"
    "  against AVDD +/-2 %% -- OUTSIDE THE WINDOW AT BOTH ENDS before any error term joins.\\n"
    "  Only a divider from AVDD itself tracks, which is why AKM drew one.\\n"
    "\\n"
    "STIFFNESS: 10 uF || 100 nF at the node, per AKM. T1-67 DOES NOT ENGAGE HERE and the\\n"
    "reason is structural, not a judgement call -- VBIAS_ADC feeds op-amp (+) inputs, which\\n"
    "are high-impedance, whereas T1-67's rule is about the INA1650's REF pin, which sits\\n"
    "inside a resistor network that BELIEVES whatever it sees. Same board, same voltage,\\n"
    "different pin class. The 10 uF is the reason R_BP had to be %s -- see NOTE5.\\n"
    "\\n"
    "TEMPERATURE: this is a RATIO, so the divider's absolute tempco cancels and only\\n"
    "TRACKING matters -- the same argument NOTE2 makes for the attenuator, and the same\\n"
    "reason an array beats two discretes over the -20..+70 degC decree."
) % (rtxt(RB_TOP), rtxt(RB_BOT), BIAS_RATIO, BIAS_V, BIAS_LO, BIAS_HI,
     100 * WIN_LO, 100 * WIN_HI,
     100 * ratio_err(0.01), WIN_LO / ratio_err(0.01),
     100 * ratio_err(0.001), WIN_LO / ratio_err(0.001),
     2.56 / (AVDD * 1.02), 2.56 / (AVDD * 0.98), rtxt(R_BP))

NOTE7 = (
    "COUPLING CORNERS -- TWO OF THEM, DELIBERATELY MATCHED, AND SIZED BY THE COLD END.\\n"
    "\\n"
    "  LEG N   C1 100 uF non-polar into R_IN %s (a virtual earth, so the load is R_IN\\n"
    "          exactly)                                   f_c = %.3f Hz\\n"
    "  LEG P   C2 22 nF film into R_BP + (R_A||R_B) = %s  f_c = %.3f Hz\\n"
    "\\n"
    "MATCHING IS WHAT MATTERS, NOT THE ABSOLUTE VALUE. A corner mismatch between the legs\\n"
    "converts signal to COMMON MODE, which the ADC rejects; it does not create a differential\\n"
    "error. At 20 Hz the two legs sit at %.2f and %.2f degrees, a %.2f degree difference =\\n"
    "%.2f %% CM conversion. That is why two wildly different capacitor TYPES are acceptable\\n"
    "in the two legs, which would otherwise look like a defect.\\n"
    "\\n"
    "COLD IS THE SIZING AXIS, NOT DC BIAS. These capacitors see %.2f V and ~0 V respectively\\n"
    "and no signal voltage worth naming above the corner, so the power sheet's DC-BIAS\\n"
    "derating discipline does not bite here -- but the -20 degC decree does, and a non-polar\\n"
    "aluminium part is where it bites. Stacking -25 %% cold on -20 %% tolerance:\\n"
    "          C1 100 uF -> %.0f uF worst case  ->  f_c = %.2f Hz\\n"
    "  At 20 Hz that is still only %.3f dB of amplitude and %.1f degrees of phase, and the\\n"
    "  AK5574's own digital HPF (HPFE strapped on, pin 44) sits above it regardless.\\n"
    "  SPECIFY C1 BY ITS LOW-TEMPERATURE IMPEDANCE RATIO, not just its capacitance -- that\\n"
    "  is the parameter the -20 degC number comes from and it is the one that varies most\\n"
    "  between otherwise identical-looking parts.\\n"
    "\\n"
    "GROUP DELAY: a 1st-order HPF at %.2f Hz has tau = %.2f ms at 20 Hz. Irrelevant in\\n"
    "absolute terms; what would matter on a 12-channel crossover is CHANNEL-TO-CHANNEL\\n"
    "mismatch, and all four channels take their corner from the same two part values, so\\n"
    "+/-20 %% spread gives +/-%.0f us between channels -- three orders below the DSP's own\\n"
    "delay resolution and far below any inter-channel effect."
) % (rtxt(R_IN), FC_N, rtxt(R_BP + RA_PAR), FC_P,
     hpf_phase(FC_N, 20), hpf_phase(FC_P, 20), abs(hpf_phase(FC_N, 20) - hpf_phase(FC_P, 20)),
     100 * abs(math.radians(hpf_phase(FC_N, 20) - hpf_phase(FC_P, 20))),
     BIAS_V, C1 * COLD_DERATE * 0.8 * 1e6, FC_N_COLD,
     20 * math.log10(1 / math.sqrt(1 + (FC_N_COLD / 20) ** 2)), hpf_phase(FC_N_COLD, 20),
     FC_N, 1e3 / (2 * math.pi * FC_N) / (1 + (20 / FC_N) ** 2),
     1e6 * (1 / (2 * math.pi * FC_N * 1.2) - 1 / (2 * math.pi * FC_N * 0.8)) / (20 / FC_N) ** 2)

NOTE8 = (
    "THE AMPLIFIER IS AN F38 LINE (F52). Its PN is not pinned; its SELECTION GATE is, as\\n"
    "three inequalities, so the moment a datasheet arrives the answer is arithmetic. The\\n"
    "SOIC-8 dual pinout and land pattern are already committed -- every candidate uses them.\\n"
    "\\n"
    "GATE 1 -- NOISE, and it is the binding one.\\n"
    "  What arrives here is already noisy: the INA1650 contributes %.1f nV/rtHz (%.2f uVrms\\n"
    "  20 Hz-20 kHz, SBOS818B) and the attenuator's %.1f kOhm per-leg Thevenin adds %.1f,\\n"
    "  for %.1f nV/rtHz and an SNR of %.1f dB at the receiver's output.\\n"
    "  COMPARE THAT AGAINST THE RIGHT ADC NUMBER. It is NOT the 112 dB S/(N+D) figure -- that\\n"
    "  is measured at -1 dBFS and INCLUDES DISTORTION, so setting a noise budget against it\\n"
    "  compares a noise figure to a noise-plus-distortion one. The noise number is DYNAMIC\\n"
    "  RANGE / S-N (A-wtd), %s. So the front end sits ~%.0f dB ABOVE the converter's own floor\\n"
    "  and THE FRONT END, NOT THE ADC, SETS THIS SIGNAL PATH'S NOISE. That does not relax the\\n"
    "  budget below -- it tightens the argument for it: every dB this stage adds lands on the\\n"
    "  term that already dominates, with no converter headroom to absorb it.\\n"
    "  This stage adds sqrt( N_res^2 + (NG_N^2 + 1) x en^2 ), N_res = %.2f nV/rtHz:\\n"
    "     en = 3 nV/rtHz  ->  %.1f total  ->  +%.2f dB\\n"
    "     en = 5          ->  %.1f        ->  +%.2f dB\\n"
    "     en = 7          ->  %.1f        ->  +%.2f dB\\n"
    "     en = 12         ->  %.1f        ->  +%.2f dB\\n"
    "  REQUIRE en <= %.1f nV/rtHz at 1 kHz (2.0 dB); TARGET <= 5 (%.2f dB).\\n"
    "  THE (NG_N^2 + 1) FACTOR IS THE COST OF GAIN 0.5 FROM A UNITY SOURCE: leg N's noise\\n"
    "  gain is %.1f while its signal gain is 0.5. Nothing in the topology avoids it -- every\\n"
    "  alternative tried (both legs from the /2 tap; cascaded inverters) is WORSE, at 5x and\\n"
    "  13x en^2 against this arrangement's %.2fx.\\n"
    "\\n"
    "GATE 2 -- INPUT COMMON MODE, AND IT IS WHY THIS IS NOT AN OPA1656.\\n"
    "  Leg P is a FOLLOWER, so its (+) input SWINGS: %.2f to %.2f V on a 5 V rail. The\\n"
    "  OPA1656 already on this board specifies VCM only to (V+) - 2.25 V = %.2f V (SBOS901C)\\n"
    "  -- it clears the BIAS point by %.0f mV and FAILS the positive signal peak by %.0f mV.\\n"
    "  A part whose VCM stops 2.25 V below the rail cannot follow a mid-rail signal on 5 V.\\n"
    "  That is the specific reason, with a number, behind 'not an OPA1656', and it is a\\n"
    "  property of leg P alone -- leg N, whose inputs both sit at %.2f V, would be fine.\\n"
    "  REQUIRE VCM to include %.2f V at V+ = 5 V, i.e. rail-to-rail or near-RRI input.\\n"
    "  Output only needs %.2f..%.2f V, so RAIL-TO-RAIL OUTPUT IS *NOT* REQUIRED -- the\\n"
    "  differential topology bought that back, and it widens the candidate set considerably.\\n"
    "  Also REQUIRE CMOS/FET input: R_BP is %s, and a bipolar 1 nA input current would put\\n"
    "  %.0f mV of offset on AINnP where a 10 pA CMOS part puts %.0f uV.\\n"
    "\\n"
    "  WHY THE SUPPLY IS SINGLE +5V_A AND NOT +/-13V5_A, STATED HERE BESIDE THE PART CHOICE\\n"
    "  BECAUSE IT IS THE LOAD-BEARING PREMISE OF THE EXCLUSION ABOVE: an amplifier powered from\\n"
    "  the SAME NET that feeds the AK5574's AVDD physically cannot drive an ADC pin past\\n"
    "  AVDD + 0.3 V. Abs-max compliance is STRUCTURAL, not analytical -- there is no sequencing\\n"
    "  order, no fault and no start-up transient that can defeat it, because a rail cannot skew\\n"
    "  against itself. That is an M3 guarantee-by-construction and it is what pays for the VCM\\n"
    "  constraint the 5 V rail imposes. MOVING THIS STAGE ONTO +/-13V5_A 'FOR HEADROOM' WOULD\\n"
    "  DELETE THAT GUARANTEE and re-open both the clamp question in NOTE9 and this one.\\n"
    "\\n"
    "GATE 3 -- QUIESCENT CURRENT, because this stage is a NEW LOAD ON +5V_A.\\n"
    "  V-17 closed +5V_A at %.0f mA (converters only). Eight amplifiers land on top of it.\\n"
    "  +6V2_A was identified at 186 mA against the 250 mA already assumed, so the headroom\\n"
    "  is 64 mA and REQUIRE IQ <= %.1f mA per channel. Comfortable for anything in class,\\n"
    "  but it is a rail number that changed and it is recorded rather than absorbed.\\n"
    "\\n"
    "GATE 4 -- STABILITY, AND THE 10 OHM IS LOAD-BEARING FOR THE AMPLIFIER.\\n"
    "  AKM's 10 R + 100 pF is not only an antialias element: the 10 R is the ISOLATION\\n"
    "  RESISTOR that makes 100 pF a survivable load, and leg P is a UNITY-GAIN FOLLOWER,\\n"
    "  which is the least stable configuration a capacitive load can be presented to.\\n"
    "  DO NOT 'IMPROVE' THIS FILTER BY DELETING THE 10 R OR MOVING THE 100 pF AHEAD OF IT.\\n"
    "  REQUIRE unity-gain stable, specified into >= 100 pF behind 10 R.\\n"
    "  The matched %.0f kHz poles (C_F across R_F, C_P across R_B -- equal because\\n"
    "  R_A||R_B = R_F = %s) roll both legs off identically before the modulator's %.3f MHz\\n"
    "  sampling rate, and they are the reason leg P needs no feedback network of its own."
) % (INA_EN * 1e9, 1.56, RS_LEG / 1e3, math.sqrt(2) * eR(RS_LEG) * 1e9, FE_EN * 1e9, FE_SNR,
     "typ 121 dB, MIN 117 dB", 117.0 - FE_SNR, N_RES * 1e9,
     n_stage(3e-9) * 1e9, degr(3e-9), n_stage(5e-9) * 1e9, degr(5e-9),
     n_stage(7e-9) * 1e9, degr(7e-9), n_stage(12e-9) * 1e9, degr(12e-9),
     EN_GATE * 1e9, degr(5e-9), NG_N, NG_N ** 2 + 1,
     BIAS_V - V_LINE * math.sqrt(2) / 2, BIAS_V + V_LINE * math.sqrt(2) / 2, AVDD - 2.25,
     (AVDD - 2.25 - BIAS_V) * 1e3, (BIAS_V + V_LINE * math.sqrt(2) / 2 - (AVDD - 2.25)) * 1e3,
     BIAS_V, BIAS_V + V_LINE * math.sqrt(2) / 2,
     BIAS_V - V_LINE * math.sqrt(2) / 2, BIAS_V + V_LINE * math.sqrt(2) / 2,
     rtxt(R_BP), 1e-9 * R_BP * 1e3, 10e-12 * R_BP * 1e6,
     I_5VA * 1e3, IQ_GATE * 1e3, F_POLE / 1e3, rtxt(R_F), 48e3 * 128 / 1e6)

NOTE9 = (
    "F49's CLAMP INEQUALITY, REPEATED ON THE +5 V SIDE -- SAME FORM, DIFFERENT RAIL.\\n"
    "\\n"
    "WHAT CAN REACH A 5 V PART WITH MORE THAN 5 V: only the INA1650, and the fault is not\\n"
    "hypothetical -- it is NOTE3's OWN documented failure. A coil or driver failure in a\\n"
    "speaker-level install leaves %.1f Vrms at the receiver, which clips at its %.1f V rail,\\n"
    "and that rail arrives through R_IN (leg N) and R_A (leg P) at pins on +5V_A.\\n"
    "  BAV99 at each op-amp input, series R as the limiter:\\n"
    "     leg N  (%.1f - %.1f - 0.7) / %s = %.2f mA        leg P  same through %s = %.2f mA\\n"
    "     four channels, both legs:  I_inj = %.1f mA\\n"
    "  LEGAL ONLY IF THE RAIL CAN ABSORB IT. +5V_A comes from an LT3045, which SOURCES but\\n"
    "  CANNOT SINK, so the test is the rail's own quiescent load, not the diode's rating:\\n"
    "     %.1f mA quiescent  vs  %.1f mA injected   ->  clears by %.1fx\\n"
    "  This is on the sheet and not in a note file for exactly F49's reason: a future\\n"
    "  low-power revision that sleeps the converters while the inputs stay hot breaks the\\n"
    "  inequality SILENTLY, and nothing about the clamp itself would show it.\\n"
    "\\n"
    "NO CLAMP AT THE ADC PINS, AND THE REASON IS CONSTRUCTIONAL. AINnP/AINnN are driven only\\n"
    "by op-amp outputs powered from +5V_A -- THE SAME NET that feeds the AK5574's AVDD and\\n"
    "VREFH1/2. An output cannot exceed its own rail, and no sequencing skew exists between a\\n"
    "rail and itself, so 'AVDD + 0.3 V' cannot be violated by any ordering of events. Adding\\n"
    "clamps here would buy nothing and cost voltage-variable capacitance on the one node in\\n"
    "the chain where the source impedance is 10 Ohm and the CCIF criterion is listening.\\n"
    "IF THE LEVEL-SHIFT STAGE IS EVER MOVED TO ITS OWN RAIL, THIS PARAGRAPH BECOMES FALSE.\\n"
    "\\n"
    "LEG N's CLAMP SITS ON A VIRTUAL EARTH -- a node that carries no signal by definition --\\n"
    "so its junction capacitance is not merely small, it is UNMODULATED. Leg P's does see\\n"
    "signal, but from a %s source (R_A||R_B), where ~1 pF of variation is nothing at audio.\\n"
    "Contrast NOTE4, where the input-side clamps had to be biased to +/-13V5_A to get the\\n"
    "same property; here the topology hands it over for free on one leg and cheaply on the\\n"
    "other. Same mechanism, same measurement, third instance on this board."
) % (SPKR_MAX / (LINE_MAX / V_LINE), V_INA_RAIL, V_INA_RAIL, AVDD, rtxt(R_IN),
     (V_INA_RAIL - AVDD - 0.7) / R_IN * 1e3, rtxt(R_A), (V_INA_RAIL - AVDD - 0.7) / R_A * 1e3,
     I_INJ * 1e3, I_5VA * 1e3, I_INJ * 1e3, I_5VA / I_INJ, rtxt(RA_PAR))

NOTE10 = (
    "F38b -- THE DATE-CODE AXIS. THE THIRD THING AN F38 SWEEP HAS TO ASK.\\n"
    "\\n"
    "T1-104, from the same page as the circuit above: 'For products with Date Code XXXXHXX,\\n"
    "AKM recommends Figure 76 as the revised circuit example... In case the original circuit\\n"
    "example is used featuring input bias voltage of 2.5 V (Typ.), S/(N+D) performance will\\n"
    "be degrade ~6 dB.' Same PN. Same package. Same vendor. Same datasheet. DIFFERENT CORRECT\\n"
    "EXTERNAL CIRCUIT, selected by WHEN THE DIE WAS MADE -- and nothing on a BOM line carries\\n"
    "a date code, so no purchasing control exists for it. The F38 sweep gains a third\\n"
    "question after suffix (F37/F38) and manufacturer (F38a):\\n"
    "     DOES THIS PART'S RECOMMENDED APPLICATION CIRCUIT DEPEND ON A DATE CODE OR SILICON\\n"
    "     REVISION?\\n"
    "\\n"
    "THE DECISION HERE: commit to the revised network -- the %s / %s divider drawn above --\\n"
    "and DO NOT fit a DNP position across the %s leg. A stuffing option would build for\\n"
    "either revision, but it would also put an unpopulated pad on the one node whose whole\\n"
    "job is to be a precise ratio, and it hedges against parts that stopped being made in\\n"
    "October 2021. THE ASSUMPTION IS STATED SO IT IS CHECKABLE RATHER THAN SILENT: any\\n"
    "currently-orderable AK5574EN long postdates the H revision.\\n"
    "\\n"
    "AND THE ASSUMPTION IS TESTED RATHER THAN TRUSTED (M3's pattern). Two lines carry it:\\n"
    "  * RECEIVING -- date code verified >= H at first-article inspection (BRINGUP.md).\\n"
    "  * ACCEPTANCE -- a 6 dB S/(N+D) miss is bench-visible and lands outside S12's own\\n"
    "    THD+N line, so an ancient part is caught even if receiving misses it.\\n"
    "The general form, for the ledger: A PART NUMBER NAMES A DESIGN, NOT A REVISION OF IT."
) % (rtxt(RB_TOP), rtxt(RB_BOT), rtxt(RB_BOT))

NOTE11 = (
    "LEG MATCHING IS A SECOND RATIO NODE, AND UNTIL NOW IT HAD NO INEQUALITY ANYWHERE.\n"
    "Criterion 1 covered the BIAS DIVIDER. This is a different set of four resistors doing a\n"
    "different job, and NOTE5's departure from Figure 76 is what created it: AKM's two legs are\n"
    "identical, so their gains track by construction. Ours are an active inverter against a\n"
    "passive divider, and nothing makes them track except tolerance.\n"
    "\n"
    "THE RESIDUAL, WHICH IS THE NUMBER THAT BELONGS ON A SHEET -- an ACCEPTANCE TEST saying the\n"
    "design lands INSIDE the window, not a violation ratio saying the rejected alternative lands\n"
    "outside it. It also does not care whether AKM's window is DC or instantaneous (NOTE5), which\n"
    "is the property that makes it survive the datasheet re-read:\n"
    "\n"
    "    AINn = V_B - g_N.V ,   AINp = V_B + g_P.V     =>     CM residual = 1/2 (g_P - g_N).V\n"
    "\n"
    "  g_N = R_F/R_IN  -- TWO parts, so worst-case ratio error is +/-2t\n"
    "  g_P = R_B/(R_A+R_B) -- a DIVIDER, so its error is (1-ratio).2t = +/-t\n"
    "  The two legs are therefore NOT equally sensitive, which is why the budget is asymmetric:\n"
    "        |g_P - g_N|max = 1.5t        CM residual = 0.75 . t . V_pk,  V_pk = %.3f V\n"
    "\n"
    "     t = 1 %%    ->  %.1f mV residual   vs the +/-%.0f mV window  ->  clears %.1fx\n"
    "     t = 0.1 %%  ->  %.2f mV residual                             ->  clears %.0fx\n"
    "\n"
    "  THE SAME FOUR PARTS ALSO SET CHANNEL GAIN -- BUT THAT IS *NOT* A SECOND REASON TO BUY\\n"
    "  0.1 %% PARTS, AND SAYING SO WOULD WEAKEN THE ARGUMENT RATHER THAN STRENGTHEN IT (C4).\\n"
    "  Differential gain is (g_P + g_N), nominal 1.000, worst-case error +/-1.5t:\\n"
    "        %.2f dB at t = 1 %%      %.3f dB at t = 0.1 %%\\n"
    "  Two things swamp it:\\n"
    "    * THE CONVERTER IS 4x WORSE THAN THE RESISTORS. AK5574 INTERCHANNEL GAIN MISMATCH is\\n"
    "      0 dB typ / **0.5 dB MAX** (p.9, figure read). Taking the resistor term from 0.13 dB\\n"
    "      to 0.013 dB improves a contributor that is already a quarter of one you cannot buy\\n"
    "      your way out of.\\n"
    "    * CHANNEL GAIN IS TRIMMABLE AND CM RESIDUAL IS NOT. This is an ADAU1466 with\\n"
    "      per-channel gain in the signal flow: ONE input-gain calibration removes the\\n"
    "      resistor term and the converter term TOGETHER. Nothing in firmware removes\\n"
    "      %.1f mV of common-mode excursion at the ADC pins.\\n"
    "  SO THE PART GRADE RESTS ON THE CM RESIDUAL ALONE, where 1 %% clears 5.2x and 0.1 %%\\n"
    "  clears 52x. The gain figure is recorded as WHAT THE DSP TRIM IS FOR. Stating it as a\\n"
    "  second reason would make two arguments look mutually reinforcing when only one is\\n"
    "  load-bearing -- and a reader who checks the weaker one may discount both.\\n"
    "\\n"
    "  GAP, SAME SHAPE AS THE CROSSTALK ONE ABOVE: S12 has NO inter-channel gain-matching\\n"
    "  criterion either. If it is a product property it wants a line; if it is trimmed at\\n"
    "  calibration then the criterion belongs to THE CALIBRATION STEP rather than the board.\\n"
    "  That is a decision to be made rather than inherited, and it is the operator's.\\n"
    "\\n"
    "  BOM CONSEQUENCE, in F9's currency and for F9's reason: R_A/R_B are EQUAL VALUES and want a\n"
    "  MATCHED PAIR (an array element pair, ideal case); R_IN/R_F are a 2:1 RATIO and want a\n"
    "  ratio-matched pair or 0.1 %% discretes. As with F9 the specification is MATCHING AND\n"
    "  TRACKING, not absolute tolerance -- and tracking is again the half discretes cannot buy at\n"
    "  any price across the -20..+70 degC decree.\n"
    "\n"
    "  1 %% PARTS ARE LEGAL HERE (%.1fx) and this is not an argument that they are not. It is an\n"
    "  argument that the number exists, is %.1f mV, and moves if anyone re-values these four."
) % (SE_PK, cm_resid(0.01) * 1e3, WIN_HALFWIDTH * 1e3, WIN_HALFWIDTH / cm_resid(0.01),
     cm_resid(0.001) * 1e3, WIN_HALFWIDTH / cm_resid(0.001),
     20 * math.log10(1 + gain_err(0.01)), 20 * math.log10(1 + gain_err(0.001)),
     cm_resid(0.01) * 1e3,
     WIN_HALFWIDTH / cm_resid(0.01), cm_resid(0.01) * 1e3)


# Adversary 010. TI raises this term in OPA320 7.3.8 and then gets its own worked example
# wrong, so the mechanism is taken and the number is computed here.
def rs_err(rl):  return R_S / (rl + R_S)

NOTE12 = (
    "R_S FORMS A DIVIDER WITH THE CONVERTER'S INPUT RESISTANCE. THE GAIN ERROR IS REAL,\n"
    "SMALL, IN THE SAFE DIRECTION -- AND IT DOUBLES IF ANYONE RETUNES R_S UPWARD.\n"
    "\n"
    "  The 10R isolation resistors above are not free. Each forms a voltage divider with\n"
    "  whatever shunts the load capacitance, and here that shunt is the AK5574's own input\n"
    "  resistance -- 3.0 / 3.6 / 4.2 kOhm min/typ/max (p.9, figure read).\n"
    "\n"
    "      error = R_S / (R_L + R_S),  R_S = 10R\n"
    "        R_L 3.0k (min)   %.4f %%   %+.4f dB\n"
    "        R_L 3.6k (typ)   %.4f %%   %+.4f dB\n"
    "        R_L 4.2k (max)   %.4f %%   %+.4f dB\n"
    "        bound on channel-to-channel spread   %.4f %%\n"
    "\n"
    "  IT ATTENUATES, so headroom GROWS rather than shrinks -- negligible against the\n"
    "  %.1f %% FS margin, and %.0fx inside the converter's own 0.5 dB interchannel gain\n"
    "  mismatch. NOTE WHAT THE SPREAD FIGURE IS: it is the min-to-max PART bound, so it\n"
    "  BOUNDS channel-to-channel mismatch rather than predicting it -- channels inside one\n"
    "  device track far better than the datasheet's production window.\n"
    "\n"
    "  THE REASON IT IS WRITTEN DOWN AT ALL: TI's own recommendation is R_S = 10 to 20 Ohm,\n"
    "  and AT 20R THE ERROR IS %.4f %% -- it DOUBLES, still inside TI's advice. This is the\n"
    "  term that gets silently doubled by someone tuning the filter who never computed it.\n"
    "  DO NOT RAISE R_S WITHOUT RE-RUNNING THIS LINE.\n"
    "\n"
    "  TWO VENDORS CONVERGE ON 10R FROM OPPOSITE ENDS OF THE INTERFACE -- AKM specifies it\n"
    "  in its own ADC-pin network, TI recommends 10-20R for capacitive-load isolation. That\n"
    "  agreement is the cheapest defence of a part that looks deletable.\n"
    "\n"
    "  AND DO NOT COPY TI'S WORKED EXAMPLE, IT IS INTERNALLY INCONSISTENT (adversary 010,\n"
    "  arithmetic confirmed here): 7.3.8 states 0.2 %% at R_L = 10k with R_S = 20R -- correct,\n"
    "  20/10020 = 0.1996 %% -- then states the error 'increases to 7.5 %%' at R_L = 600R.\n"
    "  But 20/620 = %.4f %%. 7.5 %% would need R_S = %.1f Ohm. Both examples cannot hold at\n"
    "  R_S = 20R. USE THE FORMULA, NOT THE DATASHEET'S NUMBER.\n"
) % (rs_err(R_ADC[0]) * 100, 20 * math.log10(1 - rs_err(R_ADC[0])),
     rs_err(R_ADC[1]) * 100, 20 * math.log10(1 - rs_err(R_ADC[1])),
     rs_err(R_ADC[2]) * 100, 20 * math.log10(1 - rs_err(R_ADC[2])),
     (rs_err(R_ADC[0]) - rs_err(R_ADC[2])) * 100,
     (1 - TARGET / FS_MIN) * 100,
     0.5 / abs(20 * math.log10(1 - (rs_err(R_ADC[0]) - rs_err(R_ADC[2])))),
     20.0 / (R_ADC[1] + 20.0) * 100,
     20.0 / 620.0 * 100, 600.0 * 0.075 / (1 - 0.075))



NOTE13 = (
    "AK5574 MODE CONFIGURATION: ONE SENTENCE GOVERNS ALL OF IT, AND IT IS NOT WHERE\n"
    "YOU WOULD LOOK. THE PART READS EXACTLY ONE MODE PIN.\n"
    "\n"
    "  AK5574 p.56, 'Operation Mode Control', VERBATIM:\n"
    "    'In serial control mode, register settings are prioritized so that ALL PIN\n"
    "     SETTINGS EXCEPT THE MSN PIN SETTING ARE IGNORED.'\n"
    "\n"
    "  WE RUN I2C = SERIAL CONTROL MODE. SO:\n"
    "    MSN (24)   REAL. Selects SLAVE. The one honoured mode pin -- and the one that\n"
    "               matters most, because F65's autonomous LRCK phase-detect self-reset\n"
    "               EXISTS ONLY IN SLAVE MODE.\n"
    "    LDOE (45)  REAL. No register equivalent -- selects the internal 1.8 V LDO.\n"
    "    PDN (20)   REAL. Hardware reset, not a mode pin.\n"
    "    DIF1-0 (37,38) - TDM1-0 (39,40) - DP (43) - HPFE (44) - SD (36) - SLOW (35)\n"
    "    ODP (46)   ALL INERT. The part does not read them. They are set CONSISTENT\n"
    "               with the register values -- NOT to select them. F28 wants every pin\n"
    "               at a defined level, and consistency is cheap insurance for a control\n"
    "               mode we never use. DO NOT READ THEM AS CONFIGURATION.\n"
    "\n"
    "  HOW THIS WAS FOUND, BECAUSE THE SEARCH ORDER IS THE LESSON: p.46 says the ODP\n"
    "  pin is ignored in serial mode. That INSTANCE was read three times and treated as\n"
    "  a quirk of ODP. THE RULE IS TEN PAGES EARLIER, IN THE SECTION ABOUT CONTROL MODE\n"
    "  RATHER THAN THE SECTION ABOUT THE FUNCTION. Reading about the thing found the\n"
    "  exception; reading about the MODE found the rule. (Adversary 028.)\n"
    "\n"
    "  CONSEQUENCE FOR THE RECORD: the DIF strap changed TWICE (F67, F69) and BOTH\n"
    "  CHANGES WERE FUNCTIONALLY INERT. F67 was NOT a [HARD] violation in copper -- the\n"
    "  pin selects nothing. It was an ANNOTATION asserting a function the pin does not\n"
    "  perform, which is real but a different defect.\n"
    "\n"
    "  F67/F69 -- THE DIF STRAPS WERE WRONG, AND THE FIX ITSELF NEEDED A SECOND PASS.\n"
    "  THIS LINE HAS NOW CHANGED TWICE. Reading it, distrust it and check the table.\n"
    "\n"
    "  Table 9 rows 24-27 (TDM128, slave, p.36 @190dpi) -- DIF1-0 selects BOTH the word\n"
    "  length AND the justification, and the LRCK EDGE moves with it:\n"
    "     00  24-bit MSB   LRCK rising      10  32-bit MSB   LRCK RISING\n"
    "     01  24-bit I2S   LRCK falling     11  32-bit I2S   LRCK falling\n"
    "\n"
    "  WAS 00 = 24-bit MSB. S4 [HARD] REQUIRES 32-BIT SLOTS, so 00 was a violation in\n"
    "  copper. But S4 CONSTRAINS WORD LENGTH AND IS SILENT ON JUSTIFICATION -- rows 10\n"
    "  AND 11 BOTH SATISFY IT. The first fix took 11 (I2S) without a tiebreaker, which\n"
    "  was correct against the decree and UNFORCED. The tiebreaker is this:\n"
    "\n"
    "     AK4458 00H DIF2-0 DEFAULT = 110 = 32-BIT MSB JUSTIFIED, in AKM's own prose\n"
    "     (AK4458 p.75, 190 dpi: 'Default value is 110 (Mode 6: 32-bit MSB justified)').\n"
    "\n"
    "  SO THE BOARD RUNS 32-BIT MSB-JUSTIFIED ON ALL THREE CONVERTER LINKS, and the\n"
    "  AK5574 takes ROW 26, DIF1-0 = 10, LRCK RISING EDGE.\n"
    "\n"
    "  WHY DEFAULT-MATCHING IS THE RIGHT TIEBREAKER AND NOT MERE CONVENIENCE: PDN\n"
    "  RESTORES DEFAULTS (AK5574 Note 26), so every power cycle re-imposes them. Where a\n"
    "  requirement is SILENT, choosing the reset default as the operating value makes\n"
    "  each restore BENIGN instead of a fault. It is S7.4's zero-energy logic applied to\n"
    "  configuration: THE DE-ENERGISED STATE SHOULD BE THE CORRECT STATE. It also\n"
    "  shrinks F66's boot-write set rather than growing it.\n"
    "\n"
    "  BOTH DACs THEN NEED NO DIF WRITE AT ALL -- but they DO need 00H written anyway,\n"
    "  because AK4458 RSTN DEFAULTS TO 0 = RESET: the DACs BOOT HELD IN RESET. Writing\n"
    "  00H = 0x0D sets RSTN=1 and preserves the MSB default in one access.\n"
    "\n"
    "  AND THE DSP SIDE IS THE OTHER HALF OF EVERY ONE OF THESE. LRCK is an INPUT here\n"
    "  (Table 9 I/O column = I, slave). A DIF mismatch against the ADAU1466's port is\n"
    "  TWO faults at once -- a one-BICK word shift AND an inverted frame reference, i.e.\n"
    "  CHANNELS IN THE WRONG SLOTS, not a subtle level error. THE DSP'S SDATA_IN0/OUT0/\n"
    "  OUT1 MUST BE CONFIGURED MSB-JUSTIFIED TO MATCH. That is firmware and it is NOT\n"
    "  YET WRITTEN DOWN ANYWHERE -- REQUIREMENTS S4 never states a justification.\n"
    "\n"
    "  REQUIRED WRITES, REVISED (supersedes 0x37):\n"
    "     AK5574  02H = 0x35   CKS 0110 | DIF1-0 = 10 | HPFE 1\n"
    "     AK5574  03H = 0x20   TDM1-0 = 01 (TDM128)\n"
    "     AK4458  00H = 0x0D   RSTN 1 | DIF2-0 = 110 (unchanged from default)\n"
    "\n"
    "  REJECTED, RECORDED SO IT STAYS RE-OPENABLE (M12): Table 5 CKS3-0 = 1111 is an\n"
    "  AUTO clock mode covering 8 kHz-768 kHz, which would cover us without an explicit\n"
    "  commitment. NOT TAKEN, and the reason is F65 rather than ignorance: an auto mode\n"
    "  must RE-detect, and a transient LRCK disturbance could re-detect into a DIFFERENT\n"
    "  mode. Under an explicit mode the part can only resynchronise phase within the\n"
    "  mode it was told. DETERMINISM IS THE REASON.\n"
)

_NOTE_ORDER = [NOTE1, NOTE2, NOTE3, NOTE4, NOTE5, NOTE6,
               NOTE7, NOTE8, NOTE9, NOTE10, NOTE11, NOTE12, NOTE13]



def note_extent(txt):
    """Measured extent of a note. Splits on the LITERAL escape, which is what the file holds."""
    lines = txt.split(ESC)
    return max(len(l) for l in lines) * 0.85, len(lines) * 1.9    # 1.27 mm font, measured
ESC = chr(92) + "n"          # the literal two-character escape KiCad text fields carry
# A note authored with real newlines would break the s-expression AND measure as one huge
# line, silently blowing the page. Normalise once, here, rather than relying on every note
# being escaped identically by hand -- that assumption already failed once.
_NOTE_ORDER = [t.replace(chr(10), ESC) for t in _NOTE_ORDER]
# NOTES ARE STACKED, NOT PLACED. Hard-coded y positions are the same defect as a hard-coded
# page size (F53) one level down: NOTE5 grew while answering a review, silently overran NOTE6,
# and the overlap showed up only as text going missing from the PDF. Height is measured and
# the next note starts below it -- a note can now grow freely and the column follows.
def _stack(notes, x0, y0, gap=12.0, hmax=1000.0):
    out, x, y = [], x0, y0
    for t in notes:
        w, h = note_extent(t)
        if y + h > hmax and y > y0:            # start a new column rather than run off
            x, y = x + w + 30.0, y0
        out.append((x, y, t)); y += h + gap
    return out
NOTES = _stack(_NOTE_ORDER, 650.0, 40.0)

body  = [place(*p) for p in PLACE]
for i, (nx, ny, txt) in enumerate(NOTES):
    body.append(f'\t(text "{txt}"\n\t\t(exclude_from_sim no)\n\t\t(at {snap(nx)} {snap(ny)} 0)\n'
                f'\t\t(effects (font (size 1.27 1.27)) (justify left top))\n'
                f'\t\t(uuid "{u(f"n{i}")}")\n\t)')

# ---------------------------------------------------------------- the page must CONTAIN the sheet
# F53: every sheet on this project declared (paper "A3") -- 420 x 297 mm -- while its content ran
# to a canvas several times that. Eeschema draws outside the frame quite happily, so nothing ever
# looked wrong on screen; the PDF export CLIPS TO THE PAGE, so the exported schematic silently
# dropped whole blocks and EVERY on-sheet note. The earlier proof "PDF renders 10 pages" tested
# traversal and was read as if it tested content.
# The fix is not a bigger constant -- it is that the page is DERIVED FROM THE CONTENT and asserted,
# so a sheet can never again outgrow its paper without the build stopping.
_X = [lx for lx, _ in LABELS] + [p[2] for p in PLACE]
_Y = [ly for _, ly in LABELS] + [p[3] for p in PLACE]
for _nx, _ny, _t in NOTES:
    _w, _h = note_extent(_t); _X.append(_nx + _w); _Y.append(_ny + _h)
PAPER_W = math.ceil((max(_X) + 25) / 10) * 10
PAPER_H = math.ceil((max(_Y) + 25) / 10) * 10
assert PAPER_W <= 1200 and PAPER_H <= 1200, (
    f"page {PAPER_W} x {PAPER_H} mm exceeds KiCad's user-page limit -- split the sheet")
assert min(_X) >= 0 and min(_Y) >= 0, "content at negative coordinates falls off the page origin"

sch = f'''(kicad_sch
\t(version {VER})
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{SHEET_UUID}")
\t(paper "User" {PAPER_W:.1f} {PAPER_H:.1f})
\t(title_block
\t\t(title "ODSP-12 :: Analog in -- 4 differential, dual range, into AK5574")
\t\t(date "2026-08-16")
\t\t(rev "A")
\t\t(comment 1 "ODSP12-MB-A")
\t\t(comment 2 "AINn maps to TDM slot n, no remapping -- S10 [HARD]")
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
print(f"  {len(PLACE)} device instances, all pins dispositioned")
print(f"  {len(LABELS)} global labels, no collisions")
print(f"  page {PAPER_W:.0f} x {PAPER_H:.0f} mm, derived from content and asserted (F53)")
print(f"  gain plan: Rtop {rtxt(RTOP)} / Rbot {rtxt(RBOT)} / Rspk {rtxt(RSPK)}")
print(f"    line    {LINE_MAX} Vrms -> {V_LINE:.4f} Vrms ({100*V_LINE/FS_MIN:.1f}% FSmin, {100*V_LINE/FS_RMS:.1f}% typ)")
print(f"    speaker {SPKR_MAX} Vrms -> {V_SPKR:.4f} Vrms ({100*V_SPKR/FS_MIN:.1f}% FSmin, {100*V_SPKR/FS_RMS:.1f}% typ)")
print(f"    Zin diff (line) = {ZIN:.0f} kOhm")
