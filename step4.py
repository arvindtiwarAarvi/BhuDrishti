import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="BhuDrishti Dashboard", layout="wide")

st.title("🗺️ BhuDrishti : A discriptive Analysis")

# 1. GeoJSON File Load Karein
geojson_path = "plot_30.geojson"

try:
    gdf = gpd.read_file(geojson_path)
    
    # Accurate calculations ke liye UTM projection (India - Zone 44N)
    gdf_utm = gdf.to_crs(epsg=32644)
    exact_area = gdf_utm.geometry.area.iloc[0]
    
    centroid = gdf.geometry.centroid.iloc[0]
    lat, lon = centroid.y, centroid.x

    # 2. Key Metrics Display Karein
    col1, col2, col3 = st.columns(3)
    col1.metric("Latitude", f"{lat:.6f}")
    col2.metric("Longitude", f"{lon:.6f}")
    col3.metric("Calculated Area", f"{exact_area:.2f} sq.m")

    st.markdown("---")

    # 3. Folium Map Create Karein
    m = folium.Map(location=[lat, lon], zoom_start=18)
    
    # Tile layers (Satellite / Streets)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite', name='Google Satellite').add_to(m)
    
    # Plot polygon display
    folium.GeoJson(
        gdf,
        name="Plot Boundary",
        style_function=lambda x: {'fillColor': '#2b83ba', 'color': '#000000', 'weight': 2, 'fillOpacity': 0.5}
    ).add_to(m)

    # Centroid marker
    folium.Marker([lat, lon], popup="Centroid", icon=folium.Icon(color="red")).add_to(m)
    folium.LayerControl().add_to(m)

    # 4. Dashboard me Map render karein
    st_folium(m, width=1100, height=500)

except Exception as e:
    st.error(f"Error loading GeoJSON file: {e}")