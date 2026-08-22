"""Footprint-pass guards. Adversary 055; built BEFORE the first footprint exists.

Every guard here takes DATA, not generator state (CLAUDE.md M27), so each can be handed a
known defect without running the thing that produces its input. Every guard has a negative
test below built from a part already read at figure level (M9) -- a guard that has never
fired on the real defect is not verified.

WHAT THIS SET DOES NOT COVER, stated because a completeness claim needs its gaps named:
PAD-1 ORIENTATION. None of G1-G3 catches a footprint rotated 180 degrees, which is the
classic footprint defect. The information lives in the package drawing's index marker --
geometry, not a table -- and there is no data-shaped test for it here.
"""


class FootprintDefect(AssertionError):
    pass


# --- G1: the pad set must equal the pin set ------------------------------------------
# SET equality, not count: symbol {1,2,3} against footprint {1,2,4} has the right count
# and the wrong pads. F90 is the live case -- DN2540's "3-LEAD" tables number FOUR pins,
# pin 4 being the mounting tab, so a 3-pin symbol leaves a copper pad with no net.
def assert_pad_set_matches_pins(symbol_pins, footprint_pads, refdes, tag=""):
    sp, fp = set(map(str, symbol_pins)), set(map(str, footprint_pads))
    if sp != fp:
        raise FootprintDefect(
            f"G1{tag} {refdes}: pad set != pin set. "
            f"pads with no symbol pin: {sorted(fp - sp) or 'none'}; "
            f"pins with no pad: {sorted(sp - fp) or 'none'}. "
            f"A pad with no net is not an error to ERC -- it is silence.")
    return len(sp)


# --- G2: a bonded tab must sit on its twin's net --------------------------------------
# THE ONE TO BUILD IF ONLY ONE GETS BUILT. Its failure mode is not an open, it is a SHORT
# THROUGH THE DIE, and it carries F76's exact signature: every pin involved is typed
# `passive`, so ERC has nothing to disagree with and the netlist exports cleanly.
# A TVS whose tab lands on the cathode net is a dead short across the part facing the
# battery.
# --- G2b: an EXPOSED PAD's correct net is not always a value ---------------------------
# Adversary 057. The three parts about to be drawn have exposed pads under THREE DIFFERENT
# conventions, so a single "tab -> twin's net" assertion would either fire wrongly or need
# an exemption -- and an exemption is how a guard stops guarding.
#
#   FIXED      ADAU1466 EP -> GND, mandatory. And note the trap: the pin table's Type column
#              says "None" while the same row's description says "must be grounded". The
#              machine-readable field and the human-readable field DISAGREE, and a generator
#              reading the type gets "no electrical function" for a mandatory ground.
#   EITHER-OR  AK5574 EP: "must be open or connected to the ground" (p.4). Both legal.
#   EITHER-OR  AK4458 EP: same wording, DIFFERENT CONSEQUENCE -- grounded buys 20 degC of
#   +RATING    operating range (-40..+105 grounded vs -40..+85 open, p.7). The constraint is
#              not on the net at all: it is that the net choice and the TEMPERATURE RATING
#              must agree, and they live in different documents. Not guarded here; recorded.
EP_RULE = {
    "ODSP12:ADAU1466": ("fixed", {"GND"},
                        "Rev C p.18/p.21 -- MUST be grounded; pin-table Type says 'None'"),
    "ODSP12:AK5574":   ("either", {"GND", None},
                        "p.4 -- 'must be open or connected to the ground'"),
    "ODSP12:AK4458":   ("either", {"GND", None},
                        "p.7 -- open = -40..+85 C, grounded = -40..+105 C. CHOICE, not value"),
}


def assert_exposed_pad(libid, ep_net, refdes, tag=""):
    if libid not in EP_RULE:
        return None
    kind, allowed, why = EP_RULE[libid]
    if ep_net not in allowed:
        raise FootprintDefect(
            f"G2b{tag} {refdes} ({libid}): exposed pad on {ep_net!r}; permitted "
            f"{sorted(x or 'unconnected' for x in allowed)}. {why}")
    return kind


BONDED = {                      # libid -> [(tab_pad, twin_pad, what the datasheet says)]
    "ODSP12:DN2540_SOT89":   [("4", "2", "Table 3-2: pin 2 Drain, pin 4 Drain")],
    "ODSP12:SM8S_DO218AC":   [("TAB", "A", "doc 98647 p.1: 'Polarity: heatsink is anode'")],
    "ODSP12:TLP3475_VSON4":  [("4", "3", "p.1: pin 3 Drain, pin 4 Drain")],
}


def assert_bonded_tabs_share_net(libid, nets, refdes, tag=""):
    bad = []
    for tab, twin, why in BONDED.get(libid, []):
        if tab in nets and twin in nets and nets[tab] != nets[twin]:
            bad.append(f"pad {tab} -> {nets[tab]!r} but pad {twin} -> {nets[twin]!r} ({why})")
    if bad:
        raise FootprintDefect(
            f"G2{tag} {refdes} ({libid}): BONDED TAB ON THE WRONG NET -- this is a short "
            f"through the die, not an open, and ERC cannot see it:\n  " + "\n  ".join(bad))
    return True


# --- G3: where a datasheet ties a RATING to pad geometry, the land must match ----------
# Narrow by design -- it applies only to parts whose documents say so. The SM8S is the case
# that exists: REQUIREMENTS 12 ties the load-dump capability table to "the recommended pad
# size as listed in the datasheet" and states that shrinking it MAKES THE CRITERION FALSE.
# T1-91: 15.30 x 10.70 mm carries across DO-218AB -> AC unchanged.
RATED_LAND = {"ODSP12:SM8S_DO218AC": (15.30, 10.70,
              "REQUIREMENTS 12 + T1-91 -- pad size is an ELECTRICAL input, not an outline")}


def assert_rated_land(libid, drawn_w, drawn_h, refdes, tol=0.05, tag=""):
    if libid not in RATED_LAND:
        return None
    w, h, why = RATED_LAND[libid]
    if abs(drawn_w - w) > tol or abs(drawn_h - h) > tol:
        raise FootprintDefect(
            f"G3{tag} {refdes}: land {drawn_w} x {drawn_h} mm != rated {w} x {h} mm. {why}. "
            f"Shrinking this pad does not make the part smaller -- it makes an acceptance "
            f"criterion false.")
    return (w, h)


# --- G4: PROVENANCE, because pad-1 orientation is not testable but its PROVENANCE is ----
# Adversary 059. We had both recorded pad-1 orientation as uncovered: the information lives in a
# package drawing's index marker, which is geometry, not a table. True of the ORIENTATION. NOT
# true of whether anybody checked it.
#
#   ipc_generated   pin 1 is fixed by the standard -> correct BY CONSTRUCTION. Record that
#                   construction was used; no marker needed.
#   vendor_supplied orientation is the vendor's and the risk transfers with it.
#   hand_built      the ONLY case where a human placed pad 1, and the only one needing a marker.
#
# THIS IS A WEAKER GUARANTEE THAN G1-G3 AND IS LABELLED AS SUCH: it cannot tell you a hand-built
# footprint is RIGHT. It can only tell you nobody looked. It converts a silent gap into a visible
# one rather than closing it.
SOURCES = {"vendor_supplied", "ipc_generated", "hand_built"}


def assert_footprint_provenance(refdes, source, verified_by=None, tag=""):
    if source not in SOURCES:
        raise FootprintDefect(
            f"G4{tag} {refdes}: unknown provenance {source!r}; expected one of {sorted(SOURCES)}")
    if source == "hand_built" and not verified_by:
        raise FootprintDefect(
            f"G4{tag} {refdes}: HAND-BUILT with no orientation-verification marker. Pad-1 "
            f"orientation is not machine-checkable, so the hand-built path must carry a "
            f"signature saying a human checked it. This does not prove it is right -- it "
            f"proves someone looked.")
    return source


# --- G5: every non-power component in the EXPORTED NETLIST carries a footprint ---------
# F109. G1-G4 all check a footprint's CONTENT. None of them checks that the footprint is
# REACHABLE -- and on 2026-08-22 the netlist exported 536 components with ZERO footprints,
# because gen_symbols.py wrote the property into the LIBRARY SYMBOL and the sheet generators
# emitted instances carrying only Reference and Value. Every content check would have passed
# on a library nothing could reach.
#
# M27: this guard takes the EXPORTED NETLIST, not generator state. The generator layer is
# where the bug was, so a guard reading generator state would have been blind to it by
# construction -- it would have found the footprint exactly where the bug put it.
#
# Takes (refdes, footprint) pairs so it can be handed a known-bad netlist without running
# kicad-cli. Power symbols (#PWR/#FLG) legitimately have none and are excluded BY PREFIX.
def assert_netlist_footprints(components, tag="", allow_missing=()):
    allow = set(allow_missing)
    missing = sorted(ref for ref, fp in components
                     if not ref.startswith("#") and not (fp or "").strip()
                     and ref not in allow)
    if missing:
        raise FootprintDefect(
            f"G5{tag}: {len(missing)} of {len(components)} components export with NO footprint: "
            f"{missing[:8]}{' ...' if len(missing) > 8 else ''}. "
            f"A footprint that exists in the library but not on the instance is unreachable: "
            f"'Update PCB from Schematic' places nothing and G1 parity is not failing, it is "
            f"UNMEASURABLE. Checking the library is the wrong test -- check the export.")
    return len(components)


# --- M9 NEGATIVE TESTS: each guard is fed a real defect before it is trusted -----------
def _must_fire(fn, label):
    try:
        fn()
    except FootprintDefect:
        return True
    raise SystemExit(f"GUARD IS DEFECTIVE ({label}): it passed a known defect. M9 not satisfied.")


def self_test(verbose=True):
    # G1 -- F90's real case: DN2540 SOT-89 symbol carries 3 pins, footprint has 4 pads.
    _must_fire(lambda: assert_pad_set_matches_pins(["1", "2", "3"], ["1", "2", "3", "4"],
                                                   "Q101"), "G1")
    assert_pad_set_matches_pins(["1", "2", "3", "4"], ["1", "2", "3", "4"], "Q101")  # control
    # G1 -- same count, wrong members. The case a count check passes.
    _must_fire(lambda: assert_pad_set_matches_pins(["1", "2", "3"], ["1", "2", "4"],
                                                   "Q102"), "G1-samecount")

    # G2 -- DN2540 tab off its twin, then the SM8S case, which is the worst on the board.
    _must_fire(lambda: assert_bonded_tabs_share_net(
        "ODSP12:DN2540_SOT89", {"2": "MUTED1", "4": "GND"}, "Q103"), "G2-dn2540")
    _must_fire(lambda: assert_bonded_tabs_share_net(
        "ODSP12:SM8S_DO218AC", {"A": "GND", "TAB": "VBATT_PROT"}, "D1"), "G2-sm8s")
    assert_bonded_tabs_share_net("ODSP12:SM8S_DO218AC",
                                 {"A": "GND", "TAB": "GND"}, "D1")               # control
    assert_bonded_tabs_share_net("ODSP12:TLP3475_VSON4",
                                 {"3": "AMP1_OUT", "4": "AMP1_OUT"}, "K11")      # control

    # G5 -- F109's real case: the 2026-08-22 export, 536 components and not one footprint.
    _must_fire(lambda: assert_netlist_footprints(
        [("C102", ""), ("U51", ""), ("R2", "")]), "G5-f109")
    # G5 -- the case a spot-check passes: ONE part missing among many that are fine.
    _must_fire(lambda: assert_netlist_footprints(
        [("U51", "ODSP12:AKM_LQFP-48_7x7mm_P0.5mm"), ("C102", "Capacitor_SMD:C_0603_1608Metric"),
         ("R2", "   ")]), "G5-one-missing")
    # controls: all present, and power symbols correctly ignored.
    assert_netlist_footprints([("U51", "ODSP12:AKM_LQFP-48_7x7mm_P0.5mm"),
                               ("#PWR01", ""), ("#FLG00", "")])

    # G3 -- a shrunken SM8S land.
    _must_fire(lambda: assert_rated_land("ODSP12:SM8S_DO218AC", 14.0, 10.0, "D1"), "G3")
    assert_rated_land("ODSP12:SM8S_DO218AC", 15.30, 10.70, "D1")                 # control

    # G2b -- the three exposed-pad conventions, from 057.
    _must_fire(lambda: assert_exposed_pad("ODSP12:ADAU1466", None, "U1"), "G2b-adau-open")
    _must_fire(lambda: assert_exposed_pad("ODSP12:AK5574", "+5V_A", "U40"), "G2b-ak5574")
    assert_exposed_pad("ODSP12:ADAU1466", "GND", "U1")            # control
    assert_exposed_pad("ODSP12:AK5574", None, "U40")              # control: open is legal
    assert_exposed_pad("ODSP12:AK4458", "GND", "U60")             # control: grounded is legal

    # G4 -- provenance. Hand-built with no marker must fire; the other two paths need none.
    _must_fire(lambda: assert_footprint_provenance("U99", "hand_built"), "G4-unsigned")
    _must_fire(lambda: assert_footprint_provenance("U99", "guessed"), "G4-unknown-source")
    assert_footprint_provenance("U1", "ipc_generated")                       # control
    assert_footprint_provenance("U30", "vendor_supplied")                    # control
    assert_footprint_provenance("Q1", "hand_built", verified_by="operator")  # control

    if verbose:
        print("  footprint guards: G1/G2/G2b/G3/G4/G5 negative tests ALL FIRED, controls passed "
              "(M9 satisfied)")
        print("  PARTIAL: pad-1 orientation -- G4 checks PROVENANCE, not geometry.")
        print("           It proves someone looked, not that they were right.")
        print("  UNCOVERED: BM83SM1 keepout (V-12, geometry); repeated numbers")
    return True


if __name__ == "__main__":
    self_test()
