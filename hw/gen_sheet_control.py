# Generates 03_control.kicad_sch -- ESP32-S3-WROOM-1, USB-C debug port, and the sequencing /
# monitor nets this sheet terminates.
#
# PIN MAP SOURCE OF TRUTH: ESP32-S3-WROOM-1 datasheet, Table 3 "Pin Definitions" pp.10-12,
# extracted as name+number pairs and spot-checked against the stock symbol (T1-94..T1-96).
# The stock RF_Module:ESP32-S3-WROOM-1 symbol is SELF-CONTAINED (no extends) and its pin 13/14
# are already named USB_D-/USB_D+, which is the [HARD] GPIO19/20 reservation pre-encoded.
import os, re, uuid

HW = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HW, "03_control.kicad_sch")
NS = uuid.UUID("0d5f1a00-0000-4000-8000-0000000000ff")
SHEET_UUID = str(uuid.uuid5(NS, "sheet:03_control.kicad_sch"))
SHEET_SYM_UUID = str(uuid.uuid5(NS, "inst:03_control.kicad_sch"))
ROOT_UUID = "0d5f1a00-0000-4000-8000-000000000001"
VER = "20260306"
GRID = 1.27
def snap(v): return round(v / GRID) * GRID
def u(t): return str(uuid.uuid5(NS, "ctl:" + t))

STOCK = r"C:/Program Files/KiCad/10.0/share/kicad/symbols"

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

SRC = {
    "RF_Module:ESP32-S3-WROOM-1": (STOCK + "/RF_Module.kicad_sym", "ESP32-S3-WROOM-1"),
    "Connector:USB_C_Receptacle": (STOCK + "/Connector.kicad_sym", "USB_C_Receptacle"),
    # USBLC6-2SC6: PROJECT symbol. KiCad's is an (extends "USBLC6-2P6") alias; renaming the
    # parent's children produced a cache ERC rejected as lib_symbol_mismatch, and aliasing to
    # the parent would have put SOT-666 in the BOM instead of SOT-23-6. Third extends-alias
    # trap on this project, and the first one ERC caught rather than the netlist.
    "ODSP12:USBLC6-2SC6": (os.path.join(HW, "lib", "ODSP12.kicad_sym"), "USBLC6-2SC6"),
    "Switch:SW_Push":             (STOCK + "/Switch.kicad_sym", "SW_Push"),
    "Device:R":                   (STOCK + "/Device.kicad_sym", "R"),
    "Device:C":                   (STOCK + "/Device.kicad_sym", "C"),
    "Device:LED":                 (STOCK + "/Device.kicad_sym", "LED"),
    "power:PWR_FLAG":             (STOCK + "/power.kicad_sym", "PWR_FLAG"),
}
DEFS, PINGEO = {}, {}
for libid, (path, nm) in SRC.items():
    blk, pins = extract(path, nm)
    base = libid.split(":")[1]
    blk = blk.replace(f'(symbol "{nm}_', f'(symbol "{base}_')      # children first
    DEFS[libid] = blk.replace(f'(symbol "{nm}"', f'(symbol "{libid}"', 1)   # then the parent
    PINGEO[libid] = {p[0]: (p[1], p[2]) for p in pins}

GND = "GND"

# ---------------------------------------------------------------- the GPIO map
# Every entry is (module_pin, net). Constraints honoured, each traceable to a T1 fact:
#   * pins 13/14 = IO19/IO20 -> USB D-/D+ ONLY. [HARD], CLAUDE.md s4.
#   * pins 15/16/26/27 = IO3/IO46/IO45/IO0 are STRAPPING. Nothing that drives during reset;
#     each gets a deterministic idle level rather than inheriting an internal weak pull (F21).
#   * pins 28/29/30 = IO35/36/37 are FREE on the N8R2 -- the datasheet reserves them only on
#     Octal-PSRAM modules (R8 / R16V). This is the F38 pinned-PN reason made load-bearing.
#   * pins 24/25 = IO47/IO48 carry footnote c; left as explicit no-connects.
ESP = {
    "1": GND, "40": GND, "41": GND,
    "2": "+3V3_D",
    "3": "ESP_EN",
    # --- control plane
    "4": "I2C0_SDA", "5": "I2C0_SCL",
    "6": "SPI_DSP_SCLK", "7": "SPI_DSP_MOSI", "8": "SPI_DSP_MISO", "9": "SPI_DSP_SS_N",
    "10": "BM83_UART_RXD", "11": "BM83_UART_TXD",       # U1TXD/U1RXD, ESP-side naming
    "12": "DSP_RESET_N",
    # --- USB, [HARD]
    "13": "USB_DN", "14": "USB_DP",
    # --- strapping: deterministic idle, nothing driven during reset
    "15": "STRAP_IO3", "16": "STRAP_IO46", "26": "STRAP_IO45", "27": "STRAP_IO0",
    # --- converter control
    "17": "ADC_PDN_N", "18": "DAC1_PDN_N", "19": "DAC2_PDN_N",
    "20": "ADC_OVF",                                     # F29, edge interrupt
    # The three I2C-side interrupt sources (ADS1015 ALERT, TMP461 ALERT, PCF8574 INT)
    # are ALL open-drain and all mean the same thing -- "go read I2C" -- so they
    # wire-OR onto ONE line with one pull-up. That is what gave the expander's INT
    # a home; without it SIGNAL_SENSE would have become a polled net and the poll
    # interval would have become an undeclared turn-on latency spec (S7.2).
    "21": "I2C_ALERT_N", "22": "RAILMON_ALERT",   # dedicated: rail faults are the urgent ones (F47)
    "23": "MUTE_EN",
    # IO47/IO48 carry footnote c, which is R16V-ONLY: "for modules embedded with
    # ESP32-S3R16V, as the VDD_SPI voltage ... is set to 1.8 V, the working voltage for GPIO47
    # and GPIO48 is also 1.8 V". The N8R2 is not R16V, so these are ordinary 3.3 V GPIOs --
    # the same variant-conditional shape as footnote b, and the same reason the PN is pinned.
    "24": "BM83_RST_N_MCU",                              # IO47 -- host hard-reset for the module
    "25": "BM83_TX_IND",                                 # IO48 -- BM83 P0_0 wakes the MCU
    # --- power-good sense (all open-drain, pulled up on 01_power or here)
    "28": "PG_5V_D", "29": "PG_6V2_A", "30": "PG_1V2",
    "31": "PG_13V5P", "32": "PG_13V5N",
    # --- amp interface + status
    "33": "REMOTE_IN_SENSE", "34": "REMOTE_OUT_EN", "35": "STATUS_LED_N",
    "36": "UART0_RXD", "37": "UART0_TXD",                # console, keep for bring-up
    "38": "BM83_MFB_MCU",
    "39": "VBUS_DET",                                    # ADC1_CH0, divider only -- see NOTE2
}

PLACE = [("U20", "RF_Module:ESP32-S3-WROOM-1", 90, 120, "ESP32-S3-WROOM-1-N8R2", ESP)]

# ---------------------------------------------------------------- USB-C debug port
# Criterion: VBUS NEVER meets +5V_D. It terminates on the ESD array and a sense divider and
# goes nowhere else. There is no stuffing option, no 0R, no ferrite -- see NOTE2.
UC = PINGEO["Connector:USB_C_Receptacle"]
usb = {}
for p in UC:
    if p in ("A1", "A12", "B1", "B12", "S1"): usb[p] = GND
    elif p in ("A4", "A9", "B4", "B9"):       usb[p] = "VBUS_USB"
    elif p == "A5":                            usb[p] = "USB_CC1"
    elif p == "B5":                            usb[p] = "USB_CC2"
    elif p in ("A6", "B6"):                    usb[p] = "USB_DP"
    elif p in ("A7", "B7"):                    usb[p] = "USB_DN"
    else:                                      usb[p] = None          # SBU1/SBU2 unused
PLACE.append(("J20", "Connector:USB_C_Receptacle", 300, 120, "USB-C 2.0 recept.", usb))

ED = PINGEO["ODSP12:USBLC6-2SC6"]
# USBLC6 pin map (from the parent symbol): 1,6 = I/O1 ; 3,4 = I/O2 ; 2 = GND ; 5 = VBUS.
# Pins 1/6 are the SAME internal node, as are 3/4 -- so each pair carries one net. Wiring
# "connector side" and "chip side" to different nets would leave D+/D- open in the netlist
# while looking like a tidy pass-through on the sheet.
_edmap = {"1": "USB_DP", "6": "USB_DP", "3": "USB_DN", "4": "USB_DN",
          "2": GND, "5": "VBUS_USB"}
PLACE.append(("D20", "ODSP12:USBLC6-2SC6", 240, 120, "USBLC6-2SC6",
              {p: _edmap.get(p) for p in ED}))

_pc = [0]
def passive(kind, x, y, val, na, nb, ref=None):
    _pc[0] += 1
    r = ref or (kind + str(200 + _pc[0]))
    lib = {"C": "Device:C", "L": "Device:L", "R": "Device:R", "LED": "Device:LED"}[kind]
    return (r, lib, x, y, val, {"1": na, "2": nb})

P = []
# CC pull-downs: device (UFP) role, 5.1k each. Two resistors, not one -- the port must present
# Rd on WHICHEVER CC the cable orientation lands on.
P += [passive("R", 340, 60, "5.1k", "USB_CC1", GND),
      passive("R", 370, 60, "5.1k", "USB_CC2", GND)]
# VBUS sense divider ONLY. 100k/47k from 5 V gives 1.60 V at the ADC pin, inside the 3.3 V
# range with margin, and ~34 uA of load -- detect, not power.
P += [passive("R", 400, 60, "100k", "VBUS_USB", "VBUS_DET"),
      passive("R", 430, 60, "47k",  "VBUS_DET", GND),
      passive("C", 460, 60, "100n", "VBUS_DET", GND)]
# Module supply: bulk sized for the WiFi TX burst, at the module pins.
P += [passive("C", 40, 250, "22uF/16V", "+3V3_D", GND),
      passive("C", 70, 250, "10uF/16V", "+3V3_D", GND),
      passive("C", 100, 250, "100n", "+3V3_D", GND),
      passive("C", 130, 250, "100n", "+3V3_D", GND)]
# EN: RC delay so the module releases reset after +3V3_D is settled, plus a manual reset.
P += [passive("R", 160, 250, "10k",  "+3V3_D", "ESP_EN"),
      passive("C", 190, 250, "1uF",  "ESP_EN", GND)]
PLACE.append(("SW20", "Switch:SW_Push", 220, 250, "RESET", {"1": "ESP_EN", "2": GND}))
# Strapping: deterministic levels rather than inherited internal weak pulls (F21).
P += [passive("R", 250, 250, "10k", "+3V3_D", "STRAP_IO0"),     # boot: HIGH = normal run
      passive("R", 280, 250, "10k", "STRAP_IO45", GND),         # VDD_SPI 3.3 V = default 0
      passive("R", 310, 250, "10k", "STRAP_IO46", GND),         # ROM print = default 0
      passive("R", 340, 250, "10k", "STRAP_IO3", GND)]          # JTAG sel: datasheet default
                                                                # is FLOATING -- made explicit
PLACE.append(("SW21", "Switch:SW_Push", 370, 250, "BOOT", {"1": "STRAP_IO0", "2": GND}))
# Status LED, active low from IO42.
P += [passive("R", 400, 250, "1k", "+3V3_D", "STATUS_LED_A")]
PLACE.append(("D21", "Device:LED", 430, 250, "green", {"1": "STATUS_LED_A", "2": "STATUS_LED_N"}))
# Pull-ups for the two open-drain PG pins that 01_power does not already pull up.
P += [passive("R", 460, 250, "100k", "+3V3_D", "PG_5V_D"),
      passive("R", 490, 250, "100k", "+3V3_D", "PG_6V2_A"),
      passive("R", 520, 250, "100k", "+3V3_D", "PG_1V2")]
# I2C0 bus pull-ups live here, once, with the controller.
P += [passive("R", 550, 250, "2.2k", "+3V3_D", "I2C0_SDA"),
      passive("R", 580, 250, "2.2k", "+3V3_D", "I2C0_SCL")]
# VBUS is a source with no active driver on this sheet -- declare it, do not let ERC guess.
PLACE.append(("#FLG20", "power:PWR_FLAG", 620, 60, "PWR_FLAG", {"1": "VBUS_USB"}))
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

def place(ref, libid, x, y, val, nets):
    x, y = snap(x), snap(y)
    geo = PINGEO[libid]
    assert geo, f"{ref}: no pin geometry for {libid}"
    missing = set(geo) - set(nets)
    extra = set(nets) - set(geo)
    assert not missing, f"{ref}: pins with no disposition (F28): {sorted(missing)}"
    assert not extra, f"{ref}: nets on non-existent pins {sorted(extra)} -- stale pin map"
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
        if nets[num] is None:
            out.append(f'\t(no_connect (at {lx} {ly}) (uuid "{u("nc" + ref + num)}"))')
            continue
        rot = 180 if sx < 0 else 0
        just = "right" if sx < 0 else "left"
        out += emit_label(nets[num], lx, ly, rot, just, u("l" + ref + num))
    return "\n".join(out)

NOTE1 = (
    "GPIO MAP -- F13 CLOSED. Every constraint below is a datasheet fact, not a convention.\\n"
    "\\n"
    "(a) IO35 / IO36 / IO37 ARE FREE ON THIS MODULE, and only on this module. The datasheet:\\n"
    "    'For modules with Octal SPI PSRAM, i.e. modules embedded with ESP32-S3R8 or\\n"
    "    ESP32-S3R16V, pins IO35, IO36 and IO37 are connected to the Octal SPI PSRAM and are\\n"
    "    NOT AVAILABLE for other uses.' The N8R2 is QUAD PSRAM, so they are ours -- and three\\n"
    "    power-good sense lines are sitting on them. ORDER AN R8 OR R16V VARIANT AND THREE\\n"
    "    NETS SHORT INTO THE PSRAM BUS. This is the F38 pinned-PN rule with teeth: the suffix\\n"
    "    is not a stocking preference, it is a pinout.\\n"
    "\\n"
    "(b) IO19 / IO20 CARRY USB D-/D+ AND NOTHING ELSE -- [HARD], CLAUDE.md s4. The stock symbol\\n"
    "    names pins 13/14 USB_D-/USB_D+ directly, so the reservation is visible on the sheet\\n"
    "    rather than living in a comment.\\n"
    "\\n"
    "(c) STRAPPING PINS: IO0, IO3, IO45, IO46. Nothing that DRIVES during reset is on any of\\n"
    "    them; each gets a deterministic idle level instead of inheriting an internal weak\\n"
    "    pull (F21 -- 'floating is a state someone chose'). Datasheet Table 4-1 defaults:\\n"
    "        IO0  weak pull-UP   (1)  -> 10k to +3V3_D. Momentary BOOT switch pulls it low.\\n"
    "        IO3  FLOATING       (-)  -> 10k to GND. The only one with NO internal default,\\n"
    "                                    so it is the one that must not be left to chance.\\n"
    "        IO45 weak pull-DOWN (0)  -> 10k to GND, matching default (VDD_SPI = 3.3 V).\\n"
    "        IO46 weak pull-DOWN (0)  -> 10k to GND, matching default (ROM print).\\n"
    "    The resistors do not CHANGE any default. They make the default survive a neighbouring\\n"
    "    net, a probe, or a conformal-coat leakage path, which a weak internal pull may not.\\n"
    "\\n"
    "(d) IO47 / IO48 carry footnote c and are explicit no-connects."
)
NOTE2 = (
    "USB-C IS A DEBUG PORT. VBUS MUST NEVER MEET +5V_D. THIS IS A RULE, NOT A PREFERENCE.\\n"
    "VBUS_USB terminates on exactly two things: the ESD array's VBUS pin, and a 100k/47k\\n"
    "SENSE divider into IO1 (ADC1_CH0) -- 5 V gives 1.60 V at the pin, inside the 3.3 V range,\\n"
    "at ~34 uA. DETECT ONLY.\\n"
    "There is deliberately NO 0R, NO ferrite, NO diode-OR and NO DNP position between VBUS and\\n"
    "any board rail, because the convenience those buy -- 'just power it from the bench over\\n"
    "USB' -- is exactly how two supplies end up back-feeding each other through a part nobody\\n"
    "re-examined. The board is powered from VBATT_PROT. A stuffing option here would be a\\n"
    "loaded gun with a DNP label on it.\\n"
    "Consequence to design AROUND, not to fix here: with USB attached and the vehicle off, the\\n"
    "module is unpowered and the port is dead. That is correct. Bench work uses a 12 V supply.\\n"
    "\\n"
    "CC1/CC2 get 5.1k Rd EACH -- two resistors, not one. The port is a device (UFP) and must\\n"
    "present Rd on whichever CC line the cable orientation lands on; a single resistor works\\n"
    "one way round and reads as an unattached port the other, which presents as an intermittent\\n"
    "cable rather than as a design error.\\n"
    "SBU1/SBU2 are unused and explicitly no-connected (F28).\\n"
    "\\n"
    "ESD: USBLC6-2SC6 on D+/D- with its VBUS pin tied to VBUS_USB. The connector faces the\\n"
    "outside world exactly as VBATT does -- politer, but the same class of exposure, and the\\n"
    "same reasoning that put a TVS on the battery input applies here at 1/1000th the energy."
)
NOTE3 = (
    "WHAT THIS SHEET OWES THE SEQUENCE (S7.2 / S7.3), drawn as NAMED NETS so BRINGUP.md stays\\n"
    "mechanically checkable against copper rather than by reading:\\n"
    "  PG_5V_D  PG_6V2_A  PG_1V2  PG_13V5P  PG_13V5N   -- rail readiness, all open-drain,\\n"
    "                                                     pulled up here where the reader is\\n"
    "  RAILMON_ALERT  TEMP_ALERT_N                     -- I2C monitor pair interrupts\\n"
    "  I2C0_SDA / I2C0_SCL                             -- bus pull-ups live HERE, once, with\\n"
    "                                                     the controller. Do not add more at\\n"
    "                                                     the far end; two pull-up pairs on one\\n"
    "                                                     bus is a rise-time bug that measures\\n"
    "                                                     fine and fails at temperature.\\n"
    "  DSP_RESET_N  ADC_PDN_N  DAC1_PDN_N  DAC2_PDN_N  -- step 3 and step 5 actors\\n"
    "  ADC_OVF                                         -- F29 clip flag, edge interrupt\\n"
    "  MUTE_EN                                         -- series photoMOS drive. ENERGISED to\\n"
    "                                                     pass: S7.4's zero-energy rule means\\n"
    "                                                     this net doing nothing IS mute.\\n"
    "  REMOTE_IN_SENSE  REMOTE_OUT_EN                  -- steps 1 and 6\\n"
    "  BM83_UART_TXD/RXD  BM83_MFB                     -- S5 host-mode control plane (F32)\\n"
    "  SPI_DSP_*                                       -- step 4 slave boot, 20 MHz capable\\n"
    "\\n"
    "The 12.5 ms bus-quiet window (F30) is FIRMWARE, not copper, and it is in BRINGUP.md. It\\n"
    "cannot be enforced by the schematic -- which is exactly why it is written down twice."
)

body = [place(*p) for p in PLACE]
for i, (nx, ny, txt) in enumerate([(620.0, 120.0, NOTE1), (620.0, 300.0, NOTE2),
                                   (620.0, 430.0, NOTE3)]):
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
\t\t(title "ODSP-12 :: Control -- ESP32-S3, USB-C debug, sequencing nets")
\t\t(date "2026-08-16")
\t\t(rev "A")
\t\t(comment 1 "ODSP12-MB-A")
\t\t(comment 2 "GPIO map is F13-closed: IO35-37 free on N8R2 only; IO19/20 USB only [HARD]")
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
