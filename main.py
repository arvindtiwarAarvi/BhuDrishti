from extract import get_plot_coordinates
from geo_utils import create_geodataframe, get_centroid, get_area_sqm, export_geojson
from fertility_water import estimate_fertility, detect_water_resources
from ai_report import generate_ai_report

try:
    from map_overlay import create_satellite_map
    HAS_MAP = True
except ImportError:
    HAS_MAP = False

try:
    from blockchain_module import lock_on_chain
    HAS_CHAIN = True
except ImportError:
    HAS_CHAIN = False


def analyze_plot(district, tehsil, village, plot_no):
    coords = get_plot_coordinates(district, tehsil, village, plot_no)

    gdf = create_geodataframe(coords, plot_no)
    area = get_area_sqm(gdf)
    centroid = get_centroid(gdf)
    geojson_file = export_geojson(gdf, f"plot_{plot_no}.geojson")

    map_file = None
    if HAS_MAP:
        try:
            map_file = create_satellite_map(coords, plot_no, f"plot_{plot_no}_map.html")
        except Exception as e:
            map_file = f"Map error: {e}"

    fertility = estimate_fertility(coords)
    water = detect_water_resources(coords)
    report = generate_ai_report(plot_no, fertility, water)

    chain = None
    if HAS_CHAIN:
        summary = report.get("summary", "") if isinstance(report, dict) else str(report)
        try:
            chain = lock_on_chain(district, tehsil, village, plot_no, coords, area, summary)
        except Exception as e:
            chain = {"error": str(e)}

    return {
        "plot_no": plot_no,
        "location": f"{village}, {tehsil}, {district}",
        "coordinates": coords,
        "centroid_latlon": centroid,
        "area_sqm": round(area, 2),
        "geojson": geojson_file,
        "map": map_file,
        "fertility": fertility,
        "water": water,
        "ai_report": report,
        "blockchain": chain,
    }


if __name__ == "__main__":
    result = analyze_plot("Prayagraj", "Koraon", "Koodar", "30")
    print("=" * 50)
    print("BhuDrishti — Full Analysis")
    print("=" * 50)
    print(f"Location : {result['location']}")
    print(f"Plot No  : {result['plot_no']}")
    print(f"Area     : {result['area_sqm']} sq.m")
    print(f"Centroid : {result['centroid_latlon']}")
    print(f"GeoJSON  : {result['geojson']}")
    print(f"Map      : {result['map']}")
    print("Fertility:", result["fertility"])
    print("Water    :", result["water"])
    print("AI Report:", result["ai_report"])
    print("Blockchain:", result["blockchain"])
    print("=" * 50)