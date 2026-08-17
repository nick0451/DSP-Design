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
OC = "open_collector"; PO = "power_out"

ADAU1466 = [
    (1,"DGND",P,1),(17,"DGND",P,1),(19,"DGND",P,1),(25,"DGND",P,1),(36,"DGND",P,1),
    (37,"DGND",P,1),(54,"DGND",P,1),(55,"DGND",P,1),(72,"DGND",P,1),
    (6,"AGND",P,1),(14,"PGND",P,1),
    (2,"IOVDD",P,1),(18,"IOVDD",P,1),(38,"IOVDD",P,1),(56,"IOVDD",P,1),
    (20,"DVDD",P,1),(35,"DVDD",P,1),(53,"DVDD",P,1),(71,"DVDD",P,1),
    (7,"AVDD",P,1),(15,"PVDD",P,1),(16,"PLLFILT",PA,1),("EP","EP",P,1),
    # VDRIVE typed PASSIVE, not output. It is the base drive for an external PNP we do not
    # fit, and ADI directs "connect the VDRIVE pin to ground" when DVDD is supplied externally
    # (T1-41); grounded, it merely sinks ~100 uA from IOVDD (T1-62). Typed as an output it
    # collides with the GND net's PWR_FLAG -- an Output driving a Power output -- and ERC is
    # right about that: a pin the datasheet tells you to tie to a rail is a terminated node,
    # not a driver. The pin NAME still says VDRIVE, so nothing is hidden by the retype.
    (3,"VDRIVE",PA,1),
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
    (17,"TVDD",P,2),(18,"DVSS",P,2),
    # VDD18 is the INTERNAL LDO's OUTPUT, not a supply input (T1 + the F28 do-not-load note).
    # Typed power_in it reads as a rail nobody drives, and ERC says so correctly. power_out is
    # what it is: the part supplies this pin, the board only decouples it.
    (19,"VDD18",PO,2),
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
    (4,"SDTI1",I,2),(5,"SDTI2",I,2),
    # SDTI3/4 are typed INPUT, not bidirectional. Their TDMO alternate function is unused in
    # this design, and T1-52 requires unused SDTI pins to be tied to DVSS -- a bidirectional
    # type on a pin the datasheet tells you to ground reads to ERC as a driver into a power
    # net. Same reasoning as the ADAU1466's VDRIVE retype: type the pin for how the datasheet
    # says to USE it. The NAME keeps both functions so nothing is hidden.
    (6,"SDTI3/TDMO1",I,2),(7,"SDTI4/TDMO2",I,2),
    (8,"DSDR3",I,2),(9,"DSDL4",I,2),(10,"DSDR4",I,2),
    (11,"DZF/SMUTE",B,2),(48,"PDN",I,2),
    (13,"SDA/CDTI/TDM0",B,2),(14,"SCL/CCLK/TDM1",I,2),
    (15,"CAD0_I2C/CSN/DIF",I,2),(12,"CAD1/DCHAIN",I,2),
    (16,"PS/CAD0_SPI",I,2),(17,"I2C",I,2),
    (44,"LDOE",I,2),(45,"TVDD",P,2),(46,"DVSS",P,2),
    (47,"VDD18",PO,2),   # internal LDO OUTPUT, not a supply input -- same as the AK5574
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

# LM5156-Q1, 12-pin WSON with wettable flanks (DSS). TI SNVSBI7B Rev. B, Table 7-1 p.4,
# cross-checked against Figure 7-1 on the same page -- 100% agreement, all 12 + EP.
# "This pin must not be left floating. Connect to BIAS pin if not used." -- UVLO/SYNC/EN (12).
# EP is an ELECTRICAL ground connection ("must be connected to GND"), not thermal-only.
# DITHOFF (7): tied to VCC DISABLES dither; tied to GND ENABLES it. Note the polarity --
# the pin name reads as an active-high disable and the datasheet confirms that reading.
LM5156 = [
    (1,"BIAS",P,1),(2,"VCC",PO,1),(3,"GATE",O,1),(4,"GND",P,1),
    (5,"CS",I,1),(6,"COMP",O,1),(7,"DITHOFF",I,1),(8,"FB",I,1),
    (9,"SS",PA,1),(10,"RT",PA,1),(11,"PGOOD",OC,1),(12,"UVLO/SYNC/EN",I,1),
    ("EP","EP",P,1),
]

# LT3094, 12-lead DFN 3x3 (DD). ADI LT3094 Rev. B, Pin Functions p.15, cross-checked
# against the Pin Configuration diagram p.3 -- 100% agreement, all 12 + EP.
#
# BUILT AS A PROJECT SYMBOL RATHER THAN TAKEN FROM STOCK, for two reasons:
#   1. KiCad's LT3094xDD is an (extends "LT3093xMSE") alias, so its pin geometry lives under
#      a different basename. Re-parenting it would leave child symbols whose names do not
#      match the parent -- the exact shape of the silent-empty-schematic failure in the ledger.
#   2. The EP fact below deserves to live in the symbol, not in a comment on a sheet.
#
# *** EP (pin 13) IS **IN**, NOT GND. *** The LT3045 sitting beside it on this same sheet has
# EP = GND. The two parts are sold as a matched +/- pair, share the SET architecture and the
# 100 uA reference, and have DIFFERENT lead counts and OPPOSITE exposed-pad nets:
#     LT3045 "DD" = DFN-10 + EP,  EP = GND,  pins 5/6/7 = ILIM/PGFB/SET, no VIOC
#     LT3094 "DD" = DFN-12 + EP,  EP = IN,   pins 5/6/7 = PGFB/ILIM/VIOC
# Mirroring the positive channel to draw the negative one shorts IN to GND through the pad.
LT3094 = [
    (1,"IN",P,1),(2,"IN",P,1),("EP","EP (=IN)",P,1),
    (3,"EN/UV",I,1),(4,"PG",OC,1),(5,"PGFB",I,1),(6,"ILIM",PA,1),
    (7,"VIOC",O,1),(8,"SET",I,1),(9,"GND",P,1),(10,"OUTS",I,1),
    (11,"OUT",PO,1),(12,"OUT",PA,1),   # one node internally: pin 11 is the source, 12 is
]                                      # passive. Typing both power_out makes ERC read them
                                       # as two supplies shorted together (pin_to_pin).

# AP2127K-ADJ, SOT-23-5. Diodes Inc AP2127 datasheet, Pin Descriptions p.4 (SOT-23-5 column).
# Project symbol rather than stock for the LT3094 reason: KiCad's AP2127K-ADJ is an
# (extends "AP2204K-ADJ") alias, so its pins live under a different basename.
# V_REF = 0.8 V +/-2 % (0.784 / 0.800 / 0.816) -- V-23. ADJ is an FB pin inside the loop,
# NOT a reference input: the F36 distinction, and the reason a divider here is correct.
AP2127 = [
    (1,"VIN",P,1),(2,"GND",P,1),(3,"EN",I,1),(4,"ADJ",I,1),(5,"VOUT",PO,1),
]

# USBLC6-2SC6, SOT-23-6. THIRD instance of the extends-alias problem (after LT3094 and
# AP2127K-ADJ), and the first one ERC caught rather than the netlist: renaming the parent's
# children produced a lib_symbols cache that disagreed with the library, which KiCad reports
# as lib_symbol_mismatch. Aliasing to the parent instead would have put the parent's package
# (SOT-666) in the BOM. A project symbol has neither failure mode.
#
# *** PIN MAP IS T2 -- taken from KiCad's USBLC6-2P6 parent symbol, NOT from ST's datasheet,
# *** which st.com would not serve to this environment. Tracked as V-30. Low risk (the part is
# *** symmetric on I/O1 / I/O2 and only GND and VBUS are orientation-bearing) but NOT verified,
# *** and CLAUDE.md s8 rule 9 does not have a low-risk exemption.
USBLC6 = [
    (1,"I/O1",PA,1),(6,"I/O1",PA,1),(3,"I/O2",PA,1),(4,"I/O2",PA,1),
    (2,"GND",P,1),(5,"VBUS",P,1),
]

# PCF8574T and ULN2003A -- project symbols for the SAME reason as LT3094 / AP2127K-ADJ /
# USBLC6-2SC6: KiCad's are (extends ...) aliases, and renaming the parent's children yields a
# lib_symbols cache ERC rejects as lib_symbol_mismatch. Fifth and sixth instances; the pattern
# is now "any stock symbol whose package variant is an alias needs a project symbol."
# Maps read from the parent symbols and cross-checked against the standard pinouts.
PCF8574 = [
    (1,"A0",I,1),(2,"A1",I,1),(3,"A2",I,1),(8,"GND",P,1),(16,"VDD",P,1),
    (4,"P0",B,1),(5,"P1",B,1),(6,"P2",B,1),(7,"P3",B,1),
    (9,"P4",B,1),(10,"P5",B,1),(11,"P6",B,1),(12,"P7",B,1),
    (13,"~{INT}",OC,1),(14,"SCL",I,1),(15,"SDA",B,1),
]
ULN2003 = [
    (1,"I1",I,1),(2,"I2",I,1),(3,"I3",I,1),(4,"I4",I,1),
    (5,"I5",I,1),(6,"I6",I,1),(7,"I7",I,1),(8,"GND",P,1),
    (9,"COM",P,1),
    (10,"O7",OC,1),(11,"O6",OC,1),(12,"O5",OC,1),(13,"O4",OC,1),
    (14,"O3",OC,1),(15,"O2",OC,1),(16,"O1",OC,1),
]

# OPA1656, SOIC-8 dual. SEVENTH extends-alias instance (KiCad's OPA1656ID extends LM2904), so
# project symbol per the standing rule. Standard dual-opamp SOIC-8 pinout, cross-checked against
# the parent symbol: 1 OUT_A, 2 -IN_A, 3 +IN_A, 4 V-, 5 +IN_B, 6 -IN_B, 7 OUT_B, 8 V+.
# THREE UNITS -- A, B, and power -- so M14's reconstruct-and-no-overlap assertions apply.
OPA1656 = [
    (1,"OUT_A",O,1),(2,"-IN_A",I,1),(3,"+IN_A",I,1),
    (7,"OUT_B",O,2),(6,"-IN_B",I,2),(5,"+IN_B",I,2),
    (8,"V+",P,3),(4,"V-",P,3),
]

# 24.576 MHz LVCMOS oscillator -- the S3 [HARD] master clock. PN NOT PINNED (F56); the gate is
# on 02_dsp. Same shape as OPAMP_ADCDRV: the FOOTPRINT is T1 while the part is not, because the
# 4-pad LVCMOS oscillator pinout is an industry standard across every 2520/3225/5032 package --
# 1 OE(/ST/NC), 2 GND, 3 OUT, 4 VDD. Pin 1 is typed INPUT rather than passive deliberately: on
# an NC-variant it is harmless, on an OE or ST variant it is a control, and the sheet drives it
# to a defined level either way rather than assuming which variant arrives.
XO_LVCMOS = [
    (1,"OE",I,1),(2,"GND",P,1),(3,"OUT",O,1),(4,"VDD",P,1),
]

# ADC input level-shift / single-ended-to-differential driver (F50 copper, F52 part).
# PLACEHOLDER, but a DIFFERENT KIND of placeholder from the two below, and the difference is
# worth stating: the FOOTPRINT here is T1 while the PN is not. Every candidate that clears
# 06_analog_in's three selection inequalities ships on the standard dual-opamp SOIC-8 pinout
# -- 1 OUT_A, 2 -IN_A, 3 +IN_A, 4 V-, 5 +IN_B, 6 -IN_B, 7 OUT_B, 8 V+ -- so the land pattern
# and the netlist are both committable now and only the value line waits. Cross-checked
# against OPA1656 above, which is the same pinout and was EXCLUDED on VCM (see the sheet).
OPAMP_ADCDRV = [
    (1,"OUT_A",O,1),(2,"-IN_A",I,1),(3,"+IN_A",I,1),
    (7,"OUT_B",O,2),(6,"-IN_B",I,2),(5,"+IN_B",I,2),
    (8,"V+",P,3),(4,"V-",P,3),
]

# Mute elements. BOTH ARE PLACEHOLDERS PENDING THEIR DATASHEETS (V-14 / V-15) -- the topology
# is decided and drawable, the PARTS are not pinned, and CLAUDE.md s8 rule 9 forbids inventing
# pin numbers. These carry the FUNCTION so the netlist and the fail-safe walk are checkable;
# the footprints and exact pin order land when the datasheets do.
MUTE_SERIES = [                       # Form A photoMOS, energised-to-pass (S6.4 [HARD])
    (1,"ANODE",I,1),(2,"CATHODE",I,1),(3,"DRAIN1",PA,1),(4,"DRAIN2",PA,1),
]
MUTE_SHUNT = [                        # depletion pair, back-to-back SOURCE-to-SOURCE
    (1,"G",I,1),(2,"D1",PA,1),(3,"D2",PA,1),
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
    "LM5156-Q1": dict(pins=LM5156, n=12, ep=True, units=1,
        value="LM5156QDSSRQ1", mfr="Texas Instruments",
        fp="ODSP12:TI_WSON-12_3x2mm_DSS",
        desc="3.5-60 V boost/SEPIC/flyback controller, 2.2 MHz, DRSS, AEC-Q100",
        ds="TI SNVSBI7B Rev. B"),
    "LT3094": dict(pins=LT3094, n=12, ep=True, units=1,
        value="LT3094EDD", mfr="Analog Devices",
        fp="ODSP12:ADI_DFN-12-1EP_3x3mm_P0.45mm_EP_IS_IN",
        desc="-20 V, 500 mA ultralow-noise negative LDO. EXPOSED PAD IS IN, NOT GND",
        ds="ADI LT3094 Rev. B"),
    "AP2127K-ADJ": dict(pins=AP2127, n=5, ep=False, units=1,
        value="AP2127K-ADJTRG1", mfr="Diodes Incorporated",
        fp="Package_TO_SOT_SMD:SOT-23-5",
        desc="300 mA low-noise adjustable LDO, VREF 0.8 V +/-2 %",
        ds="Diodes AP2127"),
    "USBLC6-2SC6": dict(pins=USBLC6, n=6, ep=False, units=1,
        value="USBLC6-2SC6", mfr="STMicroelectronics",
        fp="Package_TO_SOT_SMD:SOT-23-6",
        desc="2-line ESD array for USB2.0, VBUS clamp. PIN MAP T2 -- see V-30",
        ds="ST USBLC6-2SC6 (NOT HELD -- V-30)"),
    "PCF8574T": dict(pins=PCF8574, n=16, ep=False, units=1,
        value="PCF8574T", mfr="NXP", fp="Package_SO:SO-16_3.9x9.9mm_P1.27mm",
        desc="8-bit I2C GPIO expander, addr 0x20 with A2:A0=000",
        ds="NXP PCF8574"),
    "ULN2003A": dict(pins=ULN2003, n=16, ep=False, units=1,
        value="ULN2003A", mfr="Texas Instruments", fp="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm",
        desc="7ch Darlington sink array with internal freewheel diodes (COM)",
        ds="TI ULN2003A"),
    "OPA1656": dict(pins=OPA1656, n=8, ep=False, units=3,
        value="OPA1656IDR", mfr="Texas Instruments", fp="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        desc="Dual JFET audio op-amp, 2.9 nV/rtHz, rail-to-rail out to 250 mV",
        ds="TI SBOS893"),
    "XO_LVCMOS": dict(pins=XO_LVCMOS, n=4, ep=False, units=1,
        value="PLACEHOLDER F56", mfr="TBD", fp="Oscillator:Oscillator_SMD_SeikoEpson_SG210_4pin_3.2x2.5mm",
        desc="24.576 MHz LVCMOS XO, 3.3 V -- the S3 [HARD] master clock",
        ds="F56 -- gate on 02_dsp: duty 25-75 %, phase noise, +/-ppm over -20..+70 degC"),
    "OPAMP_ADCDRV": dict(pins=OPAMP_ADCDRV, n=8, ep=False, units=3,
        value="OPA2320AIDR", mfr="Texas Instruments", fp="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        desc="Dual RRIO CMOS op-amp, 8.5 nV/rtHz at 1 kHz, ADC level-shift + SE-to-differential",
        ds="TI SBOS513F"),
    "MUTE_PHOTOMOS": dict(pins=MUTE_SERIES, n=4, ep=False, units=1,
        value="TLP3475", mfr="Toshiba", fp="ODSP12:Toshiba_VSON4_11-2D1A",
        desc="1-Form-A photorelay, 50 V off-state, Ron 1.5R max, Coff 20 pF max",
        ds="Toshiba TLP3475 2023-05-24"),
    "MUTE_DEPFET": dict(pins=MUTE_SHUNT, n=3, ep=False, units=1,
        value="PLACEHOLDER V-15", mfr="TBD", fp="ODSP12:TBD_V15",
        desc="Depletion NMOS pair, back-to-back source-to-source. PN PENDING V-15",
        ds="V-15 -- NOT YET READ"),
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
