# Generates 05_spdif.kicad_sch and 09_io.kicad_sch.
#
# 09_io retires the last ERC counterparts, so after this pass the ERC number means something
# ABSOLUTE rather than "counterparts on undrawn sheets".
import os, re, uuid, math

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

SRC = {
    "Connector_Generic:Conn_01x02":(STOCK + "/Connector_Generic.kicad_sym", "Conn_01x02"),
    "Connector_Generic:Conn_01x08":(STOCK + "/Connector_Generic.kicad_sym", "Conn_01x08"),
    "Connector_Generic:Conn_02x08_Odd_Even":(STOCK + "/Connector_Generic.kicad_sym", "Conn_02x08_Odd_Even"),
    "Transistor_FET:Q_PMOS_DGS":   (STOCK + "/Transistor_FET.kicad_sym", "Q_PMOS_DGS"),
    "Transistor_BJT:Q_NPN_BEC":    (STOCK + "/Transistor_BJT.kicad_sym", "Q_NPN_BEC"),
    "Device:R": (STOCK + "/Device.kicad_sym", "R"),
    "Device:C": (STOCK + "/Device.kicad_sym", "C"),
    "Device:L": (STOCK + "/Device.kicad_sym", "L"),
    "Device:D_Zener": (STOCK + "/Device.kicad_sym", "D_Zener"),
    "Device:LED": (STOCK + "/Device.kicad_sym", "LED"),
    "Device:Transformer_1P_1S": (STOCK + "/Device.kicad_sym", "Transformer_1P_1S"),
}
DEFS, PINGEO = {}, {}
for libid, (path, nm) in SRC.items():
    blk, pins = extract(path, nm)
    base = libid.split(":")[1]
    blk = blk.replace(f'(symbol "{nm}_', f'(symbol "{base}_')
    DEFS[libid] = blk.replace(f'(symbol "{nm}"', f'(symbol "{libid}"', 1)
    PINGEO[libid] = {p[0]: (p[1], p[2]) for p in pins}
GND = "GND"; NC = None

def sheet(fname, title, comment2, build_fn):
    SHEET_UUID = str(uuid.uuid5(NS, "sheet:" + fname))
    SHEET_SYM_UUID = str(uuid.uuid5(NS, "inst:" + fname))
    tag = fname.split("_")[0]
    def u(t): return str(uuid.uuid5(NS, tag + ":" + t))
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
    def place(ref, libid, x, y, val, nets):
        x, y = snap(x), snap(y)
        geo = PINGEO[libid]
        missing = set(geo) - set(nets); extra = set(nets) - set(geo)
        assert not missing, f"{ref}: pins with no disposition (F28): {sorted(missing)}"
        assert not extra, f"{ref}: nets on non-existent pins {sorted(extra)}"
        out = ['\t(symbol', f'\t\t(lib_id "{libid}")', f'\t\t(at {x} {y} 0)', '\t\t(unit 1)',
               '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)', '\t\t(dnp no)',
               f'\t\t(uuid "{u("i"+ref)}")',
               f'\t\t(property "Reference" "{ref}" (at {x} {y-22} 0) (effects (font (size 1.27 1.27))))',
               f'\t\t(property "Value" "{val}" (at {x} {y-19} 0) (effects (font (size 1.27 1.27))))',
               '\t\t(instances', '\t\t\t(project "ODSP12-MB"',
               f'\t\t\t\t(path "/{ROOT_UUID}/{SHEET_SYM_UUID}" (reference "{ref}") (unit 1))',
               '\t\t\t)', '\t\t)', '\t)']
        for num, (sx, sy) in geo.items():
            lx, ly = snap(x + sx), snap(y - sy)
            if nets[num] is None:
                out.append(f'\t(no_connect (at {lx} {ly}) (uuid "{u("nc"+ref+num)}"))')
                continue
            rot = 180 if sx < 0 else 0
            just = "right" if sx < 0 else "left"
            out += emit_label(nets[num], lx, ly, rot, just, u("l"+ref+num))
        return "\n".join(out)
    PLACE, NOTES = [], []
    build_fn(PLACE, NOTES)
    body = [place(*p) for p in PLACE]
    for i, (nx, ny, txt) in enumerate(NOTES):
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
\t\t(title "{title}")
\t\t(date "2026-08-16")
\t\t(rev "A")
\t\t(comment 1 "ODSP12-MB-A")
\t\t(comment 2 "{comment2}")
\t)
\t(lib_symbols
{chr(10).join(DEFS.values())}
\t)
{chr(10).join(body)}
\t(embedded_fonts no)
)
'''
    open(os.path.join(HW, fname), "w", encoding="utf-8", newline="\n").write(sch)
    print(f"wrote {fname}: {len(PLACE)} instances, {len(LABELS)} labels, no collisions")

# =============================================================== 05_spdif
_n = [0]
def R(x, y, v, a, b, pre="R"):
    _n[0] += 1
    return (f"{pre}{800+_n[0]}", {"R":"Device:R","C":"Device:C","L":"Device:L"}[pre],
            x, y, v, {"1": a, "2": b})

def build_spdif(PLACE, NOTES):
    PLACE.append(("J40", "Connector_Generic:Conn_01x02", 40, 60, "RCA coax in, 75R",
                  {"1": "SPDIF_TIP", "2": "SPDIF_SHIELD"}))
    PLACE += [R(90, 60, "75R", "SPDIF_TIP", "SPDIF_SHIELD")]          # termination
    PLACE.append(("T40", "Device:Transformer_1P_1S", 140, 60, "PE-65612NL",
                  {"1": "SPDIF_TIP", "2": "SPDIF_SHIELD", "3": "SPDIF_SEC_A", "4": "SPDIF_SEC_B"}))
    PLACE += [R(200, 60, "100n", "SPDIF_SEC_A", "SPDIF_RX_IN", pre="C"),
              R(200, 80, "0R",  "SPDIF_SEC_B", GND),
              R(240, 60, "1k",  "SPDIF_RX_IN", GND)]                  # bias reference return
    # chassis reference for the coax shield -- the S6.3 RC, drawn ONCE on 09_io and referenced
    PLACE += [R(90, 100, "0R", "SPDIF_SHIELD", "CHASSIS_RC")]
    PLACE += [R(300, 60, "0R", "SPDIF_TX_OUT", "TP_SPDIF_TX")]        # testpoint only
    NOTES.append((360.0, 40.0,
        "SPDIF INPUT -- what is left after F26 deleted the AK4118A AND the WM8804.\\n"
        "S/PDIF RX is ON-DIE in the ADAU1466 (pin 4 SPDIFIN), routed to an internal ASRC, and it\\n"
        "consumes NO serial port. So this whole sheet is a front end: terminate, isolate, couple.\\n"
        "\\n"
        "*** THE AC COUPLING CAPACITOR IS REQUIRED BY THE DATASHEET, NOT A PRECAUTION. *** T1-44:\\n"
        "the RX input is a comparator centred at IOVDD/2 and 'requires an AC coupling capacitor\\n"
        "on the pin'. Removing it does not degrade the link -- IT BREAKS THE BIAS POINT. Treat\\n"
        "this part as [HARD]: it is not a coupling cap that could be a 0R in a pinch.\\n"
        "\\n"
        "75 Ohm termination across the transformer primary, matched to the coax S/PDIF standard.\\n"
        "COMPARATOR MARGIN: T1-44 requires >= 200 mV p-p at the pin. Consumer S/PDIF sources\\n"
        "deliver 0.5 V p-p nominal into 75 Ohm; a 1:1 transformer passes that, so the margin is\\n"
        "~2.5x at nominal. The transformer is the reason the margin is checked at all -- turns\\n"
        "ratio and insertion loss both live in the PN, which is why it is PINNED and not left as\\n"
        "a generic symbol: PE-65612NL class, 1:1, S/PDIF-rated. F38 line, F38a manufacturer axis.\\n"
        "\\n"
        "GALVANIC ISOLATION IS THE POINT, not impedance matching -- a source with its own mains\\n"
        "ground would otherwise inject a ground loop straight into the analog reference. The\\n"
        "shield goes to the CHASSIS RC (S6.3), NOT to signal ground.\\n"
        "\\n"
        "*** SPDIF TX IS DELETED DELIBERATELY, NOT FORGOTTEN. *** The ADAU1466 has an on-die\\n"
        "transmitter (pin 5) and it costs nothing to leave enabled in firmware, but NO\\n"
        "requirement in S1 or S12 asks for a digital output, and a DNP jack would spend panel\\n"
        "area on an outline that is still Block D UNSET. SPDIF_TX_OUT lands on a TESTPOINT so\\n"
        "the capability stays reachable for bring-up. Reopen if an output is ever specified --\\n"
        "the silicon is already paid for."))

# =============================================================== 09_io
def build_io(PLACE, NOTES):
    # --- 4 line-level RCA inputs. The DIFFERENTIAL pair's N leg lands on the jack sleeve, which
    #     is what makes a single-ended RCA source work into a differential receiver.
    for n in range(1, 5):
        PLACE.append((f"J{50+n}", "Connector_Generic:Conn_01x02", 40, 40 + (n-1)*30, "RCA in, line",
                      {"1": f"IN{n}_P", "2": f"IN{n}_N"}))
    # --- speaker-level input: a screw terminal, not RCA. 4 pairs = 8 ways.
    PLACE.append(("J60", "Connector_Generic:Conn_01x08", 150, 60, "speaker-level in, 8-way",
                  {str(i+1): (f"IN{i//2+1}_P" if i % 2 == 0 else f"IN{i//2+1}_N") for i in range(8)}))
    # --- 12 RCA outputs
    for n in range(1, 13):
        PLACE.append((f"J{70+n}", "Connector_Generic:Conn_01x02", 260 + ((n-1)//6)*70, 40 + ((n-1) % 6)*30,
                      f"RCA out AOUT{n}", {"1": f"AOUT{n}", "2": "RCA_SHIELD"}))
    # --- power + remote terminal block
    PLACE.append(("J90", "Connector_Generic:Conn_01x02", 40, 200, "power in",
                  {"1": "VBATT_IN", "2": "CHASSIS"}))
    PLACE.append(("J91", "Connector_Generic:Conn_01x02", 100, 200, "remote in/out",
                  {"1": "REMOTE_IN", "2": "REMOTE_OUT"}))
    # remote-in sense divider: 12 V logic -> 3.3 V domain
    PLACE += [R(40, 240, "100k", "REMOTE_IN", "REMOTE_IN_SENSE"),
              R(70, 240, "33k",  "REMOTE_IN_SENSE", GND),
              R(100, 240, "100n","REMOTE_IN_SENSE", GND, pre="C")]
    # --- remote-out HIGH-SIDE driver. Energised = asserted. See NOTE.
    PLACE.append(("Q90", "Transistor_BJT:Q_NPN_BEC", 150, 250, "MMBT3904",
                  {"1": "ROUT_BASE", "2": "ROUT_GATE", "3": GND}))
    PLACE += [R(130, 250, "10k", "REMOTE_OUT_EN", "ROUT_BASE"),
              R(130, 275, "100k", "ROUT_BASE", GND)]
    PLACE.append(("Q91", "Transistor_FET:Q_PMOS_DGS", 200, 250, "60V P-FET",
                  {"1": "REMOTE_OUT", "2": "ROUT_GATE", "3": "VBATT_PROT"}))
    PLACE += [R(230, 250, "100k", "ROUT_GATE", "VBATT_PROT"),
              R(260, 250, "100R", "REMOTE_OUT", GND)]
    PLACE.append(("D90", "Device:D_Zener", 290, 250, "15V",
                  {"1": "ROUT_GATE", "2": "VBATT_PROT"}))
    # --- RCA shield field -> chassis, ONE RC, referenced from everywhere else
    PLACE += [R(40, 300, "10R", "RCA_SHIELD", "CHASSIS_RC"),
              R(70, 300, "100n", "CHASSIS_RC", "CHASSIS", pre="C"),
              R(100, 300, "1M",  "CHASSIS_RC", "CHASSIS"),
              R(130, 300, "0R",  "RCA_SHIELD", GND)]
    # --- status LED
    PLACE += [R(170, 300, "1k", "+3V3_D", "LED_A")]
    PLACE.append(("D91", "Device:LED", 200, 300, "green, STATUS",
                  {"1": "LED_A", "2": "STATUS_LED_N"}))
    # --- test header: spare TDM ports + consoles + I2C, GROUNDS INTERLEAVED per S4
    hdr = {}
    sig = ["TDM_IN2_DATA", "TDM_IN3_DATA", "TDM_OUT2_DATA", "TDM_OUT3_DATA",
           "UART0_TXD", "UART0_RXD", "I2C0_SDA", "I2C0_SCL"]
    for i, nm in enumerate(sig):
        hdr[str(2*i + 1)] = nm
        hdr[str(2*i + 2)] = GND
    PLACE.append(("J95", "Connector_Generic:Conn_02x08_Odd_Even", 380, 250,
                  "test header, 0.1in", hdr))
    NOTES.append((470.0, 40.0,
        "CONNECTOR INVENTORY, SETTLED IN COPPER -- the 28-vs-18 dispute from the criteria round.\\n"
        "  RCA line inputs        J51-J54    4\\n"
        "  RCA outputs AOUT1-12   J71-J82   12\\n"
        "  RCA coax S/PDIF in     J40        1   (on 05_spdif)\\n"
        "  ------------------------------------\\n"
        "  TOTAL RCA-CLASS JACKS            17\\n"
        "  plus: speaker-level 8-way terminal (J60), power 2-way (J90), remote 2-way (J91),\\n"
        "        and one 2x8 test header (J95).\\n"
        "THE OPERATOR'S COUNT OF 17-18 WAS RIGHT AND MINE OF 28 WAS WRONG -- I had added the 12\\n"
        "outputs to a subtotal that already contained them. A total is an assertion; a sum is\\n"
        "checkable. This table is the sum.\\n"
        "\\n"
        "SPEAKER LEVEL IS A TERMINAL BLOCK, NOT AN RCA. At 30 Vrms the source is an amplifier\\n"
        "output pair, delivered on harness wire, and it is differential -- so it gets a screw\\n"
        "terminal and shares the SAME differential nets as the line jacks. The RCA sleeve is\\n"
        "IN{n}_N, which is what lets a single-ended source drive a differential receiver: the\\n"
        "sleeve is not ground here, it is the inverting input, and grounding it at the jack\\n"
        "would throw away the CMRR the INA1650 and its matched attenuator were bought for."))
    NOTES.append((470.0, 190.0,
        "REMOTE-OUT IS FAIL-SAFE BY CONSTRUCTION (S7.4), AND THAT IS WHY IT IS A HIGH-SIDE FET.\\n"
        "Q91 is a P-FET from VBATT_PROT; Q90 pulls its gate down when REMOTE_OUT_EN is asserted.\\n"
        "  ENERGISED = ASSERTED. De-energised = released.\\n"
        "THE WALK: rails sag -> Q90's base drive dies -> R(gate-to-source) pulls the gate to\\n"
        "VBATT_PROT -> Q91 turns OFF -> REMOTE_OUT RELEASES. This happens BEFORE the MCU knows\\n"
        "anything, which is the entire point: S7.3 step 1 says remote-out drops first so the\\n"
        "downstream amplifiers mute before our rails finish collapsing. A LOW-SIDE switch or a\\n"
        "GPIO-driven latch would both hold their last state into the sag -- exactly wrong.\\n"
        "D90 (15 V) clamps Vgs against the VBATT_PROT excursions the TVS lets through; the same\\n"
        "reasoning as Q2's gate zener on 01_power, and for the same reason it is not optional.\\n"
        "100R to ground bleeds the line so a floating amplifier input cannot self-assert.\\n"
        "\\n"
        "CHASSIS / SHIELD (S6.3): the RCA shield field is a SINGLE net (RCA_SHIELD) star-joined\\n"
        "to chassis through ONE RC -- 10R + 100n in parallel with 1M. The 1M bleeds static, the\\n"
        "100n gives RF a low-impedance path, the 10R stops it being a plain short. Drawn ONCE,\\n"
        "here, and referenced from 05_spdif -- a second RC elsewhere makes a loop, which is the\\n"
        "failure this arrangement exists to prevent. It is an EMC component, per S7.5.\\n"
        "\\n"
        "TEST HEADER: grounds INTERLEAVED between signals per S4's note -- every odd pin is a\\n"
        "signal, every even pin is ground. On a 0.1 inch header carrying 12.288 MHz TDM that is\\n"
        "not tidiness, it is the return path; without it the header is eight unshielded stubs."))

sheet("05_spdif.kicad_sch", "ODSP-12 :: S/PDIF -- coax front end into the DSP's on-die RX",
      "F26: AK4118A and WM8804 deleted. RX is on-die, pin 4, via ASRC", build_spdif)
sheet("09_io.kicad_sch", "ODSP-12 :: I/O -- jacks, chassis, remote, test",
      "17 RCA-class jacks. Shield field star-joined to chassis through ONE RC", build_io)
