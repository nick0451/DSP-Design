# ODSP12 symbol library generator -- ADAU1466, AK5574, AK4458.
#
# SOURCES OF TRUTH (all read at figure level per STATE.md M2, never text-extracted):
#   ADAU1466 : adau1462-1466.pdf Rev. C, Table 18 pp.18-21, cross-checked vs Figure 11 p.18
#   AK5574   : AK5574_AKM.pdf "Pin Functions" pp.5-6  (015016764-E-03)
#   AK4458   : AK4458_AKM.pdf "Pin Functions" pp.8-9  (014011794-E-02)
#
# Pin names use the I2C-mode function first, since T1-27 fixes all AKM parts to I2C.
# Alternate mode names are kept in the pin name so the schematic shows what a strap does.
import os

VER = "20251024"   # verified from share/kicad/symbols/Device.kicad_sym
DEST = r"c:\Users\nick\Documents\Claude Project\DSP Design\hw\lib\ODSP12.kicad_sym"

P = "power_in"; I = "input"; O = "output"; B = "bidirectional"; PA = "passive"

ADAU1466 = [
    (1,"DGND",P,1),(17,"DGND",P,1),(19,"DGND",P,1),(25,"DGND",P,1),(36,"DGND",P,1),
    (37,"DGND",P,1),(54,"DGND",P,1),(55,"DGND",P,1),(72,"DGND",P,1),
    (6,"AGND",P,1),(14,"PGND",P,1),
    (2,"IOVDD",P,1),(18,"IOVDD",P,1),(38,"IOVDD",P,1),(56,"IOVDD",P,1),
    (20,"DVDD",P,1),(35,"DVDD",P,1),(53,"DVDD",P,1),(71,"DVDD",P,1),
    (7,"AVDD",P,1),(15,"PVDD",P,1),(16,"PLLFILT",PA,1),(3,"VDRIVE",O,1),("EP","EP",P,1),
    (59,"SDATA_IN0",I,2),(57,"BCLK_IN0",B,2),(58,"LRCLK_IN0/MP10",B,2),
    (62,"SDATA_IN1",I,2),(60,"BCLK_IN1",B,2),(61,"LRCLK_IN1/MP11",B,2),
    (67,"SDATA_IN2",I,2),(65,"BCLK_IN2",B,2),(66,"LRCLK_IN2/MP12",B,2),
    (70,"SDATA_IN3",I,2),(68,"BCLK_IN3",B,2),(69,"LRCLK_IN3/MP13",B,2),
    (41,"SDATA_OUT0",O,2),(40,"BCLK_OUT0",B,2),(39,"LRCLK_OUT0/MP4",B,2),
    (44,"SDATA_OUT1",O,2),(43,"BCLK_OUT1",B,2),(42,"LRCLK_OUT1/MP5",B,2),
    (49,"SDATA_OUT2",O,2),(48,"BCLK_OUT2",B,2),(47,"LRCLK_OUT2/MP8",B,2),
    (52,"SDATA_OUT3",O,2),(51,"BCLK_OUT3",B,2),(50,"LRCLK_OUT3/MP9",B,2),
    (45,"MP6",B,2),(46,"MP7",B,2),
    (21,"XTALIN/MCLK",I,3),(22,"XTALOUT",O,3),(23,"CLKOUT",O,3),(24,"~{RESET}",I,3),
    (34,"SELFBOOT",I,3),(33,"~{SS}/ADDR0",I,3),(31,"SCLK/SCL",I,3),(32,"MOSI/ADDR1",I,3),
    (30,"MISO/SDA",B,3),(26,"SS_M/MP0",B,3),(27,"MOSI_M/MP1",B,3),
    (28,"SCL_M/SCLK_M/MP2",B,3),(29,"SDA_M/MISO_M/MP3",B,3),
    (4,"SPDIFIN",I,3),(5,"SPDIFOUT",O,3),(63,"THD_M",PA,3),(64,"THD_P",PA,3),
    (8,"AUXADC0",I,3),(9,"AUXADC1",I,3),(10,"AUXADC2",I,3),
    (11,"AUXADC3",I,3),(12,"AUXADC4",I,3),(13,"AUXADC5",I,3),
]

AK5574 = [
    # unit 1: analog
    (47,"AIN1P",I,1),(48,"AIN1N",I,1),(5,"AIN2P",I,1),(4,"AIN2N",I,1),
    (8,"AIN3P",I,1),(9,"AIN3N",I,1),(14,"AIN4P",I,1),(13,"AIN4N",I,1),
    (3,"VREFH1",I,1),(2,"VREFL1",I,1),(10,"VREFH2",I,1),(11,"VREFL2",I,1),
    (6,"AVDD",P,1),(7,"AVSS",P,1),(1,"NC",PA,1),(12,"NC",PA,1),
    # unit 2: digital
    (16,"MCLK",I,2),(25,"BICK",B,2),(26,"LRCK",B,2),(27,"TDMIN",I,2),
    (28,"SDTO1",O,2),(29,"SDTO2",O,2),(30,"OVF",O,2),
    (24,"MSN",I,2),(20,"PDN",I,2),(15,"TEST",I,2),
    (31,"SDA/CKS0",B,2),(33,"SCL/CKS2",I,2),(32,"CAD0_I2C/CKS1",I,2),(34,"CAD1/CKS3",I,2),
    (41,"PSN/CAD0_SPI",I,2),(42,"I2C",I,2),
    (21,"PW0",I,2),(22,"PW1",I,2),(23,"PW2",I,2),
    (35,"SLOW",I,2),(36,"SD",I,2),(37,"DIF0",I,2),(38,"DIF1",I,2),
    (39,"TDM0",I,2),(40,"TDM1",I,2),(43,"DP",I,2),(44,"HPFE",I,2),
    (45,"LDOE",I,2),(46,"ODP",I,2),
    (17,"TVDD",P,2),(18,"DVSS",P,2),(19,"VDD18",P,2),
]

AK4458 = [
    # unit 1: analog
    (18,"AOUTL1P",O,1),(19,"AOUTL1N",O,1),(23,"AOUTR1P",O,1),(22,"AOUTR1N",O,1),
    (24,"AOUTL2P",O,1),(25,"AOUTL2N",O,1),(29,"AOUTR2P",O,1),(28,"AOUTR2N",O,1),
    (32,"AOUTL3P",O,1),(33,"AOUTL3N",O,1),(37,"AOUTR3P",O,1),(36,"AOUTR3N",O,1),
    (38,"AOUTL4P",O,1),(39,"AOUTL4N",O,1),(43,"AOUTR4P",O,1),(42,"AOUTR4N",O,1),
    (21,"VREFH1",I,1),(20,"VREFL1",I,1),(27,"VREFH2",I,1),(26,"VREFL2",I,1),
    (34,"VREFH3",I,1),(35,"VREFL3",I,1),(40,"VREFH4",I,1),(41,"VREFL4",I,1),
    (31,"AVDD",P,1),(30,"AVSS",P,1),
    # unit 2: digital
    (1,"MCLK",I,2),(2,"BICK",I,2),(3,"LRCK",I,2),
    (4,"SDTI1",I,2),(5,"SDTI2",I,2),(6,"SDTI3/TDMO1",B,2),(7,"SDTI4/TDMO2",B,2),
    (8,"DSDR3",I,2),(9,"DSDL4",I,2),(10,"DSDR4",I,2),
    (11,"DZF/SMUTE",B,2),(48,"PDN",I,2),
    (13,"SDA/CDTI/TDM0",B,2),(14,"SCL/CCLK/TDM1",I,2),
    (15,"CAD0_I2C/CSN/DIF",I,2),(12,"CAD1/DCHAIN",I,2),
    (16,"PS/CAD0_SPI",I,2),(17,"I2C",I,2),
    (44,"LDOE",I,2),(45,"TVDD",P,2),(46,"DVSS",P,2),(47,"VDD18",P,2),
]

# BM83SM1. Pin names below are the HOST-MODE / our-config function.
# The module ships pre-configured in EMBEDDED mode (datasheet p.15 note), so several
# pin meanings differ from this symbol until the module is configured -- pins whose
# function is config-dependent carry a "*" suffix in the name so the schematic shows it.
BM83 = [
    # unit 1: power + audio
    (23,"BAT_IN",P,1),(22,"ADAP_IN",P,1),(24,"SYS_PWR*NC",P,1),(25,"VDD_IO*NC",P,1),
    (15,"MICBIAS",P,1),(16,"GND",P,1),(50,"GND",P,1),
    (5,"MCLK1",O,1),(3,"SCLK1",B,1),(2,"RFS1",B,1),(1,"DR1",I,1),(4,"DT1",O,1),
    (8,"AOHPL",O,1),(6,"AOHPR",O,1),(7,"AOHPM",O,1),
    (12,"AIL",I,1),(11,"AIR",I,1),
    (14,"MICP1",I,1),(13,"MICN1",I,1),(10,"MICP2",I,1),(9,"MICN2",I,1),
    (17,"DMIC_CLK",O,1),(18,"DMIC1_R",I,1),(19,"DMIC1_L",I,1),
    # unit 2: host interface + GPIO
    (43,"RST_N",I,2),(26,"PWR_MFB",I,2),
    (29,"P8_6/UART_RXD",B,2),(30,"P8_5/UART_TXD",B,2),
    (48,"P3_7/UART_CTS",B,2),(31,"P3_4/UART_RTS*CFG",B,2),
    (49,"P0_0/UART_TX_IND*",B,2),
    (46,"P1_2/TDI_CPU/SCL",B,2),(47,"P1_3/TCK_CPU/SDA",B,2),
    (37,"DP",B,2),(36,"DM",B,2),
    (32,"LED1",I,2),(34,"LED2",I,2),
    (27,"SK1_AMB_DET",I,2),(28,"SK2_KEY_AD",I,2),
    (20,"P3_2*",B,2),(21,"P2_6",B,2),(33,"P0_2*",B,2),(35,"P0_6",B,2),
    (38,"P0_3*",B,2),(39,"P2_7*",B,2),(40,"P0_5*",B,2),(41,"P1_6/PWM1",B,2),
    (42,"P2_3",B,2),(44,"P0_1*",B,2),(45,"P0_7",B,2),
]

OC = "open_collector"; PO = "power_out"

# LM61460-Q1, 14-pin VQFN-HR (RJR). TI SNVSB70F, Table 7-1 p.4.
# "Do not float" pins per the datasheet: FB (4), RT (6), EN/SYNC (7) -- F28 dispositions required.
LM61460 = [
    (8,"VIN1",P,1),(12,"VIN2",P,1),(9,"PGND1",P,1),(11,"PGND2",P,1),(3,"AGND",P,1),
    (10,"SW",O,1),(14,"CBOOT",PA,1),(13,"RBOOT",PA,1),
    (7,"EN/SYNC",I,1),(4,"FB",I,1),(6,"RT",PA,1),
    (5,"PGOOD",OC,1),            # open-drain: needs a pull-up (F34)
    (2,"VCC",PO,1),              # internal LDO output -- "do not connect to any external loads"
    (1,"BIAS",P,1),
]

# INA1650, 14-pin TSSOP (PW). TI SBOS818B, Pin Functions p.3.
INA1650 = [
    (1,"VCC",P,1),(14,"VEE",P,1),
    (2,"IN+A",I,1),(4,"IN-A",I,1),(3,"COM_A",I,1),(13,"OUT_A",O,1),(12,"REF_A",I,1),
    (7,"IN+B",I,1),(5,"IN-B",I,1),(6,"COM_B",I,1),(8,"OUT_B",O,1),(9,"REF_B",I,1),
    (11,"VMID_IN",I,1),(10,"VMID_OUT",O,1),
]

# LMK1C1104, 8-pin TSSOP (PW). TI SNAS791D, Figure 6-4 p.3.
LMK1C1104 = [
    (1,"CLKIN",I,1),(2,"1G",I,1),
    (3,"Y0",O,1),(8,"Y1",O,1),(5,"Y2",O,1),(7,"Y3",O,1),
    (6,"VDD",P,1),(4,"GND",P,1),
]

PARTS = {
    "ADAU1466": dict(pins=ADAU1466, n=72, ep=True, units=3,
        value="ADAU1466WBCPZ300", mfr="Analog Devices",
        fp="ODSP12:ADI_LFCSP-72_10x10mm_P0.5mm_EP5.3x5.3mm",
        desc="SigmaDSP 32-bit audio processor, 72-LFCSP",
        ds="adau1462-1466.pdf Rev. C"),
    "AK5574": dict(pins=AK5574, n=48, ep=False, units=2,
        value="AK5574EN", mfr="Asahi Kasei Microdevices",
        fp="ODSP12:AKM_LQFP-48_7x7mm_P0.5mm",
        desc="4ch 32-bit differential ADC, 121 dB, TDM",
        ds="AK5574 015016764-E-03"),
    "AK4458": dict(pins=AK4458, n=48, ep=False, units=2,
        value="AK4458VN", mfr="Asahi Kasei Microdevices",
        fp="ODSP12:AKM_LQFP-48_7x7mm_P0.5mm",
        desc="8ch 32-bit DAC, 115 dB, TDM8",
        ds="AK4458 014011794-E-02"),
    "BM83SM1": dict(pins=BM83, n=50, ep=False, units=2,
        value="BM83SM1", mfr="Microchip",
        fp="ODSP12:Microchip_BM83SM1_Module",
        desc="Bluetooth 5.0 stereo audio module, A2DP sink, aptX-HD/AAC",
        ds="BM83 DS70005402G"),
    "LM61460-Q1": dict(pins=LM61460, n=14, ep=False, units=1,
        value="LM61460AQRJRRQ1", mfr="Texas Instruments",
        fp="ODSP12:TI_VQFN-HR-14_RJR",
        desc="3-36 V, 6 A synchronous buck, low EMI, AEC-Q100",
        ds="TI SNVSB70F"),
    "INA1650": dict(pins=INA1650, n=14, ep=False, units=1,
        value="INA1650PW", mfr="Texas Instruments",
        fp="Package_SO:TSSOP-14_4.4x5mm_P0.65mm",
        desc="Dual-channel high-CMRR line receiver",
        ds="TI SBOS818B"),
    "LMK1C1104": dict(pins=LMK1C1104, n=8, ep=False, units=1,
        value="LMK1C1104PWR", mfr="Texas Instruments",
        fp="Package_SO:TSSOP-8_3x3mm_P0.65mm",
        desc="4-output LVCMOS clock buffer, 7.5 fs additive jitter",
        ds="TI SNAS791D"),
}

for name, d in PARTS.items():
    nums = [p[0] for p in d["pins"]]
    assert len(nums) == len(set(nums)), f"{name}: duplicate pin number"
    expected = set(range(1, d["n"] + 1)) | ({"EP"} if d["ep"] else set())
    got = set(nums)
    assert got == expected, (f"{name}: missing {sorted(expected-got, key=str)}, "
                             f"extra {sorted(got-expected, key=str)}")
    print(f"  {name}: {len(nums)} pins, 1..{d['n']}{' + EP' if d['ep'] else ''}, each exactly once  OK")

def esc(s): return s.replace('"', '\\"')

def unit_block(sym, unit, pins):
    half = (len(pins) + 1) // 2
    left, right = pins[:half], pins[half:]
    h = (max(len(left), len(right)) + 1) * 2.54
    w, top = 63.5, (max(len(left), len(right)) + 1) * 2.54 / 2
    out = [f'\t\t(symbol "{sym}_{unit}_0"',
           f'\t\t\t(rectangle (start {-w/2} {top}) (end {w/2} {-top})',
           '\t\t\t\t(stroke (width 0.254) (type default))',
           '\t\t\t\t(fill (type background))', '\t\t\t)', '\t\t)',
           f'\t\t(symbol "{sym}_{unit}_1"']
    for side, pins_side, x, rot in (("L", left, -w/2 - 5.08, 0), ("R", right, w/2 + 5.08, 180)):
        for i, (num, nm, et, _) in enumerate(pins_side):
            y = top - 2.54 * (i + 1)
            out += [f'\t\t\t(pin {et} line (at {x} {y} {rot}) (length 5.08)',
                    f'\t\t\t\t(name "{esc(nm)}" (effects (font (size 1.27 1.27))))',
                    f'\t\t\t\t(number "{num}" (effects (font (size 1.27 1.27))))', '\t\t\t)']
    out.append('\t\t)')
    return "\n".join(out)

lines = ["(kicad_symbol_lib", f'\t(version {VER})',
         '\t(generator "odsp12-symgen")', '\t(generator_version "10.0")']
for name, d in PARTS.items():
    lines += [f'\t(symbol "{name}"', '\t\t(pin_names (offset 0.254))',
              '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)']
    props = [("Reference","U",0,0),("Value",d["value"],0,-2.54),("Footprint",d["fp"],0,-5.08),
             ("Datasheet",d["ds"],0,-7.62),("Description",d["desc"],0,-10.16),
             ("MFR",d["mfr"],0,-12.7),("MPN",d["value"],0,-15.24)]
    for k, v, x, y in props:
        hide = "" if k in ("Reference", "Value") else "\n\t\t\t\t(hide yes)"
        lines += [f'\t\t(property "{k}" "{esc(v)}"', f'\t\t\t(at {x} {y} 0)',
                  f'\t\t\t(effects (font (size 1.27 1.27)){hide})', '\t\t)']
    for u in range(1, d["units"] + 1):
        lines.append(unit_block(name, u, [p for p in d["pins"] if p[3] == u]))
    lines += ['\t\t(embedded_fonts no)', '\t)']
lines.append(")")

os.makedirs(os.path.dirname(DEST), exist_ok=True)
with open(DEST, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")
print("wrote", DEST, f"({len(PARTS)} symbols)")
