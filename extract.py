"""
extract.py — plot coordinates
Live mode: UP Bhunaksha APIs via bhunaksha_client
Fallback: sample plot (old demo)
"""

from bhunaksha_client import fetch_plot_real, list_districts, list_tehsils, list_villages


# Sample fallback (Prayagraj / Koraon / Koodar / 30) — old demo
SAMPLE_COORDS = [
    [82.0680, 25.0075],
    [82.0695, 25.0075],
    [82.0695, 25.0088],
    [82.0688, 25.0088],
    [82.0688, 25.0092],
    [82.0680, 25.0092],
    [82.0680, 25.0075],
]


def find_code_by_name(items, name):
    """Match Hindi/English name loosely in Bhunaksha list."""
    if not items or not name:
        return None
    name_l = str(name).strip().lower()
    for it in items:
        val = str(it.get("value", "")).strip().lower()
        code = str(it.get("code", "")).strip()
        if name_l == val or name_l in val or val in name_l:
            return code
    # try pure code match
    for it in items:
        if str(it.get("code", "")).strip() == str(name).strip():
            return str(it.get("code"))
    return None


def resolve_codes(district_name, tehsil_name, village_name):
    """
    Name → Bhunaksha codes
    Returns dict: district, tehsil, village  OR raises ValueError
    """
    districts = list_districts()
    d_code = find_code_by_name(districts, district_name)
    if not d_code:
        raise ValueError(f"District not found on Bhunaksha: {district_name}")

    tehsils = list_tehsils(d_code)
    t_code = find_code_by_name(tehsils, tehsil_name)
    if not t_code:
        raise ValueError(f"Tehsil not found: {tehsil_name}")

    villages = list_villages(d_code, t_code)
    v_code = find_code_by_name(villages, village_name)
    if not v_code:
        raise ValueError(f"Village not found: {village_name}")

    return {"district": d_code, "tehsil": t_code, "village": v_code}


def get_plot_coordinates(district, tehsil, village, plot_no, live=True, codes=None):
    """
    Returns list of [lon, lat] ring.

    live=True  → real Bhunaksha
    live=False → sample coords
    codes=dict optional if codes already known:
        {"district":"146","tehsil":"00766","village":"124649"}
    """
    if not live:
        return [list(p) for p in SAMPLE_COORDS]

    try:
        if not codes:
            codes = resolve_codes(district, tehsil, village)

        data = fetch_plot_real(
            codes["district"],
            codes["tehsil"],
            codes["village"],
            plot_no,
        )
        # fetch_plot_real returns [(lon,lat), ...]
        coords = [[float(lon), float(lat)] for lon, lat in data["coordinates"]]
        # stash extra info for callers that want it
        get_plot_coordinates.last_meta = {
            "gis_code": data.get("gis_code"),
            "bbox_utm": data.get("bbox_utm"),
            "info_text": data.get("info_text", ""),
            "source": data.get("source"),
        }
        return coords
    except Exception as e:
        print(f"[extract] Live Bhunaksha failed: {e}")
        print("[extract] Falling back to SAMPLE coords")
        get_plot_coordinates.last_meta = {"source": "sample_fallback", "error": str(e)}
        return [list(p) for p in SAMPLE_COORDS]


# default meta
get_plot_coordinates.last_meta = {}


if __name__ == "__main__":
    # Live test: Agra sample (known working on portal)
    print("=== LIVE test Agra plot 1 ===")
    coords = get_plot_coordinates(
        "आगरा", "आगरा", "अकबरपुर", "1",
        live=True,
        codes={"district": "146", "tehsil": "00766", "village": "124649"},
    )
    print("Vertices:")
    for i, (lo, la) in enumerate(coords, 1):
        print(f"  {i}. Lat={la}, Lon={lo}")
    print("Meta:", get_plot_coordinates.last_meta)

    print("\n=== SAMPLE fallback test ===")
    coords2 = get_plot_coordinates("Prayagraj", "Koraon", "Koodar", "30", live=False)
    for i, (lo, la) in enumerate(coords2, 1):
        print(f"  {i}. Lat={la}, Lon={lo}")