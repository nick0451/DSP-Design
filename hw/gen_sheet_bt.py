# Generates 04_bluetooth.kicad_sch -- BM83SM1, its supply, the I2S slave port, and the
# Host-mode control plane.
#
# SOURCES: BM83 datasheet DS70005402G. Pin table Table 2-2 pp.13-15 (T1-56/T1-57, already the
# symbol's source); power supply s5.1 + pin 23; Host interface Figure 6-8 s6.6; currents
# Table 9-12 s9.
import os, re, uuid
import math

HW = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HW, "04_bluetooth.kicad_sch")
NS = uuid.UUID("0d5f1a00-0000-4000-8000-0000000000ff")
SHEET_UUID = str(uuid.uuid5(NS, "sheet:04_bluetooth.kicad_sch"))
SHEET_SYM_UUID = str(uuid.uuid5(NS, "inst:04_bluetooth.kicad_sch"))
ROOT_UUID = "0d5f1a00-0000-4000-8000-000000000001"
VER = "20260306"
GRID = 1.27
def snap(v): return round(v / GRID) * GRID
def u(t): return str(uuid.uuid5(NS, "bt:" + t))

STOCK = r"C:/Program Files/KiCad/10.0/share/kicad/symbols"
PROJ  = os.path.join(HW, "lib", "ODSP12.kicad_sym")

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
    assert pins, f"{name}: extracted ZERO pins -- regex/format mismatch, not an empty part"
    return blk, pins

# Per-unit geometry is recomputed with the SAME math gen_symbols.unit_block used, rather than
# scraped from the emitted file -- the BM83 symbol has TWO units, and placing one instance with
# all 50 pin positions would strand every unit-2 label in empty space: attached to nothing,
# present in the netlist, and invisible as an error. Same approach as gen_sheet_dsp.py.
import importlib.util
_spec = importlib.util.spec_from_file_location("gs", os.path.join(HW, "lib", "gen_symbols.py"))
gs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gs)          # re-runs the symbol assertions; a failure stops the sheet
PINS = gs.BM83

def geometry(unit):
    pins = [q for q in PINS if q[3] == unit]
    half = (len(pins) + 1) // 2
    left, right = pins[:half], pins[half:]
    rows = max(len(left), len(right))
    w, top = 63.5, (rows + 1) * 2.54 / 2
    out = {}
    for i, (num, *_r) in enumerate(left):  out[num] = (-w / 2 - 5.08, top - 2.54 * (i + 1))
    for i, (num, *_r) in enumerate(right): out[num] = (w / 2 + 5.08, top - 2.54 * (i + 1))
    return {str(k): v for k, v in out.items()}

SRC = {
    "ODSP12:BM83SM1": (PROJ, "BM83SM1"),
    "Device:R":       (STOCK + "/Device.kicad_sym", "R"),
    "Device:C":       (STOCK + "/Device.kicad_sym", "C"),
}
DEFS, PINGEO = {}, {}
for libid, (path, nm) in SRC.items():
    blk, pins = extract(path, nm)
    base = libid.split(":")[1]
    blk = blk.replace(f'(symbol "{nm}_', f'(symbol "{base}_')
    DEFS[libid] = blk.replace(f'(symbol "{nm}"', f'(symbol "{libid}"', 1)
    PINGEO[libid] = {p[0]: (p[1], p[2]) for p in pins}

GND = "GND"
NC = None

# ---------------------------------------------------------------- BM83SM1 dispositions
# F31 CLOSES HERE, on the datasheet's own words. Pin 23: "Power supply input; voltage range:
# 3.2V to 4.2V. Source can either be a Li-ion battery OR ANY OTHER POWER RAIL ON THE HOST
# BOARD." So a direct rail feed with no battery and no charger path is blessed, not tolerated.
# ADAP_IN is the 5 V charger input and is left floating, per its own pin description.
BM = {
    # --- unit 1: power
    "23": "+3V6_BT",
    "22": NC,          # ADAP_IN -- 5 V charger path unused, datasheet permits floating
    "24": NC, "25": NC,# SYS_PWR / VDD_IO -- "for internal use only, do not connect"
    "15": NC,          # MICBIAS unused
    "16": GND, "50": GND,
    # --- I2S: SLAVE to the DSP's SDATA_IN1 port clocks. S4 [HARD] map, S3 decree.
    "5":  NC,          # MCLK1 is OUTPUT-ONLY (T1-56) and we are the clock master. Unused.
    "3":  "TDM_IN1_BCLK",
    "2":  "TDM_IN1_LRCLK",
    "4":  "TDM_IN1_DATA",     # DT1 = module transmit = A2DP audio out toward the DSP
    "1":  GND,                # DR1 = module receive, unused INPUT -- given a level, not left
                              # floating (F21). Not an output, so grounding is safe.
    # --- analog audio: entirely unused, we take the digital port
    "8": NC, "6": NC, "7": NC, "12": NC, "11": NC,
    "14": NC, "13": NC, "10": NC, "9": NC,
    "17": NC, "18": NC, "19": NC,
    # --- unit 2: Host-mode control plane, Figure 6-8
    "43": "BM83_RST_N",
    "26": "BM83_MFB",         # host -> module wake / power key
    "29": "BM83_UART_RXD",
    "30": "BM83_UART_TXD",
    "49": "BM83_TX_IND",      # module -> host wake (P0_0)
    "48": NC,                 # UART_CTS unused -- flow control not used in this config
    "31": "BM83_CFG_MODE",    # P3_4/UART_RTS: ALSO the Application/Test strap. See NOTE2.
    "46": NC, "47": NC,       # P1_2/P1_3 (I2C in some configs) unused
    "37": NC, "36": NC,       # module USB unused
    "32": NC, "34": NC,       # LED1/LED2 unused -- driven from SYS_PWR, which we do not fit
    "27": NC, "28": NC,       # SK1/SK2 unused
    "20": NC, "21": NC, "33": NC, "35": NC, "38": NC, "39": NC,
    "40": NC, "41": NC, "42": NC, "44": NC, "45": NC,
}

PLACE = [("U30", "ODSP12:BM83SM1", 100, 120, "BM83SM1", BM)]

_pc = [0]
def passive(kind, x, y, val, na, nb):
    _pc[0] += 1
    r = kind + str(300 + _pc[0])
    return (r, {"C": "Device:C", "R": "Device:R"}[kind], x, y, val, {"1": na, "2": nb})

P = []
# BAT_IN decoupling. Worst-case draw is 59 mA (continuous TX, Table 9-12) -- the RF burst is
# the load that matters, and it is served locally, not through 30 mm of trace from the LDO.
P += [passive("C", 40, 260, "22uF/10V", "+3V6_BT", GND),
      passive("C", 70, 260, "1uF",      "+3V6_BT", GND),
      passive("C", 100, 260, "100n",    "+3V6_BT", GND)]
# RST_N: pull-up to its own rail so the module is OUT of reset by default and the ESP32 only
# has to assert. Series R protects against a host driving while the module rail is down.
P += [passive("R", 130, 260, "100k", "+3V6_BT", "BM83_RST_N"),
      passive("R", 160, 260, "1k",   "BM83_RST_N", "BM83_RST_N_MCU")]
# MFB: series resistor for the same reason -- the ESP32 runs from +3V3_D and the module from
# +3V6_BT, so the two domains meet here and at the UART.
P += [passive("R", 190, 260, "1k",   "BM83_MFB", "BM83_MFB_MCU"),
      passive("R", 220, 260, "100k", "BM83_MFB", GND)]
# Application/Test strap, pin 31. POPULATED = Application (normal). DNP = Test.
P += [passive("R", 250, 260, "10k",     "BM83_CFG_MODE", GND),
      passive("R", 280, 260, "10k DNP", "BM83_CFG_MODE", "+3V6_BT")]
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
    assert not extra, f"{ref}: nets on non-existent pins {sorted(extra)} -- stale pin map"
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
            out.append(f'\t(no_connect (at {lx} {ly}) (uuid "{u("nc" + ref + num)}"))')
            continue
        rot = 180 if sx < 0 else 0
        just = "right" if sx < 0 else "left"
        out += emit_label(nets[num], lx, ly, rot, just, u("l" + ref + num))
    return "\n".join(out)

NOTE1 = (
    "F31 CLOSES HERE, AND IT CLOSES ON THE DATASHEET'S OWN WORDS -- no battery, no charger.\\n"
    "Pin 23 BAT_IN: 'Power supply input; voltage range: 3.2V to 4.2V. Source can either be a\\n"
    "Li-ion battery OR ANY OTHER POWER RAIL ON THE HOST BOARD.' A direct rail feed is\\n"
    "BLESSED, not merely tolerated, so the charger path is not needed and ADAP_IN stays\\n"
    "floating per its own pin description.\\n"
    "\\n"
    "THE ARITHMETIC, END TO END:\\n"
    "  +3V6_BT actual = 3.584 V (AP2127K-ADJ, VREF 0.8 V +/-2 %, 34.8k/10k -- V-23).\\n"
    "  Worst case across VREF tol + both divider legs: ~3.44 V to ~3.73 V.\\n"
    "  BAT_IN window: 3.2 V to 4.2 V.  ->  clears the floor by 240 mV and the ceiling by 470 mV.\\n"
    "  Current, Table 9-12: A2DP 12.05 mA typ; SCO 14.1 mA; CONTINUOUS TX 59 mA WORST.\\n"
    "  AP2127 is a 300 mA part -> 5x margin on the worst RF case, and the LDO dissipates\\n"
    "  (5.0 - 3.584) x 0.059 = 84 mW, trivial in SOT-23-5.\\n"
    "THE OLD 100 mA ESTIMATE IN S7.1 WAS CONSERVATIVE BY ~1.7x. It is not corrected here --\\n"
    "the rail was sized on it and the margin is free -- but the measured number is now on\\n"
    "record so a future cost pass does not 'discover' the headroom and delete it.\\n"
    "\\n"
    "SYS_PWR (24) and VDD_IO (25) are 'for internal use only, do not connect'. They are\\n"
    "explicit no-connects, NOT tied to anything convenient -- the temptation is to bridge\\n"
    "SYS_PWR to the rail because the name reads like an output that wants a cap."
)
NOTE2 = (
    "FLASHING IS COPPER, NOT INTENTION (F32). The module ships in EMBEDDED mode; this design\\n"
    "is HOST mode. Nothing on this sheet works until the config is flashed, so the path to\\n"
    "flash it is drawn rather than assumed:\\n"
    "  * UART_RXD (29) / UART_TXD (30) reach the ESP32 AND a test header, so the Config Tool\\n"
    "    can drive the module directly with the ESP32 held in reset.\\n"
    "  * PIN 31 (P3_4/UART_RTS) IS ALSO THE APPLICATION / TEST MODE STRAP. Stuffing pair:\\n"
    "        POPULATED 10k to GND      = Application mode (normal operation)\\n"
    "        DNP 10k to +3V6_BT        = Test mode (programming)\\n"
    "    Two positions, one populated, so mode entry is a soldering iron and not a cut trace.\\n"
    "  * BM83_RST_N is brought out with a series 1k, so the tool can toggle reset.\\n"
    "  * PROCEDURE, INCLUDING WHO FLASHES AND WHEN, IS A BRINGUP.md LINE -- copper only makes\\n"
    "    it possible. F32 asked for the production-step decision and that is still open:\\n"
    "    factory-programmed part, or a board-level step. THIS SHEET DOES NOT DECIDE IT.\\n"
    "\\n"
    "CONFIG-DEPENDENT PINS CARRY '*' IN THE SYMBOL (F32 convention). This is the ONE part on\\n"
    "the board whose PINOUT is firmware-dependent, so F28's 'every pin dispositioned' needs a\\n"
    "second dimension here: a pin can be correctly dispositioned FOR THE WRONG CONFIG. Every\\n"
    "'*' pin above is a no-connect, which is the only disposition that stays valid in both\\n"
    "modes -- deliberately, not by accident."
)
NOTE3 = (
    "I2S: THE MODULE IS A SLAVE, AND THE DECREE SAYS SO TWICE.\\n"
    "S4 [HARD] map: SDATA_IN1 = BM83, I2S stereo, 2 channels -> ASRC.\\n"
    "S3: '... BM83 I2S port (BM83 configured as I2S slave).'\\n"
    "So SCLK1 (3) and RFS1 (2) are INPUTS here, driven by the DSP's SDATA_IN1 port clocks, and\\n"
    "DT1 (4) carries A2DP audio toward the DSP. T1-56 confirms this is possible: SCLK1 and RFS1\\n"
    "are I/O, so the module can be either -- it is CONFIGURATION that makes it a slave, which\\n"
    "means this is another line the flashed config must get right (F32 again).\\n"
    "MCLK1 (5) is OUTPUT-ONLY per T1-56 and we are the clock master, so it is unused.\\n"
    "\\n"
    "*** THE RECOVERED BLUETOOTH CLOCK NEVER ENTERS THE AUDIO CLOCK TREE. *** The module's\\n"
    "stream is asynchronous to our 48 kHz by nature, and S3 [HARD] routes it through the\\n"
    "ADAU1466's on-chip ASRC -- 'no exceptions'. Slaving the module to our clocks does NOT\\n"
    "make the STREAM synchronous; it only makes the WIRE synchronous. The ASRC is what absorbs\\n"
    "the rate difference, and removing it because 'the port is slaved now' would be the exact\\n"
    "mistake F1 caught on the S/PDIF path.\\n"
    "DR1 (1) is an unused INPUT and is tied to GND rather than left floating (F21)."
)
NOTE4 = (
    "LAYOUT INPUTS -- recorded now because they constrain PLACEMENT before any footprint\\n"
    "exists, and placement is decided long before the footprint pass.\\n"
    "  * ANTENNA KEEPOUT [HARD]: no copper, no components, no ground plane under the module's\\n"
    "    PCB antenna. Exact dimensions are V-12, whose pages are rendered but NOT YET READ --\\n"
    "    they belong with the footprint, not here.\\n"
    "  * TWO 2.4 GHz ANTENNAS ON ONE BOARD. S8 [HARD]: separate them as far as geometry\\n"
    "    allows, DO NOT STACK. This module and the ESP32-S3-WROOM-1 are both radios with\\n"
    "    integrated antennas and they share a band. The constraint is on the BOARD OUTLINE,\\n"
    "    which is still Block D UNSET -- so this note exists to make sure the outline, when it\\n"
    "    arrives, is chosen with two antenna corners in mind rather than discovered to lack\\n"
    "    them.\\n"
    "  * The module edge should face a board edge. That is a placement consequence of the\\n"
    "    keepout, not an extra rule."
)

G1, G2 = geometry(1), geometry(2)
assert set(G1) | set(G2) == set(PINGEO["ODSP12:BM83SM1"]), (
    "per-unit geometry does not reconstruct the symbol's full pin set")
assert not (set(G1) & set(G2)), "a pin appears in both units"
body  = [place("U30", "ODSP12:BM83SM1", 100, 120, "BM83SM1",
               {k: v for k, v in BM.items() if k in G1}, unit=1, geo=G1)]
body += [place("U30", "ODSP12:BM83SM1", 260, 120, "BM83SM1",
               {k: v for k, v in BM.items() if k in G2}, unit=2, geo=G2)]
body += [place(*p) for p in PLACE[1:]]
for i, (nx, ny, txt) in enumerate([(430.0, 60.0, NOTE1), (430.0, 190.0, NOTE2),
                                   (430.0, 330.0, NOTE3), (430.0, 460.0, NOTE4)]):
    body.append(f'\t(text "{txt}"\n\t\t(exclude_from_sim no)\n\t\t(at {snap(nx)} {snap(ny)} 0)\n'
                f'\t\t(effects (font (size 1.27 1.27)) (justify left top))\n'
                f'\t\t(uuid "{u(f"n{i}")}")\n\t)')

# F53 SWEEP 2026-08-20: page DERIVED from content and ASSERTED, never declared.
# Measured before the fix: this sheet's content overran (paper "A3") = 420x297 mm,
# so the PDF export silently clipped everything past the frame -- including notes the
# reviewer has been quoting back at us. A count is a receipt; open the page.
_XY = [(float(a), float(b)) for a, b in
       re.findall(r'\(at ([-\d.]+) ([-\d.]+)', chr(10).join(body))]
PAPER_W = math.ceil((max(x for x, _ in _XY) + 40) / 10) * 10
PAPER_H = math.ceil((max(y for _, y in _XY) + 40) / 10) * 10
assert PAPER_W <= 1200 and PAPER_H <= 1200, f'page {PAPER_W}x{PAPER_H} exceeds KiCad limits'

sch = f'''(kicad_sch
\t(version {VER})
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{SHEET_UUID}")
\t(paper "User" {PAPER_W:.1f} {PAPER_H:.1f})
\t(title_block
\t\t(title "ODSP-12 :: Bluetooth -- BM83SM1, I2S slave on SDATA_IN1")
\t\t(date "2026-08-16")
\t\t(rev "A")
\t\t(comment 1 "ODSP12-MB-A")
\t\t(comment 2 "Host mode. Pinout is firmware-dependent -- see the F32 note before editing")
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
print(f"  {len(LABELS)} global labels, no collisions")
