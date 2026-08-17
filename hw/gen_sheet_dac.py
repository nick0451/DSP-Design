# Generates 07_dac_a.kicad_sch and 08_dac_b.kicad_sch from ONE parameterised pass.
#
# Two sheets rather than one instantiated twice, per STATE.md's sheet plan: S10's [HARD]
# no-remapping rule wants the channel numbers written LITERALLY, not derived from an instance
# path. So the generator is shared and the CHANNEL NUMBERS are the parameter.
#
# ANCHORS (all T1):
#   AK4458 full scale = 2.8 Vpp diff = 0.99 Vrms at AVDD 5 V         (V-05)
#   Target             = 4.5 Vrms [HARD]                              (S6.2)
#   -> stage gain      = 4.55x = 13.2 dB, derived from BOTH verified endpoints
#   OPA1656 output swing = (V-)+0.25 .. (V+)-0.25 -> +/-13.25 V       (V-06)
#   OPA1656 input abs max = (V-)-0.5 .. (V+)+0.5  -> +/-14.0 V        (V-06 / F48 postscript)
import os, re, sys, uuid, math

HW = os.path.dirname(os.path.abspath(__file__))
NS = uuid.UUID("0d5f1a00-0000-4000-8000-0000000000ff")
ROOT_UUID = "0d5f1a00-0000-4000-8000-000000000001"
VER = "20260306"
GRID = 1.27
def snap(v): return round(v / GRID) * GRID

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
    if not pins:
        ext = re.search(r'\(extends "([^"]+)"', blk)
        assert ext, f"{name}: ZERO pins and no (extends ...)"
        pblk, pins = extract(path, ext.group(1))
        blk = pblk.replace(f'(symbol "{ext.group(1)}"', f'(symbol "{name}"', 1)
        blk = blk.replace(f'(symbol "{ext.group(1)}_', f'(symbol "{name}_')
    assert pins, f"{name}: extracted ZERO pins"
    return blk, pins

import importlib.util
_spec = importlib.util.spec_from_file_location("gs", os.path.join(HW, "lib", "gen_symbols.py"))
gs = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(gs)

def geometry(pinlist, unit):
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
    "ODSP12:AK4458":        (PROJ, "AK4458"),
    "ODSP12:OPA1656":       (PROJ, "OPA1656"),
    "ODSP12:MUTE_PHOTOMOS": (PROJ, "MUTE_PHOTOMOS"),
    "ODSP12:MUTE_DEPFET":   (PROJ, "MUTE_DEPFET"),
    "Device:R":             (STOCK + "/Device.kicad_sym", "R"),
    "Device:C":             (STOCK + "/Device.kicad_sym", "C"),
}
DEFS, PINGEO = {}, {}
for libid, (path, nm) in SRC.items():
    blk, pins = extract(path, nm)
    base = libid.split(":")[1]
    blk = blk.replace(f'(symbol "{nm}_', f'(symbol "{base}_')
    DEFS[libid] = blk.replace(f'(symbol "{nm}"', f'(symbol "{libid}"', 1)
    PINGEO[libid] = {p[0]: (p[1], p[2]) for p in pins}

GND = "GND"; NC = None

# ---------------------------------------------------------------- gain, derived
FS_RMS  = 2.8 / (2 * math.sqrt(2))        # 0.9899 Vrms differential, V-05
TARGET  = 4.5                             # [HARD], S6.2
GAIN    = TARGET / FS_RMS
E96 = [100,102,105,107,110,113,115,118,121,124,127,130,133,137,140,143,147,150,154,158,162,165,
       169,174,178,182,187,191,196,200,205,210,215,221,226,232,237,243,249,255,261,267,274,280,
       287,294,301,309,316,324,332,340,348,357,365,374,383,392,402,412,422,432,442,453,464,475,
       487,499,511,523,536,549,562,576,590,604,619,634,649,665,681,698,715,732,750,768,787,806,
       825,845,866,887,909,931,953,976]
def e96(t):
    b = None
    for dec in range(-1, 7):
        for m in E96:
            v = m * (10 ** dec) / 10.0
            if b is None or abs(math.log(v / t)) < abs(math.log(b / t)): b = v
    return b
def rtxt(r): return f"{r/1e6:g}M" if r >= 1e6 else (f"{r/1e3:g}k" if r >= 1e3 else f"{r:g}R")
def e96_up(t):
    """Smallest E96 value >= t. Used where the spec is a FLOOR, not a target."""
    best = None
    for dec in range(-1, 7):
        for m in E96:
            v = m * (10 ** dec) / 10.0
            if v >= t * (1 - 1e-12) and (best is None or v < best): best = v
    return best
RIN = e96(2.2e3)
# 4.5 Vrms is a [HARD] FLOOR, not a target, so Rf ROUNDS OUTWARD -- the same rule CLAUDE.md
# S7 states for grid quantization, applied to a resistor. Nearest-E96 gave 10k -> 4.479 Vrms,
# which is 0.04 dB SHORT and would have failed the acceptance line by rounding.
RF  = e96_up(RIN * GAIN)
GAIN_ACT = RF / RIN
VOUT_ACT = FS_RMS * GAIN_ACT
FC = 1.0 / (2 * math.pi * RF * 150e-12)             # feedback pole with 150 pF
RBO = e96(10.0)                                      # build-out after the mute series element

# ---------------------------------------------------------------- AK4458 mapping
# S4 [HARD]: 6 channels per device, slots 7-8 RESERVED. The device's own outputs are
# L1 R1 L2 R2 L3 R3 L4 R4; we use the first six and leave L4/R4 OPEN -- T1-52 is explicit
# that unused AOUT pins must be OPEN, not grounded, which is the opposite of the unused
# DIGITAL inputs on the same part.
AOUT_PINS = [("L1", 18, 19), ("R1", 23, 22), ("L2", 24, 25), ("R2", 29, 28),
             ("L3", 32, 33), ("R3", 37, 36)]
UNUSED_AOUT = [38, 39, 43, 42]                       # L4 P/N, R4 P/N -> OPEN

def build(sheet_file, title, dev_idx, chan_base, port, i2c_addr_strap):
    DEST = os.path.join(HW, sheet_file)
    SHEET_UUID = str(uuid.uuid5(NS, "sheet:" + sheet_file))
    SHEET_SYM_UUID = str(uuid.uuid5(NS, "inst:" + sheet_file))
    def u(t): return str(uuid.uuid5(NS, f"dac{dev_idx}:" + t))

    LABELS = {}
    def emit_label(net, lx, ly, rot, just, uid):
        prev = LABELS.get((lx, ly))
        assert prev is None or prev == net, (
            f"LABEL COLLISION at ({lx},{ly}): '{prev}' and '{net}' would be shorted.")
        LABELS[(lx, ly)] = net
        return [f'\t(global_label "{net}"', '\t\t(shape bidirectional)',
                f'\t\t(at {lx} {ly} {rot})', '\t\t(fields_autoplaced yes)',
                f'\t\t(effects (font (size 1.27 1.27)) (justify {just}))',
                f'\t\t(uuid "{uid}")', '\t)']

    def place(ref, libid, x, y, val, nets, unit=1, geo=None):
        x, y = snap(x), snap(y)
        geo = geo if geo is not None else PINGEO[libid]
        missing = set(geo) - set(nets); extra = set(nets) - set(PINGEO[libid])
        assert not missing, f"{ref}: pins with no disposition (F28): {sorted(missing)}"
        assert not extra, f"{ref}: nets on non-existent pins {sorted(extra)}"
        out = ['\t(symbol', f'\t\t(lib_id "{libid}")', f'\t\t(at {x} {y} 0)', f'\t\t(unit {unit})',
               '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)', '\t\t(dnp no)',
               f'\t\t(uuid "{u("i"+ref+str(unit))}")',
               f'\t\t(property "Reference" "{ref}" (at {x} {y-22} 0) (effects (font (size 1.27 1.27))))',
               f'\t\t(property "Value" "{val}" (at {x} {y-19} 0) (effects (font (size 1.27 1.27))))',
               '\t\t(instances', '\t\t\t(project "ODSP12-MB"',
               f'\t\t\t\t(path "/{ROOT_UUID}/{SHEET_SYM_UUID}" (reference "{ref}") (unit {unit}))',
               '\t\t\t)', '\t\t)', '\t)']
        for num, (sx, sy) in geo.items():
            lx, ly = snap(x + sx), snap(y - sy)
            if nets[num] is None:
                out.append(f'\t(no_connect (at {lx} {ly}) (uuid "{u("nc"+ref+str(unit)+num)}"))')
                continue
            rot = 180 if sx < 0 else 0
            just = "right" if sx < 0 else "left"
            out += emit_label(nets[num], lx, ly, rot, just, u("l"+ref+str(unit)+num))
        return "\n".join(out)

    PLACE = []
    D1, D2 = geometry(gs.AK4458, 1), geometry(gs.AK4458, 2)
    assert set(D1) | set(D2) == set(PINGEO["ODSP12:AK4458"]), "AK4458 units do not reconstruct"
    assert not (set(D1) & set(D2)), "AK4458 pin in two units"

    dac = {}
    for k, (_nm, pp, pn) in enumerate(AOUT_PINS):
        ch = chan_base + k
        dac[str(pp)] = f"DAC{ch}_P"; dac[str(pn)] = f"DAC{ch}_N"
    for pnum in UNUSED_AOUT: dac[str(pnum)] = NC      # T1-52: OPEN, not grounded
    dac.update({
        "21": "+5V_A", "20": GND, "27": "+5V_A", "26": GND,
        "34": "+5V_A", "35": GND, "40": "+5V_A", "41": GND,
        "31": "+5V_A", "30": GND,
        "1": "MCLK_DAC", "2": port + "_BCLK", "3": port + "_LRCLK",
        "4": port + "_DATA", "5": GND, "6": GND, "7": GND,     # SDTI2-4 unused -> DVSS (T1-52)
        "8": GND, "9": GND, "10": GND,                          # DSDR3/DSDL4/DSDR4 -> DVSS
        "11": NC,                                               # DZF must be OPEN (T1-52)
        "48": f"DAC{dev_idx}_PDN_N",
        "13": "I2C0_SDA", "14": "I2C0_SCL",
        "15": i2c_addr_strap[0], "12": i2c_addr_strap[1],       # CAD0 / CAD1
        "16": GND, "17": "+3V3_D",                              # PS low + I2C high (T1-50)
        "44": "+3V3_D", "45": "+3V3_D", "46": GND, "47": f"VDD18_DAC{dev_idx}",
    })
    PLACE.append((f"U5{dev_idx}", "ODSP12:AK4458", 90, 140, "AK4458VN",
                  {k: v for k, v in dac.items() if k in D1}, 1, D1))
    PLACE.append((f"U5{dev_idx}", "ODSP12:AK4458", 90, 330, "AK4458VN",
                  {k: v for k, v in dac.items() if k in D2}, 2, D2))

    OP1, OP2, OP3 = (geometry(gs.OPA1656, i) for i in (1, 2, 3))
    assert set(OP1)|set(OP2)|set(OP3) == set(PINGEO["ODSP12:OPA1656"]), "OPA1656 units"
    assert not (set(OP1)&set(OP2)) and not (set(OP2)&set(OP3)) and not (set(OP1)&set(OP3))

    _pc = [0]
    def passive(kind, x, y, val, na, nb):
        _pc[0] += 1
        return (kind + str(500 + dev_idx*100 + _pc[0]),
                {"C": "Device:C", "R": "Device:R"}[kind], x, y, val, {"1": na, "2": nb})
    P = []
    for k in range(6):
        ch = chan_base + k
        pkg, half = k // 2, k % 2          # 3 packages, 2 amps each
        ref = f"U6{dev_idx}{pkg}"
        y = 40 + k * 62
        # difference amplifier, gain RF/RIN, differential DAC in -> single-ended out
        inv, non, out = ("2", "3", "1") if half == 0 else ("6", "5", "7")
        unit = 1 if half == 0 else 2
        geo = OP1 if half == 0 else OP2
        PLACE.append((ref, "ODSP12:OPA1656", 300, y, "OPA1656IDR", {
            inv: f"OPI{ch}_N", non: f"OPI{ch}_P", out: f"AMP{ch}_OUT"}, unit, geo))
        P += [passive("R", 200, y,      rtxt(RIN), f"DAC{ch}_N", f"OPI{ch}_N"),
              passive("R", 200, y + 14, rtxt(RIN), f"DAC{ch}_P", f"OPI{ch}_P"),
              passive("R", 240, y,      rtxt(RF),  f"OPI{ch}_N", f"AMP{ch}_OUT"),
              passive("R", 240, y + 14, rtxt(RF),  f"OPI{ch}_P", GND),
              passive("C", 270, y,      "150p",    f"OPI{ch}_N", f"AMP{ch}_OUT"),
              passive("C", 270, y + 14, "150p",    f"OPI{ch}_P", GND)]
        # --- mute: SERIES then SHUNT, in that order (S6.4 [HARD])
        PLACE.append((f"K{dev_idx}{k+1}", "ODSP12:MUTE_PHOTOMOS", 380, y, "PLACEHOLDER V-14", {
            "1": f"MUTE_LED{ch}_A", "2": "MUTE_LED_K", "3": f"AMP{ch}_OUT", "4": f"MUTED{ch}"}))
        P += [passive("R", 350, y, "1k", "MUTE_EN", f"MUTE_LED{ch}_A")]
        PLACE.append((f"Q{dev_idx}{k+1}", "ODSP12:MUTE_DEPFET", 420, y, "PLACEHOLDER V-15", {
            "1": "MUTE_BIAS_N", "2": f"MUTED{ch}", "3": GND}))
        P += [passive("R", 450, y, rtxt(RBO), f"MUTED{ch}", f"AOUT{ch}")]
    # shunt gate bias, derived from -13V5_A: rails collapse -> bias dies -> shunt CLOSES
    P += [passive("R", 200, 440, "100k", GND, "MUTE_BIAS_N"),
          passive("R", 230, 440, "100k", "MUTE_BIAS_N", "-13V5_A"),
          passive("C", 260, 440, "1uF",  "MUTE_BIAS_N", GND)]
    # op-amp power units + decoupling
    for pkg in range(3):
        ref = f"U6{dev_idx}{pkg}"
        PLACE.append((ref, "ODSP12:OPA1656", 300, 430 + pkg * 24, "OPA1656IDR",
                      {"8": "+13V5_A", "4": "-13V5_A"}, 3, OP3))
        P += [passive("C", 330 + pkg*26, 430, "100n", "+13V5_A", GND),
              passive("C", 330 + pkg*26, 450, "100n", "-13V5_A", GND)]
    P += [passive("C", 40, 470, "10uF", "+5V_A", GND), passive("C", 70, 470, "100n", "+5V_A", GND),
          passive("C", 100, 470, "10uF", "+3V3_D", GND), passive("C", 130, 470, "100n", "+3V3_D", GND),
          passive("C", 160, 470, "1uF", f"VDD18_DAC{dev_idx}", GND)]
    PLACE += P

    n_hi = chan_base + 5
    NOTE1 = (
        "OUTPUT STAGE, DERIVED FROM BOTH VERIFIED ENDPOINTS -- neither end assumed.\\n"
        "  AK4458 full scale = 2.8 Vpp differential = %.4f Vrms   (V-05, at AVDD 5 V)\\n"
        "  S6.2 [HARD]       = 4.5 Vrms before clip into 10 kOhm\\n"
        "  -> required gain  = %.3f x = %.2f dB\\n"
        "  Rin = %s, Rf = %s per leg -> ACTUAL gain %.3f x, output %.3f Vrms (%+.2f dB vs 4.5)\\n"
        "\\n"
        "V-06 CLOSES, AND THE [HARD] LINE CLEARS ON THE DATASHEET'S NUMBER:\\n"
        "  OPA1656 output swing = (V-)+0.25 .. (V+)-0.25, i.e. +/-13.25 V on +/-13V5_A rails.\\n"
        "  4.5 Vrms needs 6.36 V peak.  13.25 / 6.36 = 2.08x -> 6.4 dB of headroom.\\n"
        "  The swing spec is quoted at RL = 2 kOhm; S6.2 loads 10 kOhm, i.e. LIGHTER, so the\\n"
        "  real margin is at least this. NOT marginal, and not assumed.\\n"
        "\\n"
        "V-06 POSTSCRIPT (F48's question asked of this stage): OPA1656 input abs max is\\n"
        "  (V-)-0.5 .. (V+)+0.5 = +/-14.0 V, the same form that caught the input sheet. Here it\\n"
        "  is NOT at risk: the op-amp inputs sit inside the feedback loop, driven only by the\\n"
        "  AK4458's outputs, which are bounded by its own AVDD (5 V). THE MUTE ELEMENTS ARE\\n"
        "  DOWNSTREAM OF THE OUTPUT PIN, so no mute transient reaches an input. The one exposed\\n"
        "  pin is OUT, and its abs max is 'output short-circuit: continuous'.\\n"
        "\\n"
        "*** THE [HARD] FLOOR IS DEFENDED JOINTLY BY THREE INDEPENDENTLY-OWNED VALUES. ***\n"
        "S12 measures at the RCA, AFTER the mute series element, so the Zout divider eats from\n"
        "the same margin the gain provides. The inequality, and it must be re-fired if ANY of\n"
        "the three moves:\n"
        "      Vout(RCA) = gain x FS x  RL / (RL + Zout)   >=  4.5 Vrms,  RL = 10 kOhm (S12)\n"
        "  Owners:  (1) Rf's E96 step      (2) the build-out resistor     (3) Ron's ceiling\n"
        "  At Zout = 100 Ohm (S6.2's own ceiling): 4.524 Vrms -> +0.046 dB. CLEARS, BARELY.\n"
        "  The floor alone would tolerate Zout <= 153 Ohm; S6.2's 100 Ohm is the BINDING limit.\n"
        "  Real photoMOS Ron is 1-2 Ohm, so the LIKELY number is Zout ~ 11 Ohm -> +0.123 dB.\n"
        "  BUT THE DESIGN MUST CLEAR AT THE CEILING, NOT AT THE LIKELY VALUE.\n"
        "  THIS IS THE LINE THAT CATCHES the future 'optimise Rf back to 10k, it is within\n"
        "  tolerance' pass: at Rf = 10k the RCA sees 4.435 Vrms and the [HARD] line FAILS --\n"
        "  by arithmetic here, rather than by a failed acceptance run months later.\n"
        "\n"
        "FILTER: 150 pF across Rf gives a pole at %.0f kHz -- far above the 19+20 kHz CCIF\\n"
        "twin-tone pair S12 tests this stage with, so the criterion measures the STAGE, not the\\n"
        "filter's skirt. A pole placed for 'niceness' near 20 kHz would corrupt that measurement."
    ) % (FS_RMS, GAIN, 20*math.log10(GAIN), rtxt(RIN), rtxt(RF), GAIN_ACT, VOUT_ACT,
         20*math.log10(VOUT_ACT/4.5), FC/1e3)

    NOTE2 = (
        "MUTE: SERIES-SHUNT, AND THE FAIL-SAFE WALK IS THE WHOLE POINT (S6.4 / S7.4 [HARD]).\\n"
        "Order along the signal path is SERIES FIRST, THEN SHUNT, THEN build-out to the jack.\\n"
        "\\n"
        "  K%d1-K%d6  Form A photoMOS, ENERGISED-TO-PASS. LED from MUTE_EN through 1k.\\n"
        "  Q%d1-Q%d6  depletion pair, BACK-TO-BACK SOURCE-TO-SOURCE, gate biased off from\\n"
        "            -13V5_A through a 100k/100k divider.\\n"
        "\\n"
        "THE WALK -- each element fails safe in its OWN polarity, and the depth is the PRODUCT:\\n"
        "  * Rails collapse (crank sag, blown fuse, pulled connector -- the S7.4 cases, none of\\n"
        "    which involve the MCU):\\n"
        "      +5V_D dies  -> LED current stops  -> SERIES OPENS. Signal path broken.\\n"
        "      -13V5_A dies -> gate bias dies    -> Vgs -> 0 -> DEPLETION DEVICE CONDUCTS\\n"
        "                                        -> SHUNT CLOSES. Residual shorted to ground.\\n"
        "    NEITHER needs firmware, a sequence, or a rail that is still alive.\\n"
        "  * A SINGLE depletion FET would RECTIFY (its body diode conducts one polarity), which\\n"
        "    is why the pair is source-to-source: two body diodes back to back block both ways.\\n"
        "  * ENHANCEMENT devices are excluded BY CONSTRUCTION -- they need Vgs to conduct, so a\\n"
        "    dead rail leaves the shunt OPEN, which is the opposite of what is wanted.\\n"
        "\\n"
        "*** V-14 and V-15 ARE BOUNDED HERE, NOT CLOSED. *** K and Q are PLACEHOLDER SYMBOLS:\\n"
        "the TOPOLOGY is drawn and netlist-checkable, the PART NUMBERS are not pinned, because\\n"
        "their datasheets are not held and CLAUDE.md s8 rule 9 has no exception for a part\\n"
        "whose function is obvious. What the parts must satisfy:\\n"
        "  V-14 series Ron: Zout budget is <= 100 Ohm (S6.2). Build-out is %s, so\\n"
        "        Ron(photoMOS) <= 100 - %s = %.0f Ohm, AND its Ron must be flat with current --\\n"
        "        a resistance that varies with signal IS distortion, measured by the same CCIF\\n"
        "        criterion. THE SERIES ELEMENT IS NOW INSIDE THE OUTPUT-IMPEDANCE BUDGET; it\\n"
        "        was not when S6.2 was written.\\n"
        "  V-15 shunt Coff: off-capacitance and its VOLTAGE COEFFICIENT. This is the mechanism\\n"
        "        S12's CCIF twin-tone line exists to catch -- both 1 kHz and 20 kHz THD are\\n"
        "        blind to it.\\n"
        "  V-16 depth: DAC residual x mute attenuation x amp gain x amp mute latency. Bound,\\n"
        "        not closed: remote-out is fail-safe and drops FIRST, so the window is tens to\\n"
        "        a couple hundred ms of someone else's amplifier, and the residual is a\\n"
        "        brown-out-resetting DAC, not programme material. Bench-refined."
    ) % (dev_idx, dev_idx, dev_idx, dev_idx, rtxt(RBO), rtxt(RBO), 100 - RBO)

    NOTE3 = (
        "CHANNEL NUMBERING -- THE ONE PLACE THE IDENTITY DELIBERATELY BREAKS (F10, S10 [HARD]).\\n"
        "  This device is AK4458 #%d. Its OWN outputs are L1 R1 L2 R2 L3 R3 (slots 1-6).\\n"
        "  They carry SYSTEM channels AOUT%d..AOUT%d.\\n"
        "  AOUTn <-> (device ceil(n/6), slot ((n-1) mod 6)+1)\\n"
        "So on THIS sheet the net names and the device's own pin names do not agree, and that\\n"
        "is correct: S10 says net names follow the SYSTEM channel number, never the per-device\\n"
        "slot. Written here, at the wire, because this is the only sheet where the two differ\\n"
        "and the temptation to 'fix' the mismatch lives exactly here.\\n"
        "\\n"
        "SLOTS 7-8 RESERVED [HARD]: L4/R4 (pins 38/39/43/42) are EXPLICIT NO-CONNECTS. T1-52 is\\n"
        "counter-intuitive and specific -- unused ANALOG outputs must be left OPEN, while unused\\n"
        "DIGITAL inputs on the same part (SDTI2-4, DSDR3, DSDL4, DSDR4) must be tied to DVSS.\\n"
        "Opposite treatments, same device, and DZF must also be left open."
    ) % (dev_idx, chan_base, n_hi)

    body = [place(*p) for p in PLACE]
    for i, (nx, ny, txt) in enumerate([(560.0, 40.0, NOTE1), (560.0, 180.0, NOTE2),
                                       (560.0, 400.0, NOTE3)]):
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
\t\t(title "{title}")
\t\t(date "2026-08-16")
\t\t(rev "A")
\t\t(comment 1 "ODSP12-MB-A")
\t\t(comment 2 "AOUT{chan_base}-{n_hi} = AK4458 #{dev_idx} slots 1-6. Net names follow the SYSTEM channel -- S10 [HARD]")
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
    print(f"  {len(PLACE)} instances, all pins dispositioned; {len(LABELS)} labels, no collisions")

print(f"gain: Rin {rtxt(RIN)} / Rf {rtxt(RF)} -> {GAIN_ACT:.3f}x = {20*math.log10(GAIN_ACT):.2f} dB")
print(f"      {FS_RMS:.4f} Vrms in -> {VOUT_ACT:.3f} Vrms out (target 4.5, {20*math.log10(VOUT_ACT/4.5):+.2f} dB)")
build("07_dac_a.kicad_sch", "ODSP-12 :: DAC A -- AK4458 #1, AOUT1-6", 1, 1, "TDM_OUT0", ("+3V3_D", GND))
# CAD0 / CAD1. #1 = (0,0) -> 0x11 ... no: CAD1:CAD0 = 0:1 -> 0x11 and 1:0 -> 0x12.
# The re-emitted S9 map caught this: BOTH devices were originally handed the same strap
# pair, so #2 also answered at 0x11 -- two DACs replying together, which presents as
# "the second DAC ignores its filter config" and is a bus fault, not a config bug.
build("08_dac_b.kicad_sch", "ODSP-12 :: DAC B -- AK4458 #2, AOUT7-12", 2, 7, "TDM_OUT1", (GND, "+3V3_D"))
