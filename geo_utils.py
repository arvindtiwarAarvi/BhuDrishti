import geopandas as gpd
from shapely.geometry import Polygon

def create_geodataframe(coords, plot_no="30"):
    poly = Polygon(coords)
    if not poly.is_valid:
        poly = poly.buffer(0)
    gdf = gpd.GeoDataFrame(
        {"plot_no": [str(plot_no)]},
        geometry=[poly],
        crs="EPSG:4326"
    )
    return gdf

def get_centroid(gdf):
    # Project to UTM for accurate centroid, then back
    gdf_utm = gdf.to_crs(epsg=32644)
    c = gdf_utm.geometry.centroid.to_crs(epsg=4326).iloc[0]
    return c.y, c.x  # lat, lon

def get_area_sqm(gdf):
    gdf_utm = gdf.to_crs(epsg=32644)
    return float(gdf_utm.area.iloc[0])

def export_geojson(gdf, filename="plot.geojson"):
    gdf.to_file(filename, driver="GeoJSON")
    return filename

if __name__ == "__main__":
    from extract import get_plot_coordinates
    coords = get_plot_coordinates("Prayagraj", "Koraon", "Koodar", "30")
    gdf = create_geodataframe(coords, "30")
    lat, lon = get_centroid(gdf)
    area = get_area_sqm(gdf)
    export_geojson(gdf, "plot_30.geojson")
    print(f"Centroid: Lat={lat:.6f}, Lon={lon:.6f}")
    print(f"Area: {area:.2f} sq.m")
    print("GeoJSON saved: plot_30.geojson")
