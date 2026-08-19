import folium
import geopandas as gpd

# 1. GeoJSON file load karein
gdf = gpd.read_file('plot_30.geojson')

# 2. Plot ka Centroid (Latitude, Longitude) nikalein
centroid = gdf.geometry.centroid.iloc[0]
lat, lon = centroid.y, centroid.x

# 3. Interactive Map create karein (Plot ke location par center karke)
m = folium.Map(location=[lat, lon], zoom_start=18)

# 4. Satellite View / OpenStreetMap layer add karein
folium.GeoJson(
    gdf,
    name="Plot Boundary",
    style_function=lambda x: {
        'fillColor': '#ff7800',
        'color': '#000000',
        'weight': 2,
        'fillOpacity': 0.4,
    }
).add_to(m)

# 5. Centroid marker add karein
folium.Marker(
    location=[lat, lon],
    popup=f"Centroid<br>Lat: {lat:.6f}<br>Lon: {lon:.6f}",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# 6. Map ko HTML file me save karein
m.save("plot_map.html")
print("Map successfully saved as 'plot_map.html'. Open it in your browser!")