import folium
from geo_utils import create_geodataframe, get_centroid

def create_satellite_map(coords, plot_no="30", output="plot_map.html"):
    """
    coords: list of (lon, lat)
    """
    gdf = create_geodataframe(coords, plot_no)
    lat, lon = get_centroid(gdf)

    # Folium needs [lat, lon]
    latlon_coords = [[lat_, lon_] for lon_, lat_ in coords]

    m = folium.Map(
        location=[lat, lon],
        zoom_start=18,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery"
    )

    folium.Polygon(
        locations=latlon_coords,
        color="red",
        weight=3,
        fill=True,
        fill_color="yellow",
        fill_opacity=0.3,
        popup=f"Plot {plot_no}"
    ).add_to(m)

    for i, (la, lo) in enumerate(latlon_coords[:-1]):
        folium.CircleMarker(
            location=[la, lo],
            radius=4,
            color="white",
            fill=True,
            fill_color="red",
            popup=f"V{i+1}: {la:.5f}, {lo:.5f}"
        ).add_to(m)

    m.save(output)
    return output


if __name__ == "__main__":
    from extract import get_plot_coordinates
    coords = get_plot_coordinates("Prayagraj", "Koraon", "Koodar", "30")
    path = create_satellite_map(coords, "30", "plot_30_map.html")
    print("Map saved:", path)