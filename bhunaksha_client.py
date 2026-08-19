"""
Real UP Bhunaksha client (public web backend)
"""
import requests
from pyproj import Transformer

BASE = "https://upbhunaksha.gov.in/bhunakshaserver"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://upbhunaksha.gov.in",
    "Referer": "https://upbhunaksha.gov.in/home",
    "User-Agent": "Mozilla/5.0 BhuDrishti/1.0",
}

# UTM zone 44N used by UP Bhunaksha tiles (EPSG:32644) → WGS84
TO_WGS84 = Transformer.from_crs("EPSG:32644", "EPSG:4326", always_xy=True)


def _post_form(path, data):
    r = requests.post(f"{BASE}/{path}", data=data, headers={
        **HEADERS,
        "Content-Type": "application/x-www-form-urlencoded",
    }, timeout=30)
    r.raise_for_status()
    return r.json()


def _post_json(path, payload):
    r = requests.post(f"{BASE}/{path}", json=payload, headers={
        **HEADERS,
        "Content-Type": "application/json",
    }, timeout=30)
    r.raise_for_status()
    return r.text if "plotinfo" in path.lower() or path.endswith("getPlotInfo") else r.json()


def list_districts():
    return _post_form("masterdata/levelvalue", {"level": 1, "codes": ""})


def list_tehsils(district_code):
    return _post_form("masterdata/levelvalue", {"level": 2, "codes": str(district_code)})


def list_villages(district_code, tehsil_code):
    # codes often need district+tehsil concatenation style used by portal
    code = f"{district_code}{tehsil_code}"
    return _post_form("masterdata/levelvalue", {"level": 3, "codes": code})


def build_gis_code(district_code, tehsil_code, village_code):
    """Portal style: district + tehsil + village digits joined."""
    return f"{district_code}{tehsil_code}{village_code}"


def get_plot_bbox(gis_code, plot_no):
    """
    Real plot extent from Bhunaksha (UTM meters).
    Returns dict: minx, miny, maxx, maxy, kide
    """
    r = requests.post(
        f"{BASE}/MapInfo/getPlotByPlotNo",
        params={"giscode": str(gis_code), "plotno": str(plot_no)},
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def get_plot_info_text(gis_code, plot_no):
    """Owner/area text info from Bhunaksha."""
    r = requests.post(
        f"{BASE}/MapInfo/getPlotInfo",
        json={"gisCode": str(gis_code), "plotNo": str(plot_no)},
        headers={**HEADERS, "Content-Type": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def bbox_to_latlon_ring(bbox):
    """
    Convert UTM bbox to closed ring of (lon, lat) corners for hashing/map.
    """
    minx, miny = float(bbox["minx"]), float(bbox["miny"])
    maxx, maxy = float(bbox["maxx"]), float(bbox["maxy"])
    corners_utm = [
        (minx, miny),
        (maxx, miny),
        (maxx, maxy),
        (minx, maxy),
        (minx, miny),  # close ring
    ]
    ring = []
    for x, y in corners_utm:
        lon, lat = TO_WGS84.transform(x, y)
        ring.append((lon, lat))
    return ring


def fetch_plot_real(district_code, tehsil_code, village_code, plot_no):
    """
    Main function for BhuDrishti:
    returns coords (lon,lat list), bbox, info_text, gis_code
    """
    gis_code = build_gis_code(district_code, tehsil_code, village_code)
    bbox = get_plot_bbox(gis_code, plot_no)
    if not bbox or "minx" not in bbox:
        raise ValueError(f"Plot not found on Bhunaksha for gis={gis_code}, plot={plot_no}")
    coords = bbox_to_latlon_ring(bbox)
    try:
        info = get_plot_info_text(gis_code, plot_no)
    except Exception:
        info = ""
    return {
        "gis_code": gis_code,
        "plot_no": str(plot_no),
        "bbox_utm": bbox,
        "coordinates": coords,  # list of (lon, lat)
        "info_text": info,
        "source": "UP Bhunaksha live API",
    }


if __name__ == "__main__":
    # Demo: Agra sample village from live portal
    # District 146, Tehsil 00766, Village 124649, Plot 1
    data = fetch_plot_real("146", "00766", "124649", "1")
    print("GIS:", data["gis_code"])
    print("BBox:", data["bbox_utm"])
    print("Coords (lon,lat):")
    for i, (lo, la) in enumerate(data["coordinates"], 1):
        print(f"  {i}. {la:.6f}, {lo:.6f}")
    print("Info:", data["info_text"][:300])