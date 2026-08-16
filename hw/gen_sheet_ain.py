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
FS_RMS   = 0.56 * 5.0 / (2 * math.sqrt(2))    # 0.99 Vrms differential at the ADC
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
TARGET = 0.95 * FS_RMS
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
    "24": GND,            # MSN low = SLAVE. S3 [HARD]: the DSP owns BCLK/LRCLK.
    "20": "ADC_PDN_N", "15": GND,                          # TEST has an internal pull-down
    "31": "I2C0_SDA", "33": "I2C0_SCL", "32": GND, "34": GND,   # CAD1:CAD0 = 00 -> 0x10
    "41": GND,            # PSN low  } T1-50: I2C mode needs BOTH
    "42": "+3V3_D",       # I2C high }
    "21": GND, "22": GND, "23": GND,                       # PW0-2
    "35": GND, "36": GND, "37": GND, "38": GND,            # SLOW/SD/DIF0/DIF1
    "39": "+3V3_D", "40": GND,                             # TDM0/TDM1 -> TDM4, 32-bit
    "43": GND, "44": "+3V3_D",                             # DP off, HPFE on
    "45": "+3V3_D", "46": GND,                             # LDOE on (internal 1.8 V), ODP off
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
        "2": f"ATT{ca}_P", "4": f"ATT{ca}_N", "3": GND, "13": f"AIN{ca}_P", "12": "AGND_REF",
        "7": f"ATT{cb}_P", "5": f"ATT{cb}_N", "6": GND, "8": f"AIN{cb}_P", "9": "AGND_REF",
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
    "  Rtop = %s per leg, Rbot = %s per leg, Rspk = %s per leg (switched by K1-K4)\\n"
    "  LINE    (Rbot alone):        %.2f Vrms in -> %.3f Vrms  (%.1f%% of FS)\\n"
    "  SPEAKER (Rbot || Rspk):      %.1f Vrms in -> %.3f Vrms  (%.1f%% of FS)\\n"
    "  Zin, line mode, differential = 2 x (Rtop + Rbot) = %.0f kOhm  vs the >= 20 kOhm decree\\n"
    "\\n"
    "NOTE WHAT IS *NOT* HERE: no gain stage. That is a consequence, not an omission -- the\\n"
    "INA1650 is fixed at 1 V/V, so any topology that attenuated further would need one, and\\n"
    "every extra stage multiplies the attenuator's own noise before the ADC sees it."
) % (FS_RMS, rtxt(RTOP), rtxt(RBOT), rtxt(RSPK),
     LINE_MAX, V_LINE, 100 * V_LINE / FS_RMS, SPKR_MAX, V_SPKR, 100 * V_SPKR / FS_RMS, ZIN)

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

body  = [place(*p) for p in PLACE]
for i, (nx, ny, txt) in enumerate([(650.0, 40.0, NOTE1), (650.0, 170.0, NOTE2),
                                   (650.0, 330.0, NOTE3), (650.0, 500.0, NOTE4)]):
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
print(f"  gain plan: Rtop {rtxt(RTOP)} / Rbot {rtxt(RBOT)} / Rspk {rtxt(RSPK)}")
print(f"    line    {LINE_MAX} Vrms -> {V_LINE:.4f} Vrms ({100*V_LINE/FS_RMS:.1f}% FS)")
print(f"    speaker {SPKR_MAX} Vrms -> {V_SPKR:.4f} Vrms ({100*V_SPKR/FS_RMS:.1f}% FS)")
print(f"    Zin diff (line) = {ZIN:.0f} kOhm")
