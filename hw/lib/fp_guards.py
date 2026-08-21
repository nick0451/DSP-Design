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

    # G3 -- a shrunken SM8S land.
    _must_fire(lambda: assert_rated_land("ODSP12:SM8S_DO218AC", 14.0, 10.0, "D1"), "G3")
    assert_rated_land("ODSP12:SM8S_DO218AC", 15.30, 10.70, "D1")                 # control

    if verbose:
        print("  footprint guards: G1/G2/G3 negative tests ALL FIRED, controls passed "
              "(M9 satisfied)")
        print("  UNCOVERED, by design: pad-1 orientation -- no data-shaped test exists")
    return True


if __name__ == "__main__":
    self_test()
